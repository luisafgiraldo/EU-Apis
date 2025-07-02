import requests
import os
import random
import time
import streamlit as st

from tqdm import tqdm
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

def upload_classification(api_key:str, url:str, folders: list, path:str):
    allowed_file_formats = [".png", ".jpeg", ".jpg", ".xml", ".bmp"]
    headers = {"apikey": api_key} 

    for folder in folders:
        folder_path = os.path.join(path, folder)
        images = [
            image_file
            for image_file in os.listdir(folder_path)
            if any(image_file.lower().endswith(ext) for ext in allowed_file_formats)
                    ]
        
        # Split images into train (80%) and dev (20%) sets
        num_images = len(images)
        dev_split = int(0.2 * num_images)  # Calculate the number of dev images
        random.shuffle(images)  # Shuffle images for random selection
        dev_images = images[:dev_split]
        train_images = images[dev_split:]
    
        for image_file in images:
            image_path = os.path.join(folder_path, image_file)
    
            # Prepare request data
            with open(image_path, "rb") as image_data:
                files = {
                    "file": (
                        image_file,
                        image_data.read(),
                    )
                }
                data = {
                "name": image_file,  # Required: File name from the loop
                "label": folder,  # Optional label based on folder
                "split": "dev" if image_file in dev_images else "train",
            }

            # Send the POST request to upload the image
            response = requests.post(url, headers=headers, files=files, data=data)

            # Check for successful upload and handle any errors
            if response.status_code == 201:
                print(f"Image {image_path} uploaded successfully!")

            else:
                print(f"Error uploading image {image_path}: {response.text}")
                print(f'\033[31m' + '============================== 1 failed upload_images.py ==============================' + '\x1b[0m')

        print('\033[32m' + '============================== 1 passed upload_images.py ==============================' + '\x1b[0m')

                
def find_similarly_named_files(directory: str):
    allowed_file_formats = [".png", ".jpeg", ".jpg", ".xml", ".bmp"]
    similar_files = defaultdict(list)

    for root, dirs, files in os.walk(directory):
        for file in files:
            # Exclude the file extension
            file_name, ext = os.path.splitext(file)
            if ext in allowed_file_formats:
                similar_files[file_name].append(os.path.join(root, file))

    return similar_files
                
def post_request(url, data, headers, files):
    return requests.post(url, headers=headers, files=files, data=data)

def upload_object_detection(api_key:str, url:str, directory:str):
    headers = {"apikey": api_key} 
    error_count = 0
    duplicated_count = 0
    medias = []
    
    CONCURRENCY_LIMIT = 16
    thread_pool = ThreadPoolExecutor(max_workers=CONCURRENCY_LIMIT)
    tasks = []
    
    labeled_files = find_similarly_named_files(directory)
    labeled_file_pairs = [
    sorted(files, key=lambda x: (not x.endswith(('.jpeg')), not x.endswith('.xml')))
    for files in labeled_files.values()
    ]
    #labeled_file_pairs = list(labeled_files.values())
    num_labeled = len(labeled_file_pairs)
    # Iterate through the folders
    for pair in tqdm(labeled_file_pairs, total=num_labeled):
        image_path = pair[0]
        image_name = image_path.split("/")[-1]
        files=[
          ('file',(image_name,open(image_path,'rb'),'image/jpeg')),
        ]
        if len(pair) > 1:
            label_path = pair[1]
            label_name = label_path.split("/")[-1]
            files.append(('label',(label_name,open(label_path,'rb'),'application/xml')))
    
        # Prepare request data
        data = {
            "name": image_name,  # Required: File name from the loop
            'tags': ["not_clean", "foo"]
        }
        task = thread_pool.submit(post_request, url, data, headers, files)
        tasks.append(task)

    # upload the images concurrently
    for task in tqdm(as_completed(tasks), total=len(tasks)):
        try:
            response = task.result()
            data = response.json()["data"]
            # Check for successful upload and handle any errors
            if response.status_code == 201:
                medias.append(data)
            elif response.status_code == 409:
                duplicated_count += 1
        except Exception as e:
            error_count += 1
        print("error_count: ", error_count)
        print("duplicated_count: ", duplicated_count)
        print("Total media that uploded correctly: ", len(medias))

    if error_count > 0:
        print(f'\033[31m' + '============================== 1 failed upload_images.py ==============================' + '\x1b[0m')
    else :
        print('\033[32m' + '============================== 1 passed upload_images.py ==============================' + '\x1b[0m')

