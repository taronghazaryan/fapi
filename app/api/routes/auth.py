from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from app.exeptions import UserAlreadyExistsError, UserNotFoundError
from app.repository.user_repository import UserRepository
from app.schemas.auth import  CreateUserSchema, GetUserSchema, UserSignIn

from app.repository.unit_of_work import UnitOfWork
from app.services.email_service import send_email
from app.services.user_service import UserService

from app.core.security import create_access_token, delete_token_from_redis
from app.core.factories.grant_factory import GrantFactory


email_verify_salt = 'email_verifcation'
email_verify_prefix = "email_verification_grant"


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
            try:
                user = user_service.get_user_by_email(pyload.email)
                grant = GrantFactory.create_and_save_grant(user.id, email_verify_prefix, email_verify_salt, 3600)
                send_email(pyload.email, pyload.first_name, f'http://localhost:8000/v1/auth/verify/{grant}')
                return JSONResponse(
                    content={"message": f"Dear {pyload.username}, check your email"},
                    status_code=201)
            except UserNotFoundError:
                return JSONResponse(content={"message": "User not found"}, status_code=404)
        except UserAlreadyExistsError:
            raise HTTPException(status_code=400, detail="User already exists")


@router.get('/verify/{grant}', status_code=200)
async def email_verify(grant: str):
    try:
        user_id = GrantFactory.get_user_id_from_grant(grant=grant, salt=email_verify_salt)
        with UnitOfWork() as unit_of_work:
            repo = UserRepository(unit_of_work.session)
            user_service = UserService(repo)
            user_service.update_user(user_id, {"verified": True})
            unit_of_work.commit()
            GrantFactory.delete_grant(user_id, prefix=email_verify_prefix)
            return RedirectResponse('http://localhost:3000/verified')
    except UserNotFoundError:
        return JSONResponse({"message": "User not found"}, status_code=404)


@router.post('/sign-in', status_code=200)
async def sign_in(pyload: UserSignIn):
    print(pyload)
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


@router.post('/sign-out', status_code=200)
async def sign_out(request: Request):
    try:
        user_id = request.session.get('user')['id']
        delete_token_from_redis(user_id)
        return JSONResponse({"message": "You logged out successfully"})
    except UserNotFoundError:
        return JSONResponse({"message": "user not found"})

