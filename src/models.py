import uuid
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict
from . import settings
import bcrypt
import jwt

class User(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "nameahex_user"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str = Field(unique=True, index=True, nullable=False)

    password_hash: str

    password_version: int = Field(default=0)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        self.password_version = self.password_version + 1

    def verificar_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )
    
    def generate_jwt(self) -> str:
        return jwt.encode(
            {"user": self.username, "pwd_v": self.password_version}, 
            settings.SECRET_KEY, 
            algorithm="HS256"
        )



class Color(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "nameahex_color"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    hex: str = Field(index=True)


class Option(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "nameahex_option"
    color_id: uuid.UUID = Field(foreign_key="nameahex_color.id", nullable=False, primary_key=True)
    name: str = Field(primary_key=True)

