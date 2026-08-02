from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.global_dependecy.password_hashing import _hash_password, _verify_password
from global_dependecy.token_hashing import create_access_token, create_refresh_token
import app.repo.auth_repo as repo

from app.models.pokemon_owners import PokemonOwner
from app.schemas.pokemon_owner import PokemonOwnerCreate, PokemonOwnerLogin


class PokemonOwnerService:
    def __init__(self, db: Session):
        self.db = db

    async def _get_by_name(self, name: str) -> PokemonOwner | None:
        user = await repo.get_by_name(name)
        return user

    async def register(self, data: PokemonOwnerCreate) -> PokemonOwner:
        existing = self._get_by_name(data.name)
        if existing:
            # error handler
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nama owner sudah terdaftar.",
            )

        new_owner = PokemonOwner(
            name=data.name,
            age=data.age,
            personality=data.personality,
            hashed_password=_hash_password(data.password),
        )

        try:
            new_owner = await repo.create(new_owner)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create owner. The name may already be in use.",
            )

        payload = {
            "id": new_owner.id,
            "name": new_owner.name,
        }

        access_token = create_access_token(payload)

        refresh_token = create_refresh_token(payload)

        return {
            "owner": new_owner,
            "access_token": access_token,
        }

    async def login(self, data: PokemonOwnerLogin) -> PokemonOwner:
        owner = self._get_by_name(data.name)

        if not owner or not _verify_password(data.password, owner.hashed_password):
            # error handler
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Nama atau password salah.",
            )

        payload = {
            "id": owner.id,
            "name": owner.name,
        }

        access_token = create_access_token(payload)

        refresh_token = create_refresh_token(payload)

        return {
            "owner": owner,
            "access_token": access_token,
        }

    async def logout(self, user_id: str) -> dict:
        existing = await repo.
