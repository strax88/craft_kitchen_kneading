from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from library.repositories.mixins.base_repository_mixin import BaseRepositoryMixin
from library.repositories.paginators.limit_offset_paginator import LimitOffsetRepository


class AsyncReadRepositoryMixin(BaseRepositoryMixin):
    """"""

    @classmethod
    async def read(
        cls, session: AsyncSession, limit: int | None = None, offset: int | None = None
    ) -> list[BaseModel] | dict:
        """"""
        query = select(cls.model)
        if cls.paginator and limit is not None and offset is not None:
            total_query = select(func.count()).select_from(query.subquery())
            paginated_query = await cls.paginator.paginate(query, limit, offset)
            total = await session.scalar(total_query)
            executed_results = await session.execute(paginated_query)
            instances = executed_results.scalars().all()
            return await LimitOffsetRepository.make_limit_offset_data(instances, total)
        else:
            execute_result = await session.execute(query)
            instances = execute_result.scalars().all()
            instances = [cls.read_serializer_class.model_validate(item) for item in instances]
            return instances

    @classmethod
    async def read_one(cls, session: AsyncSession, uid: UUID) -> BaseModel:
        """"""
        instance = await session.get(cls.model, uid)
        if instance:
            return cls.read_serializer_class.model_validate(instance)
