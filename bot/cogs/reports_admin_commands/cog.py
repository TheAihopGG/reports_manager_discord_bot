from disnake.ext import commands
from disnake import (
    AppCmdInter,
    CategoryChannel,
    Member,
    Role,
    TextChannel,
)
from sqlalchemy import delete, select, update

from .views import *
from .embeds import *
from .modals import GetReportResult
from ...core.database import session_factory
from ...core.models import (
    ReportsAdminRoleModel,
    ReportsConfigModel,
    ReportModel,
)
from ...core.embeds import (
    not_enough_permissions_embed,
    this_is_guild_command_embed,
    bot_is_unacceptable_embed,
    unknown_guild_use_setup_embed,
)
from ...core.base_embeds import (
    ErrorEmbed,
    SuccessEmbed,
    InfoEmbed,
)
from ...services.reports_service import (
    is_reports_admin,
    UnknownGuildError,
    get_reports_config_by_guild_id,
)
from ...services.logs_service import (
    send_log,
    LogsTypesEnum,
    ReportsAdminRoleAdded,
    ReportsAdminRoleRemoved,
    MemberAddedToReportChannel,
    MemberRemovedFromReportChannel,
)


class ReportsAdminCommandsCog(commands.Cog):
    @commands.slash_command()
    async def setup(self, inter: AppCmdInter) -> None:
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                async with session_factory() as session:
                    if (await session.execute(select(ReportsConfigModel).where(ReportsConfigModel.guild_id == inter.guild_id))).scalar_one_or_none() is None:
                        session.add(ReportsConfigModel(guild_id=inter.guild_id))
                        await session.commit()
                        await inter.response.send_message(
                            embed=SuccessEmbed(description="Guild setup has successfully."),
                            ephemeral=True,
                        )
                    else:
                        await inter.response.send_message(
                            embed=ErrorEmbed(description="Guild setup was successfully."),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def add_reports_admin_role(
        self,
        inter: AppCmdInter,
        role: Role,
    ) -> None:
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                async with session_factory() as session:
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        if not (
                            (
                                await session.execute(
                                    select(ReportsAdminRoleModel).where(
                                        ReportsAdminRoleModel.role_id == role.id,
                                        ReportsAdminRoleModel.guild_id == inter.guild_id,
                                    )
                                )
                            )
                            .scalars()
                            .all()
                        ):
                            await send_log(
                                session,
                                inter,
                                reports_config=reports_config,
                                log_type=ReportsAdminRoleAdded(role=role),
                            )
                            reports_admin_role = ReportsAdminRoleModel(
                                guild_id=inter.guild_id,
                                role_id=role.id,
                            )
                            session.add(reports_admin_role)
                            await session.commit()
                            await inter.response.send_message(
                                embed=SuccessEmbed(description="Role has added to reports admins roles."),
                                ephemeral=True,
                            )
                        else:
                            await inter.response.send_message(
                                embed=ErrorEmbed(description="This role is already a reports admin role"),
                                ephemeral=True,
                            )

                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def remove_reports_admin_role(
        self,
        inter: AppCmdInter,
        role: Role,
    ) -> None:
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                async with session_factory() as session:
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        if (
                            await session.execute(
                                delete(
                                    ReportsAdminRoleModel,
                                ).where(
                                    ReportsAdminRoleModel.guild_id == inter.guild_id,
                                    ReportsAdminRoleModel.role_id == role.id,
                                ),
                            )
                        ).rowcount:
                            await send_log(
                                session,
                                inter,
                                reports_config=reports_config,
                                log_type=ReportsAdminRoleRemoved(role=role),
                            )
                            await session.commit()
                            await inter.response.send_message(
                                embed=SuccessEmbed(description="Role has removed from reports admins roles."),
                                ephemeral=True,
                            )
                        else:
                            await inter.response.send_message(
                                embed=ErrorEmbed(description="Role has not found in reports admins roles."),
                                ephemeral=True,
                            )
                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def close_report(self, inter: AppCmdInter) -> None:
        if inter.guild:
            async with session_factory() as session:
                if inter.author.guild_permissions.administrator or await is_reports_admin(
                    session,
                    guild_id=inter.guild_id,
                    member=inter.author,
                ):
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        if report := (
                            await session.execute(
                                select(
                                    ReportModel,
                                ).where(
                                    ReportModel.channel_id == inter.channel_id,
                                ),
                            )
                        ).scalar_one_or_none():
                            if report.is_closed:
                                await inter.response.send_message(
                                    embed=InfoEmbed(description="The report has already closed."),
                                    ephemeral=True,
                                )
                            else:
                                await inter.response.send_modal(
                                    modal=GetReportResult(
                                        report=report,
                                        reports_config=reports_config,
                                    ),
                                )
                        else:
                            await inter.response.send_message(
                                embed=ErrorEmbed(description="The channel is not a report channel."),
                                ephemeral=True,
                            )
                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
                else:
                    await inter.response.send_message(
                        embed=not_enough_permissions_embed(),
                        ephemeral=True,
                    )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def set_reports_logs_channel(
        self,
        inter: AppCmdInter,
        channel: TextChannel,
    ) -> None:
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                async with session_factory() as session:
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        reports_config.logs_channel_id = channel.id
                        await session.commit()
                        await inter.response.send_message(embed=SuccessEmbed(description=f"Reports logs channel has set to {channel.mention}."))
                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def set_reports_channels_category(
        self,
        inter: AppCmdInter,
        category: CategoryChannel,
    ) -> None:
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                async with session_factory() as session:
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        reports_config.report_tickets_category_id = category.id
                        await session.commit()
                        await inter.response.send_message(embed=SuccessEmbed(description=f"Reports tickets category has set to {category.mention}."))
                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def add_member_report_channel(
        self,
        inter: AppCmdInter,
        member: Member,
    ) -> None:
        if inter.guild:
            if not member.bot:
                async with session_factory() as session:
                    if inter.author.guild_permissions.administrator or await is_reports_admin(
                        session,
                        guild_id=inter.guild_id,
                        member=inter.author,
                    ):
                        try:
                            reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                            if report := (
                                await session.execute(
                                    select(
                                        ReportModel,
                                    ).where(
                                        ReportModel.channel_id == inter.channel_id,
                                        ReportModel.guild_id == inter.guild_id,
                                    ),
                                )
                            ).scalar_one_or_none():
                                await send_log(
                                    session,
                                    inter,
                                    reports_config=reports_config,
                                    log_type=MemberAddedToReportChannel(report=report),
                                )
                                await inter.channel.set_permissions(
                                    member,
                                    view_channel=True,
                                    send_messages=True,
                                )
                                await inter.response.send_message(
                                    embed=SuccessEmbed(description="Member has added to report channel."),
                                )
                            else:
                                await inter.response.send_message(
                                    embed=ErrorEmbed(description="The channel is not a report channel."),
                                    ephemeral=True,
                                )
                        except UnknownGuildError:
                            await inter.response.send_message(
                                embed=unknown_guild_use_setup_embed(),
                                ephemeral=True,
                            )
                    else:
                        await inter.response.send_message(
                            embed=not_enough_permissions_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=bot_is_unacceptable_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def remove_member_report_channel(
        self,
        inter: AppCmdInter,
        member: Member,
    ) -> None:
        if inter.guild:
            if not member.bot:
                async with session_factory() as session:
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        if report := (
                            await session.execute(
                                select(
                                    ReportModel,
                                ).where(
                                    ReportModel.channel_id == inter.channel_id,
                                    ReportModel.guild_id == inter.guild_id,
                                ),
                            )
                        ).scalar_one_or_none():
                            await send_log(
                                session,
                                inter,
                                reports_config=reports_config,
                                log_type=MemberRemovedFromReportChannel(report=report),
                            )
                            await inter.channel.set_permissions(
                                member,
                                view_channel=False,
                                send_messages=False,
                            )
                            await inter.response.send_message(
                                embed=SuccessEmbed(description="Member has removed from report channel."),
                            )
                        else:
                            await inter.response.send_message(
                                embed=ErrorEmbed(description="The channel is not a report channel."),
                                ephemeral=True,
                            )
                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=bot_is_unacceptable_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def enable_log_type(
        self,
        inter: AppCmdInter,
        type: str,
    ) -> None:
        type = type.upper()
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                if type in LogsTypesEnum:
                    async with session_factory() as session:
                        try:
                            reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                            if not reports_config.enabled_logs_types.get(type, False):
                                reports_config.enabled_logs_types[type] = True
                                await session.execute(
                                    update(
                                        ReportsConfigModel,
                                    )
                                    .values(
                                        enabled_logs_types=reports_config.enabled_logs_types,
                                    )
                                    .where(
                                        ReportsConfigModel.id == reports_config.id,
                                    ),
                                )
                                await session.commit()
                                await inter.response.send_message(embed=SuccessEmbed(description=f"Sending logs with this type `{type}` has enabled."))
                            else:
                                await inter.response.send_message(embed=SuccessEmbed(description=f"Sending logs with this type `{type}` has already enabled."))
                        except UnknownGuildError:
                            await inter.response.send_message(
                                embed=unknown_guild_use_setup_embed(),
                                ephemeral=True,
                            )
                else:
                    await inter.response.send_message(
                        embed=ErrorEmbed(description="Unknown log type"),
                        ephemeral=True,
                    )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def disable_log_type(
        self,
        inter: AppCmdInter,
        type: str,
    ) -> None:
        type = type.upper()
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                if type in LogsTypesEnum:
                    async with session_factory() as session:
                        try:
                            reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                            if not reports_config.enabled_logs_types.get(type, False):
                                reports_config.enabled_logs_types[type] = False
                                await session.execute(
                                    update(
                                        ReportsConfigModel,
                                    )
                                    .values(
                                        enabled_logs_types=reports_config.enabled_logs_types,
                                    )
                                    .where(
                                        ReportsConfigModel.id == reports_config.id,
                                    ),
                                )
                                await session.commit()
                                await inter.response.send_message(embed=SuccessEmbed(description=f"Sending logs with this type `{type}` has disabled."))
                            else:
                                await inter.response.send_message(embed=SuccessEmbed(description=f"Sending logs with this type `{type}` has already disabled."))
                        except UnknownGuildError:
                            await inter.response.send_message(
                                embed=unknown_guild_use_setup_embed(),
                                ephemeral=True,
                            )
                else:
                    await inter.response.send_message(
                        embed=ErrorEmbed(description="Unknown log type"),
                        ephemeral=True,
                    )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def enable_reports(self, inter: AppCmdInter) -> None:
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                async with session_factory() as session:
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        if not reports_config.is_reports_enabled:
                            reports_config.is_reports_enabled = False
                            await session.commit()
                            await inter.response.send_message(embed=SuccessEmbed(description=f"Reports has enabled."))
                        else:
                            await inter.response.send_message(embed=SuccessEmbed(description=f"Reports has already enabled."))
                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def disable_reports(self, inter: AppCmdInter) -> None:
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                async with session_factory() as session:
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        if reports_config.is_reports_enabled:
                            reports_config.is_reports_enabled = False
                            await session.commit()
                            await inter.response.send_message(embed=SuccessEmbed(description=f"Reports has disabled."))
                        else:
                            await inter.response.send_message(embed=SuccessEmbed(description=f"Reports has already disabled."))
                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def enable_logs(self, inter: AppCmdInter) -> None:
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                async with session_factory() as session:
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        if not reports_config.is_logs_enabled:
                            reports_config.is_logs_enabled = True
                            await session.commit()
                            await inter.response.send_message(embed=SuccessEmbed(description=f"Logs has enabled."))
                        else:
                            await inter.response.send_message(embed=SuccessEmbed(description=f"Logs has already enabled."))
                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )

    @commands.slash_command()
    async def disable_logs(self, inter: AppCmdInter) -> None:
        if inter.guild:
            if inter.author.guild_permissions.administrator:
                async with session_factory() as session:
                    try:
                        reports_config = await get_reports_config_by_guild_id(session, guild_id=inter.guild_id)
                        if reports_config.is_logs_enabled:
                            reports_config.is_logs_enabled = False
                            await session.commit()
                            await inter.response.send_message(embed=SuccessEmbed(description=f"Logs has disabled."))
                        else:
                            await inter.response.send_message(embed=SuccessEmbed(description=f"Logs has already disabled."))
                    except UnknownGuildError:
                        await inter.response.send_message(
                            embed=unknown_guild_use_setup_embed(),
                            ephemeral=True,
                        )
            else:
                await inter.response.send_message(
                    embed=not_enough_permissions_embed(),
                    ephemeral=True,
                )
        else:
            await inter.response.send_message(
                embed=this_is_guild_command_embed(),
                ephemeral=True,
            )
