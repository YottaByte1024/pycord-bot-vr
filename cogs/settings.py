from core import BaseCog, Role, Channel
import discord
from discord.ext import commands
from discord.commands import Option


class Settings(BaseCog):
    """Команды для настройки бота"""

    settings_group = discord.SlashCommandGroup('settings',
                                               'Команды записи голосового канала',

                                               guild_only=True)

    @settings_group.command(name='free_roles',
                            description='Назначение ролей доступных для получения всеми',
                            )
    @commands.has_permissions(administrator=True)
    async def change_free_roles(self, ctx: discord.ApplicationContext,
                                action: Option(str, choices=['add', 'delete', 'change']),
                                role: Option(discord.Role, required=True, name='role'),
                                desc: Option(str, required=False, name='description')):
        # await ctx.defer()

        # Переменная, обозначающая отсутствие desc
        ex_desc = False
        if desc is None:
            ex_desc = True

        created = await Role.get_or_none(id=role.id)
        ex_already_free = False
        ex_already_created = False
        if created is not None:
            ex_already_created = True
            if created.free_role:
                ex_already_free = True

        temp_message = f"Выполнено\n" \
                       f"Роль уже есть в памяти: {ex_already_created}\n" \
                       f"Уже есть free role: {ex_already_free} \n"

        match action:
            case 'add':
                if created is None:
                    if ex_desc:
                        await Role.create(id=role.id, free_role=True, guild_id=ctx.guild.id)
                    else:
                        await Role.create(id=role.id, free_role=True, description=desc, guild_id=ctx.guild.id, )
                elif not ex_already_free:
                    if ex_desc:
                        await Role.filter(id=role.id).update(free_role=True)
                    else:
                        await Role.filter(id=role.id).update(free_role=True, description=desc)

                message = temp_message + f"Нет описания: {ex_desc}"
                await ctx.respond(message, ephemeral=True)
            case 'delete':
                deleted = False
                if ex_already_free and (created is not None):
                    await Role.filter(id=role.id).update(free_role=False)
                    deleted = True
                message = temp_message + f"Убрано: {deleted}"
                await ctx.respond(message, ephemeral=True)
            case 'change':
                changed = False
                if not ex_desc and (created is not None):
                    await Role.filter(id=role.id).update(description=desc)
                    changed = True

                message = temp_message + f"Нет описания: {ex_desc}\n" \
                                         f"Изменено: {changed}"
                await ctx.respond(message, ephemeral=True)

    @settings_group.command(name='greetings_roles',
                            description='Назначение ролей для >18-летних и согласившихся с правилами',
                            )
    @commands.has_permissions(administrator=True)
    async def change_roles(self, ctx: discord.ApplicationContext,
                           kind: Option(str, choices=['rules', 'adult']),
                           role: Option(discord.Role, required=True, name='role')):
        # await ctx.defer()

        created = await Role.get_or_none(id=role.id)

        ex_already_rules = False
        if await Role.get_or_none(id=role.id, resident_role=True):
            ex_already_rules = True

        ex_already_adult = False
        if await Role.get_or_none(id=role.id, adult_role=True):
            ex_already_adult = True

        ex_already_created = False
        if created is not None:
            ex_already_created = True

        temp_message = f"Выполнено\n" \
                       f"Роль уже есть в памяти: {ex_already_created}\n" \
                       f"Уже rule role: {ex_already_rules} \n" \
                       f"Уже adult role: {ex_already_adult} \n"
        message = ""

        match kind:
            case 'rules':
                resident_role_exists = await Role.filter(guild_id=ctx.guild.id, resident_role=True).exists()
                if not resident_role_exists:
                    if not ex_already_created:
                        await Role.create(id=role.id, resident_role=True, guild_id=ctx.guild.id)
                    else:
                        await Role.filter(id=role.id).update(resident_role=True)
                    message = "Роль не была уже определена"
                else:
                    await Role.filter(guild_id=ctx.guild.id, resident_role=True).update(resident_role=False)
                    await Role.filter(id=role.id).update(resident_role=True)
                    message = "Роль была уже определена, и переопределена"
                await ctx.respond(temp_message + message, ephemeral=True)

            case 'adult':
                adult_role_exists = await Role.filter(guild_id=ctx.guild.id, adult_role=True).exists()
                if not adult_role_exists:
                    if not ex_already_created:
                        await Role.create(id=role.id, adult_role=True, guild_id=ctx.guild.id)
                    else:
                        await Role.filter(id=role.id).update(adult_role=True)
                    message = "Роль не была уже определена"
                else:
                    await Role.filter(guild_id=ctx.guild.id, adult_role=True).update(adult_role=False)
                    await Role.filter(id=role.id).update(adult_role=True)
                    message = "Роль была уже определена, и переопределена"
                await ctx.respond(temp_message + message, ephemeral=True)

    @settings_group.command(name='channels',
                            description='Назначение канала с правилами и канала для сообщений от бота',
                            )
    @commands.has_permissions(administrator=True)
    async def change_channels(self, ctx: discord.ApplicationContext,
                              kind: Option(str, choices=['rules', 'bot']),
                              channel: Option(discord.TextChannel, required=True, name='channel')):
        # await ctx.defer()

        created = await Channel.get_or_none(id=channel.id)

        ex_already_rules = False
        if await Channel.get_or_none(id=channel.id, rules_channel=True):
            ex_already_rules = True

        ex_already_bot = False
        if await Channel.get_or_none(id=channel.id, bot_channel=True):
            ex_already_bot = True

        ex_already_created = False
        if created is not None:
            ex_already_created = True

        temp_message = f"Выполнено\n" \
                       f"Канал уже есть в памяти: {ex_already_created}\n" \
                       f"Уже rules channel: {ex_already_rules} \n" \
                       f"Уже bot channel: {ex_already_bot} \n"
        message = ""

        match kind:
            case 'rules':
                rules_channel_exists = await Channel.filter(guild_id=ctx.guild.id, rules_channel=True).exists()
                if not rules_channel_exists:
                    if not ex_already_created:
                        await Channel.create(id=channel.id, rules_channel=True, guild_id=ctx.guild.id)
                    else:
                        await Channel.filter(id=channel.id).update(rules_channel=True)
                    message = "Канал не был уже определен"
                else:
                    await Channel.filter(guild_id=ctx.guild.id, rules_channel=True).update(rules_channel=False)
                    await Channel.filter(id=channel.id).update(rules_channel=True)
                    message = "Канал был уже определен, и переопределен"
                await ctx.respond(temp_message + message, ephemeral=True)

            case 'bot':
                bot_channel_exists = await Channel.filter(guild_id=ctx.guild.id, bot_channel=True).exists()
                if not bot_channel_exists:
                    if not ex_already_created:
                        await Channel.create(id=channel.id, bot_channel=True, guild_id=ctx.guild.id)
                    else:
                        await Channel.filter(id=channel.id).update(bot_channel=True)
                    message = "Канал не был уже определен"
                else:
                    await Channel.filter(guild_id=ctx.guild.id, bot_channel=True).update(bot_channel=False)
                    await Channel.filter(id=channel.id).update(bot_channel=True)
                    message = "Канал был уже определен, и переопределен"
                await ctx.respond(temp_message + message, ephemeral=True)


def setup(bot):
    bot.add_cog(Settings(bot))
