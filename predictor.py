"""
predictor.py
Analizza lo storico EUR/USD e predice il cambio per il giorno e il mese successivo.
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import json
from pathlib import Path

DATA_CSV = Path("data/eur_usd_history.csv")
DATA_JSON = Path("data/eur_usd_rate.json")

# Carica lo storico
history = pd.read_csv(DATA_CSV)
history['timestamp'] = pd.to_datetime(history['timestamp'])
history = history.sort_values('timestamp')

# Prepara i dati per la regressione
history['days'] = (history['timestamp'] - history['timestamp'].min()).dt.days
X = history[['days']]
y = history['eur_usd']

# Modello di regressione lineare
model = LinearRegression()
model.fit(X, y)

# Predizione giorno successivo
last_day = history['days'].iloc[-1]
next_day = last_day + 1
pred_next_day = model.predict([[next_day]])[0]

# Predizione mese successivo
next_month = last_day + 30
pred_next_month = model.predict([[next_month]])[0]

# Salva le predizioni
predictions = {
    "next_day": {
        "date": (history['timestamp'].iloc[-1] + timedelta(days=1)).strftime('%Y-%m-%d'),
        "eur_usd": round(pred_next_day, 4)
    },
    "next_month": {
        "date": (history['timestamp'].iloc[-1] + timedelta(days=30)).strftime('%Y-%m-%d'),
        "eur_usd": round(pred_next_month, 4)
    }
}

with open("data/eur_usd_predictions.json", "w") as f:
    json.dump(predictions, f, indent=4)

print("Predizione giorno successivo:", predictions["next_day"])
print("Predizione mese successivo:", predictions["next_month"])
