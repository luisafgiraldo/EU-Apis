import requests
import pandas as pd
import utils as u


def create(url: str, image_path: str, prompt: str, api_key: str):
    querystring = {"timeout": "300"}

    # Crear el payload
    payload = {"image": u.transformer(image_path), "prompt": prompt}

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {api_key}",
    }

    try:
        # Enviar solicitud POST
        response = requests.post(url, json=payload, headers=headers, params=querystring)

        # Comprobación del response_data
        if response.status_code == 200:
            response_data = response.json()

            # Procesar datos
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
                    + "============================== 1 passed Countgd.py =============================="
                    + "\x1b[0m"
                )
                return df
            else:
                print("Error: 'data' key not found in response.")
                print(
                    f"\033[31m"
                    + "============================== 1 failed Countgd.py =============================="
                    + "\x1b[0m"
                )

                return pd.DataFrame()  # DataFrame vacío
        else:
            print(f"Error {response.status_code}: {response.text}")
            print(
                f"\033[31m"
                + "============================== 1 failed Countgd.py =============================="
                + "\x1b[0m"
            )
            return pd.DataFrame()  # DataFrame vacío en caso de error
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        print(
            f"\033[31m"
            + "============================== 1 failed Countgd.py =============================="
            + "\x1b[0m"
        )

        return pd.DataFrame()  # DataFrame vacío en caso de error
