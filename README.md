#  Phishing Detector con NLP y Machine Learning

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-green)
![ML](https://img.shields.io/badge/Machine%20Learning-Scikit--learn-orange)
![NLP](https://img.shields.io/badge/NLP-NLTK-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

Sistema de ciberseguridad desarrollado con Python que detecta emails y mensajes de phishing utilizando técnicas de Procesamiento de Lenguaje Natural (NLP) y Machine Learning.

El proyecto analiza texto sospechoso, identifica patrones comunes de fraude y clasifica automáticamente si un mensaje es legítimo o malicioso. Además, expone una API REST construida con Flask para integrarse fácilmente en otros sistemas o aplicaciones.

---

#  Características

-  Detección automática de phishing y spam
-  Procesamiento de texto con NLP
-  Clasificación mediante Machine Learning
-  API REST desarrollada con Flask
-  Evaluación del modelo con métricas reales
-  Pipeline de limpieza y preprocesamiento
-  Soporte para análisis individual y por lotes

---

#  Resultados del modelo

| Métrica | Resultado |
|---|---|
| Accuracy | 98.2% |
| Precision (Phishing) | 98% |
| Recall (Phishing) | 90% |
| F1-Score | 94% |

Estas métricas muestran que el modelo logra identificar correctamente la mayoría de intentos de phishing manteniendo una alta precisión y reduciendo falsos positivos.

---

#  ¿Cómo funciona?

El sistema sigue un pipeline de procesamiento de datos:

```text
Texto → Limpieza → Tokenización → Vectorización → Modelo ML → Clasificación

## Arquitectura del sistema

El detector de phishing sigue un pipeline de procesamiento de lenguaje natural y machine learning:

### 1. Preprocesamiento de texto
Se realiza limpieza y normalización del contenido:
- eliminación de stopwords
- lematización
- normalización de URLs
- eliminación de caracteres especiales y números

### 2. Vectorización TF-IDF
Los emails se transforman en vectores numéricos de aproximadamente 3000 dimensiones usando TF-IDF, permitiendo que el modelo interprete patrones lingüísticos matemáticamente.

### 3. Clasificación con Machine Learning
Se utiliza un modelo **Multinomial Naive Bayes** entrenado con más de **5572 emails reales** clasificados entre legítimos y phishing.

### 4. API REST
El modelo se expone mediante una API REST desarrollada con Flask para facilitar integración con otros sistemas y aplicaciones.

---

# Instalación y uso

## Requisitos

- Python 3.10+
- pip

---

## Configuración del proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/phishing-detector.git

# 2. Entrar al proyecto
cd phishing-detector

# 3. Crear entorno virtual
python -m venv venv

# 4. Activar entorno virtual

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Descargar dataset
python download_data.py

# 7. Entrenar el modelo
cd src
python train_model.py

# 8. Iniciar la API
cd ../api
python app.py
```

---

#  Uso de la API

## Analizar un email

```bash
curl -X POST http://localhost:5000/predecir \
  -H "Content-Type: application/json" \
  -d '{"texto": "CONGRATULATIONS! You won a prize! Click now!"}'
```

---

##  Respuesta esperada

```json
{
  "resultado": "phishing",
  "es_phishing": true,
  "confianza": 0.9823,
  "alerta": "PELIGRO: posible phishing"
}
```

---

#  Estructura del proyecto

phishing-detector/
├── api/
│   ├── app.py          ← API REST con Flask
│   └── test_api.py     ← Tests de los endpoints
├── src/
│   ├── preprocessor.py ← Módulo NLP reutilizable
│   └── train_model.py  ← Entrenamiento y evaluación
├── notebooks/
│   ├── 01_exploracion.ipynb   ← Análisis exploratorio
│   └── 02_evaluacion.ipynb    ← Métricas y gráficas
├── data/
│   ├── confusion_matrix.png
│   └── distribucion.png
├── models/             ← Modelos entrenados (generados localmente)
├── download_data.py
├── requirements.txt
└── README.md

## Stack tecnológico

- **NLP**: NLTK (tokenización, lematización, stopwords)
- **ML**: Scikit-learn (TF-IDF, Naive Bayes, Random Forest)
- **API**: Flask
- **Análisis**: Pandas, Matplotlib, Seaborn
- **Dataset**: SMS Spam Collection (UCI ML Repository)

##  Mejoras futuras

- [ ] Reentrenamiento automático con nuevos datos
- [ ] Soporte para análisis de URLs en tiempo real
- [ ] Dashboard web para visualizar predicciones
- [ ] Dockerizar la aplicación
- [ ] Integración con Gmail API

## Autor

**Sonia Marcela Restrepo Perez** — [LinkedIn](www.linkedin.com/in/sonia-marcela-restrepo-perez-83b893289) · 
[GitHub](https://github.com/sonyrp)