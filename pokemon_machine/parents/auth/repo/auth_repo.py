from sqlalchemy.orm import Session
from parents.auth.models.pokemon_owners import PokemonOwner


class PokemonOwnerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str) -> PokemonOwner | None:
        return self.db.query(PokemonOwner).filter(PokemonOwner.name == name).first()

    def create(self, owner: PokemonOwner) -> PokemonOwner:
        self.db.add(owner)
        self.db.commit()
        self.db.refresh(owner)
        return owner

    def delete(self, owner: PokemonOwner) -> None:
        self.db.delete(owner)
        self.db.commit()
