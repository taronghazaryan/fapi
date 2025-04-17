import json
from uuid import UUID

from fastapi import APIRouter, HTTPException

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.exeptions import UserAlreadyExistsError, UserNotFoundError
from app.repository.user_repository import UserRepository
from app.repository.unit_of_work import UnitOfWork
from app.schemas.user import ProfileSchema
from app.services.user_service import UserService


router = APIRouter(
    prefix='/users',
    tags=['users']
)

@router.get('/profile')
async def profile(request: Request):
    with UnitOfWork() as unit_of_work:
        repo = UserRepository(unit_of_work.session)
        user_service = UserService(repo)
        try:
            user_id = request.session.get('user')['id']
            user = user_service.get_user(user_id)
        except:
            return JSONResponse({"message": "User Not Found"}, status_code=404)
        return ProfileSchema(**user)


@router.get('/{user_id}')
async def get_user(user_id: str):
    with UnitOfWork() as unit_of_work:
        repo = UserRepository(unit_of_work.session)
        user_service = UserService(repo)
        try:
            user = user_service.get_user(user_id)
        except:
            return JSONResponse({"message": "User Not Found"}, status_code=404  )

        return JSONResponse({"data": user})

@router.get('/')
async def get_users(limit: int = None):
    with UnitOfWork() as unit_of_work:
        repo = UserRepository(unit_of_work.session)
        user_service = UserService(repo)
        users = user_service.list_users(limit=limit)
        return {"users": [user.dict() for user in users]}


