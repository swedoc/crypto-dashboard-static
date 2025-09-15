import os
import datetime
from pathlib import Path
import requests

BASE = os.getenv("DATA_BASE_URL", "").rstrip("/")


def fetch_json(url: str, timeout: int = 30):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


def fetch_binance_btcusd(timeout: int = 20) -> float | None:
    """Hämtar BTCUSDT-pris i USD från Binance."""
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        data = requests.get(url, timeout=timeout).json()
        return float(data["price"])
    except Exception:
        return None


def fmt_num(x, decimals=3):
    if x is None:
        return "—"
    try:
        return f"{float(x):.{decimals}f}".rstrip("0").rstrip(".")
    except Exception:
        return str(x)


def fmt_price0(x):
    if x is None:
        return "—"
    try:
        return f"{float(x):,.0f}"
    except Exception:
        return str(x)


def main():
    # Hämta dina egna endpoints
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

    # BTC-pris från BINANCE (endast)
    btc_price_usd = fetch_binance_btcusd()

    # Fält ur dina JSON
    s_signal = signal.get("signal") if isinstance(signal, dict) else None
    s_score  = signal.get("score")  if isinstance(signal, dict) else None
    s_pfi    = signal.get("pfi")    if isinstance(signal, dict) else None
    s_price  = signal.get("price")  if isinstance(signal, dict) else None

    p_status = pgl.get("status") if isinstance(pgl, dict) else None
    p_score  = pgl.get("score")  if isinstance(pgl, dict) else None
    p_price  = pgl.get("price")  if isinstance(pgl, dict) else None

    # Text för “BTC Price (Binance)”
    if btc_price_usd:
        million = btc_price_usd / 1_000_000
        sats_per_usd = int(100_000_000 / btc_price_usd)
        signal_price_block = f"{million:.3f} million USD<br/>{sats_per_usd} sats/USD"
    else:
        signal_price_block = "—"

    updated = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Ersättare
    repl = {
        "{{ UPDATED_TS }}": updated,
        "{{ SIGNAL_SIGNAL }}": s_signal if s_signal is not None else "—",
        "{{ SIGNAL_SCORE }}": fmt_num(s_score),
        "{{ SIGNAL_PFI }}": fmt_num(s_pfi),
        "{{ SIGNAL_PRICE }}": signal_price_block,  # används i BTC Price-kortet
        "{{ PGL_STATUS }}": p_status if p_status is not None else "—",
        "{{ PGL_SCORE }}": str(p_score) if p_score is not None else "—",
        "{{ PGL_PRICE }}": fmt_price0(p_price),
        # Om någonstans i layouten dyker dessa upp:
        "{{PRICE_MILLION}}": f"{(btc_price_usd/1_000_000):.3f}" if btc_price_usd else "—",
        "{{PRICE_SATS}}": f"{int(100_000_000 / btc_price_usd)}" if btc_price_usd else "—",
    }

    html = Path("static_layout.html").read_text(encoding="utf-8")
    for k, v in repl.items():
        html = html.replace(k, v)

    outdir = Path("public")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "index.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
