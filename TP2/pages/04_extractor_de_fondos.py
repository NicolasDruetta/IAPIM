import cv2
import numpy as np
import streamlit as st

from pathlib import Path
from functions import configure_page

GALLERY_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "images"
    / "04_extractor_de_fondos"
)
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "rmbg-1.4-quantized.onnx"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

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
            "model_session": None,
        }
    return st.session_state.visionlab_background_extractor

def load_model(page_state):
    """Carga RMBG-1.4 ONNX una sola vez por sesión."""
    if page_state["model_session"] is not None:
        return page_state["model_session"]
    if not MODEL_PATH.is_file():
        raise OSError(f"No se encontró el modelo RMBG-1.4 en {MODEL_PATH}.")
    try:
        import onnxruntime
    except ImportError as error:
        raise OSError("ONNX Runtime no está instalado. Instale las dependencias de Vision Lab.") from error
    page_state["model_session"] = onnxruntime.InferenceSession(
        str(MODEL_PATH),
        providers=["CPUExecutionProvider"],
    )
    return page_state["model_session"]

def prepare_gallery_images(image_paths):
    """Prepara miniaturas con un tamaño común."""
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
    target_width = max(image.shape[1] for _, image in decoded_images)
    target_height = max(image.shape[0] for _, image in decoded_images)
    prepared_images = []
    for image_path, image in decoded_images:
        scale = min(target_width / image.shape[1], target_height / image.shape[0])
        resized_width = max(1, round(image.shape[1] * scale))
        resized_height = max(1, round(image.shape[0] * scale))
        resized_image = cv2.resize(
            image,
            (resized_width, resized_height),
            interpolation=cv2.INTER_AREA,
        )
        canvas = np.full((target_height, target_width, 3), 255, dtype=np.uint8)
        offset_x = (target_width - resized_width) // 2
        offset_y = (target_height - resized_height) // 2
        canvas[
            offset_y:offset_y + resized_height,
            offset_x:offset_x + resized_width,
        ] = resized_image
        prepared_images.append(
            (image_path, cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        )
    return prepared_images

def remove_background(image_bgr, model_session):
    """Obtiene la máscara RMBG-1.4 y crea una imagen BGRA transparente."""
    image_height, image_width = image_bgr.shape[:2]
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    model_input = cv2.resize(image_rgb, (1024, 1024), interpolation=cv2.INTER_LINEAR)
    model_input = model_input.astype(np.float32) / 255.0
    model_input = (model_input - 0.5).transpose(2, 0, 1)[None]
    input_name = model_session.get_inputs()[0].name
    model_output = model_session.run(None, {input_name: model_input})[0]
    mask = np.squeeze(model_output)
    if mask.ndim != 2:
        raise ValueError("RMBG-1.4 devolvió una máscara con formato inesperado.")
    mask = cv2.resize(mask, (image_width, image_height), interpolation=cv2.INTER_LINEAR)
    mask_min, mask_max = float(mask.min()), float(mask.max())
    if mask_max <= mask_min:
        raise ValueError("RMBG-1.4 no produjo una máscara válida.")
    alpha = ((mask - mask_min) / (mask_max - mask_min) * 255).astype(np.uint8)
    result_rgba = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2BGRA)
    result_rgba[:, :, 3] = alpha
    return result_rgba

def read_image_bytes(image_bytes):
    """Valida y decodifica una fotografía recibida."""
    return decode_image(image_bytes)

configure_page("IAPIM - Extractor inteligente de fondos con RMBG-1.4")
page_state = initialize_state()
processing_placeholder = None

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("04 – Extractor inteligente de fondos con RMBG-1.4")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Separe el objeto principal de una fotografía mediante RMBG-1.4.")
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
        processing_placeholder = st.empty()
        processing_placeholder.write(
            f"Imagen seleccionada: {page_state['selected_name']} · Trabajando..."
        )
with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía original y el resultado sin fondo.")
    if page_state["selected_bytes"] is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        result_placeholder = st.empty()
        with result_placeholder.container(height=400, border=True):
            st.write("")
        try:
            image_bgr = read_image_bytes(page_state["selected_bytes"])
            result_rgba = remove_background(image_bgr, load_model(page_state))
            original_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
            result_placeholder.empty()
            with result_placeholder.container():
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
                    width="content",
                )
            processing_placeholder.write(
                f"Imagen seleccionada: {page_state['selected_name']}"
            )
        except (OSError, ValueError, cv2.error) as error:
            result_placeholder.empty()
            processing_placeholder.write(
                f"Imagen seleccionada: {page_state['selected_name']}"
            )
            st.error(str(error))

st.info(
    "**Modelo seleccionado:** RMBG-1.4, un modelo preentrenado de segmentación que separa personas y objetos "
    "del fondo automáticamente mediante una máscara alfa."
)
