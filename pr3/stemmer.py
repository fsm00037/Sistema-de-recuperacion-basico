from collections import Counter
import json
import os
import time
from clize import run
import nltk
from nltk.stem import SnowballStemmer
import sys

sys.path.insert(1, os.path.join(os.getcwd(), "pr1"))

from etl import load

stemmerES = SnowballStemmer("spanish")
stemmerEN = SnowballStemmer("english")
def snowball_stemmer(tokens, language='es'):
    if language == 'es': stemmer = stemmerES
    else: stemmer = stemmerEN
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

def cargar_configuracion(ruta_archivo_config):
    with open(ruta_archivo_config) as f:
        config = json.load(f)
    return config

def runStemmer(archivo_config: str ,logs: bool = True):
   
    """Extrae las raices de los tokens"""
    start_time = time.time()
    config = cargar_configuracion(archivo_config)
    media_tokens = 0
    total = Counter()
    rutaResultados = config["rutaResultadosETL"]
    
    for archivo in os.listdir(config["rutaResultadosStopper"]):
        if archivo.endswith('.json'):
            with open(os.path.join(config["rutaResultadosStopper"], archivo), 'r') as f:
                datos_json = json.load(f)
                tokens_post_stemmer = snowball_stemmer(datos_json, config["idioma"])
                media_tokens += len(tokens_post_stemmer)
                total.update(tokens_post_stemmer)
                load(tokens_post_stemmer, archivo, config["rutaResultadosStemmer"])
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"\tTiempo de stemmer: {execution_time} segundos")
    if logs:
        print("Después del stemmer:")
       
        print("\tTotal de tokens: " + str(media_tokens))
        media_tokens /= len(os.listdir(config["rutaResultadosStopper"]))  # Calcular la media después de sumar todos los tokens
        print("\tMedia de tokens: " + str(round(media_tokens)))
        palabrasUnicas = len(set(total))
        print("\tPalabras únicas: "+str(palabrasUnicas))
        print("\tPalabras más comunes:")
        for palabra, frecuencia in total.most_common(10):
            print("\t\t{:<20} {:<10}".format(palabra, frecuencia))   
# Ejemplo de uso
if __name__ == "__main__":
    run(runStemmer)
