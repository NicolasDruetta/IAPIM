import streamlit as st
import cv2 #pip install opencv-python ( debemos instalar esa libreria)
import numpy as np
from PIL import Image

# Título de la aplicación
st.title("Aplicación de Filtros Básicos de Imágenes")

# Subida de imagen
uploaded_file = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Convertir la imagen cargada a un formato compatible
    image = Image.open(uploaded_file)
    image_np = np.array(image)
    # Mostrar la imagen original
    st.subheader("Imagen Original")
    st.image(image, caption="Imagen Original", use_container_width=True)

    # Seleccionar el filtro a aplicar
    filtro = st.selectbox(
        "Selecciona un filtro para aplicar:",
        ["Escala de grises", "Suavizado (Blur)", "Detección de bordes (Canny)"]
    )
    # Procesar la imagen según el filtro seleccionado
    if filtro == "Escala de grises":
        # Convertir a escala de grises
        processed_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        st.subheader("Imagen en Escala de Grises")
        st.image(processed_image, caption="Imagen en Escala de Grises", use_container_width=True, channels="GRAY")

    elif filtro == "Suavizado (Blur)":
        # Aplicar suavizado
        processed_image = cv2.GaussianBlur(image_np, (15, 15), 0)
        st.subheader("Imagen Suavizada")
        st.image(processed_image, caption="Imagen Suavizada", use_container_width=True)

    elif filtro == "Detección de bordes (Canny)":
        # Convertir a escala de grises y detectar bordes
        gray_image = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray_image, 100, 200)
        st.subheader("Bordes Detectados")
        st.image(edges, caption="Bordes Detectados", use_container_width=True)
else:
    st.write("Por favor, sube una imagen para comenzar.")