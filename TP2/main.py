import streamlit as st

from pathlib import Path
from PIL import Image, ImageOps
from functions import configure_page

configure_page("IAPIM - Vision Lab")

ASSETS_DIRECTORY = Path(__file__).resolve().parent / "assets" / "images"
CARD_DEFINITIONS = (
    (
        "00_main/01.jpg",
        "pages/01_detector_facial.py",
        "**01 – Detector de emociones faciales con FER+**",
        "Detecte rostros y analice sus expresiones faciales.",
    ),
    (
        "00_main/02.jpg",
        "pages/02_reconocedor_de_gestos.py",
        "**02 – Reconocedor de gestos de manos con MediaPipe**",
        "Detecte manos e identifique gestos mediante inteligencia artificial.",
    ),
    (
        "03_detector_de_objetos/01.jpg",
        "pages/03_detector_de_objetos.py",
        "**03 – Detector de objetos con YOLO11n**",
        "Detecte objetos visualmente separables.",
    ),
    (
        "04_extractor_de_fondos/01.jpg",
        "pages/04_extractor_de_fondos.py",
        "**04 – Extractor inteligente de fondos con RMBG-1.4**",
        "Separe el objeto principal de una fotografía.",
    ),
    (
        "05_analizador_de_escenas/01.jpg",
        "pages/05_analizador_de_escenas.py",
        "**05 – Analizador de escenas con SegFormer**",
        "Identifique regiones semánticas en escenas.",
    ),
    (
        "06_mejorador_de_imagenes/01.jpg",
        "pages/06_mejorador_de_imagenes.py",
        "**06 – Mejorador inteligente de imágenes con OpenCV**",
        "Mejore el contraste y la luminosidad de una fotografía.",
    ),
    (
        "07_clasificador_de_imagenes/01.jpg",
        "pages/07_clasificador_de_imagenes.py",
        "**07 – Clasificador de imágenes con MobileNetV2**",
        "Clasifique fotografías en categorías de ImageNet.",
    ),
)

with st.container(horizontal=True, vertical_alignment="center", width="content"):
    st.title("IAPIM - Vision Lab")
st.subheader("Laboratorio de Visión Artificial y Procesamiento de Imágenes.")

st.divider()

for row_start in range(0, len(CARD_DEFINITIONS), 4):
    card_columns = st.columns(4, gap="small")
    for card_column, card_definition in zip(
        card_columns,
        CARD_DEFINITIONS[row_start:row_start + 4],
    ):
        image_relative_path, page_path, title, description = card_definition
        with card_column:
            with st.container(border=True, height="stretch"):
                card_image = ImageOps.fit(
                    Image.open(ASSETS_DIRECTORY / image_relative_path).convert("RGB"),
                    (640, 360),
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.5),
                )
                st.image(card_image, width="stretch")
                if page_path is None:
                    st.write(title)
                    st.caption(description)
                else:
                    st.page_link(
                        page_path,
                        label=f"{title}\n\n{description}",
                        width="stretch",
                    )

st.divider()

with st.container(key="footer"):
    st.caption("Autor: Nicolás Druetta. Año: 2026.")
