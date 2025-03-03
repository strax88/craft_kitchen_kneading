from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from database.mixins import UUIDSerializer, TimestampSerializer


class UserCreateSerializer(BaseModel):
    """"""

    email: str | None = None
    telegram: str | None = None
    phone: str | None = None
    username: str
    password: str
    is_active: bool = True
    is_verified: bool = False
    surname: str | None = None
    name: str | None = None
    patronymic: str | None = None
    birthday: date | None = None


class UserUpdateSerializer(BaseModel):
    """"""

    email: str | None = None
    telegram: str | None = None
    phone: str | None = None
    username: str | None = Field(default=None, exclude=True)
    password: str | None = None
    is_active: bool = True
    is_verified: bool = False
    surname: str | None = None
    name: str | None = None
    patronymic: str | None = None
    birthday: date | None = None


class UserReadSerializer(UUIDSerializer, TimestampSerializer, UserCreateSerializer):
    """"""

    password: None = Field(None, exclude=True)
    model_config = ConfigDict(from_attributes=True)


class AuthSerializer(BaseModel):
    """"""

    username: str
    password: str


class SubPermissionSerializer(BaseModel):
    role_id: UUID
    role_name: str
    role_description: str | None


class PermissionSerializer(BaseModel):
    """"""

    group_id: UUID
    group_name: str
    group_description: str | None
    group_roles: list[SubPermissionSerializer]

    # model_config = ConfigDict(arbitrary_types_allowed=True)
