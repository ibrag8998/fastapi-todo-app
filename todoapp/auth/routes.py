from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..config import settings
from ..db.base import Session
from . import schemas
from .auth import CredentialsError, authenticate_user, create_access_token

r = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@r.post("/token", response_model=schemas.Token)
async def obtain_access_token(data: OAuth2PasswordRequestForm = Depends()):
    with Session() as s:
        user = authenticate_user(s, data.username, data.password)

    if not user:
        raise CredentialsError()

    access_token = create_access_token(sub=user.username, expires_delta=settings.ACCESS_TOKEN_EXPIRES)

    return {"access_token": access_token, "token_type": "bearer"}


auth_router = r
