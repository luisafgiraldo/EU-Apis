import custom_trainning as ct
import custom_trainning_backbone as ctb
import pandas as pd
import os

# Base URL for API requests
url_base = "https://api.staging.landing.ai/v1/projects"
# API key for authentication
api_key = "land_sk_T5RoQWkJzbRNLKtFc7hJchRJa3IdBZK5SZBBz5RBu7iB384BiX"  # Org by kelly: FT Relase CW 20

# Dictionary to map project type IDs to their corresponding names
projectType = {1: "classification", 2: "segmentation", 3: "object-detection"}

# Dictionary to map training type IDs to their corresponding names
trainType = {1: "Benchmarks", 2: "Backbone"}

# Create an empty DataFrame with specified columns
df = pd.DataFrame(
    columns=[
        "type_train",
        "type_project",
        "project_id",
        "time_training",
        "architecture",
        "train",
        "dev",
        "test",
        "date",
        "epochs"
    ]
)

# List of commands for benchmarks training
v_commands_benchmarks = [
    # ## segmentation ##
    {
        "project_id": 27690194505764,
        "type_project": projectType.get(2),
        "type_train": trainType.get(1),
    },
    {
        "project_id": 96409414840361,
        "type_project": projectType.get(2),
        "type_train": trainType.get(1),
    },
    {
        "project_id": 27700933251117,
        "type_project": projectType.get(2),
        "type_train": trainType.get(1),
    },
    # object-detection ##
    {
        "project_id": 27678212788265,
        "type_project": projectType.get(3),
        "type_train": trainType.get(1),
    },
    {
        "project_id": 27679128959018,
        "type_project": projectType.get(3),
        "type_train": trainType.get(1),
    },
    {
        "project_id": 27689531707438,
        "type_project": projectType.get(3),
        "type_train": trainType.get(1),
    },
    ## classification ##
    {
        "project_id": 28737850517539,
        "type_project": projectType.get(1),
        "type_train": trainType.get(1),
    },
    {
        "project_id": 28738068686884,
        "type_project": projectType.get(1),
        "type_train": trainType.get(1),
    },
    {
        "project_id": 28738664783910,
        "type_project": projectType.get(1),
        "type_train": trainType.get(1),
    },
]

# Execute benchmarks training commands and update DataFrame
benchmarks = ct.execute(v_commands_benchmarks, url_base, api_key, df)

