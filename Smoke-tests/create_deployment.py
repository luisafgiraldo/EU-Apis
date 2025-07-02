import requests

def create(api_key:str, url:str, data: dict):
    headers = {"apikey": api_key}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        response_data = response.json()
        print(response_data)
        print("Deploy created successfully!")
        print('\033[32m' + '============================== 1 passed create_deployment.py ==============================' + '\x1b[0m')

    else:
        print(f"Error creating classes: {response.text}")
        print(f'\033[31m' + '============================== 1 failed create_deployment.py ==============================' + '\x1b[0m')

    return response_data