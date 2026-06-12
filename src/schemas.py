from typing import Optional
import uuid

from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseSchema):
    username: str
    password: str

class TokenSchema(BaseSchema):
    access_token: str
    token_type: str = "Bearer"

class UserSchema(BaseSchema):
    id: uuid.UUID
    username: str

class UserSchemaWithPassword(UserSchema):
    id: Optional[uuid.UUID] = None
    password: str