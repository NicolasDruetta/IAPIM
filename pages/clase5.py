import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("Clase 5")
uploaded_file = st.file_uploader("Subí una imagen", type=["jpg", "jpeg", "png"])
if uploaded_file is None:
    st.stop()

# Convierte la imagen a los formatos necesarios para trabajar con OpenCV y Streamlit.
image_pil = Image.open(uploaded_file).convert("RGB")
image_rgb = np.array(image_pil)
image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
rows, cols = image_bgr.shape[:2]

# Menú interno de la Clase 5.
st.sidebar.markdown("## **Clase 5**")
section = st.sidebar.radio("Contenido", ["Imagen original", "Traslación", "Rotación", "Escalado", "Blur promedio", "Gaussian Blur", "Sobel", "Canny"])

if section == "Imagen original":
    st.code('image = cv2.imread("imagen.jpg")', language="python")
    st.image(image_rgb, caption="Imagen original", use_container_width=True)

elif section == "Traslación":
    tx = st.slider("Desplazamiento horizontal", -cols, cols, min(100, cols))
    ty = st.slider("Desplazamiento vertical", -rows, rows, min(50, rows))
    matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    translated_image = cv2.warpAffine(image_bgr, matrix, (cols, rows))
    st.code(f"M = np.float32([[1, 0, {tx}], [0, 1, {ty}]])\ntranslated_image = cv2.warpAffine(image, M, (cols, rows))", language="python")
    st.image(cv2.cvtColor(translated_image, cv2.COLOR_BGR2RGB), caption="Imagen trasladada", use_container_width=True)

elif section == "Rotación":
    angle = st.slider("Ángulo", -180, 180, 45)
    scale = st.slider("Escala", 0.10, 2.00, 1.00, 0.10)
    center = (cols // 2, rows // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, scale)
    rotated_image = cv2.warpAffine(image_bgr, matrix, (cols, rows))
    st.code(f"M = cv2.getRotationMatrix2D(center, {angle}, {scale:.2f})\nrotated_image = cv2.warpAffine(image, M, (cols, rows))", language="python")
    st.image(cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB), caption="Imagen rotada", use_container_width=True)

elif section == "Escalado":
    scale_factor = st.slider("Factor de escala", 0.10, 2.00, 0.50, 0.10)
    scaled_image = cv2.resize(image_bgr, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    st.code(f"scaled_image = cv2.resize(image, None, fx={scale_factor:.2f}, fy={scale_factor:.2f}, interpolation=cv2.INTER_LINEAR)", language="python")
    st.image(cv2.cvtColor(scaled_image, cv2.COLOR_BGR2RGB), caption="Imagen escalada", use_container_width=True)

elif section == "Blur promedio":
    kernel_size = st.slider("Tamaño del kernel", 1, 31, 5, 2)
    blurred_image = cv2.blur(image_bgr, (kernel_size, kernel_size))
    st.code(f"blurred_image = cv2.blur(image, ({kernel_size}, {kernel_size}))", language="python")
    st.image(cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB), caption="Blur promedio", use_container_width=True)

elif section == "Gaussian Blur":
    kernel_size = st.slider("Tamaño del kernel", 1, 31, 5, 2)
    gaussian_image = cv2.GaussianBlur(image_bgr, (kernel_size, kernel_size), 0)
    st.code(f"gaussian_image = cv2.GaussianBlur(image, ({kernel_size}, {kernel_size}), 0)", language="python")
    st.image(cv2.cvtColor(gaussian_image, cv2.COLOR_BGR2RGB), caption="Gaussian Blur", use_container_width=True)

elif section == "Sobel":
    direction = st.radio("Dirección", ["Horizontal", "Vertical", "Ambos"], horizontal=True)
    kernel_size = st.slider("Tamaño del kernel Sobel", 1, 7, 3, 2)
    if direction == "Horizontal":
        sobel_image = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=kernel_size)
        code = f"sobel_image = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize={kernel_size})"
    elif direction == "Vertical":
        sobel_image = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=kernel_size)
        code = f"sobel_image = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize={kernel_size})"
    else:
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=kernel_size)
        sobel_image = cv2.magnitude(sobel_x, sobel_y)
        code = f"sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize={kernel_size})\nsobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize={kernel_size})\nsobel_image = cv2.magnitude(sobel_x, sobel_y)"
    st.code(code, language="python")
    st.image(sobel_image, caption="Filtro Sobel", use_container_width=True, clamp=True)

elif section == "Canny":
    lower_threshold = st.slider("Umbral inferior", 0, 255, 100)
    upper_threshold = st.slider("Umbral superior", 0, 255, 200)
    canny_image = cv2.Canny(gray_image, lower_threshold, upper_threshold)
    st.code(f"canny_image = cv2.Canny(image, {lower_threshold}, {upper_threshold})", language="python")
    st.image(canny_image, caption="Filtro Canny", use_container_width=True, clamp=True)