from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas.pokemon_owner import PokemonOwnerCreate, PokemonOwnerLogin

app = FastAPI()

@app.post("/auth/register")
async def create_identity(user_data: PokemonOwnerCreate, db: Session = Depends(get_db)):
    result = 
    return result

@app.post("/auth/login")
async def login(user_data: PokemonOwnerLogin, db: Session = Depends(get_db)):
    result:
    return result

@app.post('/auth/logout')
async def logout():
    result:
    return result