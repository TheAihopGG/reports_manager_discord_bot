from sqlalchemy.orm import mapped_column, Mapped

from .base import BaseModel
from .mixins import IDMixin, GuildIDMixin


class ReportsAdminRoleModel(
    BaseModel,
    IDMixin,
    GuildIDMixin,
):
    __tablename__ = "reports_admins"
    role_id: Mapped[int] = mapped_column(nullable=False, unique=True)
