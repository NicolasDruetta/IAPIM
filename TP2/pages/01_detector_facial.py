import cv2
import numpy as np
import streamlit as st

from functions import configure_page
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

def fit_result_image(image_rgb):
    """Ajusta la imagen procesada al tamaño visual del cuadro de resultado."""
    target_width = 640
    target_height = 400
    image_height, image_width = image_rgb.shape[:2]
    scale = min(target_width / image_width, target_height / image_height)
    resized_width = int(image_width * scale)
    resized_height = int(image_height * scale)
    resized_image = cv2.resize(
        image_rgb,
        (resized_width, resized_height),
        interpolation=cv2.INTER_AREA,
    )
    fitted_image = np.full(
        (target_height, target_width, 3),
        45,
        dtype=np.uint8,
    )
    offset_x = (target_width - resized_width) // 2
    offset_y = (target_height - resized_height) // 2
    fitted_image[
        offset_y:offset_y + resized_height,
        offset_x:offset_x + resized_width,
    ] = resized_image
    return fitted_image

configure_page("IAPIM - Vision Lab")

title_column, home_column = st.columns([5, 1])

with title_column:
    st.title("01 – Detector facial")
    st.write("Capturá una fotografía y analizala para detectar rostros.")

with home_column:
    st.write("")
    if st.button("Volver al Inicio", width="stretch"):
        st.switch_page("main.py")

if "camera_key" not in st.session_state:
    st.session_state.camera_key = 0
if "captured_image_bytes" not in st.session_state:
    st.session_state.captured_image_bytes = None
if "detection_error" not in st.session_state:
    st.session_state.detection_error = None
if "detection_result" not in st.session_state:
    st.session_state.detection_result = None
if "face_count" not in st.session_state:
    st.session_state.face_count = 0

empty_result_image = np.full((400, 640, 3), 45, dtype=np.uint8)

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Captura de imagen")
    st.write("Tomá una fotografía con la cámara")
    captured_image = st.camera_input(
        "Cámara",
        key=f"camera_input_{st.session_state.camera_key}",
        label_visibility="collapsed",
    )

    if captured_image is not None:
        captured_image_bytes = captured_image.getvalue()

        if st.session_state.captured_image_bytes != captured_image_bytes:
            st.session_state.captured_image_bytes = captured_image_bytes

            try:
                processed_image, face_count = detect_faces(captured_image_bytes)
            except (RuntimeError, ValueError) as error:
                st.session_state.detection_error = str(error)
                st.session_state.detection_result = None
                st.session_state.face_count = 0
            else:
                st.session_state.detection_error = None
                st.session_state.detection_result = processed_image
                st.session_state.face_count = face_count
    elif st.session_state.captured_image_bytes is not None:
        st.session_state.camera_key += 1
        st.session_state.captured_image_bytes = None
        st.session_state.detection_error = None
        st.session_state.detection_result = None
        st.session_state.face_count = 0
        st.rerun()

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualizá la fotografía con los rostros detectados")

    if st.session_state.detection_error:
        st.error(st.session_state.detection_error)
    elif st.session_state.detection_result is None:
        st.image(empty_result_image, width="stretch")
    else:
        st.image(
            fit_result_image(st.session_state.detection_result),
            caption="Fotografía procesada",
            width="stretch",
        )
        st.metric("Rostros detectados", st.session_state.face_count)

        if st.session_state.face_count == 0:
            st.warning("No se detectaron rostros en la fotografía.")
