import importlib
import io
import pages.clase1 as clase1
import pages.clase2 as clase2
import streamlit as st
import utils

from pathlib import Path
from PIL import Image

st.set_page_config(page_title="TP1", layout="wide", initial_sidebar_state="expanded")
clase1 = importlib.reload(clase1)
clase2 = importlib.reload(clase2)
utils = importlib.reload(utils)

cache_dir = Path(__file__).with_name(".cache")
cache_image_name_path = cache_dir / "last_image_name.txt"
cache_image_path = cache_dir / "last_image"
cache_page_path = cache_dir / "page.txt"
cache_theme_path = cache_dir / "theme.txt"


def restore_cached_image():
    if "image_bytes" not in st.session_state and cache_image_path.exists():
        st.session_state.image_bytes = cache_image_path.read_bytes()
        st.session_state.image_name = (
            cache_image_name_path.read_text(encoding="utf-8")
            if cache_image_name_path.exists()
            else "imagen_guardada"
        )


restore_cached_image()


def clear_image():
    st.session_state.pop("image_bytes", None)
    st.session_state.pop("image_name", None)
    st.session_state.upload_version += 1
    cache_image_path.unlink(missing_ok=True)
    cache_image_name_path.unlink(missing_ok=True)
    st.session_state.page = "Inicio"
    cache_dir.mkdir(exist_ok=True)
    cache_page_path.write_text("Inicio", encoding="utf-8")
    st.rerun()


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
    utils.title(
        "TP1 - Procesamiento de Imágenes",
        "Cargue una imagen para comenzar a trabajar con el programa.",
    )

    if "upload_version" not in st.session_state:
        st.session_state.upload_version = 0

    uploaded_file = st.file_uploader(
        "Seleccione una imagen",
        type=["jpg", "jpeg", "png"],
        help="Formatos admitidos: JPG, JPEG y PNG.",
        key=f"image_uploader_{st.session_state.upload_version}",
    )

    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        if image_bytes != st.session_state.get("image_bytes"):
            # Guardo los bytes en session_state para conservar la imagen
            # mientras navego por las distintas secciones.
            st.session_state.image_bytes = image_bytes
            st.session_state.image_name = uploaded_file.name
            cache_dir.mkdir(exist_ok=True)
            cache_image_path.write_bytes(image_bytes)
            cache_image_name_path.write_text(uploaded_file.name, encoding="utf-8")
            st.rerun()

    if "image_bytes" in st.session_state:
        image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
        dimensions = utils.get_dimensions_text(image)
        with st.container(horizontal=True, width="content"):
            st.success(f"Imagen lista para procesar: {st.session_state.image_name}")
            if st.button(
                "Eliminar imagen",
                key="clear_image",
                help="Eliminar imagen y reiniciar",
                type="primary",
            ):
                clear_image()
        st.image(image, caption=dimensions, width=768)
        st.info("Ahora puede elegir una sección desde el menú lateral.")
    else:
        st.warning("El menú lateral se habilitará después de cargar una imagen.")


pages = {
    "Inicio": home,
    "Clase 1": clase1.show_class,
    "Clase 2": clase2.show_class,
}

if "page" not in st.session_state:
    selected_page = (
        cache_page_path.read_text(encoding="utf-8")
        if cache_page_path.exists()
        else "Inicio"
    )
    st.session_state.page = selected_page if selected_page in pages else "Inicio"

if st.query_params:
    st.query_params.clear()

with st.sidebar:
    st.title("IAPIM")
    st.markdown("""
        Trabajo Práctico nro 1.  
        Autor: Nicolás Druetta.  
        Año: 2026.
    """)

    if "dark_mode" not in st.session_state:
        saved_theme = (
            cache_theme_path.read_text(encoding="utf-8")
            if cache_theme_path.exists()
            else "light"
        )
        st.session_state.dark_mode = saved_theme == "dark"

    if st.session_state.dark_mode:
        if st.button(
            "Light mode",
            icon=":material/light_mode:",
            key="light_button",
        ):
            st.session_state.dark_mode = False
            cache_dir.mkdir(exist_ok=True)
            cache_theme_path.write_text("light", encoding="utf-8")
            st.rerun()
    elif st.button(
        "Dark mode",
        icon=":material/dark_mode:",
        key="dark_button",
    ):
        st.session_state.dark_mode = True
        cache_dir.mkdir(exist_ok=True)
        cache_theme_path.write_text("dark", encoding="utf-8")
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
            cache_dir.mkdir(exist_ok=True)
            cache_page_path.write_text(page_name, encoding="utf-8")
            st.rerun()

pages[st.session_state.page]()
