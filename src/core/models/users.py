import uuid
from typing import List, TYPE_CHECKING

from fastapi import Request
from jinja2 import Template

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.roles import Role
    from src.core.models.auth_token import AuthToken
    from src.core.models.references import Location


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id", ondelete="CASCADE"),
    )

    # RELATIONSHIPS
    roles: Mapped[List["Role"]] = relationship(
        back_populates="users",
        secondary="users_roles",
    )
    tokens: Mapped[List["AuthToken"]] = relationship(
        back_populates="user",
        cascade="save-update, merge, delete",
        passive_deletes=True,
    )
    location: Mapped["Location"] = relationship(back_populates="user")

    # ADMIN REPRESENTATION
    async def __admin_repr__(self, request: Request):
        return self.username

    async def __admin_select2_repr__(self, request: Request) -> str:
        return Template(
            source="<span>{{ username }}</span>",
            autoescape=True,
        ).render(username=self.username)
