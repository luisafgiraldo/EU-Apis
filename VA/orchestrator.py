import pytest
import utils as u
import os
import time
from Florencev2QA import create




IMAGES_PATH_BASE = os.path.join("VA", "Images")

# URL_BASE = "https://api.va.staging.landing.ai/v1/tools"
# URL_BASE = "https://api.va.landing.ai/v1/tools"

# API_KEY = "eTdiN3pjM2dpbWlhbnIwMzJlcDdvOnFoTlZZNDIwTk9ORDV4U3M5UVA3R0JZN1VrS3JhVXV0"
# API_KEY = "dmd1bDcxaWJ1MDU3Z3IxczU5cjUyOjlsZDNuczR0WGdKN292S0lDbXNTVkx2bE9mS2NzNlRT"

CONFIGS = [
    {
        "URL_BASE": "https://api.va.staging.landing.ai/v1/tools",
        "API_KEY": "eTdiN3pjM2dpbWlhbnIwMzJlcDdvOnFoTlZZNDIwTk9ORDV4U3M5UVA3R0JZN1VrS3JhVXV0"
    },
    {
        "URL_BASE": "https://api.va.landing.ai/v1/tools",
        "API_KEY": "dmd1bDcxaWJ1MDU3Z3IxczU5cjUyOjlsZDNuczR0WGdKN292S0lDbXNTVkx2bE9mS2NzNlRT"
    }
]

# 🔁 Interactive user input
user_choice = input("Which environment do you want to use? (1 = Staging, 2 = Production, 3 = Both): ").strip()

if user_choice == "1":
    CONFIGS = [CONFIGS[0]]
elif user_choice == "2":
    CONFIGS = [CONFIGS[1]]
# If "3", leave CONFIGS unchanged (use both)

print(f"✅ Selected configuration(s): {[config['URL_BASE'] for config in CONFIGS]}")

@pytest.fixture(scope="module", autouse=True)
def timer():
    start_time = time.time()
    yield
    end_time = time.time()
    total_time_minutes = (end_time - start_time) / 60
    print(f"Total execution time: {total_time_minutes:.2f} minutes")

import os
import pytest
import pandas as pd
import Agentic_Object_Detection
import IXC25VQA
from Temporal_localization import temporal_localization
import utils as u  # Asumo que 'u' es tu módulo utilitario

allowed_extensions = ['.jpg', '.jpeg', '.png', '.heic', '.webp', '.avif', '.mp4', '.mov']
IMAGES_PATH_BASE = "VA/Images"  # Asegúrate que este path sea correcto


@pytest.mark.parametrize("config", CONFIGS)
def test_text_to_instance_segmentation(config):
    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']

    import Text_to_segmentation
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Sam2")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)

    if IMAGE_PATH is None:
        print("❌ No se encontró ninguna imagen válida en el directorio.")
        assert False, "No se encontró ninguna imagen válida en el directorio."

    if not any(IMAGE_PATH.lower().endswith(ext) for ext in allowed_extensions):
        print(f"❌ Formato de archivo no permitido: {IMAGE_PATH}")
        assert False, f"Formato de archivo no permitido: {IMAGE_PATH}"

    URL = f"{URL_BASE}/text-to-instance-segmentation"
    PROMPT = "apple"

    result = Text_to_segmentation.create(URL, IMAGE_PATH, PROMPT, API_KEY)
    assert result is not None, "Text To Instance Segmentation result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_video_temporal_localization(config):
    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']

    VIDEO_DIR = u.union_path(IMAGES_PATH_BASE, "IXC25 Temporal Localization")
    VIDEO_PATH = u.first_file_finder(VIDEO_DIR)
    URL = f"{URL_BASE}/video-temporal-localization"
    PROMPT = "Describe lo que ocurre en el video"
    CHUNK_LENGTH = 5

    result = temporal_localization(URL, VIDEO_PATH, PROMPT, CHUNK_LENGTH, API_KEY)
    assert result, "Response JSON is empty or None"

@pytest.mark.parametrize("config", CONFIGS)
def test_ixc25(config):
    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']

    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "IXC25")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR, allowed_extensions)

    URL = f"{URL_BASE}/internlm-xcomposer2"
    PROMPT = "What color is the building behind the car?"

    result = IXC25VQA.create(URL, IMAGE_PATH, PROMPT, API_KEY)
    assert result is not None, "IXC25 result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_agentic_document_analysis(config):
    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import Agentic_Document_Analysis
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "ADE")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)

    if IMAGE_PATH is None:
        print("❌ No se encontró ninguna imagen válida en el directorio.")
        assert False, "No se encontró ninguna imagen válida en el directorio."
    
    if not any(IMAGE_PATH.lower().endswith(ext) for ext in allowed_extensions):
        print(f"❌ Formato de archivo no permitido: {IMAGE_PATH}")
        assert False, f"Formato de archivo no permitido: {IMAGE_PATH}"

    URL = f"{URL_BASE}/agentic-document-analysis"
    PROMPT = "Describe the document content"

    result = Agentic_Document_Analysis.create(URL, IMAGE_PATH, PROMPT, API_KEY)
    assert not result.empty, "Agentic Document Analysis result is empty"

