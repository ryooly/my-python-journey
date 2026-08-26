"""Run this once to create all database tables.

Usage (from pokemon_machine/ folder):
    python init_db.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from parents.auth.db.base import Base
from parents.auth.db.session import engine

# Import every model so Base knows about them
from parents.auth.models.pokemon_owners import PokemonOwner     # noqa
from parents.auth.models.pokemons import Pokemon                # noqa
from parents.auth.models.owned_pokemon import OwnedPokemon      # noqa
from parents.auth.models.refresh_token import RefreshToken       # noqa

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done! All tables created in PostgreSQL.")
