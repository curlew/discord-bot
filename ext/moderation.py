from typing import Union
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Kicks a user")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author != ctx.guild.owner and ctx.author.top_role <= member.top_role:
            raise commands.BadArgument("Your top role is not above this member's top role.")

        await member.kick(reason=reason)
        e = discord.Embed(title=f":white_check_mark: **Kicked {member}**", color=discord.Colour.green())
        if reason is not None:
            e.description = f"**Reason:** {reason}"
        await ctx.channel.send(embed=e)

    @commands.command(help="Bans a user")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: Union[discord.Member, discord.User], *, reason=None):
        if ctx.author != ctx.guild.owner and ctx.author.top_role <= member.top_role:
            raise commands.BadArgument("Your top role is not above this member's top role.")

        await ctx.guild.ban(user=member, reason=reason)
        e = discord.Embed(title=f":white_check_mark: **Banned {member}**", color=discord.Colour.green())
        if reason is not None:
            e.description = f"**Reason:** {reason}"
        await ctx.channel.send(embed=e)

    @commands.command(help="Unbans a user")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User, *, reason=None):
        try:
            await ctx.guild.unban(user=user, reason=reason)
        except discord.NotFound:
            raise commands.BadArgument("No ban found for this user.")

        e = discord.Embed(title=f":white_check_mark: **Unbanned {user}**", color=discord.Colour.green())
        if reason is not None:
            e.description = f"**Reason:** {reason}"
        await ctx.channel.send(embed=e)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
