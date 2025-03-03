from cgitb import reset
from typing import Any
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from library.repositories import AsyncORMRepository
from services.personality.api.groups.serializers import GroupReadSerializer
from services.personality.api.roles.serializers import RoleReadSerializer
from services.personality.api.users.serializers import (
    UserReadSerializer,
    UserUpdateSerializer,
    PermissionSerializer,
    SubPermissionSerializer,
)
from services.personality.models import UserORM, UserGroupRoleORM, GroupORM, RoleORM


class UserORMRepository(AsyncORMRepository):
    """"""

    model: BaseModel = UserORM
    read_serializer_class = UserReadSerializer
    update_serializer_class = UserUpdateSerializer

    @classmethod
    async def create(cls, session: AsyncSession, serializer: BaseModel) -> UUID:
        """"""
        model_data = serializer.model_dump()
        password = model_data.pop("password")
        instance = cls.model(**model_data)
        instance.set_password(password)
        session.add(instance)
        await session.flush()
        await session.commit()
        return UUID(str(instance.id))

    @classmethod
    async def add_user_to_group_with_role(cls, session, user_id: UUID, group_id: UUID, role_ids: list[UUID]) -> None:
        """"""
        for role_id in role_ids:
            user_group_role = UserGroupRoleORM(user_id=user_id, group_id=group_id, role_id=role_id)
            session.add(user_group_role)
        await session.flush()
        await session.commit()

    @classmethod
    async def read_groups_with_roles(cls, session, user_id: UUID) -> list[PermissionSerializer]:
        """"""
        query = select(UserGroupRoleORM).filter(UserGroupRoleORM.user_id == user_id)
        execute_result = await session.execute(query)
        relations = execute_result.scalars().all()

        group_ids = list(set(item.group_id for item in relations))
        role_ids = list(set(item.role_id for item in relations))

        roles_query = select(RoleORM).filter(RoleORM.id.in_(role_ids))
        roles_result = await session.execute(roles_query)
        roles = roles_result.scalars().all()
        roles_dict = {
            str(role.id): SubPermissionSerializer(
                role_id=role.id,
                role_name=role.name.value[0],
                role_description=role.description,
            )
            for role in roles
        }

        groups_query = select(GroupORM).filter(GroupORM.id.in_(group_ids))
        groups_result = await session.execute(groups_query)
        groups = groups_result.scalars().all()

        result = []
        for group in groups:
            group_roles = [roles_dict[str(relation.role_id)] for relation in relations if relation.group_id == group.id]
            serialized_group = PermissionSerializer(
                group_id=group.id, group_name=group.name, group_description=group.description, group_roles=group_roles
            )
            # group_data = {"group_id": group.id, "group_name": group.name, "group_description": group.description, "group_roles": group_roles}
            result.append(serialized_group)

        return result

    @classmethod
    async def change_password(cls, instance: UserORM, value: Any) -> None:
        """"""
        instance.set_password(value)

    @classmethod
    async def update_by_field(cls, instance: UserORM, field: str, value: Any) -> None:
        """"""
        if field == "password":
            return await cls.change_password(instance, value)
        current_value = getattr(instance, field)
        if value != current_value:
            setattr(instance, field, value)

    @classmethod
    async def delete(cls, session: AsyncSession, uid: UUID) -> None:
        """"""
        instance = await session.get(cls.model, uid)
        if instance.username == "root":
            raise HTTPException(status_code=400, detail=f"You can't drop 'root' user.")
        if instance:
            await session.delete(instance)
            await session.commit()

    @classmethod
    async def read_groups(cls, session: AsyncSession, uid: UUID) -> list[GroupReadSerializer]:
        """"""
        query = select(UserGroupRoleORM).filter(UserGroupRoleORM.user_id == uid)
        execute_result = await session.execute(query)
        relations = execute_result.scalars().all()
        group_ids = [item.group_id for item in relations]
        query = select(GroupORM).filter(GroupORM.id.in_(group_ids))
        execute_result = await session.execute(query)
        instances = execute_result.scalars().all()
        instances = [GroupReadSerializer.model_validate(item) for item in instances]
        return instances

    @classmethod
    async def read_roles(cls, session: AsyncSession, uid: UUID) -> list[RoleReadSerializer]:
        """"""
        query = select(UserGroupRoleORM).filter(UserGroupRoleORM.user_id == uid)
        execute_result = await session.execute(query)
        relations = execute_result.scalars().all()
        role_ids = [item.role_id for item in relations]
        query = select(RoleORM).filter(RoleORM.id.in_(role_ids))
        execute_result = await session.execute(query)
        instances = execute_result.scalars().all()
        instances = [RoleReadSerializer.model_validate(item) for item in instances]
        return instances

    @classmethod
    async def auth(cls, session, username, password) -> UserReadSerializer:
        """"""
        query = select(UserORM).filter(UserORM.username == username)
        execute_result = await session.execute(query)
        user = execute_result.scalar_one_or_none()
        if user:
            assert user.check_password(password)
            return UserReadSerializer.model_validate(user)
