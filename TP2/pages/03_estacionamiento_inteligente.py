import streamlit as st

from functions import load_custom_css
from pathlib import Path


gallery_directory = (
    Path(__file__).resolve().parents[1]
    / "images"
    / "03_estacionamiento_inteligente"
)
gallery_extensions = {".jpg", ".jpeg", ".png"}
gallery_images = sorted(
    image_path
    for image_path in gallery_directory.glob("*")
    if image_path.suffix.lower() in gallery_extensions
)

st.set_page_config(
    page_title="IAPIM - Estacionamiento inteligente",
    layout="wide",
)

load_custom_css()

st.title("03 – Estacionamiento inteligente")
st.write(
    "Seleccioná una imagen de la galería para analizar las plazas de estacionamiento."
)

if not gallery_images:
    st.warning(
        "La galería todavía no contiene imágenes de estacionamientos. "
        "Para habilitar esta herramienta necesitamos fotografías propias de "
        "estacionamientos con varias plazas visibles, tomadas desde un punto "
        "fijo y con buena iluminación."
    )
    st.info(
        "También será necesario definir las regiones de interés de cada plaza "
        "para cada fotografía antes de calcular ocupación."
    )
else:
    st.error(
        "Las imágenes de la galería están disponibles, pero todavía no tienen "
        "regiones de interés definidas para este escenario."
    )

st.page_link("main.py", label="Volver al Home")
