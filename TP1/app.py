
import io
import streamlit as st

from pathlib import Path
from PIL import Image

st.set_page_config(page_title="TP1", layout="wide", initial_sidebar_state="expanded")

def apply_theme(dark_mode):
    """Aplica el tema visual elegido en la barra lateral."""
    if dark_mode:
        theme_variables = {
            "--background": "#0E1117",
            "--sidebar": "#161B22",
            "--text": "#FAFAFA",
            "--selected": "#26364A",
            "--selected-text": "#9FB3C8",
            "--disabled": "#21262D",
            "--disabled-text": "#8B949E",
            "--control": "#262730",
            "--border": "#30363D",
            "--warning-text": "#FFD166",
            "--success-text": "#A5D6A7",
            "--info-text": "#90CAF9",
            "--color-scheme": "dark",
        }
    else:
        theme_variables = {
            "--background": "#FFFFFF",
            "--sidebar": "#F0F2F6",
            "--text": "#262730",
            "--selected": "#D6E4F7",
            "--selected-text": "#5B6B84",
            "--disabled": "#E8E1E3",
            "--disabled-text": "#6B7280",
            "--control": "#FFFFFF",
            "--border": "#D6D9E0",
            "--warning-text": "#7A4B00",
            "--success-text": "#1B5E20",
            "--info-text": "#2F6FB5",
            "--color-scheme": "light",
        }

    stylesheet_path = Path(__file__).with_name("style.css")
    stylesheet = stylesheet_path.read_text(encoding="utf-8")
    variables = (
        ":root {"
        + "".join(f"{name}: {value};" for name, value in theme_variables.items())
        + "}"
    )
    st.markdown(f"<style>{variables}{stylesheet}</style>", unsafe_allow_html=True)

def home():
    st.title("TP1 - Procesamiento de Imágenes")
    st.write("Cargá una imagen para comenzar a trabajar con el programa.")

    uploaded_file = st.file_uploader(
        "Seleccioná una imagen",
        type=["jpg", "jpeg", "png"],
        help="Formatos admitidos: JPG, JPEG y PNG.",
    )

    if uploaded_file is not None:
        # Guardo los bytes en session_state para conservar la imagen
        # mientras navego por las distintas secciones.
        st.session_state.image_bytes = uploaded_file.getvalue()
        st.session_state.image_name = uploaded_file.name

    if "image_bytes" in st.session_state:
        image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
        st.success(f"Imagen lista para procesar: {st.session_state.image_name}")
        st.image(image, caption="Imagen de trabajo", use_container_width=True)
        st.info("Ahora podés elegir una sección desde el menú lateral.")
    else:
        st.warning("El menú lateral se habilitará después de cargar una imagen.")

def process_image():
    st.title("Procesar imagen")

def compare_images():
    st.title("Comparar imágenes")

def about():
    st.title("Acerca del proyecto")

pages = {
    "Inicio": home,
    "Procesar imagen": process_image,
    "Comparar imágenes": compare_images,
    "Acerca del proyecto": about,
}

if "page" not in st.session_state:
    st.session_state.page = "Inicio"

with st.sidebar:
    st.title("IAPIM")
    st.markdown("""
        Trabajo Práctico nro 1.  
        Autor: Nicolás Druetta.  
        Año: 2026.
    """)

    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = st.query_params.get("theme", "light") == "dark"

    if st.session_state.dark_mode:
        if st.button("☀️ Light mode", key="light_button"):
            st.session_state.dark_mode = False
            st.query_params["theme"] = "light"
            st.rerun()
    elif st.button("🌙 Dark mode", key="dark_button"):
        st.session_state.dark_mode = True
        st.query_params["theme"] = "dark"
        st.rerun()

apply_theme(st.session_state.dark_mode)

with st.sidebar:
    st.divider()
    image_loaded = "image_bytes" in st.session_state

    for page_name in pages:
        if st.button(
            page_name,
            key=page_name,
            use_container_width=True,
            type="primary" if st.session_state.page == page_name else "secondary",
            disabled=page_name != "Inicio" and not image_loaded,
        ):
            st.session_state.page = page_name
            st.rerun()

pages[st.session_state.page]()
