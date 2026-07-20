from pydantic import BaseModel

from app.models.pokemon_owners import PokemonStatus


class OwnedPokemonCreate(BaseModel):
    owner_id: int
    pokemon_id: int
    level: int = 1


class OwnedPokemonUpdate(BaseModel):
    status: PokemonStatus | None = None


class OwnedPokemonResponse(BaseModel):
    id: int
    owner_id: int
    pokemon_id: int
    level: int
    status: PokemonStatus

    model_config = {
        "from_attributes": True
    }