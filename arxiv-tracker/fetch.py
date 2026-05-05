"""
Fetch latest arXiv q-fin papers and append to a daily markdown file.
"""
from __future__ import annotations

import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARXIV_URL = (
    "http://export.arxiv.org/api/query?"
    "search_query=cat:q-fin.*"
    "&sortBy=submittedDate&sortOrder=descending&max_results=10"
)
NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch() -> list[dict]:
    req = urllib.request.Request(ARXIV_URL, headers={"User-Agent": "daily-quant-log"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    root = ET.fromstring(data)
    out = []
    for entry in root.findall("a:entry", NS):
        title = (entry.findtext("a:title", default="", namespaces=NS) or "").strip().replace("\n", " ")
        summary = (entry.findtext("a:summary", default="", namespaces=NS) or "").strip().replace("\n", " ")
        link = (entry.findtext("a:id", default="", namespaces=NS) or "").strip()
        published = (entry.findtext("a:published", default="", namespaces=NS) or "").strip()
        authors = [
            (a.findtext("a:name", default="", namespaces=NS) or "").strip()
            for a in entry.findall("a:author", NS)
        ]
        out.append({
            "title": title,
            "summary": summary[:400] + ("..." if len(summary) > 400 else ""),
            "link": link,
            "published": published,
            "authors": ", ".join(authors[:4]) + (" et al." if len(authors) > 4 else ""),
        })
    return out


def main() -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    year = today[:4]
    month = today[5:7]
    out_dir = ROOT / "papers" / year / month
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{today}.md"

    papers = fetch()
    lines = [f"# arXiv q-fin — {today}\n", f"_Fetched at {datetime.now(timezone.utc).isoformat(timespec='seconds')}_\n"]
    for i, p in enumerate(papers, 1):
        lines.append(f"\n## {i}. {p['title']}\n")
        lines.append(f"- **Authors:** {p['authors']}")
        lines.append(f"- **Published:** {p['published']}")
        lines.append(f"- **Link:** {p['link']}")
        lines.append(f"\n> {p['summary']}\n")

    out_file.write_text("\n".join(lines) + "\n")
    print(f"Wrote {out_file} ({len(papers)} papers)")


if __name__ == "__main__":
    main()
