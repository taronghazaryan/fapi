from app.repository.models import UserModel
from app.services.users import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def add(self, data):
        record = UserModel(**data.dict())
        self.session.add(record)

    def _get(self, id_):
        return (self.session.query(UserModel)
                .filter(UserModel.id == str(id_))
                .filter_by(**filters)
                .first())

    def get(self, id_):
        user = self._get(id_)
        if user is not None:
            return User(**user.dict())

    def get_by_email(self, email):
        return (self.session.query(UserModel)
                    .filter(UserModel.email == str(email))
                    .first())

    def get_by_username(self, username):
        return (self.session.query(UserModel)
                    .filter(UserModel.username == str(username))
                    .first())


    def list(self, limit=None, **filters):
        query = self.session.query(UserModel)

        records = query.filter_by(**filters).limit(limit).all()
        return [User(**record.dict()) for record in records]

    def update(self, id_, **payload):
        record = self._get(id_)
        if 'data' in payload:
            for data in record.datas:
                self.session.delete(data)
            record.items = [
                UserModel(**data) for data in payload.pop('datas')
            ]

        for key, value in payload.datas():
            setattr(record, key, value)
        return User(**record.dict())

    def delete(self, id_):
        self.session.delete(self._get(id_))