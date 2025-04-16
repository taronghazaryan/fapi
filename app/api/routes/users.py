from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.exeptions import UserAlreadyExistsError, UserNotFoundError
from app.repository.user_repository import UserRepository
from app.repository.unit_of_work import UnitOfWork
from app.services.user_service import UserService


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
        return JSONResponse({"data": user})

@router.get('/')
async def get_users(limit: int = None):
    with UnitOfWork() as unit_of_work:
        repo = UserRepository(unit_of_work.session)
        user_service = UserService(repo)
        users = user_service.list_users(limit=limit)
        return {"users": [user.dict() for user in users]}



