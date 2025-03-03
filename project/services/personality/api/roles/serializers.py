from pydantic import BaseModel, ConfigDict

from database.mixins import UUIDSerializer


class RoleCreateSerializer(BaseModel):
    """"""

    name: str = None
    description: str | None = None


class RoleUpdateSerializer(RoleCreateSerializer):
    """"""

    model_config = ConfigDict(from_attributes=True)


class RoleReadSerializer(UUIDSerializer, RoleCreateSerializer):
    """"""

    model_config = ConfigDict(from_attributes=True)
