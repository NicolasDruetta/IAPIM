@echo off
setlocal

REM Este archivo debe estar dentro de IAPIM, junto a requirements.txt.
set "PROJECT_DIR=%~dp0"
for %%I in ("%PROJECT_DIR%..") do set "VENV_DIR=%%~fI"

if not exist "%PROJECT_DIR%requirements.txt" (
    echo ERROR: No se encontro requirements.txt en IAPIM.
    pause
    exit /b 1
)
if not exist "%PROJECT_DIR%TP2\main.py" (
    echo ERROR: No se encontro TP2\main.py en IAPIM.
    pause
    exit /b 1
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creando entorno virtual con Python 3.14...
    py -3.14 -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno con Python 3.14.
        pause
        exit /b 1
    )
)

call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual.
    pause
    exit /b 1
)

python -c "import sys; sys.exit(0 if sys.version_info[:2] == (3, 14) else 1)"
if errorlevel 1 (
    echo ERROR: El entorno virtual no utiliza Python 3.14.
    pause
    exit /b 1
)

echo Instalando dependencias desde requirements.txt...
python -m pip install -r "%PROJECT_DIR%requirements.txt"
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo Iniciando Vision Lab...
cd /d "%PROJECT_DIR%TP2"
python -m streamlit run main.py
if errorlevel 1 (
    echo ERROR: Streamlit finalizo con un error.
    pause
    exit /b 1
)

pause
endlocal
