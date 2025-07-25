from disnake.ext import commands

from .cogs.reports_admin_commands.cog import ReportsAdminCommandsCog
from .cogs.reports_member_commands.cog import ReportsMemberCommandsCog
from .core.configuration import BOT_TOKEN
from .core.logger import logger


bot = commands.InteractionBot()

bot.add_cog(ReportsAdminCommandsCog())
bot.add_cog(ReportsMemberCommandsCog())


@bot.event
async def on_ready() -> None:
    logger.info("Bot successfully launched")


def main() -> None:
    bot.run(BOT_TOKEN)
