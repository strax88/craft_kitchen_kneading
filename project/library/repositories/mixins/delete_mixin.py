from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from library.repositories.mixins.base_repository_mixin import BaseRepositoryMixin


class AsyncDeleteRepositoryMixin(BaseRepositoryMixin):
    """"""

    @classmethod
    async def delete(cls, session: AsyncSession, uid: UUID) -> None:
        """"""
        instance = await session.get(cls.model, uid)
        if instance:
            await session.delete(instance)
            await session.commit()