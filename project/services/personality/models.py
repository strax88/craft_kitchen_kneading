import enum
import os
from datetime import datetime, date

import bcrypt
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import Enum, Table, Column, UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, foreign, relationship

from base_settings import PROJECT_DIR
from database.mixins import UUIDModelMixin, TimestampModelMixin
from database.model import Model
from services.personality.app import APP_PREFIX

# user_group_role_association = Table(
#     "user_group_role",
#     Model.metadata,
#     Column("user_id", UUID, ForeignKey(f"{APP_PREFIX}_user.id")),
#     Column("group_id", UUID, ForeignKey(f"{APP_PREFIX}_group.id")),
#     Column("role_id", UUID, ForeignKey(f"{APP_PREFIX}_role.id")),
# )


class RootUserData(BaseSettings):
    """"""

    username: str = "root"
    password: str = "123456"
    email: str | None = None
    telegram: str | None = None
    phone: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="root_", env_file=f"{PROJECT_DIR}/main.env", env_file_encoding="utf-8", extra="ignore"
    )


ROOT_USER = RootUserData()


class UserORM(UUIDModelMixin, TimestampModelMixin, Model):
    """"""

    __tablename__ = f"{APP_PREFIX}_user"

    email: Mapped[str | None] = mapped_column(unique=True, nullable=True, default=None)
    telegram: Mapped[str | None] = mapped_column(unique=True, nullable=True, default=None)
    phone: Mapped[str | None] = mapped_column(unique=True, nullable=True, default=None)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str]

    def set_password(self, password: str) -> None:
        """"""
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """"""
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    is_active: Mapped[bool] = True
    is_verified: Mapped[bool] = False
    surname: Mapped[str | None]
    name: Mapped[str | None]
    patronymic: Mapped[str | None]
    birthday: Mapped[date | None]


class BaseGroupsEnum(enum.Enum):
    """"""

    ADMINISTRATORS = "ADMINISTRATORS", "Группа администраторов"
    MODERATORS = "MODERATORS", "Группа модераторов"
    USERS = "USERS", "Группа пользователей"


class GroupORM(UUIDModelMixin, Model):
    """"""

    __tablename__ = f"{APP_PREFIX}_group"

    name: Mapped[str]
    description: Mapped[str]


class RolesEnum(enum.Enum):
    """"""

    READ = "READ", "права на чтение"
    CREATE = "CREATE", "права на создание"
    UPDATE = "UPDATE", "права на редактирование"
    DELETE = "DELETE", "права на удаление"
    ROOT = "ROOT", "права на администрирование"


class RoleORM(UUIDModelMixin, Model):
    """"""

    __tablename__ = f"{APP_PREFIX}_role"

    name: Mapped[str] = mapped_column(Enum(RolesEnum), nullable=False)
    description: Mapped[str]


class UserGroupRoleORM(UUIDModelMixin, Model):
    """"""

    __tablename__ = f"{APP_PREFIX}_user_group_role"
    __table_args__ = (UniqueConstraint("user_id", "group_id", "role_id", name="unique_user_group_role"),)

    user_id: Mapped[UUID] = Column("user_id", UUID, ForeignKey(f"{APP_PREFIX}_user.id", ondelete="CASCADE"))
    group_id: Mapped[UUID] = Column("group_id", UUID, ForeignKey(f"{APP_PREFIX}_group.id", ondelete="CASCADE"))
    role_id: Mapped[UUID] = Column("role_id", UUID, ForeignKey(f"{APP_PREFIX}_role.id", ondelete="CASCADE"))
