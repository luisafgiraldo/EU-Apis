#!/bin/bash

API_KEY=aGhqY25qMjA3c29wMHRpOGtwenN4Olo5MXhtNzFsVEZMUFRrTHp3Z09yWG5DbWdtNjVQRnE5
PARALLEL_REQUESTS=100
TOTAL_REQUESTS=100
STATUS_LOG="status_codes.log"

# Ensure the log file is empty
> "$STATUS_LOG"

process_request() {
  local i=$1
  echo "Request $i: start"
  start_time=$(date +%s.%N)
  response=$(curl -X 'POST' \
    'https://api.va.landing.ai/v1/tools/agentic-object-detection' \
    -H "Authorization: Basic $API_KEY" \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F "prompts=word" \
    -F 'image=@./small-img.png;' -s -w "%{http_code}\n" -o /dev/null)
  echo "$response" >> "$STATUS_LOG"
  end_time=$(date +%s.%N)
  elapsed_time=$(echo "$end_time - $start_time" | bc)
  
  echo "Request $i: end Status Code: $response ($elapsed_time seconds)"
}

export -f process_request
export API_KEY
export STATUS_LOG

# Capture the start time of the test
test_start_time=$(date +%s.%N)

for ((i=1; i<=TOTAL_REQUESTS; i++)); do
  # Start process in background
  bash -c "process_request $i" &

  # If we've reached our parallelism limit or the last request, wait
  if (( i % PARALLEL_REQUESTS == 0 )) || (( i == TOTAL_REQUESTS )); then
    wait # Wait for all background processes to complete
  fi
done

# Capture the end time of the test
test_end_time=$(date +%s.%N)

# Once all requests are done, count and display the occurrences of each status code
awk '{count[$1]++} END {for (code in count) print "Count of " code " responses: " count[code]}' "$STATUS_LOG"

# Calculate and display the total duration of the test
test_duration=$(echo "$test_end_time - $test_start_time" | bc)
echo "Total test duration: $test_duration seconds"