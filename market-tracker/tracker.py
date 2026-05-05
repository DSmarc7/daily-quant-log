"""
Daily market tracker.

Pulls latest closing prices for indices, crypto, and FX, and appends rows to
per-category CSVs. Also writes a fresh LATEST.md summary at the repo root.

Designed to be run by GitHub Actions every day, but works locally too.
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)

ASSETS: dict[str, dict[str, str]] = {
    "indices": {
        "SP500": "^GSPC",
        "CAC40": "^FCHI",
        "NIKKEI": "^N225",
        "EUROSTOXX50": "^STOXX50E",
        "FTSE100": "^FTSE",
    },
    "crypto": {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "SOL": "SOL-USD",
    },
    "fx": {
        "EURUSD": "EURUSD=X",
        "USDJPY": "USDJPY=X",
        "GBPUSD": "GBPUSD=X",
        "EURJPY": "EURJPY=X",
    },
}


def fetch_latest(ticker: str) -> dict | None:
    """Return latest close, day-over-day % change, and volume."""
    try:
        hist = yf.Ticker(ticker).history(period="5d", interval="1d")
        if hist.empty:
            return None
        latest = hist.iloc[-1]
        prev = hist.iloc[-2] if len(hist) >= 2 else latest
        close = float(latest["Close"])
        prev_close = float(prev["Close"])
        change_pct = ((close - prev_close) / prev_close * 100) if prev_close else 0.0
        volume = latest.get("Volume", 0)
        # NaN guard
        volume = int(volume) if volume == volume else 0  # noqa: PLR0124
        return {
            "date": latest.name.strftime("%Y-%m-%d"),
            "close": round(close, 4),
            "change_pct": round(change_pct, 3),
            "volume": volume,
        }
    except Exception as exc:  # noqa: BLE001
        print(f"[error] {ticker}: {exc}")
        return None


def append_row(csv_path: Path, name: str, ticker: str, info: dict) -> None:
    is_new = not csv_path.exists()
    with csv_path.open("a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(
                ["fetched_at_utc", "date", "name", "ticker", "close", "change_pct", "volume"]
            )
        w.writerow(
            [
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
                info["date"],
                name,
                ticker,
                info["close"],
                info["change_pct"],
                info["volume"],
            ]
        )


def main() -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"# Market snapshot — {today} (UTC)\n"]

    for category, assets in ASSETS.items():
        csv_path = DATA_DIR / f"{category}.csv"
        lines.append(f"\n## {category.upper()}\n")
        lines.append("| Asset | Date | Close | Change |")
        lines.append("|---|---|---|---|")
        for name, ticker in assets.items():
            info = fetch_latest(ticker)
            if info is None:
                lines.append(f"| {name} | n/a | n/a | n/a |")
                continue
            append_row(csv_path, name, ticker, info)
            arrow = "🟢" if info["change_pct"] >= 0 else "🔴"
            lines.append(
                f"| {name} | {info['date']} | {info['close']} | {arrow} {info['change_pct']:+.2f}% |"
            )

    summary_path = REPO_ROOT / "LATEST.md"
    summary_path.write_text("\n".join(lines) + "\n")
    print(f"Wrote {summary_path}")


if __name__ == "__main__":
    main()
