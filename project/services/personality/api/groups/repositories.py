from pydantic import BaseModel

from library.repositories import AsyncORMRepository
from services.personality.api.groups.serializers import GroupReadSerializer, GroupUpdateSerializer
from services.personality.models import GroupORM


class GroupORMRepository(AsyncORMRepository):
    """"""

    model: BaseModel = GroupORM
    read_serializer_class = GroupReadSerializer
    update_serializer_class = GroupUpdateSerializer
