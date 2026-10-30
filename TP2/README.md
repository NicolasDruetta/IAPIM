# IAPIM Vision Lab

## Presentación

IAPIM Vision Lab es un laboratorio académico de visión artificial y procesamiento de imágenes desarrollado para la materia Inteligencia Artificial y Procesamiento de Imágenes.

- Autor: Nicolás Druetta.
- Año: 2026.
- Trabajo práctico: Parcial 1.

## Descripción general

La aplicación reúne herramientas independientes para explorar problemas de visión artificial. El laboratorio aborda la detección de rostros, la detección de objetos y la segmentación semántica de escenas.

Estas técnicas tienen aplicaciones prácticas en sistemas de asistencia, inspección visual, automatización de tareas, análisis de escenas y apoyo a la toma de decisiones. Los resultados dependen de la calidad de las imágenes y de las condiciones específicas de cada escenario.

## Tecnologías utilizadas

- Python 3.14.
- Streamlit 1.66.0 para la interfaz multipágina.
- OpenCV 5.0.0.93 para lectura y transformación de imágenes.
- NumPy 2.5.4 para representar imágenes y realizar operaciones matriciales.
- PyTorch 2.15.0 como motor de inferencia de aprendizaje profundo.
- Torchvision 0.29.2 como dependencia de visión de PyTorch.
- Transformers 5.22.0 para cargar el procesador y el modelo SegFormer.
- Ultralytics 8.4.193 para ejecutar modelos YOLO.
- `pathlib`, incluida en la biblioteca estándar de Python, para resolver rutas de recursos.

El archivo `requirements.txt` también conserva dependencias disponibles para el entorno académico general: Matplotlib, pandas, Pillow y scikit-image. La implementación actual de TP2 utiliza directamente Streamlit, OpenCV, NumPy, Pillow, PyTorch, Torchvision, Transformers, Ultralytics y `pathlib`.

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
│       └── 03_analizador_de_escenas/
├── functions.py
├── main.py
├── yolo11n.pt
├── pages/
│   ├── 01_detector_facial.py
│   ├── 02_detector_de_objetos.py
│   └── 03_analizador_de_escenas.py
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

**Objetivo:** detectar objetos reconocidos por un modelo general preentrenado y mostrar sus categorías con sus niveles de confianza.

**Entrada:** una imagen cargada desde la computadora mediante `st.file_uploader()` o una imagen precargada de `assets/images/02_detector_de_objetos/`.

**Funcionamiento:** la imagen se entrega a YOLO11n, un modelo de detección general preentrenado sobre el conjunto de datos COCO. El modelo devuelve las cajas delimitadoras, las categorías y las confianzas de cada detección. La inferencia utiliza Apple Metal Performance Shaders (MPS) cuando está disponible y CPU como alternativa.

**Algoritmos:** inferencia de detección de objetos mediante YOLO11n y representación de cajas delimitadoras mediante Ultralytics.

**Resultados:** la aplicación muestra la imagen procesada con rectángulos, categoría y confianza de cada detección. También informa la cantidad total y el recuento agrupado por categoría.

**Modelo y procedencia:** se utiliza `yolo11n.pt`, distribuido por Ultralytics como modelo preentrenado para detección general. El paquete Ultralytics se distribuye bajo licencia AGPL-3.0 y el modelo se basa en las categorías de COCO. El archivo de pesos debe conservarse junto a `main.py` para que la aplicación pueda cargarlo de forma local.

**Resultados de validación:** con un umbral de confianza de 0.25, las cinco imágenes precargadas produjeron los siguientes resultados:

| Imagen | Detecciones | Categorías observadas |
| --- | ---: | --- |
| `01.jpg` | 4 | cake (4) |
| `02.jpg` | 0 | ninguna |
| `03.jpg` | 2 | clock (1), cell phone (1) |
| `04.jpg` | 1 | cell phone (1) |
| `05.jpg` | 4 | potted plant (1), scissors (3) |

**Limitaciones:** las imágenes precargadas contienen figuras geométricas sintéticas que no representan necesariamente las categorías de COCO. Por esa razón, YOLO puede no detectar objetos, asignar categorías incorrectas o producir detecciones de baja confianza. El modelo no fue entrenado específicamente para esas figuras y no se modificaron artificialmente los resultados.

### 03 – Analizador de escenas

**Objetivo:** segmentar semánticamente una fotografía y asignar una categoría a cada píxel según las clases reconocidas por ADE20K, como cielo, edificios, calles, árboles, vegetación, suelo, paredes y muebles.

**Entrada:** una fotografía cargada desde la computadora mediante `st.file_uploader()` o una fotografía real precargada en `assets/images/03_analizador_de_escenas/`. La página también permite elegir una fotografía aleatoria de la galería cuando esta contiene imágenes.

**Segmentación semántica:** cada píxel recibe una clase del modelo. El resultado no representa objetos individuales ni utiliza cajas delimitadoras; una misma categoría puede aparecer en varias regiones de la imagen.

**Modelo:** se utiliza `nvidia/segformer-b0-finetuned-ade-512-512`, un modelo SegFormer preentrenado sobre ADE20K. `AutoImageProcessor` prepara la imagen y ajusta el mapa de clases a la resolución original mediante el postprocesamiento de Transformers.

**Resultados:** la página muestra la fotografía original, una superposición coloreada, una leyenda con los nombres reales de las categorías, el porcentaje de píxeles de cada categoría y la cantidad de categorías presentes. La opacidad se modifica con un slider sin repetir la inferencia: el mapa y las estadísticas permanecen en `st.session_state`.

**Procesamiento:** el modelo se carga con `st.cache_resource()`. La inferencia selecciona CUDA cuando está disponible, MPS en Apple Silicon como alternativa y CPU en los demás equipos. La primera ejecución descarga el procesador, la configuración y los pesos desde Hugging Face y los conserva en la caché local del usuario.

**Estado de la galería:** al momento de esta implementación no hay fotografías variadas disponibles en el repositorio. La carpeta `assets/images/03_analizador_de_escenas/` queda preparada para incorporar fotografías reales de ciudad, calle, bosque, playa, oficina o habitación. Hasta agregar esas imágenes, la interfaz muestra un aviso y permite utilizar la carga manual.

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

Las imágenes deben presentar suficiente resolución, contraste y calidad para el algoritmo correspondiente. La iluminación uniforme, la reducción de oclusiones y la separación visual entre objetos favorecen resultados más estables. En la herramienta 03, la primera carga del modelo SegFormer requiere conexión a Internet y espacio de caché para los archivos descargados; las ejecuciones posteriores pueden reutilizar esa caché.

Los métodos de detección utilizados dependen del modelo, sus categorías de entrenamiento, el umbral de confianza, la resolución y las condiciones de la escena. En particular, YOLO11n no debe interpretarse como un clasificador universal de objetos fuera de las categorías para las que fue entrenado.

## Estado actual del proyecto

Se encuentran implementados el Home, la navegación entre las tres herramientas, el detector facial, el detector de objetos mediante YOLO11n y el analizador de escenas mediante SegFormer. La galería de escenas queda preparada, pero requiere fotografías reales para evaluar visualmente la herramienta con imágenes precargadas. La inferencia real se ejecutará después de instalar las dependencias y descargar el modelo desde Hugging Face.
