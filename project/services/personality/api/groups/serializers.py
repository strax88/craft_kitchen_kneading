from pydantic import BaseModel, ConfigDict

from database.mixins import UUIDSerializer


class GroupCreateSerializer(BaseModel):
    """"""

    name: str = None
    description: str | None = None


class GroupUpdateSerializer(GroupCreateSerializer):
    """"""

    model_config = ConfigDict(from_attributes=True)


class GroupReadSerializer(UUIDSerializer, GroupCreateSerializer):
    """"""

    model_config = ConfigDict(from_attributes=True)
