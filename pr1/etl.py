from collections import Counter
import time
#import nltk
#nltk.download('punkt')
#from nltk.tokenize import word_tokenize
from lxml import etree
import json
import os
import re
from clize import run

#extract() -> Función para eliminar etiquetas de los archivos .xml y quedarnos con el contenido de las etiquetas dadas en idioma deseado
def extract(ruta_archivo,idioma_deseado='es',etiquetas_deseadas=[]):
    contenido_limpio = ''

    # Crear un analizador XML
    parser = etree.XMLParser(recover=True)

    # Leer el archivo XML
    tree = etree.parse(ruta_archivo, parser)

    namespaces = {
    'dc': 'http://purl.org/dc/elements/1.1/'
    }

    # Obtener todas las etiquetas <dc:title> y <dc:description>
    etiquetas = []
    for etiqueta in etiquetas_deseadas:
        etiquetas += tree.xpath('//dc:'+etiqueta, namespaces=namespaces)

    # Iterar sobre las etiquetas de título y descripción
    for etiqueta in etiquetas:
        idioma = etiqueta.get('{http://www.w3.org/XML/1998/namespace}lang')
        if idioma == idioma_deseado or not idioma:
            contenido_limpio += etiqueta.text + ' '  # Concatenar los textos con un espacio entre cada uno

    return contenido_limpio.strip()  # Eliminar los espacios en blanco al principio y al final

#transform() -> Función que dado un texto lo tokeniza quedandose con los caracteres deseados
def transform(texto):
    # Convertir a minúsculas
    texto = texto.lower()

     # Eliminar caracteres no alfanuméricos y espacios
    texto = texto.replace(',', ' ')
    texto = re.sub(r'[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ\s]', '', texto)
    
    
    # Tokenización
    #tokens = word_tokenize(texto)
    tokens = texto.split()
    return tokens

#load() -> Función que almacena los tokens en un .json
def load(lista, nombre_archivo,directorio_destino):
    # Guardar la lista en un archivo JSON
    #eliminamos la extension del archivo dado
    nombre_archivo = nombre_archivo[:nombre_archivo.rfind(".")]
    # Comprobamos si la carpeta no existe
    if not os.path.exists(directorio_destino):
        # Creamos la carpeta si no existe
        os.makedirs(directorio_destino)
    ruta_archivo_json = os.path.join(directorio_destino, nombre_archivo + '.json')
    with open(ruta_archivo_json, 'w') as archivo_json:
        json.dump(lista, archivo_json, indent=4)
def cargar_configuracion(ruta_archivo_config):
    with open(ruta_archivo_config) as f:
        config = json.load(f)
    return config

def obtener_archivos_xml(directorio):
    archivos_xml = []
    for archivo in os.listdir(directorio):
        if archivo.endswith('.xml'):
            archivos_xml.append(archivo)
    return archivos_xml
#Programa Principal 
def etlXML(archivo_config: str ,logs: bool = True):
    """Conviente un directorio de xml a jsons de tokens"""
    config = cargar_configuracion(archivo_config)
    rutaResultados = config["rutaResultadosETL"]
    total = Counter()
    media_tokens = 0
    archivos_xml = obtener_archivos_xml(config['rutaXML'])
    start_time = time.time()
    for archivo in archivos_xml:
        if logs:print("Procesando " + archivo)
        contenido_seleccionado = extract(os.path.join(config['rutaXML'], archivo), config['idioma'], config['etiquetasXML'])
        tokens = transform(contenido_seleccionado)
        total.update(tokens)  # Actualizar el contador total con los tokens del archivo
        load(tokens, archivo, rutaResultados)
    total_tokens = sum(total.values())
    media_tokens = total_tokens / len(archivos_xml)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\tTiempo de etl: {execution_time} segundos")
    if logs:
        print("\tTotal de tokens procesados: " + str(total_tokens))
        print("\tTotal de archivos procesados: " + str(len(archivos_xml)))
        print("\tMedia de tokens por archivo: "+str(round(media_tokens)))
        print("\tPalabras más comunes:")
        for palabra, frecuencia in total.most_common(10):
            print("\t\t{:<20} {:<10}".format(palabra, frecuencia))
if __name__ == "__main__":
    run(etlXML)
    

