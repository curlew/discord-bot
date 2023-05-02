import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class Meta(commands.Cog):
    """Operations which act on the bot itself."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sync(self, ctx, guild: discord.Object = None):
        """Sync application commands"""
        if guild is not None:
            ctx.bot.tree.clear_commands(guild=guild)
            await ctx.bot.tree.sync(guild=guild)
        else:
            await ctx.bot.tree.sync()
        message = f"Synced commands {'globally' if guild is None else f'to {guild.id}'}."
        await ctx.reply(message)
        logger.info(message)


async def setup(bot):
    await bot.add_cog(Meta(bot))
