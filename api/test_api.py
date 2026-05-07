import requests
import json

BASE = "http://127.0.0.1:5000"

print("=" * 50)
print("TEST 1 — Verificar que la API responde")
r = requests.get(f"{BASE}/health")
print(json.dumps(r.json(), indent=2, ensure_ascii=False))

print("\n" + "=" * 50)
print("TEST 2 — Email de phishing clásico")
payload = {
    "texto": "CONGRATULATIONS! You've won $1000! Click http://claim-prize.com NOW to collect your reward!!!"
}
r = requests.post(f"{BASE}/predecir", json=payload)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))

print("\n" + "=" * 50)
print("TEST 3 — Email legítimo")
payload = {
    "texto": "Hi John, just a reminder about our meeting tomorrow at 3pm. Let me know if you need to reschedule."
}
r = requests.post(f"{BASE}/predecir", json=payload)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))

print("\n" + "=" * 50)
print("TEST 4 — Análisis por lote")
payload = {
    "textos": [
        "FREE entry! Text WIN to 87121 to claim your prize",
        "Please find attached the report for Q3 review",
        "Urgent: Your account will be suspended. Verify now at http://fake-bank.com",
        "Can we schedule a call for next week?"
    ]
}
r = requests.post(f"{BASE}/predecir/lote", json=payload)
print(json.dumps(r.json(), indent=2, ensure_ascii=False))