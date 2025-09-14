from collections import defaultdict
import numpy as np
import math
def vector_de_palabras_totales(bag: dict[str, list[str]]):
    lista_pal_totales = []
    for _, lista_palabras in bag.items():
        for palabr in lista_palabras:
            for pal in palabr:
                if pal not in lista_pal_totales:
                    lista_pal_totales.append(pal)
    
    return lista_pal_totales

def TF_IDF(lista_tol: list[str], corpus: dict[str, list[str]],dicc_pal_uni__texto:dict[str, list[str]]):
    
    diccionario_num_pal = defaultdict(list)
    #cantidad de veces que aparece cada palabra en el documento X
    for doc, palabras in corpus.items():
        for palabra in palabras:
            lista_aux = [0] * len(lista_tol)
            for pala in palabra.split():
                if pala in lista_tol:
                    index = lista_tol.index(pala)
                    lista_aux[index] += 1
            diccionario_num_pal[doc].append(lista_aux)
   
    #vector TF---> número de veces que aparece el termino t en el documento d / Número total de términos en el documento d
    diccionario_TF = defaultdict(list)
    for doc, vector in diccionario_num_pal.items():
        for vector_pal in vector:
            lista_aux2 = [0] * len(lista_tol)
            num_palabras_totales_documento = sum(vector_pal)
            
            for indice,palabra_frecuencia in enumerate(vector_pal):
                lista_aux2[indice] = palabra_frecuencia/num_palabras_totales_documento
            diccionario_TF[doc].append(lista_aux2)
    #vector IDF--->
    diccionario_IDF = defaultdict(list)
    numero_documentos = len(dicc_pal_uni__texto.values())
    lista_IDF = [0] * len(lista_tol)
    
    for indice,palabra in enumerate(lista_tol):
 
        num_doc_pal = num_pal_doc(dicc_pal_uni__texto,palabra)
        operacion = math.log10(numero_documentos/(1+num_doc_pal))
        lista_IDF[indice] = operacion
   
    #vector TF_IDF
    diccionario_TF_IDF = defaultdict(list)
    for etiqueta, tf in diccionario_TF.items():
        for palabras_tf in tf:
            operacion_lista = [x*y for x, y in zip(palabras_tf,lista_IDF)]
            diccionario_TF_IDF[etiqueta].append(operacion_lista)
    
    return diccionario_TF_IDF

    
        
def num_pal_doc(dicc_pal_uni__texto:dict[str, list[str]], palabra:str):
    num_doc = 0
    for etiqueta, palabras in dicc_pal_uni__texto.items():
        if palabra in palabras:
            num_doc += 1
    return num_doc

        



        
    
    

    


