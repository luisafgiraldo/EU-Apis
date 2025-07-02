import requests


def SnapShotExport(api_key: str, url: str):
    headers = {"apikey": api_key}
    querystring = {"timeout": "300"}
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        response_data = response.json()
        print(response_data)  # Inspeccionar la estructura de la respuesta
        # Acceder a la data esperada que es un diccionario
        if isinstance(response_data["data"], dict):
            export = response_data["data"]
            download_url = export.get("downloadUrl")
            download_expires = export.get("downloadExpiresAt")
            print(f"Download URL: {download_url}")
            print(f"Download Expires At: {download_expires}")
            print("Get successfully!")
        else:
            print("Unexpected response structure or 'data' is not a dictionary.")
            export = None
    else:
        print(f"Error get export: {response.text}")
        export = None

    return export


def download_file_from_url(url, local_filename):
    # Hace una solicitud GET para descargar el archivo
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Lanza un error si la solicitud falla
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(
                chunk_size=8192
            ):  # Descarga el archivo en bloques
                file.write(chunk)
    return local_filename
