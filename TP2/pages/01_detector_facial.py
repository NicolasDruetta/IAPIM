import cv2
import numpy as np
import streamlit as st

from pathlib import Path
from functions import configure_page

def detect_faces(image_bytes):
    """Detecta rostros y dibuja sus rectángulos sobre una imagen."""
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía capturada.")
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    classifier_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
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
    resized_width = max(1, int(image_width * scale))
    resized_height = max(1, int(image_height * scale))
    resized_image = cv2.resize(
        image_rgb,
        (resized_width, resized_height),
        interpolation=cv2.INTER_AREA,
    )
    fitted_image = np.full((target_height, target_width, 3), 45, dtype=np.uint8)
    offset_x = (target_width - resized_width) // 2
    offset_y = (target_height - resized_height) // 2
    fitted_image[
        offset_y:offset_y + resized_height,
        offset_x:offset_x + resized_width,
    ] = resized_image

    return fitted_image

configure_page("IAPIM - Vision Lab")

if "visionlab_face" not in st.session_state:
    st.session_state.visionlab_face = {
        "selected_bytes": None,
        "result": None,
        "error": None,
    }

page_state = st.session_state.visionlab_face

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("01 – Detector facial")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Capture una fotografía y analícela para detectar rostros.")

st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

analysis_requested = False

with left_column:
    st.subheader("Captura de imagen")
    st.write("Tome una fotografía con la cámara.")
    captured_image = st.camera_input("Cámara", label_visibility="collapsed")

    image_bytes = captured_image.getvalue() if captured_image is not None else None

    if image_bytes != page_state["selected_bytes"]:
        page_state["selected_bytes"] = image_bytes
        page_state["result"] = None
        page_state["error"] = None
        analysis_requested = image_bytes is not None

    info_placeholder = st.empty()
    if page_state["selected_bytes"] is not None:
        info_placeholder.write("Fotografía capturada")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía con los rostros detectados.")

    if analysis_requested:
        info_placeholder.write("Fotografía capturada. Analizando...")
        with st.spinner("Analizando imagen...", show_time=False):
            try:
                page_state["result"] = detect_faces(page_state["selected_bytes"])
            except (RuntimeError, ValueError) as error:
                page_state["error"] = str(error)
        info_placeholder.write("Fotografía capturada")

    if page_state["error"]:
        st.error(page_state["error"])
    elif page_state["result"] is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        processed_image, face_count = page_state["result"]

        st.image(fit_result_image(processed_image), caption="Fotografía procesada", width="stretch")

        st.metric("Rostros detectados", face_count)
        if face_count == 0:
            st.warning("No se detectaron rostros en la fotografía.")
