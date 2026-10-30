import cv2
import streamlit as st

from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from io import BytesIO
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from ultralytics import YOLO

from functions import configure_page

YOLO_MODEL_PATH = Path(__file__).resolve().parents[2] / "yolo11n.pt"
INFERENCE_DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

def detect_objects(image_bytes, model):
    """Detecta objetos con YOLO y devuelve la imagen y sus estadísticas."""
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except (OSError, ValueError) as error:
        raise ValueError("No se pudo leer la imagen seleccionada.") from error

    results = model.predict(
        source=np.array(image),
        conf=0.25,
        device=INFERENCE_DEVICE,
        verbose=False,
    )
    result = results[0]
    processed_image = result.plot()[:, :, ::-1]
    category_names = [
        result.names[int(class_id)]
        for class_id in result.boxes.cls.tolist()
    ]
    category_counts = dict(sorted(Counter(category_names).items()))
    return processed_image, len(category_names), category_counts

def get_detection_executor():
    """Crea el ejecutor compartido para inferencias en segundo plano."""
    return ThreadPoolExecutor(max_workers=1)

def load_yolo_model():
    """Carga una única instancia compartida del modelo YOLO11n."""
    if not YOLO_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el modelo preentrenado: {YOLO_MODEL_PATH}"
        )
    return YOLO(str(YOLO_MODEL_PATH))

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

def run_detection(image_bytes):
    """Ejecuta la inferencia completa fuera del hilo de la interfaz."""
    return detect_objects(image_bytes, load_yolo_model())

configure_page("IAPIM - Detector de objetos")

with st.container(
    horizontal=True,
    vertical_alignment="center",
    gap="small",
    width="content",
):
    st.title("02 – Detector de objetos")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write(
    "Suba una imagen para segmentar y localizar objetos visualmente separables."
)

if "object_detection_error" not in st.session_state:
    st.session_state.object_detection_error = None
if "object_detection_result" not in st.session_state:
    st.session_state.object_detection_result = None
if "object_count" not in st.session_state:
    st.session_state.object_count = 0
if "object_category_counts" not in st.session_state:
    st.session_state.object_category_counts = {}
if "detection_future" not in st.session_state:
    st.session_state.detection_future = None
if "uploaded_image_signature" not in st.session_state:
    st.session_state.uploaded_image_signature = None
left_column, right_column = st.columns([1, 1], gap="large")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía con los objetos detectados.")
    result_placeholder = st.empty()

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
    with st.container(key="object-gallery"):
        for row_start in range(0, len(card_images), 4):
            gallery_row = card_images[row_start:row_start + 4]
            image_columns = st.columns(4, gap="small")

            for image_column, (image_path, card_image) in zip(
                image_columns,
                gallery_row,
            ):
                with image_column:
                    with st.container(border=True):
                        st.image(card_image, width="stretch")
                        if st.button(
                            "Usar",
                            key=f"select_{image_path.name}",
                            width="stretch",
                        ):
                            st.session_state.detection_future = (
                                get_detection_executor().submit(
                                    run_detection,
                                    image_path.read_bytes(),
                                )
                            )
                            st.session_state.object_detection_error = None
                            st.session_state.object_detection_result = None
                            st.session_state.object_count = 0
                            st.session_state.object_category_counts = {}

    if uploaded_image is not None:
        uploaded_image_bytes = uploaded_image.getvalue()
        uploaded_image_signature = hash(uploaded_image_bytes)
        if (
            uploaded_image_signature
            != st.session_state.uploaded_image_signature
        ):
            st.session_state.uploaded_image_signature = uploaded_image_signature
            st.session_state.detection_future = (
                get_detection_executor().submit(
                    run_detection,
                    uploaded_image_bytes,
                )
            )
            st.session_state.object_detection_error = None
            st.session_state.object_detection_result = None
            st.session_state.object_count = 0
            st.session_state.object_category_counts = {}

@st.fragment(run_every=0.2)
def update_detection_panel():
    """Actualiza el panel mientras la inferencia se ejecuta."""
    detection_future = st.session_state.detection_future

    if detection_future is not None and not detection_future.done():
        with result_placeholder.container(height=400, border=True):
            st.write("Analizando imagen...")
        return

    if detection_future is not None:
        try:
            (
                processed_image,
                object_count,
                category_counts,
            ) = detection_future.result()
        except Exception as error:
            st.session_state.object_detection_error = str(error)
            st.session_state.object_detection_result = None
            st.session_state.object_count = 0
            st.session_state.object_category_counts = {}
        else:
            st.session_state.object_detection_error = None
            st.session_state.object_detection_result = processed_image
            st.session_state.object_count = object_count
            st.session_state.object_category_counts = category_counts
        finally:
            st.session_state.detection_future = None

    with result_placeholder.container():
        if st.session_state.object_detection_error:
            st.error(st.session_state.object_detection_error)
        elif st.session_state.object_detection_result is None:
            with st.container(height=400, border=True):
                st.write("")
        else:
            st.image(
                st.session_state.object_detection_result,
                caption="Objetos segmentados",
                width="stretch",
            )
            st.metric("Objetos detectados", st.session_state.object_count)
            st.write("Cantidad por categoría")
            for category_name, category_count in (
                st.session_state.object_category_counts.items()
            ):
                st.write(f"- {category_name}: {category_count}")

update_detection_panel()
