import cv2
import io
import functions as fn
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

    image_rgb = np.array(image)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    rows, columns = image_bgr.shape[:2]

    fn.st_subheader(
        "Operación o filtro",
        "Permite desplazar, rotar, escalar o analizar los bordes de la imagen.",
    )
    operation = st.selectbox(
        "Elija una operación o filtro",
        [
            "Imagen original",
            "Traslación",
            "Rotación",
            "Escalado",
            "Desenfoque promedio",
            "Desenfoque gaussiano",
            "Sobel",
            "Canny",
        ],
    )

    result = image_rgb
    if operation == "Traslación":
        horizontal = st.slider(
            "Desplazamiento horizontal",
            -columns,
            columns,
            min(100, columns),
            width=st.session_state.default_width,
        )
        vertical = st.slider(
            "Desplazamiento vertical",
            -rows,
            rows,
            min(50, rows),
            width=st.session_state.default_width,
        )
        matrix = np.float32([[1, 0, horizontal], [0, 1, vertical]])
        result = cv2.cvtColor(
            cv2.warpAffine(image_bgr, matrix, (columns, rows)),
            cv2.COLOR_BGR2RGB,
        )
    elif operation == "Rotación":
        angle = st.slider(
            "Ángulo",
            -180,
            180,
            45,
            width=st.session_state.default_width,
        )
        scale = st.slider(
            "Escala",
            0.10,
            2.00,
            1.00,
            0.10,
            width=st.session_state.default_width,
        )
        center = (columns // 2, rows // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, scale)
        result = cv2.cvtColor(
            cv2.warpAffine(image_bgr, matrix, (columns, rows)),
            cv2.COLOR_BGR2RGB,
        )
    elif operation == "Escalado":
        scale = st.slider(
            "Factor de escala",
            0.10,
            2.00,
            0.50,
            0.10,
            width=st.session_state.default_width,
        )
        result = cv2.cvtColor(
            cv2.resize(
                image_bgr,
                None,
                fx=scale,
                fy=scale,
                interpolation=cv2.INTER_LINEAR,
            ),
            cv2.COLOR_BGR2RGB,
        )
    elif operation == "Desenfoque promedio":
        kernel_size = st.slider(
            "Tamaño del kernel",
            1,
            31,
            5,
            2,
            width=st.session_state.default_width,
        )
        result = cv2.cvtColor(
            cv2.blur(image_bgr, (kernel_size, kernel_size)),
            cv2.COLOR_BGR2RGB,
        )
    elif operation == "Desenfoque gaussiano":
        kernel_size = st.slider(
            "Tamaño del kernel",
            1,
            31,
            5,
            2,
            width=st.session_state.default_width,
        )
        result = cv2.cvtColor(
            cv2.GaussianBlur(
                image_bgr,
                (kernel_size, kernel_size),
                0,
            ),
            cv2.COLOR_BGR2RGB,
        )
    elif operation == "Sobel":
        direction = st.radio(
            "Dirección",
            ["Horizontal", "Vertical", "Ambos"],
            horizontal=True,
        )
        kernel_size = st.slider(
            "Tamaño del kernel Sobel",
            1,
            7,
            3,
            2,
            width=st.session_state.default_width,
        )
        if direction == "Horizontal":
            result = cv2.Sobel(
                gray_image,
                cv2.CV_64F,
                1,
                0,
                ksize=kernel_size,
            )
        elif direction == "Vertical":
            result = cv2.Sobel(
                gray_image,
                cv2.CV_64F,
                0,
                1,
                ksize=kernel_size,
            )
        else:
            sobel_x = cv2.Sobel(
                gray_image,
                cv2.CV_64F,
                1,
                0,
                ksize=kernel_size,
            )
            sobel_y = cv2.Sobel(
                gray_image,
                cv2.CV_64F,
                0,
                1,
                ksize=kernel_size,
            )
            result = cv2.magnitude(sobel_x, sobel_y)
    elif operation == "Canny":
        lower_threshold = st.slider(
            "Umbral inferior",
            0,
            255,
            100,
            width=st.session_state.default_width,
        )
        upper_threshold = st.slider(
            "Umbral superior",
            0,
            255,
            200,
            width=st.session_state.default_width,
        )
        result = cv2.Canny(
            gray_image,
            lower_threshold,
            upper_threshold,
        )

    fn.st_image(
        result,
        caption=f"Resultado: {operation}",
    )
