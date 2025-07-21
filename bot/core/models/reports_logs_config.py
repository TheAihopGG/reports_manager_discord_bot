from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel
from .mixins import IDMixin, GuildIDMixin


class ReportsLogsConfigModel(
    BaseModel,
    IDMixin,
    GuildIDMixin,
):
    """
    ReportsLogsConfigModel provides fields to ignore certain logs types.
    """

    __tablename__ = "reports_logs_configs"
    record_report_sended: Mapped[int] = mapped_column(nullable=False, default=True)
    record_report_closed: Mapped[int] = mapped_column(nullable=False, default=True)
    record_member_added_to_report_ticket: Mapped[int] = mapped_column(nullable=False, default=True)
    record_member_removed_from_report_ticket: Mapped[int] = mapped_column(nullable=False, default=True)
    record_reports_admin_added: Mapped[int] = mapped_column(nullable=False, default=True)
    record_reports_admin_removed: Mapped[int] = mapped_column(nullable=False, default=True)


__all__ = ("ReportsLogsConfigModel",)
