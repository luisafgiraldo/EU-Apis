# -*- coding: utf-8 -*-
"""
"""
import requests

def getProject(api_key: str, url: str, project_id : int):
    url_project = f"{url}/{project_id}"
    headers = {"apikey": api_key}
    response = requests.get(url_project, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        project_id = response_data["data"]["id"]
        print(f"Project getting with ID {project_id}")
        print("Project getting successfully!")  
        print('\033[32m' + '============================== 1 passed getProject.py ==============================' + '\x1b[0m')
    else:
        print(f"Error getting project: {response.text}")
        print(f'\033[31m' + '============================== 1 failed getProject.py ==============================' + '\x1b[0m')
    project_id = int(response_data['data']['id'])
    print(project_id)
    return project_id
