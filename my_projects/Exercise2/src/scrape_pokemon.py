# Vi importerar requests-biblioteket som låter oss göra HTTP-anrop (hämta data från webben).
import requests

def fetch_pokemon_list(limit=151, offset=0):
    """
    Hämtar en lista med Pokémon-namn från PokeAPI.

    Argument:
        limit (int): Hur många Pokémon vi vill hämta (standard: 151 för generation 1).
        offset (int): Var i listan vi vill börja (0 = från första Pokémon).

    Returnerar:
        list[str]: En lista med Pokémon-namn.
    """
    # Bygger URL till PokeAPI.
    # Exempel: https://pokeapi.co/api/v2/pokemon?limit=151&offset=0
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"

    # Gör ett GET-anrop (hämtar data från API:t).
    response = requests.get(url)

    # raise_for_status kastar ett fel om anropet misslyckades (t.ex. 404 eller 500).
    # Bra för att slippa gå vidare med trasiga svar.
    response.raise_for_status()

    # Konverterar svaret från JSON-text till en Python-dictionary.
    data = response.json()

    # Hämta listan med Pokémon från nyckeln "results".
    # Om den inte finns, använd en tom lista som default.
    results = data.get("results", [])

    # Plocka ut bara namnen (API:t returnerar {"name": "...", "url": "..."})
    names = [pokemon["name"] for pokemon in results]

    # Returnera listan med namn.
    return names


# Om vi kör filen direkt (inte bara importerar den i ett annat script):
if __name__ == "__main__":
    # Hämta de första 151 Pokémon.
    pokemons = fetch_pokemon_list()

    # Skriv ut de första 10 som ett test.
    print("Första 10 Pokémon:")
    print(pokemons[:10])