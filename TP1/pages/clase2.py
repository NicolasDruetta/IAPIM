import io
import streamlit as st
import utils

from PIL import Image, ImageEnhance, ImageOps

def show_class():
    utils.title(
        "Clase 2 - Flujo de trabajo",
        "Cargue, preprocese, transforme y analice la imagen.",
    )

    if "image_bytes" not in st.session_state:
        st.warning("Primero cargue una imagen desde Inicio.")
        return

    image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")

    st.subheader("Imagen de entrada")
    st.image(image, caption=st.session_state.image_name, width=768)

    st.divider()
    st.subheader("Preprocesamiento")
    grayscale = st.checkbox("Convertir a escala de grises")
    enhance_contrast = st.checkbox("Mejorar contraste")

    processed_image = image
    if grayscale:
        processed_image = processed_image.convert("L").convert("RGB")
    if enhance_contrast:
        processed_image = ImageEnhance.Contrast(processed_image).enhance(1.5)

    st.image(processed_image, caption="Resultado del preprocesamiento", width=768)

    st.divider()
    st.subheader("Transformación")
    transformation = st.selectbox(
        "Elija una transformación",
        [
            "Sin transformación",
            "Rotar 90°",
            "Rotar 180°",
            "Rotar 270°",
            "Voltear horizontalmente",
            "Voltear verticalmente",
            "Escalar al 25%",
            "Escalar al 50%",
            "Escalar al 75%",
            "Recortar el centro",
        ],
    )

    transformed_image = processed_image
    if transformation == "Rotar 90°":
        transformed_image = processed_image.rotate(90, expand=True)
    elif transformation == "Rotar 180°":
        transformed_image = processed_image.rotate(180, expand=True)
    elif transformation == "Rotar 270°":
        transformed_image = processed_image.rotate(270, expand=True)
    elif transformation == "Voltear horizontalmente":
        transformed_image = ImageOps.mirror(processed_image)
    elif transformation == "Voltear verticalmente":
        transformed_image = ImageOps.flip(processed_image)
    elif transformation.startswith("Escalar al"):
        scale = int(transformation.split()[2].rstrip("%")) / 100
        transformed_image = processed_image.resize(
            (
                round(processed_image.width * scale),
                round(processed_image.height * scale),
            )
        )
    elif transformation == "Recortar el centro":
        left = processed_image.width // 4
        top = processed_image.height // 4
        right = processed_image.width - left
        bottom = processed_image.height - top
        transformed_image = processed_image.crop((left, top, right, bottom))

    width, height = transformed_image.size
    display_width = min(width, 768)
    st.image(
        transformed_image,
        caption=f"Resultado de la transformación: {width} x {height} px",
        width=display_width,
    )
