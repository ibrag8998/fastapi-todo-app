from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session as SessionType

from ..config.settings import ACCESS_TOKEN_EXPIRES, AUTH_JWT_ALGORITHM, SECRET_KEY
from ..db.base import Session
from ..users.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def get_user(s: SessionType, username: str) -> Optional[User]:
    return s.query(User).filter(User.username == username).first()


def authenticate(s: SessionType, username: str, password: str) -> Optional[User]:
    user = get_user(s, username)
    if user is None:
        return None
    if not user.check_password(password):
        return None
    return user


def create_access_token(data: dict, expires: Optional[timedelta] = None):
    if expires is None:
        expires = ACCESS_TOKEN_EXPIRES

    return jwt.encode(
        {
            **data,
            "exp": datetime.utcnow() + expires,
        },
        SECRET_KEY,
        algorithm=AUTH_JWT_ALGORITHM
    )


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[AUTH_JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    with Session() as s:
        user = get_user(s, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
