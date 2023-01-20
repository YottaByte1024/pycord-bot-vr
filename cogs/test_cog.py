from config import config
from core import BaseCog, Guild
import discord
from discord.ext import commands
from discord.commands import Option


class TestCog(BaseCog):
    @commands.slash_command(
        guild_ids=config['debug_guilds'],
    )
    async def test_command(self, ctx: discord.ApplicationContext):

        await ctx.respond('done', ephemeral=True)


def setup(bot):
    bot.add_cog(TestCog(bot))
