import json
import requests

def process_documents(retry_count=2):
    VA_API_KEY = 'NXFlNjB3NDJsb2ZzZjljb3Zhc2lmOmVrWmdLQmlRY1ZsTUNhRlVYbnE5WU94MWhVZ3p4OUZa'
    headers = {"Authorization": f"Basic {VA_API_KEY}"}
    url = "https://api.va.staging.landing.ai/v1/tools/agentic-document-analysis"

    base_pdf_path = r"fieldex/files"
    pdf_name = "PDF-id-cards.pdf"
    pdf_path = f"{base_pdf_path}/{pdf_name}"

    schema_name = "idcards-schema-def.json"
    base_schema_path = "fieldex/schemas"
    schema_path = f"{base_schema_path}/{schema_name}"

    with open(schema_path, "r") as file:
        schema = json.load(file)

    files = [
        ("pdf", (pdf_name, open(pdf_path, "rb"), "application/pdf")),
    ]

    payload = {"fields_schema": json.dumps(schema)}

    response = requests.request("POST", url, headers=headers, files=files, data=payload)

    output_data = response.json()["data"]
    extracted_info = output_data["extracted_schema"]
    print(extracted_info)

    # Initialize a dictionary to hold counts for each field
    field_counts = {
        "Name": 0,
        "ID number": 0,
        "Address": 0,
        "Restrictions": 0,
        "Date of birth": 0,
    }

    # Assuming the extracted data follows the new schema and the information is under 'values'
    for item in extracted_info.get("values", []):
        for field in field_counts.keys():
            if field in item:
                field_counts[field] += 1

    print("---------------------------------------------------------------")
    print("TEST RESULTS:")
    # Initialize a list to hold discrepancy reports
    discrepancies = []

    expected_count = 10
    for field, count in field_counts.items():
        if count != expected_count:
            discrepancies.append(f"Field '{field}' contains {count} values, expected {expected_count}.")

    # Check if there were any discrepancies
    if discrepancies:
        # Join all discrepancy reports into a single string message
        discrepancy_message = "\n".join(discrepancies)
        # Raise an assertion error with the comprehensive discrepancy message
        raise AssertionError(f"Discrepancies found in field counts:\n{discrepancy_message}")

    print("All fields contain the expected number of values.")
    print("---------------------------------------------------------------")


# Main execution with retry logic
retry_attempts = 0
max_retries = 1  # Set to 1 retry after the initial attempt
while retry_attempts <= max_retries:
    try:
        process_documents()
        break  # Success, exit the loop
    except AssertionError as e:
        print(f"Attempt {retry_attempts + 1} failed with error: {e}")
        retry_attempts += 1
        if retry_attempts > max_retries:
            print("Max retry attempts reached. Exiting.")
            raise  # Re-raise the last exception after max retries
        else:
            print("Retrying...")


#------------------------------------------------------------------------------------------------------
#ORG CREDENTIALS in STG
#username: daniel.giraldo.external+fieldextest@landing.ai
#psswd: Paletaforma11%
#------------------------------------------------------------------------------------------------------
