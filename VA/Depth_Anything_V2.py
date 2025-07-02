import requests
import pandas as pd
import utils as u


def create(url: str, image_path: str, api_key: str):
    querystring = {"timeout": "300"}

    # Crear el payload
    payload = {"image": u.transformer(image_path), "grayscale": True}

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Basic {api_key}",
    }

    try:
        # Send POST request
        response = requests.post(url, json=payload, headers=headers, params=querystring)

        # Check if the response is successful
        if response.status_code == 200:
            response_data = response.json()
            # Ensure response matches the expected format
            if "data" in response_data and "map" in response_data["data"]:
                print(
                    "\033[32m"
                    + "============================== 1 passed Depth_Anything_V2.py =============================="
                    + "\x1b[0m"
                )
                return response_data
            else:
                print("Unexpected response format:", response_data)
                print(
                    f"\033[31m"
                    + "============================== 1 failed Depth_Anything_V2.py =============================="
                    + "\x1b[0m"
                )
                return pd.DataFrame()  # Empty DataFrame for unexpected response
        else:
            print(f"Error {response.status_code}: {response.text}")
            print(
                f"\033[31m"
                + "============================== 1 failed Depth_Anything_V2.py =============================="
                + "\x1b[0m"
            )

            return pd.DataFrame()  # Empty DataFrame in case of error
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        print(
            f"\033[31m"
            + "============================== 1 failed Depth_Anything_V2.py =============================="
            + "\x1b[0m"
        )
        return pd.DataFrame()  # Empty DataFrame in case of error
