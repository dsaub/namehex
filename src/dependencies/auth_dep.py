
from typing import Annotated
import jwt
from .. import settings
from ..models import User
from ..database import engine
from sqlmodel import Session, select
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("user")
        password_version = payload.get("pwd_v")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    with Session(engine) as session:
        q = select(User).where(User.username == username and User.password_version == password_version).limit(1)
        result: User | None = session.exec(q).first()
        if not result:
            raise credentials_exception
    return result
    