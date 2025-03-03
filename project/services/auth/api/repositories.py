from sqlalchemy.ext.asyncio import AsyncSession

from base_settings import SERVICES_BASE_URL
from library.http_clients.async_http_client import AsyncHTTPClient
from services.auth.api.serializers import JWTSerializer
from services.auth.exceptions import CredentialHTTPException, IncorrectUsernamePasswordHTTPException
from services.auth.security import JWTRepository


class AuthRepository:
    http_client = AsyncHTTPClient(SERVICES_BASE_URL.user, {})

    @classmethod
    async def get_personality(cls, session, username, password) -> tuple:
        """"""
        # todo: получение данных из API personality / из очереди
        try:
            data = await cls.http_client.post(
                "/personality/users/auth", data={"username": username, "password": password}
            )
        except Exception as err_msg:
            raise CredentialHTTPException
        return data.get("user"), data.get("groups")

    @classmethod
    async def authenticate_user_with_jwt(cls, session: AsyncSession, username: str, password: str) -> JWTSerializer:
        """"""
        user, groups = await cls.get_personality(session, username, password)
        if not user:
            raise IncorrectUsernamePasswordHTTPException()
        data = {"sub": user["username"], "user_data": user, "user_permissions": groups}
        access_token = await JWTRepository.create_access_token(data)
        refresh_token = await JWTRepository.create_refresh_token(data)
        return JWTSerializer(**{"access_token": access_token, "token_type": "Bearer", "refresh_token": refresh_token})

    @classmethod
    async def refresh_access_token(cls, refresh_token: str) -> str:
        """"""
        access_token = await JWTRepository.refresh_access_token(refresh_token)
        return access_token
