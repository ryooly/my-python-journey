from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from parents.auth.db.base import Base


class PokemonOwner(Base):
    __tablename__ = "pokemon_owners"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    personality = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    pokemon_limit = Column(Integer, default=3)
    pokemon_count = Column(Integer, default=0)
    pokemons = relationship(
        "OwnedPokemon",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
