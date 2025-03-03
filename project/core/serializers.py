from pydantic import BaseModel, ConfigDict

from database.mixins import UUIDSerializer, TimestampSerializer


class TaskAddSerializer(BaseModel):
    """"""

    name: str
    description: str | None


class TaskReadSerializer(UUIDSerializer, TimestampSerializer, TaskAddSerializer):
    """"""

    model_config = ConfigDict(from_attributes=True)
