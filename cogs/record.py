from core import BaseCog
import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup, context

connections = {}


class Record(BaseCog):
    async def once_done(self, sink: discord.sinks, channel: discord.TextChannel, *args):
        # Our voice client already passes these in.

        user_recorded = [  # A list of recorded users
            f"<@{user_id}>"
            for user_id, audio in sink.audio_data.items()
        ]
        await sink.vc.disconnect()  # Disconnect from the voice channel.
        files = [discord.File(audio.file, f"{self.bot.get_user(user_id).display_name}.{sink.encoding}") \
                 for user_id, audio in sink.audio_data.items()]  # List down the files.

        await channel.send(f"Finished recording audio for: {', '.join(user_recorded)}.", files=files)
        # Send a message with the accumulated files.

    record_group = SlashCommandGroup('record', 'Команды записи голосового канала', guild_only=True)

    @record_group.command(name="start", description='Start record', guild_only=True)
    async def record(self, ctx: context.ApplicationContext):  # If you're using commands.Bot, this will also work.
        voice = ctx.author.voice

        if not voice:
            await ctx.respond("You aren't in a voice channel!")

        vc = await voice.channel.connect()  # Connect to the voice channel the author is in.
        connections.update({ctx.guild.id: vc})  # Updating the cache with the guild and channel.

        vc.start_recording(
            discord.sinks.WaveSink(),  # The sink type to use.
            self.once_done,  # What to do once done.
            ctx.channel  # The channel to disconnect from.
        )
        await ctx.respond("Started recording!")

    @record_group.command(name="stop", description='Stop record', guild_only=True)
    async def stop_recording(self, ctx: context.ApplicationContext):
        if ctx.guild.id in connections:  # Check if the guild is in the cache.
            vc = connections[ctx.guild.id]
            vc.stop_recording()  # Stop recording, and call the callback (once_done).
            del connections[ctx.guild.id]  # Remove the guild from the cache.
            await ctx.delete()  # And delete.
        else:
            await ctx.respond("I am currently not recording here.")  # Respond with this if we aren't recording.


def setup(bot):
    bot.add_cog(Record(bot))
