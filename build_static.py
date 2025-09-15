import os
import datetime
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Bas-URL till din befintliga backend (Render eller liknande), sätts i GitHub repo variables
BASE = os.getenv("DATA_BASE_URL", "").rstrip("/")

def fetch_json(url: str, timeout: int = 30):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()

def main():
    # Hämta data från dina två endpoints
    signal = {"error": "DATA_BASE_URL not set"} if not BASE else None
    pgl = {"error": "DATA_BASE_URL not set"} if not BASE else None

    if BASE:
        try:
            signal = fetch_json(f"{BASE}/api/signal")
        except Exception as e:
            signal = {"error": str(e)}
        try:
            pgl = fetch_json(f"{BASE}/api/pgl")
        except Exception as e:
            pgl = {"error": str(e)}

    # Tidsstämpel i UTC
    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Rendera HTML från template.html (ligger i repo-roten)
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
    )
    tpl = env.get_template("template.html")
    html = tpl.render(signal=signal, pgl=pgl, timestamp=timestamp)

    # Skriv till public/index.html (Actions publicerar denna mapp)
    outdir = Path("public")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "index.html").write_text(html, encoding="utf-8")

if __name__ == "__main__":
    main()
