from disnake import MessageInteraction, ButtonStyle
from disnake.ui import button, View, Button

from ...core.models import ReportModel, ReportsConfigModel
from ...core.database import session_factory
from ...core.base_embeds import InfoEmbed
from ...core.embeds import not_enough_permissions_embed
from ...services.reports_service import is_reports_admin
from ...services.logs_service import ReportClosed, send_log


class ConfirmReportCloseView(View):
    def __init__(
        self,
        *,
        report: ReportModel,
        reports_config: ReportsConfigModel,
    ):
        super().__init__(
            timeout=30,
        )
        self.report = report
        self.reports_config = reports_config

    @button(style=ButtonStyle.primary, label="Confirm")
    async def confirm_button_callback(
        self,
        button: Button,
        inter: MessageInteraction,
    ) -> None:
        async with session_factory() as session:
            if inter.author.guild_permissions.administrator or await is_reports_admin(
                session,
                guild_id=inter.guild_id,
                member=inter.author,
            ):
                if self.report.is_closed:
                    await inter.response.send_message(
                        embed=InfoEmbed(description="The report has already closed."),
                        ephemeral=True,
                    )
                else:
                    self.report.is_closed = True
                    if report_channel := inter.guild.get_channel(self.report.channel_id):
                        await report_channel.delete()
                    await session.commit()
                    await session.refresh(self.report)
                    await send_log(
                        session,
                        inter,
                        reports_config=self.reports_config,
                        log_type=ReportClosed(report=self.report),
                    )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )


__all__ = ("ConfirmReportCloseView",)
