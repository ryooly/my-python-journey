from pokemon_machine.parents.auth.db.session import SessionLocal
from repositories.insert_pokemon import PokemonRepository


class PokemonService:

    @staticmethod
    async def create_pokemon(data: dict):
        db = SessionLocal()

        try:
            pokemon = PokemonRepository.create(
                db,
                data
            )

            return pokemon

        except Exception:
            db.rollback()
            raise UniversalProblemException(
                message="An error occurred while creating a pokemon",
            )

        finally:
            db.close()


