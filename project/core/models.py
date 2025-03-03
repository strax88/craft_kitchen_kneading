from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column

from core.app import APP_PREFIX
from database.mixins import UUIDModelMixin, TimestampModelMixin
from database.model import Model


class TaskORM(UUIDModelMixin, TimestampModelMixin, Model):
    __tablename__ = f"{APP_PREFIX}_tasks"

    name: Mapped[str]
    description: Mapped[str | None]
