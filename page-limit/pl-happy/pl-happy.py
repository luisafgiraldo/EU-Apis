import requests
import time
import io
import json
import re
import sys  # Import sys for exiting with a status code

url = "https://api.va.staging.landing.ai/v1/tools/agentic-document-analysis"
headers = {
    "Authorization": "Basic eTh6ZG9jcnV3aHhwb20wdHdoNDJ0OlplQ00ydTdsSVBTUG1zQW1JOG5BVHRiY3pTamE5eEx4"
}
start_time = time.time()
with open(r"page-limit/pdfs/Marco_Aurelio_Meditaciones_100_pages.pdf", "rb") as f:
    files = {"pdf": f}
    response = requests.post(url, files=files, headers=headers)
end_time = time.time()
elapsed_time = end_time - start_time

# Create a temporary log
log_buffer = io.StringIO()
log_buffer.write(f"Execution time: {elapsed_time:.2f} secs\n")
log_buffer.write(f"Response: {response.text}\n")

# Reading from a temporary log
log_content = log_buffer.getvalue()

# Extracting JSON from the line that contains "Response: "
match = re.search(r'Response:\s*({.*})', log_content, re.DOTALL)
if not match:
    print("❌ No valid JSON content was found in the log.")
    sys.exit(1)  # Exit with a non-zero status code to indicate failure
else:
    try:
        data = json.loads(match.group(1))
        grounding_pages = set()
        # Navigate through the chunks and extract 'page'
        for chunk in data.get("data", {}).get("chunks", []):
            for g in chunk.get("grounding", []):
                if "page" in g:
                    grounding_pages.add(g["page"])
        print(f"✅ Total amount of processed pages: {len(grounding_pages)}")
        print(f"Pages: {sorted(grounding_pages)}")
        if len(grounding_pages) < 100:
            raise AssertionError(f"❌ Test FAILED: only {len(grounding_pages)} pages were found, while 100 pages were expected.")
    except json.JSONDecodeError as e:
        print("❌ JSON decodification error:", e)
        sys.exit(1)  # Exit with a non-zero status code to indicate failure
    except AssertionError as e:
        print(str(e))
        sys.exit(1)  # Exit with a non-zero status code to indicate failure

        
        
#-------------------------------------------------------------------------------------------------
#account_credentials
#-------------------------------------------------------------------------------------------------
#username: internal.qatest+tier3-plhappy@landing.ai
#password: rmb@pct0gnc2PYG9tza
#-------------------------------------------------------------------------------------------------