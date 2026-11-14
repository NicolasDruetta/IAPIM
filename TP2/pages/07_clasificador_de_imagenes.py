import cv2
import io
import numpy as np
import streamlit as st
import torch

from pathlib import Path
from PIL import Image, ImageOps
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2
from functions import configure_page

GALLERY_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "images" / "07_clasificador_de_imagenes"
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "mobilenet_v2-7ebf99e0.pth"

def run_classifier(image_bytes):
    """Clasifica una fotografía con las transformaciones oficiales de MobileNetV2."""
    with Image.open(io.BytesIO(image_bytes)) as source:
        if source.format not in {"JPEG", "PNG"}:
            raise ValueError("Seleccione una fotografía JPG o PNG.")
        image = ImageOps.exif_transpose(source).convert("RGB")

    weights = MobileNet_V2_Weights.DEFAULT
    model = mobilenet_v2(weights=None)
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu", weights_only=True))
    model.eval()
    batch = weights.transforms()(image).unsqueeze(0)

    with torch.inference_mode():
        probabilities = model(batch).softmax(dim=1)[0]
        scores, indices = probabilities.topk(5)

    predictions = [
        (weights.meta["categories"][index], score * 100)
        for score, index in zip(scores.tolist(), indices.tolist())
    ]
    return image, predictions

configure_page("IAPIM - Clasificador de imágenes con MobileNetV2")

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
        "Cargue una fotografía",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )
    selected_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    selected_name = uploaded_image.name if uploaded_image is not None else None

    gallery_images = sorted(
        path for path in GALLERY_DIRECTORY.glob("*")
        if path.suffix.lower() in {".jpg", ".jpeg", ".png"}
    )
    decoded_images = [(path, cv2.imread(str(path))) for path in gallery_images]
    decoded_images = [(path, image) for path, image in decoded_images if image is not None]
    card_images = []

    if decoded_images:
        maximum_height = max(image.shape[0] for _, image in decoded_images)
        maximum_width = max(image.shape[1] for _, image in decoded_images)
        for image_path, image in decoded_images:
            image_height, image_width = image.shape[:2]
            scale = min(maximum_width / image_width, maximum_height / image_height)
            resized = cv2.resize(
                image,
                (round(image_width * scale), round(image_height * scale)),
                interpolation=cv2.INTER_AREA,
            )
            canvas = np.full((maximum_height, maximum_width, 3), 255, dtype=np.uint8)
            offset_x = (maximum_width - resized.shape[1]) // 2
            offset_y = (maximum_height - resized.shape[0]) // 2
            canvas[offset_y:offset_y + resized.shape[0], offset_x:offset_x + resized.shape[1]] = resized
            card_images.append((image_path, cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)))

    st.write("Imágenes predefinidas")

    for row_start in range(0, len(card_images), 4):
        for image_column, (image_path, card_image) in zip(
            st.columns(4, gap="small"),
            card_images[row_start:row_start + 4],
        ):
            with image_column:
                with st.container(border=True):
                    st.image(card_image, width="stretch")
                    if st.button("Usar", key=f"classifier_{image_path.name}", width="stretch"):
                        selected_bytes = image_path.read_bytes()
                        selected_name = image_path.name

    info_placeholder = st.empty()
    if selected_name is not None:
        info_placeholder.write(f"Imagen seleccionada: {selected_name}")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice las cinco categorías más probables.")

    if selected_bytes is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        info_placeholder.write(f"Imagen seleccionada: {selected_name}. Analizando...")
        try:
            image, predictions = run_classifier(selected_bytes)
        except Exception as error:
            st.error(f"No se pudo clasificar la fotografía: {error}")
        else:
            info_placeholder.write(f"Imagen seleccionada: {selected_name}")
            st.image(image, caption="Fotografía clasificada", width="stretch")
            category_summary = " · ".join(
                f"{category.replace('_', ' ')}: {percentage:.2f}%"
                for category, percentage in predictions
            )
            st.write(f"**Categorías presentes:** {len(predictions)} · {category_summary}")

st.info(
    "**Modelo seleccionado:** MobileNetV2, un modelo preentrenado con ImageNet para clasificar fotografías "
    "en 1.000 categorías de forma eficiente."
)
