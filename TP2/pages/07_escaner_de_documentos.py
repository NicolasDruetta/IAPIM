import cv2
import numpy as np
import streamlit as st

from pathlib import Path
from functions import configure_page

GALLERY_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "images"
    / "07_escaner_de_documentos"
)
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def apply_document_scan(image_bgr, display_mode):
    """Detecta un documento, corrige su perspectiva y aplica el modo elegido."""
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(blurred_image, 75, 200)
    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    document = None
    for contour in sorted(contours, key=cv2.contourArea, reverse=True):
        perimeter = cv2.arcLength(contour, True)
        approximation = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approximation) == 4 and cv2.contourArea(approximation) > 1000:
            document = approximation.reshape(4, 2).astype(np.float32)
            break
    if document is None:
        raise ValueError("No se detectó correctamente un documento rectangular.")
    ordered_points = order_points(document)
    top_left, top_right, bottom_right, bottom_left = ordered_points
    width = max(
        np.linalg.norm(bottom_right - bottom_left),
        np.linalg.norm(top_right - top_left),
    )
    height = max(
        np.linalg.norm(top_right - bottom_right),
        np.linalg.norm(top_left - bottom_left),
    )
    output_width = max(1, int(width))
    output_height = max(1, int(height))
    destination = np.array(
        [
            [0, 0],
            [output_width - 1, 0],
            [output_width - 1, output_height - 1],
            [0, output_height - 1],
        ],
        dtype=np.float32,
    )
    transform = cv2.getPerspectiveTransform(ordered_points, destination)
    scanned = cv2.warpPerspective(
        image_bgr,
        transform,
        (output_width, output_height),
    )
    if display_mode == "Blanco y negro":
        scanned_gray = cv2.cvtColor(scanned, cv2.COLOR_BGR2GRAY)
        scanned = cv2.adaptiveThreshold(
            scanned_gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )
    return scanned

def decode_image(image_bytes):
    """Decodifica una fotografía JPG o PNG."""
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía seleccionada.")
    return image_bgr

def get_gallery_images():
    """Obtiene las fotografías precargadas disponibles."""
    return sorted(
        image_path
        for image_path in GALLERY_DIRECTORY.glob("*")
        if image_path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

def initialize_state():
    """Inicializa el estado de la página."""
    if "visionlab_document_scanner" not in st.session_state:
        st.session_state.visionlab_document_scanner = {
            "selected_bytes": None,
            "selected_name": None,
            "last_upload": None,
            "error": None,
        }
    return st.session_state.visionlab_document_scanner

def order_points(points):
    """Ordena las esquinas como superior izquierda, superior derecha, inferior derecha e inferior izquierda."""
    ordered = np.zeros((4, 2), dtype=np.float32)
    sums = points.sum(axis=1)
    differences = np.diff(points, axis=1).ravel()
    ordered[0] = points[np.argmin(sums)]
    ordered[2] = points[np.argmax(sums)]
    ordered[1] = points[np.argmin(differences)]
    ordered[3] = points[np.argmax(differences)]
    return ordered

def prepare_gallery_images(image_paths):
    """Prepara miniaturas para la galería."""
    prepared_images = []
    for image_path in image_paths:
        image = cv2.imread(str(image_path))
        if image is not None:
            prepared_images.append((image_path, cv2.cvtColor(image, cv2.COLOR_BGR2RGB)))
    return prepared_images

configure_page("IAPIM - Escáner inteligente de documentos")
page_state = initialize_state()

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("07 – Escáner inteligente de documentos")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Enderece un documento fotografiado y genere una versión similar a un escaneo.")
st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Selección de imagen")
    st.write("Cargue una fotografía del documento.")
    uploaded_image = st.file_uploader(
        "Cargue una fotografía",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )
    uploaded_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    if uploaded_bytes != page_state["last_upload"]:
        page_state["last_upload"] = uploaded_bytes
        if uploaded_image is not None:
            page_state["selected_bytes"] = uploaded_bytes
            page_state["selected_name"] = uploaded_image.name
            page_state["error"] = None
    gallery_images = prepare_gallery_images(get_gallery_images())
    if not gallery_images:
        st.info("La galería todavía no contiene fotografías.")
    else:
        st.write("Imágenes precargadas")
        for row_start in range(0, len(gallery_images), 4):
            gallery_columns = st.columns(4, gap="small")
            for gallery_column, (image_path, prepared_image) in zip(
                gallery_columns,
                gallery_images[row_start:row_start + 4],
            ):
                with gallery_column:
                    with st.container(border=True):
                        st.image(prepared_image, width="stretch")
                        if st.button("Usar", key=f"scanner_{image_path.name}", width="stretch"):
                            page_state["selected_bytes"] = image_path.read_bytes()
                            page_state["selected_name"] = image_path.name
                            page_state["error"] = None
    if page_state["selected_name"] is not None:
        st.write(f"Imagen seleccionada: {page_state['selected_name']}")

with right_column:
    st.subheader("Resultados del análisis")
    if page_state["selected_bytes"] is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        display_mode = st.radio(
            "Modo de visualización",
            ["Color", "Blanco y negro"],
            horizontal=True,
        )
        try:
            image_bgr = decode_image(page_state["selected_bytes"])
            scanned_image = apply_document_scan(image_bgr, display_mode)
            if scanned_image.ndim == 2:
                st.image(scanned_image, caption="Documento corregido", width="stretch")
            else:
                st.image(
                    cv2.cvtColor(scanned_image, cv2.COLOR_BGR2RGB),
                    caption="Documento corregido",
                    width="stretch",
                )
            success, encoded_result = cv2.imencode(".png", scanned_image)
            if not success:
                raise ValueError("No se pudo preparar la descarga PNG.")
            st.download_button(
                "Descargar documento PNG",
                data=encoded_result.tobytes(),
                file_name="documento_escaneado.png",
                mime="image/png",
                width="stretch",
            )
        except (OSError, ValueError, cv2.error) as error:
            st.error(str(error))
