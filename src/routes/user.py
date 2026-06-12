from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import LoginSchema, TokenSchema, UserSchema, UserSchemaWithPassword
from ..database import engine
from ..models import User
from ..dependencies.auth_dep import get_current_user
from sqlmodel import Session, select
from .. import constants
router = APIRouter(
    prefix="/api/user",
    tags=["users"]
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
@router.post(
    "/register",
    response_model=UserSchema,
    summary="Registrarse",
    responses = {
        status.HTTP_409_CONFLICT: {
            "description": "User already exists"
        }
    }
)
async def register(data: UserSchemaWithPassword) -> UserSchema:
    with Session(engine) as session:
        q = select(User).where(User.username == data.username).limit(1)
        if session.exec(q).first() is not None:
            raise constants.USER_ALREADY_EXISTS
        
        user_data = data.model_dump()
        user = User(**user_data)
        user.set_password(data.password)
        session.add(user)
        session.commit()
        session.refresh(user)
    return UserSchema.model_validate(user)
@router.get("/me")
async def me(user: User = Depends(get_current_user)) -> UserSchema:
    return UserSchema.model_validate(user)