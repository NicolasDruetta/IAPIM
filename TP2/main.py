import streamlit as st

from functions import load_custom_css


st.set_page_config(page_title="IAPIM - Vision Lab", layout="wide")

load_custom_css()

st.title("IAPIM - Vision Lab")
st.subheader("Laboratorio de Visión Artificial y Procesamiento de Imágenes.")
st.write("Autor: Nicolás Druetta. Año: 2026.")

first_column, second_column, third_column = st.columns(3, gap="medium")

with first_column:
    with st.container(border=True):
        st.page_link(
            "pages/01_detector_facial.py",
            label=(
                "**01 – Detector facial**\n\n"
                "Capturá una fotografía con la cámara y detectá los rostros presentes"
            ),
            width="stretch",
        )

with second_column:
    with st.container(border=True):
        st.page_link(
            "pages/02_detector_de_objetos.py",
            label=(
                "**02 – Detector de objetos**\n\n"
                "Subí una imagen y detectá objetos visualmente separables"
            ),
            width="stretch",
        )

with third_column:
    with st.container(border=True):
        st.page_link(
            "pages/03_estacionamiento_inteligente.py",
            label=(
                "**03 – Estacionamiento inteligente**\n\n"
                "Analizá plazas libres y ocupadas en imágenes de estacionamiento"
            ),
            width="stretch",
        )
