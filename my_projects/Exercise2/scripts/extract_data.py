#!/usr/bin/env python3
import os, json, sys, time, random
import requests
import pandas as pd
from io import StringIO

URLS = [
    # primär desktop
    "https://sv.wikipedia.org/wiki/Lista_%C3%B6ver_Pok%C3%A9mon",
    # mobil
    "https://sv.m.wikipedia.org/wiki/Lista_%C3%B6ver_Pok%C3%A9mon",
    # printable
    "https://sv.wikipedia.org/w/index.php?title=Lista_%C3%B6ver_Pok%C3%A9mon&printable=yes"
]

UAS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
]

BASE_HEADERS = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language":"sv-SE,sv;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer":"https://sv.wikipedia.org/"
}

def fetch_html_with_fallback(urls, retries_per_url=2, wait=1.0) -> str:
    s = requests.Session()
    last_status = None
    for url in urls:
        for attempt in range(retries_per_url):
            headers = dict(BASE_HEADERS)
            headers["User-Agent"] = random.choice(UAS)
            try:
                r = s.get(url, headers=headers, timeout=20, allow_redirects=True)
                last_status = r.status_code
                if r.status_code == 200 and "text/html" in r.headers.get("content-type",""):
                    return r.text
            except requests.RequestException:
                pass
            time.sleep(wait)
    raise RuntimeError(f"HTTP {last_status} från alla URL:er")

def parse_gen1(html: str) -> dict:
    tables = pd.read_html(StringIO(html), header=0)
    # hitta tabeller som har Pokédex + Engelskt namn
    candidates = []
    for t in tables:
        cols = [str(c).lower() for c in t.columns]
        if any(("pokédex" in c) or ("pokedex" in c) for c in cols) and \
           any((("engelskt" in c) or ("engelska" in c)) and ("namn" in c) for c in cols):
            candidates.append(t)
    if not candidates:
        raise RuntimeError("Hittade ingen tabell med Pokédex + Engelskt namn.")
    df = pd.concat(candidates, ignore_index=True)

    # normalisera kolumnnamn
    rename = {}
    for c in df.columns:
        lc = str(c).lower()
        if ("pokédex" in lc) or ("pokedex" in lc):
            rename[c] = "dex"
        if (("engelskt" in lc) or ("engelska" in lc)) and ("namn" in lc):
            rename[c] = "name_en"
    df = df.rename(columns=rename)
    df = df[[c for c in df.columns if c in ("dex", "name_en")]].dropna()

    def parse_dex(x):
        s = "".join(ch for ch in str(x) if ch.isdigit())
        return int(s) if s else None

    df["dex"] = df["dex"].map(parse_dex)
    df = df.dropna(subset=["dex"]).astype({"dex": int})
    df = df[(df["dex"] >= 1) & (df["dex"] <= 151)]

    def clean_name(s: str) -> str:
        s = str(s).strip()
        return s.split("[")[0].strip()

    df["name_en"] = df["name_en"].map(clean_name)
    df = df.sort_values("dex")
    mapping = {str(int(row.dex)): str(row.name_en) for row in df.itertuples()}

    # sanity check
    if mapping.get("1","").lower() != "bulbasaur" or mapping.get("151","").lower() != "mew":
        raise RuntimeError("Sanity check misslyckades (ville ha Bulbasaur #1 och Mew #151).")
    return mapping

def main():
    html = fetch_html_with_fallback(URLS)
    mapping = parse_gen1(html)

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    out_dir = os.path.join(root, "pokedata")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "pokelist.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Sparade {len(mapping)} pokémon till {out_path}")
    first10 = {k: mapping[k] for k in sorted(mapping, key=lambda x: int(x))[:10]}
    print("Första 10:", first10)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(f"[Fel] {e}\n")
        sys.exit(1)
