"""Shared fixtures for pokemate tests."""

import sys
import os
import pytest

# Ensure the project root (pokemon_machine/) is on sys.path so that
# ``game_feature.*`` and ``parents.auth.*`` imports resolve correctly.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture
def fake_session():
    """A session dict that mimics a successful login response."""
    return {
        "owner": {
            "id": 1,
            "name": "Ash",
            "age": 10,
            "pokemon_limit": 3,
            "pokemon_count": 1,
        },
        "access_token": "fake-jwt-token",
    }


@pytest.fixture
def full_session():
    """A session where the owner has hit their pokemon limit."""
    return {
        "owner": {
            "id": 2,
            "name": "Gary",
            "age": 12,
            "pokemon_limit": 3,
            "pokemon_count": 3,
        },
        "access_token": "fake-jwt-token",
    }
