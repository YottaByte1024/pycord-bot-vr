from core import BaseCog, Guild, Role
import discord
from discord.ext import commands
from discord.commands import Option


class RoleButton(discord.ui.Button):
    def __init__(self, role: discord.Role):
        """
        A button for one role. `custom_id` is needed for persistent views.
        """
        super().__init__(
            label=role.name,
            style=discord.enums.ButtonStyle.primary,
            custom_id=str(role.id),
        )

    async def callback(self, interaction: discord.Interaction):
        """This function will be called any time a user clicks on this button.
        Parameters
        ----------
        interaction : discord.Interaction
            The interaction object that was created when a user clicks on a button.
        """
        # Figure out who clicked the button.
        user = interaction.user
        # Get the role this button is for (stored in the custom ID).
        role = interaction.guild.get_role(int(self.custom_id))

        if role is None:
            # If the specified role does not exist, return nothing.
            # Error handling could be done here.
            return

        # Add the role and send a response to the uesr ephemerally (hidden to other users).
        if role not in user.roles:
            # Give the user the role if they don't already have it.
            await user.add_roles(role)
            await interaction.response.send_message(f"🎉 Вы получили роль {role.mention}", ephemeral=True)
        else:
            # Else, Take the role from the user
            await user.remove_roles(role)
            await interaction.response.send_message(
                f"❌ Роль {role.mention} была отнята у вас", ephemeral=True
            )


class FreeRoles(BaseCog):
    """Команды для получения ролей"""

    @commands.slash_command(
        name="roles",
        description="Показывает доступные роли",
    )
    async def free_roles(self, ctx):
        view = discord.ui.View(timeout=None)

        free_roles = list(await Role.filter(guild_id=ctx.guild.id, free_role=True))
        role_ids = [obj.id for obj in free_roles]
        if len(role_ids) == 0:
            await ctx.respond('Свободных ролей не прописано', ephemeral=True)
            return

        for role_id in role_ids:
            role = ctx.guild.get_role(role_id)
            view.add_item(RoleButton(role))
        embed = discord.Embed(title="Распродажа ролей!", type='article',
                              description=f'''Вы можете выбирать себе роли.''')
        for role_id in role_ids:
            desc = await Role.filter(id=role_id).first()
            if desc.description != '':
                desc = desc.description
            else:
                desc = 'Нет описания'
            embed.add_field(name=discord.utils.get(ctx.guild.roles, id=role_id).name,
                            value=desc, inline=False)
        await ctx.respond(embed=embed, view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(FreeRoles(bot))
