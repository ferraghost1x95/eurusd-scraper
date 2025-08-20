import requests
import json
import csv
from datetime import datetime
from pathlib import Path

API_URL = "https://api.frankfurter.app/latest?from=EUR&to=USD"

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
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as ex:
        raise RuntimeError(f"API request failed: {ex}")

    print("DEBUG - response content:", response.text)

    # Frankfurter API returns: {"amount":1,"base":"EUR","date":"2025-08-20","rates":{"USD":1.09}}
    if "rates" not in data or "USD" not in data["rates"]:
        raise RuntimeError("Unexpected response format: missing 'rates/USD'")

    rate = data["rates"]["USD"]
    # Usa la data dell'API se disponibile, altrimenti UTC
    timestamp = data.get("date", datetime.utcnow().isoformat())
    return {"timestamp": timestamp, "eur_usd": rate}

def save_outputs(data):
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # overwrite JSON
    with open(data_dir / "eur_usd_rate.json", "w") as f:
        json.dump(data, f, indent=4)

    # append to CSV
    csv_path = data_dir / "eur_usd_history.csv"
    write_header = not csv_path.exists()
    with open(csv_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "eur_usd"])
        if write_header:
            writer.writeheader()
        writer.writerow(data)

    # overwrite HTML for Netlify
    html_content = HTML_TEMPLATE.format(eur_usd=data["eur_usd"], timestamp=data["timestamp"])
    with open("eurusd.html", "w") as f:
        f.write(html_content)

def main():
    try:
        data = fetch_eur_usd_rate()
        save_outputs(data)
        print(f"Saved rate: {data}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()