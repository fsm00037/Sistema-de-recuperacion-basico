
import json
import math
import os
import time

from clize import run
from pr1 import etl
from pr2 import stopper
from pr3 import stemmer
import pickle
#import numpy as np
import xml.etree.ElementTree as ET
import heapq

def cargar_configuracion(ruta_archivo_config):
    with open(ruta_archivo_config) as f:
        config = json.load(f)
    return config

def transformQuery(query,idioma):
    tokens  = etl.transform(query)
    tokens = stopper.stopper(tokens,idioma)
    tokens = stemmer.snowball_stemmer(tokens,idioma)
    tokens = list(set(tokens))
    return tokens
def normalizarTokens(tokens,term2id,idfs):
    normas = {}
    norma = 0
    for token in tokens:
        if token in term2id:
            idf = idfs[term2id[token]] 
            normas[term2id[token]] =  idf
            norma += idf * idf
    norma = math.sqrt(norma)    
    for clave, valor in normas.items():
        normas[clave] =valor/norma
    return normas    
def calculoSimilitud(normasQuery,pesos):
    similitud = {}
    for idTerm, norma in normasQuery.items():
        if idTerm in pesos:
            for id_doc, peso in pesos[idTerm].items():
                if id_doc not in similitud: 
                    similitud[id_doc] = 0
                pesoDoc = norma * peso  
                similitud[id_doc] += pesoDoc  
    return similitud   
def loadQueries(archivo):
    queries = []
    with open(archivo, 'r',encoding='utf-8') as archivoQueris:
        # Itera sobre cada línea del archivo 
        for linea in archivoQueris:
            queries.append(linea.strip())
    return queries
def getTitulo(idDoc,id2doc,directorio):
    ns = {'dc': 'http://purl.org/dc/elements/1.1/', 'xml': 'http://www.w3.org/XML/1998/namespace'}
    # Parsear el archivo XML
    nombre_archivo = id2doc[idDoc].replace(".json", "") + '.xml'
    arbol = ET.parse(os.path.join(directorio,nombre_archivo))
    raiz = arbol.getroot()
    # Encontrar la etiqueta 'lang' con atributo 'es'
    etiqueta_title = raiz.find(".//dc:title[@{http://www.w3.org/XML/1998/namespace}lang='es']", namespaces=ns)
    if etiqueta_title is not None:
        # Si se encuentra la etiqueta 'lang', obtener el contenido de 'title'
        return etiqueta_title.text
    else:
        print("No se encontró la etiqueta 'title' en español.")
def run_busca(archivo_config: str ,k: int):
    """Busca documentos relevantes"""
    start_time = time.time()
    config = cargar_configuracion(archivo_config)
    with open(config["rutaPesos"], 'rb') as f:
        pesos = pickle.load(f)
    with open(config["rutaIdfs"], 'rb') as f:
        idfs = pickle.load(f)    
    with open(config["rutaTerm2id"], 'rb') as f:
        term2id = pickle.load(f)      
    with open(config["rutaId2doc"], 'rb') as f:
        id2doc = pickle.load(f)   

    queries = loadQueries(config["rutaQueris"])

    nquery=0
    compact=""
    for query in queries:    
        nquery+=1
        tokens = transformQuery(query,config["idioma"]) 
        normas = normalizarTokens(tokens,term2id,idfs)
        similitud = calculoSimilitud(normas,pesos)
        k_primeros = dict(heapq.nlargest(k, similitud.items(), key=lambda item: item[1]))
        print("\nQuery: "+ query)
        pos = 0
        for indice, suma_columna in k_primeros.items():
                pos+=1
                print(str(pos)+"."+"("+str(suma_columna)+")"+"Doc:"+str(id2doc[indice]))
                print(" Titulo: "+getTitulo(indice,id2doc,config["rutaXML"]))
                compact+=str(nquery)+"."+str(id2doc[indice]).replace(".json", "")+"\n"
    #Guardamos el resultado compacto        
    with open(config["rutaResultadoQueries"], "w") as archivo:
    # Escribe el texto en el archivo
        archivo.write(compact)          
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de búsqueda: {execution_time} segundos")
    
if __name__ == "__main__":
    run(run_busca)
   
