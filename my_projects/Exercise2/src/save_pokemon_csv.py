"""
Hämtar första 151 Pokémon:
- För varje Pokémon tittar vi i species-API:t (har namn på många språk)
- Vi plockar ut engelska namnet (och struntar i t.ex. japanska)
- Sparar en CSV i data/pokemon_list.csv med kolumner: id, name (engelska)
"""

# csv = inbyggt Python-bibliotek för att jobba med CSV-filer
# time = för att kunna pausa mellan anrop (så vi inte spammar API:t)
# requests = bibliotek för att göra HTTP-anrop (hämta data från webben)
import csv
import time
import requests

# URL för att hämta listan på Pokémon (första 151 från generation 1)
POKE_LIST_URL = "https://pokeapi.co/api/v2/pokemon?limit=151&offset=0"

def get_pokemon_list():
    """
    Hämtar en lista med Pokémon från API:t.
    Returnerar en lista med dictar, t.ex:
    [{'name': 'bulbasaur', 'url': 'https://pokeapi.co/...'}, ...]
    """
    resp = requests.get(POKE_LIST_URL, timeout=20)  # hämta data från webben
    resp.raise_for_status()  # om något gick fel (404, 500) → krascha direkt
    return resp.json().get("results", [])  # plocka ut 'results' ur svaret

def get_species_data(pokemon_name: str) -> dict:
    """
    Hämtar "species"-data för en Pokémon.
    Species-info innehåller bl.a. namn på olika språk.
    Exempel på URL: https://pokeapi.co/api/v2/pokemon-species/bulbasaur
    """
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name}"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json()

def pick_english_name(species: dict) -> str:
    """
    Plockar ut det engelska namnet från species['names'].
    Varje entry i 'names' har formatet:
        {"name": "Bulbasaur", "language": {"name": "en"}}
    Vi letar efter den där 'language.name' == 'en'.
    """
    for entry in species.get("names", []): # lista med namn på olika språk
        lang = entry.get("language", {}).get("name") # t.ex. 'en', 'ja', 'fr'
        if lang == "en":  # engelska
            return entry.get("name") # det engelska namnet
    # fallback: om engelska inte hittas, ta det "vanliga" namnet
    return species.get("name", "")

def pick_id(species: dict) -> int: # -> int betyder att funktionen returnerar en int
    """Returnerar Pokémonens id (Pokédex-numret)."""
    return species.get("id", 0) # returnerar 0 om 'id' inte finns

def main():
    # Hämta listan på alla 151 Pokémon
    pokelist = get_pokemon_list()

    rows = []  # här samlar vi upp raderna som ska sparas i CSV
    for i, p in enumerate(pokelist, start=1): # loopa över alla Pokémon
        name_api = p["name"]  # t.ex. 'bulbasaur'

        # Pausa mellan varje anrop (2 sekunder)
        # Bra "API-hyfs" – annars kan servern blockera oss
        time.sleep(2)

        # Hämta species-data för den här Pokémon
        species = get_species_data(name_api)

        # Plocka ut engelska namnet (ignorera japanska)
        eng_name = pick_english_name(species)

        # Plocka ut Pokémon-id
        pid = pick_id(species)

        # Lägg till en rad (dict) till listan med rader
        # Vi sparar bara 'id' och 'name' (på engelska)
        rows.append({
            "id": pid,
            "name": eng_name,
        })

        # Skriv progress i terminalen (så vi ser att det händer något)
        print(f"[{i}/{len(pokelist)}] {eng_name}")

    # När loopen är klar sparar vi allt till en CSV-fil
    out_path = "data/pokemon_list.csv"  # var filen ska hamna
    with open(out_path, "w", newline="", encoding="utf-8") as f: # öppna filen för skrivning    
        # Vi talar om vilka kolumner vi vill ha
        writer = csv.DictWriter(f, fieldnames=["id", "name"])
        writer.writeheader()     # skriv header-raden: id,name
        writer.writerows(rows)   # skriv alla raderna från listan

    print(f"\n✅ Klart! Sparade {len(rows)} rader till {out_path}")

# Detta körs bara om filen körs direkt (inte om den importeras som modul)
if __name__ == "__main__":
    main()