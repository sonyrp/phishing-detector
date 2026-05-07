import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, 
                              confusion_matrix, 
                              accuracy_score)
from preprocessor import limpiar_texto, preparar_labels


def cargar_datos(ruta):
    df = pd.read_csv(ruta, sep='\t', header=None, names=['label', 'text'])
    df['texto_limpio'] = df['text'].apply(limpiar_texto)
    df['label_num'] = preparar_labels(df['label'])
    return df


def entrenar_y_evaluar(df):
    X = df['texto_limpio']
    y = df['label_num']

    # Dividir en entrenamiento (80%) y prueba (20%)
    # random_state=42 garantiza que siempre obtienes la misma división
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    # stratify=y mantiene la proporción spam/ham en ambos conjuntos

    # Vectorizar (solo fit en train, transform en ambos)
    vectorizer = TfidfVectorizer(max_features=3000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    # IMPORTANTE: fit_transform solo en train para no "contaminar"
    # el modelo con información del conjunto de prueba

    # ── Modelo 1: Naive Bayes ──
    print("\n═══ NAIVE BAYES ═══")
    nb = MultinomialNB()
    nb.fit(X_train_vec, y_train)
    evaluar_modelo(nb, X_test_vec, y_test)

    # ── Modelo 2: Random Forest ──
    print("\n═══ RANDOM FOREST ═══")
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train_vec, y_train)
    evaluar_modelo(rf, X_test_vec, y_test)

    # Guardar el mejor modelo (Naive Bayes para este caso)
    guardar_modelo(nb, vectorizer)


def evaluar_modelo(modelo, X_test, y_test):
    predicciones = modelo.predict(X_test)
    
    print(f"Accuracy: {accuracy_score(y_test, predicciones):.4f}")
    print("\nReporte completo:")
    print(classification_report(y_test, predicciones,
                                 target_names=['Legítimo', 'Phishing']))
    print("Matriz de confusión:")
    print(confusion_matrix(y_test, predicciones))


def guardar_modelo(modelo, vectorizer):
    os.makedirs('../models', exist_ok=True)
    
    with open('../models/modelo_phishing.pkl', 'wb') as f:
        pickle.dump(modelo, f)
    
    with open('../models/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("\n✓ Modelo guardado en models/")


if __name__ == "__main__":
    print("Cargando datos...")
    df = cargar_datos('../data/emails.tsv')
    print(f"Dataset: {len(df)} emails")
    entrenar_y_evaluar(df)