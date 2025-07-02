import time
import requests

def monitoring(api_key: str, url: str):
    headers = {"apikey": api_key}
    
    # Continuously check training status until completion
    training_complete = False
    start_time = None
    elapsed_time = 0

    while not training_complete:
        time.sleep(10)  # Adjust the wait time between checks (in seconds)
    
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            data = response.json()
            training_status = data["data"]["status"]
            print(f"Training status: {training_status}")
            
            if training_status == "TRAINING":
                if start_time is None:
                    start_time = time.time()
                    print("Training started.")
            elif training_status in ["EVALUATING", "PUBLISHING"]:
                if start_time is not None:
                    elapsed_time = time.time() - start_time
                    print(f"Training has been in progress for {elapsed_time:.2f} seconds.")
            elif training_status == "SUCCEEDED":
                training_complete = True
                if start_time is not None:
                    elapsed_time = time.time() - start_time
                print(f"Training completed successfully! Total training time: {elapsed_time:.2f} seconds.")
                print(f'\033[32m' + '============================== 1 passed  monitor_train.py ==============================' + '\x1b[0m')

            elif training_status == "FAILED":
                training_complete = True
                print("Training failed. Please check the LandingLens platform for details.")
                print(f'\033[31m' + '============================== 1 failed monitor_train.py ==============================' + '\x1b[0m')

        else:
            print(f"Error during training status request: {response.text}")
            print(f'\033[31m' + '============================== 1 failed monitor_train.py  ==============================' + '\x1b[0m')

