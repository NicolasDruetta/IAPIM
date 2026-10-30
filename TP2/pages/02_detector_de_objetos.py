import cv2
import numpy as np
import streamlit as st

from functions import configure_page
from pathlib import Path

def detect_objects(image_bytes):
    """Segmenta objetos separables y dibuja sus contornos rectangulares."""
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise ValueError("No se pudo leer la imagen seleccionada.")

    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, binary_image = cv2.threshold(
        blurred_image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )
    kernel = np.ones((5, 5), dtype=np.uint8)
    cleaned_image = cv2.morphologyEx(
        binary_image,
        cv2.MORPH_OPEN,
        kernel,
        iterations=1,
    )
    cleaned_image = cv2.morphologyEx(
        cleaned_image,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=2,
    )

    image_height, image_width = gray_image.shape
    minimum_area = image_height * image_width * 0.01
    contours, _ = cv2.findContours(
        cleaned_image,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    detected_contours = [
        contour
        for contour in contours
        if cv2.contourArea(contour) >= minimum_area
    ]
    processed_image = image_bgr.copy()

    for contour in detected_contours:
        x_coordinate, y_coordinate, width, height = cv2.boundingRect(contour)
        cv2.rectangle(
            processed_image,
            (x_coordinate, y_coordinate),
            (x_coordinate + width, y_coordinate + height),
            (0, 255, 0),
            2,
        )

    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
    return processed_image, len(detected_contours)

def prepare_card_images(image_paths):
    """Ajusta las miniaturas al tamaño de la imagen más grande."""
    decoded_images = [
        (image_path, cv2.imread(str(image_path)))
        for image_path in image_paths
    ]
    decoded_images = [
        (image_path, image)
        for image_path, image in decoded_images
        if image is not None
    ]

    if not decoded_images:
        return []

    maximum_height = max(image.shape[0] for _, image in decoded_images)
    maximum_width = max(image.shape[1] for _, image in decoded_images)
    prepared_images = []

    for image_path, image in decoded_images:
        image_height, image_width = image.shape[:2]
        scale = min(
            maximum_width / image_width,
            maximum_height / image_height,
        )
        resized_width = round(image_width * scale)
        resized_height = round(image_height * scale)
        resized_image = cv2.resize(
            image,
            (resized_width, resized_height),
            interpolation=cv2.INTER_AREA,
        )
        canvas = np.zeros(
            (maximum_height, maximum_width, 3),
            dtype=np.uint8,
        )
        offset_x = (maximum_width - resized_width) // 2
        offset_y = (maximum_height - resized_height) // 2
        canvas[
            offset_y:offset_y + resized_height,
            offset_x:offset_x + resized_width,
        ] = resized_image
        prepared_images.append(
            (image_path, cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        )

    return prepared_images

configure_page("IAPIM - Detector de objetos")

title_column, home_column = st.columns([5, 1])

with title_column:
    st.title("02 – Detector de objetos")
    st.write(
        "Suba una imagen para segmentar y localizar objetos visualmente separables."
    )

with home_column:
    st.write("")
    st.write("")
    if st.button("Volver al Inicio", width="stretch"):
        st.switch_page("main.py")

if "object_detection_error" not in st.session_state:
    st.session_state.object_detection_error = None
if "object_detection_result" not in st.session_state:
    st.session_state.object_detection_result = None
if "object_count" not in st.session_state:
    st.session_state.object_count = 0
empty_result_image = np.full((400, 640, 3), 45, dtype=np.uint8)

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Selección de imagen")
    st.write("Cargue una imagen para analizarla.")
    preloaded_images_directory = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "images"
        / "02_detector_de_objetos"
    )
    preloaded_images = sorted(
        image_path
        for image_path in preloaded_images_directory.glob("*")
        if image_path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )
    card_images = prepare_card_images(preloaded_images)
    uploaded_image = st.file_uploader(
        "Cargue una imagen",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    st.write("Imágenes precargadas")
    image_columns = st.columns(5, gap="small")

    for image_column, (image_path, card_image) in zip(image_columns, card_images):
        with image_column:
            with st.container(border=True):
                st.image(card_image, width="stretch")
                if st.button(
                    "Usar",
                    key=f"select_{image_path.name}",
                    width="stretch",
                ):
                    try:
                        processed_image, object_count = detect_objects(
                            image_path.read_bytes()
                        )
                    except ValueError as error:
                        st.session_state.object_detection_error = str(error)
                        st.session_state.object_detection_result = None
                        st.session_state.object_count = 0
                    else:
                        st.session_state.object_detection_error = None
                        st.session_state.object_detection_result = processed_image
                        st.session_state.object_count = object_count

    if uploaded_image is not None:
        try:
            processed_image, object_count = detect_objects(uploaded_image.getvalue())
        except ValueError as error:
            st.session_state.object_detection_error = str(error)
            st.session_state.object_detection_result = None
            st.session_state.object_count = 0
        else:
            st.session_state.object_detection_error = None
            st.session_state.object_detection_result = processed_image
            st.session_state.object_count = object_count

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía con los objetos detectados.")

    if st.session_state.object_detection_error:
        st.error(st.session_state.object_detection_error)
    elif st.session_state.object_detection_result is None:
        st.image(empty_result_image, width="stretch")
    else:
        st.image(
            st.session_state.object_detection_result,
            caption="Objetos segmentados",
            width="stretch",
        )
        st.metric("Objetos detectados", st.session_state.object_count)
