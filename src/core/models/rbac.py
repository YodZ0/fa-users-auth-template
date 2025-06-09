from typing import List, TYPE_CHECKING

from fastapi import Request
from jinja2 import Template

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.roles import Role


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    permissions: Mapped[List["Permission"]] = relationship(back_populates="action")

    # ADMIN REPRESENTATION
    async def __admin_repr__(self, request: Request):
        return self.name

    async def __admin_select2_repr__(self, request: Request) -> str:
        return Template(
            source="<span>{{ name }}</span>",
            autoescape=True,
        ).render(name=self.name)


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    permissions: Mapped[List["Permission"]] = relationship(back_populates="resource")

    # ADMIN REPRESENTATION
    async def __admin_repr__(self, request: Request):
        return self.name

    async def __admin_select2_repr__(self, request: Request) -> str:
        return Template(
            source="<span>{{ name }}</span>",
            autoescape=True,
        ).render(name=self.name)


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    resource_id: Mapped[int] = mapped_column(
        ForeignKey("resources.id", ondelete="CASCADE")
    )
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id", ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("resource_id", "action_id"),)

    roles: Mapped[List["Role"]] = relationship(
        back_populates="permissions",
        secondary="permissions_roles",
    )
    resource: Mapped["Resource"] = relationship(back_populates="permissions")
    action: Mapped["Action"] = relationship(back_populates="permissions")

    # ADMIN REPRESENTATION
    async def __admin_repr__(self, request: Request):
        return self.name

    async def __admin_select2_repr__(self, request: Request) -> str:
        return Template(
            source="<span>{{ name }}</span>",
            autoescape=True,
        ).render(name=self.name)


class PermissionRole(Base):
    __tablename__ = "permissions_roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
