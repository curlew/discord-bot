from typing import Union
import discord
from discord.ext import commands
from utils import format_datetime


class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def userinfo(self,
                       ctx: commands.Context,
                       user: Union[discord.Member,
                                   discord.User] = commands.Author):
        """Shows information about a user"""
        e = discord.Embed(title=f"**{user}**", color=discord.Color.dark_blue())
        e.set_thumbnail(url=user.display_avatar)
        e.set_footer(text=f"ID: {user.id}")
        if user.banner:
            e.set_image(url=user.banner)
        e.add_field(inline=True,
                    name="**Created**",
                    value=format_datetime(user.created_at))

        if flags := ", ".join(flag.name for flag in user.public_flags.all()):
            # TODO:
            e.add_field(inline=True, name="**Badges**", value=flags)

        if isinstance(user, discord.Member):
            e.add_field(inline=True,
                        name="**Joined**",
                        value=format_datetime(user.joined_at))

            # skip @everyone (roles[0])
            if roles := ", ".join(role.name for role in user.roles[1:]):
                e.add_field(inline=True, name="**Roles**", value=roles)

            if user.premium_since:
                e.add_field(inline=True,
                            name="**Boosting since**",
                            value=format_datetime(user.premium_since))

        await ctx.send(embed=e)

    @commands.hybrid_command(aliases=["guildinfo"])
    @commands.guild_only()
    async def serverinfo(self, ctx: commands.Context):
        """Shows information about the server"""
        guild = ctx.guild

        e = discord.Embed(title=f"**{guild.name}**",
                          color=discord.Color.dark_blue())
        e.set_thumbnail(url=guild.icon)
        e.set_footer(text=f"ID: {guild.id}")
        if guild.description:
            e.description = guild.description

        e.add_field(inline=True, name="**Owner**", value=str(guild.owner))
        e.add_field(inline=True,
                    name="**Created**",
                    value=format_datetime(guild.created_at))
        e.add_field(inline=True, name="**Members**", value=guild.member_count)
        if guild.premium_subscription_count != 0:
            e.add_field(inline=True,
                        name="**Boosts**",
                        value=guild.premium_subscription_count)
        if emojis := " ".join(str(emoji) for emoji in guild.emojis):
            e.add_field(inline=True, name="**Emojis**", value=emojis)

        await ctx.send(embed=e)


async def setup(bot):
    await bot.add_cog(General(bot))
