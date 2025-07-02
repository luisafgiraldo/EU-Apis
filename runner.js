const { execSync } = require('child_process');
const fs = require('fs');

try {
  const output1 = execSync('node ratelimit/ratelimit-testADE-Tier1.js --tier staging --rpm 25 --duration 3', { 
    encoding: 'utf-8',
    stdio: ['pipe', 'pipe', 'pipe'], // stdin, stdout, stderr pipes activados
  });

  const output2 = execSync('node ratelimit/ratelimit-testADE-Tier2.js --tier staging --rpm 40 --duration 3', { encoding: 'utf-8' });
  fs.writeFileSync('ADE-Tier2.txt', output2);

  const output3 = execSync('node ratelimit/ratelimit-testADE-Tier3.js --tier staging --rpm 80 --duration 3', { encoding: 'utf-8' });
  fs.writeFileSync('ADE-Tier3.txt', output3);

  const output4 = execSync('node ratelimit/ratelimit-testAOD.js --tier staging --rpm 25 --duration 3', { encoding: 'utf-8' });
  fs.writeFileSync('AOD.txt', output4);

  //const output5 = execSync('node ratelimit/ratelimit-testSam2.js --tier staging --rpm 100 --duration 3', { encoding: 'utf-8' });
  //fs.writeFileSync('Sam2.txt', output5);

  
} catch (error) {
  console.error('One of the scripts failed:', error);
  process.exit(1);
}
