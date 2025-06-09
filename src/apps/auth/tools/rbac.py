from typing import Protocol, Annotated
from fastapi import Depends, Request

from ..schemas.tokens import TokenPayload
from ..repositories.permissions import PermissionsRepositoryProtocol
from ..depends import PermissionsRepository

redis_roles = {}


class RBACProtocol(Protocol):
    async def check_permissions(self, token: TokenPayload) -> bool: ...


class RBACImpl:
    def __init__(
        self, repository: PermissionsRepositoryProtocol, request: Request
    ) -> None:
        self.repository = repository
        self.request = request

    async def check_permissions(self, token: TokenPayload) -> bool:
        roles = token.payload.get("roles")

        scope = self.request.scope
        route_name: str = scope["route"].name
        resource, action = tuple(route_name.split("."))

        if redis_roles:
            print("GET FROM REDIS")
            r = redis_roles
        else:
            print("GET FROM DB")
            roles_permissions = await self.repository.get_permissions_map()
            print(roles_permissions)
            # print("SAVE IN REDIS")
            # redis_roles.update(roles_permissions.roles)
            # r = redis_roles
            r = roles_permissions.roles
            print(r)

        for role in roles:
            actions = r.get(role).get(resource)
            if not actions:  # skip role that has no access to resource
                continue
            if action in actions:
                return True
        return False


def get_rbac(repository: PermissionsRepository, request: Request) -> RBACProtocol:
    return RBACImpl(repository=repository, request=request)


RBAC = Annotated[RBACProtocol, Depends(get_rbac)]
