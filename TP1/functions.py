import streamlit as st

from pathlib import Path

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

def clear_image(cache):
    st.session_state.pop("image_bytes", None)
    st.session_state.pop("image_name", None)
    st.session_state.upload_version += 1

    cache.image_path.unlink(missing_ok=True)
    cache.image_name_path.unlink(missing_ok=True)

    st.session_state.page = "Inicio"
    cache.dir.mkdir(exist_ok=True)
    cache.page_path.write_text("Inicio", encoding="utf-8")
    st.rerun()

def get_dimensions_text(image, max_width=520):
    original_width, original_height = image.size
    display_width = min(max_width, original_width)
    display_height = round(original_height * display_width / original_width)

    return original_width, original_height, display_width, display_height

def get_image_caption(image, image_name, max_width=520):
    dimensions = get_dimensions_text(image, max_width)
    original_width, original_height, display_width, display_height = dimensions
    return (
        f"{image_name} - Original: {original_width} x {original_height} px "
        f"(Escalado: {display_width} x {display_height} px)"
    )

def restore_cached_image(cache):
    if "image_bytes" not in st.session_state and cache.image_path.exists():
        st.session_state.image_bytes = cache.image_path.read_bytes()

        st.session_state.image_name = (
            cache.image_name_path.read_text(encoding="utf-8")
            if cache.image_name_path.exists()
            else "imagen_guardada"
        )

def show_basic_info(image):
    width, height = image.size

    st.write(f"**Nombre:** {st.session_state.image_name}")
    st.write(f"**Dimensiones:** {width} x {height} píxeles")
    st.write(f"**Canales:** {len(image.getbands())}")
    st.write(f"**Modo:** {image.mode}")

def show_color_channels(image):
    columns = st.columns(3)

    for column, channel in zip(columns, image.getbands()):
        with column:
            st_image(
                image.getchannel(channel),
                caption=f"Canal {channel}",
                width="stretch",
            )

def show_original_image(image, image_name):
    caption = get_image_caption(image, image_name)
    st_image(image, caption=caption)

def st_image(image, caption=None, width=520):
    st.image(image, caption=caption, width=width)

def st_subheader(subheader, write=None):
    st.markdown('<br>', unsafe_allow_html=True)
    st.subheader(subheader)
    if write:
        st.write(write)
    st.markdown('<hr class="divider-alt">', unsafe_allow_html=True)
