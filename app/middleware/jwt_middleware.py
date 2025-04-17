from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from jose import jwt, JWTError

from app.core.config import settings, redis_instance
from app.repository.user_repository import UserRepository
from app.repository.unit_of_work import UnitOfWork
from app.services.user_service import UserService


EXCLUDED_PATHS = {
    "/v1/auth/sign-in",
    "/v1/auth/sign-up",
    "/v1/auth/verify"
}


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if not any(request.url.path.startswith(path) for path in EXCLUDED_PATHS):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return JSONResponse({"message": "Unauthorized"}, status_code=401)
            token_type, token = auth_header.split(' ')

            if token_type != 'Bearer' or not token:
                return JSONResponse({"message": "Unidentified authorization"}, status_code=401)
            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                user_id = payload['sub']
                access_token_in_redis = redis_instance.get(f"user:{user_id}:access_token")

                if not access_token_in_redis:
                    return JSONResponse({"message": "Unidentified authorization"}, status_code=401)

                with UnitOfWork() as unit_of_work:
                    repo = UserRepository(unit_of_work.session)
                    user_service = UserService(repo)
                    user = user_service.get_user(user_id)
                    if not user:
                        return JSONResponse({"message": "Unidentified authorization"}, status_code=401)
                    elif not user['verified']:
                        return JSONResponse({"message": "Email not verified"}, status_code=401)
                    elif user['disabled']:
                        return JSONResponse({"message": "User are disabled"}, status_code=401)

                request.state.user = {"id": user_id}
                request.session['user'] = {'id': user_id}
            except JWTError:
                return JSONResponse({"message": "Invalid or expired token"}, status_code=401)

        response = await call_next(request)
        return response
