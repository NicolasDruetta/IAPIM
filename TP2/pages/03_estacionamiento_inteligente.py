import numpy as np
import streamlit as st

from functions import configure_page
from pathlib import Path

gallery_directory = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "images"
    / "03_estacionamiento_inteligente"
)
gallery_extensions = {".jpg", ".jpeg", ".png"}
gallery_images = sorted(
    image_path
    for image_path in gallery_directory.glob("*")
    if image_path.suffix.lower() in gallery_extensions
)

configure_page("IAPIM - Estacionamiento inteligente")

title_column, home_column = st.columns([5, 1])

with title_column:
    st.title("03 – Estacionamiento inteligente")
    st.write(
        "Seleccione una imagen de la galería para analizar las plazas de estacionamiento."
    )

with home_column:
    st.write("")
    st.write("")
    if st.button("Volver al Inicio", width="stretch"):
        st.switch_page("main.py")

empty_result_image = np.full((400, 640, 3), 45, dtype=np.uint8)

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Selección de imagen")
    st.write("Cargue una imagen para analizarla.")
    uploaded_image = st.file_uploader(
        "Cargue una imagen",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    st.write("Imágenes precargadas")

    if not gallery_images:
        st.warning("La galería todavía no contiene imágenes de estacionamientos.")
    else:
        if "selected_parking_image" not in st.session_state:
            st.session_state.selected_parking_image = None

        gallery_columns_count = min(5, len(gallery_images))

        for row_start in range(0, len(gallery_images), gallery_columns_count):
            gallery_row = gallery_images[
                row_start:row_start + gallery_columns_count
            ]
            gallery_columns = st.columns(gallery_columns_count, gap="small")

            for gallery_column, image_path in zip(gallery_columns, gallery_row):
                with gallery_column:
                    with st.container(border=True):
                        st.image(image_path.read_bytes(), width="stretch")
                        if st.button(
                            "Usar",
                            key=f"parking_{image_path.name}",
                            width="stretch",
                        ):
                            st.session_state.selected_parking_image = image_path

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía con las plazas detectadas.")
    if uploaded_image is not None:
        st.image(
            uploaded_image.getvalue(),
            caption="Imagen seleccionada",
            width="stretch",
        )
    elif st.session_state.get("selected_parking_image") is not None:
        selected_image_path = st.session_state.selected_parking_image
        st.image(
            selected_image_path.read_bytes(),
            caption="Imagen seleccionada",
            width="stretch",
        )
    else:
        st.image(empty_result_image, width="stretch")
