# market-tracker

Automated daily snapshot of indices, crypto, and FX. Runs via GitHub Actions every day at ~22:30 UTC (after US close, late evening Paris time) and appends one row per asset to the CSVs in `data/`.

## What's tracked

- **Indices:** S&P 500, CAC 40, Nikkei 225, Euro Stoxx 50, FTSE 100
- **Crypto:** BTC, ETH, SOL (USD pairs)
- **FX:** EUR/USD, USD/JPY, GBP/USD, EUR/JPY

Easy to add more — edit the `ASSETS` dict in `tracker.py`.

## Data source

[`yfinance`](https://github.com/ranaroussi/yfinance) — Yahoo Finance scraper, free, no API key. Coverage is good for the basics; for production-grade data you'd want a paid feed (Refinitiv, Bloomberg, Polygon, etc.) but for a daily log this is fine.

## Output

- `data/indices.csv`, `data/crypto.csv`, `data/fx.csv` — append-only history
- `../LATEST.md` at the repo root — fresh summary table each run

## Notes on weekends / holidays

Equity markets and FX are closed on weekends, so the script will append the same Friday close on Saturday/Sunday with `change_pct = 0`. Crypto runs 24/7 so it always has a fresh value. If you want to skip weekends entirely for indices/FX, gate the fetch on `datetime.utcnow().weekday() < 5`.
