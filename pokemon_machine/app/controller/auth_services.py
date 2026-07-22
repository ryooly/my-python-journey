from sqlalchemy.orm import Session
from schemas.pokemon_owner import PokemonOwnerCreate, PokemonOwnerLogin
from schemas.pokemon_owner import PokemonOwnerResponse
from services.auth_services import PokemonOwnerService

async def createIdentityHandle(user_data: PokemonOwnerCreate, db: Session) -> PokemonOwnerResponse:
    service = PokemonOwnerService(db)
    result = service.register(user_data)
    return result

async def loginHandle(user_data: PokemonOwnerCreate, db: Session) -> PokemonOwnerResponse:
    service = PokemonOwnerService(db)
    result = service.register(user_data)
    return result

