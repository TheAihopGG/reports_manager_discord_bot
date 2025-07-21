from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel
from .mixins import IDMixin, GuildIDMixin


class ReportsConfigModel(
    BaseModel,
    IDMixin,
    GuildIDMixin,
):
    """
    ReportsConfigModel contains configuration for reports system, such as channels ids, categories ids and other.
    """

    __tablename__ = "reports_configs"
    logs_channel_id: Mapped[int] = mapped_column(nullable=True, default=None)
    report_tickets_category_id: Mapped[int] = mapped_column(nullable=True, default=None)


__all__ = ("ReportsConfigModel",)
