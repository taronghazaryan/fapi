import redis

from passlib.context import CryptContext

from datetime import datetime, timedelta

from jose import jwt

from app.core.config import settings



pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)



def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    expire_seconds = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    redis_key = f"user:{data['sub']}:access_token"
    redis_instance.set(redis_key, encoded_jwt, ex=expire_seconds)
    token = redis_instance.get(redis_key)

    return token

def delete_token_from_redis(user_id: str):
    redis_key = f"user:{user_id}:access_token"
    redis_instance.delete(redis_key)



