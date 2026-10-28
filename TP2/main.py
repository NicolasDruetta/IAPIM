import streamlit as st


st.set_page_config(page_title="IAPIM - Vision Lab", layout="wide")
st.set_option("client.showSidebarNavigation", False)

st.title("IAPIM - Vision Lab")
st.subheader("Laboratorio de Visión Artificial y Procesamiento de Imágenes.")
st.write("Autor: Nicolás Druetta. Año: 2026.")

with st.container(border=True):
    st.page_link(
        "pages/01_detector_facial.py",
        label=(
            "**01 – Detector facial**\n\n"
            "Capturá una fotografía con la cámara y detectá los rostros presentes"
        ),
        width="stretch",
    )
