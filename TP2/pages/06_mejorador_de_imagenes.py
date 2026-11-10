import cv2
import numpy as np
import streamlit as st

from pathlib import Path
from functions import configure_page

GALLERY_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "images" / "06_mejorador_de_imagenes"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def run_enhancement(image_bytes, method, intensity):
    """Decodifica, mejora y devuelve la imagen original y la versión mejorada."""
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía seleccionada.")

    if method == "Ecualización de histogramas":
        ycrcb_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)
        luminance, channel_cr, channel_cb = cv2.split(ycrcb_image)
        equalized_luminance = cv2.equalizeHist(luminance)
        equalized_image = cv2.cvtColor(
            cv2.merge((equalized_luminance, channel_cr, channel_cb)),
            cv2.COLOR_YCrCb2BGR,
        )
        enhanced_bgr = cv2.addWeighted(
            image_bgr,
            1 - intensity / 100,
            equalized_image,
            intensity / 100,
            0,
        )
    elif method == "CLAHE":
        lab_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2LAB)
        lightness, channel_a, channel_b = cv2.split(lab_image)
        clahe = cv2.createCLAHE(clipLimit=intensity, tileGridSize=(8, 8))
        enhanced_lightness = clahe.apply(lightness)
        enhanced_bgr = cv2.cvtColor(
            cv2.merge((enhanced_lightness, channel_a, channel_b)),
            cv2.COLOR_LAB2BGR,
        )
    else:
        lookup_table = np.array(
            [((index / 255.0) ** (1.0 / intensity)) * 255 for index in range(256)],
            dtype=np.uint8,
        )
        enhanced_bgr = cv2.LUT(image_bgr, lookup_table)

    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB), cv2.cvtColor(enhanced_bgr, cv2.COLOR_BGR2RGB)

configure_page("IAPIM - Mejorador inteligente de imágenes con OpenCV")

if "enhancer_selected_bytes" not in st.session_state:
    st.session_state.enhancer_selected_bytes = None
    st.session_state.enhancer_selected_name = None

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("06 – Mejorador inteligente de imágenes con OpenCV")

    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Mejore el contraste y la luminosidad de una fotografía mediante OpenCV.")
st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Selección de imagen")
    st.write("Cargue una fotografía para mejorarla.")

    uploaded_image = st.file_uploader(
        "Cargue una fotografía",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )
    uploaded_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    if uploaded_bytes is not None:
        st.session_state.enhancer_selected_bytes = uploaded_bytes
        st.session_state.enhancer_selected_name = uploaded_image.name

    selected_bytes = st.session_state.enhancer_selected_bytes
    selected_name = st.session_state.enhancer_selected_name

    gallery_images = sorted(
        path for path in GALLERY_DIRECTORY.glob("*")
        if path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    decoded_images = [(path, cv2.imread(str(path))) for path in gallery_images]
    decoded_images = [(path, image) for path, image in decoded_images if image is not None]
    card_images = []

    if decoded_images:
        target_height = max(image.shape[0] for _, image in decoded_images)
        target_width = max(image.shape[1] for _, image in decoded_images)
        for image_path, image in decoded_images:
            image_height, image_width = image.shape[:2]
            scale = min(target_width / image_width, target_height / image_height)
            resized = cv2.resize(
                image,
                (round(image_width * scale), round(image_height * scale)),
                interpolation=cv2.INTER_AREA,
            )
            canvas = np.full((target_height, target_width, 3), 255, dtype=np.uint8)
            offset_x = (target_width - resized.shape[1]) // 2
            offset_y = (target_height - resized.shape[0]) // 2
            canvas[offset_y:offset_y + resized.shape[0], offset_x:offset_x + resized.shape[1]] = resized
            card_images.append((image_path, cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)))

    st.write("Imágenes precargadas")
    for row_start in range(0, len(card_images), 4):
        for image_column, (image_path, card_image) in zip(
            st.columns(4, gap="small"),
            card_images[row_start:row_start + 4],
        ):
            with image_column:
                with st.container(border=True):
                    st.image(card_image, width="stretch")
                    if st.button("Usar", key=f"enhancer_{image_path.name}", width="stretch"):
                        st.session_state.enhancer_selected_bytes = image_path.read_bytes()
                        st.session_state.enhancer_selected_name = image_path.name
                        selected_bytes = st.session_state.enhancer_selected_bytes
                        selected_name = st.session_state.enhancer_selected_name

    info_placeholder = st.empty()
    if selected_name is not None:
        info_placeholder.write(f"Imagen seleccionada: {selected_name}")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía original y la versión mejorada.")

    if selected_bytes is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        method = st.selectbox(
            "Método de mejora",
            ["Ecualización de histogramas", "CLAHE", "Corrección gamma"],
        )
        if method == "Ecualización de histogramas":
            intensity = st.slider("Intensidad del efecto", 0, 100, 50, 5, format="%d%%")
        elif method == "CLAHE":
            intensity = st.slider("Intensidad del efecto", 1.0, 5.0, 3.0, 0.5)
        else:
            intensity = st.slider("Gamma", 0.2, 3.0, 1.6, 0.1)

        info_placeholder.write(f"Imagen seleccionada: {selected_name}. Analizando...")
        try:
            original_image, enhanced_image = run_enhancement(selected_bytes, method, intensity)
        except (OSError, ValueError, cv2.error) as error:
            st.error(str(error))
        else:
            info_placeholder.write(f"Imagen seleccionada: {selected_name}")
            original_column, enhanced_column = st.columns(2, gap="small")
            with original_column:
                st.image(original_image, caption="Original", width="stretch")
            with enhanced_column:
                st.image(enhanced_image, caption="Mejorada", width="stretch")

            method_descriptions = {
                "Ecualización de histogramas": "Redistribuye la luminancia para mejorar el contraste global.",
                "CLAHE": "Mejora el contraste local por regiones y limita la amplificación.",
                "Corrección gamma": "Ajusta la luminosidad para aclarar u oscurecer la fotografía.",
            }
            st.write(f"\\* **{method_descriptions[method]}**")

st.info(
    "**Modelo seleccionado:** OpenCV, mediante funciones clásicas de procesamiento de imágenes para mejorar "
    "el contraste y la luminosidad sin utilizar un modelo de aprendizaje automático."
)
