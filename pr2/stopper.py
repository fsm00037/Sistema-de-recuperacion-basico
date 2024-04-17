
#from nltk.corpus import stopwords
#import nltk
from collections import Counter
import json
import os
import pickle
import time
from clize import run, parameters
import sys

sys.path.insert(1, os.path.join(os.getcwd(), "pr1"))

from etl import load
#nltk.download('stopwords')

#stop_es = set(stopwords.words('spanish'))
#stop_en = set(stopwords.words('english'))
   
def stopper(milista, idioma):
  resultado=[]
  if idioma == "es":
      with open(os.path.join("pr2","stop_es.pkl"), 'rb') as f:
        stop_es = pickle.load(f) 
      resultado = [word for word in milista if word not in stop_es and len(word)>1]
  elif idioma == "en":
      with open(os.path.join("pr2","stop_en.pkl"), 'rb') as f:
        stop_en = pickle.load(f) 
      resultado = [word for word in milista if word not in stop_en and len(word)>1]
  
  return resultado

def cargar_configuracion(ruta_archivo_config):
    with open(ruta_archivo_config) as f:
        config = json.load(f)
    return config

def runStopper(archivo_config: str ,logs: bool = True):
  """Elimina las palabras vacías de un directorio de tokens"""
  start_time = time.time()
  config = cargar_configuracion(archivo_config)
  media_tokens = 0
  total = Counter()
  rutaResultados = config["rutaResultadosETL"]
  for archivo in os.listdir(rutaResultados):
      if archivo.endswith('.json'):
          with open(os.path.join(rutaResultados, archivo), 'r') as f:
              datos_json = json.load(f)
              tokens_post_stopper = stopper(datos_json, config["idioma"])
              media_tokens += len(tokens_post_stopper)
              total.update(tokens_post_stopper)
              load(tokens_post_stopper, archivo, config["rutaResultadosStopper"])
  end_time = time.time()
  execution_time = end_time - start_time
  print(f"\tTiempo de stopper: {execution_time} segundos")
  if logs:
    print("Después del stopper:") 
    print("\tTotal de tokens: " + str(media_tokens))
    media_tokens /= len(os.listdir(config["rutaResultadosStopper"]))  # Calcular la media después de sumar todos los tokens
    print("\tMedia de tokens: " + str(round(media_tokens)))
    palabrasUnicas = len(set(total))
    print("\tPalabras únicas: "+str(palabrasUnicas))
    print("\tPalabras más comunes:")
    for palabra, frecuencia in total.most_common(10):
        print("\t\t{:<20} {:<10}".format(palabra, frecuencia))

if __name__ == "__main__":
  run(runStopper)
