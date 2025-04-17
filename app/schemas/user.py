from pydantic import BaseModel, Field, EmailStr


class ProfileSchema(BaseModel):
    username: str = Field(min_length=8, max_length=16)
    email: EmailStr
    first_name: str = Field(max_length=32, min_length=2)
    last_name: str = Field(max_length=32, min_length=2)

