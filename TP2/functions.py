"""Utilidades compartidas del laboratorio IAPIM Vision Lab."""

import streamlit as st

from pathlib import Path


def load_custom_css():
    """Carga el archivo CSS compartido por todas las páginas."""
    custom_css_path = Path(__file__).resolve().parent / "assets" / "custom.css"
    custom_css = custom_css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)