def upload_segmentation(api_key:str, url:str, directory:str):
    headers = {"apikey": api_key} 
    error_count = 0
    duplicated_count = 0
    medias = []
    
    CONCURRENCY_LIMIT = 16
    thread_pool = ThreadPoolExecutor(max_workers=CONCURRENCY_LIMIT)
    tasks = []
    
    labeled_files = find_similarly_named_files(directory)
    labeled_file_pairs = [
    sorted(files, key=lambda x: (not x.endswith(('.jpeg')), not x.endswith('.png')))
    for files in labeled_files.values()
    ]
    #labeled_file_pairs = list(labeled_files.values())
    num_labeled = len(labeled_file_pairs)
    # Iterate through the folders
    for pair in tqdm(labeled_file_pairs, total=num_labeled):
        image_path = pair[0]
        image_name = image_path.split("/")[-1]
        files=[
          ('file',(image_name,open(image_path,'rb'),'image/jpeg')),
        ]
        if len(pair) > 1:
            label_path = pair[1]
            label_name = label_path.split("/")[-1]
            files.append(('label',(label_name,open(label_path,'rb'),'image/png')))
        # Prepare request data
        data = {
            "name": image_name,  # Required: File name from the loop
            'tags': ["not_clean", "foo"]
        }
        task = thread_pool.submit(post_request, url, data, headers, files)
        tasks.append(task)

    # upload the images concurrently
    for task in tqdm(as_completed(tasks), total=len(tasks)):
        try:
            response = task.result()
            data = response.json()["data"]
            # Check for successful upload and handle any errors
            if response.status_code == 201:
                medias.append(data)
            elif response.status_code == 409:
                duplicated_count += 1
        except Exception as e:
            error_count += 1
        print("error_count: ", error_count)
        print("duplicated_count: ", duplicated_count)
        print("Total media that uploded correctly: ", len(medias))
    
    if error_count > 0:
        print(f'\033[31m' + '============================== 1 failed upload_images.py ==============================' + '\x1b[0m')
    else :
        print('\033[32m' + '============================== 1 passed upload_images.py ==============================' + '\x1b[0m')

def upload_anomaly_detection(api_key:str, url:str, folders: list, folder_to_label: list, path:str):
    allowed_file_formats = [".png", ".jpeg", ".jpg", ".xml", ".bmp"]
    headers = {"apikey": api_key} 
    print(folder_to_label, folders, url)
    for folder in folders:
        folder_path = os.path.join(path, folder)
        images = [
            image_file
            for image_file in os.listdir(folder_path)
            if any(image_file.lower().endswith(ext) for ext in allowed_file_formats)
                    ]
    
        for image_file in images:
            image_path = os.path.join(folder_path, image_file)
    
            # Prepare request data
            with open(image_path, "rb") as image_data:
                files = {
                    "file": (
                        image_file,
                        image_data.read(),
                    )
                }
                data = {
                    "name": image_file,
                    "label": folder_to_label[folder],
                    "tags": ["test", "automation"],
                }

            # Send the POST request to upload the image
            response = requests.post(url, headers=headers, files=files, data=data)

            # Check for successful upload and handle any errors
            if response.status_code == 200:
                print(f"Image {image_path} uploaded successfully!")

            else:
                print(f"Error uploading image {image_path}: {response.text}")
                print(f'\033[31m' + '============================== 1 failed upload_images.py ==============================' + '\x1b[0m')

        print('\033[32m' + '============================== 1 passed upload_images.py ==============================' + '\x1b[0m')
