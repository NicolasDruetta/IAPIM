# IAPIM Vision Lab – Detector facial

## Objetivo

La herramienta 01 permite capturar una fotografía y detectar los rostros
presentes mediante procesamiento de imágenes con OpenCV.

## Funcionamiento

La fotografía se captura desde la cámara del navegador. Al tomarla, la imagen
se convierte a escala de grises y se procesa con un clasificador Haar frontal.
Los rostros encontrados se marcan con rectángulos verdes y se informa la
cantidad total detectada.

La detección se ejecuta automáticamente al capturar o reemplazar una
fotografía. No es necesario presionar un botón adicional para iniciar el
análisis. Los controles nativos de la cámara permiten tomar, limpiar o
reemplazar la fotografía.

## Dependencias

- Python 3.15.
- Streamlit 1.66.0.
- OpenCV Headless 4.14.0.94.
- NumPy 2.5.4.

El clasificador `haarcascade_frontalface_default.xml` se utiliza desde los
archivos incluidos en la instalación de OpenCV. No se descargan modelos
externos.

## Limitaciones conocidas

- Haar Cascade puede no detectar rostros con poca iluminación, inclinación,
  oclusiones o encuadres poco frontales.
- La disponibilidad de la cámara depende de los permisos del navegador.
- Esta etapa no implementa detección de ojos ni reconocimiento de identidad,
  edad, género o emociones.
