import cv2
import functions as fn
import io
import numpy as np
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
        "Manipulación de píxeles",
        "Permite recortar, redimensionar y rotar la imagen.",
    )
    pixel_operation = st.radio(
        "",
        [
            "Imagen original",
            "Recortar",
            "Redimensionar al 50%",
            "Rotar 45°",
        ],
        horizontal=True,
        key="class4_pixel_operation",
        label_visibility="collapsed",
    )

    pixel_image = np.array(image)
    pixel_cod = ("np.array(image)")
    pixel_width = st.session_state.default_width

    if pixel_operation == "Recortar":
        height, width = pixel_image.shape[:2]
        pixel_image = pixel_image[
            height // 4:height * 3 // 4,
            width // 4:width * 3 // 4,
        ]
        pixel_cod = ("pixel_image[height // 4:height * 3 // 4, width // 4:width * 3 // 4]")
    elif pixel_operation == "Redimensionar al 50%":
        pixel_image = cv2.resize(
            pixel_image,
            (image.width // 2, image.height // 2),
            interpolation=cv2.INTER_LINEAR,
        )
        pixel_width = st.session_state.default_width // 2
        pixel_cod = ("cv2.resize(pixel_image, (image.width // 2, image.height // 2), interpolation=cv2.INTER_LINEAR)")
    elif pixel_operation == "Rotar 45°":
        height, width = pixel_image.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, 45, 1.0)
        pixel_image = cv2.warpAffine(pixel_image, rotation_matrix, (width, height))
        pixel_cod = ("cv2.warpAffine(pixel_image, cv2.getRotationMatrix2D(center, 45, 1.0), (width, height))")

    fn.st_image(pixel_image, caption=pixel_cod, width=pixel_width)

    fn.st_subheader(
        "Espacios de color",
        "Permite convertir la imagen entre RGB, escala de grises, HSV y LAB.",
    )
    color_operation = st.radio(
        "",
        [
            "Imagen original",
            "Escala de grises",
            "RGB a HSV",
            "RGB a LAB",
        ],
        horizontal=True,
        key="class4_color_operation",
        label_visibility="collapsed",
    )

    color_image = np.array(image)
    color_cod = ("np.array(image)")

    if color_operation == "Escala de grises":
        color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)
        color_cod = ("cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)")
    elif color_operation == "RGB a HSV":
        color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2HSV)
        color_cod = ("cv2.cvtColor(color_image, cv2.COLOR_RGB2HSV)")
    elif color_operation == "RGB a LAB":
        color_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2LAB)
        color_cod = ("cv2.cvtColor(color_image, cv2.COLOR_RGB2LAB)")

    fn.st_image(color_image, caption=color_cod)

    fn.st_subheader(
        "Brillo, contraste y color",
        "Permite ajustar la luminosidad, el contraste o invertir los colores.",
    )
    adjustment_operation = st.radio(
        "",
        [
            "Imagen original",
            "Aumentar brillo",
            "Reducir brillo",
            "Aumentar contraste",
            "Invertir colores",
        ],
        horizontal=True,
        key="class4_adjustment_operation",
        label_visibility="collapsed",
    )

    adjustment_image = image
    adjustment_cod = "image"

    if adjustment_operation == "Aumentar brillo":
        adjustment_image = ImageEnhance.Brightness(image).enhance(1.5)
        adjustment_cod = ("ImageEnhance.Brightness(image).enhance(1.5)")
    elif adjustment_operation == "Reducir brillo":
        adjustment_image = ImageEnhance.Brightness(image).enhance(0.5)
        adjustment_cod = ("ImageEnhance.Brightness(image).enhance(0.5)")
    elif adjustment_operation == "Aumentar contraste":
        adjustment_image = ImageEnhance.Contrast(image).enhance(1.8)
        adjustment_cod = ("ImageEnhance.Contrast(image).enhance(1.8)")
    elif adjustment_operation == "Invertir colores":
        adjustment_image = ImageOps.invert(image)
        adjustment_cod = ("ImageOps.invert(image)")

    fn.st_image(adjustment_image, caption=adjustment_cod)
