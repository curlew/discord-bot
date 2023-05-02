from typing import Union
import discord
from discord.ext import commands


class Moderation(commands.Cog):
    """Server moderation commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        autorole_id = await self.bot.db_pool.fetchval(
            "SELECT autorole_id FROM guilds WHERE id = $1", guild.id)
        if autorole_id is not None:
            autorole = discord.utils.get(guild.roles, id=autorole_id)
            await member.add_roles(autorole)

    @commands.hybrid_group(name="autorole",
                           fallback="get",
                           invoke_without_command=True)
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def autorole(self, ctx: commands.Context):
        """Show the current autorole"""
        query = "SELECT autorole_id FROM guilds WHERE id = $1"
        current_autorole_id = await self.bot.db_pool.fetchval(
            query, ctx.guild.id)
        e = discord.Embed(color=discord.Color.green())
        if current_autorole_id is None:
            e.title = "Autorole is currently disabled"
        else:
            current_autorole = discord.utils.get(ctx.guild.roles,
                                                 id=current_autorole_id)
            e.title = f"The current autorole is *{current_autorole}*"
        await ctx.send(embed=e)

    @autorole.command(name="set")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def autorole_set(self, ctx: commands.Context, role: discord.Role):
        """Automatically assign a role to new members"""
        if role.is_default():
            raise commands.BadArgument("Role cannot be @everyone.")
        if ctx.author.top_role < role and ctx.author != ctx.guild.owner:
            raise commands.BadArgument(
                "Your top role must be above the desired autorole.")
        query = """INSERT INTO guilds (id, autorole_id) VALUES ($1, $2)
                   ON CONFLICT (id) DO UPDATE SET autorole_id = EXCLUDED.autorole_id"""
        await self.bot.db_pool.execute(query, ctx.guild.id, role.id)
        await ctx.send(
            embed=discord.Embed(title=f"Set autorole to *{role.name}*",
                                color=discord.Color.green()))

    @autorole.command(name="off")
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def autorole_off(self, ctx: commands.Context):
        """Disable the autorole"""
        query = """INSERT INTO guilds (id, autorole_id) VALUES ($1, NULL)
                   ON CONFLICT (id) DO UPDATE SET autorole_id = NULL"""
        await self.bot.db_pool.execute(query, ctx.guild.id)
        await ctx.send(embed=discord.Embed(title="Disabled autorole",
                                           color=discord.Color.green()))

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self,
                   ctx: commands.Context,
                   member: discord.Member,
                   *,
                   reason=None):
        """Kick a user"""
        if ctx.author != ctx.guild.owner and ctx.author.top_role <= member.top_role:
            raise commands.BadArgument(
                "Your top role is not above this member's top role.")

        await member.kick(reason=reason)
        await ctx.send(embed=discord.Embed(
            title=f":white_check_mark: **Kicked {member}**",
            color=discord.Color.green(),
            description=f"**Reason:** {reason}" if reason else None))

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self,
                  ctx: commands.Context,
                  member: Union[discord.Member, discord.User],
                  *,
                  reason=None):
        """Ban a user"""
        if ctx.author != ctx.guild.owner and ctx.author.top_role <= member.top_role:
            raise commands.BadArgument(
                "Your top role is not above this member's top role.")

        await ctx.guild.ban(user=member, reason=reason)
        await ctx.send(embed=discord.Embed(
            title=f":white_check_mark: **Banned {member}**",
            color=discord.Color.green(),
            description=f"**Reason:** {reason}" if reason else None))

    @commands.hybrid_command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self,
                    ctx: commands.Context,
                    user: discord.User,
                    *,
                    reason=None):
        """Unban a user"""
        try:
            await ctx.guild.unban(user=user, reason=reason)
        except discord.NotFound:
            raise commands.BadArgument("No ban found for this user.")

        await ctx.send(embed=discord.Embed(
            title=f":white_check_mark: **Unbanned {user}**",
            color=discord.Color.green(),
            description=f"**Reason:** {reason}" if reason else None))


async def setup(bot):
    await bot.add_cog(Moderation(bot))
