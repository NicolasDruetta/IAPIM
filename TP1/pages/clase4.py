import io
import functions as fn
import streamlit as st

from PIL import Image, ImageEnhance, ImageOps

def body_class4():
    st.title("Clase 4: Operaciones básicas sobre imágenes")

    fn.st_subheader(
        "Imagen original",
        "Muestra la imagen cargada antes de aplicar una operación.",
    )
    image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
    fn.show_original_image(image, st.session_state.image_name)

    fn.st_subheader(
        "Operación",
        "Permite modificar la luminosidad, el contraste o los colores de la imagen.",
    )
    operation = st.selectbox(
        "Elija una operación",
        [
            "Imagen original",
            "Aumentar brillo",
            "Reducir brillo",
            "Aumentar contraste",
            "Invertir colores",
        ],
    )

    result = image
    if operation == "Aumentar brillo":
        result = ImageEnhance.Brightness(image).enhance(1.5)
    elif operation == "Reducir brillo":
        result = ImageEnhance.Brightness(image).enhance(0.5)
    elif operation == "Aumentar contraste":
        result = ImageEnhance.Contrast(image).enhance(1.8)
    elif operation == "Invertir colores":
        result = ImageOps.invert(image)

    fn.st_image(
        result,
        caption=f"Resultado: {operation}",
    )
