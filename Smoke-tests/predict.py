import os
import requests
from landingai.data_management.client import _URL_ROOTS  
from landingai.predict import Predictor
from PIL import Image
import io

# Correcting the URL assignment
_URL_ROOTS["LANDING_API"] = "https://app.staging.landing.ai/"

def get_data_from_api(url, api_key):
    headers = {"apikey": api_key}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        print(response_data)  # Inspect the structure of the response data
    else:
        print(f"Error get project: {response.text}")
        print(f'\033[31m' + '============================== 1 failed predict.py ==============================' + '\x1b[0m')

def predict(image_dir: str, endpoint_id: str, api_key: str):
    images_path = []
    allowed_file_formats = [".png", ".jpeg", ".jpg", ".xml", ".bmp"]
    
    for file in os.listdir(image_dir):
        if any(file.lower().endswith(ext) for ext in allowed_file_formats):
            all_image_path = os.path.join(image_dir, file)
            images_path.append(all_image_path)
            print(f'Added: {all_image_path}')
    
    predictor = Predictor(endpoint_id, api_key=api_key)
    
    # Loop through the images and make predictions
    for image_path in images_path:
        try:
            with Image.open(image_path) as image:
                # Convert the image to a format suitable for prediction
                image_format = image.convert('RGB')
                # Save the image to a byte array to be sent in the HTTP request
                image_bytes = io.BytesIO()
                image_format.save(image_bytes, format='JPEG')
                image_bytes.seek(0)
                
                # Perform prediction using requests
                url = f"https://predict.app.staging.landing.ai/inference/v1/predict?endpoint_id={endpoint_id}"
                headers = {
                    "apikey": api_key
                }
                files = {
                    "file": image_bytes
                }
                response = requests.post(url, headers=headers, files=files)
                if response.status_code == 200:
                    predictions = response.json()
                    print(f'Predictions for {image_path}: {predictions}')
                    
                else:
                    print(f'Error processing {image_path}: {response.text}')
                    print(f'\033[31m' + '============================== 1 failed predict.py ==============================' + '\x1b[0m')

        except Exception as e:
            print(f'Error processing {image_path}: {str(e)}')
            print(f'\033[31m' + '============================== 1 failed predict.py ==============================' + '\x1b[0m')

    print('\033[32m' + '============================== 1 passed predict.py ==============================' + '\x1b[0m')
    print('\033[32m' + '============================== 1 passed delete-project.py ==============================' + '\x1b[0m')