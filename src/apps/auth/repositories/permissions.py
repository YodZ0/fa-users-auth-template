from collections import defaultdict
from sqlalchemy import select

from src.core.repositories.db_repository import (
    DBRepositoryProtocol,
    DBRepositoryImpl,
)
from src.core.models.rbac import PermissionRole, Permission, Resource, Action
from src.core.models.roles import Role

from ..enums import ResourcesEnum, ActionsEnum
from ..schemas.rbac import (
    PermissionReadSchema,
    PermissionCreateSchema,
    PermissionUpdateSchema,
    AccessControlMap,
)


class PermissionsRepositoryProtocol(
    DBRepositoryProtocol[
        PermissionRole,
        PermissionReadSchema,
        PermissionCreateSchema,
        PermissionUpdateSchema,
    ],
):
    async def get_permissions_map(self) -> AccessControlMap: ...


class PermissionsRepositoryImpl(
    PermissionsRepositoryProtocol,
    DBRepositoryImpl[
        PermissionRole,
        PermissionReadSchema,
        PermissionCreateSchema,
        PermissionUpdateSchema,
    ],
):
    model_type = PermissionRole
    read_schema_type = PermissionReadSchema

    async def get_permissions_map(self) -> AccessControlMap:
        async with self.session as s:
            statement = (
                select(
                    PermissionRole.id,
                    Role.name,
                    Resource.name,
                    Action.name,
                )
                .join(Role, PermissionRole.role_id == Role.id)
                .join(Permission, PermissionRole.permission_id == Permission.id)
                .join(Resource, Permission.resource_id == Resource.id)
                .join(Action, Permission.action_id == Action.id)
            )
            models = (await s.execute(statement)).all()
            acl = parse_permissions(models)
            return acl


def parse_permissions(raw_data: list[tuple[int, str, str, str]]) -> AccessControlMap:
    permissions_map: dict[str, dict[ResourcesEnum, set[ActionsEnum]]] = defaultdict(
        lambda: defaultdict(set)
    )

    for _, role, resource, action in raw_data:
        resource_enum = ResourcesEnum(resource)
        action_enum = ActionsEnum(action)
        permissions_map[role][resource_enum].add(action_enum)

    return AccessControlMap(
        roles={
            role: {res: list(actions) for res, actions in resources.items()}
            for role, resources in permissions_map.items()
        }
    )
