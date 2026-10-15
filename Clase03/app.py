import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# --------------------------------------------------
# TÍTULOS Y TEXTO
# --------------------------------------------------

st.title("First App with Streamlit")
st.header("Header")
st.subheader("SubHeader")
st.text("Lorem ipsum basic text")
st.markdown("**Texto en negrita** y *texto en cursiva* con Markdown")
st.write("st.write() sirve para mostrar casi cualquier tipo de contenido.")

# --------------------------------------------------
# DATOS DE EJEMPLO
# --------------------------------------------------

data = {
    "Nombre": ["Ana", "Luis", "Carlos"],
    "Edad": [23, 30, 35]
}
df = pd.DataFrame(data)

# --------------------------------------------------
# TABLAS
# --------------------------------------------------

st.header("Tablas")
st.table(df)
st.write(df)
st.dataframe(df, width=1000, height=200)

# --------------------------------------------------
# INPUTS
# --------------------------------------------------

st.header("Inputs")
nombre = st.text_input("Ingrese su nombre")
edad = st.number_input("Ingrese su edad", min_value=0, max_value=120, value=18)
opcion = st.selectbox("Seleccione una opción", ["Python", "C#", "JavaScript"])
lenguajes = st.multiselect(
    "Seleccione uno o más lenguajes",
    ["Python", "C#", "JavaScript", "SQL", "Java"]
)
nivel = st.radio("Seleccione un nivel", ["Básico", "Intermedio", "Avanzado"])
mostrar = st.checkbox("Mostrar mensaje")
valor = st.slider("Seleccione un valor", 0, 100, 50)
fecha = st.date_input("Seleccione una fecha")

st.write("Nombre:", nombre)
st.write("Edad:", edad)
st.write("Opción:", opcion)
st.write("Lenguajes:", lenguajes)
st.write("Nivel:", nivel)
st.write("Valor:", valor)
st.write("Fecha:", fecha)

if mostrar:
    st.write("El checkbox está seleccionado.")

if st.button("Presioname"):
    st.success("Presionaste el botón.")

# --------------------------------------------------
# ARCHIVOS
# --------------------------------------------------

st.header("Archivos")
archivo = st.file_uploader(
    "Seleccione un archivo",
    type=["csv", "txt", "jpg", "png"]
)

if archivo is not None:
    st.write("Archivo cargado:", archivo.name)

# --------------------------------------------------
# COLUMNAS
# --------------------------------------------------

st.header("Columnas")
col1, col2 = st.columns(2)

with col1:
    st.write("Columna 1")

with col2:
    st.write("Columna 2")

# --------------------------------------------------
# MÉTRICAS
# --------------------------------------------------

st.header("Métricas")
col1, col2, col3 = st.columns(3)
col1.metric("Ventas", "$15.000", "5 %")
col2.metric("Usuarios", "1.250", "120")
col3.metric("Errores", "15", "-3")

# --------------------------------------------------
# MENSAJES
# --------------------------------------------------

st.header("Mensajes")
st.success("Mensaje de éxito")
st.info("Mensaje informativo")
st.warning("Mensaje de advertencia")
st.error("Mensaje de error")

# --------------------------------------------------
# GRÁFICO CON MATPLOTLIB
# --------------------------------------------------

st.header("Gráfico con Matplotlib")
x = np.arange(1, 11)
y = x ** 2

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Ejemplo de gráfico")
ax.set_xlabel("X")
ax.set_ylabel("Y")

st.pyplot(fig)

# --------------------------------------------------
# GRÁFICOS DE STREAMLIT
# --------------------------------------------------

st.header("Gráficos de Streamlit")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)

st.line_chart(chart_data)
st.bar_chart(chart_data)
st.area_chart(chart_data)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Menú lateral")
pagina = st.sidebar.selectbox(
    "Seleccione una página",
    ["Inicio", "Datos", "Gráficos"]
)
st.sidebar.write("Página seleccionada:", pagina)

# --------------------------------------------------
# EXPANDER
# --------------------------------------------------

with st.expander("Ver más información"):
    st.write("Contenido oculto dentro del expander.")

# --------------------------------------------------
# CONTAINER
# --------------------------------------------------

with st.container():
    st.subheader("Container")
    st.write("Contenido dentro de un contenedor.")

# --------------------------------------------------
# DIVISOR
# --------------------------------------------------

st.divider()

# --------------------------------------------------
# EJEMPLO INTERACTIVO FINAL
# --------------------------------------------------

st.header("Ejemplo interactivo")

nombre_usuario = st.text_input(
    "Nombre",
    key="nombre_usuario"
)

edad_usuario = st.slider(
    "Edad",
    0,
    100,
    25,
    key="edad_usuario"
)

lenguaje_usuario = st.selectbox(
    "Lenguaje favorito",
    ["Python", "C#", "JavaScript", "SQL"],
    key="lenguaje_usuario"
)

if st.button("Mostrar información"):
    st.write("Nombre:", nombre_usuario)
    st.write("Edad:", edad_usuario)
    st.write("Lenguaje favorito:", lenguaje_usuario)
    st.success("Datos procesados correctamente")