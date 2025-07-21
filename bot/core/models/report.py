from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import String

from .base import BaseModel
from .mixins import IDMixin, CreatedAtMixin, GuildIDMixin


class ReportModel(
    BaseModel,
    IDMixin,
    CreatedAtMixin,
    GuildIDMixin,
):
    __tablename__ = "reports"
    author_id: Mapped[int]
    channel_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    message_text: Mapped[str] = mapped_column(String(length=200), nullable=False)


__all__ = ("ReportModel",)
