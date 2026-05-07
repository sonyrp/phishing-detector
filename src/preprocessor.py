import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Cargamos herramientas de NLTK
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


def limpiar_texto(texto):
    """
    Toma un email crudo y lo convierte en texto limpio y normalizado.
    Pasos: minúsculas → sin URLs → sin números → sin puntuación → sin stopwords → lematizar
    """

    # 1. Todo a minúsculas
    texto = texto.lower()

    # 2. Eliminar URLs (http://... o www....)
    texto = re.sub(r'http\S+|www\S+', 'url', texto)

    # 3. Reemplazar números por la palabra 'numero'
    texto = re.sub(r'\d+', 'numero', texto)

    # 4. Eliminar puntuación
    texto = texto.translate(str.maketrans('', '', string.punctuation))

    # 5. Separar en palabras (tokenizar)
    palabras = texto.split()

    # 6. Eliminar stopwords y lematizar cada palabra
    palabras = [
        lemmatizer.lemmatize(palabra)
        for palabra in palabras
        if palabra not in stop_words and len(palabra) > 2
    ]

    # 7. Volver a unir como texto limpio
    return ' '.join(palabras)


def preparar_labels(serie):
    """Convierte 'ham'/'spam' en 0/1 para el modelo"""
    return serie.map({'ham': 0, 'spam': 1})