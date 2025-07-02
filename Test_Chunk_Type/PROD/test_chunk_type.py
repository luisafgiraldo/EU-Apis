import requests
import time
import io
import json
import re
import sys
from collections import Counter

url = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"
headers = {
    "Authorization": "Basic eGd1YWZsYXprYndtMDQ0Zm95N2I2OkZQb1p5bDduQVZtTk5yUUMxMEFISTlJelp1d3ZNUG5x"
}


start_time = time.time()
try:
    with open("Test_Chunk_Type/PDF/Marco_Aurelio_11Pages.pdf", "rb") as f:
        files = {"pdf": f}
        response = requests.post(url, files=files, headers=headers)
except FileNotFoundError:
    print("❌ PDF not found. Make sure it's at pdfs/Marco_Aurelio_Meditaciones_11_pages.pdf")
    sys.exit(1)

end_time = time.time()
elapsed_time = end_time - start_time

# --- Log temporal ---
log_buffer = io.StringIO()
log_buffer.write(f"Execution time: {elapsed_time:.2f} secs\n")
log_buffer.write(f"Response: {response.text}\n")

log_content = log_buffer.getvalue()

match = re.search(r'Response:\s*({.*})', log_content, re.DOTALL)
if not match:
    print("❌ No valid JSON content was found in the log.")
    sys.exit(1)

try:
    data = json.loads(match.group(1))

    accepted_types = {"marginalia", "text", "table", "figure"}
    grounding_pages = set()
    all_types_counter = Counter()
    invalid_types_found = set()

    chunks = data.get("data", {}).get("chunks", [])
    print(f"\n🔍 Total chunks received: {len(chunks)}")

    for i, chunk in enumerate(chunks):
        raw_chunk_type = chunk.get("chunk_type")
        if raw_chunk_type:
            chunk_type = raw_chunk_type.lower()
            all_types_counter[chunk_type] += 1
            if chunk_type not in accepted_types:
                invalid_types_found.add(chunk_type)
        else:
            print(f"⚠️ Chunk #{i} has no 'chunk_type': {json.dumps(chunk, indent=2)[:300]}...")

        for g in chunk.get("grounding", []):
            if "page" in g:
                grounding_pages.add(g["page"])

    print(f"\n⏱️ Execution time: {elapsed_time:.2f} secs")
    print(f"📄 Total amount of processed pages: {len(grounding_pages)}")
    print(f"Pages: {sorted(grounding_pages)}")

    print("\n📊 Chunk types found:")
    if all_types_counter:
        for t, count in all_types_counter.items():
            status = "✅ Accepted" if t in accepted_types else "❌ Invalid"
            print(f"  - {t}: {count} ({status})")
    else:
        print("⚠️ No chunk types were found.")

    
    assert len(grounding_pages) == 11, f"❌ Test FAILED: only {len(grounding_pages)} pages were found, expected 11."
    assert not invalid_types_found, f"❌ Test FAILED: found invalid chunk types: {sorted(invalid_types_found)}"

    print("\n✅ Test PASSED: All chunk types are valid and 11 pages were processed.")

except json.JSONDecodeError as e:
    print("❌ JSON decode error:", e)
    sys.exit(1)
except AssertionError as e:
    print(str(e))
    sys.exit(1)

#------------------------------------------------------------
#ACCOUNT CREDENTIALS
#------------------------------------------------------------
#username: luisa.aristizabal.external+ADE@landing.ai
#psswd: Luisa2336097