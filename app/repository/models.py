import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class UserModel(Base):

    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String(32), nullable=False, unique=True)
    username = Column(String(32), nullable=False, unique=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    password = Column(String(32), nullable=False)
    verified = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())

    def dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
            "created": self.created,
            "updated": self.updated,
        }

class DialogModel(Base):
    __tablename__ = 'dialog'

    id = Column(String, primary_key=True, default=generate_uuid)
    from_user = Column(String, ForeignKey('users.id'), nullable=False)
    to_user = Column(String, ForeignKey('users.id'), nullable=False)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())

    def dict(self):
        return {
            'id': self.id,
            'from_user': self.from_user,
            'to_user': self.to_user,
            "created": self.created,
            "updated": self.updated,
        }

class MessageModel(Base):

    __tablename__ = 'messages'

    id = Column(String, primary_key=True, default=generate_uuid)
    dialog_id = Column(String, ForeignKey('dialog.id'),  nullable=False)
    from_user = Column(String, ForeignKey('users.id'), nullable=False)
    message = Column(String, nullable=False)
    viewed = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now())

    def dict(self):
        return {
            'id': self.id,
            'dialog_id': self.dialog_id,
            'from_user': self.from_user,
            'message': self.message,
            'viewed': self.viewed,
            "created": self.created,
            "updated": self.updated,
        }
