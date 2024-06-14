from core import BaseCog, Channel, Role, Guild
import discord
from discord.ext import commands
from discord.commands import Option


class Button(discord.ui.Button):
    def __init__(self, role: discord.Role, guild: discord.Guild, member: discord.Member,
                 style=discord.ButtonStyle.secondary):
        super().__init__(
            label=role.name,
            style=style,
            custom_id=str(role.id), )
        self.guild = guild
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        # role = interaction.guild.get_role(int(self.custom_id))
        role = self.guild.get_role(int(self.custom_id))
        if role is None:
            return

        # if role not in user.roles:
        if role not in self.member.roles:
            await self.member.add_roles(role)

            await interaction.response.send_message(f"🎉 Вы получили роль \"{role.name}\"", ephemeral=True)
        else:
            # await user.remove_roles(role)
            await interaction.response.send_message(
                f"❌ Роль \"{role.name}\" уже выдана вам", ephemeral=True
            )


class Greetings(BaseCog):
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        rules_channel = await Channel.get_or_none(guild_id=member.guild.id, rules_channel=True)
        if rules_channel is not None:
            rules_chat = discord.utils.get(
                member.guild.channels, id=rules_channel.id)
            rules_chat_mention = rules_chat.mention
        else:
            rules_chat_mention = "<Канал не найден (узнайте у администрации сервера)>"

        bot_channel = await Channel.get_or_none(guild_id=member.guild.id, bot_channel=True)
        if bot_channel is None:
            bot_channel = member.guild.system_channel.id
        else:
            bot_channel = bot_channel.id

        view = discord.ui.View(timeout=None)

        dm_ex = False
        try:
            dm = await member.create_dm()
            await dm.send('Привет!')
        except:
            dm_ex = True

        not_found = "Произошла ошибка, роль {role_name} не найдена"

        # Create button for rules
        role_q = await Role.get_or_none(guild_id=member.guild.id, resident_role=True)
        if role_q is not None:
            role = member.guild.get_role(role_q.id)
            view.add_item(Button(role, member.guild, member,
                          discord.ButtonStyle.green))
        elif not dm_ex:
            await dm.send(not_found.format(role_name='для согласившегося с правилами'))
        else:
            await member.guild.get_channel(bot_channel).send(
                not_found.format(role_name='для согласившегося с правилами'),
            )

        # Create button for adults
        role_q = await Role.get_or_none(guild_id=member.guild.id, adult_role=True)
        if role_q is not None:
            role18 = member.guild.get_role(role_q.id)
            view.add_item(Button(role18, member.guild, member,
                          discord.ButtonStyle.blurple))
        elif not dm_ex:
            await dm.send(not_found.format(role_name='для 18-летних'))
        else:
            await member.guild.get_channel(bot_channel).send(
                not_found.format(role_name='для 18-летних'))

        embed = discord.Embed(
            title="Welcome!", type='article', color=discord.Color.red(),
            description=f"Привет, {member.mention}!\n"
            f"Если хочешь стать резидентом, согласись с правилами:\n"
            f"{rules_chat_mention}\n"
            f"Для этого нажми на зеленую кнопку ниже (первая).\n"
            f"Если тебе есть 18 лет, нажми на синюю кнопку (вторая).\n"
            f"(Сможешь видеть историю сообщений)"
            f"Также у тебя есть доступ к некоторым ролям по команде:\n"
            f"/roles (доступна на сервере)",
        )

        if not dm_ex:
            await dm.send(embed=embed, view=view)
        else:
            await member.guild.get_channel(bot_channel).send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        print('Joined to ', guild)
        message = ""
        created = await Guild.get_or_none(id=guild.id)
        if created is not None:
            message = message + "Эта гильдия уже есть в моей памяти..."
        else:
            message = message + "Записываю в память эту гильдию..."
            await Guild.create(id=guild.id)

        await self.bot.register_commands()
        await self.bot.sync_commands()

        embed = discord.Embed(title="Здравствуйте всем!",
                              description=message, color=discord.Color.blue())
        embed.add_field(
            name="Настройка",
            value="Для настройки бота воспользуйтесь группой команд /settings",
            inline=False,
        )
        embed.add_field(
            name="Совет",
            value="Для работы с ролями роль бота должна быть выше этих ролей",
            inline=False,
        )
        await guild.system_channel.send('', embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        if guild_q := await Guild.get_or_none(id=guild.id):
            await guild_q.delete()


def setup(bot):
    bot.add_cog(Greetings(bot))
