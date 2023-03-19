from core import BaseCog
import discord
from discord.ext import commands
from discord.commands import Option


layout_en2ru = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                 'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                                 "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))

layout_ru2en = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                 'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                                 "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                 'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))


class LayoutSwitcher(BaseCog):

    @commands.message_command(name="Switch RU to EN",)
    async def message_layout_switcher_ru2en(self, ctx: discord.ApplicationContext, message: discord.Message):

        result = message.content.translate(layout_ru2en)

        await ctx.respond(f"{message.author.mention} написал:\n {result}", ephemeral=False)

    @commands.message_command(name="Switch EN to RU",)
    async def message_layout_switcher_en2ru(self, ctx: discord.ApplicationContext, message: discord.Message):

        result = message.content.translate(layout_en2ru)

        await ctx.respond(f"{message.author.mention} написал:\n {result}", ephemeral=False)


def setup(bot):
    bot.add_cog(LayoutSwitcher(bot))
