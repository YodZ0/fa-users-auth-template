from typing import TYPE_CHECKING

from fastapi import Request
from jinja2 import Template

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.models.base import Base


if TYPE_CHECKING:
    from src.core.models.users import User
    # from src.core.models.example import Example


class Reference(Base):
    """
    Base class for Reference models.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(50), unique=True)

    # ADMIN REPRESENTATION
    async def __admin_repr__(self, request: Request):
        return self.name

    async def __admin_select2_repr__(self, request: Request) -> str:
        return Template(
            source="<span>{{ name }}</span>",
            autoescape=True,
        ).render(name=self.name)


# ==== General references ====
class Location(Reference):
    __tablename__ = "locations"

    # Relationships
    user: Mapped["User"] = relationship(back_populates="location")


# ==== Specific references ====
class Gender(Reference):
    __tablename__ = "genders"

    # Relationships
    # Add relationships here
    # example: Mapped["Example"] = relationship(back_populates="gender")


class Status(Reference):
    __tablename__ = "statuses"

    # Relationships
    # Add relationships here
    # example: Mapped["Example"] = relationship(back_populates="status")
