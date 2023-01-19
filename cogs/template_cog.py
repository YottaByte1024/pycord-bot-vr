from core import BaseCog
import discord
from discord.ext import commands
from discord.commands import Option


class Cog(BaseCog):
    pass


def setup(bot):
    bot.add_cog(Cog(bot))
