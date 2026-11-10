import colorsys
import numpy as np
import streamlit as st
import torch

from io import BytesIO
from pathlib import Path
from PIL import Image
from transformers import AutoImageProcessor, SegformerForSemanticSegmentation
from functions import configure_page

MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"
GALLERY_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "images" / "05_analizador_de_escenas"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def run_scene(image_bytes, opacity):
    """Segmenta la fotografía y devuelve la superposición, estadísticas y dispositivo."""
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except (OSError, ValueError) as error:
        raise ValueError("No se pudo leer la imagen seleccionada.") from error

    processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
    model = SegformerForSemanticSegmentation.from_pretrained(MODEL_NAME)
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    model.to(device)
    model.eval()

    inputs = processor(images=image, return_tensors="pt")
    inputs = {
        key: value.to(device) if torch.is_tensor(value) else value
        for key, value in inputs.items()
    }

    with torch.inference_mode():
        outputs = model(**inputs)

    segmentation = processor.post_process_semantic_segmentation(
        outputs,
        target_sizes=[(image.height, image.width)],
    )[0]
    segmentation_map = segmentation.cpu().numpy().astype(np.int32)
    class_ids, pixel_counts = np.unique(segmentation_map, return_counts=True)
    palette = {}
    total_classes = max(len(class_ids), 1)
    for position, class_id in enumerate(sorted(class_ids)):
        hue = position / total_classes
        red, green, blue = colorsys.hsv_to_rgb(hue, 0.75, 0.95)
        palette[int(class_id)] = tuple(round(channel * 255) for channel in (red, green, blue))

    image_array = np.asarray(image)
    color_mask = np.zeros_like(image_array)
    for class_id, color in palette.items():
        color_mask[segmentation_map == class_id] = color
    overlay = image_array.astype(np.float32) * (1 - opacity) + color_mask.astype(np.float32) * opacity
    overlay = np.clip(overlay, 0, 255).astype(np.uint8)

    category_statistics = []
    total_pixels = segmentation_map.size
    labels = model.config.id2label
    for class_id, pixel_count in zip(class_ids, pixel_counts):
        class_number = int(class_id)
        label = labels.get(class_number, labels.get(str(class_number), f"Clase {class_number}"))
        category_statistics.append({
            "label": label,
            "percentage": pixel_count / total_pixels * 100,
        })

    return image, overlay, category_statistics, device

configure_page("IAPIM - Analizador de escenas con SegFormer")

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("05 – Analizador de escenas con SegFormer")

    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Seleccione una fotografía y observe cómo la inteligencia artificial identifica las regiones de la escena.")
st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Selección de imagen")
    st.write("Elija una fotografía de la galería o cargue una imagen propia.")

    uploaded_image = st.file_uploader(
        "Cargue una fotografía",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )
    selected_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    selected_name = uploaded_image.name if uploaded_image is not None else None

    gallery_images = sorted(
        path for path in GALLERY_DIRECTORY.glob("*")
        if path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    decoded_images = []
    for image_path in gallery_images:
        try:
            decoded_images.append((image_path, Image.open(image_path).convert("RGB")))
        except (OSError, ValueError):
            continue

    card_images = []
    if decoded_images:
        target_width = max(image.width for _, image in decoded_images)
        target_height = max(image.height for _, image in decoded_images)
        for image_path, image in decoded_images:
            scale = min(target_width / image.width, target_height / image.height)
            resized_size = (round(image.width * scale), round(image.height * scale))
            resized_image = image.resize(resized_size, Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (target_width, target_height), "white")
            offset = ((target_width - resized_image.width) // 2, (target_height - resized_image.height) // 2)
            canvas.paste(resized_image, offset)
            card_images.append((image_path, canvas))

    st.write("Imágenes precargadas")
    for row_start in range(0, len(card_images), 4):
        for image_column, (image_path, card_image) in zip(
            st.columns(4, gap="small"),
            card_images[row_start:row_start + 4],
        ):
            with image_column:
                with st.container(border=True):
                    st.image(card_image, width="stretch")
                    if st.button("Usar", key=f"scene_{image_path.name}", width="stretch"):
                        selected_bytes = image_path.read_bytes()
                        selected_name = image_path.name

    info_placeholder = st.empty()
    if selected_name is not None:
        info_placeholder.write(f"Imagen seleccionada: {selected_name}")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la segmentación semántica de la fotografía seleccionada.")

    if selected_bytes is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        opacity = st.slider(
            "Opacidad de la superposición",
            min_value=0.0,
            max_value=1.0,
            value=0.50,
            step=0.05,
        )
        info_placeholder.write(f"Imagen seleccionada: {selected_name}. Analizando...")
        try:
            original_image, overlay, category_statistics, device = run_scene(selected_bytes, opacity)
        except (OSError, RuntimeError, ValueError, ImportError) as error:
            st.error(str(error))
        else:
            info_placeholder.write(f"Imagen seleccionada: {selected_name}")
            st.image(overlay, caption=f"Segmentación semántica · dispositivo: {device}", width="stretch")
            category_summary = " · ".join(
                f"{category['label']}: {category['percentage']:.2f}%"
                for category in category_statistics
            )
            st.write(f"**Categorías presentes:** {len(category_statistics)} · {category_summary}")

st.info(
    "**Modelo seleccionado:** SegFormer B0, un modelo preentrenado sobre ADE20K para segmentar semánticamente "
    "las regiones de una escena de forma local."
)
