import io
import functions as fn
import streamlit as st

from PIL import Image

def body_home(cache):
    st.title("TP1 - Procesamiento de Imágenes")

    fn.st_subheader(
        "Subir imagen",
        "Seleccione una imagen para comenzar a trabajar con ella.",
    )

    if "upload_version" not in st.session_state:
        st.session_state.upload_version = 0

    uploaded_file = st.file_uploader(
        "Seleccionar imagen",
        type=["jpg", "jpeg", "png"],
        help="Formatos admitidos: JPG, JPEG y PNG.",
        key=f"image_uploader_{st.session_state.upload_version}",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        if image_bytes != st.session_state.get("image_bytes"):
            st.session_state.image_bytes = image_bytes
            st.session_state.image_name = uploaded_file.name
            cache.dir.mkdir(exist_ok=True)
            cache.image_path.write_bytes(image_bytes)
            cache.image_name_path.write_text(uploaded_file.name, encoding="utf-8")
            st.rerun()

    if "image_bytes" in st.session_state:
        image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
        caption = fn.get_image_caption(image, st.session_state.image_name)

        with st.container(horizontal=True, width="content"):
            st.success(f"Imagen lista para procesar: {st.session_state.image_name}")
            if st.button(
                "Eliminar imagen",
                key="clear_image",
                help="Eliminar imagen y reiniciar",
                type="primary",
            ):
                fn.clear_image(
                    cache,
                )

        fn.st_image(
            image,
            caption=caption,
        )
        st.info("Ahora puede elegir una sección desde el menú lateral.")
    else:
        st.warning("El menú lateral se habilitará tras cargar una imagen.")
