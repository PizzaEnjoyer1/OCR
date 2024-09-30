import os
import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
import time

# Configurar la carpeta temporal
if not os.path.exists("temp"):
    os.mkdir("temp")

st.title("Reconocimiento óptico de Caracteres")

img_file_buffer = st.camera_input("Toma una Foto")

with st.sidebar:
    filtro = st.radio("Aplicar Filtro", ('Con Filtro', 'Sin Filtro'))

# Inicializar variables de estado
text = ""
audio_file_name = ""

if img_file_buffer is not None:
    # Leer el buffer de la imagen con OpenCV
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    
    # Mostrar el texto reconocido
    st.write(text)

    # Limpiar el audio previo
    if audio_file_name and os.path.exists(audio_file_name):
        os.remove(audio_file_name)

    # Botón para generar audio
    if st.button("Generar Audio"):
        if text:
            # Mostrar el GIF de carga
            gif_placeholder = st.empty()
            gif_placeholder.image("loading.gif")  # Asegúrate de tener un archivo GIF llamado loading.gif en tu directorio

            # Generar el audio
            tts = gTTS(text=text, lang='es')  # Cambia 'es' por el idioma que necesites
            audio_file_name = f"temp/audio_{int(time.time())}.mp3"
            tts.save(audio_file_name)

            # Reproducir el audio
            audio_file = open(audio_file_name, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

            # Quitar el GIF de carga
            gif_placeholder.empty()

            # Opcional: eliminar el archivo de audio después de reproducirlo (descomentar si es necesario)
            # os.remove(audio_file_name)

# Opción para eliminar el texto y audio si se toma una nueva foto
if st.button("Borrar Texto y Audio"):
    text = ""
    audio_file_name = ""
    st.write("")  # Limpiar la visualización del texto
