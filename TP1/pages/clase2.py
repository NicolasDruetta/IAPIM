import io
import functions as fn
import streamlit as st

from PIL import Image, ImageEnhance, ImageOps

def body_class2():
    st.title("Clase 2 - Flujo de trabajo")

    fn.st_subheader(
        "Imagen original",
        "Muestra la imagen cargada antes de procesarla.",
    )
    image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
    fn.show_original_image(image, st.session_state.image_name)

    fn.st_subheader(
        "Preprocesamiento",
        "Permite preparar la imagen antes de aplicar transformaciones.",
    )
    grayscale = st.checkbox("Convertir a escala de grises")
    enhance_contrast = st.checkbox("Mejorar contraste")
    processed_image = image
    if grayscale:
        processed_image = processed_image.convert("L").convert("RGB")
    if enhance_contrast:
        processed_image = ImageEnhance.Contrast(processed_image).enhance(1.5)
    fn.st_image(
        processed_image,
        caption="Resultado del preprocesamiento",
    )

    fn.st_subheader(
        "Transformación",
        "Permite cambiar la posición, el sentido o el tamaño de la imagen.",
    )
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
    fn.st_image(
        transformed_image,
        caption=f"Resultado de la transformación: {width} x {height} px",
    )
