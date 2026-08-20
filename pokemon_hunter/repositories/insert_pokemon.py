from sqlalchemy.orm import Session
from pokemon_machine.parents.auth.models.pokemons import Pokemon


class PokemonRepository:

    @staticmethod
    def create(db: Session, data: dict) -> Pokemon:
        pokemon = Pokemon(
            pokeapi_id=data["id"],
            name=data["name"],
            base_experience=data["base_experience"],
            height=data["height"],
            weight=data["weight"],
            order=data["order"],

            types=[
                {
                    "slot": t["slot"],
                    "name": t["type"]["name"]
                }
                for t in data["types"]
            ],

            abilities=[
                {
                    "name": a["ability"]["name"],
                    "slot": a["slot"],
                    "is_hidden": a["is_hidden"]
                }
                for a in data["abilities"]
            ],

            stats=[
                {
                    "name": s["stat"]["name"],
                    "base_stat": s["base_stat"],
                    "effort": s["effort"]
                }
                for s in data["stats"]
            ],

            sprites=data["sprites"],
            cries=data.get("cries"),
            species=data["species"]["name"],

            forms=[
                form["name"]
                for form in data["forms"]
            ],

            moves=[
                {
                    "name": move["move"]["name"],
                    "version_group_details": move["version_group_details"]
                }
                for move in data["moves"]
            ],

            held_items=[
                {
                    "name": item["item"]["name"],
                    "version_details": item["version_details"]
                }
                for item in data["held_items"]
            ],
        )

        db.add(pokemon)
        db.commit()
        db.refresh(pokemon)

        return pokemon

