import requests
import pandas as pd
import utils as u


def create(url: str, image_path: str, prompt: str, api_key: str):
    querystring = {"timeout": "300"}

    # Enviar la imagen como archivo binario y el prompt como texto
    files = {"image": open(image_path, "rb")}
    data = {"prompt": prompt}

    headers = {
        "Authorization": f"Basic {api_key}"
    }

    try:
        response = requests.post(url, files=files, data=data, headers=headers, params=querystring)

        if response.status_code == 200:
            response_data = response.json()

            # Procesamiento de respuesta si aplica
            if isinstance(response_data, dict):
                print(response_data)
                print(
                    "\033[32m"
                    + "============================== 1 passed IXC25.py =============================="
                    + "\x1b[0m"
                )
                return pd.DataFrame([response_data])  # Lo envolvemos en un DataFrame por consistencia
            else:
                print("Error: respuesta inesperada.")
        else:
            print(f"Error {response.status_code}: {response.text}")

        print(
            f"\033[31m"
            + "============================== 1 failed IXC25  Image VQA.py =============================="
            + "\x1b[0m"
        )
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        print(
            f"\033[31m"
            + "============================== 1 failed IXC25 Image VQA.py =============================="
            + "\x1b[0m"
        )
        return pd.DataFrame()
