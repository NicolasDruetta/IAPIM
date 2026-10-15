import importlib
import io
import pages.clase1 as clase1
import streamlit as st

from pathlib import Path
from PIL import Image
from utils import get_dimensions_text

st.set_page_config(page_title="TP1", layout="wide", initial_sidebar_state="expanded")
clase1 = importlib.reload(clase1)

image_cache_dir = Path(__file__).with_name(".cache")
image_cache_path = image_cache_dir / "last_image"
image_name_cache_path = image_cache_dir / "last_image_name.txt"


def restore_cached_image():
    if "image_bytes" not in st.session_state and image_cache_path.exists():
        st.session_state.image_bytes = image_cache_path.read_bytes()
        st.session_state.image_name = (
            image_name_cache_path.read_text(encoding="utf-8")
            if image_name_cache_path.exists()
            else "imagen_guardada"
        )


restore_cached_image()


def clear_image():
    st.session_state.pop("image_bytes", None)
    st.session_state.pop("image_name", None)
    st.session_state.upload_version += 1
    image_cache_path.unlink(missing_ok=True)
    image_name_cache_path.unlink(missing_ok=True)
    st.session_state.page = "Inicio"
    st.query_params.pop("page", None)
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
    st.title("TP1 - Procesamiento de Imágenes")
    st.write("Cargá una imagen para comenzar a trabajar con el programa.")

    if "upload_version" not in st.session_state:
        st.session_state.upload_version = 0

    uploaded_file = st.file_uploader(
        "Seleccioná una imagen",
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
            image_cache_dir.mkdir(exist_ok=True)
            image_cache_path.write_bytes(image_bytes)
            image_name_cache_path.write_text(uploaded_file.name, encoding="utf-8")
            st.rerun()

    if "image_bytes" in st.session_state:
        image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
        dimensions = get_dimensions_text(image)
        status_column, clear_column = st.columns([6, 3])
        with status_column:
            st.success(f"Imagen lista para procesar: {st.session_state.image_name}")
        with clear_column:
            if st.button(
                "Eliminar imagen",
                key="clear_image",
                help="Eliminar imagen y reiniciar",
                type="primary",
            ):
                clear_image()
        st.image(image, caption=dimensions, width=768)
        st.info("Ahora podés elegir una sección desde el menú lateral.")
    else:
        st.warning("El menú lateral se habilitará después de cargar una imagen.")


pages = {
    "Inicio": home,
    "Clase 1": clase1.show_class,
}

if "page" not in st.session_state:
    selected_page = st.query_params.get("page", "Inicio")
    st.session_state.page = selected_page if selected_page in pages else "Inicio"

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
        if st.button(
            "Light mode",
            icon=":material/light_mode:",
            key="light_button",
        ):
            st.session_state.dark_mode = False
            st.query_params["theme"] = "light"
            st.rerun()
    elif st.button(
        "Dark mode",
        icon=":material/dark_mode:",
        key="dark_button",
    ):
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
            st.query_params["page"] = page_name
            st.rerun()

pages[st.session_state.page]()
