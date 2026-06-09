import uuid
from typing import Optional
import os
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict
from . import settings
import hashlib
import hmac
import jwt

class User(SQLModel, table=True):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    __tablename__ = "nameahex_user"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str = Field(unique=True, index=True, nullable=False)

    password_hash: str
    password_version: int = Field(default=0)
    password_salt: str

    def set_password(self, password: str):
        salt_bytes = os.urandom(16)
        password_bytes = password.encode("utf-8")
        key_bytes = settings.SECRET_KEY.encode("utf-8")
        salt_combinada = salt_bytes + key_bytes
        hash_bytes = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password_bytes,
            salt=salt_combinada,
            iterations=settings.ITERATIONS
        )

        self.password_hash = hash_bytes.hex()
        self.password_salt = salt_bytes.hex()
        self.password_version = self.password_version + 1
    def verificar_password(self, password: str):
        salt_bytes = bytes.fromhex(self.password_salt)
        hash_guardado_bytes = bytes.fromhex(self.password_hash)

        password_bytes = password.encode("utf-8")
        key_bytes = settings.SECRET_KEY.encode("utf-8")

        salt_combinada = salt_bytes + key_bytes

        nuevo_hash_bytes = hashlib.pbkdf2_hmac(
            hash_name = 'sha256',
            password = password_bytes,
            salt = salt_combinada,
            iterations= settings.ITERATIONS
        )

        return hmac.compare_digest(nuevo_hash_bytes, hash_guardado_bytes)
    
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

