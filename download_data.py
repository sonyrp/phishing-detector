import urllib.request
import os

# Crear carpeta data si no existe
os.makedirs("data", exist_ok=True)

# Dataset de spam/phishing de emails
url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
destino = "data/emails.tsv"

print("Descargando dataset...")
urllib.request.urlretrieve(url, destino)
print(f"Guardado en {destino}")