# List of commands for backbone training
v_commands_backbone = [
    # ## segmentation ##
    f"""
    project_id=27690194505764,
    name=None,
    architecture="FastVit-[14M]",
    epochs=20,
    height=800,
    width=800,
    paddingValue=0,
    horizontalFlip=0.5,
    verticalFlip=None,
    numberTransforms=1,
    magnitude=4,
    p=1,
    type_project="{projectType.get(2)}",
    type_train="{trainType.get(2)}"
    """,
    f"""
        project_id=27690194505764,
        name=None,
        architecture="SegFormer-[14M]",
        epochs=20,
        height=800,
        width=800,
        paddingValue=0,
        horizontalFlip=None,
        verticalFlip=0.5,
        numberTransforms=1,
        magnitude=4,
        p=None,
        type_project="{projectType.get(2)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27690194505764,
        name=None,
        architecture="SEGLVMQA2-[27M]",
        epochs=20,
        height=64,
        width=64,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=2,
        magnitude=4,
        p=1,
        type_project="{projectType.get(2)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=96409414840361,
        name=None,
        architecture="FastVit-[14M]",
        epochs=20,
        height=800,
        width=800,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=None,
        numberTransforms=1,
        magnitude=4,
        p=1,
        type_project="{projectType.get(2)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=96409414840361,
        name=None,
        architecture="SegFormer-[14M]",
        epochs=20,
        height=800,
        width=800,
        paddingValue=0,
        horizontalFlip=None,
        verticalFlip=0.5,
        numberTransforms=1,
        magnitude=4,
        p=None,
        type_project="{projectType.get(2)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=96409414840361,
        name=None,
        architecture="SEGLVMQA2-[27M]",
        epochs=20,
        height=64,
        width=64,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=2,
        magnitude=4,
        p=1,
        type_project="{projectType.get(2)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id= 27700933251117,
        name=None,
        architecture="FastVit-[14M]",
        epochs=20,
        height=800,
        width=800,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=None,
        numberTransforms=1,
        magnitude=4,
        p=1,
        type_project="{projectType.get(2)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27700933251117,
        name=None,
        architecture="SegFormer-[14M]",
        epochs=20,
        height=800,
        width=800,
        paddingValue=0,
        horizontalFlip=None,
        verticalFlip=0.5,
        numberTransforms=1,
        magnitude=4,
        p=None,
        type_project="{projectType.get(2)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id= 27700933251117,
        name=None,
        architecture="SEGLVMQA2-[27M]",
        epochs=20,
        height=64,
        width=64,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=2,
        magnitude=4,
        p=1,
        type_project="{projectType.get(2)}",
        type_train="{trainType.get(2)}"
        """,
    # object-detection ##
    f"""
        project_id=27678212788265,
        name=None,
        architecture="RepPoints-[37M]",
        epochs=20,
        height=640,
        width=640,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=2,
        magnitude=4,
        p=1,
        type_project="{projectType.get(3)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27678212788265,
        name=None,
        architecture="RepPoints-[20M]",
        epochs=20,
        height=640,
        width=640,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=2,
        magnitude=4,
        p=1,
        type_project="{projectType.get(3)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27678212788265,
        name=None,
        architecture="RtmDet-[9M]",
        epochs=10,
        height=800,
        width=800,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=None,
        magnitude=None,
        p=None,
        type_project="{projectType.get(3)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27679128959018,
        name=None,
        architecture="RepPoints-[37M]",
        epochs=20,
        height=640,
        width=640,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=2,
        magnitude=4,
        p=1,
        type_project="{projectType.get(3)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27679128959018,
        name=None,
        architecture="RepPoints-[20M]",
        epochs=20,
        height=640,
        width=640,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=2,
        magnitude=4,
        p=1,
        type_project="{projectType.get(3)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27679128959018,
        name=None,
        architecture="RtmDet-[9M]",
        epochs=20,
        height=640,
        width=640,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=None,
        magnitude=None,
        p=None,
        type_project="{projectType.get(3)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27689531707438,
        name=None,
        architecture="RepPoints-[37M]",
        epochs=20,
        height=640,
        width=640,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=2,
        magnitude=4,
        p=1,
        type_project="{projectType.get(3)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27689531707438,
        name=None,
        architecture="RepPoints-[20M]",
        epochs=20,
        height=640,
        width=640,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=2,
        magnitude=4,
        p=1,
        type_project="{projectType.get(3)}",
        type_train="{trainType.get(2)}"
        """,
    f"""
        project_id=27689531707438,
        name=None,
        architecture="RtmDet-[9M]",
        epochs=20,
        height=640,
        width=640,
        paddingValue=0,
        horizontalFlip=0.5,
        verticalFlip=0.5,
        numberTransforms=None,
        magnitude=None,
        p=None,
        type_project="{projectType.get(3)}",
        type_train="{trainType.get(2)}"
        """,
    ## classification ##
    f"""
        project_id=28737850517539,
        name=None,
        architecture="ConvNext-[16M]",
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
        project_id=28737850517539,
        name=None,
        architecture="ConvNext-[29M]",
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
        project_id=28737850517539,
        name=None,
        architecture="CLSLVMQA2-[21M]",
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
        project_id=28737850517539,
        name=None,
        architecture="CLSLVMQA2-[27M]",
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
        project_id=28738068686884,
        name=None,
        architecture="ConvNext-[16M]",
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
        project_id=28738068686884,
        name=None,
        architecture="ConvNext-[29M]",
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
        project_id=28738068686884,
        name=None,
        architecture="CLSLVMQA2-[21M]",
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
        project_id=28738068686884,
        name=None,
        architecture="CLSLVMQA2-[27M]",
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
        project_id=28738664783910,
        name=None,
        architecture="ConvNext-[16M]",
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
        project_id=28738664783910,
        name=None,
        architecture="ConvNext-[29M]",
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
        project_id=28738664783910,
        name=None,
        architecture="CLSLVMQA2-[21M]",
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
        project_id=28738664783910,
        name=None,
        architecture="CLSLVMQA2-[27M]",
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
backbone = ctb.execute(v_commands_backbone, url_base, api_key, df)

# Concatenate the backbone and large images DataFrames and reset the index
result_vertical_reset = pd.concat([benchmarks, backbone], axis=0).reset_index(drop=True)
# Define the file path
file_path = os.path.join("Benchmarks", "reports", "report.xlsx")

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
