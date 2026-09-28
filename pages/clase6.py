import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

st.title("Clase 6")
uploaded_file = st.file_uploader("Subí una imagen", type=["jpg", "jpeg", "png"])
if uploaded_file is None:
    st.stop()

# Convierte la imagen a los formatos necesarios para trabajar con histogramas y contraste.
image_pil = Image.open(uploaded_file).convert("RGB")
image_rgb = np.array(image_pil)
image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

# Calcula el histograma manualmente recorriendo todos los píxeles.
def calculate_manual_histogram(image):
    histogram = np.zeros(256, dtype=int)
    for row in image:
        for intensity in row:
            histogram[intensity] += 1
    return histogram

# Genera una figura reutilizable para visualizar histogramas.
def create_histogram_figure(histogram, title):
    figure, axis = plt.subplots(figsize=(10, 4))
    axis.plot(histogram)
    axis.set_title(title)
    axis.set_xlabel("Niveles de intensidad")
    axis.set_ylabel("Frecuencia")
    axis.set_xlim([0, 255])
    axis.grid(True, alpha=0.25)
    return figure

manual_histogram = calculate_manual_histogram(gray_image)
opencv_histogram = cv2.calcHist([gray_image], [0], None, [256], [0, 256]).flatten()

# Menú interno de la Clase 6.
st.sidebar.markdown("## **Clase 6**")
section = st.sidebar.radio("Contenido", ["Imagen original", "Histograma manual", "Histograma automático", "Interpretación", "Ecualización", "Brillo y contraste", "Expansión del histograma", "Kernel y convolución"])

if section == "Imagen original":
    st.code('image = cv2.imread("imagen.jpg", cv2.IMREAD_GRAYSCALE)', language="python")
    st.image(image_rgb, caption="Imagen original", use_container_width=True)

elif section == "Histograma manual":
    st.code("histogram = np.zeros(256, dtype=int)\nhistogram[intensity] += 1", language="python")
    st.image(gray_image, caption="Imagen en escala de grises", use_container_width=True, clamp=True)
    st.pyplot(create_histogram_figure(manual_histogram, "Histograma manual"))

elif section == "Histograma automático":
    st.code("histogram = cv2.calcHist([image], [0], None, [256], [0, 256])", language="python")
    st.image(gray_image, caption="Imagen en escala de grises", use_container_width=True, clamp=True)
    st.pyplot(create_histogram_figure(opencv_histogram, "Histograma con OpenCV"))

elif section == "Interpretación":
    st.image(gray_image, caption="Imagen analizada", use_container_width=True, clamp=True)
    st.pyplot(create_histogram_figure(opencv_histogram, "Distribución de intensidades"))
    st.write("Izquierda: tonos oscuros. Derecha: tonos claros. Rango estrecho: bajo contraste. Distribución amplia: mayor variedad tonal.")

elif section == "Ecualización":
    equalized_image = cv2.equalizeHist(gray_image)
    equalized_histogram = cv2.calcHist([equalized_image], [0], None, [256], [0, 256]).flatten()
    st.code("equalized_image = cv2.equalizeHist(image)", language="python")
    col1, col2 = st.columns(2)
    with col1:
        st.image(gray_image, caption="Imagen original", use_container_width=True, clamp=True)
    with col2:
        st.image(equalized_image, caption="Imagen ecualizada", use_container_width=True, clamp=True)
    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(create_histogram_figure(opencv_histogram, "Histograma original"))
    with col4:
        st.pyplot(create_histogram_figure(equalized_histogram, "Histograma ecualizado"))

elif section == "Brillo y contraste":
    contrast = st.slider("Contraste", 0.50, 3.00, 1.00, 0.10)
    brightness = st.slider("Brillo", -100, 100, 0, 1)
    adjusted_image = cv2.convertScaleAbs(image_rgb, alpha=contrast, beta=brightness)
    st.code(f"adjusted_image = cv2.convertScaleAbs(image, alpha={contrast:.2f}, beta={brightness})", language="python")
    col1, col2 = st.columns(2)
    with col1:
        st.image(image_rgb, caption="Imagen original", use_container_width=True)
    with col2:
        st.image(adjusted_image, caption="Imagen ajustada", use_container_width=True)

elif section == "Expansión del histograma":
    expanded_image = cv2.normalize(gray_image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    expanded_histogram = cv2.calcHist([expanded_image], [0], None, [256], [0, 256]).flatten()
    st.code("expanded_image = cv2.normalize(image, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)", language="python")
    col1, col2 = st.columns(2)
    with col1:
        st.image(gray_image, caption="Imagen original", use_container_width=True, clamp=True)
    with col2:
        st.image(expanded_image, caption="Imagen expandida", use_container_width=True, clamp=True)
    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(create_histogram_figure(opencv_histogram, "Histograma original"))
    with col4:
        st.pyplot(create_histogram_figure(expanded_histogram, "Histograma expandido"))

elif section == "Kernel y convolución":
    kernel_type = st.selectbox("Kernel", ["Promedio", "Enfoque", "Detección de bordes"])
    if kernel_type == "Promedio":
        kernel = np.ones((3, 3), dtype=np.float32) / 9
    elif kernel_type == "Enfoque":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
    else:
        kernel = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32)
    filtered_image = cv2.filter2D(gray_image, -1, kernel)
    st.code("filtered_image = cv2.filter2D(image, -1, kernel)", language="python")
    st.dataframe(kernel, use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image(gray_image, caption="Imagen original", use_container_width=True, clamp=True)
    with col2:
        st.image(filtered_image, caption="Resultado de la convolución", use_container_width=True, clamp=True)