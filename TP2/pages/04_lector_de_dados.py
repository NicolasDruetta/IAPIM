import cv2
import numpy as np
import streamlit as st

from pathlib import Path
from functions import configure_page

GALLERY_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "images" / "04_lector_de_dados"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

def annotate_dice(image_bgr, dice_results):
    """Dibuja los dados, los puntos y sus valores sobre la fotografía."""
    annotated_image = image_bgr.copy()
    for position, (x, y, width, height, count, centers) in enumerate(dice_results, 1):
        cv2.rectangle(
            annotated_image,
            (x, y),
            (x + width, y + height),
            (0, 200, 0),
            3,
        )
        for center_x, center_y in centers:
            cv2.circle(
                annotated_image,
                (x + center_x, y + center_y),
                7,
                (0, 0, 255),
                2,
            )
        cv2.putText(
            annotated_image,
            f"Dado {position}: {count}",
            (x, max(y - 10, 24)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 120, 0),
            2,
            cv2.LINE_AA,
        )

    return cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

def count_pips(die_image):
    """Cuenta componentes circulares que pueden corresponder a puntos."""
    die_height, die_width = die_image.shape[:2]
    margin_x = max(2, round(die_width * 0.1))
    margin_y = max(2, round(die_height * 0.1))
    interior = die_image[margin_y:die_height - margin_y, margin_x:die_width - margin_x]
    gray_image = cv2.cvtColor(interior, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    _, threshold = cv2.threshold(
        blurred_image,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )
    kernel = np.ones((3, 3), dtype=np.uint8)
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    interior_area = interior.shape[0] * interior.shape[1]
    minimum_area = max(4, interior_area * 0.002)
    maximum_area = interior_area * 0.12
    centers = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if not minimum_area <= area <= maximum_area:
            continue
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * area / perimeter ** 2
        if circularity < 0.45:
            continue
        x, y, width, height = cv2.boundingRect(contour)
        if width > interior.shape[1] * 0.55 or height > interior.shape[0] * 0.55:
            continue
        moment = cv2.moments(contour)
        if moment["m00"] == 0:
            continue
        center = (
            round(moment["m10"] / moment["m00"]) + margin_x,
            round(moment["m01"] / moment["m00"]) + margin_y,
        )
        if all(np.linalg.norm(np.subtract(center, previous)) > 8 for previous in centers):
            centers.append(center)

    return len(centers), sorted(centers, key=lambda point: (point[1], point[0]))

def detect_dice_regions(image_bgr):
    """Detecta regiones cuadradas o cuadriláteras que pueden ser dados."""
    image_height, image_width = image_bgr.shape[:2]
    image_area = image_height * image_width
    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    edges = cv2.Canny(blurred_image, 50, 150)
    kernel = np.ones((7, 7), dtype=np.uint8)
    closed_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(
        closed_edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    minimum_area = max(900, image_area * 0.005)
    candidates = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < minimum_area:
            continue
        perimeter = cv2.arcLength(contour, True)
        approximation = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        x, y, width, height = cv2.boundingRect(contour)
        ratio = width / height if height else 0
        if not 0.55 <= ratio <= 1.8:
            continue
        if len(approximation) < 4 and not cv2.isContourConvex(approximation):
            continue
        candidates.append((x, y, width, height))

    regions = []
    for candidate in sorted(candidates, key=lambda region: region[2] * region[3], reverse=True):
        x, y, width, height = candidate
        candidate_area = width * height
        overlaps = False
        for previous_x, previous_y, previous_width, previous_height in regions:
            intersection_width = max(
                0,
                min(x + width, previous_x + previous_width) - max(x, previous_x),
            )
            intersection_height = max(
                0,
                min(y + height, previous_y + previous_height) - max(y, previous_y),
            )
            intersection_area = intersection_width * intersection_height
            if intersection_area / candidate_area > 0.4:
                overlaps = True
                break
        if not overlaps:
            regions.append(candidate)

    return sorted(regions, key=lambda region: (region[1], region[0]))

def get_gallery_images():
    """Obtiene las fotografías disponibles para la galería."""
    return sorted(
        image_path
        for image_path in GALLERY_DIRECTORY.glob("*")
        if image_path.suffix.lower() in SUPPORTED_EXTENSIONS
    )

def initialize_state():
    """Inicializa el estado de la página sin sobrescribir una selección vigente."""
    if "visionlab_dice" not in st.session_state:
        st.session_state.visionlab_dice = {
            "selected_bytes": None,
            "selected_name": None,
            "last_upload": None,
            "result": None,
            "error": None,
        }

    return st.session_state.visionlab_dice

def prepare_gallery_images(image_paths):
    """Ajusta las miniaturas a un lienzo común según la imagen más alta."""
    decoded_images = []
    for image_path in image_paths:
        image = cv2.imread(str(image_path))
        if image is not None:
            decoded_images.append((image_path, image))
    if not decoded_images:
        return []
    target_width = max(image.shape[1] for _, image in decoded_images)
    target_height = max(image.shape[0] for _, image in decoded_images)
    prepared_images = []
    for image_path, image in decoded_images:
        image_height, image_width = image.shape[:2]
        scale = min(target_width / image_width, target_height / image_height)
        resized_size = (round(image_width * scale), round(image_height * scale))
        resized_image = cv2.resize(image, resized_size, interpolation=cv2.INTER_AREA)
        canvas = np.full(
            (target_height, target_width, 3),
            255,
            dtype=np.uint8,
        )
        offset_x = (target_width - resized_size[0]) // 2
        offset_y = (target_height - resized_size[1]) // 2
        canvas[
            offset_y:offset_y + resized_size[1],
            offset_x:offset_x + resized_size[0],
        ] = resized_image
        prepared_images.append(
            (image_path, cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        )
    return prepared_images

def process_dice_image(image_bytes):
    """Detecta dados, cuenta puntos y devuelve la fotografía anotada."""
    image_bgr = read_image(image_bytes)
    dice_results = []
    for x, y, width, height in detect_dice_regions(image_bgr):
        die_image = image_bgr[y:y + height, x:x + width]
        count, centers = count_pips(die_image)
        dice_results.append((x, y, width, height, count, centers))
    annotated_image = annotate_dice(image_bgr, dice_results)
    dice_counts = [result[4] for result in dice_results]
    return annotated_image, dice_counts, sum(dice_counts)

def read_image(image_bytes):
    """Decodifica una fotografía recibida como bytes."""
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía seleccionada.")
    return image_bgr

configure_page("IAPIM - Lector inteligente de dados")
page_state = initialize_state()

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("04 – Lector inteligente de dados")
    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Detecte dados, cuente sus puntos y calcule el resultado total.")

st.divider()

left_column, right_column = st.columns([1, 1], gap="large")
analysis_requested = False

with left_column:
    st.subheader("Selección de imagen")
    st.write("Cargue una fotografía para detectar dados y contar sus puntos")
    gallery_images = get_gallery_images()
    card_images = prepare_gallery_images(gallery_images)
    uploaded_image = st.file_uploader(
        "Cargue una fotografía",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )
    uploaded_bytes = uploaded_image.getvalue() if uploaded_image is not None else None
    if uploaded_bytes != page_state["last_upload"]:
        page_state["last_upload"] = uploaded_bytes
        if uploaded_bytes is not None:
            page_state["selected_bytes"] = uploaded_bytes
            page_state["selected_name"] = uploaded_image.name
            page_state["result"] = None
            page_state["error"] = None
            analysis_requested = True
    if not gallery_images:
        st.warning("La galería todavía no contiene fotografías de dados.")
    else:
        st.write("Imágenes precargadas")
        with st.container(key="dice-gallery"):
            for row_start in range(0, len(card_images), 4):
                gallery_row = card_images[row_start:row_start + 4]
                gallery_columns = st.columns(4, gap="small")
                for gallery_column, (image_path, prepared_image) in zip(
                    gallery_columns,
                    gallery_row,
                ):
                    with gallery_column:
                        with st.container(border=True):
                            st.image(prepared_image, width="stretch")
                            if st.button(
                                "Usar",
                                key=f"dice_{image_path.name}",
                                width="stretch",
                            ):
                                page_state["selected_bytes"] = image_path.read_bytes()
                                page_state["selected_name"] = image_path.name
                                page_state["result"] = None
                                page_state["error"] = None
                                analysis_requested = True
    info_placeholder = st.empty()
    if page_state["selected_name"] is not None:
        info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}")
    if analysis_requested:
        info_placeholder.write(
            f"Imagen seleccionada: {page_state['selected_name']}. Analizando..."
        )
        try:
            page_state["result"] = process_dice_image(page_state["selected_bytes"])
        except (OSError, ValueError, cv2.error) as error:
            page_state["error"] = str(error)
        info_placeholder.write(f"Imagen seleccionada: {page_state['selected_name']}")

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía con los dados y puntos detectados")
    if page_state["error"]:
        st.error(page_state["error"])
    elif page_state["result"] is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        processed_image, dice_counts, total = page_state["result"]
        st.image(processed_image, caption="Dados y puntos detectados", width="stretch")
        if dice_counts:
            dice_summary = " · ".join(
                f"Dado {position}: {count}"
                for position, count in enumerate(dice_counts, 1)
            )
            st.write(
                f"**Dados detectados:** {len(dice_counts)} · {dice_summary} · **Total:** {total}"
            )
        else:
            st.write("No se detectaron dados en la fotografía.")
