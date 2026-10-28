"""Funciones compartidas del laboratorio IAPIM Vision Lab."""

import cv2
import numpy as np
import streamlit as st

from pathlib import Path


def detect_faces(image_bytes):
    """Detecta rostros y dibuja sus rectángulos sobre una imagen."""
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía capturada.")

    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    classifier_path = (
        Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    )
    face_classifier = cv2.CascadeClassifier(str(classifier_path))

    if face_classifier.empty():
        raise RuntimeError("No se pudo cargar el clasificador Haar frontal.")

    faces = face_classifier.detectMultiScale(
        gray_image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )
    processed_image = image_bgr.copy()

    for x_coordinate, y_coordinate, width, height in faces:
        cv2.rectangle(
            processed_image,
            (x_coordinate, y_coordinate),
            (x_coordinate + width, y_coordinate + height),
            (0, 255, 0),
            2,
        )

    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
    return processed_image, len(faces)


def home():
    """Muestra la página de inicio del laboratorio."""
    st.title("IAPIM Vision Lab")
    st.subheader("Laboratorio de Visión Artificial y Procesamiento de Imágenes")
    st.write("Autor: Nicolás Druetta")

    with st.container(border=True):
        st.subheader("01 – Detector facial")
        st.write("Capturá una fotografía con la cámara y detectá los rostros presentes")
        if st.button("Abrir herramienta"):
            st.switch_page("pages/01_detector_facial.py")
