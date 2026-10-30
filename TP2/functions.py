"""Utilidades compartidas del laboratorio IAPIM Vision Lab."""

import streamlit as st

from pathlib import Path

def configure_page(page_title):
    """Configura una página con el estilo y la identidad del laboratorio."""
    st.set_page_config(
        page_title=page_title,
        page_icon=Path(__file__).resolve().parent / "assets" / "icon.png",
        layout="wide",
    )

    custom_css_path = Path(__file__).resolve().parent / "assets" / "custom.css"
    custom_css = custom_css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)