@pytest.mark.parametrize("config", CONFIGS)
def test_agentic_od(config):
    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']

    import Agentic_Object_Detection
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Agentic Object Detection")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    
    if IMAGE_PATH is None:
        print("❌ No se encontró ninguna imagen válida en el directorio.")
        assert False, "No se encontró ninguna imagen válida en el directorio."  # Cambié return por assert
    
    if not any(IMAGE_PATH.lower().endswith(ext) for ext in allowed_extensions):
        print(f"❌ Formato de archivo no permitido: {IMAGE_PATH}")
        assert False, f"Formato de archivo no permitido: {IMAGE_PATH}"  # Cambié return por assert
    
    URL = f"{URL_BASE}/agentic-object-detection"
    PROMPT = "Detect Aircraft"

    result = Agentic_Object_Detection.create(URL, IMAGE_PATH, PROMPT, API_KEY)
    assert result is not None, "Agentic Object Detection result is None"


@pytest.mark.parametrize("config", CONFIGS)
def test_owlv2(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']

    import os
    print("Current working directory:", os.getcwd())
    import Owlv2
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "OWLv2 Image")
    print(f"IMAGE_DIR: {IMAGE_DIR}")  # Verifica la ruta
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    print(f"IMAGE_PATH: {IMAGE_PATH}")  # Verifica si encuentra un archivo
    assert IMAGE_PATH is not None, "No se encontró una imagen en el directorio"

    URL = f"{URL_BASE}/owlv2"
    PROMPTS = "Detect animals"
    result = Owlv2.create(URL, IMAGE_PATH, PROMPTS, API_KEY)
    assert result is not None, "Owlv2 result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_countgd(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import Countgd
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Countgd Counting")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/countgd"
    PROMPTS = "Dogs"
    result = Countgd.create(URL, IMAGE_PATH, PROMPTS, API_KEY)
    assert result is not None, "Countgd result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_florencev2_roberta(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import Florencev2
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Florence-2 Roberta Vqa")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/florence2"
    TASK = "<CAPTION>"
    result = Florencev2.create(URL, IMAGE_PATH, TASK, API_KEY)
    assert result is not None, "Florencev2 Roberta result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_florencev2_ocr(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import Florencev2
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Florence2 OCR")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/florence2"
    TASK = "<OCR>"
    result = Florencev2.create(URL, IMAGE_PATH, TASK, API_KEY)
    assert result is not None, "Florencev2 OCR result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_florencev2qa(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import Florencev2QA
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "IXC25 Image VQA")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/florence2-qa"
    QUESTION = "What color is the car?"
    result = Florencev2QA.create(URL, IMAGE_PATH, QUESTION, API_KEY)
    assert result is not None, "Florencev2QA result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_depth_anything_v2(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import Depth_Anything_V2
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Depth Anything V2")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/depth-anything-v2"
    result = Depth_Anything_V2.create(URL, IMAGE_PATH, API_KEY)
    assert result is not None, "Depth Anything V2 result is None"

# def test_text_to_od(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
#     import Text_To_Od
#     IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "OWLv2 Video")
#     VIDEO_PATH = u.first_file_finder(IMAGE_DIR)
#     URL = f"{URL_BASE}/text-to-object-detection"
#     PROMPTS = "elephants"
#     result = Text_To_Od.create(URL, VIDEO_PATH, PROMPTS, API_KEY)
#     assert result is not None, "Text To Od result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_nsfw_classification(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import nsfw_classification
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "ViT NSFW Classification")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/nsfw-classification"
    result = nsfw_classification.create(URL, IMAGE_PATH, API_KEY)
    assert result is not None, "NSFW Classification result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_wsi_embedding(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import Wsi_Embedding
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Tool Wsi Embedding")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/wsi-embedding"
    result = Wsi_Embedding.create(URL, IMAGE_PATH, API_KEY)
    assert result is not None, "WSI Embedding result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_qr_reader(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import qr_reader
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Tool Qr Reader")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/qr-reader"
    result = qr_reader.create(URL, IMAGE_PATH, API_KEY)
    assert result is not None, "QR Reader result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_loca(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import loca
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Loca Zero Shot Counting")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/loca"
    result = loca.create(URL, IMAGE_PATH, API_KEY)
    assert result is not None, "Loca result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_pose_detection(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import Pose_Detection
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Pose Detection")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/pose-detector"
    result = Pose_Detection.create(URL, IMAGE_PATH, API_KEY)
    assert result is not None, "Pose Detection result is None"

@pytest.mark.parametrize("config", CONFIGS)
def test_barcode_reader(config):

    URL_BASE = config['URL_BASE']
    API_KEY = config['API_KEY']
    
    import Barcode_Reader
    IMAGE_DIR = u.union_path(IMAGES_PATH_BASE, "Barcode Reader")
    IMAGE_PATH = u.first_file_finder(IMAGE_DIR)
    URL = f"{URL_BASE}/barcode-reader"
    result = Barcode_Reader.create(URL, IMAGE_PATH, API_KEY)
    assert result is not None, "Barcode Reader result is None"
