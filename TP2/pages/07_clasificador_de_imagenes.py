import io

import cv2
import numpy as np

import streamlit as st
import torch

from pathlib import Path
from PIL import Image, ImageOps
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2

GALLERY_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "assets" / "images" / "07_clasificador_de_imagenes"
)

def classify_image(image_bytes, state):
    """Clasifica con los pesos y las transformaciones oficiales de torchvision."""
    with Image.open(io.BytesIO(image_bytes)) as source:
        if source.format not in {"JPEG", "PNG"}:
            raise ValueError("Seleccione una fotografía JPG o PNG.")
        image = ImageOps.exif_transpose(source).convert("RGB")
    weights = MobileNet_V2_Weights.DEFAULT
    if state["model"] is None:
        state["model"] = mobilenet_v2(weights=weights).eval()
    batch = weights.transforms()(image).unsqueeze(0)
    with torch.inference_mode():
        probabilities = state["model"](batch).softmax(dim=1)[0]
        scores, indices = probabilities.topk(5)
    predictions = [
        (weights.meta["categories"][index], score * 100)
        for score, index in zip(scores.tolist(), indices.tolist())
    ]
    return image, predictions

def prepare_gallery_images(image_paths):
    """Ajusta las miniaturas a un lienzo común según la imagen más alta."""
    decoded_images = []
    for image_path in image_paths:
        image = cv2.imread(str(image_path))
        if image is not None:
            decoded_images.append((image_path, image))
    if not decoded_images:
        return []
    target_width = max(image.shape[1] for _, image in decoded_images)
    target_height = max(image.shape[0] for _, image in decoded_images)
    prepared_images = []
    for image_path, image in decoded_images:
        image_height, image_width = image.shape[:2]
        scale = min(target_width / image_width, target_height / image_height)
        resized_size = (round(image_width * scale), round(image_height * scale))
        resized_image = cv2.resize(image, resized_size, interpolation=cv2.INTER_AREA)
        canvas = np.full(
            (target_height, target_width, 3),
            255,
            dtype=np.uint8,
        )
        offset_x = (target_width - resized_size[0]) // 2
        offset_y = (target_height - resized_size[1]) // 2
        canvas[
            offset_y:offset_y + resized_size[1],
            offset_x:offset_x + resized_size[0],
        ] = resized_image
        prepared_images.append(
            (image_path, cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        )
    return prepared_images

def select_image(image_bytes, name, state):
    """Actualiza la selección e invalida el análisis anterior."""
    state.update(selected_bytes=image_bytes, selected_name=name, result=None, error=None)

st.set_page_config(
    page_title="IAPIM - Clasificador de imágenes",
    page_icon=Path(__file__).resolve().parents[1] / "assets" / "icon.png",
    layout="wide",
)
if "visionlab_classifier" not in st.session_state:
    st.session_state.visionlab_classifier = {
        "selected_bytes": None, "selected_name": None, "last_upload": None,
        "model": None, "result": None, "error": None,
    }
page_state = st.session_state.visionlab_classifier

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("07 – Clasificador de imágenes con MobileNetV2")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")
st.write("Clasifique fotografías en las 1.000 categorías de ImageNet con MobileNetV2.")
st.divider()
left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Selección de imagen")
    st.write("Cargue una fotografía para clasificarla.")
    uploaded_image = st.file_uploader(
        "Cargue una fotografía", type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )
    uploaded_bytes = uploaded_image.getvalue() if uploaded_image else None
    upload_signature = (uploaded_image.name, uploaded_bytes) if uploaded_image else None
    if upload_signature != page_state["last_upload"]:
        page_state["last_upload"] = upload_signature
        if uploaded_image is not None:
            select_image(uploaded_bytes, uploaded_image.name, page_state)
    gallery_images = sorted(
        path for path in GALLERY_DIRECTORY.glob("*")
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )
    card_images = prepare_gallery_images(gallery_images)
    if not gallery_images:
        st.info("La galería todavía no contiene fotografías.")
    for row_start in range(0, len(card_images), 4):
        for column, (image_path, prepared_image) in zip(
            st.columns(4, gap="small"), card_images[row_start:row_start + 4]
        ):
            with column:
                with st.container(border=True):
                    try:
                        st.image(prepared_image, width="stretch")
                        if st.button("Usar", key=f"classifier_{image_path.name}", width="stretch"):
                            select_image(image_path.read_bytes(), image_path.name, page_state)
                    except (OSError, ValueError):
                        st.warning("No se pudo leer esta fotografía.")
    info_placeholder = st.empty()
    if page_state["selected_name"] is not None:
        info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}")

with right_column:
    st.subheader("Resultados del análisis")
    if page_state["selected_bytes"] is None:
        with st.container(height=400, border=True):
            st.empty()
    else:
        if page_state["result"] is None and page_state["error"] is None:
            info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}. Analizando...")
            try:
                page_state["result"] = classify_image(page_state["selected_bytes"], page_state)
            except Exception as error:
                page_state["error"] = f"No se pudo clasificar la fotografía: {error}"
            finally:
                info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}")
        if page_state["error"]:
            st.error(page_state["error"])
        else:
            image, predictions = page_state["result"]
            st.image(image, width="stretch")
            st.write(" · ".join(
                f"{category.replace('_', ' ')}: {percentage:.2f} %"
                for category, percentage in predictions
            ))
            st.caption("Las probabilidades corresponden a categorías de ImageNet; no garantizan una identificación correcta.")

st.info(
    "**Modelo seleccionado:** MobileNetV2, un modelo preentrenado con ImageNet para clasificar fotografías "
    "en 1.000 categorías de forma eficiente."
)
