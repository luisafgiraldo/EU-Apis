import requests

def create(api_key:str, url:str, data: dict):
    headers = {"apikey": api_key}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        response_data = response.json()
        project_id = response_data["data"]["id"]
        print(f"Project created with ID {project_id}")
        print("Project created successfully!")
        print('\033[32m' + '============================== 1 passed create_project.py ==============================' + '\x1b[0m')


    else:
        print(f"Error creating project: {response.text}")
        print(f'\033[31m' + '============================== 1 failed create_project.py ==============================' + '\x1b[0m')

    project_id = int(response_data['data']['id'])
    print(project_id)
    return project_id



