from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import status

from core.app import APP_PREFIX
from core.repositories import TaskORMRepository
from core.serializers import TaskAddSerializer, TaskReadSerializer
from database.mixins import UUIDSerializer
from database.engine import get_session

router = APIRouter(
    prefix=f"/{APP_PREFIX}",
    tags=["Таски"],
)


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def add_task(task: TaskAddSerializer = Depends(), session=Depends(get_session)) -> dict[str, UUID]:
    new_task_id = await TaskORMRepository.add_task(task, session)
    return {"id": new_task_id}


@router.get("/tasks")
async def get_tasks(session=Depends(get_session)) -> list[TaskReadSerializer]:
    tasks = await TaskORMRepository.get_tasks(session)
    return tasks
