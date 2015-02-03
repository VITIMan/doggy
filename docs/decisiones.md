# Decisiones tomadas

## Compresión de logs

La librería `logging` de Python incluye diversos tipos de manejadores de logs. Se pide un rotado de log por un tiempo determinado. El manejador `TimedrotatingFileHandler` es adecuado para ello.

Para la compresión de log no ha sido más que hacer una subclase de este manejador en el método `doRollover`.

Como complejidad. Por defecto, este manejador inserta un timestamp en lugar de unos números autoincrementales. Por lo que aplicar la compresión al fichero concreto no ha sido tan sencillo. La idea final ha sido obtener el fichero con la marca más reciente y comprimirlo, para después sustituirlo por el fichero en crudo.

Se ofrece la posibilidad de compresión zip o gzip. Por lo que podría extenderse a cualquier otra.

## Configuración

Tanto en doggy-wrapper como en doggy se han utilizado tres configuraciones:

- Configuración por defecto: Unos valores por defecto predefinidos
- Línea de comandos: Introducción de los parámetros mediante el prompt
- Fichero de configuración: Dado un fichero de configuración

El fichero de configuración debe indicarse mediante línea de comandos con la opción -c. En el caso de doggy-wrapper puede coger un fichero de configuración por defecto (doggy-wrapper.conf)

El fichero de configuración sobreescribe las opciones de línea de comandos y ambos a la configuración por defecto.


## Multiprocessing

Esta aplicación no hace una ejecución en paralelo en sí. Se ha usado la librería subprocess, que ejecuta programas como subprocesos desde un programa python. Efectivamente puede ejecutar tantos subprocesos como la máquina resista, pero no es una ejecución paralela en sí

La opción sería usar la librería multiprocessing. Sin embargo, la salida de logs no salía correcta por lo que tras varios intentos y por timing he tenido que desechar la idea y no poder investigar más al respecto.

Se deja old\_doggy\_wrapper.py a modo de consulta.

# Librerías externas

Para este proyecto he tomado la decisión de NO usar ninguna librería externa, sólo se utilizan librerías incluidas en Python 2.7. He decidido esto puesto que podemos estar en un entorno linux sin acceso a la red externa. Además de comodidad a la hora de ejecutar la prueba.

- Podría optarse por gevent o circuits para utilizar una gestión de eventos.
- Podría utilizarse celery (aunque demasiado para este proyecto), para una gestión eficaz de multiprocesamiento.

# Elección de Python

Es un lenguaje interpretado multipropósito presente en toda máquina UNIX. Su cantidad de librerías por defecto son adecuadas para múltiples entornos y una gestión eficaz en servidores.
