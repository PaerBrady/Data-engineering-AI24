
import json
import time
from pathlib import Path
from faker import Faker

def extract_users(number_users: int = 5, users_directory: Path = Path("users")):
    """
    Genererar ett antal fejkade användare (default: 5) och sparar dem som JSON-filer
    i den angivna mappen (default: 'users'). Om det redan finns användare där,
    fortsätter numreringen så att inga skrivs över.
    """

    # Skapa mappen där filerna ska sparas, om den inte redan finns
    users_directory.mkdir(parents=True, exist_ok=True)

    # Räkna hur många JSON-filer som redan finns i mappen
    existing_files = list(users_directory.glob("*.json"))
    start_index = len(existing_files) + 1  # Börja efter senaste ID

    # Skapar ett Faker-objekt som genererar svenska namn, adresser osv.
    faker = Faker("sv_SE")

    # Skapa nya användare
    for i in range(start_index, start_index + number_users):
        user = {
            "id": i,
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "phone_number": faker.phone_number(),
            "date_of_birth": faker.date_of_birth().isoformat(),
            "avatar": f"https://i.pravatar.cc/150?img={i}",
            "address": {
                "street": faker.street_address(),
                "city": faker.city(),
                "zip": faker.postcode(),
                "coordinates": {
                    "lat": float(faker.latitude()),
                    "lng": float(faker.longitude())
                }
            }
        }

        file_path = users_directory / f"{i}.json"

        with open(file_path, "w") as f:
            json.dump(user, f, indent=2)

        print(f"Saved user {user['id']} to {file_path}")
        time.sleep(1)  # Frivillig paus (kan tas bort)

if __name__ == "__main__":
    extract_users()





# %%
# import json              # För att spara data som JSON-filer
# import time              # För att lägga in pauser (t.ex. simulera nätverksanrop)
# from pathlib import Path # För att hantera sökvägar på ett säkert sätt
# from faker import Faker  # Bibliotek för att generera fejkad (men realistisk) data

# # Funktion som genererar ett antal fejkade användare
# # Om inget anges skapas 5 användare och de sparas i mappen "users"
# def extract_users(number_users: int = 5, users_directory: Path = Path("users")):
#     """
#     Genererar ett antal fejkade användare (default: 5) och sparar dem som JSON-filer
#     i den angivna mappen (default: 'users').
#     """

#     # Skapa mappen där filerna ska sparas, om den inte redan finns
#     users_directory.mkdir(parents=True, exist_ok=True)

#     # Skapar ett Faker-objekt som genererar svenska namn, adresser osv.
#     faker = Faker("sv_SE")

#     # Loopar det antal gånger som anges (standard är 5 gånger)
#     for i in range(number_users):
#         # Skapa en fejkad användare som en ordbok (dictionary)
#         user = {
#             "id": i + 1,                                 # Unikt ID
#             "first_name": faker.first_name(),           # Förnamn
#             "last_name": faker.last_name(),             # Efternamn
#             "email": faker.email(),                     # E-postadress
#             "phone_number": faker.phone_number(),       # Telefonnummer
#             "date_of_birth": faker.date_of_birth().isoformat(),  # Födelsedatum
#             "avatar": f"https://i.pravatar.cc/150?img={i + 1}",  # Avatarbild
#             "address": {                                 # Adress som ordbok
#                 "street": faker.street_address(),        # Gatuadress
#                 "city": faker.city(),                    # Stad
#                 "zip": faker.postcode(),                 # Postnummer
#                 "coordinates": {
#                     "lat": float(faker.latitude()),      # Latitud
#                     "lng": float(faker.longitude())      # Longitud
#                 }
#             }
#         }


#         # Skapa sökvägen till filen, t.ex. "users/1.json", "users/2.json" osv.
#         file_path = users_directory / f"{i + 1}.json"

#         # Öppna filen i skrivläge och spara användardatan som JSON
#         with open(file_path, "w") as f:
#             json.dump(user, f, indent=2)  # indent=2 gör JSON-filen mer läsbar

#         # Skriv ut i terminalen att användaren har sparats
#         print(f"Saved user {user['id']} to {file_path}")

#         # Vänta 2 sekunder (kan tas bort om man inte behöver pauser)
#         time.sleep(2)

# # Om scriptet körs direkt (inte importeras som modul), kör funktionen
# if __name__ == "__main__":
#     # Kör funktionen utan att ange något → skapar 5 användare automatiskt
#     extract_users()




# %%