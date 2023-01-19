from discord.ext import commands
from .bot import VRBot
from .models import Guild, User, Role, Channel

__all__ = ('VRBot', 'BaseCog',
           'Guild', 'User', 'Role', 'Channel')


class BaseCog(commands.Cog):
    """Base class for all cogs"""

    def __init__(self, bot_class: VRBot) -> None:
        self.bot = bot_class
