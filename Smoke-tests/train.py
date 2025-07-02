import requests

def training(api_key:str, url:str):
    headers = {"apikey": api_key}
    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            training_id = data["data"]["trainingId"]
            print(f"Training started successfully! Training ID: {training_id}")
            print('\033[32m' + '============================== 1 passed train.py ==============================' + '\x1b[0m')

            return training_id
        else:
            # Log detailed error information or handle different status codes if needed
            print(f"Error during training request: {response.text}")
            print(f'\033[31m' + '============================== 1 failed train.py  ==============================' + '\x1b[0m')

    except requests.RequestException as e:
        # Handle exceptions that may occur during the request
        print(f"An error occurred during the training request: {str(e)}")
        print(f'\033[31m' + '============================== 1 failed train.py ==============================' + '\x1b[0m')

    return None

def training_anomaly(api_key:str, url:str, json:list):
    headers = {"apikey": api_key}
    try:
        response = requests.post(url, headers=headers, json=json)
        if response.status_code == 200:
            data = response.json()
            print(data)
            training_id = data["data"]["runId"]
            print(f"Training started successfully! Training ID: {training_id}")
            print('\033[32m' + '============================== 1 passed train.py ==============================' + '\x1b[0m')

            return training_id
        else:
            # Log detailed error information or handle different status codes if needed
            print(f"Error during training request: {response.text}")
            print(f'\033[31m' + '============================== 1 failed train.py  ==============================' + '\x1b[0m')

    except requests.RequestException as e:
        # Handle exceptions that may occur during the request
        print(f"An error occurred during the training request: {str(e)}")
        print(f'\033[31m' + '============================== 1 failed train.py ==============================' + '\x1b[0m')

    return None