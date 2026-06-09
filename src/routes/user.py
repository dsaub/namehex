from fastapi import APIRouter, HTTPException, status
from ..schemas import LoginSchema, TokenSchema
from ..database import engine
from ..models import User
from sqlmodel import Session, select
from .. import constants
router = APIRouter(
    prefix="/api/user"
)


@router.post(
        "/login",
        response_model=TokenSchema,
        summary="Iniciar sesión",
        responses = {
            403: {
                "description": "El usuario ha fallado el login"
            }
        }
)
async def login(data: LoginSchema) -> TokenSchema:
    username = data.username
    password = data.password

    with Session(engine) as session:
        q = select(User).where(User.username == username).limit(1)
        result = session.exec(q).first()
        if result is None:
            raise constants.INVALID_LOGIN
        if result.verificar_password(password):
            return TokenSchema(access_token=result.generate_jwt())
        else:
            raise constants.INVALID_LOGIN