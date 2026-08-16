from fastapi import FastAPI, Depends, HTTPException
from pokemon_machine.parents.auth.db import session
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas.pokemon_owner import PokemonOwnerCreate, PokemonOwnerLogin
from parents.auth.controller.auth_controller import createIdentityHandle, loginHandle, logoutHandle
from exceptions.base import AppException
from handlers.app_exception import app_exception_handler

app = FastAPI()
app.add_exception_handler(AppException, app_exception_handler)

@app.post("/auth/register")
async def create_identity(user_data: PokemonOwnerCreate, db: Session = Depends(get_db)):
    result = await createIdentityHandle(user_data, db)
    return result

@app.post("/auth/login")
async def login(user_data: PokemonOwnerLogin, db: Session = Depends(get_db)):
    result = await loginHandle(user_data, db)
    return result

@app.post('/auth/logout')
async def logout(user_id: str, db: Session = Depends(get_db)):
    result = await logoutHandle(user_id, db)
    return result
