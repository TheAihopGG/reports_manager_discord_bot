from disnake import Member
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.models import ReportsAdminRoleModel, ReportsConfigModel
from ...core.errors import UnknownGuildError


async def is_reports_admin(
    session: AsyncSession,
    *,
    guild_id: int,
    member: Member,
) -> bool:
    """
    Checks is member a reports admin

    :return: True if member is a reports admin

    :raise UnknownGuildError: if guild was not found is db
    """
    member_roles_ids: list[int] = [role.id for role in member.roles]
    if (
        reports_admins_roles := (
            await session.execute(
                select(ReportsAdminRoleModel).where(ReportsAdminRoleModel.guild_id == guild_id),
            )
        )
        .scalars()
        .all()
    ):
        return any(reports_admins_role.role_id in member_roles_ids for reports_admins_role in reports_admins_roles)
    else:
        raise UnknownGuildError(guild_id=guild_id)


async def get_reports_admins(
    session: AsyncSession,
    *,
    guild_id: int,
) -> list[ReportsAdminRoleModel]:
    """
    Returns reports admins roles models.

    :return: list of reports admins roles models or empty list
    """
    if (
        reports_admins_roles := (
            await session.execute(
                select(ReportsAdminRoleModel).where(ReportsAdminRoleModel.guild_id == guild_id),
            )
        )
        .scalars()
        .all()
    ):
        return reports_admins_roles
    else:
        return []


async def get_reports_config_by_guild_id(
    session: AsyncSession,
    *,
    guild_id: int,
) -> ReportsConfigModel:
    """
    Returns reports config model

    :raise UnknownGuildError: if guild was not found is db
    """
    if reports_config := (
        await session.execute(
            select(
                ReportsConfigModel,
            ).where(
                ReportsConfigModel.guild_id == guild_id,
            )
        )
    ).scalar_one_or_none():
        return reports_config
    else:
        raise UnknownGuildError(guild_id=guild_id)
