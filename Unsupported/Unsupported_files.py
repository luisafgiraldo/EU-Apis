import requests
import time
import os


url = "https://api.va.staging.landing.ai/v1/tools/agentic-document-analysis"
headers = {
    "Authorization": "Basic YW1ocTZseGltNzM1Z2txdmVpNWNzOnVqV0FvVEQ1eHlMSzNqVDA0Mkg0NzJ0RTVQU1ZFQ1JG",
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

        
        assert response.status_code == 500, f"Expected status 500, got {response.status_code} for file: {os.path.basename(filepath)}"
        assert json_data.get("message") == "Internal Server Error", f"Unexpected error message for file: {os.path.basename(filepath)}"

print("\n✅ All unsupported file tests passed successfully.")
