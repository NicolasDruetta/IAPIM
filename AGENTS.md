# Reglas

## REGLA UNIVERSAL DE SEPARACIÓN

- No puede haber más de una línea en blanco consecutiva en ningún archivo del proyecto.
- Nunca separo dos funciones, clases, bloques o instrucciones con dos o más líneas en blanco.

## Convenciones generales

- Uso la convención PEP 8 para la nomenclatura y el formato del código.
- Entre funciones y bloques de código dejo exactamente una línea en blanco: ni cero ni dos.
- No dejo líneas en blanco consecutivas. Toda separación utiliza como máximo una
  sola línea en blanco; nunca separo dos definiciones con dos o más líneas.
- Ordeno alfabéticamente todas las funciones dentro de cada archivo.
- Primero van todos los `import`, después todos los `from`, y cada grupo se ordena alfabéticamente.
- Utilizo solamente componentes nativos de Streamlit, sin HTML, CSS ni JavaScript.
- No utilizo selectores CSS basados en atributos `data-testid`; cuando se
  autoriza CSS, utilizo únicamente clases reales y semánticas de Streamlit.
- `functions.py` no contiene HTML, CSS inline ni componentes visuales; toda la
  interfaz queda escrita directamente en `main.py` y en cada página.

## Arquitectura permanente de IAPIM Vision Lab – TP2

1. `main.py` es el punto de entrada y contiene toda la interfaz del Home.
2. Cada archivo de `pages/` contiene su propia interfaz Streamlit y sus algoritmos específicos.
3. `functions.py` contiene exclusivamente funciones auxiliares compartidas entre varias páginas.
4. Ningún componente visual de Streamlit debe estar en `functions.py`.
5. Mantengo las páginas independientes y los nombres numerados en `snake_case`.
6. Utilizo solamente algoritmos y bibliotecas autorizados por el material de IAPIM.
7. No creo archivos ni implemento funcionalidades futuras sin autorización.
8. No modifico la ubicación del proyecto ni el entorno virtual.
9. Respeto Python 3.15 y las convenciones de programación acordadas.
10. Cada nueva regla permanente o decisión de arquitectura debe documentarse en este archivo.

## Interfaz de páginas

- Todas las páginas Streamlit construyen su interfaz directamente en el cuerpo principal de su archivo `.py`.
- No encapsulo la interfaz completa dentro de funciones como `home()`, `render()`, `show_page()`, `main()` o equivalentes.
- Esta regla aplica a `main.py` y a todos los archivos presentes y futuros de `pages/`.
- Los componentes visuales, controles, eventos, resultados y lógica específica permanecen en el archivo de la página correspondiente.
- Mantengo `functions.py` exclusivamente para funciones auxiliares reutilizadas entre varias páginas, sin componentes de interfaz Streamlit.
- Mantengo la navegación nativa sin crear archivos adicionales ni funciones que encapsulen páginas.

## Arquitectura multipágina tradicional

- `main.py` es exclusivamente el Home y no utiliza `st.navigation()`, `st.Page()`, controladores de páginas ni ejecución de otras páginas.
- Cada archivo de `pages/` es independiente, contiene su interfaz directamente y se accede mediante enlaces nativos.
- La navegación entre páginas se realiza exclusivamente con los enlaces de las tarjetas y los enlaces de retorno.
- Esta arquitectura se aplica a todas las herramientas presentes y futuras.
