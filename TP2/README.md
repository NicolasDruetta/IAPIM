# IAPIM Vision Lab – Herramientas de visión artificial

## Objetivo

El laboratorio reúne tres herramientas independientes de visión artificial.

## Herramienta 01 – Detector facial

Permite capturar una fotografía y detectar los rostros presentes mediante
procesamiento de imágenes con OpenCV.

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

## Herramienta 02 – Detector de objetos

Recibe una imagen desde la computadora mediante `st.file_uploader()`. La
interfaz muestra la fotografía original, permite ejecutar el análisis y muestra
una copia procesada con rectángulos sobre las regiones detectadas, además del
total de objetos encontrados.

El algoritmo utiliza escala de grises, desenfoque gaussiano, umbralización de
Otsu, operaciones morfológicas y contornos externos. Está pensado para objetos
visualmente separables del fondo y no identifica categorías semánticas como
"auto", "persona" o "botella". El resultado puede variar según iluminación,
contraste, tamaño y proximidad entre objetos.

## Herramienta 03 – Estacionamiento inteligente

La herramienta está preparada para trabajar con una galería local ubicada en
`images/03_estacionamiento_inteligente/`. No solicita cargas desde la
computadora: cuando existan imágenes adecuadas, permitirá seleccionar una
fotografía o elegir una de forma aleatoria, ejecutar el análisis y mostrar el
total de plazas, las plazas ocupadas, las libres y el porcentaje de ocupación.

El análisis requiere regiones de interés definidas específicamente para cada
escenario de la galería. Se utilizará procesamiento clásico sobre esas regiones
para clasificar cada plaza, sin YOLO, MediaPipe ni modelos externos.

Actualmente la galería no contiene fotografías, por lo que la página informa
qué material falta y no inventa resultados. Se necesitan fotografías de
estacionamientos con varias plazas visibles, tomadas desde un punto fijo, con
buena iluminación y suficiente resolución para distinguir cada plaza.
