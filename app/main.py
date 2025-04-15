from fastapi import FastAPI, APIRouter

from app.api.routes import users
from app.api.routes import auth

app = FastAPI()

v1 = APIRouter(prefix='/v1', tags=['v1'])
v1.include_router(auth.router)
v1.include_router(users.router)

app.include_router(v1)

