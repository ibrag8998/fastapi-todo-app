from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from ..config.settings import ACCESS_TOKEN_EXPIRES, AUTH_JWT_ALGORITHM, SECRET_KEY
from ..db.base import Session
from ..users.models import User
from . import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

r = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


def CredentialsError(detail: str = None) -> HTTPException:
    """
    Designed to use like this:

    >>> raise CredentialsError()
    or
    >>> raise CredentialsError(detail="Invalid username")
    """

    if detail is None:
        detail = "Could not validate credentials"

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_user(s: Session, username: str) -> Optional[User]:
    """
    Get user by username.
    """
    return s.query(User).filter(User.username == username).first()


def authenticate_user(s: Session, username: str, password: str) -> Optional[User]:
    """
    Get user by username, then check if password is valid.
    """

    user = get_user(s, username)
    if user is None:
        return None
    if not user.check_password(password):
        return None
    return user


def create_access_token(sub: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    No validation here. Just create the access token with `sub` (username) given.
    """

    if expires_delta is None:
        expires_delta = ACCESS_TOKEN_EXPIRES

    return jwt.encode(
        {
            'sub': sub,
            'exp': datetime.utcnow() + expires_delta,
        },
        key=SECRET_KEY,
        algorithm=AUTH_JWT_ALGORITHM,
    )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get current user based on token got from `oauth2_scheme`.
    This function returns you the current user, which is logged in and exists in database, or raises an error.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[AUTH_JWT_ALGORITHM])
    except JWTError:
        raise CredentialsError()

    username = payload.get("sub")
    if username is None:
        raise CredentialsError()

    with Session() as s:
        user = get_user(s, username)

    if user is None:
        raise CredentialsError()

    return user


@r.post("/token", response_model=schemas.Token)
async def obtain_access_token(data: OAuth2PasswordRequestForm = Depends()):
    with Session() as s:
        user = authenticate_user(s, data.username, data.password)

    if not user:
        raise CredentialsError()

    access_token = create_access_token(sub=user.username, expires_delta=ACCESS_TOKEN_EXPIRES)

    return {"access_token": access_token, "token_type": "bearer"}
