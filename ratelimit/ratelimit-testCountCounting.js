#!/usr/bin/env node
/* eslint-disable no-console */
const fs = require('fs');
const path = require('path');
// Parse command line arguments
const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i += 2) {
  const key = args[i].replace(/^-+/, ''); // Remove both single and double dashes
  const value = args[i + 1];
  if (key && value) {
    params[key] = value;
  }
}

// Set default values and parse arguments
const concurrency = 1; // Fixed to 1 for now
const tier = params.tier || 'staging';
const apiKey = params.apikey || 'OHYwZW8ydWoyYXVhZmRpazZzbzlqOmRCTDR0TVR1eFJ3SHVwU1dIVVNLSGVjRjllRWFFdnI2';
const rpm = parseInt(params.rpm) || 200; // Default to 60 requests per minute
const durationMinutes = parseInt(params.duration) || 2; // Default to 5 minutes
const TOTAL_REQUESTS = Math.ceil(rpm * durationMinutes); // Calculate total requests based on duration and RPM

// Add counters for statistics
let successfulRequests = 0;
let failedRequests = 0;
let startTime = null;
let requestsPerMinute = new Map(); // Track requests per minute
let failedRequestsPerMinute = new Map(); // Track failed requests per minute

// Set URL based on tier
const API_URL = {
  staging: 'https://api.va.staging.landing.ai/v1/tools/text-to-object-detection',
  production: 'https://api.va.landing.ai/v1/tools/text-to-object-detection',
  dev: 'https://api.va.dev.landing.ai/v1/tools/text-to-object-detection'
}[tier];

if (!API_URL) {
  console.error('Invalid tier. Must be one of: staging|dev|production');
  process.exit(1);
}

// Calculate number of iterations needed
const iterations = Math.ceil(TOTAL_REQUESTS / concurrency);

console.log(`Hitting endpoint: ${API_URL}`);
console.log(`Running with concurrency: ${concurrency}`);
console.log(`Using tier: ${tier}`);
console.log(`Duration: ${durationMinutes} minutes`);
console.log(`Target RPM: ${rpm}`);
console.log(`Total requests: ${TOTAL_REQUESTS}`);
console.log(`Number of iterations: ${iterations}`);
console.log('Press Ctrl+C to stop the test');

// Handle Ctrl+C gracefully
process.on('SIGINT', () => {
  console.log('\nStopping all requests...');
  process.exit(0);
});

async function makeRequest(requestNumber) {
  const requestStartTime = Date.now();
  if (!startTime) startTime = requestStartTime;

  try {
    const formData = new FormData();
    const pdfPath = path.join(__dirname, 'small-img.png');
    const pdfBuffer = fs.readFileSync(pdfPath);
    formData.append('image', new Blob([pdfBuffer], { type: 'image/png' }));


    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        Authorization: `Basic ${apiKey}`,
        accept: 'application/json',
        'X-Ratelimit-Test': 'true',
      },
      body: formData,
    });

    const endTime = Date.now();
    const elapsedTime = ((endTime - requestStartTime) / 1000).toFixed(3);
    const minuteNumber = Math.floor((endTime - startTime) / (60 * 1000));

    if (response.status !== 429) {
      successfulRequests++;
      requestsPerMinute.set(minuteNumber, (requestsPerMinute.get(minuteNumber) || 0) + 1);
      console.log(`✅ request ${requestNumber}: Status Code: ${response.status}, time: ${elapsedTime}s`);
    } else {
      failedRequests++;
      failedRequestsPerMinute.set(minuteNumber, (failedRequestsPerMinute.get(minuteNumber) || 0) + 1);
      console.error(`⚠️ request ${requestNumber}: Rate Limited (429), time: ${elapsedTime}s`);
    }
  } catch (error) {
    failedRequests++;
    const minuteNumber = Math.floor((Date.now() - startTime) / (60 * 1000));
    failedRequestsPerMinute.set(minuteNumber, (failedRequestsPerMinute.get(minuteNumber) || 0) + 1);
    console.error(`request ${requestNumber}: Error: ${error.message}`);
  }
}

async function runTest() {
  const delayBetweenRequests = (60 * 1000) / (rpm * concurrency);
  for (let i = 1; i <= iterations; i++) {
    const requests = [];
    for (let j = 1; j <= concurrency; j++) {
      const requestNumber = (i - 1) * concurrency + j;
      requests.push(makeRequest(requestNumber));
      await new Promise(resolve => setTimeout(resolve, delayBetweenRequests));
    }
    await Promise.all(requests);
  }

  // Calculate and display summary
  const endTime = Date.now();
  const totalTimeInMinutes = (endTime - startTime) / (1000 * 60);
  const actualRpm = successfulRequests / totalTimeInMinutes;

  console.log('\n=== Test Summary ===');
  console.log(`Total Requests: ${TOTAL_REQUESTS}`);
  console.log(`Successful Requests: ${successfulRequests}`);
  console.log(`Failed Requests: ${failedRequests}`);
  console.log(`Success Rate: ${((successfulRequests / TOTAL_REQUESTS) * 100).toFixed(2)}%`);
  console.log(`Total Time: ${totalTimeInMinutes.toFixed(2)} minutes`);
  console.log(`Actual Rate: ${actualRpm.toFixed(2)} requests/minute`);
  console.log(`Target Rate: ${rpm} requests/minute`);

  // Display per-minute breakdown
  console.log('\n=== Per-Minute Breakdown ===');
  const sortedMinutes = Array.from(new Set([...requestsPerMinute.keys(), ...failedRequestsPerMinute.keys()])).sort(
    (a, b) => a - b,
  );
  for (const minute of sortedMinutes) {
    const successful = requestsPerMinute.get(minute) || 0;
    const failed = failedRequestsPerMinute.get(minute) || 0;
    const total = successful + failed;
    console.log(
      // eslint-disable-next-line max-len
      `Minute ${minute + 1}: ${total} total requests (${successful} successful, ${failed} failed)`,
    );
  }
  console.log('==========================\n');
}

runTest().catch(console.error); 