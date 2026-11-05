#!/bin/bash

# Este archivo debe estar dentro de IAPIM, junto a requirements.txt.
set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$(dirname "$PROJECT_DIR")"

cd "$PROJECT_DIR"

if [ ! -f "$PROJECT_DIR/requirements.txt" ] || [ ! -f "$PROJECT_DIR/TP2/main.py" ]; then
    echo "ERROR: No se encontraron requirements.txt y TP2/main.py en IAPIM."
    read -r -p "Presioná Enter para cerrar esta ventana..."
    exit 1
fi

if [ ! -x "$VENV_DIR/bin/python" ]; then
    echo "Creando entorno virtual con Python 3.14..."
    if ! command -v python3.14 >/dev/null 2>&1; then
        echo "ERROR: Python 3.14 no está instalado o no está disponible en PATH."
        read -r -p "Presioná Enter para cerrar esta ventana..."
        exit 1
    fi
    python3.14 -m venv "$VENV_DIR"
fi

# Activar el entorno, incluso si se ejecuta desde Finder.
source "$VENV_DIR/bin/activate"

if [ "$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')" != "3.14" ]; then
    echo "ERROR: El entorno no utiliza Python 3.14."
    read -r -p "Presioná Enter para cerrar esta ventana..."
    exit 1
fi

echo "Instalando dependencias desde requirements.txt..."
if ! python -m pip install -r "$PROJECT_DIR/requirements.txt"; then
    echo "ERROR: No se pudieron instalar las dependencias."
    read -r -p "Presioná Enter para cerrar esta ventana..."
    exit 1
fi

echo "Iniciando Vision Lab..."
cd "$PROJECT_DIR/TP2"
python -m streamlit run main.py
status=$?
echo "Streamlit finalizó con código $status."
read -r -p "Presioná Enter para cerrar esta ventana..."
exit "$status"
