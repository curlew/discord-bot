import asyncio
import logging
from os import getenv
from signal import SIGTERM
import asyncpg
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class Bot(commands.Bot):

    def __init__(self, *args, db_pool: asyncpg.Pool, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_pool = db_pool

    async def setup_hook(self):
        await self.load_extension("ext.general")
        await self.load_extension("ext.moderation")
        await self.load_extension("ext.meta")

    async def on_ready(self):
        logger.info("Ready. ID: %d", self.user.id)

    async def on_command_error(self, ctx, error: commands.CommandError, /):
        e = discord.Embed(color=discord.Colour.red())
        if isinstance(error, commands.MissingPermissions):
            e.title = "You are missing permission(s) required to use this command."
        elif isinstance(error, commands.BotMissingPermissions):
            e.title = "I am missing permission(s) required to do this."
        else:
            e.title = str(error)
            logger.warning("Unhandled error from command '%s': %s", ctx.message.content, str(error))
        await ctx.channel.send(embed=e)


async def main():
    discord.utils.setup_logging()

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    db_uri = (
        f"postgres://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
        f"@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
    )

    async with asyncpg.create_pool(db_uri) as db_pool:
        async with Bot(commands.when_mentioned_or("-"),
                       db_pool=db_pool,
                       activity=discord.Game(name="-help"),
                       intents=intents) as bot:
            bot.loop.add_signal_handler(SIGTERM, lambda: asyncio.ensure_future(bot.close()))
            await bot.start(getenv("TOKEN"))


if __name__ == "__main__":
    asyncio.run(main())
