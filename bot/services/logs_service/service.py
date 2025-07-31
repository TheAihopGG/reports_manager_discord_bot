from disnake import AppCmdInter
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.models import ReportsConfigModel
from .logs_types import BaseLogsType


async def send_log(
    session: AsyncSession,
    inter: AppCmdInter,
    *,
    reports_config: ReportsConfigModel,
    log_type: BaseLogsType,
) -> None:
    """
    Sends log to logs channel. It checks, does logs enabled, does logs channel exists, if the logs channel is not exists it sets the field to `None`.

    :param log_type: An object of `LogsType` class
    """
    if reports_config.is_logs_enabled:
        if not reports_config.logs_channel_id is None:
            if reports_config.enabled_logs_types.get(log_type.name, False):
                if logs_channel := inter.guild.get_channel(reports_config.logs_channel_id):
                    await logs_channel.send(embed=log_type.get_message_embed().add_field("Event type", log_type.name))
                else:
                    await session.execute(
                        update(
                            ReportsConfigModel,
                        )
                        .values(
                            logs_channel_id=None,
                        )
                        .where(
                            ReportsConfigModel.id == reports_config.id,
                        ),
                    )
                    await session.commit()
