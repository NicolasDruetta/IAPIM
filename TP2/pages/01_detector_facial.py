import streamlit as st

from functions import detect_faces, home


if "camera_key" not in st.session_state:
    st.session_state.camera_key = 0
if "captured_image_bytes" not in st.session_state:
    st.session_state.captured_image_bytes = None
if "detection_error" not in st.session_state:
    st.session_state.detection_error = None
if "detection_result" not in st.session_state:
    st.session_state.detection_result = None
if "face_count" not in st.session_state:
    st.session_state.face_count = 0

st.title("01 – Detector facial")
st.write("Capturá una fotografía y analizala para detectar rostros.")

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Captura de imagen")
    captured_image = st.camera_input(
        "Tomá una fotografía con la cámara",
        key=f"camera_input_{st.session_state.camera_key}",
    )

    if captured_image is not None:
        captured_image_bytes = captured_image.getvalue()

        if st.session_state.captured_image_bytes != captured_image_bytes:
            st.session_state.captured_image_bytes = captured_image_bytes

            try:
                processed_image, face_count = detect_faces(captured_image_bytes)
            except (RuntimeError, ValueError) as error:
                st.session_state.detection_error = str(error)
                st.session_state.detection_result = None
                st.session_state.face_count = 0
            else:
                st.session_state.detection_error = None
                st.session_state.detection_result = processed_image
                st.session_state.face_count = face_count
    elif st.session_state.captured_image_bytes is not None:
        st.session_state.camera_key += 1
        st.session_state.captured_image_bytes = None
        st.session_state.detection_error = None
        st.session_state.detection_result = None
        st.session_state.face_count = 0
        st.rerun()

with right_column:
    st.subheader("Resultados del análisis")

    if st.session_state.detection_error:
        st.error(st.session_state.detection_error)
    elif st.session_state.detection_result is None:
        st.info("Todavía no se ejecutó ningún análisis.")
    else:
        st.image(
            st.session_state.detection_result,
            caption="Fotografía procesada",
        )
        st.metric("Rostros detectados", st.session_state.face_count)

        if st.session_state.face_count == 0:
            st.warning("No se detectaron rostros en la fotografía.")

if st.button("Volver al Home"):
    st.switch_page(st.Page(home, title="Home"))
