import requests
import json
import monitor_train as mt
import getMetrics as gm
import pandas as pd
from datetime import datetime


# Function to parse a string of parameters and convert it into a dictionary of arguments
def parse_command(command_str):
    command_dict = {}
    lines = command_str.strip().split("\n")
    for line in lines:
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('",')
            if value.lower() in ["none", ""]:
                value = None
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            elif value.replace(".", "", 1).isdigit():
                value = float(value)
                if value.is_integer():
                    value = int(value)
            command_dict[key] = value
    return command_dict


# Function to create a payload for the model training request
def create_payload(
    name=None,
    architecture=None,
    epochs=None,
    height=None,
    width=None,
    paddingValue=None,
    horizontalFlip=None,
    verticalFlip=None,
    numberTransforms=None,
    magnitude=None,
    p=None,
):
    payload = {}

    if name is not None:
        payload["name"] = name

    payload["model"] = {"architecture": architecture, "hyperParams": {"epochs": epochs}}

    preprocessing = {
        "rescaleWithPadding": {
            "height": height,
            "width": width,
            "paddingValue": paddingValue,
        }
    }

    payload["transforms"] = {"preprocessing": [preprocessing], "augmentations": []}

    if horizontalFlip is not None:
        if horizontalFlip < 0:
            horizontalFlip = 0
        elif horizontalFlip > 1:
            horizontalFlip = 1
        payload["transforms"]["augmentations"].append(
            {"horizontalFlip": {"p": horizontalFlip}}
        )

    if verticalFlip is not None:
        if verticalFlip < 0:
            verticalFlip = 0
        elif verticalFlip > 1:
            verticalFlip = 1
        payload["transforms"]["augmentations"].append(
            {"verticalFlip": {"p": verticalFlip}}
        )

    if numberTransforms is not None or magnitude is not None or p is not None:
        rand_augment = {}
        if numberTransforms is not None:
            rand_augment["numberTransforms"] = numberTransforms
        if magnitude is not None:
            rand_augment["magnitude"] = magnitude
        if p is not None:
            rand_augment["p"] = p
        payload["transforms"]["augmentations"].append({"randAugment": rand_augment})

    return payload


# Function to create a project payload with the given parameters
def create_project_payload(
    project_id,
    type_project,
    type_train,
    name=None,
    architecture=None,
    epochs=None,
    height=None,
    width=None,
    paddingValue=None,
    horizontalFlip=None,
    verticalFlip=None,
    numberTransforms=None,
    magnitude=None,
    p=None,
):
    payload = create_payload(
        name=name,
        architecture=architecture,
        epochs=epochs,
        height=height,
        width=width,
        paddingValue=paddingValue,
        horizontalFlip=horizontalFlip,
        verticalFlip=verticalFlip,
        numberTransforms=numberTransforms,
        magnitude=magnitude,
        p=p,
    )

    project_data = {
        "project_id": project_id,
        "type_project": type_project,
        "type_train": type_train,
        "payload": payload,  # Send as a dictionary, not as a JSON string
    }

    return project_data


# Create an empty DataFrame
df = pd.DataFrame(
    columns=[
        "type_train",
        "type_project",
        "project_id",
        "time_training",
        "architecture",
        "rescaleWithPadding",
        "metrics",
        "date",
        "epochs"
    ]
)

all_metrics_objects = []


# Function to execute a list of commands and process the training requests
def execute(v_commands: list, url_base: str, api_key: str, df):

    for command in v_commands:
        command_args = parse_command(command)
        project_id = command_args.pop("project_id", None)
        type_project = command_args.pop("type_project", None)
        type_train = command_args.pop("type_train", None)
        epochs = command_args.get("epochs", None)  


        project_data = create_project_payload(
            project_id=project_id,
            type_project=type_project,
            type_train=type_train,
            **command_args,
        )

        print(f"Project ID: {project_data['project_id']}")
        print(f"type_project: {project_data['type_project']}")
        print(f"type_train: {project_data['type_train']}")
        print(f"Payload: {project_data['payload']}")

        headers = {"apikey": api_key}
        url = f"{url_base}/{project_id}/train"

        try:
            response = requests.post(url, headers=headers, json=project_data["payload"])
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

        architecture = project_data["payload"]["model"]["architecture"]

        preprocessing = project_data["payload"]["transforms"]["preprocessing"]
        rescale_with_padding = next(
            (
                item["rescaleWithPadding"]
                for item in preprocessing
                if "rescaleWithPadding" in item
            ),
            None,
        )

        # Create a temporary DataFrame for the new row to be addedr
        new_row = pd.DataFrame(
            [
                {
                    "type_train": type_train,
                    "type_project": type_project,
                    "project_id": str(project_id),
                    "time_training": elapsed_time,
                    "architecture": architecture,
                    "rescaleWithPadding": rescale_with_padding,
                    "train": f"{round(float(train) * 100)}%" if train not in [None, 'None', '', 'N/A'] else "N/A",
                    "dev": f"{round(float(dev) * 100)}%" if dev not in [None, 'None', '', 'N/A'] else "N/A",
                    "test": f"{round(float(test) * 100)}%" if test not in [None, 'None', '', 'N/A'] else "N/A",
                    "date": current_date_time,
                    "epochs": str(epochs)
                }
            ]
        )

        # Concatenate the new DataFrame with the original DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

    return df
