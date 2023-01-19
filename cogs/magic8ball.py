from core import BaseCog
import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
import random as rm
from asyncio import sleep


class Magic8ball(BaseCog):
    """Команды Magic 8ball"""

    magicball = SlashCommandGroup("magic8ball", "description")

    @magicball.command(
        name="yes_or_no",
        description="Дает краткий ответ на заданный вопрос"
    )
    async def yes_or_no(self, ctx: discord.ApplicationContext,
                        question: Option(str, "Задаваемый вопрос", required=True)):
        await ctx.defer()
        answer = rm.choice(('Да', 'Нет'))
        await sleep(3)
        embed = discord.Embed(title="", type='article')
        embed.add_field(name="Вопрос от:", value=ctx.author.mention, inline=False)
        embed.add_field(name="Вопрос:", value=question, inline=False)
        embed.add_field(name="Мой ответ:", value=answer, inline=False)
        await ctx.respond('', embed=embed)

    @magicball.command(
        name="magic8ball",
        description="Дает умный ответ на заданный вопрос"
    )
    async def magic_8ball(self,
                          ctx: discord.ApplicationContext,
                          question: Option(str, "Задаваемый вопрос", required=True)
                          ):
        await ctx.defer()
        answer = rm.choice(('Бесспорно',
                            'Предрешено', 'Никаких сомнений',
                            'Определённо да', 'Можешь быть уверен в этом',
                            'Мне кажется — «да»', 'Вероятнее всего',
                            'Хорошие перспективы', 'Знаки говорят — «да»',
                            'Да', 'Пока не ясно, попробуй снова',
                            'Спроси позже', 'Лучше не рассказывать',
                            'Сейчас нельзя предсказать', 'Сконцентрируйся и спроси опять',
                            'Даже не думай', 'Мой ответ — «нет»',
                            'По моим данным — «нет»', 'Перспективы не очень хорошие',
                            'Весьма сомнительно',))
        await sleep(5)
        embed = discord.Embed(title="", type='article')
        embed.add_field(name="Вопрос от:", value=ctx.author.mention, inline=False)
        embed.add_field(name="Вопрос:", value=question, inline=False)
        embed.add_field(name="Мой ответ:", value=answer, inline=False)
        await ctx.respond('', embed=embed)


def setup(bot):
    bot.add_cog(Magic8ball(bot))
