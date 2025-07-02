import requests
import time

pdf_path = "page-limit/pdfs/Marco_Aurelio_Meditaciones_101_pages.pdf"

tiers = [
    {
        "name": "tier1",
        "api_key": "d2tmdnJ1em9zODBmbWxycG52M3RkOnVKeTJIeGxtU2VnY0FiSFJYUk8wSDk2RDBjSE9TdDVV",
        "expected_status": 422,
        "expected_message": "PDF must not exceed 50 pages."
    },
    {
        "name": "tier2",
        "api_key": "cHZvcnduNGgzbXoxOGFpZnFqaWV0OlQ2OWRvRnJLcWFnSndzaGo4NmQ0STJNeXlwMG5zNWVN",
        "expected_status": 422,
        "expected_message": "PDF must not exceed 50 pages."
    },
    {
        "name": "tier3",
        "api_key": "ZHh2dzF4Nnk3bm9ubGlyd3ZzaHpnOjRYM2Rrb0VLdEFvN1JtRkN2RWhkWENZNlFXcTlqbXBr",
        "expected_status": 422,
        "expected_message": "PDF must not exceed 100 pages."
    }
]

url = "https://api.va.landing.ai/v1/tools/agentic-document-analysis"

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


#-------------------------------------------------------------------------------------------------
#CREDENTIALS TO ACCOUNTS USED IN THIS TEST IN PROD
#-------------------------------------------------------------------------------------------------
#T1-PROD:
#username: internal.qatest+tier1-plunhappy@landing.ai
#apikey: d2tmdnJ1em9zODBmbWxycG52M3RkOnVKeTJIeGxtU2VnY0FiSFJYUk8wSDk2RDBjSE9TdDVV
#psswd: rmb@pct0gnc2PYG9tza
#T2-PROD:
#username: internal.qatest+tier2-plunhappy@landing.ai
#apikey: cHZvcnduNGgzbXoxOGFpZnFqaWV0OlQ2OWRvRnJLcWFnSndzaGo4NmQ0STJNeXlwMG5zNWVN
#psswd: rmb@pct0gnc2PYG9tza
#T3-PROD:
#username: internal.qatest+tier3-plunhappy@landing.ai
#apikey: ZHh2dzF4Nnk3bm9ubGlyd3ZzaHpnOjRYM2Rrb0VLdEFvN1JtRkN2RWhkWENZNlFXcTlqbXBr
#psswd: rmb@pct0gnc2PYG9tza
#-------------------------------------------------------------------------------------------------
