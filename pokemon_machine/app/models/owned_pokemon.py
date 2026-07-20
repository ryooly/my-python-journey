from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class OwnedPokemon(Base):
    __tablename__ = "owned_pokemons"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(
        Integer,
        ForeignKey("pokemon_owners.id"),
        nullable=False
    )
    pokemon_id = Column(
        Integer,
        ForeignKey("pokemons.id"),
        nullable=False
    )
    level = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship(
        "PokemonOwner",
        back_populates="pokemons"
    )
    pokemon = relationship(
        "Pokemon",
        back_populates="owners"
    )