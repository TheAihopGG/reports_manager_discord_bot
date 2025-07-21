from datetime import datetime
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy import func


class IDMixin:
    @declared_attr
    def id(cls) -> Mapped[int]:
        return mapped_column(primary_key=True, index=True)


class GuildIDMixin:
    @declared_attr
    def guild_id(cls) -> Mapped[int]:
        return mapped_column(nullable=False, unique=True)


class CreatedAtMixin:
    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(default=func.now)


class UpdatedAtMixin:
    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(default=func.now, onupdate=func.now)


__all__ = (
    "IDMixin",
    "GuildIDMixin",
    "CreatedAtMixin",
    "UpdatedAtMixin",
)
