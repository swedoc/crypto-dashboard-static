import os
import json
import datetime
from pathlib import Path

import requests

BASE = os.getenv("DATA_BASE_URL", "").rstrip("/")


def fetch_json(url: str, timeout: int = 30):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def fmt_num(x, decimals=3):
    try:
        if x is None:
            return "—"
        if isinstance(x, (int, float)):
            return f"{x:.{decimals}f}".rstrip("0").rstrip(".")
        return str(x)
    except Exception:
        return str(x)


def fmt_price(x):
    try:
        if x is None:
            return "—"
        return f"{float(x):,.0f}"
    except Exception:
        return str(x)


def main():
    # 1) Hämta data
    if not BASE:
        signal = {"error": "DATA_BASE_URL not set"}
        pgl = {"error": "DATA_BASE_URL not set"}
    else:
        try:
            signal = fetch_json(f"{BASE}/api/signal")
        except Exception as e:
            signal = {"error": str(e)}
        try:
            pgl = fetch_json(f"{BASE}/api/pgl")
        except Exception as e:
            pgl = {"error": str(e)}

    # 2) Plocka ut fält (tål att fält saknas)
    s_signal = (signal.get("signal") if isinstance(signal, dict) else None) if signal else None
    s_score  = (signal.get("score")  if isinstance(signal, dict) else None) if signal else None
    s_pfi    = (signal.get("pfi")    if isinstance(signal, dict) else None) if signal else None
    s_price  = (signal.get("price")  if isinstance(signal, dict) else None) if signal else None

    p_status = (pgl.get("status") if isinstance(pgl, dict) else None) if pgl else None
    p_score  = (pgl.get("score")  if isinstance(pgl, dict) else None) if pgl else None
    p_price  = (pgl.get("price")  if isinstance(pgl, dict) else None) if pgl else None

    # 3) Förbered ersättningar
    updated = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    repl = {
        "{{ UPDATED_TS }}": updated,
        "{{ SIGNAL_SIGNAL }}": str(s_signal) if s_signal is not None else "—",
        "{{ SIGNAL_SCORE }}": fmt_num(s_score),
        "{{ SIGNAL_PFI }}": fmt_num(s_pfi),
        "{{ SIGNAL_PRICE }}": fmt_price(s_price),

        "{{ PGL_STATUS }}": str(p_status) if p_status is not None else "—",
        "{{ PGL_SCORE }}": str(p_score) if p_score is not None else "—",
        "{{ PGL_PRICE }}": fmt_price(p_price),
    }

    # 4) Läs din layout och ersätt markörer
    tpl_path = Path("static_layout.html")
    html = tpl_path.read_text(encoding="utf-8")

    for k, v in repl.items():
        html = html.replace(k, v)

    # 5) Skriv ut som public/index.html (Pages plockar härifrån)
    outdir = Path("public")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
