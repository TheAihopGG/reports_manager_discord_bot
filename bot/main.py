import cogs.reports_admin_commands.cog
import cogs.reports_member_commands.cog
from disnake.ext import commands
from disnake import Intents

from core.configuration import BOT_TOKEN
from core.logger import logger


bot = commands.InteractionBot(intents=Intents.all())

bot.add_cog(cogs.reports_admin_commands.cog.ReportsAdminCommandsCog())
bot.add_cog(cogs.reports_member_commands.cog.ReportsMemberCommandsCog())


@bot.event
async def on_ready() -> None:
    logger.info("Bot successfully launched")


bot.run(BOT_TOKEN)
