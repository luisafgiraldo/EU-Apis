import custom_trainning as ct
import pandas as pd
import openpyxl
from datetime import datetime
import os

# Base URL for API requests
url_base = "https://api.staging.landing.ai/v1/projects"
# API key for authentication
api_key = "land_sk_wlWFn5kyB1VNoUwsHLrNLk2Mnv6XByS4YMP7bpOdNFRGXn5YBB"  # Org: Enterprise Org

# Dictionary to map project type IDs to their corresponding names
projectType = {1: "classification", 2: "segmentation", 3: "object-detection"}

# Dictionary to map training type IDs to their corresponding names
trainType = {1: "Epochs", 2: "Backbone EdgeAI"}

# Create an empty DataFrame with specified columns
df = pd.DataFrame(
    columns=[
        "type_train",
        "type_project",
        "project_id",
        "time_training",
        "architecture",
        "rescaleWithPadding",
        "train",
        "dev",
        "test",
        "date",
        "epochs"
    ]
)

# List of commands for Epochs training
v_commands_epochs = [
    #OD
    f"""
    project_id=139863102765096,
    name=None,
    architecture="RtmDet-[9M]",
    epochs=50,
    height=600,
    width=600,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=None,
    numberTransforms=None,
    magnitude=None,
    p=None,
    type_project="{projectType.get(3)}",
    type_train="{trainType.get(1)}"

     """,
    f"""
    project_id=139863102765096,
    name=None,
    architecture="RepPoints-[20M]",
    epochs=100,
    height=600,
    width=600,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=None,
    numberTransforms=1,
    magnitude=4,
    p=1,
    type_project="{projectType.get(3)}",
    type_train="{trainType.get(1)}"
    """,
    f"""
    project_id=139863102765096,
    name=None,
    architecture="RepPoints-[37M]",
    epochs=150,
    height=600,
    width=600,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=None,
    numberTransforms=1,
    magnitude=4,
    p=1,
    type_project="{projectType.get(3)}",
    type_train="{trainType.get(1)}"
    """,

    #Class
    f"""
    project_id=139863258720298,
    name=None,
    architecture="ConvNext-[29M]",
    epochs=50,
    height=512,
    width=512,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=None,
    numberTransforms=None,
    magnitude=None,
    p=None,
    type_project="{projectType.get(1)}",
    type_train="{trainType.get(1)}"
     """,
    f"""
    project_id=139863258720298,
    name=None,
    architecture="ConvNext-[16M]",
    epochs=100,
    height=512,
    width=512,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=None,
    numberTransforms=None,
    magnitude=None,
    p=None,
    type_project="{projectType.get(1)}",
    type_train="{trainType.get(1)}"
    """,
    f"""
    project_id=139863258720298,
    name=None,
    architecture="ConvNext-[16M]",
    epochs=150,
    height=512,
    width=512,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=0.5,
    numberTransforms=None,
    magnitude=None,
    p=None,
    type_project="{projectType.get(1)}",
    type_train="{trainType.get(1)}"
    """,

    #SEG
    f"""
    project_id=139863342313515,
    name=None,
    architecture="SegFormer-[14M]",
    epochs=50,
    height=800,
    width=800,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=None,
    numberTransforms=1,
    magnitude=4,
    p=1,
    type_project="{projectType.get(2)}",
    type_train="{trainType.get(1)}"
    """,
    f"""
    project_id=139863342313515,
    name=None,
    architecture="FastVit-[14M]",
    epochs=100,
    height=800,
    width=800,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=None,
    numberTransforms=1,
    magnitude=4,
    p=1,
    type_project="{projectType.get(2)}",
    type_train="{trainType.get(1)}"
    """,
    f"""
    project_id=139863342313515,
    name=None,
    architecture="SegFormer-[14M]",
    epochs=150,
    height=800,
    width=800,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=None,
    numberTransforms=1,
    magnitude=4,
    p=1,
    type_project="{projectType.get(2)}",
    type_train="{trainType.get(1)}"
    """,
]

# Execute epochs training commands and update DataFrame
epochs = ct.execute(v_commands_epochs, url_base, api_key, df)

v_commands_backbone = [
    ### CLASS - EdgeAI Backbone ###
    f"""
        project_id=137764742426668,
        name=None,
        architecture="ConvNextEmbeddeed-[16M]",
        epochs=20,
        height=512,
        width=512,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=None,
        magnitude=None,
        p=None,
        type_project="{projectType.get(1)}",
        type_train="{trainType.get(2)}"
       """,
    f"""
        project_id=137764864798766,
        name=None,
        architecture="ConvNextEmbeddeed-[16M]",
        epochs=20,
        height=512,
        width=512,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=None,
        magnitude=None,
        p=None,
        type_project="{projectType.get(1)}",
        type_train="{trainType.get(2)}"
       """,
    f"""
        project_id=137764891097135,
        name=None,
        architecture="ConvNextEmbeddeed-[16M]",
        epochs=20,
        height=512,
        width=512,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=None,
        magnitude=None,
        p=None,
        type_project="{projectType.get(1)}",
        type_train="{trainType.get(2)}"
       """,
]

# Execute backbone training commands and update DataFrame
backbone = ct.execute(v_commands_backbone, url_base, api_key, df)

result_vertical_reset = pd.concat([epochs, backbone], axis=0).reset_index(drop=True)

# Define the file path
file_path = os.path.join("Epochs", "reports", "report.xlsx")

# Check if the file exists
if os.path.exists(file_path):
    # If it exists, load the existing Excel file
    existing_data = pd.read_excel(file_path)
    # Concatenate the existing data with the new data
    final_data = pd.concat([existing_data, result_vertical_reset], axis=0).reset_index(
        drop=True
    )
else:
    # If it does not exist, use the new data directly
    final_data = result_vertical_reset

# Save the final DataFrame to the Excel file
final_data.to_excel(file_path, index=False)
