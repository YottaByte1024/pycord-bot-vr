from config import config
from core import BaseCog
import discord
from discord.ext import commands
from discord.commands import Option
from googletrans import Translator


class Translation(BaseCog):
    """Команды для перевода текста"""

    @commands.slash_command()
    async def translate(self, ctx: discord.ApplicationContext,
                        lang: Option(str, choices=['ru', 'en', 'cz'], required=True,
                                     description="Язык, на который необходимо перевести"),
                        text: Option(str, description="Переводимый текст", required=True),
                        ephemeral: Option(bool, default=True)):
        try:
            translator = Translator()
            result = translator.translate(text, dest='cs' if lang == 'cz' else lang)
            await ctx.respond(f"[{result.src} -> {lang}] {result.text}", ephemeral=ephemeral)
        except:
            await ctx.respond(f"Произошла ошибка, попробуйте снова", ephemeral=True)

    @commands.message_command(name="Translate to RU",)
    async def message_translate_ru(self, ctx: discord.ApplicationContext, message: discord.Message):
        try:
            translator = Translator()
            result = translator.translate(message.content, dest="ru")
            await ctx.respond(f"[{result.src} -> ru] {result.text}", ephemeral=True)
        except:
            await ctx.respond(f"Произошла ошибка, попробуйте снова", ephemeral=True)


def setup(bot):
    bot.add_cog(Translation(bot))
