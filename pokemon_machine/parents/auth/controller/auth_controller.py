from sqlalchemy.orm import Session
from parents.auth.schemas.pokemon_owner import PokemonOwnerCreate, PokemonOwnerLogin, PokemonOwnerResponse
from parents.auth.services.auth_services import PokemonOwnerService


def createIdentityHandle(user_data: PokemonOwnerCreate, db: Session) -> dict:
    service = PokemonOwnerService(db)
    result = service.register(user_data)
    return result


def loginHandle(user_data: PokemonOwnerLogin, db: Session) -> dict:
    service = PokemonOwnerService(db)
    result = service.login(user_data)
    return result


def logoutHandle(user_id: str, db: Session) -> dict:
    service = PokemonOwnerService(db)
    result = service.logout(user_id)
    return result
