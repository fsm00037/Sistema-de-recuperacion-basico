# Sistema de Recuperación de Información (SRI)

## Introducción:

En este repositorio, encontrarás dos programas principales dentro de la carpeta `SRI`:

- `indexador.py`
- `buscador.py`

Además, hay carpetas que contienen los módulos utilizados en `indexador.py`, donde cada módulo puede ejecutarse por separado:

- `pr1`
- `pr2`
- `pr3`
- `pr4`
- `pr5`

También se incluyen carpetas auxiliares:

- `data`
- `indices`
- `resultados`

Y los archivos:

- `config.json`
- `queries.txt`

## Instrucciones para `indexador.py`:

1. Añade todos los archivos XML que desees procesar en la carpeta `data`.
2. Configura el archivo `config.json` según tus necesidades.
3. Ejecuta uno a uno cada módulo o directamente ejecuta `indexador.py` usando el siguiente comando:
    ```
    python indexador.py [archivo configuración] [bool: imprimir logs en consola]
    ```
4. Los archivos JSON con los términos se generarán en la carpeta `resultados`, mientras que los índices se guardarán en la carpeta `indices`.

## Instrucciones para `buscador.py`:

1. Una vez indexados los documentos XML en la carpeta `data`, añade las consultas en el archivo `queries.txt`.
2. Ejecuta `buscador.py` mediante el siguiente comando:
    ```
    python buscador.py [archivo configuración] [k documentos relevantes]
    ```
3. Los resultados se mostrarán por consola y se generarán de forma compacta en `resultados/resultadosQueries`.
