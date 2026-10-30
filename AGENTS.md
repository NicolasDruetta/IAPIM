# Convenciones generales de IAPIM

## Propósito

Este documento establece las convenciones generales de programación, organización y mantenimiento aplicables a las clases, ejercicios, trabajos prácticos y proyectos del repositorio IAPIM. Las decisiones particulares de cada trabajo se documentan en el README correspondiente.

## Convenciones de Python

- Python 3.15 es la versión de referencia, salvo que un proyecto documente explícitamente otra versión compatible.
- El código sigue el estilo PEP 8.
- Las variables, funciones y módulos utilizan nombres en `snake_case`.
- Las clases utilizan nombres en `PascalCase` cuando corresponde.
- Las constantes utilizan nombres en `UPPER_SNAKE_CASE`.
- Los nombres son descriptivos y favorecen la legibilidad del código.
- Entre funciones y bloques de código se deja exactamente una línea en blanco, de acuerdo con la convención adoptada para este repositorio.
- Las importaciones se ubican al comienzo de cada archivo y se organizan con los `import` antes de los `from`.
- Los comentarios y docstrings se incorporan cuando aportan contexto, explican una decisión o mejoran la comprensión del código.
- Los decoradores se reservan para necesidades técnicas justificadas.

## Organización del código

La organización del código mantiene una separación clara entre interfaz, procesamiento y utilidades. Las funciones compartidas se centralizan cuando existe reutilización real y una responsabilidad común claramente definida.

Los módulos conservan independencia y responsabilidades acotadas. La estructura procura ser sencilla, legible y proporcional al alcance del proyecto, evitando abstracciones innecesarias.

Cada carpeta conserva las convenciones y estructuras existentes de su proyecto. Los cambios se integran de forma localizada para mantener la coherencia con el código que ya se encuentra implementado.

## Streamlit

Cuando un proyecto utiliza Streamlit, la interfaz se construye con componentes nativos de la biblioteca. Cada página define directamente sus componentes de presentación, controles, eventos y resultados.

La organización multipágina se utiliza cuando el alcance del proyecto lo requiere. La presentación permanece separada de las funciones auxiliares y la navegación se resuelve mediante los mecanismos nativos disponibles.

La distribución de la interfaz contempla distintos tamaños de pantalla y mantiene una presentación adaptable. Los textos, entradas, acciones y resultados se organizan con una jerarquía clara y consistente.

Los textos visibles de las interfaces utilizan tratamiento formal de usted y evitan el voseo.

## Procesamiento de imágenes

El procesamiento de imágenes utiliza las bibliotecas estudiadas en IAPIM y selecciona los algoritmos de acuerdo con los objetivos de cada ejercicio.

Las implementaciones validan las imágenes de entrada, contemplan errores de lectura o procesamiento y presentan los resultados de manera clara. La interpretación de cada resultado incluye las limitaciones propias del algoritmo, los datos de entrada y las condiciones de la escena.

## Dependencias y entornos

Los proyectos utilizan entornos virtuales de Python para aislar sus dependencias y facilitar la reproducción del entorno de trabajo.

Las bibliotecas se declaran en archivos de requisitos o en el sistema de gestión de dependencias adoptado por cada proyecto. Su incorporación responde a necesidades reales de implementación y mantiene compatibilidad con la versión de Python documentada.

Las rutas de recursos se resuelven de manera relativa cuando corresponde, favoreciendo la portabilidad entre equipos y evitando dependencias de rutas personales o absolutas.

## Documentación y mantenimiento

La documentación técnica se mantiene clara, actualizada y coherente con el estado real del código. Cada trabajo práctico cuenta con su README específico cuando necesita explicar objetivos, arquitectura, instalación, funcionamiento o limitaciones particulares.

Las modificaciones son puntuales y preservan el comportamiento existente cuando el alcance no requiere cambios funcionales. El desarrollo incremental permite incorporar y validar cada funcionalidad de manera independiente.

La validación incluye la comprobación de sintaxis, la revisión de dependencias, la ejecución de las funcionalidades afectadas y la verificación de que la documentación continúa representando la implementación.

## Criterios de formato

No se utilizan dos o más líneas en blanco consecutivas en los archivos del repositorio. Toda separación entre funciones, clases, bloques o secciones utiliza como máximo una línea en blanco.
