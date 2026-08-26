from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import importlib

from parents.auth.global_dependecy.password_hashing import _hash_password, _verify_password
from parents.auth.global_dependecy.token_hashing import create_access_token, create_refresh_token
from parents.auth.repo.auth_repo import PokemonOwnerRepository
from parents.auth.repo.token_repo import TokenRepository
from parents.auth.models.pokemon_owners import PokemonOwner
from parents.auth.schemas.pokemon_owner import PokemonOwnerCreate, PokemonOwnerLogin

_errors = importlib.import_module("parents.auth.exceptions.global")
DataAlreadyExistsException = _errors.DataAlreadyExistsException
FailedInsertDataException = _errors.FailedInsertDataException
VerificationFailedException = _errors.VerificationFailedException
DataNotFoundException = _errors.DataNotFoundException
UniversalProblemException = _errors.UniversalProblemException


class PokemonOwnerService:

    def __init__(self, db: Session):
        self.db = db
        self.owner_repo = PokemonOwnerRepository(db)
        self.token_repo = TokenRepository(db)

    def _get_by_name(self, name: str) -> PokemonOwner | None:
        return self.owner_repo.get_by_name(name)

    def register(self, data: PokemonOwnerCreate) -> dict:
        try:
            existing = self._get_by_name(data.name)

            if existing:
                raise DataAlreadyExistsException()

            new_owner = PokemonOwner(
                name=data.name,
                age=data.age,
                personality=data.personality,
                hashed_password=_hash_password(data.password),
            )

            try:
                new_owner = self.owner_repo.create(new_owner)
            except IntegrityError:
                self.db.rollback()
                raise FailedInsertDataException()

            payload = {
                "id": new_owner.id,
                "name": new_owner.name,
            }

            access_token = create_access_token(payload)
            refresh_token = create_refresh_token(payload)

            self.token_repo.create_refresh_token(refresh_token, new_owner.id)

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

    def login(self, data: PokemonOwnerLogin) -> dict:
        try:
            owner = self._get_by_name(data.name)

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

            self.token_repo.create_refresh_token(refresh_token, owner.id)

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

    def logout(self, user_id: str) -> dict:
        try:
            existing = self.token_repo.get_refresh_token_by_user_id(int(user_id))

            if not existing:
                raise DataNotFoundException()

            self.token_repo.revoke_refresh_token(int(user_id))

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
