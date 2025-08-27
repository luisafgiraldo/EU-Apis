import requests
import time
import os


url = "https://api.va.eu-west-1.landing.ai/v1/tools/agentic-document-analysis"
headers = {
    "Authorization": "Basic bHU4ZXlraHBjeWE2NmpjN2YxY2M4OjVNRlpramdpTzB1TVRIV0FnanVqcTNqVE5VYVlLSGh4",
}


unsupported_files = [
    "Unsupported/Files/presentation.pptx",
    "Unsupported/Files/Report_1.avif",
    "Unsupported/Files/report.docx",
    "Unsupported/Files/Sheet-ODS.ods",
    "Unsupported/Files/ThirstyData_Site.heic",
    "Unsupported/Files/XLS.xlsx",
]

field_name = "image" 


for filepath in unsupported_files:
    print(f"\nTesting file: {filepath}")
    with open(filepath, "rb") as file:
        files = {field_name: file}
        
        start_time = time.time()
        response = requests.post(url, files=files, headers=headers)
        end_time = time.time()
        
        duration_seconds = end_time - start_time
        minutes = int(duration_seconds // 60)
        seconds = duration_seconds % 60
        
        print(f"Status Code: {response.status_code}")
        try:
            json_data = response.json()
            print(json_data)
        except ValueError:
            json_data = {"message": "Invalid JSON"}
            print("Response content is not valid JSON")
        
        print(f"Request duration: {minutes} minutes and {seconds:.3f} seconds")

        
        assert response.status_code == 422, f"Expected status 422, got {response.status_code} for file: {os.path.basename(filepath)}"
        assert json_data.get("message") == "Failed to open image. Ensure it is a valid image file.", (f"❌ Unexpected error message for file: {os.path.basename(filepath)} - Got: {json_data.get('message')}")


print("\n✅ All unsupported file tests passed successfully.")
