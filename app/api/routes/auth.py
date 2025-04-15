from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.exeptions import UserAlreadyExistsError
from app.repository.user_repository import UserRepository
from app.schemas.auth import  CreateUserSchema, GetUserSchema

from app.repository.unit_of_work import UnitOfWork
from app.services.user_service import UserService

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
            return JSONResponse(content={"message": f"Dear {pyload.username}, your profile is created successfully!!!"},
                                status_code=201)
        except UserAlreadyExistsError:
            raise HTTPException(status_code=400, detail="User already exists")

