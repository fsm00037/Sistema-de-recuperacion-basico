from clize import run
from pr1 import etl
from pr2 import stopper
from pr3 import stemmer
from pr4 import diccionario
from pr5 import pesaje

def runIndexador(archivo_config: str ,logs: bool = False):
    """Ejecuta todos los módulos desarrollados en las practicas"""
    etl.etlXML(archivo_config,logs)
    stopper.runStopper(archivo_config,logs)
    stemmer.runStemmer(archivo_config,logs)
    diccionario.runInvertexIndex(archivo_config,logs)
    pesaje.run_pesos(archivo_config,logs)
if __name__ == "__main__":
    run(runIndexador)