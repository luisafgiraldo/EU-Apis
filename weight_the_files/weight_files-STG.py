import requests
import time
import os

url = "https://api.va.staging.landing.ai/v1/tools/agentic-document-analysis"

headers = {
    "Authorization": "Basic YW1ocTZseGltNzM1Z2txdmVpNWNzOnVqV0FvVEQ1eHlMSzNqVDA0Mkg0NzJ0RTVQU1ZFQ1JG",
}


FAKE_LARGE_IMAGE_PATH = "simulated_oversized_image.png"


test_files = [
    {
        "type": "image",
        "path": "weight_the_files/pdf/Adobe Express - file.png",
        "expected_status": 200,
    },
    {
        "type": "pdf",
        "path": "weight_the_files/pdf/Document Chunk Classification.pdf",
        "expected_status": 200,
    },
    {
        "type": "image",
        "path": "weight_the_files/pdf/accident_new.png",
        "expected_status": 200,
    },
    {
        "type": "image",
        "path": FAKE_LARGE_IMAGE_PATH,
        "expected_status": 422,
        "expected_message": "Image size should be less than 50MB."
    },
]

results_summary = []

if not os.path.exists(FAKE_LARGE_IMAGE_PATH):
    print(f"🛠️ Creating fake image: {FAKE_LARGE_IMAGE_PATH} (51MB)")
    with open(FAKE_LARGE_IMAGE_PATH, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"0" * (51 * 1024 * 1024))  # 51MB fake PNG content

for test_file in test_files:
    file_type = test_file["type"]
    file_path = test_file["path"]
    expected_status = test_file["expected_status"]
    expected_message = test_file.get("expected_message")

    print(f"\n🔍 Testing file: {os.path.basename(file_path)} (Expecting status {expected_status})")

    with open(file_path, "rb") as f:
        files = {file_type: f}

        start_time = time.time()
        response = requests.post(url, files=files, headers=headers)
        end_time = time.time()

        duration = end_time - start_time
        minutes = int(duration // 60)
        seconds = duration % 60

        print(f"Status Code: {response.status_code}")
        try:
            response_json = response.json()
            print(response_json)
        except ValueError:
            response_json = None
            print("Response content is not valid JSON")

        print(f"⏱️ Request duration: {minutes} minutes and {seconds:.3f} seconds")

        
        assert response.status_code == expected_status, (
            f"❌ Expected status {expected_status}, but got {response.status_code} for file {file_path}"
        )

        
        if expected_status == 422 and expected_message:
            assert response_json is not None, "❌ Expected JSON response but got None."
            assert "message" in response_json, "❌ Response JSON does not contain 'message' key."
            assert response_json["message"] == expected_message, (
                f"❌ Expected message '{expected_message}', but got '{response_json['message']}'"
            )

      
        results_summary.append({
            "file": os.path.basename(file_path),
            "expected": expected_status,
            "actual": response.status_code,
            "status": "✅ Passed" if response.status_code == expected_status else "❌ Failed"
        })


print("\n📋 Test Summary:")
for result in results_summary:
    print(f"- {result['file']}: Expected {result['expected']}, Got {result['actual']} → {result['status']}")


if os.path.exists(FAKE_LARGE_IMAGE_PATH):
    os.remove(FAKE_LARGE_IMAGE_PATH)
    print(f"\n🧹 Deleted simulated file: {FAKE_LARGE_IMAGE_PATH}")
