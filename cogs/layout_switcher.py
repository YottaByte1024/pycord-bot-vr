from core import BaseCog
import discord
from discord.ext import commands
from discord.commands import Option


layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`йцукенгшщзхъфывапролджэячсмитьбю.ё"
                           'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                           "йцукенгшщзхъфывапролджэячсмитьбю.ёqwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                           'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,ЁQWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))


class LayoutSwitcher(BaseCog):
    
    @commands.message_command(name="Switch layout",)
    async def message_layout_switcher(self, ctx: discord.ApplicationContext, message: discord.Message):
        
        result = message.content.translate(layout)
        
        await ctx.respond(f"{message.author.mention} написал:\n {result}", ephemeral=False)


def setup(bot):
    bot.add_cog(LayoutSwitcher(bot))
