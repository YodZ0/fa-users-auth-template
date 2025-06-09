from typing import List, TYPE_CHECKING

from fastapi import Request
from jinja2 import Template

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.users import User
    from src.core.models.rbac import Permission


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    users: Mapped[List["User"]] = relationship(
        back_populates="roles",
        secondary="users_roles",
    )
    permissions: Mapped[List["Permission"]] = relationship(
        back_populates="roles",
        secondary="permissions_roles",
    )

    # ADMIN REPRESENTATION
    async def __admin_repr__(self, request: Request):
        return self.name

    async def __admin_select2_repr__(self, request: Request) -> str:
        return Template(
            source="<span>{{ name }}</span>",
            autoescape=True,
        ).render(name=self.name)
