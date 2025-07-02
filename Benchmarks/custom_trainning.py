import requests
import monitor_train as mt
import getMetrics as gm
import pandas as pd
from datetime import datetime


# Function to execute a list of commands and process the training requests
def execute(v_commands: list, url_base: str, api_key: str, df):

    for command in v_commands:

        project_id = command["project_id"]
        type_project = command["type_project"]
        type_train = command["type_train"]

        print(f"Project ID: {project_id}")
        print(f"type_project: {type_project}")
        print(f"type_train: {type_train}")

        headers = {"apikey": api_key}
        url = f"{url_base}/{project_id}/train"

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            print(response_data)
        except requests.exceptions.RequestException as e:
            print(f"Error creating classes: {e}")
            continue

        try:
            training_id = response_data["data"]["trainingId"]
            print(f"Training ID: {training_id}")
        except KeyError as e:
            training_id = f"Error: {e}"
            print(f"Error: {e}")
            continue

        url = f"{url_base}/{project_id}/train/architectures"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            print(response_data)
        except requests.exceptions.RequestException as e:
            print(f"Error creating classes: {e}")
            continue

        if isinstance(response_data, list) and len(response_data) > 1:
            architecture = response_data[1].get("data", {}).get("name", "N/A")
        else:
            architecture = "N/A"

        url = f"{url_base}/{project_id}/train/{training_id}/status"
        try:
            elapsed_time = mt.monitoring(api_key=api_key, url=url)
            print(elapsed_time)
            elapsed_time = f"{float(elapsed_time)/60:.2f} minutes"
        except Exception as e:
            elapsed_time = f"Error monitoring training: {e}"
            print(f"Error monitoring training: {e}")

        url = f"{url_base}/{project_id}/train/{training_id}/results/metrics"
        try:
            metrics = gm.metrics_summary(api_key=api_key, url=url)
            print(metrics)
        except Exception as e:
            metrics = f"Error retrieving metrics: {e}"
            print(f"Error retrieving metrics: {e}")

        now = datetime.now()

        if metrics and isinstance(metrics, list):
            try:
                # Initialize variables for each set
                train = dev = test = "N/A"

                # Iterate over each element in 'metrics' to find and assign values
                for metric in metrics:
                    name = metric.get("name")
                    metric_data = metric.get("metrics")

                    if metric_data:
                        performance = metric_data[0].get("performance", "N/A")
                        if name == "train":
                            train = performance
                        elif name == "dev":
                            dev = performance
                        elif name == "test":
                            test = performance
                    else:
                        print(
                            f"No metrics available for {name}. Setting default 'N/A'."
                        )

            except (IndexError, KeyError, TypeError) as e:
                print(f"Error accessing metrics: {e}")
                train = dev = test = "N/A"
        else:
            print("Metrics is None or not a list. Cannot extract data.")
            train = dev = test = "N/A"

        print(f"Train: {train}, Dev: {dev}, Test: {test}")

        # Format the current date and time as a string
        current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        print("current date and time:", current_date_time)

        # Create a temporary DataFrame for the new row to be addedr
        new_row = pd.DataFrame(
            [
                {
                    "type_train": type_train,
                    "type_project": type_project,
                    "project_id": str(project_id),
                    "time_training": elapsed_time,
                    "architecture": architecture,
                    "train": f"{round(float(train) * 100)}%" if train not in [None, 'None', '', 'N/A'] else "N/A",
                    "dev": f"{round(float(dev) * 100)}%" if dev not in [None, 'None', '', 'N/A'] else "N/A",
                    "test": f"{round(float(test) * 100)}%" if test not in [None, 'None', '', 'N/A'] else "N/A",
                    "date": current_date_time,
                    "epochs": str(20)
                }
            ]
        )

        # Concatenate the new DataFrame with the original DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

    return df
