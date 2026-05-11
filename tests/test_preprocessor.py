import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from preprocessor import limpiar_texto, preparar_labels
import pandas as pd


def test_limpieza_basica():
    """El texto debe quedar en minúsculas sin puntuación"""
    resultado = limpiar_texto("Hello World!!!")
    assert resultado == resultado.lower()
    assert "!" not in resultado


def test_urls_reemplazadas():
    """Las URLs deben convertirse en la palabra 'url'"""
    resultado = limpiar_texto("Visit http://fake-site.com now")
    assert "url" in resultado
    assert "http" not in resultado


def test_stopwords_eliminadas():
    """Palabras vacías como 'the' no deben aparecer"""
    resultado = limpiar_texto("the quick brown fox")
    assert "the" not in resultado.split()


def test_texto_vacio():
    """Texto vacío debe retornar string vacío sin errores"""
    resultado = limpiar_texto("")
    assert isinstance(resultado, str)


def test_numeros_reemplazados():
    """Los números deben convertirse en la palabra 'numero'"""
    resultado = limpiar_texto("Call 123456789 now")
    assert "numero" in resultado
    assert "123456789" not in resultado


def test_preparar_labels():
    """ham debe ser 0, spam debe ser 1"""
    serie = pd.Series(['ham', 'spam', 'ham', 'spam'])
    resultado = preparar_labels(serie)
    assert list(resultado) == [0, 1, 0, 1]