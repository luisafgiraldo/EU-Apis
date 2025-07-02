import requests

def temporal_localization(url: str, video_path: str, prompt: str, chunk_length: int, api_key: str) -> dict:
    """
    Envía un video para detección temporal y devuelve la respuesta JSON.
    """
    headers = {
        "Authorization": f"Basic {api_key}"
    }
    data = {
        "prompt": prompt,
        "chunk_length": chunk_length,
        "model": "internlm-xcomposer"
    }

    try:
        with open(video_path, "rb") as video_file:
            files = {"video": video_file}
            response = requests.post(url, files=files, data=data, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        print(response_json)
        print("\033[32m============================== 1 passed video_temporal_localization ==============================\x1b[0m")
        return response_json

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        print("\033[31m============================== 1 failed video_temporal_localization ==============================\x1b[0m")
        return {}

