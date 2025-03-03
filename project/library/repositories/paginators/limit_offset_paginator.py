from typing import Iterable, Any

from sqlalchemy import Select, select, func
from sqlalchemy.ext.asyncio import AsyncSession


class LimitOffsetRepository:
    """"""

    @classmethod
    async def make_limit_offset_data(cls, data: Any, total: int) -> dict[str, Any]:
        """"""

        return {"count": len(data), "total": total, "results": data}


class LimitOffsetPaginator:

    max_limit = 10

    @classmethod
    async def paginate(cls, query: Select, limit: int, offset: int):
        """"""
        current_limit = [limit, cls.max_limit][limit > cls.max_limit]
        paginated_query = query.limit(current_limit).offset(offset * limit)
        return paginated_query
