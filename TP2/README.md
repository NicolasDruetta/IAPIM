# IAPIM Vision Lab

## Presentación

IAPIM Vision Lab es un laboratorio académico de visión artificial y procesamiento de imágenes desarrollado para la materia Inteligencia Artificial y Procesamiento de Imágenes.

- Autor: Nicolás Druetta.
- Año: 2026.
- Trabajo práctico: Parcial 2.

## Descripción general

La aplicación reúne siete herramientas independientes para explorar problemas de visión artificial y procesamiento de imágenes: detección de emociones faciales, reconocimiento de gestos, detección de objetos, extracción de fondos, segmentación semántica de escenas, mejora de imágenes y clasificación de imágenes.

Estas técnicas tienen aplicaciones prácticas en sistemas de asistencia, inspección visual, automatización de tareas, análisis de escenas y apoyo a la toma de decisiones. Los resultados dependen de la calidad de las imágenes y de las condiciones específicas de cada escenario.

## Tecnologías utilizadas

- Python 3.14.
- Streamlit 1.66.0 para la interfaz multipágina.
- OpenCV 4.14.0.94 para lectura y transformación de imágenes.
- NumPy 2.5.4 para representar imágenes y realizar operaciones matriciales.
- PyTorch 2.15.0 como motor de inferencia de aprendizaje profundo.
- Torchvision 0.29.2 como dependencia de visión de PyTorch.
- Transformers 5.22.0 para cargar el procesador y el modelo SegFormer.
- Ultralytics 8.4.193 para ejecutar modelos YOLO.
- `pathlib`, incluida en la biblioteca estándar de Python, para resolver rutas de recursos.

El archivo `requirements.txt` también conserva dependencias disponibles para el entorno académico general: Matplotlib, pandas y scikit-image. La implementación actual de TP2 utiliza directamente Streamlit, OpenCV, NumPy, Pillow, PyTorch, Torchvision, Transformers, Ultralytics, MediaPipe, ONNX Runtime y `pathlib`.

## Arquitectura

El proyecto utiliza la arquitectura multipágina tradicional de Streamlit. `main.py` funciona como punto de entrada y Home, mientras que cada archivo de `pages/` define una herramienta independiente con su interfaz y su procesamiento específico. `functions.py` centraliza la configuración común de las páginas, incluida la identidad de la aplicación, el ícono, el diseño ancho y la carga del estilo global del proyecto.

La interfaz se construye con componentes nativos de Streamlit. El archivo `assets/custom.css` contiene ajustes globales de espaciado, adaptación de columnas, alineación del pie de página y ajuste de texto de los enlaces. Las imágenes predefinidas se organizan por herramienta dentro de `assets/images/` y se descubren mediante rutas relativas al proyecto.

### Estructura real

```text
TP2/
├── assets/
│   ├── custom.css
│   ├── icon.png
│   └── images/
│       ├── 00_main/
│       ├── 03_detector_de_objetos/
│       ├── 04_extractor_de_fondos/
│       ├── 05_analizador_de_escenas/
│       ├── 06_mejorador_de_imagenes/
│       └── 07_clasificador_de_imagenes/
├── functions.py
├── main.py
├── models/
│   ├── emotion-ferplus-12-int8.onnx
│   ├── gesture_recognizer.task
│   ├── mobilenet_v2-7ebf99e0.pth
│   ├── rmbg-1.4-quantized.onnx
│   ├── segformer-b0-finetuned-ade-512-512/
│   └── yolo11n.pt
├── pages/
│   ├── 01_detector_facial.py
│   ├── 02_reconocedor_de_gestos.py
│   ├── 03_detector_de_objetos.py
│   ├── 04_extractor_de_fondos.py
│   ├── 05_analizador_de_escenas.py
│   ├── 06_mejorador_de_imagenes.py
│   └── 07_clasificador_de_imagenes.py
├── explicacion.txt
└── README.md
```

## Herramientas del laboratorio

### 01 – Detector de emociones faciales

**Objetivo:** detectar rostros y reconocer sus emociones en una fotografía capturada con la cámara del navegador.

**Entrada:** una fotografía tomada mediante `st.camera_input()`.

**Funcionamiento:** la imagen se decodifica con OpenCV, se convierte a escala de grises y se procesa mediante el clasificador Haar frontal `haarcascade_frontalface_default.xml`, incluido en la instalación de OpenCV.

**Algoritmos:** conversión a escala de grises y detección de objetos mediante Haar Cascade.

**Resultados:** la aplicación dibuja rectángulos verdes sobre los rostros detectados e informa la cantidad total.

**Limitaciones:** el método puede verse afectado por poca iluminación, inclinación, oclusiones, rostros pequeños y encuadres poco frontales. No realiza reconocimiento de identidad ni estima edad o género.

