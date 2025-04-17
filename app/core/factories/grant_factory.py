from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from app.core.config import settings, redis_instance

from app.exeptions import InvalidActionError


class GrantFactory:

    @staticmethod
    def create_and_save_grant(user_id, prefix, salt, exp):
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
        grant = serializer.dumps(user_id, salt=salt)
        redis_key = f"{prefix}:{user_id}"
        redis_instance.set(redis_key, grant, exp)
        return grant

    @staticmethod
    def get_user_id_from_grant(grant, salt):
        serializer = URLSafeTimedSerializer(settings.SECRET_KEY)
        try:
            user_id = serializer.loads(grant, salt=salt)
            return user_id
        except SignatureExpired:
            raise InvalidActionError("Grant has expired")
        except BadSignature:
            raise InvalidActionError("Invalid grant signature")
        except Exception as e:
            raise InvalidActionError(f"Unexpected error: {e}")

    @staticmethod
    def get_grant(user_id, prefix):
        redis_key = f"{prefix}:{user_id}"
        grant = redis_instance.get(redis_key)
        return grant

    @staticmethod
    def delete_grant(user_id, prefix):
        redis_key = f"{prefix}:{user_id}"
        redis_instance.delete(redis_key)