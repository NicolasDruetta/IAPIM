import cv2
import numpy as np
import streamlit as st
import torch

from collections import Counter
from io import BytesIO
from pathlib import Path
from PIL import Image
from ultralytics import YOLO
from functions import configure_page

YOLO_MODEL_PATH = Path(__file__).resolve().parents[2] / "yolo11n.pt"

def detect_objects(image_bytes, model):
    """Detecta objetos con YOLO y devuelve imagen, cantidad y categorías."""
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except (OSError, ValueError) as error:
        raise ValueError("No se pudo leer la imagen seleccionada.") from error

    if torch.cuda.is_available():
        inference_device = "cuda"
    elif torch.backends.mps.is_available():
        inference_device = "mps"
    else:
        inference_device = "cpu"

    results = model.predict(
        source=np.array(image),
        conf=0.25,
        device=inference_device,
        verbose=False,
    )

    result = results[0]

    processed_image = result.plot()[:, :, ::-1]

    category_names = [
        result.names[int(class_id)] for class_id in result.boxes.cls.tolist()
    ]

    category_counts = dict(sorted(Counter(category_names).items()))

    return processed_image, len(category_names), category_counts

def prepare_card_images(image_paths):
    """Ajusta las miniaturas al tamaño de la imagen más grande."""
    decoded_images = [(path, cv2.imread(str(path))) for path in image_paths]
    decoded_images = [
        (path, image) for path, image in decoded_images if image is not None
    ]

    if not decoded_images:
        return []
    maximum_height = max(image.shape[0] for _, image in decoded_images)
    maximum_width = max(image.shape[1] for _, image in decoded_images)
    prepared_images = []

    for image_path, image in decoded_images:
        image_height, image_width = image.shape[:2]
        scale = min(maximum_width / image_width, maximum_height / image_height)
        resized_width = round(image_width * scale)
        resized_height = round(image_height * scale)
        resized_image = cv2.resize(
            image,
            (resized_width, resized_height),
            interpolation=cv2.INTER_AREA,
        )
        canvas = np.zeros((maximum_height, maximum_width, 3), dtype=np.uint8)
        offset_x = (maximum_width - resized_width) // 2
        offset_y = (maximum_height - resized_height) // 2
        canvas[
            offset_y : offset_y + resized_height, offset_x : offset_x + resized_width
        ] = resized_image
        prepared_images.append((image_path, cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)))

    return prepared_images

def run_detection(image_bytes, page_state):
    """Carga YOLO una sola vez por sesión y ejecuta la detección."""

    if page_state["model"] is None:
        if not YOLO_MODEL_PATH.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo preentrenado: {YOLO_MODEL_PATH}"
            )
        page_state["model"] = YOLO(str(YOLO_MODEL_PATH))

    return detect_objects(image_bytes, page_state["model"])

configure_page("IAPIM - Detector de objetos")

if "visionlab_objects" not in st.session_state:
    st.session_state.visionlab_objects = {
        "selected_bytes": None,
        "selected_name": None,
        "last_upload": None,
        "result": None,
        "error": None,
        "model": None,
    }

page_state = st.session_state.visionlab_objects

with st.container(
    horizontal=True, vertical_alignment="center", gap="small", width="content"
):
    st.title("02 – Detector de objetos")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Suba una imagen para detectar y localizar objetos visualmente separables.")

st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

analysis_requested = False

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

    uploaded_bytes = uploaded_image.getvalue() if uploaded_image is not None else None

    if uploaded_bytes != page_state["last_upload"]:
        page_state["last_upload"] = uploaded_bytes

        if uploaded_bytes is not None:
            page_state["selected_bytes"] = uploaded_bytes
            page_state["selected_name"] = uploaded_image.name
            page_state["result"] = None
            page_state["error"] = None
            analysis_requested = True

    st.write("Imágenes precargadas")

    with st.container(key="object-gallery"):
        for row_start in range(0, len(card_images), 4):
            gallery_row = card_images[row_start : row_start + 4]
            image_columns = st.columns(4, gap="small")
            for image_column, (image_path, card_image) in zip(
                image_columns, gallery_row
            ):
                with image_column:
                    with st.container(border=True):
                        st.image(card_image, width="stretch")
                        if st.button(
                            "Usar", key=f"select_{image_path.name}", width="stretch"
                        ):
                            page_state["selected_bytes"] = image_path.read_bytes()
                            page_state["selected_name"] = image_path.name
                            page_state["result"] = None
                            page_state["error"] = None
                            analysis_requested = True

    info_placeholder = st.empty()
    if page_state["selected_name"] is not None:
        info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía con los objetos detectados.")

    if analysis_requested:
        info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}. Analizando...")
        with st.spinner("Analizando imagen...", show_time=False):
            try:
                page_state["result"] = run_detection(
                    page_state["selected_bytes"], page_state
                )
            except Exception as error:
                page_state["error"] = str(error)
        info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}")

    if page_state["error"]:
        st.error(page_state["error"])
    elif page_state["result"] is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        processed_image, object_count, category_counts = page_state["result"]

        st.image(processed_image, caption="Objetos detectados", width="stretch")

        category_summary = " · ".join(
            f"{category_name}: {category_count}"
            for category_name, category_count in category_counts.items()
        )

        st.write(f"**Objetos detectados:** {object_count} · {category_summary}")
