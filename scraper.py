
"""
scraper.py
Modulo per la raccolta e salvataggio del cambio EUR/USD.
Responsabilità: fetch, salvataggio storico, generazione HTML.
"""
import requests
import json
import csv
from datetime import datetime
from pathlib import Path

API_URL = "https://api.frankfurter.app/latest?from=EUR&to=USD"
DATA_DIR = Path("data")
HTML_PATH = Path("eurusd.html")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>EUR/USD Rate</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f7f7f7; color: #222; }}
        .container {{ max-width: 400px; margin: 60px auto; background: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 2px 8px #ccc; }}
        h1 {{ font-size: 2em; margin-bottom: 0.5em; }}
        .rate {{ font-size: 2em; color: #0077ff; margin-bottom: 1em; }}
        .timestamp {{ color: #888; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class=\"container\">
        <h1>EUR/USD Exchange Rate</h1>
        <div class=\"rate\">{eur_usd}</div>
        <div class=\"timestamp\">Updated: {timestamp}</div>
    </div>
</body>
</html>
"""

def fetch_eur_usd_rate():
    """
    Recupera il cambio EUR/USD dalla Frankfurter API.
    Returns: dict con 'timestamp' e 'eur_usd'.
    """
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as ex:
        raise RuntimeError(f"API request failed: {ex}")

    # Frankfurter API returns: {"amount":1,"base":"EUR","date":"2025-08-20","rates":{"USD":1.09}}
    if "rates" not in data or "USD" not in data["rates"]:
        raise RuntimeError("Unexpected response format: missing 'rates/USD'")

    rate = data["rates"]["USD"]
    timestamp = data.get("date", datetime.utcnow().isoformat())
    return {"timestamp": timestamp, "eur_usd": rate}

def save_json(data, path):
    """Salva i dati in formato JSON."""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def append_csv(data, path):
    """Aggiunge una riga allo storico CSV."""
    write_header = not path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "eur_usd"])
        if write_header:
            writer.writeheader()
        writer.writerow(data)

def save_html(data, path):
    """Genera la pagina HTML con il cambio attuale e le predizioni."""
    # Carica predizioni se disponibili
    predictions_path = DATA_DIR / "eur_usd_predictions.json"
    pred_html = ""
    if predictions_path.exists():
        with open(predictions_path) as f:
            preds = json.load(f)
        pred_html = f"""
        <div class='prediction'>
            <h2>Predizioni</h2>
            <div>Domani ({preds['next_day']['date']}): <b>{preds['next_day']['eur_usd']}</b></div>
            <div>Tra un mese ({preds['next_month']['date']}): <b>{preds['next_month']['eur_usd']}</b></div>
        </div>
        """
    html_content = HTML_TEMPLATE.format(eur_usd=data["eur_usd"], timestamp=data["timestamp"])
    # Inserisco le predizioni prima della chiusura del container
    html_content = html_content.replace("</div>\n</body>", f"{pred_html}</div>\n</body>")
    with open(path, "w") as f:
        f.write(html_content)

def main():
    """Esegue la raccolta e il salvataggio dei dati."""
    DATA_DIR.mkdir(exist_ok=True)
    try:
        data = fetch_eur_usd_rate()
        save_json(data, DATA_DIR / "eur_usd_rate.json")
        append_csv(data, DATA_DIR / "eur_usd_history.csv")
        save_html(data, HTML_PATH)
        print(f"Saved rate: {data}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()