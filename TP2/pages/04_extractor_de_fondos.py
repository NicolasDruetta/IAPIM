import cv2
import numpy as np
import onnxruntime
import streamlit as st

from pathlib import Path
from functions import configure_page

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "rmbg-1.4-quantized.onnx"
GALLERY_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "images" / "04_extractor_de_fondos"

def run_background(image_bytes):
    """Carga RMBG-1.4, elimina el fondo y devuelve una imagen transparente."""
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía seleccionada.")

    if not MODEL_PATH.is_file():
        raise OSError(f"No se encontró el modelo RMBG-1.4 en {MODEL_PATH}.")

    image_height, image_width = image_bgr.shape[:2]
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    model_input = cv2.resize(image_rgb, (1024, 1024), interpolation=cv2.INTER_LINEAR)
    model_input = (model_input.astype(np.float32) / 255.0 - 0.5).transpose(2, 0, 1)[None]

    model_session = onnxruntime.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
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

    return image_bgr, result_rgba

### Empieza la página:

configure_page("IAPIM - Extractor inteligente de fondos con RMBG-1.4")

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

    uploaded_image = st.file_uploader("Cargue una fotografía", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    uploaded_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    selected_bytes = uploaded_bytes
    selected_name = uploaded_image.name if uploaded_image is not None else None
    analysis_requested = selected_bytes is not None

    gallery_images = sorted(path for path in GALLERY_DIRECTORY.glob("*") if path.suffix.lower() in {".jpg", ".jpeg", ".png"})
    st.write("Imágenes precargadas")

    for row_start in range(0, len(gallery_images), 4):
        for gallery_column, image_path in zip(st.columns(4, gap="small"), gallery_images[row_start:row_start + 4]):
            with gallery_column:
                with st.container(border=True):
                    st.image(str(image_path), width="stretch")
                    if st.button("Usar", key=f"extractor_{image_path.name}", width="stretch"):
                        selected_bytes = image_path.read_bytes()
                        selected_name = image_path.name
                        analysis_requested = True

    processing_placeholder = st.empty()
    if selected_name is not None:
        processing_placeholder.write(f"Imagen seleccionada: {selected_name}")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía original y el resultado sin fondo.")

    if analysis_requested:
        processing_placeholder.write(f"Imagen seleccionada: {selected_name}. Trabajando...")
        try:
            image_bgr, result_rgba = run_background(selected_bytes)
        except (OSError, ValueError, cv2.error) as error:
            st.error(str(error))
        else:
            processing_placeholder.write(f"Imagen seleccionada: {selected_name}")
            original_column, result_column = st.columns(2, gap="small")
            with original_column:
                st.image(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), caption="Original", width="stretch")
            with result_column:
                st.image(
                    cv2.cvtColor(result_rgba, cv2.COLOR_BGRA2RGBA),
                    caption="Fondo transparente",
                    width="stretch",
                )
            success, encoded_result = cv2.imencode(".png", result_rgba)
            if not success:
                st.error("No se pudo preparar la descarga PNG.")
            else:
                _, download_column = st.columns([3, 1])
                with download_column:
                    st.download_button(
                        "Descargar PNG transparente",
                        data=encoded_result.tobytes(),
                        file_name="imagen_sin_fondo.png",
                        mime="image/png",
                        width="stretch",
                    )
    else:
        with st.container(height=400, border=True):
            st.write("")

st.info(
    "**Modelo seleccionado:** RMBG-1.4, un modelo preentrenado de segmentación que separa personas y objetos "
    "del fondo automáticamente mediante una máscara alfa."
)
