from sys import argv
from traceback import format_exception

import discord
from discord.ext import commands
from tortoise import Tortoise, run_async
from tortoise import utils

from config import config


async def db_init():
    await Tortoise.init(
        db_url='sqlite://data/db.sqlite3',
        modules={'models': ['core.models']}
    )
    await Tortoise.generate_schemas()


class VRBot(commands.Bot):

    def __init__(self):
        super().__init__(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"/help"
            ),
            # allowed_mentions=discord.AllowedMentions.none(),
            # chunk_guilds_at_startup=False,
            # help_command=,
            intents=discord.Intents(
                members=True,
                messages=True,
                message_content=True,
                guilds=True,
                bans=True,
            ),
            owner_id=config['owner_id'],
            debug_guilds=config['debug_guilds']
        )

        for cog in [
            # 'cogs.test_cog',
            'cogs.magic8ball',
            'cogs.random',
            'cogs.help',
            'cogs.free_roles',
            'cogs.greetings',
            'cogs.settings',
            'cogs.anon',
            # 'cogs.record'
        ]:
            print(cog)
            self.load_cog(cog)

    def load_cog(self, cog: str) -> None:
        try:
            self.load_extension(cog)
        except Exception as e:
            e = getattr(e, "original", e)
            print("".join(format_exception(type(e), e, e.__traceback__)))

    async def on_ready(self):
        await db_init()

        # await super().register_commands()
        print(f"We have logged in as {self.user}")

    def run(self, token):
        super().run(token)
