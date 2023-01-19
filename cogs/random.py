from discord import guild_only

from core import BaseCog
import discord
from discord.ext import commands
from discord.commands import Option
import random as rm


class Random(BaseCog):
    """Команды рандомайзера"""

    @commands.slash_command(
        name="randint",
        description="Дает случайное целое число из заданного диапазона"
    )
    async def randint(self,
                      ctx: discord.ApplicationContext,
                      first_num: Option(int, "Первое число", required=True, default=0),
                      second_num: Option(int, "Второе число", required=True, default=1)
                      ):
        await ctx.respond("Ваше случайное число: " + str(rm.randint(first_num, second_num)))

    @commands.slash_command(
        name="random_user",
        description="Выбирает случайного пользователя из выбранных"
    )
    @guild_only()
    async def random_user(self,
                          ctx: discord.ApplicationContext,
                          option1: Option(discord.User, "User", required=True, name="1"),
                          option2: Option(discord.User, "User", required=True, name="2"),
                          option3: Option(discord.User, "User", required=False, name="3"),
                          option4: Option(discord.User, "User", required=False, name="4"),
                          option5: Option(discord.User, "User", required=False, name="5"),
                          option6: Option(discord.User, "User", required=False, name="6"),
                          option7: Option(discord.User, "User", required=False, name="7"),
                          option8: Option(discord.User, "User", required=False, name="8"),
                          option9: Option(discord.User, "User", required=False, name="9"),
                          option10: Option(discord.User, "User", required=False, name="10"),
                          option11: Option(discord.User, "User", required=False, name="11"),
                          option12: Option(discord.User, "User", required=False, name="12"),
                          option13: Option(discord.User, "User", required=False, name="13"),
                          option14: Option(discord.User, "User", required=False, name="14"),
                          option15: Option(discord.User, "User", required=False, name="15"),
                          ):
        options = [option1, option2, option3, option4, option5, option6, option7,
                   option8, option9, option10, option11, option12, option13,
                   option14, option15]
        while True:
            random_index = rm.randint(0, len(options) - 1)
            # print(random_index)
            winner = options[random_index]
            if winner is not None:
                break
        await ctx.respond("Случайно выбранный участник: " + winner.mention)

def setup(bot):
    bot.add_cog(Random(bot))
