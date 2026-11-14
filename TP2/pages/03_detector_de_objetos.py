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

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "yolo11n.pt"
GALLERY_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "images" / "03_detector_de_objetos"

def run_objects(image_bytes):
    """Carga YOLO11n, detecta objetos y devuelve la imagen anotada."""
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    inference_device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    model = YOLO(str(MODEL_PATH))

    result = model.predict(
        source=np.array(image),
        conf=0.25,
        imgsz=960,
        device=inference_device,
        verbose=False,
    )[0]

    processed_image = result.plot()
    category_names = [result.names[int(class_id)] for class_id in result.boxes.cls.tolist()]
    category_counts = dict(sorted(Counter(category_names).items()))

    return processed_image, len(category_names), category_counts

### Empieza la página:

configure_page("IAPIM - Detector de objetos con YOLO11n")

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("03 – Detector de objetos con YOLO11n")

    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Suba una imagen para detectar y localizar objetos visualmente separables.")
st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Selección de imagen")
    st.write("Cargue una imagen para analizarla.")

    preloaded_images = sorted(
        path for path in GALLERY_DIRECTORY.glob("*")
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )

    decoded_images = [(path, cv2.imread(str(path))) for path in preloaded_images]
    decoded_images = [(path, image) for path, image in decoded_images if image is not None]
    card_images = []

    if decoded_images:
        maximum_height = max(image.shape[0] for _, image in decoded_images)
        maximum_width = max(image.shape[1] for _, image in decoded_images)
        for image_path, image in decoded_images:
            image_height, image_width = image.shape[:2]
            scale = min(maximum_width / image_width, maximum_height / image_height)
            resized = cv2.resize(image, (round(image_width * scale), round(image_height * scale)), interpolation=cv2.INTER_AREA)
            canvas = np.zeros((maximum_height, maximum_width, 3), dtype=np.uint8)
            offset_x = (maximum_width - resized.shape[1]) // 2
            offset_y = (maximum_height - resized.shape[0]) // 2
            canvas[offset_y:offset_y + resized.shape[0], offset_x:offset_x + resized.shape[1]] = resized
            card_images.append((image_path, cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)))

    uploaded_image = st.file_uploader("Cargue una imagen", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    uploaded_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    selected_bytes = uploaded_bytes
    selected_name = uploaded_image.name if uploaded_image is not None else None
    analysis_requested = selected_bytes is not None

    st.write("Imágenes predefinidas")

    for row_start in range(0, len(card_images), 4):
        for image_column, (image_path, card_image) in zip(st.columns(4, gap="small"), card_images[row_start:row_start + 4]):
            with image_column:
                with st.container(border=True):
                    st.image(card_image, width="stretch")
                    if st.button("Usar", key=f"select_{image_path.name}", width="stretch"):
                        selected_bytes = image_path.read_bytes()
                        selected_name = image_path.name
                        analysis_requested = True

    info_placeholder = st.empty()
    if selected_name is not None:
        info_placeholder.write(f"Imagen seleccionada: {selected_name}")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía con los objetos detectados.")

    if analysis_requested:
        info_placeholder.write(f"Imagen seleccionada: {selected_name}. Analizando...")
        try:
            processed_image, object_count, category_counts = run_objects(selected_bytes)
        except Exception as error:
            st.error(str(error))
        else:
            info_placeholder.write(f"Imagen seleccionada: {selected_name}")
            st.image(processed_image, caption="Objetos detectados", width="stretch")
            category_summary = " · ".join(f"{name}: {count}" for name, count in category_counts.items())
            st.write(f"**Objetos detectados:** {object_count} · {category_summary}")
    else:
        with st.container(height=400, border=True):
            st.write("")

st.info(
    "**Modelo seleccionado:** YOLO11n, la versión más liviana de YOLO11, entrenada con el conjunto de datos COCO (80 categorías). "
    "Lo utilizo porque ofrece detección de objetos rápida y eficiente para el análisis local."
)
