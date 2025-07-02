import requests

def auto_split(url:str, api_key: str, data: dict):
    headers = {"apikey": api_key}
    # Prepare the payload (adheres to the required format)
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print("Successfully splitted the data!")
        print('\033[32m' + '============================== 1 passed auto_split.py ==============================' + '\x1b[0m')

    else:
        print(f"Error splitting the data: {response.text}")
        print(f'\033[31m' + '============================== 1 failed auto_split.py ==============================' + '\x1b[0m')
