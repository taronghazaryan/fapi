from app.exeptions import UserNotFoundError, UserAlreadyExistsError, PasswordMismatch
from app.repository.models import UserModel
from app.core.security import hash_password, verify_password

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def place_user(self, data):
        if data.password != data.password2:
            raise PasswordMismatch(
                "Passwords do not match"
            )

        if self.user_repository.get_by_email(data.email):
            raise UserAlreadyExistsError(
                f"User with email: {data.email} already exist"
            )

        if self.user_repository.get_by_username(data.username):
            raise UserAlreadyExistsError(
                f"User with username: {data.username} already exist"
            )

        user = UserModel(
            email=data.email,
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            password=hash_password(data.password)
        )

        self.user_repository.add(user)
        return user

    def authenticate(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)
        if user and verify_password(password, user.password):
            return user
        return None

    def get_user(self, user_id):
        user = self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id:{user_id} not found.")
        return user

    def get_user_by_email(self, email):
        user = self.user_repository.get_by_email(email)
        if user is None:
            raise UserNotFoundError(f"User with email:{email} not found.")
        return user

    def update_user(self, user_id, data: dict):
        user = self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundError(f"User with id:{user_id} not found.")
        return self.user_repository.update(user_id, data)

    def list_users(self, **filters):
        limit = filters.pop('limit', None)
        return self.user_repository.list(limit=limit, **filters)
