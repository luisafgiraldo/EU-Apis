####################### PARAMETERS ####################################
import os
from datetime import datetime
import time

# Start time
start_time = time.time()

fecha_actual = datetime.now().strftime("%Y-%m-%d")
print(fecha_actual)

projectType = {1: "classification", 2: "segmentation", 3: "object-detection", 4: "anomaly-detection"}
################### PARAMETERS TO CHANGE ###########################
# api_key = "land_sk_VtHE8Gx36OvgODIYxyl0cesFMhiZUJEvtEc3YI1Dk1C5tf76ku"  # Enterprise-Org
api_key = "land_sk_GPoLEAN9CThf44guBoAip85Vodx837XEKKGxCLQNuUNn60HQRz"   # Enterprise-Org
url_base = "https://api.staging.landing.ai/v1"
# %%

for i in range(1, 5):
    ################### PARAMETERS TO CHANGE ###########################
    choose_project = projectType.get(i)
    name_proyecto = f"{choose_project}-{fecha_actual}"
    # %%
    ######################## CREATE PROJECT ###############################
    import create_project as cp

    url = f"{url_base}/projects"
    data = {"projectType": choose_project, "name": name_proyecto}
    project_id = cp.create(api_key=api_key, url=url, data=data)
    # %%
    ######################## GET PROJECT ##################################
    import getProject as gp

    gp.getProject(api_key, url, project_id)
    # %%
    ######################## CREATE CLASSES ###############################
    import create_classes as cc
    url = f"{url}/{project_id}/classes"
    if choose_project == "anomaly-detection":
        True
    else:
        if choose_project == "classification":
            data = {"0": {"name": "Roll-Print"}, "1": {"name": "Side-line"}}
        elif choose_project == "segmentation":
            data = {"1": {"name": "Screw"}}
        elif choose_project == "object-detection":
            data = {"1": {"name": "Screw", "color": "#FFFF00"}}
        cc.create(api_key=api_key, url=url, data=data)
    # %%
    ####################### UPLOAD IMAGES #################################
    import upload_images as ui

    url = url.replace("classes", "images")
    if choose_project == "classification":
        folders = [
            data[key]["name"] for key in data
        ]  # A list is created, because the class is the same folder.
        path = os.path.join("Smoke-tests", "Images-CLASS")
        ui.upload_classification(api_key, url, folders, path)
    elif choose_project == "object-detection":
        path = os.path.join("Smoke-tests", "Images-OD")
        ui.upload_object_detection(api_key, url, directory=path)
        import auto_split as asp

        url = url.replace("images", "autosplit")
        # Prepare the payload (adheres to the required format)
        data = {
            "splitPercentages": {
                "train": 65,
                "dev": 25,
                "test": 10,
            },
            "selectOption": "all-labeled",
        }

        asp.auto_split(url, api_key, data)

    elif choose_project == "segmentation":
        path = os.path.join("Smoke-tests", "images-SEG")
        ui.upload_segmentation(api_key, url, directory=path)
        import auto_split as asp

        url = url.replace("images", "autosplit")
        # Prepare the payload (adheres to the required format)
        data = {
            "splitPercentages": {
                "train": 65,
                "dev": 25,
                "test": 10,
            },
            "selectOption": "all-labeled",
        }

        asp.auto_split(url, api_key, data)

    elif choose_project == "anomaly-detection":
        folders = ["clean", "contaminated"]
        folder_to_label = {
            "clean": "normal",
            "contaminated": "abnormal",
        }
        path = os.path.join("Smoke-tests", "Images-ANOMALY")
        ui.upload_anomaly_detection(api_key, url, folders, folder_to_label, path)
        import auto_split as asp

        url = url.replace("images", "autosplit")
        data = {
            "splitPercentages": {
                "train": 65,
                "dev": 25,
                "test": 10,
            },
            "selectOption": "all-labeled",
            "constraints": {
                "train": {
                    "labels": ["normal"]
                },
                "dev": {
                    "labels": ["normal", "abnormal"]
                },
                "test": {
                    "labels": ["normal", "abnormal"]
                }
            }
        }

        asp.auto_split(url, api_key, data)

    # %%
    ####################### TRAIN #########################################
    import train as t

    if choose_project == "classification":
        url = url.replace("images", "train")
        training_id = t.training(api_key, url)
    elif choose_project == "object-detection":
        url = url.replace("autosplit", "train")
        training_id = t.training(api_key, url)
    elif choose_project == "segmentation":
        url = url.replace("autosplit", "train")
        training_id = t.training(api_key, url)
    elif choose_project == "anomaly-detection":
        url = url.replace("autosplit", "train")
        url = "https://app.staging.landing.ai/api/model/train"
        json = {        
        "experimentType": "anomaly-detection",
        "projectId": project_id
        }
        training_id = t.training_anomaly(api_key, url, json)

    ###################### MONITOR TRAIN ##################################
    import monitor_train as mt

    if choose_project == 'anomaly-detection':
        url = f"https://app.staging.landing.ai/api/registered_model/model_status?projectId={project_id}&modelId={training_id}&lastUpdatedAt=null"
    else:
        url = f"{url}/{training_id}/status"
    mt.monitoring(api_key, url)
    # %%
    ##################### MODELS #########################################
    import get_models as gm

    url = f"{url_base}/projects/{project_id}/models"
    models = gm.model(api_key, url)
    model = models[0]
    threshold = 0.5
    # %%
    ###################### DEPLOYMENT #####################################
    import create_deployment as cd

    url = url.replace("models", "deployments")
    if choose_project == "classification":
        data = {
            "name": model.get("name"),
            "modelId": model.get("id"),
            "threshold": threshold,
        }
    elif choose_project == "object-detection":
        data = {"name": model.get("name"), "modelId": model.get("id")}
    elif choose_project == "segmentation":
        data = {"name": model.get("name"), "modelId": model.get("id")}
    elif choose_project == "anomaly-detection":
        data = {"name": model.get("name"), "modelId": model.get("id")}
    deployment = cd.create(api_key, url, data)
    print(deployment)
    deployment = deployment["data"]
    predictionUrl = deployment["predictionUrl"]
    endpoint_id = deployment["id"]
    # %%
    ###################### PREDICT ########################################
    import predict as p

    url = url.replace("deployments", "usage/summary")
    if choose_project == "classification":
        folder = "Predictions/Class"
    elif choose_project == "object-detection":
        folder = "Images"
    elif choose_project == "segmentation":
        folder = "Images"
    elif choose_project == "anomaly-detection":
        folder = "clean"
    image_dir = os.path.join(path, folder)
    p.predict(image_dir=image_dir, endpoint_id=endpoint_id, api_key=api_key)

# End time and execution time calculation
end_time = time.time()
execution_time = end_time - start_time

# Convert time to hours, minutes, and seconds
hours = int(execution_time // 3600)
minutes = int((execution_time % 3600) // 60)
seconds = int(execution_time % 60)

print(f"Total execution time: {hours} hours, {minutes} minutes, and {seconds} seconds.")