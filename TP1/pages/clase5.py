import cv2
import functions as fn
import io
import numpy as np
import streamlit as st

from PIL import Image

def body_class5():
    st.title("Clase 5: Transformaciones geométricas y filtrado")

    fn.st_subheader(
        "Imagen original",
        "Muestra la imagen cargada antes de aplicar una operación o un filtro.",
    )
    image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
    fn.show_original_image(image, st.session_state.image_name)

    fn.st_subheader(
        "Transformaciones geométricas",
        "Permite desplazar, rotar y escalar la imagen.",
    )
    transformation = st.radio(
        "",
        [
            "Imagen original",
            "Traslación",
            "Rotación",
            "Escalado",
        ],
        horizontal=True,
        key="class5_transformation",
        label_visibility="collapsed",
    )

    image_rgb = np.array(image)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    rows, columns = image_bgr.shape[:2]
    default_width = st.session_state.default_width

    transformation_image = image_rgb
    transformation_cod = "image_rgb"
    transformation_width = default_width

    if transformation == "Traslación":
        horizontal = st.slider("Desplazamiento horizontal", -columns, columns, min(100, columns), width=default_width)
        vertical = st.slider("Desplazamiento vertical", -rows, rows, min(50, rows), width=default_width)
        matrix = np.float32([[1, 0, horizontal], [0, 1, vertical]])
        transformation_image = cv2.cvtColor(cv2.warpAffine(image_bgr, matrix, (columns, rows)), cv2.COLOR_BGR2RGB)
        transformation_cod = ("cv2.cvtColor(cv2.warpAffine(image_bgr, matrix, (columns, rows)), cv2.COLOR_BGR2RGB)")
    elif transformation == "Rotación":
        angle = st.slider("Ángulo", -180, 180, 45, width=default_width)
        scale = st.slider("Escala", 0.10, 2.00, 1.00, 0.10, width=default_width)
        center = (columns // 2, rows // 2)
        transformation_image = cv2.cvtColor(cv2.warpAffine(image_bgr, cv2.getRotationMatrix2D(center, angle, scale), (columns, rows)), cv2.COLOR_BGR2RGB)
        transformation_cod = ("cv2.cvtColor(cv2.warpAffine(image_bgr, cv2.getRotationMatrix2D(center, angle, scale), (columns, rows)), cv2.COLOR_BGR2RGB)")
    elif transformation == "Escalado":
        scale = st.slider("Factor de escala", 0.10, 2.00, 0.50, 0.10, width=default_width)
        transformation_image = cv2.cvtColor(cv2.resize(image_bgr, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR), cv2.COLOR_BGR2RGB)
        transformation_width = max(1, int(default_width * scale))
        transformation_cod = ("cv2.cvtColor(cv2.resize(image_bgr, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR), cv2.COLOR_BGR2RGB)")
    fn.st_image(
        transformation_image,
        caption=transformation_cod,
        width=transformation_width,
    )

    fn.st_subheader(
        "Filtros",
        "Permite suavizar la imagen y detectar sus bordes mediante kernels y umbrales.",
    )
    filter_name = st.radio(
        "",
        [
            "Imagen original",
            "Desenfoque promedio",
            "Desenfoque gaussiano",
            "Sobel",
            "Canny",
        ],
        horizontal=True,
        key="class5_filter",
        label_visibility="collapsed",
    )

    filter_image = image_rgb
    filter_cod = "image_rgb"

    if filter_name == "Desenfoque promedio":
        kernel_size = st.slider("Tamaño del kernel", 1, 31, 5, 2, width=default_width)
        filter_image = cv2.cvtColor(
            cv2.blur(image_bgr, (kernel_size, kernel_size)),
            cv2.COLOR_BGR2RGB,
        )
        filter_cod = ("cv2.blur(image_bgr, (kernel_size, kernel_size))")
    elif filter_name == "Desenfoque gaussiano":
        kernel_size = st.slider("Tamaño del kernel", 1, 31, 5, 2, width=default_width)
        filter_image = cv2.cvtColor(
            cv2.GaussianBlur(
                image_bgr,
                (kernel_size, kernel_size),
                0,
            ),
            cv2.COLOR_BGR2RGB,
        )
        filter_cod = ("cv2.GaussianBlur(image_bgr, (kernel_size, kernel_size), 0)")
    elif filter_name == "Sobel":
        direction = st.radio(
            "Dirección",
            ["Horizontal", "Vertical", "Ambos"],
            horizontal=True,
            key="class5_sobel_direction",
        )
        kernel_size = st.slider("Tamaño del kernel Sobel", 1, 7, 3, 2, width=default_width)
        if direction == "Horizontal":
            sobel_image = cv2.Sobel(
                gray_image,
                cv2.CV_64F,
                1,
                0,
                ksize=kernel_size,
            )
            filter_cod = ("cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=kernel_size)")
        elif direction == "Vertical":
            sobel_image = cv2.Sobel(
                gray_image,
                cv2.CV_64F,
                0,
                1,
                ksize=kernel_size,
            )
            filter_cod = ("cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=kernel_size)")
        else:
            sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=kernel_size)
            sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=kernel_size)
            sobel_image = cv2.magnitude(sobel_x.astype(np.float32), sobel_y.astype(np.float32))
            filter_cod = ("cv2.magnitude(cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=kernel_size), cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=kernel_size))")
        filter_image = cv2.normalize(
            np.abs(sobel_image),
            None,
            0,
            255,
            cv2.NORM_MINMAX,
        ).astype(np.uint8)
    elif filter_name == "Canny":
        lower_threshold = st.slider("Umbral inferior", 0, 255, 100, width=default_width)
        upper_threshold = st.slider("Umbral superior", 0, 255, 200, width=default_width)
        filter_image = cv2.Canny(
            gray_image,
            lower_threshold,
            upper_threshold,
        )
        filter_cod = ("cv2.Canny(gray_image, lower_threshold, upper_threshold)")
    fn.st_image(filter_image, caption=filter_cod)
