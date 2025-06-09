import uuid
from typing import Annotated
from fastapi import Depends

from .bearer import AccessToken
from .rbac import RBAC
from ..enums import TokenPayloadFieldsEnum as tf
from ..exceptions import NotEnoughPermissions


async def get_current_user(
    token: AccessToken,
    rbac: RBAC,
) -> uuid.UUID:
    if not await rbac.check_permissions(token):
        raise NotEnoughPermissions
    user_id = token.payload.get(tf.SUB_FIELD)
    return user_id


CurrentUser = Annotated[uuid.UUID, Depends(get_current_user)]
