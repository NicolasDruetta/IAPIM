import io
import functions as fn
import streamlit as st

from PIL import Image, ImageFilter

def body_class3():
    st.title("Clase 3 - Filtros básicos")

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
    filter_name = st.selectbox(
        "Elija un filtro",
        [
            "Imagen original",
            "Escala de grises",
            "Desenfoque gaussiano",
            "Detección de bordes",
        ],
    )

    filtered_image = image
    if filter_name == "Escala de grises":
        filtered_image = image.convert("L").convert("RGB")
    elif filter_name == "Desenfoque gaussiano":
        filtered_image = image.filter(ImageFilter.GaussianBlur(radius=2))
    elif filter_name == "Detección de bordes":
        filtered_image = image.convert("L").filter(ImageFilter.FIND_EDGES)
    fn.st_image(
        filtered_image,
        caption=f"Resultado: {filter_name}",
    )
