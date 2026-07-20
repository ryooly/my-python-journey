from typing import Any

from pydantic import BaseModel


class PokemonCreate(BaseModel):
    pokeapi_id: int
    name: str
    base_experience: int | None = None
    height: int | None = None
    weight: int | None = None
    order: int | None = None

    types: list[Any] | None = None
    abilities: list[Any] | None = None
    stats: list[Any] | None = None
    sprites: dict[str, Any] | None = None
    cries: dict[str, Any] | None = None
    species: str | None = None
    forms: list[Any] | None = None
    moves: list[Any] | None = None
    held_items: list[Any] | None = None


class PokemonResponse(PokemonCreate):
    id: int

    model_config = {
        "from_attributes": True
    }