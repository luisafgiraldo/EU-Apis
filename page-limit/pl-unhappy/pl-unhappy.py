import requests
import time

pdf_path = "page-limit/pdfs/Marco_Aurelio_Meditaciones_101_pages.pdf"

tiers = [
    {
        "name": "tier1",
        "api_key": "cXc3OHczMmhkMmY3a3QxaHJrc3lhOlVqUzM0U3lrM1BqczlKN0tJMVNxRnJFOExhcmpWbHM1",
        "expected_status": 422,
        "expected_message": "PDF must not exceed 50 pages."
    },
    {
        "name": "tier2",
        "api_key": "eTcyM3p2eHloMTQ2Y25xdmg0YXl6OlV0cnAxdFVNVGk1VUpKcUUzMzNqNFZMSmZRRjYwTnRu",
        "expected_status": 422,
        "expected_message": "PDF must not exceed 50 pages."
    },
    {
        "name": "tier3",
        "api_key": "YW1ocTZseGltNzM1Z2txdmVpNWNzOnVqV0FvVEQ1eHlMSzNqVDA0Mkg0NzJ0RTVQU1ZFQ1JG",
        "expected_status": 422,
        "expected_message": "PDF must not exceed 100 pages."
    }
]

url = "https://api.va.staging.landing.ai/v1/tools/agentic-document-analysis"

results = []

for tier in tiers:
    print(f"\n🔍 Testing {tier['name']}")
    headers = {
        "Authorization": f"Basic {tier['api_key']}"
    }

    start_time = time.time()

    with open(pdf_path, "rb") as f:
        files = {"pdf": f}
        response = requests.post(url, files=files, headers=headers)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)
    print(f"⏱ Execution time: {elapsed_time:.2f} seconds")

    try:
        assert response.status_code == tier["expected_status"], f"Unexpected status code: {response.status_code}"
        assert tier["expected_message"] in response.text, f"Unexpected error message: {response.text}"
        print(f"✅ {tier['name']} passed all validations.")
        results.append((tier['name'], "PASSED"))
    except AssertionError as e:
        print(f"❌ {tier['name']} failed: {e}")
        results.append((tier['name'], "FAILED"))

print("\n📋 Test Summary:")
any_failed = False
for name, result in results:
    print(f"- {name}: {result}")
    if result == "FAILED":
        any_failed = True

if any_failed:
    exit(1)  # Mark the workflow as failed
