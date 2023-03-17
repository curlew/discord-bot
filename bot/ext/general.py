from typing import Union
from datetime import datetime
import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx: commands.Context,
                       user: Union[discord.Member, discord.User] = None):
        if user is None:
            user = ctx.author

        def format_datetime(dt: datetime) -> str:
            return dt.strftime("%Y-%m-%d %H:%M:%S %Z")

        e = discord.Embed(title=f"**{user}**", color=discord.Color.dark_blue())
        e.set_thumbnail(url=user.display_avatar)
        if user.banner:
            e.set_image(url=user.banner)
        e.add_field(inline=True, name="**Created**", value=format_datetime(user.created_at))
        e.add_field(inline=True, name="**ID**", value=user.id)

        flags = ", ".join(flag.name for flag in user.public_flags.all())
        if flags:
            # TODO:
            e.add_field(inline=True, name="**Badges**", value=flags)

        if isinstance(user, discord.Member):
            e.add_field(inline=True, name="**Joined**", value=format_datetime(user.joined_at))

            # skip @everyone (roles[0])
            roles = ", ".join(role.name for role in user.roles[1:])
            if roles:
                e.add_field(inline=True, name="**Roles**", value=roles)

            if user.premium_since:
                e.add_field(inline=True, name="**Boosting since**", value=format_datetime(user.premium_since))

        await ctx.channel.send(embed=e)

async def setup(bot):
    await bot.add_cog(General(bot))
