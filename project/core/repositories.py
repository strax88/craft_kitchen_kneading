from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.serializers import TaskReadSerializer, TaskAddSerializer
from database.engine import get_session
from core.models import TaskORM

class TaskORMRepository:

    @classmethod
    async def add_task(cls, task: TaskAddSerializer, session: AsyncSession) -> UUID:
        """"""
        data = task.model_dump()
        new_task = TaskORM(**data)
        session.add(new_task)
        await session.flush()
        await session.commit()
        return new_task.id


    @classmethod
    async def get_tasks(cls, session) -> list[TaskReadSerializer]:
        """"""
        query = select(TaskORM)
        result = await session.execute(query)
        task_models = result.scalars().all()
        tasks = [TaskReadSerializer.model_validate(task_model) for task_model in task_models]
        return tasks
