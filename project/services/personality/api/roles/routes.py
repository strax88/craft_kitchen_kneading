from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status
from pydantic import BaseModel

from database.engine import get_session
from services.personality.api.roles.serializers import RoleCreateSerializer, RoleReadSerializer, RoleUpdateSerializer
from services.personality.app import APP_PREFIX
from services.personality.api.roles.repositories import RoleORMRepository


class RoleRouter:
    """"""

    route_prefix = "roles"
    router = APIRouter(
        prefix=f"/{APP_PREFIX}/{route_prefix}",
        tags=["Управление ролями"],
    )

    @staticmethod
    @router.post("", status_code=status.HTTP_201_CREATED)
    async def create(instance: RoleCreateSerializer = Depends(), session=Depends(get_session)) -> dict[str, UUID]:
        uid = await RoleORMRepository.create(session, instance)
        return {"id": uid}

    @staticmethod
    @router.get("")
    async def read(
        limit: int | None = None, offset: int | None = None, session=Depends(get_session)
    ) -> list[RoleReadSerializer | BaseModel] | dict[str, int | None | list[RoleReadSerializer | BaseModel]]:
        instances = await RoleORMRepository.read(session, limit, offset)
        return instances

    @staticmethod
    @router.get("/{uid}")
    async def read_one(uid: UUID, session=Depends(get_session)) -> RoleReadSerializer | BaseModel:
        instance = await RoleORMRepository.read_one(session, uid)
        return instance

    @staticmethod
    @router.put("/{uid}")
    async def update(
        cls, uid: UUID, instance: RoleUpdateSerializer = Depends(), session=Depends(get_session)
    ) -> RoleReadSerializer | BaseModel:
        instance = await RoleORMRepository.update(session, uid, instance, "put")
        return instance

    @staticmethod
    @router.patch("/{uid}")
    async def update(uid: UUID, instance: dict, session=Depends(get_session)) -> RoleReadSerializer | BaseModel:
        instance = await RoleORMRepository.update(session, uid, instance, "patch")
        return instance

    @staticmethod
    @router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(uid: UUID, session=Depends(get_session)) -> None:
        await RoleORMRepository.delete(session, uid)
