import os
import subprocess
import sys


def create_virtual_environment(env_name="venv", requirements=None, post_install_commands=None):
    """
    Creates a virtual environment and ensures the necessary libraries are installed.
    Args:
        env_name (str): Name or path of the virtual environment.
        requirements (list): List of libraries to install.
        post_install_commands (list): List of additional commands to run.
    """
    # Check if the virtual environment folder already exists
    if not os.path.exists(env_name):
        print(f"Creating the virtual environment in '{env_name}'...")
        subprocess.check_call([sys.executable, "-m", "venv", env_name])
    else:
        print(f"The virtual environment '{env_name}' already exists.")

    # Activate the pip executable of the virtual environment
    pip_executable = (
        os.path.join(env_name, "Scripts", "pip")
        if os.name == "nt"
        else os.path.join(env_name, "bin", "pip")
    )
    
    # Activate the Python executable of the virtual environment
    python_executable = (
        os.path.join(env_name, "Scripts", "python")
        if os.name == "nt"
        else os.path.join(env_name, "bin", "python")
    )

    # Update pip
    print("Updating pip...")
    subprocess.check_call([pip_executable, "install", "--upgrade", "pip"])

    # Install required libraries
    if requirements:
        print("Installing required libraries...")
        subprocess.check_call([pip_executable, "install"] + requirements)

    # Run additional commands (e.g., playwright install chromium)
    if post_install_commands:
        print("Running additional commands...")
        for command in post_install_commands:
            subprocess.check_call([python_executable, "-m"] + command.split())


if __name__ == "__main__":
    # Virtual environment name
    env_name = "venv"

    # Libraries to install
    libraries = [
    "landingai", "requests", "pandas", "openpyxl", "streamlit", "numpy",
    "pytest-xdist", "pytest", "pyautogui", "playwright", "pytest-asyncio"
    ]


    # Additional commands to run after installation
    additional_commands = [
        "playwright install chromium"
    ]

    # Create the virtual environment and install libraries and additional commands
    create_virtual_environment(env_name, libraries, additional_commands)
