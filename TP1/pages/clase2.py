import cv2
import functions as fn
import io
import numpy as np
import streamlit as st

from PIL import Image, ImageFilter, ImageOps
from skimage import color, filters, transform

def body_class2():
    st.title("Clase 2: Herramientas y Bibliotecas")

    fn.st_subheader(
        "Imagen original",
        "Muestra la imagen cargada sin aplicar modificaciones.",
    )
    image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
    fn.show_original_image(image, st.session_state.image_name)

    fn.st_subheader(
        "Pillow",
        "Permite abrir, convertir, redimensionar y aplicar filtros a imágenes.",
    )
    pillow_operation = st.radio(
        "",
        [
            "Imagen original",
            "Escala de grises",
            "Redimensionar al 50%",
            "Rotar 90°",
            "Voltear horizontalmente",
            "Desenfoque gaussiano",
            "Detección de bordes",
        ],
        horizontal=True,
        key="pillow_operation",
        label_visibility="collapsed",
    )
    pillow_image = image
    pillow_code = "pillow_image = image"
    if pillow_operation == "Escala de grises":
        pillow_image = ImageOps.grayscale(image)
        pillow_code = "pillow_image = ImageOps.grayscale(image)"
    elif pillow_operation == "Redimensionar al 50%":
        pillow_image = image.resize((image.width // 2, image.height // 2))
        pillow_code = (
            "pillow_image = image.resize("
            "(image.width // 2, image.height // 2)"
            ")"
        )
    elif pillow_operation == "Rotar 90°":
        pillow_image = image.rotate(90, expand=True)
        pillow_code = "pillow_image = image.rotate(90, expand=True)"
    elif pillow_operation == "Voltear horizontalmente":
        pillow_image = ImageOps.mirror(image)
        pillow_code = "pillow_image = ImageOps.mirror(image)"
    elif pillow_operation == "Desenfoque gaussiano":
        pillow_image = image.filter(ImageFilter.GaussianBlur(radius=5))
        pillow_code = (
            "pillow_image = image.filter("
            "ImageFilter.GaussianBlur(radius=5)"
            ")"
        )
    elif pillow_operation == "Detección de bordes":
        pillow_image = image.filter(ImageFilter.FIND_EDGES)
        pillow_code = "pillow_image = image.filter(ImageFilter.FIND_EDGES)"
    fn.st_image(pillow_image, caption=pillow_code)

    fn.st_subheader(
        "OpenCV",
        "Ofrece operaciones rápidas para procesamiento y visión por computadora.",
    )
    opencv_operation = st.radio(
        "",
        [
            "Imagen original",
            "Escala de grises",
            "Desenfoque gaussiano",
            "Detección de bordes",
            "Redimensionar al 50%",
            "Rotar 90°",
        ],
        horizontal=True,
        key="opencv_operation",
        label_visibility="collapsed",
    )
    opencv_image = np.array(image)
    opencv_code = "opencv_image = np.array(image)"
    if opencv_operation == "Escala de grises":
        opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2GRAY)
        opencv_code = (
            "opencv_image = cv2.cvtColor("
            "opencv_image, cv2.COLOR_RGB2GRAY"
            ")"
        )
    elif opencv_operation == "Desenfoque gaussiano":
        opencv_image = cv2.GaussianBlur(opencv_image, (9, 9), 0)
        opencv_code = "opencv_image = cv2.GaussianBlur(opencv_image, (9, 9), 0)"
    elif opencv_operation == "Detección de bordes":
        gray_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2GRAY)
        opencv_image = cv2.Canny(gray_image, 100, 200)
        opencv_code = (
            "gray_image = cv2.cvtColor("
            "opencv_image, cv2.COLOR_RGB2GRAY\n"
            ")\n"
            "opencv_image = cv2.Canny(gray_image, 100, 200)"
        )
    elif opencv_operation == "Redimensionar al 50%":
        opencv_image = cv2.resize(
            opencv_image,
            (image.width // 2, image.height // 2),
        )
        opencv_code = (
            "opencv_image = cv2.resize("
            "opencv_image, (image.width // 2, image.height // 2)"
            ")"
        )
    elif opencv_operation == "Rotar 90°":
        opencv_image = cv2.rotate(opencv_image, cv2.ROTATE_90_CLOCKWISE)
        opencv_code = (
            "opencv_image = cv2.rotate("
            "opencv_image, cv2.ROTATE_90_CLOCKWISE"
            ")"
        )
    fn.st_image(opencv_image, caption=opencv_code)

    fn.st_subheader(
        "Scikit-image",
        "Incluye filtros y transformaciones para el análisis científico de imágenes.",
    )
    skimage_operation = st.radio(
        "",
        [
            "Imagen original",
            "Escala de grises",
            "Desenfoque gaussiano",
            "Detección de bordes",
            "Redimensionar al 50%",
        ],
        horizontal=True,
        key="skimage_operation",
        label_visibility="collapsed",
    )
    skimage_image = np.array(image)
    skimage_code = "skimage_image = np.array(image)"
    if skimage_operation == "Escala de grises":
        skimage_image = color.rgb2gray(skimage_image)
        skimage_code = "skimage_image = color.rgb2gray(skimage_image)"
    elif skimage_operation == "Desenfoque gaussiano":
        skimage_image = filters.gaussian(skimage_image, sigma=2)
        skimage_code = "skimage_image = filters.gaussian(skimage_image, sigma=2)"
    elif skimage_operation == "Detección de bordes":
        skimage_image = filters.sobel(color.rgb2gray(skimage_image))
        skimage_code = (
            "gray_image = color.rgb2gray(skimage_image)\n"
            "skimage_image = filters.sobel(gray_image)"
        )
    elif skimage_operation == "Redimensionar al 50%":
        skimage_image = transform.resize(
            skimage_image,
            (image.height // 2, image.width // 2),
            anti_aliasing=True,
        )
        skimage_code = (
            "skimage_image = transform.resize("
            "skimage_image, (image.height // 2, image.width // 2),\n"
            "anti_aliasing=True"
            ")"
        )
    fn.st_image(skimage_image, caption=skimage_code)
