import streamlit as st

from functions import configure_page

configure_page("IAPIM - Vision Lab")

st.title("IAPIM - Vision Lab")
st.subheader("Laboratorio de Visión Artificial y Procesamiento de Imágenes.")

st.divider()

first_column, second_column, third_column = st.columns(3, gap="medium")

with first_column:
    with st.container(border=True):
        st.page_link(
            "pages/01_detector_facial.py",
            label=(
                "**01 – Detector facial**\n\n"
                "Capture una fotografía con la cámara y detecte los rostros presentes"
            ),
            width="stretch",
        )

with second_column:
    with st.container(border=True):
        st.page_link(
            "pages/02_detector_de_objetos.py",
            label=(
                "**02 – Detector de objetos**\n\n"
                "Suba una imagen y detecte objetos visualmente separables"
            ),
            width="stretch",
        )

with third_column:
    with st.container(border=True):
        st.page_link(
            "pages/03_analizador_de_escenas.py",
            label=(
                "**03 – Analizador de escenas**\n\n"
                "Seleccioná una fotografía y descubrí cómo la inteligencia artificial identifica las regiones de una escena"
            ),
            width="stretch",
        )

st.divider()

empty_column, footer_column = st.columns([5, 1])

with footer_column:
    st.caption("Autor: Nicolás Druetta. Año: 2026.")
