import asyncio
import os
import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        await self.load_extension("ext.general")
        await self.load_extension("ext.moderation")

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def on_command_error(self, ctx, error: commands.CommandError):
        e = discord.Embed(color=discord.Colour.red())
        if isinstance(error, commands.MissingPermissions):
            e.title = "You are missing permission(s) required to use this command."
        elif isinstance(error, commands.BotMissingPermissions):
            e.title = "I am missing permission(s) required to do this."
        else:
            e.title = str(error)
        await ctx.channel.send(embed=e)

async def main():
    discord.utils.setup_logging()

    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    async with Bot(commands.when_mentioned_or("-"), intents=intents) as bot:
        await bot.start(os.getenv("TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
