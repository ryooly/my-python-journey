import enum as _enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from parents.auth.db.base import Base


class PokemonStatus(str, _enum.Enum):
    ALIVE = "alive"
    DEAD = "dead"


class Pokemon(Base):
    __tablename__ = "pokemons"
    id = Column(Integer, primary_key=True, index=True)
    pokeapi_id = Column(Integer, unique=True, nullable=False)
    name = Column(String(100), nullable=False, unique=True)
    base_experience = Column(Integer)
    height = Column(Integer)
    weight = Column(Integer)
    order = Column(Integer)
    status = Column(
        String(20),
        default=PokemonStatus.ALIVE.value,
        nullable=False,
    )
    types = Column(JSON)
    abilities = Column(JSON)
    stats = Column(JSON)
    sprites = Column(JSON)
    cries = Column(JSON)
    species = Column(String(100))
    forms = Column(JSON)
    moves = Column(JSON)
    held_items = Column(JSON)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    owners = relationship(
        "OwnedPokemon",
        back_populates="pokemon"
    )
