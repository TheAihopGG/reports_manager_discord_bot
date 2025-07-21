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
    is_closed: Mapped[bool] = mapped_column(default=False)
    result_text: Mapped[str] = mapped_column(String(length=200), nullable=True)


__all__ = ("ReportModel",)
