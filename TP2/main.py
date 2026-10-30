import streamlit as st

from functions import configure_page

configure_page("IAPIM - Vision Lab")

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
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
                "Detecte rostros en fotografías"
            ),
            width="stretch",
        )

with second_column:
    with st.container(border=True):
        st.page_link(
            "pages/02_detector_de_objetos.py",
            label=(
                "**02 – Detector de objetos**\n\n"
                "Detecte objetos visualmente separables"
            ),
            width="stretch",
        )

with third_column:
    with st.container(border=True):
        st.page_link(
            "pages/03_analizador_de_escenas.py",
            label=(
                "**03 – Analizador de escenas**\n\n"
                "Identifique regiones semánticas en escenas"
            ),
            width="stretch",
        )

fourth_column, empty_column, another_empty_column = st.columns(3, gap="medium")

with fourth_column:
    with st.container(border=True):
        st.page_link(
            "pages/04_lector_de_dados.py",
            label=(
                "**04 – Lector inteligente de dados**\n\n"
                "Detectá dados en una fotografía, contá sus puntos y calculá el resultado total"
            ),
            width="stretch",
        )

st.divider()

with st.container(key="footer"):
    st.caption("Autor: Nicolás Druetta. Año: 2026.")
