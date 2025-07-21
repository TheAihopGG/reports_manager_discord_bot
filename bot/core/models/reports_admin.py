from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel
from .mixins import IDMixin, GuildIDMixin


class ReportsAdminModel(
    BaseModel,
    IDMixin,
    GuildIDMixin,
):
    __tablename__ = "reports_admins"
    admin_id: Mapped[int] = mapped_column(nullable=False, unique=True)
