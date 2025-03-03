from typing import Any, Literal
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status
from pydantic import BaseModel

from database.engine import get_session
from services.personality.api.permission_repository import PermissionRepository
from services.personality.api.groups.serializers import GroupReadSerializer
from services.personality.api.roles.serializers import RoleReadSerializer
from services.personality.api.users.serializers import (
    UserCreateSerializer,
    UserReadSerializer,
    UserUpdateSerializer,
    AuthSerializer,
    PermissionSerializer,
)
from services.personality.app import APP_PREFIX
from services.personality.api.users.repositories import UserORMRepository


class UserRouter:
    """"""

    route_prefix = "users"
    router = APIRouter(
        prefix=f"/{APP_PREFIX}/{route_prefix}",
        tags=["Управление пользователями"],
    )

    @staticmethod
    @router.post("", status_code=status.HTTP_201_CREATED)
    async def create(instance: UserCreateSerializer = Depends(), session=Depends(get_session)) -> dict[str, UUID]:
        uid = await UserORMRepository.create(session, instance)
        return {"id": uid}

    @staticmethod
    @router.get("")
    async def read(
        limit: int | None = None, offset: int | None = None, session=Depends(get_session)
    ) -> list[UserReadSerializer | BaseModel] | dict[str, int | None | list[UserReadSerializer | BaseModel]]:
        instances = await UserORMRepository.read(session, limit, offset)
        return instances

    @staticmethod
    @router.post("/auth")
    async def auth(
        auth_data: AuthSerializer, session=Depends(get_session)
    ) -> dict[Literal["user", "groups"], UserReadSerializer | BaseModel | list[PermissionSerializer]]:
        user = await UserORMRepository.auth(session, auth_data.username, auth_data.password)
        groups = await UserRouter.read_groups_and_roles(user.id, session)
        return {"user": user, "groups": groups}

    @staticmethod
    @router.post("/{uid}/permissions", status_code=status.HTTP_202_ACCEPTED)
    async def add_user_to_group_with_role(
        uid: UUID, group_id: UUID, role_ids: list[UUID], session=Depends(get_session)
    ) -> None:
        await UserORMRepository.add_user_to_group_with_role(session, uid, group_id, role_ids)

    @staticmethod
    @router.get("/{uid}/permissions")
    async def read_groups_and_roles(
        uid: UUID, session=Depends(get_session), current_user=Depends(PermissionRepository.user_access_required)
    ) -> list[PermissionSerializer]:
        return await UserORMRepository.read_groups_with_roles(session, uid)

    @staticmethod
    @router.get("/{uid}/groups")
    async def read_groups(uid: UUID, session=Depends(get_session)) -> list[GroupReadSerializer | BaseModel]:
        instances = await UserORMRepository.read_groups(session, uid)
        return instances

    @staticmethod
    @router.get("/{uid}/roles")
    async def read_roles(uid: UUID, session=Depends(get_session)) -> list[RoleReadSerializer | BaseModel]:
        instances = await UserORMRepository.read_roles(session, uid)
        return instances

    @staticmethod
    @router.get("/{uid}")
    async def read_one(uid: UUID, session=Depends(get_session)) -> UserReadSerializer | BaseModel:
        instance = await UserORMRepository.read_one(session, uid)
        return instance

    @staticmethod
    @router.put("/{uid}")
    async def update(
        cls, uid: UUID, instance: UserUpdateSerializer = Depends(), session=Depends(get_session)
    ) -> UserReadSerializer | BaseModel:
        instance = await UserORMRepository.update(session, uid, instance, "put")
        return instance

    @staticmethod
    @router.patch("/{uid}")
    async def update(uid: UUID, instance: dict, session=Depends(get_session)) -> UserReadSerializer | BaseModel:
        instance = await UserORMRepository.update(session, uid, instance, "patch")
        return instance

    @staticmethod
    @router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(uid: UUID, session=Depends(get_session)) -> None:
        await UserORMRepository.delete(session, uid)
