# API

## Table of Contents

- [Introduction](#introduction)
- [LibrariRequirementses](#Requirements)
- [Getting Started](#getting-started)
- [Hi! What do you want to execute?](#hi-what-do-you-want-to-execute)

# Introduction

This project provides a set of APIs developed in Python to perform various tasks for Landing AI.

Don’t worry, this project runs anywhere.

## Requirements

To run this project, you'll need:
- Python 3.8 or higher
- Libraries 
  - `pip install landingai, requests, pandas, openpyxl, streamlit, numpy, pytest-xdist, pytest, pyautogui, playwright, pytest-asyncio `

## Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/luisafgiraldo/API-s-.git
   ```

2. Open the project in Visual Studio Code
3. Open the Console 

    - **If you are using Windows OS:**

        ```bash
        Ctrl + J
        ```

    - **If you are using macOS:**

        ```bash
        Command + J
        ```

4. Run the file:

 - **If you are using Windows OS:**
    ```bash
    python entorno.py
    ```

 - **If you are using MacOS:**
    ```bash
    python3 entorno.py
    ```

5. After running it, activate the virtual environment:

    - **If you are using Windows OS:**

        ```bash
        .venv/Scripts/Activate
        ```

        If you encounter a permissions error, run this command:
        
        ```bash
          Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        ```

    - **If you are using macOS:**

      ```bash
      source venv/bin/activate
      ```
6. Run the file:

    - **If you are using Windows OS:**

        ```bash
        py executor.py
        ```

    - **If you are using macOS:**

        ```bash
        python3 executor.py
        ```

### Hi! What do you want to execute?

  1. Benchmarks  
  2. Epochs
  3. Large Images  
  4. Smoke-tests  
  5. Snapshot  
  6. VA
  7. Va_playwright  

  **Select an option by typing the number** (e.g., `1` for Benchmarks).

---

When you run the `executor.py` script, this menu will appear asking you to choose an option. Based on your selection, the corresponding task will be executed. Just type the number corresponding to your choice, and the script will proceed with the selected operation.

For example, if you choose `1`, it will execute the Benchmarks. Similarly, selecting any of the other options will trigger their respective actions.

For example, if you choose option 7, the VA_playwright tests will run, and the following menu will appear:
### TESTS
1. test_agentic_batsman.py
2. test_living_room.py
3. test_soda_chat.py
 A. Execite all tests in parallel.
 
With this menu, the user can run each test individually or execute all tests in parallel, depending on the selected option.


**Author**: Luisa Fernanda Aristizabal Giraldo
**Position**: Tester QA





















