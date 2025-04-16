import redis
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.exeptions import UserAlreadyExistsError, UserNotFoundError
from app.repository.user_repository import UserRepository
from app.schemas.auth import  CreateUserSchema, GetUserSchema, UserSignIn

from app.repository.unit_of_work import UnitOfWork
from app.services.email_service import send_email
from app.services.user_service import UserService

from app.core.config import settings
from app.core.security import create_access_token




router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post('/sign-up', status_code=201)
async def sign_up(pyload: CreateUserSchema):
    with UnitOfWork() as unit_of_work:
        repo = UserRepository(unit_of_work.session)
        user_service = UserService(repo)
        try:
            user_service.place_user(pyload)
            unit_of_work.commit()
            send_email(pyload.email, pyload.first_name, 'http://example.com')
            return JSONResponse(content={"message": f"Dear {pyload.username}, your profile is created successfully!!!"},
                                status_code=201)
        except UserAlreadyExistsError:
            raise HTTPException(status_code=400, detail="User already exists")


@router.post('/sign-in', status_code=200)
async def sign_in(pyload: UserSignIn):
    with UnitOfWork() as unit_of_work:
        repo = UserRepository(unit_of_work.session)
        user_service = UserService(repo)
        try:
            username = pyload.username
            password = pyload.password
            user = user_service.authenticate(username=username, password=password)
            if user is not None:
                data = {
                    "sub": user.id,
                }
                token = create_access_token(data)
                return {"access_token": token}
            return JSONResponse({"message": "User Not Found"}, status_code=404)
        except UserNotFoundError:
            return JSONResponse({"message": "Invalid username or password"}, status_code=400)

