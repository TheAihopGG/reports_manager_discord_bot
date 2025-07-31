from typing import TYPE_CHECKING
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import JSON

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
    is_reports_enabled: Mapped[bool] = mapped_column(nullable=False, default=True)
    is_logs_enabled: Mapped[bool] = mapped_column(nullable=False, default=True)
    logs_channel_id: Mapped[int] = mapped_column(nullable=True, default=None)
    report_tickets_category_id: Mapped[int] = mapped_column(nullable=True, default=None)
    enabled_logs_types: Mapped[dict[str, bool]] = mapped_column(
        JSON(none_as_null=True),
        default=lambda: {},
    )


__all__ = ("ReportsConfigModel",)
