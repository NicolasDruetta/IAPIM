import io
import streamlit as st

from PIL import Image
from utils import get_dimensions_text

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
    st.subheader("Información básica")
    width, height = image.size
    st.write(f"**Nombre:** {st.session_state.image_name}")
    st.write(f"**Dimensiones:** {width} x {height} píxeles")
    st.write(f"**Canales:** {len(image.getbands())}")

    st.divider()
    st.subheader("Canales de color")
    for channel in image.getbands():
        st.image(
            image.getchannel(channel),
            caption=f"Canal {channel}",
            width=768,
        )
