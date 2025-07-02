import requests

def model(api_key: str, url: str):
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        print(response_data)  # Inspect the structure of the response data
        
        # Assuming `response_data["data"]` is a list and we need the first element's "id"
        if isinstance(response_data["data"], list) and response_data["data"]:
            model = response_data["data"]
            print(f"Project ID {model}")
            print("Get successfully!")
            print('\033[32m' + '============================== 1 passed get_models.py ==============================' + '\x1b[0m')
            
        else:
            print("Unexpected response structure or 'data' is empty.")
            model = None
            print(f'\033[31m' + '============================== 1 failed get_models.py ==============================' + '\x1b[0m')

    else:
        print(f"Error get project: {response.text}")
        model = None
        print(f'\033[31m' + '============================== 1 failed get_models.py  ==============================' + '\x1b[0m')

    return model
