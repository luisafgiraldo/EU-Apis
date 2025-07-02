import requests

# URL de la API
url = "https://lnedkxw-webendpoint.sandbox.staging.landing.ai/inference"

# URL del video (debe ir en 'video_path' según el error anterior)
video_url = "https://media.istockphoto.com/id/1255754954/es/v%C3%ADdeo/school-of-fish-sharks-nadan-en-c%C3%ADrculo.jpg?s=640x640&k=20&c=_DIjdO17k7TJiOG-XIJ_cHgkBg_WDN1rnqKqaFJg3_I="

# Encabezados con autenticación
headers = {
    "Authorization": "Basic eTdiN3pjM2dpbWlhbnIwMzJlcDdvOnFoTlZZNDIwTk9ORDV4U3M5UVA3R0JZN1VrS3JhVXV0",
    "Content-Type": "application/x-www-form-urlencoded"  # O "application/json" si la API lo requiere
}

# Enviar la URL del video como parámetro en el body
data = {"video_path": video_url}

# Hacer la solicitud
response = requests.post(url, data=data, headers=headers)

# Imprimir la respuesta
print(response.status_code)
print(response.json())


