# AGENTS.md

## Proyecto

Este repositorio contiene una aplicación de Streamlit para la materia de Procesamiento de Imágenes.

La carpeta raíz de la aplicación se llama exactamente:

`IAPIM`

Estructura actual:

```text
env/
└── IAPIM/
    ├── main.py
    └── pages/
        ├── clase5.py
        ├── clase6.py
        └── futuras_clases.py
```

El punto de entrada único de la aplicación es `main.py`.

Comando de ejecución:

```bash
streamlit run env/IAPIM/main.py
```

## Navegación global

`main.py` debe construir dinámicamente la navegación leyendo los archivos `.py` existentes dentro de `pages`.

Reglas obligatorias:

- El menú global debe estar siempre arriba de todo en la barra lateral.
- Debe mostrar el encabezado `Menú` como texto fijo, grande y en negrita.
- `Menú` no debe ser colapsable ni formar parte de un grupo plegable.
- Debajo deben aparecer los nombres reales de los archivos.
- Los nombres no se deben capitalizar ni transformar.
- Si el archivo se llama `clase5.py`, debe verse exactamente `clase5.py`.
- Si se agrega `clase7.py`, debe aparecer automáticamente sin editar manualmente `main.py`.
- `main.py` también debe aparecer como opción de navegación.
- El cuerpo de `main.py` no debe quedar vacío.
- El cuerpo de `main.py` debe mostrar links dinámicos a los archivos encontrados dentro de `pages`.
- No mezclar el menú global con los menús internos de cada clase.

La estructura visual esperada es:

```text
Menú
main.py
clase5.py
clase6.py
...
```

## Navegación interna de cada clase

Cada archivo de clase mantiene su propio menú interno.

Flujo obligatorio:

1. Al entrar a una clase, primero debe aparecer la opción de subir una imagen.
2. Antes de subir una imagen no debe aparecer el menú interno de operaciones.
3. Después de subir la imagen debe aparecer el menú interno de esa clase debajo del menú global.
4. El menú global nunca debe desaparecer ni ser reemplazado.
5. El encabezado interno debe identificar la clase, por ejemplo `Clase 5` o `Clase 6`.

Ejemplo conceptual:

```text
Menú
main.py
clase5.py
clase6.py

Clase 5
Contenido
Imagen original
Traslación
Rotación
Escalado
Blur promedio
Gaussian Blur
Sobel
Canny
```

## Comportamiento de clase5.py y clase6.py

Ambas clases deben seguir la misma estructura general:

- Pantalla inicial: subir imagen.
- Después de cargarla: mostrar menú interno en la barra lateral.
- Cada opción del menú representa una transformación, filtro o análisis.
- Antes de mostrar el resultado de una transformación, mostrar en el front la línea o bloque de código Python que realiza esa operación.
- Debajo del código, mostrar el resultado visual.
- Siempre que tenga sentido, los parámetros deben ser interactivos.

Ejemplos de controles interactivos:

- Traslación: desplazamiento horizontal y vertical.
- Rotación: ángulo.
- Escalado: factor de escala.
- Blur: tamaño del kernel.
- Gaussian Blur: tamaño del kernel.
- Canny: umbral inferior y superior.
- Brillo y contraste: valores ajustables.
- Kernel y convolución: tipo o tamaño del kernel cuando corresponda.

El código visible en el front debe reflejar los valores actuales elegidos por el usuario.

## Estilo de código obligatorio

Todo el código Python debe respetar estas reglas:

- Usar `snake_case` para variables y funciones.
- Conservar comentarios útiles por bloque lógico.
- No eliminar comentarios relevantes para compactar el archivo.
- Usar como máximo una sola línea vacía entre bloques principales.
- Nunca usar dos o más líneas vacías consecutivas.
- Antes de un `def`, como máximo una sola línea vacía.
- No agregar separaciones excesivas entre bloques.
- El archivo debe terminar exactamente en la última línea de código.
- No debe existir salto de línea final ni una línea vacía después de la última línea de código.
- Mantener el mismo nombre de archivo original al devolver una modificación.
- Nunca agregar sufijos como `_final`, `_edit`, `_modified` o similares salvo pedido explícito.

## Regla crítica de trabajo con archivos

Cuando se creen, modifiquen, revisen o empaqueten archivos:

- No mostrar código Python de trabajo en el chat.
- No mostrar scripts auxiliares.
- No mostrar comandos internos usados para generar archivos.
- No mostrar contenido crudo leído de archivos.
- No mostrar dumps, JSON ni resultados intermedios.
- No mostrar razonamiento interno.
- Trabajar internamente y mantener la conversación limpia.

En el chat solo mostrar:

- estado breve si hace falta;
- conclusiones;
- cambios realizados;
- archivo final para descargar;
- comando final que el usuario necesite ejecutar.

Excepción: mostrar código únicamente cuando el usuario lo pida explícitamente.

## Archivos Streamlit

Cuando se entregue un archivo destinado a Streamlit, incluir siempre el comando exacto para ejecutarlo.

Para este proyecto:

```bash
streamlit run env/IAPIM/main.py
```

## Errores que no hay que repetir

- No convertir `Menú` en una sección colapsable.
- No mover `Menú` debajo de los links de navegación.
- No renombrar visualmente `clase5.py` como `Clase 5` en el menú global.
- No hardcodear manualmente las clases en `main.py` si pueden leerse dinámicamente desde `pages`.
- No usar rutas incorrectas para `st.Page` que hagan que Streamlit no encuentre `clase5.py` o `clase6.py`.
- No dejar el cuerpo de `main.py` vacío.
- No mezclar navegación global con navegación interna.
- No mostrar el menú interno de una clase antes de subir una imagen.
- No perder comentarios útiles.
- No introducir dobles líneas vacías.
- No dejar una línea vacía al final de los archivos.
- No cambiar nombres de archivo al devolver versiones corregidas.
- No mostrar Python en el chat mientras se generan o corrigen archivos.

## Regla de extensión futura

Al agregar una nueva clase:

1. Crear el archivo correspondiente dentro de `IAPIM/pages`.
2. Mantener el nombre exacto elegido, por ejemplo `clase7.py`.
3. No modificar manualmente la lista de navegación del `main.py`.
4. `main.py` debe detectarla automáticamente.
5. La nueva clase debe seguir la misma estructura de carga de imagen, menú interno, código visible en el front y controles interactivos.