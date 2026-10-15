import streamlit as st

def title(title_text, subtitle):
    st.title(title_text)
    st.write(subtitle)
    st.divider()

def get_dimensions_text(image, max_width=768):
    original_width, original_height = image.size
    display_width = min(max_width, original_width)
    display_height = round(original_height * display_width / original_width)
    return (
        f"Original: {original_width} x {original_height} px "
        f"(Escalado: {display_width} x {display_height} px)"
    )
