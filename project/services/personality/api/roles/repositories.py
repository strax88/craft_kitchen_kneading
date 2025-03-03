from pydantic import BaseModel

from library.repositories import AsyncORMRepository
from services.personality.api.roles.serializers import RoleReadSerializer, RoleUpdateSerializer
from services.personality.models import RoleORM


class RoleORMRepository(AsyncORMRepository):
    """"""

    model: BaseModel = RoleORM
    read_serializer_class = RoleReadSerializer
    update_serializer_class = RoleUpdateSerializer
