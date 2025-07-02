import os

# Configurar las variables de entorno
os.environ['VISION_AGENT_API_KEY'] = 'eTdiN3pjM2dpbWlhbnIwMzJlcDdvOnFoTlZZNDIwTk9ORDV4U3M5UVA3R0JZN1VrS3JhVXV0'
os.environ['LANDINGAI_URL'] = "https://api.va.staging.landing.ai"

import vision_agent.tools as T
import matplotlib.pyplot as plt

# Ruta de la imagen
image_path = "/Users/luisaaristizabal/Desktop/image1.png"

# Cargar imagen
image = T.load_image(image_path)

# Detectar personas en la imagen
dets = T.countgd_object_detection("person", image)

# Dibujar los bounding boxes sobre la imagen
viz = T.overlay_bounding_boxes(image, dets)

# Guardar la imagen con detecciones
output_path = "/Users/luisaaristizabal/Downloads/people_detected.png"
T.save_image(viz, output_path)

# Mostrar la imagen
plt.imshow(viz)
plt.axis("off")  # Ocultar los ejes
plt.show()
