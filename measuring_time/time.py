import requests
import time
import os

url = "https://api.va.staging.landing.ai/v1/tools/agentic-document-analysis"

headers = {
    "Authorization": "Basic YW1ocTZseGltNzM1Z2txdmVpNWNzOnVqV0FvVEQ1eHlMSzNqVDA0Mkg0NzJ0RTVQU1ZFQ1JG",
}

# Lista de archivos (imágenes + PDF)
file_paths = [
    "measuring_time/pdf/1966 Corvette.jpeg",
    "measuring_time/pdf/Camaro Sport Coupe .jpeg",
    "measuring_time/pdf/pdf.pdf"
]

summary = []
errors = []
num_requests_per_file = 3

for file_path in file_paths:
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext in [".jpeg", ".jpg", ".png"]:
        file_key = "image"
    elif file_ext == ".pdf":
        file_key = "pdf"
    else:
        print(f"❌ Unsupported file type for {file_name}, skipping.")
        continue
    
    for i in range(1, num_requests_per_file + 1):
        with open(file_path, "rb") as f:
            files = {file_key: f}

            start_time = time.time()
            response = requests.post(url, files=files, headers=headers)
            duration = time.time() - start_time

            status_code = response.status_code

            if status_code != 200:
                errors.append(f"{file_name} | Run {i} failed with status code {status_code}")

            summary.append({
                "file": file_name,
                "run": i,
                "status": status_code,
                "time": f"{duration:.3f} seconds"
            })

# Summary 
print("\n===== TEST SUMMARY =====")
for result in summary:
    print(f"File: {result['file']} | Run: {result['run']} | Status: {result['status']} | Time: {result['time']}")
print("=========================")

if errors:
    print("\n❌ Some tests failed:")
    for e in errors:
        print(f"- {e}")
    raise Exception("One or more requests failed.")
else:
    print("\n✅ All requests succeeded.")
