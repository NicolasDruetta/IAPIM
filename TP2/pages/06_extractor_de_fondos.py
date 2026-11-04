import cv2
import numpy as np
import streamlit as st

from pathlib import Path
from functions import configure_page

GALLERY_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "images"
    / "06_extractor_de_fondos"
)
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def apply_grabcut(image_bgr, horizontal_range, vertical_range):
    """Separa el primer plano usando una región rectangular ajustable."""
    image_height, image_width = image_bgr.shape[:2]
    left_percent, right_percent = horizontal_range
    top_percent, bottom_percent = vertical_range
    left = min(round(image_width * left_percent / 100), max(0, image_width - 2))
    top = min(round(image_height * top_percent / 100), max(0, image_height - 2))
    right = max(left + 2, min(image_width, round(image_width * right_percent / 100)))
    bottom = max(top + 2, min(image_height, round(image_height * bottom_percent / 100)))
    rect = (
        left,
        top,
        max(1, right - left),
        max(1, bottom - top),
    )
    mask = np.zeros((image_height, image_width), np.uint8)
    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(
        image_bgr,
        mask,
        rect,
        background_model,
        foreground_model,
        5,
        cv2.GC_INIT_WITH_RECT,
    )
    foreground = np.where(
        (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD),
        255,
        0,
    ).astype(np.uint8)
    result_rgba = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2BGRA)
    result_rgba[:, :, 3] = foreground
    return result_rgba

def decode_image(image_bytes):
    """Decodifica una fotografía JPG o PNG."""
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía seleccionada.")
    return image_bgr

def get_gallery_images():
    """Obtiene las fotografías precargadas disponibles."""
    return sorted(
        image_path
        for image_path in GALLERY_DIRECTORY.glob("*")
        if image_path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

def initialize_state():
    """Inicializa el estado de la página."""
    if "visionlab_background_extractor" not in st.session_state:
        st.session_state.visionlab_background_extractor = {
            "selected_bytes": None,
            "selected_name": None,
            "last_upload": None,
            "error": None,
        }
    return st.session_state.visionlab_background_extractor

def prepare_gallery_images(image_paths):
    """Prepara miniaturas con un tamaño común."""
    prepared_images = []
    for image_path in image_paths:
        image = cv2.imread(str(image_path))
        if image is None:
            continue
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        prepared_images.append((image_path, image))
    return prepared_images

def read_image_bytes(image_bytes):
    """Valida y decodifica una fotografía recibida."""
    return decode_image(image_bytes)

configure_page("IAPIM - Extractor inteligente de fondos")
page_state = initialize_state()

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("06 – Extractor inteligente de fondos")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Separe el objeto principal de una fotografía mediante GrabCut.")
st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Selección de imagen")
    st.write("Cargue una fotografía para extraer su fondo.")
    uploaded_image = st.file_uploader(
        "Cargue una fotografía",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )
    uploaded_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    if uploaded_bytes != page_state["last_upload"]:
        page_state["last_upload"] = uploaded_bytes
        if uploaded_image is not None:
            page_state["selected_bytes"] = uploaded_bytes
            page_state["selected_name"] = uploaded_image.name
            page_state["error"] = None
    gallery_images = prepare_gallery_images(get_gallery_images())
    if not gallery_images:
        st.info("La galería todavía no contiene fotografías.")
    else:
        st.write("Imágenes precargadas")
        for row_start in range(0, len(gallery_images), 4):
            gallery_columns = st.columns(4, gap="small")
            for gallery_column, (image_path, prepared_image) in zip(
                gallery_columns,
                gallery_images[row_start:row_start + 4],
            ):
                with gallery_column:
                    with st.container(border=True):
                        st.image(prepared_image, width="stretch")
                        if st.button("Usar", key=f"extractor_{image_path.name}", width="stretch"):
                            page_state["selected_bytes"] = image_path.read_bytes()
                            page_state["selected_name"] = image_path.name
                            page_state["error"] = None
    if page_state["selected_name"] is not None:
        st.write(f"Imagen seleccionada: {page_state['selected_name']}")

with right_column:
    st.subheader("Resultados del análisis")
    if page_state["selected_bytes"] is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        horizontal_range = st.slider(
            "Región horizontal",
            min_value=0,
            max_value=100,
            value=(10, 90),
        )
        vertical_range = st.slider(
            "Región vertical",
            min_value=0,
            max_value=100,
            value=(10, 90),
        )
        try:
            image_bgr = read_image_bytes(page_state["selected_bytes"])
            result_rgba = apply_grabcut(image_bgr, horizontal_range, vertical_range)
            original_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            original_column, result_column = st.columns(2, gap="small")
            with original_column:
                st.image(original_rgb, caption="Original", width="stretch")
            with result_column:
                st.image(result_rgba, caption="Fondo transparente", width="stretch")
            success, encoded_result = cv2.imencode(".png", result_rgba)
            if not success:
                raise ValueError("No se pudo preparar la descarga PNG.")
            st.download_button(
                "Descargar PNG transparente",
                data=encoded_result.tobytes(),
                file_name="imagen_sin_fondo.png",
                mime="image/png",
                width="stretch",
            )
        except (OSError, ValueError, cv2.error) as error:
            st.error(str(error))
