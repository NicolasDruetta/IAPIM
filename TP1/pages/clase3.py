import cv2
import functions as fn
import io
import numpy as np
import streamlit as st

from PIL import Image

def body_class3():
    st.title("Clase 3: Streamlit")

    fn.st_subheader(
        "Imagen original",
        "Muestra la imagen cargada antes de aplicar un filtro.",
    )
    image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
    fn.show_original_image(image, st.session_state.image_name)

    fn.st_subheader(
        "Filtro",
        "Elija una opción para modificar o resaltar partes de la imagen.",
    )
    filter_name = st.radio(
        "Elija un filtro",
        [
            "Imagen original",
            "Escala de grises",
            "Suavizado (Blur)",
            "Detección de bordes (Canny)",
        ],
        horizontal=True,
    )

    image_array = np.array(image)
    filtered_image = image_array
    filter_codex = "image_array"

    if filter_name == "Escala de grises":
        filtered_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        filter_codex = ("cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)")
    elif filter_name == "Suavizado (Blur)":
        filtered_image = cv2.GaussianBlur(image_array, (15, 15), 0)
        filter_codex = ("cv2.GaussianBlur(image_array, (15, 15), 0)")
    elif filter_name == "Detección de bordes (Canny)":
        gray_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        filtered_image = cv2.Canny(gray_image, 100, 200)
        filter_codex = ("cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY); cv2.Canny(gray_image, 100, 200)")
    fn.st_image(
        filtered_image,
        caption=filter_codex,
    )
