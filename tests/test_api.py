import sys
import os
import pickle
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))


# Solo correr tests de API si el modelo existe
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'modelo_phishing.pkl')
modelo_existe = os.path.exists(MODEL_PATH)


@pytest.mark.skipif(not modelo_existe, reason="Modelo no entrenado aún")
def test_endpoint_health(client):
    """El endpoint /health debe responder 200"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


@pytest.mark.skipif(not modelo_existe, reason="Modelo no entrenado aún")
def test_predecir_phishing(client):
    """Email de phishing clásico debe detectarse correctamente"""
    payload = {"texto": "FREE WINNER! Click http://prize.com to claim $1000 NOW!!!"}
    response = client.post('/predecir', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert 'resultado' in data
    assert 'confianza' in data
    assert data['es_phishing'] == True


@pytest.mark.skipif(not modelo_existe, reason="Modelo no entrenado aún")
def test_predecir_sin_texto(client):
    """Request sin campo 'texto' debe retornar error 400"""
    response = client.post('/predecir', json={"otro_campo": "valor"})
    assert response.status_code == 400


@pytest.mark.skipif(not modelo_existe, reason="Modelo no entrenado aún")
def test_predecir_lote(client):
    """El endpoint de lote debe retornar el conteo correcto"""
    payload = {"textos": ["Hello friend", "WIN FREE PRIZE NOW"]}
    response = client.post('/predecir/lote', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_analizados'] == 2


@pytest.fixture
def client():
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client