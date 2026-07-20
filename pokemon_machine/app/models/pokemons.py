from sqlalchemy import (
    Column,
    Integer,
    String,
    JSON,
    DateTime,
    enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class PokemonStatus(str, enum):
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
    enum(PokemonStatus),
    default=PokemonStatus.ALIVE,
    nullable=False
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