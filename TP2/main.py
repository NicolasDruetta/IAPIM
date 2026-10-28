import streamlit as st

from functions import home


st.set_page_config(page_title="IAPIM Vision Lab", layout="wide")
detector_facial_page = st.Page(
    "pages/01_detector_facial.py",
    title="01 – Detector facial",
)
home_page = st.Page(home, title="Home", default=True)
selected_page = st.navigation(
    [home_page, detector_facial_page],
    position="hidden",
)
selected_page.run()
