import requests

def metrics_summary(api_key: str, url: str):
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        print(response_data)  # Inspect the structure of the response data
        # Assuming `response_data["data"]` is a list and we need the first element's "id"
        if isinstance(response_data["data"], list) and response_data["data"]:
            metrics = response_data["data"]
            print(f"metrics {metrics}")
            print("Get successfully!")      
        else:
            print("Unexpected response structure or 'data' is empty.")
            metrics = None
    else:
        print(f"Error get metrics: {response.text}")
        metrics = None

    return metrics
