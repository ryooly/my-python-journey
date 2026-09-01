import requests
import importlib
from pokemon_hunter.services.services import PokemonService

_errors = importlib.import_module("parents.auth.exceptions.global")
FailedInsertDataException = _errors.FailedInsertDataException
DataNotFoundException = _errors.DataNotFoundException
UniversalProblemException = _errors.UniversalProblemException

async def get_pokemon(name_id):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{str(name_id).lower()}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        result = await PokemonService.create_pokemon(data)

        if not result:
            raise FailedInsertDataException()
            

        return result

    except FailedInsertDataException:
        raise

    except DataNotFoundException:
        raise

    except requests.exceptions.RequestException:
        raise DataNotFoundException()

    except Exception:
        raise UniversalProblemException(
            message="An unexpected error occurred while fetching Pokémon data",
        )