# Agentic_Document_Analysis.py
import requests
import pandas as pd

def create(url: str, image_path: str, prompt: str, api_key: str):
    allowed_extensions = [".jpg", ".jpeg", ".png", ".heic", ".webp", ".avif", ".mp4", ".mov"]
    if not any(image_path.lower().endswith(ext) for ext in allowed_extensions):
        print(f"❌ Formato de archivo no permitido: {image_path}")
        return pd.DataFrame()

    files = {
        "image": open(image_path, "rb")
    }

    data = {
        "prompts": prompt,
        "model": "agentic"
    }

    headers = {
        "Authorization": f"Basic {api_key}"
    }

    response = requests.post(url, files=files, data=data, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        print("✅ Response:")
        print(response_data)
        print(
            "\033[32m"
            + "============================== 1 passed Agentic_Document_Analysis.py =============================="
            + "\x1b[0m"
        )
        return pd.DataFrame([response_data])
    else:
        print(f"❌ Error {response.status_code}:")
        try:
            print(response.json())
        except Exception:
            print(response.text)
        print(
            "\033[31m"
            + "============================== 1 failed Agentic_Document_Analysis.py =============================="
            + "\x1b[0m"
        )
        return pd.DataFrame()
