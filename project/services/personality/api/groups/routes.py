from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status
from pydantic import BaseModel

from database.engine import get_session
from services.personality.api.groups.serializers import (
    GroupCreateSerializer,
    GroupReadSerializer,
    GroupUpdateSerializer,
)
from services.personality.app import APP_PREFIX
from services.personality.api.groups.repositories import GroupORMRepository


class GroupRouter:
    """"""

    route_prefix = "groups"
    router = APIRouter(
        prefix=f"/{APP_PREFIX}/{route_prefix}",
        tags=["Управление группами"],
    )

    @staticmethod
    @router.post("", status_code=status.HTTP_201_CREATED)
    async def create(instance: GroupCreateSerializer = Depends(), session=Depends(get_session)) -> dict[str, UUID]:
        uid = await GroupORMRepository.create(session, instance)
        return {"id": uid}

    @staticmethod
    @router.get("")
    async def read(
        limit: int | None = None, offset: int | None = None, session=Depends(get_session)
    ) -> list[GroupReadSerializer | BaseModel] | dict[str, int | None | list[GroupReadSerializer | BaseModel]]:
        instances = await GroupORMRepository.read(session, limit, offset)
        return instances

    @staticmethod
    @router.get("/{uid}")
    async def read_one(uid: UUID, session=Depends(get_session)) -> GroupReadSerializer | BaseModel:
        instance = await GroupORMRepository.read_one(session, uid)
        return instance

    @staticmethod
    @router.put("/{uid}")
    async def update(
        cls, uid: UUID, instance: GroupUpdateSerializer = Depends(), session=Depends(get_session)
    ) -> GroupReadSerializer | BaseModel:
        instance = await GroupORMRepository.update(session, uid, instance, "put")
        return instance

    @staticmethod
    @router.patch("/{uid}")
    async def update(uid: UUID, instance: dict, session=Depends(get_session)) -> GroupReadSerializer | BaseModel:
        instance = await GroupORMRepository.update(session, uid, instance, "patch")
        return instance

    @staticmethod
    @router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(uid: UUID, session=Depends(get_session)) -> None:
        await GroupORMRepository.delete(session, uid)
