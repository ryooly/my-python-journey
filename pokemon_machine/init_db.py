"""Run this once to create all database tables.

Usage (from pokemon_machine/ folder):
    python init_db.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from parents.auth.db.base import Base
from parents.auth.db.session import engine
import parents.auth.models  # noqa: loads all models for relationship resolution

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Done! All tables created in PostgreSQL.")
