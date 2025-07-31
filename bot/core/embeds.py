from typing import Callable
from disnake import Embed

from .base_embeds import ErrorEmbed

type CallableEmbed[**P] = Callable[P, Embed]

not_enough_permissions_embed: CallableEmbed = lambda: ErrorEmbed(description="Not enough permissions for the action.")
this_is_guild_command_embed: CallableEmbed = lambda: ErrorEmbed(description="This is guild-only command.")
bot_is_unacceptable_embed: CallableEmbed = lambda: ErrorEmbed(description="A bot is unacceptable.")
unknown_guild_use_setup_embed: CallableEmbed = lambda: ErrorEmbed(description="Unknown guild, use the /setup command.")  # TODO: replace /setup
