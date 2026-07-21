from pydantic import BaseModel, computed_field
from app.schemas.pokemons import OwnedPokemonResponse

class PokemonOwnerCreate(BaseModel):
    name: str
    age: int
    personality: str
    pokemon_limit: int = 6


class PokemonOwnerLogin(BaseModel):
    name: str
    password: str


class PokemonOwnerUpdate(BaseModel):
    name: str | None = None


class PokemonOwnerResponse(BaseModel):
    id: int
    name: str
    age: int
    pokemon_limit: int
    pokemons: list[OwnedPokemonResponse]

    @computed_field
    @property
    def pokemon_count(self) -> int:
        return len(self.pokemons)

    model_config = {
        "from_attributes": True
    }