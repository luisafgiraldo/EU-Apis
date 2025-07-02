import json
import requests

def process_documents(retry_count=2):
    # ------------------ Configuración ------------------
    VA_API_KEY = 'eXR5OWR3bHdibTkwenk3Z2lwb3B0OldYZ1hpZFQ2M01OZWE1VnBJcjBMaENRaWVYVTFvZlJk'
    headers = {"Authorization": f"Basic {VA_API_KEY}"}
    url = "https://api.va.eu-west-1.landing.ai/v1/tools/agentic-document-analysis"

    base_pdf_path = "fieldex/files"
    pdf_name = "PDF-id-cards.pdf"
    pdf_path = f"{base_pdf_path}/{pdf_name}"

    schema_name = "idcards-schema-def.json"
    base_schema_path = "fieldex/schemas"
    schema_path = f"{base_schema_path}/{schema_name}"

    # ------------------ Leer schema JSON ------------------
    with open(schema_path, "r") as file:
        schema = json.load(file)

    files = [
        ("pdf", (pdf_name, open(pdf_path, "rb"), "application/pdf")),
    ]
    payload = {"fields_schema": json.dumps(schema)}

    # ------------------ Hacer petición ------------------
    print("Enviando request a:", url)
    response = requests.post(url, headers=headers, files=files, data=payload)

    print("STATUS CODE:", response.status_code)
    try:
        response_json = response.json()
        print("RESPONSE JSON:", json.dumps(response_json, indent=2))
    except json.JSONDecodeError:
        print("ERROR: La respuesta no es un JSON válido.")
        print("RESPUESTA RAW:", response.text)
        raise

    if "data" not in response_json:
        print("ERROR: La clave 'data' no está presente en la respuesta.")
        raise KeyError("'data' key missing in API response")

    output_data = response_json["data"]

    # ------------------ Validar presencia de markdown y chunks ------------------
    if "markdown" not in output_data or "chunks" not in output_data:
        raise KeyError("La respuesta no contiene 'markdown' o 'chunks'.")

    print("\nResumen markdown del documento:")
    print(output_data["markdown"])

    chunks = output_data["chunks"]

    # ------------------ Contar ocurrencias de campos esperados ------------------
    field_counts = {
        "Name": 0,
        "ID number": 0,
        "Address": 0,
        "Restrictions": 0,
        "Date of birth": 0,
    }

    for chunk in chunks:
        text = chunk.get("text", "")
        for field in field_counts:
            if field in text:
                field_counts[field] += 1

    print("---------------------------------------------------------------")
    print("TEST RESULTS:")

    expected_count = 10
    discrepancies = []
    for field, count in field_counts.items():
        if count != expected_count:
            discrepancies.append(f"Field '{field}' contains {count} matches, expected {expected_count}.")

    if discrepancies:
        raise AssertionError("Discrepancies found in chunk field counts:\n" + "\n".join(discrepancies))

    print("All fields contain the expected number of values.")
    print("---------------------------------------------------------------")

# ------------------ Ejecutar con reintentos ------------------
retry_attempts = 0
max_retries = 1
while retry_attempts <= max_retries:
    try:
        process_documents()
        break
    except AssertionError as e:
        print(f"Intento {retry_attempts + 1} fallido con error:\n{e}")
        retry_attempts += 1
        if retry_attempts > max_retries:
            print("Se alcanzó el número máximo de reintentos. Saliendo.")
            raise
        else:
            print("Reintentando...")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        raise
