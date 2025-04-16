from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.exeptions import UserAlreadyExistsError, UserNotFoundError
from app.repository.user_repository import UserRepository
from app.schemas.auth import  CreateUserSchema, GetUserSchema, UserSignIn

from app.repository.unit_of_work import UnitOfWork
from app.services.user_service import UserService

from app.core.config import settings
from app.core.security import create_access_token

router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get('/{user_id}')
async def get_user(user_id: str):
    with UnitOfWork() as unit_of_work:
        repo = UserRepository(unit_of_work.session)
        user_service = UserService(repo)
        user = user_service.get_user(user_id)
        if not user:
            return JSONResponse({"message": "User Not Found"})
        return JSONResponse({"data": user.dict()})
