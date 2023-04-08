import discord
from discord.ext import commands


class Meta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def sync(self, ctx, guild: discord.Object = None):
        """Sync application commands."""
        if guild is not None:
            ctx.bot.tree.copy_global_to(guild=guild)
            synced = await ctx.bot.tree.sync(guild=guild)
        else:
            synced = await ctx.bot.tree.sync()
        await ctx.reply(
            (f"Synced {len(synced)} command(s)"
             f" {'globally' if guild is None else f'to {guild.id}'}."))


async def setup(bot):
    await bot.add_cog(Meta(bot))
