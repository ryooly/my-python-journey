import requests
from services.services import create_pokemon

async def get_pokemon(name_id):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{str(name_id).lower()}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        result = await create_pokemon(data)

        # tambahkan errrorHandler

        return result

    except requests.exceptions.HTTPError as e:
        print(f"Pokémon not found: {e}")
        return None #ganti jadi error yang berkualitas

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve Pokémon data: {e}")
        return None #ganti jadi error yang berkualitas