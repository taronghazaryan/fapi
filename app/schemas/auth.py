from pydantic import BaseModel, Field, EmailStr, Extra

from typing import List
from uuid import UUID


class CreateUserSchema(BaseModel):
    first_name: str = Field(max_length=32, min_length=2)
    last_name: str = Field(max_length=32, min_length=2)
    email: EmailStr
    username: str = Field(min_length=8, max_length=16)
    password: str = Field(min_length=8, max_length=32)
    password2: str = Field(min_length=8, max_length=32)

    class Config:
        extra = Extra.forbid


class GetUserSchema(CreateUserSchema):
    first_name: str = Field(max_length=32, min_length=2)
    last_name: str = Field(max_length=32, min_length=2)
    email: EmailStr
    username: str = Field(min_length=8, max_length=16)
    #
    # class Config:
    #     orm_mode = True

class GetUsersSchema(BaseModel):
    users: List[GetUserSchema]

    class Config:
        extra = Extra.forbid

class UserSignIn(BaseModel):
    username: str = Field(min_length=8, max_length=16)
    password: str = Field(min_length=8, max_length=32)

    class Config:
        extra = Extra.forbid

