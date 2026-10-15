import importlib
import functions as fn
import pages.clase1 as clase1
import pages.clase2 as clase2
import pages.clase3 as clase3
import pages.home as home
import streamlit as st

from functools import partial
from pathlib import Path
from types import SimpleNamespace

st.set_page_config(page_title="TP1", layout="wide", initial_sidebar_state="expanded")
fn = importlib.reload(fn)
clase1 = importlib.reload(clase1)
clase2 = importlib.reload(clase2)
clase3 = importlib.reload(clase3)
home = importlib.reload(home)

cache = SimpleNamespace(
    dir=Path(__file__).with_name(".cache"),
    image_name_path=Path(__file__).with_name(".cache") / "last_image_name.txt",
    image_path=Path(__file__).with_name(".cache") / "last_image",
    page_path=Path(__file__).with_name(".cache") / "page.txt",
    theme_path=Path(__file__).with_name(".cache") / "theme.txt",
)

fn.restore_cached_image(cache)

pages = {
    "Inicio": partial(
        home.body_home,
        cache,
    ),
    "Clase 1": clase1.body_class1,
    "Clase 2": clase2.body_class2,
    "Clase 3": clase3.body_class3,
}

if "page" not in st.session_state:
    selected_page = (
        cache.page_path.read_text(encoding="utf-8")
        if cache.page_path.exists()
        else "Inicio"
    )
    st.session_state.page = selected_page if selected_page in pages else "Inicio"

if st.session_state.page != "Inicio" and "image_bytes" not in st.session_state:
    st.session_state.page = "Inicio"
    cache.dir.mkdir(exist_ok=True)
    cache.page_path.write_text("Inicio", encoding="utf-8")

if st.query_params:
    st.query_params.clear()

with st.sidebar:
    st.title("IAPIM")
    # Doble espacio para salto de línea simple en markdown.
    st.markdown("""
        Trabajo Práctico nro 1.  
        Autor: Nicolás Druetta.  
        Año: 2026.
    """)

    if "dark_mode" not in st.session_state:
        saved_theme = (
            cache.theme_path.read_text(encoding="utf-8")
            if cache.theme_path.exists()
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
            cache.dir.mkdir(exist_ok=True)
            cache.theme_path.write_text("light", encoding="utf-8")
            st.rerun()
    elif st.button(
        "Dark mode",
        icon=":material/dark_mode:",
        key="dark_button",
    ):
        st.session_state.dark_mode = True
        cache.dir.mkdir(exist_ok=True)
        cache.theme_path.write_text("dark", encoding="utf-8")
        st.rerun()

fn.apply_theme(st.session_state.dark_mode)

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
            cache.dir.mkdir(exist_ok=True)
            cache.page_path.write_text(page_name, encoding="utf-8")
            st.rerun()

pages[st.session_state.page]()
