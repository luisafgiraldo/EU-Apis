import requests
import time
import sys  # Import the sys module

url = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"

# Ensure to uncomment the specific file you want to send in the request
files = {
    # OR, for PDF
    "pdf": open(r"zero-credits/pdfs/infographic-1pg.pdf", "rb")
}

headers = {
    #Zero-credits
    "Authorization": "Basic aXJrZWRnb2UxdjFjb2s2M3BweXRkOklSTk9EYUNYa2pJbVFBaXZxNW43bG55NDdQSHdVdVJ4",
}

# Record the start time
start_time = time.time()

# Make the request
response = requests.post(url, files=files, headers=headers)

# Record the end time
end_time = time.time()

# Calculate the duration
duration_seconds = end_time - start_time

# Convert the duration to minutes and seconds
minutes = int(duration_seconds // 60)
seconds = duration_seconds % 60

test_passed = False

try:
    response_json = response.json()
    print(response_json)
    # Assert to check the status code and the specific error message
    assert response.status_code == 402, f"Expected status code 402, got {response.status_code}"
    assert response_json.get('error') == "Payment Required. User balance is insufficient.", "Error message does not match expected."
    test_passed = True
except ValueError:  # Includes simplejson.decoder.JSONDecodeError
    print("Response content is not valid JSON")
    test_passed = False
except AssertionError as e:
    print(f"Assertion Error: {e}")
    test_passed = False

print("----------------------------------------------------------------")
print(f"REPORT")
print(f"Status Code: {response.status_code}")
print(f"Request duration: {minutes} minutes and {seconds:.3f} seconds")
if test_passed:
    print("Test PASSED ✅, user was shown this error message: '"+response_json.get('error')+"'" )
else:
    print(f"Test FAILED ❌. Actual status code received was {response.status_code}")
print("----------------------------------------------------------------")

# Close the file objects to free up system resources
for file in files.values():
    file.close()

# Exit script with non-zero exit code if test failed
if not test_passed:
    sys.exit(1)  # Exit with a status code of 1, indicating failure




#------------------------------------------------------------
#ACCOUNT CREDENTIALS
#------------------------------------------------------------
#username: internal.qatest+tier3-0credits@landing.ai
#psswd: rmb@pct0gnc2PYG9tza