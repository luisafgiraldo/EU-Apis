import streamlit as st
import requests
import time
import re
from bs4 import BeautifulSoup
from collections import defaultdict

# Configuración básica de la app
st.set_page_config(page_title="Análisis de Documentos PDF", layout="wide")
st.title("📄 Analizador de Documentos con Landing AI")

uploaded_file = st.file_uploader("📤 Sube un archivo PDF", type=["pdf"])

if uploaded_file:
    st.info("⏳ Enviando el archivo a la API...")

    url = "https://api.va.staging.landing.ai/v1/tools/agentic-document-analysis"
    headers = {
        "Authorization": "Basic aWlqMmo2a2ZpbHA2ODhzY3o5ZGFlOnIzSFI5UnhCV1B5SzRyTHYySTBJSHY4WDZyTHJDaDM0"
    }

    files = {"pdf": uploaded_file}

    start_time = time.time()
    response = requests.post(url, files=files, headers=headers)
    elapsed_time = time.time() - start_time

    if response.status_code == 200:
        try:
            data = response.json()
            markdown = data["data"]["markdown"]

            # Añadir un chequeo de la estructura para saber si está realmente dividiendo las páginas
            # La clave aquí será buscar un patrón que indique claramente los números de las páginas
            page_pattern = re.compile(r'<!--.*?from page (\d+).*?-->')

            # Dividir el contenido en bloques y revisar la estructura
            chunks = re.split(page_pattern, markdown)

            # Agrupar el contenido por número de página
            pages_dict = defaultdict(str)
            for i in range(1, len(chunks), 2):
                page_num = int(chunks[i])
                html_content = chunks[i + 1]
                soup = BeautifulSoup(html_content, 'html.parser')
                clean_text = soup.get_text(separator='\n').strip()
                if clean_text:
                    pages_dict[page_num] += "\n" + clean_text

            st.success(f"✅ Documento procesado en {elapsed_time:.2f} segundos")
            st.subheader("📄 Contenido dividido por página")

            # Mostrar el contenido de cada página en un expander
            for page_number in sorted(pages_dict.keys()):
                with st.expander(f"📄 Página {page_number}"):
                    st.text(pages_dict[page_number].strip())

        except Exception as e:
            st.error("⚠️ No se pudo procesar la respuesta de la API.")
            st.text(response.text)
    else:
        st.error(f"❌ Error {response.status_code} al procesar el documento.")
        st.text(response.text)

