Estructura del sitio:

- app.py: es el controlador principal. Configura la aplicación, muestra el menú lateral y llama a la página seleccionada.
- functions.py: contiene las funciones reutilizables y las herramientas específicas que utilizan cada una de las páginas.
- pages/ contiene el home y una página por cada clase. Cada archivo tiene el cuerpo de su página y usa las funciones de functions.py.
- assets/ contiene custom.css, que mejora visualmente los estilos nativos de streamlit y define los modos claro y oscuro.