import io
import functions as fn
import streamlit as st

from PIL import Image

def body_class1():
    st.title("Clase 1 - Introducción al procesamiento de imágenes")

    fn.st_subheader(
        "Imagen original",
        "Muestra la imagen cargada sin aplicar modificaciones.",
    )
    image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
    fn.show_original_image(image, st.session_state.image_name)

    fn.st_subheader(
        "Información básica",
        "Presenta los datos principales de la imagen cargada.",
    )
    fn.show_basic_info(image)

    fn.st_subheader(
        "Escala de grises",
        "Representa la imagen usando distintos niveles de gris.",
    )
    fn.st_image(
        image.convert("L"),
        caption="Imagen en escala de grises",
    )

    fn.st_subheader(
        "Canales de color",
        "Separa la imagen en sus canales rojo, verde y azul.",
    )
    fn.show_color_channels(image)
