from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from app.api.routes import users
from app.api.routes import auth
from app.api.routes import chat

from app.core.config import settings

from app.middleware.jwt_middleware import JWTAuthMiddleware

origins = [
    "http://localhost:3000",
    "https://127.0.0.1:3000",
]

app = FastAPI()

app.add_middleware(
    JWTAuthMiddleware
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


v1 = APIRouter(prefix='/v1', tags=['v1'])
v1.include_router(auth.router)
v1.include_router(users.router)
v1.include_router(chat.router)

app.include_router(v1)

