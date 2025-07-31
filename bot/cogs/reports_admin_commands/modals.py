from disnake import TextInputStyle, ModalInteraction
from disnake.ui import Modal, TextInput
from sqlalchemy import select

from .views import ConfirmReportCloseView
from ...core.models import ReportModel, ReportsConfigModel
from ...core.database import session_factory
from ...core.base_embeds import InfoEmbed, SuccessEmbed, ErrorEmbed
from ...core.errors import UnknownGuildError
from ...services.reports_service import get_reports_config_by_guild_id
from ...services.logs_service import ReportClosed, send_log


class GetReportResult(Modal):
    def __init__(
        self,
        *,
        report: ReportModel,
        reports_config: ReportsConfigModel,
    ):
        super().__init__(
            title="Report result",
            components=TextInput(
                label="Result text",
                style=TextInputStyle.paragraph,
                placeholder="Enter result text",
                required=True,
            ),
        )
        self.report = report
        self.reports_config = reports_config

    async def callback(self, inter: ModalInteraction) -> None:
        await inter.response.defer()
        await inter.response.send_message(
            embed=InfoEmbed(description="Do you really want to close the report?"),
            view=ConfirmReportCloseView(
                report=self.report,
                reports_config=self.reports_config,
            ),
            ephemeral=True,
        )


__all__ = ("GetReportResult",)
