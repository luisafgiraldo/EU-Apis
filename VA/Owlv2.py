import requests
import utils as u
import json
import pandas as pd

def create(url: str, image_path: str, prompt: str, api_key: str):
    querystring = {"timeout": "300"}

    # Crear el payload con "prompts" como una lista
    payload = {
        "image": u.transformer(image_path),
        "prompts": [prompt],  # Cambiado a lista de un solo elemento
        "confidence": 0,
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {api_key}",
    }

    # Enviar solicitud POST
    response = requests.post(url, json=payload, headers=headers, params=querystring)

    # Comprobación del response_data
    if response.status_code == 200:
        # Imprimir el JSON completo en un formato legible
        response_data = response.json()
        print("Response Data (Formato JSON legible):")
        print(json.dumps(response_data, indent=4))

        # Verificar las claves en response_data
        print("\nClaves en Response Data:", response_data.keys())

        # Ejemplo de acceso a campos específicos si existen
        if "data" in response_data:
            processed_data = []
            for item in response_data["data"]:
                label = item.get("label", "No label")
                score = item.get("score", None)
                bbox = item.get("bbox", [])

                # Validación de campos
                has_label = label != "No label"
                has_score = score is not None
                has_bbox = bool(bbox)

                processed_data.append(
                    {
                        "Label": label,
                        "Score": score,
                        "BBox": bbox,
                        "Has Label": has_label,
                        "Has Score": has_score,
                        "Has BBox": has_bbox,
                    }
                )

            # Crear el DataFrame
            df = pd.DataFrame(processed_data)
            print(df)
            print(
                "\033[32m"
                + "============================== 1 passed Owlv2.py =============================="
                + "\x1b[0m"
            )
    else:
        response_data = response.json()
        print(f"Error {response.status_code}:")
        print(json.dumps(response_data, indent=4))
        df = pd.DataFrame()
        print(
            f"\033[31m"
            + "============================== 1 failed Owlv2.py =============================="
            + "\x1b[0m"
        )
    return df
