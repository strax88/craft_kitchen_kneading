from typing import Literal
from uuid import UUID

from fastapi import Request
from sqlalchemy.testing.suite.test_reflection import users

from base_settings import SERVICES_BASE_URL
from library.http_clients.async_http_client import AsyncHTTPClient
from library.http_clients.exceptions import AsyncClientBaseHTTPException
from services.personality.api.users.serializers import UserReadSerializer, PermissionSerializer
from services.personality.models import BaseGroupsEnum, RolesEnum


class CreateRolePermissionMixin:
    """"""

    @classmethod
    async def is_create_role(cls, method, groups: list[PermissionSerializer]):
        """"""
        for group in groups:
            for role in group.group_roles:
                if role.role_name == "CREATE" and method == "POST":
                    return True
        return False


class ReadRolePermissionMixin:
    """"""

    @classmethod
    async def is_read_role(cls, method, groups: list[PermissionSerializer]):
        """"""
        for group in groups:
            for role in group.group_roles:
                if role.role_name == "READ" and method == "GET":
                    return True
        return False


class UpdateRolePermissionMixin:
    """"""

    @classmethod
    async def is_update_role(cls, method, groups: list[PermissionSerializer]):
        """"""
        for group in groups:
            for role in group.group_roles:
                if role.role_name == "UPDATE" and method in ["PUT", "PATCH"]:
                    return True
        return False


class DeleteRolePermissionMixin:
    """"""

    @classmethod
    async def is_delete_role(cls, method, groups: list[PermissionSerializer]):
        """"""
        for group in groups:
            for role in group.group_roles:
                if role.role_name == "DELETE" and method == "DELETE":
                    return True
        return False


class AdministratorPermissionMixin:
    """"""

    @classmethod
    async def is_administrators_group(cls, groups: list[PermissionSerializer]):
        """"""
        for group in groups:
            if group.group_name == "ADMINISTRATORS":
                return True
        return False

    @classmethod
    async def is_root_role(cls, groups: list[PermissionSerializer]):
        """"""
        for group in groups:
            for role in group.group_roles:
                if role.role_name == "ROOT":
                    return True
        return False


class ModeratorsPermissionMixin:
    """"""

    @classmethod
    async def is_moderators_group(cls, groups: list[PermissionSerializer]):
        """"""
        for group in groups:
            if group.group_name == "MODERATORS":
                return True
        return False


class UsersPermissionMixin:
    """"""

    @classmethod
    async def is_users_group(cls, groups: list[PermissionSerializer]):
        """"""
        for group in groups:
            if group.group_name == "USERS":
                return True
        return False


class PermissionBridge(
    AdministratorPermissionMixin,
    CreateRolePermissionMixin,
    ReadRolePermissionMixin,
    UpdateRolePermissionMixin,
    DeleteRolePermissionMixin,
    ModeratorsPermissionMixin,
    UsersPermissionMixin,
):
    """"""

    @classmethod
    async def find_permission(
        cls,
        method: Literal["POST", "GET", "PUT", "PATCH", "DELETE"] | str,
        groups: list[PermissionSerializer],
        required_group: BaseGroupsEnum | None = None,
    ) -> bool:
        """"""
        root_role = await cls.is_root_role(groups)
        if root_role is True:
            return True

        mapped_methods = {
            "POST": cls.is_create_role,
            "GET": cls.is_read_role,
            "PUT": cls.is_update_role,
            "PATCH": cls.is_update_role,
            "DELETE": cls.is_delete_role,
        }
        mapped_groups = {
            "MODERATORS": cls.is_moderators_group,
            "USERS": cls.is_users_group,
        }
        method_permissions_function = mapped_methods[method]
        method_permissions = await method_permissions_function(method, groups)
        admin_group = await cls.is_administrators_group(groups)
        if method_permissions and admin_group:
            return True
        if required_group is not None:
            group_permissions_function = mapped_groups[required_group.value[0]]
            group_permissions = await group_permissions_function(groups)
            return group_permissions and method_permissions
        return method_permissions


class PermissionRepository:
    http_client = AsyncHTTPClient(SERVICES_BASE_URL.auth, {})

    @classmethod
    async def user_access_required(cls, uid: UUID, request: Request):
        """"""
        method = request.method.upper()
        headers = request.headers.mutablecopy()
        current_user, permissions = await cls.get_current_user(headers)
        if current_user.id == uid or await PermissionBridge.find_permission(method, permissions, BaseGroupsEnum.MODERATORS):
            return current_user

    @classmethod
    async def get_current_user(cls, headers) -> tuple[UserReadSerializer, list[PermissionSerializer]]:
        """"""
        try:
            cls.http_client.headers = headers
            data = await cls.http_client.post("/auth/token/current-user")
            return UserReadSerializer.model_validate(data["user_data"]), [
                PermissionSerializer.model_validate(item) for item in data["user_permissions"]
            ]
        except Exception as err_msg:
            raise AsyncClientBaseHTTPException(detail=f"{err_msg}")
