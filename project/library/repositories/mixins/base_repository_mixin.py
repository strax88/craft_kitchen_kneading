from typing import Type

from pydantic import BaseModel

from database.mixins import UUIDModelMixin
from database.model import Model
from library.repositories.paginators import LimitOffsetPaginator


class BaseRepositoryMixin:

    model: Type[UUIDModelMixin | Model] = None
    read_serializer_class: BaseModel = None
    update_serializer_class: BaseModel = None
    create_serializer_class: BaseModel | None = None
    paginator = LimitOffsetPaginator
