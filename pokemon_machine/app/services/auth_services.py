from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.global_dependecy.password_hashing import _hash_password, _verify_password
from global_dependecy.token_hashing import create_access_token, create_refresh_token
from exceptions.global import (
    DataAlreadyExistsException,
    FailedInsertDataException,
    VerificationFailedException,
    DataNotFoundException,
    UniversalProblemException,
)
import app.repo.auth_repo as repo
import app.repo.token_repo as token_repo

from app.models.pokemon_owners import PokemonOwner
from app.schemas.pokemon_owner import PokemonOwnerCreate, PokemonOwnerLogin


class PokemonOwnerService:

    def __init__(self, db: Session):
        self.db = db

    async def _get_by_name(self, name: str) -> PokemonOwner | None:
        user = await repo.get_by_name(name)
        return user

    async def register(self, data: PokemonOwnerCreate) -> PokemonOwner:
        try:
            existing = await self._get_by_name(data.name)

            if existing:
                raise DataAlreadyExistsException()

            new_owner = PokemonOwner(
                name=data.name,
                age=data.age,
                personality=data.personality,
                hashed_password=_hash_password(data.password),
            )

            try:
                new_owner = await repo.create(new_owner)

            except IntegrityError:
                raise FailedInsertDataException()

            payload = {
                "id": new_owner.id,
                "name": new_owner.name,
            }

            access_token = create_access_token(payload)
            refresh_token = create_refresh_token(payload)

            await token_repo.create_refresh_token(refresh_token)

            return {
                "owner": new_owner,
                "access_token": access_token,
            }

        except (DataAlreadyExistsException, FailedInsertDataException):
            raise

        except Exception:
            raise UniversalProblemException(
                message="An error occurred during registration",
            )

    async def login(self, data: PokemonOwnerLogin) -> PokemonOwner:
        try:
            owner = await self._get_by_name(data.name)

            if not owner or not _verify_password(
                data.password,
                owner.hashed_password,
            ):
                raise VerificationFailedException()

            payload = {
                "id": owner.id,
                "name": owner.name,
            }

            access_token = create_access_token(payload)
            refresh_token = create_refresh_token(payload)

            await token_repo.create_refresh_token(refresh_token)

            return {
                "owner": owner,
                "access_token": access_token,
            }

        except VerificationFailedException:
            raise

        except Exception:
            raise UniversalProblemException(
                message="An error occurred during login",
            )

    async def logout(self, user_id: str) -> dict:
        try:
            existing = await token_repo.get_refresh_token_by_user_id(user_id)

            if not existing:
                raise DataNotFoundException()

            await token_repo.revoke_refresh_token(user_id)

            return {
                "status": "success",
                "message": "Logout successful",
            }

        except DataNotFoundException:
            raise

        except Exception:
            raise UniversalProblemException(
                message="An error occurred during logout",
            )


