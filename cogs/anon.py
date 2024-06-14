from core import BaseCog
import discord
from discord.ext import commands
from discord.commands import Option


class Anon(BaseCog):
    """Команды для отправки сообщений анонимно"""

    @commands.slash_command(
        name='anon_send',
        description='Отправляет сообщение анонимно',
        guild_only=True,
    )
    async def anon_send(self, ctx: discord.ApplicationContext,
                        text: discord.Option(str, required=True),
                        user: discord.Option(discord.User, required=False)):
        if user is None:
            await ctx.channel.send("Кто-то оставил записку тут:\n" + text)
            await ctx.respond("Сообщение отправлено", ephemeral=True)
        else:
            try:
                dm = await user.create_dm()
                await dm.send("Кто-то оставил записку тебе:\n" + text)
                await ctx.respond("Сообщение отправлено", ephemeral=True)
            except:
                await ctx.respond("У получателя закрыт доступ к личным сообщениям", ephemeral=True)


def setup(bot):
    bot.add_cog(Anon(bot))
