import requests
from datetime import datetime

def listSnapShots(api_key: str, url: str):
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if isinstance(response_data["data"], list) and response_data["data"]:
            # Convertir 'creationTime' a objetos datetime y ordenar
            for snapshot in response_data["data"]:
                snapshot['creationTime'] = datetime.fromisoformat(snapshot['creationTime'].replace('Z', '+00:00'))
            # Ordenar los snapshots por 'creationTime' en orden descendente
            sorted_snapshots = sorted(response_data["data"], key=lambda x: x['creationTime'], reverse=True)
            if sorted_snapshots:
                return sorted_snapshots[0]  # Devuelve el más reciente
            else:
                return None
        else:
            print("Unexpected response structure or 'data' is empty.")
            return None
    else:
        print(f"Error get listSnapShots: {response.text}")
        return None

def display_snapshot(snapshot):
    print("{")
    print('  "data": {')
    print(f'    "name": "{snapshot["name"]}",')
    print(f'    "version": {snapshot["version"]},')
    print(f'    "creationTime": "{snapshot["creationTime"].isoformat()}"')
    print("  }")
    print("}")
