#!/bin/bash

# Default concurrency to 1 if not provided
CONCURRENCY=${1:-1}
# Default tier to staging if not provided
TIER=${2:-staging}
# Default API key if not provide, this is junjie.guan@landing.ai's key in staging
API_KEY=${3:-"OWNrZXJkZ2w4N2huNDNud2VmanhiOmFJSnB0b29wakh0aHFxc1Z2cHNMTXNnMFZVSnJzb01r"}
TOTAL_REQUESTS=100

# Set URL based on tier
case $TIER in
  "staging")
    API_URL="https://api.va.staging.landing.ai/v1/tools/agentic-document-analysis"
    ;;
  "production")
    API_URL="https://api.va.landing.ai/v1/tools/agentic-document-analysis"
    ;;
  "dev")
    API_URL="https://api.va.dev.landing.ai/v1/tools/agentic-document-analysis"
    ;;
  *)
    echo "Invalid tier. Must be one of: staging|dev|production"
    exit 1
    ;;
esac

# Calculate number of iterations needed
ITERATIONS=$((TOTAL_REQUESTS / CONCURRENCY))

# Array to store background process PIDs
declare -a PIDS

# Function to cleanup background processes
cleanup() {
    echo -e "\nStopping all background processes..."
    for pid in "${PIDS[@]}"; do
        if kill -0 $pid 2>/dev/null; then
            kill $pid
        fi
    done
    exit 0
}

# Set up signal handler for Ctrl+C
trap cleanup SIGINT SIGTERM

echo "Running with concurrency: $CONCURRENCY"
echo "Using tier: $TIER"
echo "Total requests: $TOTAL_REQUESTS"
echo "Number of iterations: $ITERATIONS"
echo "Press Ctrl+C to stop the test"

for i in $(seq 1 $ITERATIONS); do
  # Launch concurrent requests
  for j in $(seq 1 $CONCURRENCY); do
    {
      start_time=$(date +%s.%g)
      response=$(curl -X 'POST' \
        "$API_URL" \
        -H "Authorization: Basic $API_KEY" \
        -H 'accept: application/json' \
        -H 'Content-Type: multipart/form-data' \
        -H 'X-Ratelimit-Test: true' \
        -F 'image=@./public/pdfs/Loan+Form.pdf;' -s -w "Status Code: %{http_code}" -o /dev/null)
      end_time=$(date +%s.%g)
      elapsed_time=$(printf "%.3f" $(echo "$end_time - $start_time" | bc))
      echo "request $(((i-1)*CONCURRENCY + j)): $response, time: ${elapsed_time}s"
    } &
    PIDS+=($!)  # Store the PID of the background process
  done

  wait  # Wait for all concurrent requests to complete
  sleep 1  # Optional: Add a small delay between batches
done