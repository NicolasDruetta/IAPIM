import colorsys
import numpy as np
import streamlit as st
import torch
from io import BytesIO
from pathlib import Path
from PIL import Image
from functions import configure_page
MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"
GALLERY_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "images" / "03_analizador_de_escenas"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
def build_palette(class_ids):
    """Genera colores diferenciados y deterministas para las clases presentes."""
    palette = {}
    total_classes = max(len(class_ids), 1)
    for position, class_id in enumerate(sorted(class_ids)):
        hue = position / total_classes
        red, green, blue = colorsys.hsv_to_rgb(hue, 0.75, 0.95)
        palette[class_id] = tuple(round(channel * 255) for channel in (red, green, blue))

    return palette
def create_overlay(original_image, color_mask, opacity):
    """Combina la imagen original y la máscara con la opacidad indicada."""
    original_array = np.asarray(original_image).astype(np.float32)
    mask_array = color_mask.astype(np.float32)
    overlay = original_array * (1 - opacity) + mask_array * opacity

    return np.clip(overlay, 0, 255).astype(np.uint8)
def prepare_gallery_images(image_paths):
    """Ajusta las miniaturas a un lienzo común según la imagen más alta."""
    decoded_images = []
    for image_path in image_paths:
        try:
            image = Image.open(image_path).convert("RGB")
        except (OSError, ValueError):
            continue
        decoded_images.append((image_path, image))

    if not decoded_images:
        return []
    target_width = max(image.width for _, image in decoded_images)
    target_height = max(image.height for _, image in decoded_images)
    prepared_images = []

    for image_path, image in decoded_images:
        scale = min(target_width / image.width, target_height / image.height)
        resized_size = (round(image.width * scale), round(image.height * scale))
        resized_image = image.resize(resized_size, Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (target_width, target_height), "white")
        offset = (
            (target_width - resized_image.width) // 2,
            (target_height - resized_image.height) // 2,
        )
        canvas.paste(resized_image, offset)
        prepared_images.append((image_path, canvas))

    return prepared_images
def get_inference_device():
    """Selecciona CUDA, MPS o CPU según la disponibilidad del equipo."""

    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")
def segment_scene(image_bytes, page_state):
    """Segmenta la imagen y devuelve máscara, estadísticas y dispositivo."""
    from transformers import AutoImageProcessor, SegformerForSemanticSegmentation
    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except (OSError, ValueError) as error:
        raise ValueError("No se pudo leer la imagen seleccionada.") from error

    if page_state["model"] is None:
        processor = AutoImageProcessor.from_pretrained(MODEL_NAME)
        model = SegformerForSemanticSegmentation.from_pretrained(MODEL_NAME)
        device = get_inference_device()
        model.to(device)
        model.eval()
        page_state["model"] = processor, model, device

    processor, model, device = page_state["model"]

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
    palette = build_palette(class_ids)
    image_array = np.asarray(image)
    color_mask = np.zeros_like(image_array)

    for class_id, color in palette.items():
        color_mask[segmentation_map == class_id] = color

    category_statistics = []

    total_pixels = segmentation_map.size
    labels = model.config.id2label

    for class_id, pixel_count in zip(class_ids, pixel_counts):
        class_number = int(class_id)
        label = labels.get(class_number, labels.get(str(class_number), f"Clase {class_number}"))
        category_statistics.append({
            "class_id": class_number,
            "label": label,
            "pixel_count": int(pixel_count),
            "percentage": pixel_count / total_pixels * 100,
            "color": palette[int(class_id)],
        })

    return image, color_mask, category_statistics, device
configure_page("IAPIM - Analizador de escenas")

if "visionlab_scenes" not in st.session_state:
    st.session_state.visionlab_scenes = {
        "selected_bytes": None,
        "last_upload": None,
        "result": None,
        "error": None,
        "model": None,
        "selected_name": None,
    }

page_state = st.session_state.visionlab_scenes

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("03 – Analizador de escenas")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Seleccione una fotografía y observe cómo la inteligencia artificial identifica las regiones de la escena.")

left_column, right_column = st.columns([1, 1], gap="large")

analysis_requested = False

with left_column:
    st.subheader("Selección de imagen")
    st.write("Elija una fotografía de la galería o cargue una imagen propia.")

    gallery_images = sorted(
        image_path
        for image_path in GALLERY_DIRECTORY.glob("*")
        if image_path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    card_images = prepare_gallery_images(gallery_images)

    uploaded_image = st.file_uploader(
        "Cargue una fotografía",
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

    if not gallery_images:
        st.warning("La galería todavía no contiene fotografías. Agregue imágenes en assets/images/03_analizador_de_escenas/.")
    else:
        st.write("Imágenes precargadas")
        with st.container(key="scene-gallery"):
            for row_start in range(0, len(card_images), 4):
                gallery_row = card_images[row_start:row_start + 4]
                gallery_columns = st.columns(4, gap="small")
                for gallery_column, (image_path, prepared_image) in zip(gallery_columns, gallery_row):
                    with gallery_column:
                        with st.container(border=True):
                            st.image(prepared_image, width="stretch")
                            if st.button("Usar", key=f"scene_{image_path.name}", width="stretch"):
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
    st.write("Visualice la segmentación semántica de la fotografía seleccionada.")

    if analysis_requested:
        info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}. Analizando...")
        with st.spinner("Analizando imagen...", show_time=False):
            try:
                page_state["result"] = segment_scene(page_state["selected_bytes"], page_state)
            except (OSError, RuntimeError, ValueError, ImportError) as error:
                page_state["error"] = str(error)
        info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}")

    if page_state["error"]:
        st.error(page_state["error"])
    elif page_state["result"] is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        original_image, color_mask, category_statistics, inference_device = page_state["result"]

        opacity = st.slider(
            "Opacidad de la superposición",
            min_value=0.0,
            max_value=1.0,
            value=0.55,
            step=0.05,
        )

        st.image(
            create_overlay(original_image, color_mask, opacity),
            caption=f"Segmentación semántica · dispositivo: {inference_device}",
            width="stretch",
        )

        category_summary = " · ".join(
            f"{category['label']}: {category['percentage']:.2f}%"
            for category in category_statistics
        )

        st.write(f"**Categorías presentes:** {len(category_statistics)} · {category_summary}")
