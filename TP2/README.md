# IAPIM Vision Lab

## Presentación

IAPIM Vision Lab es un laboratorio académico de visión artificial y procesamiento de imágenes desarrollado para la materia Inteligencia Artificial y Procesamiento de Imágenes.

- Autor: Nicolás Druetta.
- Año: 2026.
- Trabajo práctico: Parcial 1.

## Descripción general

La aplicación reúne herramientas independientes para explorar problemas básicos de visión artificial mediante procesamiento clásico de imágenes. El laboratorio aborda la detección de rostros, la segmentación de objetos visualmente separables y la preparación de un análisis de ocupación de plazas de estacionamiento.

Estas técnicas tienen aplicaciones prácticas en sistemas de asistencia, inspección visual, automatización de tareas, análisis de escenas y apoyo a la toma de decisiones. Los resultados dependen de la calidad de las imágenes y de las condiciones específicas de cada escenario.

## Tecnologías utilizadas

- Python 3.15.
- Streamlit 1.66.0 para la interfaz multipágina.
- OpenCV Headless 4.14.0.94 para lectura, transformación y procesamiento de imágenes.
- NumPy 2.5.4 para representar imágenes y realizar operaciones matriciales.
- `pathlib`, incluida en la biblioteca estándar de Python, para resolver rutas de recursos.

El archivo `requirements.txt` también conserva dependencias disponibles para el entorno académico general: Matplotlib, pandas, Pillow y scikit-image. La implementación actual de TP2 utiliza directamente Streamlit, OpenCV, NumPy y `pathlib`.

## Arquitectura

El proyecto utiliza la arquitectura multipágina tradicional de Streamlit. `main.py` funciona como punto de entrada y Home, mientras que cada archivo de `pages/` define una herramienta independiente con su interfaz y su procesamiento específico. `functions.py` centraliza la configuración común de las páginas, incluida la identidad de la aplicación, el ícono, el diseño ancho y la carga del estilo global del proyecto.

La interfaz se construye con componentes nativos de Streamlit. El archivo `assets/custom.css` contiene únicamente ajustes globales de espaciado y adaptación de columnas. Las imágenes precargadas se organizan por herramienta dentro de `assets/images/` y se descubren mediante rutas relativas al proyecto.

### Estructura real

```text
TP2/
├── assets/
│   ├── custom.css
│   ├── icon.png
│   └── images/
│       ├── 02_detector_de_objetos/
│       └── 03_estacionamiento_inteligente/
├── functions.py
├── main.py
├── pages/
│   ├── 01_detector_facial.py
│   ├── 02_detector_de_objetos.py
│   └── 03_estacionamiento_inteligente.py
└── README.md
```

## Herramientas del laboratorio

### 01 – Detector facial

**Objetivo:** detectar rostros en una fotografía capturada con la cámara del navegador.

**Entrada:** una fotografía tomada mediante `st.camera_input()`.

**Funcionamiento:** la imagen se decodifica con OpenCV, se convierte a escala de grises y se procesa mediante el clasificador Haar frontal `haarcascade_frontalface_default.xml`, incluido en la instalación de OpenCV.

**Algoritmos:** conversión a escala de grises y detección de objetos mediante Haar Cascade.

**Resultados:** la aplicación dibuja rectángulos verdes sobre los rostros detectados e informa la cantidad total.

**Limitaciones:** el método puede verse afectado por poca iluminación, inclinación, oclusiones, rostros pequeños y encuadres poco frontales. No realiza reconocimiento de identidad ni estima edad, género o emociones.

### 02 – Detector de objetos

**Objetivo:** localizar objetos visualmente separables en una imagen, sin asignarles categorías semánticas.

**Entrada:** una imagen cargada desde la computadora mediante `st.file_uploader()` o una imagen precargada de `assets/images/02_detector_de_objetos/`.

**Funcionamiento:** la imagen se convierte a escala de grises, se suaviza con un desenfoque gaussiano, se binariza mediante el método de Otsu y se limpia con operaciones morfológicas. Luego se obtienen los contornos externos y se descartan las regiones con un área inferior al umbral definido por el tamaño de la imagen.

**Algoritmos:** escala de grises, desenfoque gaussiano, umbralización de Otsu, apertura y cierre morfológicos, detección de contornos y rectángulos delimitadores.

**Resultados:** la aplicación muestra la imagen procesada con rectángulos verdes y el total de regiones detectadas.

**Limitaciones:** el método está orientado a objetos separables del fondo. Puede agrupar objetos cercanos, dividir un mismo objeto o detectar regiones irrelevantes cuando cambian la iluminación, el contraste, el fondo o la escala.

### 03 – Estacionamiento inteligente

**Objetivo:** preparar el análisis clásico de plazas libres y ocupadas en escenarios de estacionamiento.

**Entrada:** imágenes precargadas en `assets/images/03_estacionamiento_inteligente/`. La página no solicita fotografías desde la computadora.

**Estado actual:** la galería local contiene seis imágenes y la interfaz permite visualizarlas y seleccionarlas mediante el botón «Usar». Todavía no están implementadas las regiones de interés, la clasificación de cada plaza ni el cálculo de plazas totales, ocupadas, libres y porcentaje de ocupación.

**Funcionamiento previsto:** cada escenario requerirá regiones de interés definidas de acuerdo con la distribución de sus plazas. Sobre esas regiones se aplicarán técnicas clásicas de procesamiento para estimar la ocupación.

**Limitaciones actuales:** no se presentan resultados de ocupación hasta definir y validar las regiones de interés de cada imagen. No se utilizan YOLO, MediaPipe ni modelos externos.

## Instalación y ejecución

### Requisitos previos

- Python 3.15.
- Un navegador con permisos para utilizar la cámara en la herramienta 01.
- Un entorno virtual de Python.

### Instalación

Desde la raíz del proyecto, cree o active el entorno virtual e instale las dependencias:

```bash
python3.15 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

En Windows, la activación equivalente es:

```powershell
.venv\Scripts\Activate.ps1
```

### Ejecución

```bash
cd TP2
streamlit run main.py
```

Streamlit indicará la dirección local de la aplicación, normalmente `http://localhost:8501`. El puerto puede variar si ya existe otra instancia en ejecución.

## Consideraciones técnicas

Las imágenes deben presentar suficiente resolución, contraste y calidad para el algoritmo correspondiente. La iluminación uniforme, la reducción de oclusiones y la separación visual entre objetos favorecen resultados más estables.

Los métodos clásicos utilizados no poseen comprensión semántica general. Sus resultados dependen de umbrales, geometría, textura, contraste y configuración de la escena. Por este motivo, las salidas deben interpretarse como estimaciones basadas en procesamiento de imágenes y no como clasificación universal de objetos.

## Estado actual del proyecto

Se encuentran implementados el Home, la navegación entre las tres herramientas, el detector facial y el detector de objetos. La galería de estacionamiento se encuentra integrada y permite seleccionar imágenes locales. El análisis de plazas mediante regiones de interés y sus métricas permanece pendiente de implementación y validación.
