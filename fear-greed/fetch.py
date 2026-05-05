"""
Fetch Alternative.me Crypto Fear & Greed index and append to CSV.
Free public API, no key required.
"""
from __future__ import annotations

import csv
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "data" / "fear_greed.csv"
URL = "https://api.alternative.me/fng/?limit=1"


def main() -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(URL, headers={"User-Agent": "daily-quant-log"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.loads(r.read())
    item = payload["data"][0]
    value = int(item["value"])
    classification = item["value_classification"]
    ts = int(item["timestamp"])
    date = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")
    fetched_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    is_new = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["fetched_at_utc", "date", "value", "classification"])
        w.writerow([fetched_at, date, value, classification])

    print(f"{date}: {value} ({classification})")


if __name__ == "__main__":
    main()
