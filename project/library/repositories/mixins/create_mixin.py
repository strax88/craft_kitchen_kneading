from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from library.repositories.mixins.base_repository_mixin import BaseRepositoryMixin


class AsyncCreateRepositoryMixin(BaseRepositoryMixin):
    """"""

    @classmethod
    async def create(cls, session: AsyncSession, serializer: BaseModel) -> UUID:
        """"""
        model_data = serializer.model_dump()
        instance = cls.model(**model_data)
        session.add(instance)
        await session.flush()
        await session.commit()
        return UUID(str(instance.id))
