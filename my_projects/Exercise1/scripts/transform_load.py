#!/usr/bin/env python3
import os
import sys
import json
import glob
from datetime import datetime
from pathlib import Path
import pandas as pd

# --- KONSTANTER ---
ROOT = Path(__file__).resolve().parent.parent  # .../Exercise2
BELT_DIR = ROOT / "pokedata" / "pokebelt"
OBS_DIR = ROOT / "pokedata" / "observations"

def transform(belt_dir: Path) -> pd.DataFrame:
    """
    Läser PokeAPI 'pokemon-species' JSON-filer i pokebelt/ och returnerar en DataFrame
    med kolumnerna: pokemon, happiness.
    """
    rows = []
    files = sorted(glob.glob(str(belt_dir / "*.json")))
    if not files:
        raise RuntimeError(f"Hittade inga JSON-filer i {belt_dir}. Kör b) först för att fylla pokebelt.")

    for fp in files:
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)

        # Säker extraktion
        # PokeAPI pokemon-species har fälten: "name" (lowercase) och "base_happiness" (int)
        name = (data.get("name") or Path(fp).stem).strip().lower()
        happiness = data.get("base_happiness", None)

        # Om fält saknas, hoppa över posten (eller sätt default)
        if happiness is None:
            # fallback om det mot förmodan saknas
            continue

        rows.append({"pokemon": name, "happiness": int(happiness)})

    if not rows:
        raise RuntimeError("Inga giltiga poster extraherades (saknade base_happiness?).")

    # Sortera lite snyggt för determinism
    df = pd.DataFrame(rows).sort_values(["pokemon"]).reset_index(drop=True)
    return df


def load(df: pd.DataFrame, out_dir: Path) -> Path:
    """
    Sparar DataFrame till CSV i observations/ med tidsstämpel i filnamn.
    Filnamn: observation_YY-MM-DD_HH_MM.csv
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%y-%m-%d_%H_%M")
    out_path = out_dir / f"observation_{ts}.csv"
    # Exakt rubriker enligt uppgiften
    df.to_csv(out_path, index=False, header=["pokemon", "happiness"])
    return out_path


def main():
    df = transform(BELT_DIR)
    out_path = load(df, OBS_DIR)
    print(f"Sparade observation: {out_path}")
    # Visa snabbt innehållet
    print(df.to_string(index=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.stderr.write(f"[Fel] {e}\n")
        sys.exit(1)