import io
import streamlit as st

from PIL import Image
from utils import get_dimensions_text

def show_basic_info(image):
    width, height = image.size

    st.subheader("Información básica")
    st.write(f"**Nombre:** {st.session_state.image_name}")
    st.write(f"**Dimensiones:** {width} x {height} píxeles")
    st.write(f"**Canales:** {len(image.getbands())}")
    st.write(f"**Modo:** {image.mode}")

def show_color_channels(image):
    st.subheader("Canales de color")
    columns = st.columns(3)

    for column, channel in zip(columns, image.getbands()):
        with column:
            st.image(
                image.getchannel(channel),
                caption=f"Canal {channel}",
                width="stretch",
            )

def show_class():
    st.title("Clase 1 - Introducción al procesamiento de imágenes")

    if "image_bytes" not in st.session_state:
        st.warning("Primero cargá una imagen desde Inicio.")
        return

    image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
    dimensions = get_dimensions_text(image)

    st.subheader("Imagen original")
    st.image(image, caption=dimensions, width=768)

    st.divider()
    show_basic_info(image)

    st.divider()
    show_color_channels(image)

    st.divider()
    st.subheader("Escala de grises")
    st.image(image.convert("L"), caption="Imagen en escala de grises", width=768)
