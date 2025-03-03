from typing import Any

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_session
from services.auth.api.repositories import AuthRepository
from services.auth.api.serializers import JWTSerializer
from services.auth.app import APP_PREFIX
from services.auth.security import JWTRepository


class AuthRouter:

    route_prefix = "token"
    router = APIRouter(prefix=f"/{APP_PREFIX}/{route_prefix}", tags=["Авторизация"])

    @staticmethod
    @router.post("")
    async def with_token(
        form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)
    ) -> JWTSerializer:
        """"""
        jwt_auth_data = await AuthRepository.authenticate_user_with_jwt(session, form_data.username, form_data.password)
        return jwt_auth_data

    @staticmethod
    @router.post("/refresh")
    async def refresh_access_token(data: JWTSerializer, session: AsyncSession = Depends(get_session)) -> JWTSerializer:
        """"""
        new_access_token = await AuthRepository.refresh_access_token(data.refresh_token)
        new_data = JWTSerializer(
            refresh_token=data.refresh_token, access_token=new_access_token, token_type=data.token_type
        )
        return new_data

    @staticmethod
    @router.post("/current-user")
    async def get_current_user(current_user = Depends(JWTRepository.get_current_user)) -> Any:
        """"""
        return current_user
