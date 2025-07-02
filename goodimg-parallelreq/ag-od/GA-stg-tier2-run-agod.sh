#!/bin/bash

API_KEY="M3c0a3VzMWthb284dnF4d2pzOTdjOkdKZ2ZvaEl4MERuVGdKSkJ3QXhSbGgwYTI5c3FjWGxx"
PARALLEL_REQUESTS=100
TOTAL_REQUESTS=100
STATUS_LOG="status_codes.log"
OUTPUT_FILE="goodimg-parallelreq/reports/AOD-T2_goodimg_report.txt"
TEMP_REPORT="temp_report.txt"

# Ensure the log and output files are empty
> "$STATUS_LOG"
> "$OUTPUT_FILE"
> "$TEMP_REPORT"

process_request() {
  local i=$1
  local request_log="request_${i}_log.tmp"
  echo "Request $i: start" > "$request_log"
  start_time=$(date +%s.%N)
  response=$(curl -X 'POST' \
    'https://api.va.staging.landing.ai/v1/tools/agentic-object-detection' \
    -H "Authorization: Basic $API_KEY" \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F "prompts=word" \
    -F 'image=@./goodimg-parallelreq/ag-od/small-img.png;' -s -w "%{http_code}\n" -o /dev/null)
  echo "$response" >> "$STATUS_LOG"
  end_time=$(date +%s.%N)
  elapsed_time=$(echo "$end_time - $start_time" | bc)
  
  echo "Request $i: end Status Code: $response ($elapsed_time seconds)" >> "$request_log"
  cat "$request_log" | tee -a "$OUTPUT_FILE"
  rm "$request_log"  # Clean up temporary log file
}

export -f process_request
export API_KEY
export STATUS_LOG
export OUTPUT_FILE

# Capture the start time of the test
test_start_time=$(date +%s.%N)

for ((i=1; i<=TOTAL_REQUESTS; i++)); do
  # Start process in background
  (process_request $i) &

  # If we've reached our parallelism limit or the last request, wait
  if (( i % PARALLEL_REQUESTS == 0 )) || (( i == TOTAL_REQUESTS )); then
    wait # Wait for all background processes to complete
  fi
done

# Capture the end time of the test
test_end_time=$(date +%s.%N)

# Generate the final report content and display it in the console
{
    echo -e "--------------------------------\nAOD-T2-GOOD_IMG_TEST-Report:"
    awk '{count[$1]++} END {for (code in count) print "Count of " code " responses: " count[code]}' "$STATUS_LOG"
    test_duration=$(echo "$test_end_time - $test_start_time" | bc)
    echo "Total test duration: $test_duration seconds"
    echo "--------------------------------"
    echo ""
} | tee "$TEMP_REPORT"

# Since the final report is already printed to the console, 
# we directly prepend the report to the beginning of the output file.
cat "$TEMP_REPORT" "$OUTPUT_FILE" > temp && mv temp "$OUTPUT_FILE"

# Clean up the temporary report file
rm "$TEMP_REPORT"




#-------------------------------------------------------------------------------------------------
#account_credentials
#-------------------------------------------------------------------------------------------------
#username: internal.qatest+tier2-goodimg@landing.ai
#password: rmb@pct0gnc2PYG9tza
#-------------------------------------------------------------------------------------------------