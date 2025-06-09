import uuid

from typing import TYPE_CHECKING

from fastapi import Request
from jinja2 import Template

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models.base import Base

if TYPE_CHECKING:
    from src.core.models.users import User


class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    is_used: Mapped[bool] = mapped_column(nullable=False, default=False)
    user: Mapped["User"] = relationship(back_populates="tokens")

    # ADMIN REPRESENTATION
    async def __admin_repr__(self, request: Request):
        return f"TokenId: {self.id} - IsUsed: {self.is_used}"

    async def __admin_select2_repr__(self, request: Request) -> str:
        return Template(
            source="<span>{{ user_email }} - Is used: {{ is_used }}</span>",
            autoescape=True,
        ).render(user_email=self.user.username, is_used=self.is_used)
