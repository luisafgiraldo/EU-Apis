import time
import requests

def monitoring(api_key: str, url: str):
    headers = {"apikey": api_key}

    training_complete = False
    training_started = False
    training_time = 0
    last_training_start = None

    while not training_complete:
        time.sleep(10)
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            training_status = data["data"]["status"]
            print(f"Training status: {training_status}")

            if training_status == "TRAINING":
                if not training_started:
                    training_started = True
                    last_training_start = time.time()
                    print("Training started.")
            else:
                if training_started:
                    # Terminó el estado TRAINING, sumamos tiempo
                    training_duration = time.time() - last_training_start
                    training_time += training_duration
                    training_started = False
                    print(f"Training phase ended. Time in TRAINING: {training_duration:.2f} seconds.")

                if training_status == "SUCCEEDED":
                    training_complete = True
                    print(f"Training completed successfully! Total time in TRAINING: {training_time:.2f} seconds.")
                elif training_status == "FAILED":
                    training_complete = True
                    print("Training failed. Please check the LandingLens platform for details.")
        else:
            print(f"Error during training status request: {response.text}")

    return training_time
