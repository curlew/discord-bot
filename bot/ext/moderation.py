from typing import Union, Literal
import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        autorole_id = await self.bot.db_pool.fetchval("SELECT autorole_id FROM guilds WHERE id = $1", guild.id)
        if autorole_id is not None:
            autorole = discord.utils.get(guild.roles, id=autorole_id)
            await member.add_roles(autorole)

    @commands.command(help="Sets a role to be automatically assigned to new members")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def autorole(self, ctx,
                       option: Literal["enable", "disable", "status"]
                       = commands.param(description="enable/disable/status"),
                       role: discord.Role = None):
        e = discord.Embed(color=discord.Color.green())

        if option == "enable":
            if role is None:
                raise commands.MissingRequiredArgument(self.autorole.params["role"])
            query = """INSERT INTO guilds (id, autorole_id) VALUES ($1, $2)
                       ON CONFLICT (id) DO UPDATE SET autorole_id = EXCLUDED.autorole_id"""
            await self.bot.db_pool.execute(query, ctx.guild.id, role.id)
            e.title = f"Set autorole to *{role.name}*"
        elif option == "disable":
            query = """INSERT INTO guilds (id, autorole_id) VALUES ($1, NULL)
                       ON CONFLICT (id) DO UPDATE SET autorole_id = NULL"""
            await self.bot.db_pool.execute(query, ctx.guild.id)
            e.title = "Disabled autorole"
        elif option == "status":
            query = "SELECT autorole_id FROM guilds WHERE id = $1"
            current_autorole_id = await self.bot.db_pool.fetchval(query, ctx.guild.id)
            if current_autorole_id is None:
                e.title = f"Autorole is currently disabled"
            else:
                current_autorole = discord.utils.get(ctx.guild.roles, id=current_autorole_id)
                e.title = f"The current autorole is *{current_autorole}*"

        await ctx.channel.send(embed=e)

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
