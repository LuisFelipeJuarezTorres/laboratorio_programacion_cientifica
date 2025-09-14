from pathlib import Path
from collections import defaultdict
import re, unicodedata
import matplotlib.pyplot as plt

base = Path(r"C:\Users\fjt99\OneDrive\Documentos\Estudioautonomoprogramacion\programación_cientifica\lab1")  

subcarpetas = [p.name for p in base.iterdir() if p.is_dir()]

STOPWORDS_ES = {
    "de","la","que","el","en","y","a","los","del","se","las","por","un","para","con",
    "no","una","su","al","lo","como","más","pero","sus","le","ya","o","este","sí",
    "porque","esta","entre","cuando","muy","sin","sobre","también","me","hasta","hay",
    "donde","quien","desde","todo","nos","durante","todos","uno","les","ni","contra",
    "otros","ese","eso","ante","ellos","e","esto","mí","antes","algunos","qué","unos",
    "yo","otro","otras","otra","él","tanto","esa","estos","mucho","quienes","nada",
    "muchos","cual","poco","ella","estar","estas","algunas","algo","nosotros","mi",
    "mis","tú","te","ti","tu","tus","ellas","nosotras","vosostros","vosostras","os",
    "mío","mía","míos","mías","tuyo","tuya","tuyos","tuyas","suyo","suya","suyos",
    "suyas","nuestro","nuestra","nuestros","nuestras","vuestro","vuestra","vuestros",
    "vuestras","esos","esas","estoy","estás","está","estamos","estáis","están","esté",
    "estés","estemos","estéis","estén","estaré","estarás","estará","estaremos",
    "estaréis","estarán"  
}


def leer_docs(extension=".txt"):
    carpeta = defaultdict(list)
    for car in base.iterdir():
        
        if car.is_dir():
            etiqueta = car.name
            for c in car.rglob(f"*{extension}"):
                try:
                    texto = c.read_text(encoding="utf-8")

                except UnicodeDecodeError:
                    texto = c.read_text(encoding="latin-1", errors="ignore")
                carpeta[etiqueta].append(texto)
    return carpeta


def normalizar_texto(texto: str):
    t = texto.lower()

    t = t.replace("ñ", "<<enye>>")

    t = unicodedata.normalize("NFD", t)

    t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")

    t = t.replace("<<enye>>", "ñ")

    t = re.sub(r"[^\w\s]", " ", t, flags=re.UNICODE)
    
    t = re.sub(r"\s+", " ", t).strip()
    
    return t
def get_Tokens(texto: str):
    texto = normalizar_texto(texto)
    palabras_unicas = []
    
    for pal in texto.split():
        if pal not in palabras_unicas and pal not in STOPWORDS_ES:
            palabras_unicas.append(pal)
    
    return palabras_unicas

def preparacion_datos(corpus: dict[str, list[str]]):
    palabras_por_etiqueta = defaultdict(list)
    
    for etiqueta, texto in corpus.items():
        for text in texto:
            
            tokens = get_Tokens(text)
            palabras_por_etiqueta[etiqueta].append(tokens)

    return palabras_por_etiqueta


'''
l = [1,2,3,4,5]
lista = [x**2 for x in l]
print(lista)

#recursión vs programación dinamica
#estudiar fibonnaci-su arbol-como aplicar programación dinámica 
listax = [(n^2+1) for n in range(1,31) if n%2 == 0 or n%3==0]

secuences = ["ASAIJSI", "OSOWDJOJDJ", "ASASOA", "SSSWAAA"]

lista_adn = [x for x in secuences if "A" in x]

numbers = ["04588484883", "9493882292", "6604588888"]
lista_verona = [x for x in numbers if x.startswith("045")]

print(lista_verona)

atoms = ["SER A 96 77.253 20.522 75.007", "VAL A 97 76.006 22.304 71.921"]
lista = [ float(i) for x in atoms for i in x.split()[3:]]
print(lista)
'''