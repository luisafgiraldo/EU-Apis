import requests
import pandas as pd
import utils as u


# def create(url: str, video_path: str, prompts: str):
#     querystring = {"timeout": "300"}
#     files = [("video", open(video_path, "rb"))]
#     # Crear el payload
#     payload = {
#         "prompts": [prompts],
#         "model": "owlv2",
#     }

#     headers = {
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Accept": "application/json",
#     }

#     try:
#         # Enviar solicitud POST
#         response = requests.post(
#             url, headers=headers, data=payload, files=files, params=querystring
#         )

#         # Comprobación del response_data
#         if response.status_code == 200:
#             response_data = response.json()
#             print(response_data)
#         else:
#             print(f"Error {response.status_code}: {response.text}")
#             return pd.DataFrame()  # DataFrame vacío en caso de error
#     except requests.exceptions.RequestException as e:
#         print(f"Request error: {e}")
#         return pd.DataFrame()  # DataFrame vacío en caso de error


def create(url: str, video_path: str, prompts: str, api_key: str):
    # querystring = {"timeout": "300"}
    files = [("video", open(video_path, "rb"))]

    # Crear el payload
    payload = {
        "prompts": [prompts],
        "model": "owlv2",
    }

    headers = {"apikey": api_key}

    try:
        # Enviar solicitud POST
        response = requests.post(
            url, headers=headers, data=payload, files=files, timeout=300000
        )

        # Comprobación del response_data
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            print(
                "\033[32m"
                + "============================== 1 passed Text_To_Od.py =============================="
                + "\x1b[0m"
            )
        else:
            print(f"Error {response.status_code}: {response.text}")
            print(
                f"\033[31m"
                + "============================== 1 failed Text_To_Od.py =============================="
                + "\x1b[0m"
            )
            return pd.DataFrame()  # DataFrame vacío en caso de error
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        print(
            f"\033[31m"
            + "============================== 1 failed Text_To_Od.py =============================="
            + "\x1b[0m"
        )
        return pd.DataFrame()  # DataFrame vacío en caso de error
