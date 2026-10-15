
import streamlit as st

st.set_page_config(
    page_title="TP1",
    layout="wide",
    initial_sidebar_state="expanded"
)

def home():
    st.title("TP1 - Procesamiento de Imágenes")
    st.write("Bienvenido al primer trabajo práctico.")

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
    "Acerca del proyecto": about
}

if "page" not in st.session_state:
    st.session_state.page = "Inicio"

with st.sidebar:
    st.title("Procesamiento de Imágenes")
    st.write("Trabajo Práctico N.º 1")
    st.write("Autor: Nicolás")
    st.divider()

    for page_name in pages:
        if st.button(
            page_name,
            key=page_name,
            use_container_width=True,
            type="primary" if st.session_state.page == page_name else "secondary"
        ):
            st.session_state.page = page_name
            st.rerun()

pages[st.session_state.page]()
