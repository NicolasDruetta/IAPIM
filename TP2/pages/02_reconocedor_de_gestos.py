import cv2
import mediapipe as mp
import numpy as np
import streamlit as st

from pathlib import Path
from functions import configure_page
from mediapipe.tasks.python.vision import HandLandmarksConnections

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "gesture_recognizer.task"
GESTURE_LABELS = {
    "Closed_Fist": "Puño cerrado",
    "ILoveYou": "Te quiero",
    "Open_Palm": "Mano abierta",
    "Pointing_Up": "Señalar hacia arriba",
    "Thumb_Down": "Pulgar abajo",
    "Thumb_Up": "Pulgar arriba",
    "Victory": "Victoria",
}

def run_hand(captured_bytes):
    """Procesa una captura, detecta manos y muestra sus gestos."""
    image_array = np.frombuffer(captured_bytes, dtype=np.uint8)
    image_bgr = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image_bgr is None:
        raise ValueError("No se pudo leer la fotografía seleccionada.")

    base_options = mp.tasks.BaseOptions(model_asset_path=str(MODEL_PATH))
    options = mp.tasks.vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        num_hands=4,
    )
    recognizer = mp.tasks.vision.GestureRecognizer.create_from_options(options)

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
    recognition_result = recognizer.recognize(mp_image)

    annotated_image = image_bgr.copy()
    image_height, image_width = annotated_image.shape[:2]
    for hand_landmarks in recognition_result.hand_landmarks:
        points = []

        for landmark in hand_landmarks:
            point = (
                min(image_width - 1, max(0, round(landmark.x * image_width))),
                min(image_height - 1, max(0, round(landmark.y * image_height))),
            )
            points.append(point)
            cv2.circle(annotated_image, point, 4, (0, 180, 255), -1)

        for connection in HandLandmarksConnections.HAND_CONNECTIONS:
            cv2.line(
                annotated_image,
                points[connection.start],
                points[connection.end],
                (0, 220, 0),
                2,
            )

    return annotated_image, recognition_result

configure_page("IAPIM - Reconocedor de gestos de manos con MediaPipe")

with st.container(horizontal=True, vertical_alignment="center", gap="small", width="content"):
    st.title("02 – Reconocedor de gestos de manos con MediaPipe")

    if st.button("Volver al Inicio", width="content"):
        st.switch_page("main.py")

st.write("Detecte manos e identifique gestos de las manos.")
st.divider()

left_column, right_column = st.columns([1, 1], gap="large")

with left_column:
    st.subheader("Captura de imagen")
    st.write("Tome una fotografía con la cámara.")
    captured_image = st.camera_input("Fotografía", label_visibility="collapsed")
    captured_bytes = captured_image.getvalue() if captured_image is not None else None

with right_column:
    st.subheader("Resultados del análisis")
    st.write("Visualice la fotografía con las manos y gestos detectados.")

    if captured_bytes is None:
        with st.container(height=400, border=True):
            st.write("")
    else:
        try:
            annotated_image, recognition_result = run_hand(captured_bytes)

            st.image(
                cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB),
                caption="Fotografía procesada",
                width="stretch",
            )

            hand_count = len(recognition_result.hand_landmarks)
            st.write(f"Manos detectadas: {hand_count}")

            if hand_count == 0:
                st.info("No se detectaron manos en la fotografía.")

            for index in range(hand_count):
                gestures = (
                    recognition_result.gestures[index]
                    if index < len(recognition_result.gestures)
                    else []
                )

                if not gestures or gestures[0].score < 0.5:
                    st.write(
                        f"Mano {index + 1}: no se reconoció un gesto con suficiente confianza."
                    )
                    continue

                gesture = gestures[0]
                label = GESTURE_LABELS.get(
                    gesture.category_name,
                    gesture.category_name,
                )
                st.write(
                    f"**Mano {index + 1}: {label} "
                    f"({gesture.score * 100:.2f} %)**"
                )
        except (OSError, ValueError, cv2.error) as error:
            st.error(str(error))

st.info(
    "**Modelo seleccionado:** MediaPipe Gesture Recognizer, un modelo preentrenado para detectar landmarks "
    "de las manos y clasificar gestos localmente con baja latencia."
)
