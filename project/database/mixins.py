from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Column, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as DB_UUID
from database.model import Model


class UUIDModelMixin(Model):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(DB_UUID(as_uuid=True), primary_key=True, default=lambda: uuid4())


class TimestampModelMixin(Model):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True, default=None)


class UUIDSerializer(BaseModel):
    """"""

    id: UUID


class TimestampSerializer(BaseModel):
    """"""

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None
