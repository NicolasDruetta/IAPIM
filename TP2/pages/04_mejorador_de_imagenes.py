import cv2
import numpy as np
import streamlit as st

from pathlib import Path
from functions import configure_page

GALLERY_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "images"
    / "04_mejorador_de_imagenes"
)
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def apply_clahe(image_bgr, intensity):
    """Mejora el contraste local mediante CLAHE sobre la luminancia."""
    lab_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
    lightness, channel_a, channel_b = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=intensity, tileGridSize=(8, 8))
    enhanced_lightness = clahe.apply(lightness)
    enhanced_lab = cv2.merge((enhanced_lightness, channel_a, channel_b))
    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

def apply_gamma(image_bgr, gamma):
    """Ajusta la luminosidad mediante una corrección gamma."""
    lookup_table = np.array(
        [((index / 255.0) ** (1.0 / gamma)) * 255 for index in range(256)],
        dtype=np.uint8,
    )
    return cv2.LUT(image_bgr, lookup_table)

def apply_histogram_equalization(image_bgr, intensity):
    """Ecualiza el histograma de la luminancia y mezcla según la intensidad."""
    ycrcb_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
    luminance, channel_cr, channel_cb = cv2.split(ycrcb_image)
    equalized_luminance = cv2.equalizeHist(luminance)
    equalized_image = cv2.cvtColor(
        cv2.merge((equalized_luminance, channel_cr, channel_cb)),
        cv2.COLOR_YCrCb2BGR,
    )
    return cv2.addWeighted(
        image_bgr,
        1 - intensity,
        equalized_image,
        intensity,
        0,
    )

def apply_image_enhancement(image_bgr, method, intensity):
    """Aplica el método seleccionado con su intensidad correspondiente."""
    if method == "Ecualización de histogramas":
        return apply_histogram_equalization(image_bgr, intensity / 100)
    if method == "CLAHE":
        return apply_clahe(image_bgr, intensity)
    return apply_gamma(image_bgr, intensity)

def get_gallery_images():
    """Obtiene las fotografías disponibles para la galería."""
    return sorted(
        image_path
        for image_path in GALLERY_DIRECTORY.glob("*")
        if image_path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

def initialize_state():
    """Inicializa el estado de la página sin sobrescribir una selección vigente."""
    if "visionlab_enhancer" not in st.session_state:
        st.session_state.visionlab_enhancer = {
            "selected_bytes": None,
            "selected_name": None,
            "last_upload": None,
            "last_settings": None,
            "result": None,
            "error": None,
        }

    return st.session_state.visionlab_enhancer

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

def process_image(image_bytes, method, intensity):
    """Decodifica, mejora y convierte la imagen para su presentación."""
    image_bgr = read_image(image_bytes)
    enhanced_bgr = apply_image_enhancement(image_bgr, method, intensity)
    return (
        cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB),
        cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB),
    )

def read_image(image_bytes):
    """Decodifica una fotografía recibida como bytes."""
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía seleccionada.")
    return image_bgr

configure_page("IAPIM - Mejorador inteligente de imágenes")
page_state = initialize_state()

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("04 – Mejorador inteligente de imágenes")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Mejore el contraste y la luminosidad de una fotografía mediante OpenCV.")

st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Selección de imagen")
    st.write("Cargue una fotografía para mejorarla.")
    gallery_images = get_gallery_images()
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
    if not gallery_images:
        st.warning("La galería todavía no contiene fotografías.")
    else:
        st.write("Imágenes precargadas")
        with st.container(key="enhancer-gallery"):
            for row_start in range(0, len(card_images), 4):
                gallery_row = card_images[row_start:row_start + 4]
                gallery_columns = st.columns(4, gap="small")
                for gallery_column, (image_path, prepared_image) in zip(
                    gallery_columns,
                    gallery_row,
                ):
                    with gallery_column:
                        with st.container(border=True):
                            st.image(prepared_image, width="stretch")
                            if st.button(
                                "Usar",
                                key=f"enhancer_{image_path.name}",
                                width="stretch",
                            ):
                                page_state["selected_bytes"] = image_path.read_bytes()
                                page_state["selected_name"] = image_path.name
                                page_state["result"] = None
                                page_state["error"] = None
    if page_state["selected_name"] is not None:
        st.write(f"Imagen seleccionada: {page_state['selected_name']}")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía original y la versión mejorada.")
    if page_state["selected_bytes"] is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        method = st.selectbox(
            "Método de mejora",
            [
                "Ecualización de histogramas",
                "CLAHE",
                "Corrección gamma",
            ],
        )
        if method == "Ecualización de histogramas":
            intensity = st.slider(
                "Intensidad del efecto",
                min_value=0,
                max_value=100,
                value=50,
                step=5,
                format="%d%%",
            )
        elif method == "CLAHE":
            intensity = st.slider(
                "Intensidad del efecto",
                min_value=1.0,
                max_value=5.0,
                value=3.0,
                step=0.5,
            )
        else:
            intensity = st.slider(
                "Gamma",
                min_value=0.2,
                max_value=3.0,
                value=1.6,
                step=0.1,
            )
        current_settings = (method, intensity)
        if (
            page_state["result"] is None
            or page_state["last_settings"] != current_settings
        ):
            try:
                page_state["result"] = process_image(
                    page_state["selected_bytes"],
                    method,
                    intensity,
                )
                page_state["last_settings"] = current_settings
                page_state["error"] = None
            except (OSError, ValueError, cv2.error) as error:
                page_state["error"] = str(error)
        if page_state["error"]:
            st.error(page_state["error"])
        elif page_state["result"] is None:
            with st.container(height=400, border=True):
                st.write("")
        else:
            original_image, enhanced_image = page_state["result"]
            original_column, enhanced_column = st.columns(2, gap="small")
            with original_column:
                st.image(original_image, caption="Original", width="stretch")
            with enhanced_column:
                st.image(enhanced_image, caption="Mejorada", width="stretch")
            method_descriptions = {
                "Ecualización de histogramas": (
                    "Redistribuye la luminancia para mejorar el contraste global."
                ),
                "CLAHE": (
                    "Mejora el contraste local por regiones y limita la amplificación."
                ),
                "Corrección gamma": (
                    "Ajusta la luminosidad para aclarar u oscurecer la fotografía."
                ),
            }
            st.info(method_descriptions[method])
