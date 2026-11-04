import cv2
import numpy as np
import onnxruntime as ort
import streamlit as st

from pathlib import Path
from functions import configure_page

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "emotion-ferplus-12-int8.onnx"
EMOTION_NAMES = (
    "Neutral", "Alegría", "Sorpresa", "Tristeza",
    "Enojo", "Asco", "Miedo", "Desprecio",
)

def run_face(captured_bytes):
    """Procesa una captura, detecta rostros y obtiene su emoción dominante."""
    image_array = np.frombuffer(captured_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía capturada.")

    gray_image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    classifier_path = Path(cv2.data.haarcascades) / "haarcascade_frontalface_default.xml"
    face_classifier = cv2.CascadeClassifier(str(classifier_path))

    if face_classifier.empty():
        raise RuntimeError("No se pudo cargar el clasificador Haar frontal.")

    faces = face_classifier.detectMultiScale(
        gray_image,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
    )

    emotion_session = ort.InferenceSession(
        str(MODEL_PATH),
        providers=["CPUExecutionProvider"],
    )
    model_input = emotion_session.get_inputs()[0]

    processed_image = image_bgr.copy()
    emotions = []

    for face_number, (x_coordinate, y_coordinate, width, height) in enumerate(faces, start=1):
        face_gray = gray_image[y_coordinate:y_coordinate + height, x_coordinate:x_coordinate + width]
        face_input = cv2.resize(face_gray, (64, 64), interpolation=cv2.INTER_AREA)
        face_input = face_input.astype(np.float32).reshape(1, 1, 64, 64)
        scores = np.asarray(
            emotion_session.run(
                None,
                {emotion_session.get_inputs()[0].name: face_input},
            )[0]
        )

        if scores.shape != (1, 8) or not np.isfinite(scores).all():
            raise ValueError("FER+ devolvió puntuaciones inválidas.")

        scores = scores[0].astype(np.float64)
        probabilities = np.exp(scores - np.max(scores))
        percentages = probabilities / probabilities.sum() * 100
        dominant_index = int(np.argmax(percentages))
        emotions.append((EMOTION_NAMES[dominant_index], percentages[dominant_index]))

        cv2.putText(
            processed_image,
            f"Rostro {face_number}",
            (x_coordinate, max(15, y_coordinate - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 0),
            1,
        )
        cv2.rectangle(
            processed_image,
            (x_coordinate, y_coordinate),
            (x_coordinate + width, y_coordinate + height),
            (0, 255, 0),
            2,
        )

    return cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB), emotions

configure_page("IAPIM - Detector de emociones faciales con FER+")

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("01 – Detector de emociones faciales con FER+")

    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Capture una fotografía para detectar rostros y analizar sus expresiones faciales.")
st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Captura de imagen")
    st.write("Tome una fotografía con la cámara.")
    captured_image = st.camera_input("Fotografía", label_visibility="collapsed")
    captured_bytes = captured_image.getvalue() if captured_image is not None else None

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía con los rostros detectados.")

    if captured_bytes is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        try:
            processed_image, emotions = run_face(captured_bytes)

            st.image(processed_image, caption="Fotografía procesada", width="stretch")
            st.write(f"Rostros detectados: {len(emotions)}")

            if not emotions:
                st.warning("No se detectaron rostros en la fotografía.")

            for face_number, (dominant_emotion, dominant_percentage) in enumerate(emotions, start=1):
                st.write(
                    f"**Rostro {face_number}: {dominant_emotion} "
                    f"({dominant_percentage:.2f} %)**"
                )
        except Exception as error:
            st.error(f"No se pudo analizar la fotografía: {error}")

st.info(
    "**Modelo seleccionado:** FER+, un modelo preentrenado para reconocer ocho expresiones faciales. "
    "Se utiliza porque permite analizar emociones localmente, sin enviar la fotografía a servicios externos."
)
