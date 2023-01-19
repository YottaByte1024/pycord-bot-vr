from core import BaseCog
import discord
from discord.ext import commands
from discord.commands import Option


class HelpSelect(discord.ui.Select):
    def __init__(self, cog: commands.Cog) -> None:
        super().__init__(
            placeholder="Выберите категорию",
            options=[
                discord.SelectOption(
                    label=cog_name,
                    description=cog.__doc__,
                )
                for cog_name, cog in cog.bot.cogs.items()
                if cog.__cog_commands__
                   and cog_name not in ["Test", "Ex_Groups", "Help", "Cog", "Greetings"]
            ],
        )
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        cog = self.cog.bot.get_cog(self.values[0])
        assert cog
        embed = discord.Embed(
            title=f"{cog.__cog_name__} - {cog.__doc__}",
            description="\n".join(
                f"`/{command.qualified_name}`: {command.description}"
                for command in cog.walk_commands()
            ),
            color=discord.Color.blue(),
            timestamp=discord.utils.utcnow(),
        )
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True,
        )


class Help(BaseCog):
    @commands.slash_command(name="help")
    async def help_command(self, ctx: discord.ApplicationContext):
        """Получить помощь с ботом по командам."""
        assert self.bot.user
        embed = discord.Embed(
            title=self.bot.user.name,
            description=(
                "Этот бот создан для выдачи ролей и приветствия новых участников.\n"
                "Также добавлены различные фичи.\n"
                f"Разработчик бота: <@{self.bot.owner_id}>\n"
                "Родительский бот: https://github.com/Dorukyum/Toolkit\n"
                "Для получения помощи выберите внизу категорию команд."
            ),
            colour=discord.Color.blue(),
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url) \
            .add_field(name="Число пользователей", value=str(len(self.bot.users))) \
            .add_field(name="Число серверов", value=str(len(self.bot.guilds)))

        view = discord.ui.View(HelpSelect(self))
        await ctx.respond(embed=embed, view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(Help(bot))
