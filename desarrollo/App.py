from pathlib import Path
from collections import defaultdict
import re, unicodedata
import matplotlib.pyplot as plt
from limpieza_datos import normalizar_texto,preparacion_datos
from TF_IF import vector_de_palabras_totales,TF_IDF
import math

base = Path(r"C:\Users\fjt99\OneDrive\Documentos\Estudioautonomoprogramacion\programación_cientifica\lab1")  

def leer_docs(extension=".txt"):

    carpeta = defaultdict(list)
    for car in base.iterdir():
        nombre_carpeta = car.name
        for c in car.rglob(f"*{extension}"):
        
            try:
                texto = c.read_text(encoding="utf-8")
                texto = normalizar_texto(texto)
            except UnicodeDecodeError:
                texto = c.read_text(encoding="latin-1", errors="ignore")
                texto = normalizar_texto(texto)
            carpeta[nombre_carpeta].append(texto)

    return carpeta
def coseno_tf_idf(diccionario:dict[str, list[str]]):
    
    diccionario_coseno = defaultdict(list)
    for vector_tf_idf in diccionario["consulta"]:
        
        for etiqueta, vector in diccionario.items():
            
            if etiqueta != "consulta":
                
                for vector_pal in vector:
                    
                    operacion = operacion_coseno(vector_tf_idf,vector_pal)
                    diccionario_coseno[etiqueta].append(operacion)
    return diccionario_coseno

    


def operacion_coseno(lista1: list[float], lista2: list[float]):
    
    
    numerador = [x*y for x, y in zip(lista1,lista2)]
    denominador1 = [x**2 for x in lista1]
    denominador2 = [x**2 for x in lista2]
    operacion = sum(numerador) / (math.sqrt(sum(denominador1)) * math.sqrt(sum(denominador2)))
    return operacion

def k_vecinos(diccionario:dict[str, list[str]]):
    lista_doc = []
    lista_cos = []
    for etiqueta, cos in diccionario.items():
        for indice,cosx in enumerate(cos):
            lista_doc.append(etiqueta+str(indice+1))
            lista_cos.append(cosx)
    
    lista_unificada = zip(lista_doc,lista_cos)
    k_vecinos = sorted(lista_unificada, key=lambda x: x[1], reverse=True)
    print("---------------K vecinos mas cercanos--------------------")
    for i in range(3):
        print(k_vecinos[i])

    count = 0
    ranking = {}
    

    for doc, cos in k_vecinos[:3]:
        categoria = doc[:-1]
        
        ranking[categoria] = ranking.get(categoria,0) + 1

    max = 0
    categoria_mayor = ""
    for categoria, conteo in ranking.items():
        if conteo > max:
            max = conteo
            categoria_mayor = categoria
    
    print(f"La consulta es cercana a la categoria: {categoria_mayor}")
        
    


        



def main():
    corpus = leer_docs()
    
    dicc_palabras_unicas_por_texto = preparacion_datos(corpus)
    lista_palabras = vector_de_palabras_totales(dicc_palabras_unicas_por_texto)
    dicc_tf_idf = TF_IDF(lista_palabras,corpus,dicc_palabras_unicas_por_texto)
    print(f"---------vector TF-IDF, para consulta:--------------\n {dicc_tf_idf["consulta"]}")
    dicc_coseno = coseno_tf_idf(dicc_tf_idf)
    k_vecinos(dicc_coseno)


    



if __name__ == "__main__":
    main()
