import os
from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from services.auth.exceptions import CredentialHTTPException, InvalidRefreshTokenHTTPException, \
    UserNotFoundHTTPException

SECRET_KEY = os.environ.get("SECRET_KEY", default="my-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class JWTRepository:
    """"""

    @classmethod
    async def create_access_token(cls, data: dict, expires_delta: timedelta | None = None) -> str:
        """"""
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    async def create_refresh_token(cls, data: dict, expires_delta: timedelta | None = None):
        """"""
        to_encode = data.copy()
        expire = datetime.now() + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @classmethod
    async def get_payload(cls, encoded_jwt: str) -> dict[str, str]:
        """"""
        try:
            payload = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise CredentialHTTPException()

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
        """"""
        payload = await JWTRepository.get_payload(token)
        username = payload.get("sub")
        if username is None:
            raise UserNotFoundHTTPException()
        payload.pop("exp")
        payload.pop("sub")
        return payload

    @classmethod
    async def refresh_access_token(cls, refresh_token: str) -> str:
        """"""
        payload = await JWTRepository.get_payload(refresh_token)
        if payload.get("type") != "refresh":
            raise InvalidRefreshTokenHTTPException()
        username = payload.get("sub")
        user = payload.get("user_data")
        groups = payload.get("user_permissions")
        access_token = await cls.create_access_token({"sub": username, "user_data": user, "user_permissions": groups})
        return access_token
