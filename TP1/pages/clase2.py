import io
import streamlit as st
import utils

from PIL import Image, ImageEnhance, ImageOps

def show_class():
    utils.title(
        "Clase 2 - Flujo de trabajo",
        "Cargá, preprocesá, transformá y analizá la imagen.",
    )

    if "image_bytes" not in st.session_state:
        st.warning("Primero cargá una imagen desde Inicio.")
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
        "Elegí una transformación",
        ["Sin transformación", "Rotar 90°", "Voltear horizontalmente", "Reducir al 50%"],
        width="content",
    )

    transformed_image = processed_image
    if transformation == "Rotar 90°":
        transformed_image = processed_image.rotate(90, expand=True)
    elif transformation == "Voltear horizontalmente":
        transformed_image = ImageOps.mirror(processed_image)
    elif transformation == "Reducir al 50%":
        transformed_image = processed_image.resize(
            (processed_image.width // 2, processed_image.height // 2)
        )

    st.image(transformed_image, caption="Resultado de la transformación", width=768)

    st.divider()
    st.subheader("Análisis")
    width, height = transformed_image.size
    columns = st.columns(3)
    columns[0].metric("Ancho", f"{width} px")
    columns[1].metric("Alto", f"{height} px")
    columns[2].metric("Canales", len(transformed_image.getbands()))

