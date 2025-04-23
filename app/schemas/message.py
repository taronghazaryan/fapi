from pydantic import BaseModel, Field

class DialogSchema(BaseModel):
    from_user: str = Field(max_length=45)
    to_user: str = Field(max_length=45)

class MessageSchema(BaseModel):
    dialog_id: str = Field(max_length=45)
    from_user: str = Field(max_length=45)
    message: str = Field(max_length=255)

class WSConnectionDTO(BaseModel):
    dialog_id: str
    from_user: str
