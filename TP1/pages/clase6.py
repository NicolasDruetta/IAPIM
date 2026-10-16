import cv2
import functions as fn
import io
import numpy as np
import pandas as pd
import streamlit as st

from PIL import Image

def body_class6():
    st.title("Clase 6: Histogramas y mejora de imágenes")

    fn.st_subheader(
        "Imagen original",
        "Muestra la imagen que se utilizará para calcular y analizar su histograma.",
    )
    image = Image.open(io.BytesIO(st.session_state.image_bytes)).convert("RGB")
    fn.show_original_image(image, st.session_state.image_name)

    image_rgb = np.array(image)
    gray_image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    manual_histogram = fn.calculate_manual_histogram(gray_image)
    automatic_histogram = cv2.calcHist(
        [gray_image],
        [0],
        None,
        [256],
        [0, 256],
    ).flatten()

    fn.st_subheader(
        "Análisis",
        "Elija una herramienta para estudiar la distribución de intensidades o mejorar la imagen.",
    )
    analysis = st.selectbox(
        "Elija un análisis",
        [
            "Histograma manual",
            "Histograma automático",
            "Interpretación",
            "Ecualización",
            "Expansión del histograma",
            "Brillo y contraste",
            "Kernel y convolución",
        ],
    )

    if analysis == "Histograma manual":
        fn.st_image(
            gray_image,
            caption="Imagen en escala de grises",
        )
        fn.get_histograma(manual_histogram, "Histograma manual")
    elif analysis == "Histograma automático":
        fn.st_image(
            gray_image,
            caption="Imagen en escala de grises",
        )
        fn.get_histograma(automatic_histogram, "Histograma con OpenCV")
    elif analysis == "Interpretación":
        fn.st_image(
            gray_image,
            caption="Imagen analizada",
        )
        fn.get_histograma(
            automatic_histogram,
            "Distribución de intensidades",
        )
        st.write(
            "Los valores cercanos a 0 representan tonos oscuros y los cercanos a "
            "255 representan tonos claros. Una distribución amplia suele indicar "
            "mayor contraste.",
        )
    elif analysis == "Ecualización":
        equalized_image = cv2.equalizeHist(gray_image)
        equalized_histogram = cv2.calcHist(
            [equalized_image],
            [0],
            None,
            [256],
            [0, 256],
        ).flatten()
        columns = st.columns(2)
        with columns[0]:
            fn.st_image(gray_image, caption="Imagen original")
        with columns[1]:
            fn.st_image(
                equalized_image,
                caption="Imagen ecualizada",
            )
        histograms = st.columns(2)
        with histograms[0]:
            fn.get_histograma(automatic_histogram, "Histograma original")
        with histograms[1]:
            fn.get_histograma(equalized_histogram, "Histograma ecualizado")
    elif analysis == "Brillo y contraste":
        contrast = st.slider(
            "Contraste",
            0.50,
            3.00,
            1.00,
            0.10,
            width=st.session_state.default_width,
        )
        brightness = st.slider(
            "Brillo",
            -100,
            100,
            0,
            width=st.session_state.default_width,
        )
        adjusted_image = cv2.convertScaleAbs(
            image_rgb,
            alpha=contrast,
            beta=brightness,
        )
        fn.st_image(
            adjusted_image,
            caption="Imagen ajustada",
        )
    elif analysis == "Expansión del histograma":
        expanded_image = cv2.normalize(
            gray_image,
            None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX,
            dtype=cv2.CV_8U,
        )
        expanded_histogram = cv2.calcHist(
            [expanded_image],
            [0],
            None,
            [256],
            [0, 256],
        ).flatten()
        columns = st.columns(2)
        with columns[0]:
            fn.st_image(gray_image, caption="Imagen original")
        with columns[1]:
            fn.st_image(
                expanded_image,
                caption="Imagen expandida",
            )
        histograms = st.columns(2)
        with histograms[0]:
            fn.get_histograma(automatic_histogram, "Histograma original")
        with histograms[1]:
            fn.get_histograma(expanded_histogram, "Histograma expandido")
    elif analysis == "Kernel y convolución":
        kernel_type = st.selectbox(
            "Elija un kernel",
            ["Promedio", "Enfoque", "Detección de bordes"],
        )
        if kernel_type == "Promedio":
            kernel = np.ones((3, 3), dtype=np.float32) / 9
        elif kernel_type == "Enfoque":
            kernel = np.array(
                [[0, -1, 0], [-1, 5, -1], [0, -1, 0]],
                dtype=np.float32,
            )
        else:
            kernel = np.array(
                [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]],
                dtype=np.float32,
            )
        filtered_image = cv2.filter2D(gray_image, -1, kernel)
        kernel_table = pd.DataFrame(kernel, columns=["0", "1", "2"])
        with st.container(width=st.session_state.default_width):
            st.table(kernel_table)
        fn.st_image(
            filtered_image,
            caption="Resultado de la convolución",
        )