### 03 – Detector de objetos

**Objetivo:** detectar objetos reconocidos por un modelo general preentrenado y mostrar sus categorías con sus niveles de confianza.

**Entrada:** una imagen cargada desde la computadora mediante `st.file_uploader()` o una imagen precargada de `assets/images/03_detector_de_objetos/`.

**Funcionamiento:** la imagen se entrega a YOLO11n, un modelo de detección general preentrenado sobre el conjunto de datos COCO. El modelo devuelve las cajas delimitadoras, las categorías y las confianzas de cada detección. La inferencia utiliza CUDA cuando está disponible, Apple Metal Performance Shaders (MPS) como alternativa y CPU en los demás equipos.

**Algoritmos:** inferencia de detección de objetos mediante YOLO11n y representación de cajas delimitadoras mediante Ultralytics.

**Resultados:** la aplicación muestra la imagen procesada con rectángulos, categoría y confianza de cada detección. También informa la cantidad total y el recuento agrupado por categoría.

**Modelo y procedencia:** se utiliza `models/yolo11n.pt`, distribuido por Ultralytics como modelo preentrenado para detección general. El paquete Ultralytics se distribuye bajo licencia AGPL-3.0 y el modelo se basa en las categorías de COCO.

**Limitaciones:** las detecciones dependen de las categorías de COCO, el umbral de confianza, la resolución y las condiciones de cada fotografía. YOLO puede no detectar algunos objetos o asignar categorías incorrectas cuando la escena no coincide con sus datos de entrenamiento.

### 05 – Analizador de escenas

**Objetivo:** segmentar semánticamente una fotografía y asignar una categoría a cada píxel según las clases reconocidas por ADE20K, como cielo, edificios, calles, árboles, vegetación, suelo, paredes y muebles.

**Entrada:** una fotografía cargada desde la computadora mediante `st.file_uploader()` o una fotografía real precargada en `assets/images/05_analizador_de_escenas/`. La página permite elegir una fotografía de la galería cuando esta contiene imágenes.

**Segmentación semántica:** cada píxel recibe una clase del modelo. El resultado no representa objetos individuales ni utiliza cajas delimitadoras; una misma categoría puede aparecer en varias regiones de la imagen.

**Modelo:** se utiliza el modelo local `models/segformer-b0-finetuned-ade-512-512`, un modelo SegFormer preentrenado sobre ADE20K. `AutoImageProcessor` prepara la imagen y ajusta el mapa de clases a la resolución original mediante el postprocesamiento de Transformers.

**Resultados:** la página muestra la fotografía original, una superposición coloreada, una leyenda con los nombres reales de las categorías, el porcentaje de píxeles de cada categoría y la cantidad de categorías presentes. La opacidad se modifica con un slider y la aplicación vuelve a procesar la imagen con el nuevo valor.

**Procesamiento:** el modelo se carga desde `models/segformer-b0-finetuned-ade-512-512`. La inferencia selecciona CUDA cuando está disponible, MPS en Apple Silicon como alternativa y CPU en los demás equipos. Los archivos del procesador, la configuración y los pesos se incluyen localmente en el proyecto.

**Estado de la galería:** el repositorio incluye fotografías precargadas en `assets/images/05_analizador_de_escenas/`. La interfaz también permite utilizar la carga manual.

**Limitaciones:** la calidad depende de las clases y del entrenamiento de ADE20K, la resolución, la iluminación y la composición de la fotografía. La inferencia en CPU puede ser lenta y las categorías no deben interpretarse como detecciones de instancias ni como una descripción exhaustiva de la escena.

## Instalación y ejecución

### Requisitos previos

- Python 3.14.
- Un navegador con permisos para utilizar la cámara en la herramienta 01.
- Un entorno virtual de Python.

### Instalación

Desde la raíz del proyecto, cree o active el entorno virtual e instale las dependencias:

```bash
    python3.14 -m venv .venv
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

Las imágenes deben presentar suficiente resolución, contraste y calidad para el algoritmo correspondiente. La iluminación uniforme, la reducción de oclusiones y la separación visual entre objetos favorecen resultados más estables. El analizador de escenas utiliza los archivos locales de SegFormer incluidos en `models/`.

Los métodos de detección utilizados dependen del modelo, sus categorías de entrenamiento, el umbral de confianza, la resolución y las condiciones de la escena. En particular, YOLO11n no debe interpretarse como un clasificador universal de objetos fuera de las categorías para las que fue entrenado.

## Estado actual del proyecto

Se encuentran implementados el Home y las siete herramientas del laboratorio. La galería de escenas incluye fotografías predefinidas y los modelos utilizados están incluidos localmente en `models/`. La inferencia se ejecuta después de instalar las dependencias.
