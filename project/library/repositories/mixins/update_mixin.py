from typing import Any
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from library.repositories.mixins.base_repository_mixin import BaseRepositoryMixin


class AsyncUpdateRepositoryMixin(BaseRepositoryMixin):
    """"""

    @classmethod
    async def update_by_field(cls, instance: Any, field: str, value: Any) -> None:
        """"""
        current_value = getattr(instance, field)
        if value != current_value:
            setattr(instance, field, value)

    @classmethod
    async def full_update(cls, instance: Any, serializer: BaseModel) -> None:
        """"""
        for field, value in serializer.model_dump().items():
            await cls.update_by_field(instance, field, value)

    @classmethod
    async def partial_update(cls, instance: Any, data: dict[str, Any]) -> None:
        """"""
        cls.update_serializer_class.model_validate(data)
        for field, value in data.items():
            await cls.update_by_field(instance, field, value)

    @classmethod
    async def update(
        cls, session: AsyncSession, uid: UUID, serializer: BaseModel | dict[str, Any], method: str = "put"
    ) -> BaseModel:
        """"""
        strategies = {"put": cls.full_update, "patch": cls.partial_update}
        instance = await session.get(cls.model, uid)
        strategy = strategies[method]
        await strategy(instance, serializer)
        await session.flush()
        await session.commit()
        instance = await session.get(cls.model, uid)
        return cls.read_serializer_class.model_validate(instance)
