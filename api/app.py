from flask import Flask, request, jsonify
import pickle
import os
import sys

# Agregamos src al path para importar nuestro preprocesador
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from preprocessor import limpiar_texto

app = Flask(__name__)

# ── Cargar modelo y vectorizador al iniciar la app ──
# Se cargan una sola vez en memoria para responder rápido
BASE = os.path.join(os.path.dirname(__file__), '..', 'models')

with open(os.path.join(BASE, 'modelo_phishing.pkl'), 'rb') as f:
    modelo = pickle.load(f)

with open(os.path.join(BASE, 'vectorizer.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)


# ── Endpoint de salud ──
# Sirve para verificar que la API está corriendo
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "mensaje": "API de detección de phishing activa"
    })


# ── Endpoint principal ──
@app.route('/predecir', methods=['POST'])
def predecir():
    # 1. Validar que llegó un JSON con el campo "texto"
    datos = request.get_json()
    if not datos or 'texto' not in datos:
        return jsonify({
            "error": "Debes enviar JSON con el campo 'texto'"
        }), 400

    texto_original = datos['texto']

    if len(texto_original.strip()) == 0:
        return jsonify({"error": "El texto no puede estar vacío"}), 400

    # 2. Preprocesar exactamente igual que en el entrenamiento
    texto_limpio = limpiar_texto(texto_original)

    # 3. Vectorizar
    vector = vectorizer.transform([texto_limpio])

    # 4. Predecir clase y probabilidad
    prediccion = modelo.predict(vector)[0]
    probabilidades = modelo.predict_proba(vector)[0]

    # 5. Armar respuesta clara
    es_phishing = bool(prediccion == 1)
    confianza = float(probabilidades[1] if es_phishing 
                      else probabilidades[0])

    return jsonify({
        "texto_analizado": texto_original,
        "resultado": "phishing" if es_phishing else "legitimo",
        "es_phishing": es_phishing,
        "confianza": round(confianza, 4),
        "alerta": "⚠️ PELIGRO: posible phishing" if es_phishing 
                  else "✓ Email aparentemente legítimo"
    })


# ── Endpoint de análisis por lote ──
# Analiza varios textos de una sola vez
@app.route('/predecir/lote', methods=['POST'])
def predecir_lote():
    datos = request.get_json()
    if not datos or 'textos' not in datos:
        return jsonify({
            "error": "Debes enviar JSON con el campo 'textos' (lista)"
        }), 400

    textos = datos['textos']
    if not isinstance(textos, list) or len(textos) == 0:
        return jsonify({"error": "'textos' debe ser una lista no vacía"}), 400

    resultados = []
    for texto in textos:
        limpio = limpiar_texto(texto)
        vector = vectorizer.transform([limpio])
        pred = modelo.predict(vector)[0]
        prob = modelo.predict_proba(vector)[0]
        es_phishing = bool(pred == 1)
        resultados.append({
            "texto": texto[:80] + "..." if len(texto) > 80 else texto,
            "resultado": "phishing" if es_phishing else "legitimo",
            "confianza": round(float(prob[1] if es_phishing 
                                     else prob[0]), 4)
        })

    total_phishing = sum(1 for r in resultados 
                         if r['resultado'] == 'phishing')

    return jsonify({
        "total_analizados": len(resultados),
        "phishing_detectados": total_phishing,
        "legitimos": len(resultados) - total_phishing,
        "resultados": resultados
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)