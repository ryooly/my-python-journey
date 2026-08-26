from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from parents.auth.db.session import get_db
from parents.auth.schemas.pokemon_owner import PokemonOwnerCreate, PokemonOwnerLogin
from parents.auth.controller.auth_controller import createIdentityHandle, loginHandle, logoutHandle
from parents.auth.exceptions.base import AppException
from parents.auth.handlers.app_exception import app_exception_handler

app = FastAPI()
app.add_exception_handler(AppException, app_exception_handler)


@app.post("/auth/register")
def create_identity(user_data: PokemonOwnerCreate, db: Session = Depends(get_db)):
    result = createIdentityHandle(user_data, db)
    return result


@app.post("/auth/login")
def login(user_data: PokemonOwnerLogin, db: Session = Depends(get_db)):
    result = loginHandle(user_data, db)
    return result


@app.post('/auth/logout')
def logout(user_id: str, db: Session = Depends(get_db)):
    result = logoutHandle(user_id, db)
    return result
