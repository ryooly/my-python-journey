from sqlalchemy.orm import Session
from app.schemas.pokemon_owner import PokemonOwner


class PokemonOwnerRepository:
    def __init__(self, db: Session):
        self.db = db

    async def get_by_name(self, name: str) -> PokemonOwner | None:
        return self.db.query(PokemonOwner).filter(PokemonOwner.name == name).first()

    async def create(self, owner: PokemonOwner) -> PokemonOwner:
        self.db.add(owner)
        self.db.commit()
        self.db.refresh(owner)
        return owner

    async def delete(self, owner: PokemonOwner) -> None:
        self.db.delete(owner)
        self.db.commit()