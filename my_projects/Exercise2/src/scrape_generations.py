"""
Hämtar pokémon-species per generation från PokeAPI och sparar CSV-filer.

Vad vi gör:
1) Hämtar listan av generationer från: https://pokeapi.co/api/v2/generation/
2) För varje generation hämtar vi dess "pokemon_species" (namn + url).
3) Vi extraherar species_id ur url:en (utan extra API-anrop).
4) Vi sparar:
   - data/generations/gen_<nr>.csv            (species_id, species_name, generation)
   - data/generations/all_generations.csv     (alla rader ihop)
5) Om data/pokemon_list.csv (från steg c) finns:
   - vi delar upp din tidigare lista (id,name) i generationer och sparar:
     data/generations/pokemon_gen_<nr>.csv
"""

import csv
import os
import time
import requests
from urllib.parse import urlparse

GEN_ROOT = "https://pokeapi.co/api/v2/generation/"   # root för alla generationer
OUT_DIR = "data/generations"
PREV_LIST = "data/pokemon_list.csv"  # från steg c (id,name)

def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)

def fetch_all_generations():
    """
    Hämtar listan över generationer (namn + url). Returnerar en lista av dicts.
    Exempel: {'name': 'generation-i', 'url': 'https://.../generation/1/'}
    """
    resp = requests.get(GEN_ROOT, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    # 'results' innehåller alla generationer; vi behåller ordningen de kommer i
    return data.get("results", [])

def fetch_generation_detail(gen_url):
    """
    Hämtar en enskild generation (med pokemon_species-listan).
    """
    resp = requests.get(gen_url, timeout=20)
    resp.raise_for_status()
    return resp.json()

def species_id_from_url(species_url: str) -> int:
    """
    Extrahera species-id från url, t.ex:
    https://pokeapi.co/api/v2/pokemon-species/1/  -> 1
    """
    path = urlparse(species_url).path  # '/api/v2/pokemon-species/1/'
    # sista segmentet är tomt pga slash i slutet, näst sista är id:t
    parts = [p for p in path.split('/') if p]
    # parts = ['api','v2','pokemon-species','1']
    try:
        return int(parts[-1])
    except Exception:
        return 0

def write_csv(path, rows, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

def load_previous_list(path=PREV_LIST):
    """
    Läser tidigare CSV (id,name) om den finns.
    Returnerar dict: id -> name
    """
    if not os.path.exists(path):
        return {}
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                pid = int(row["id"])
            except Exception:
                continue
            out[pid] = row.get("name", "")
    return out

def main():
    ensure_out_dir()

    print("Hämtar lista över generationer…")
    gens = fetch_all_generations()
    # Förväntat: generation-i, generation-ii, … men vi vill också ha ett löpnummer.
    # PokeAPI:s ordning är vanligtvis 1..N, så vi numrerar i den ordningen:
    indexed_gens = [(idx + 1, g["name"], g["url"]) for idx, g in enumerate(gens)]

    all_rows = []  # för master-CSV
    prev_map = load_previous_list()  # id -> English Name (om finns från steg c)

    for gen_num, gen_name, gen_url in indexed_gens:
        print(f"\n[{gen_num}] Hämtar {gen_name} → {gen_url}")
        time.sleep(1)  # lite hyfs mot API:t

        detail = fetch_generation_detail(gen_url)
        species_list = detail.get("pokemon_species", [])  # lista med {'name', 'url'}

        # Bygg rader: species_id, species_name, generation
        gen_rows = []
        for s in species_list:
            s_name = s.get("name", "")  # lowercase species-namn, t.ex. 'bulbasaur'
            s_id = species_id_from_url(s.get("url", ""))  # plocka id från url
            gen_rows.append({
                "species_id": s_id,
                "species_name": s_name,
                "generation": gen_num,
            })

        # Sortera efter species_id så det ser snyggt ut
        gen_rows.sort(key=lambda r: r["species_id"] or 999999)

        # Spara per-generation CSV
        out_path = os.path.join(OUT_DIR, f"gen_{gen_num}.csv")
        write_csv(out_path, gen_rows, fieldnames=["species_id", "species_name", "generation"])
        print(f"  → Sparade {len(gen_rows)} rader till {out_path}")

        # Lägg till i master-listan
        all_rows.extend(gen_rows)

        # Om vi har tidigare lista (id,name), dela upp den efter generation
        # Vi matchar på species_id (samma som id i din tidigare CSV för Gen 1
        # och i praktiken för de flesta), annars får den bara inte med den raden.
        if prev_map:
            subset = []
            for r in gen_rows:
                pid = r["species_id"]
                if pid in prev_map:
                    subset.append({"id": pid, "name": prev_map[pid]})
            if subset:
                out_previous = os.path.join(OUT_DIR, f"pokemon_gen_{gen_num}.csv")
                write_csv(out_previous, subset, fieldnames=["id", "name"])
                print(f"  → Delmängd från din tidigare lista: {len(subset)} rader → {out_previous}")

    # Spara master-CSV med alla generationer samlade
    master_path = os.path.join(OUT_DIR, "all_generations.csv")
    # Sortera master efter generation och id
    all_rows.sort(key=lambda r: (r["generation"], r["species_id"] or 999999))
    write_csv(master_path, all_rows, fieldnames=["species_id", "species_name", "generation"])
    print(f"\n✅ Klart! Sparade master-lista ({len(all_rows)} rader) → {master_path}")

if __name__ == "__main__":
    main()