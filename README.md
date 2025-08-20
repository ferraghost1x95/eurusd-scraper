# eurusd-scraper

Scraper e predittore EUR/USD secondo le best practice vibe coding.

## Struttura
- `scraper.py`: raccoglie e salva i dati.
- `predictor.py`: analizza i dati e predice il cambio per il giorno e il mese successivo.
- `eurusd.html`: visualizza il tasso attuale.
- `data/eur_usd_history.csv`: storico dei cambi.
- `data/eur_usd_rate.json`: ultimo cambio.

## Dipendenze
Vedi `requirements.txt`.

## Utilizzo
1. Installa le dipendenze:
   ```sh
   pip install -r requirements.txt
   ```
2. Esegui lo scraper:
   ```sh
   python scraper.py
   ```
3. Esegui la predizione:
   ```sh
   python predictor.py
   ```

## Riferimenti
- API Frankfurter: https://www.frankfurter.app/
- Modello ML: regressione lineare (scikit-learn)

## Autore
ferraghost1x95
