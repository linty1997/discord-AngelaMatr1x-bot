from discord.commands import slash_command, Option, OptionChoice
from discord.ext import commands
import discord


class Main(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ping
    @slash_command(description="Get bot ping.")
    async def ping(self, ctx):
        await ctx.respond(f"`{round(self.bot.latency * 1000)} ms`", ephemeral=True)

    @slash_command(description="Give roles in batches from Voice channel.")
    @commands.has_permissions(administrator=True)
    async def give_roles(self, ctx, role: discord.Role, channel_id: Option(str, required=False)):
        await ctx.defer(ephemeral=True)
        not_allowed_roles = [947693944525946900, 1072808183111893033, 1077491907086798858, 1012687394799108127,
                             1060832489377116241, 1020896531777327144, 1069184681548992513, 1070221518992310273,
                             1072408513269207040, 1069140078762393652, 1081858245905354782]

        if role.id in not_allowed_roles:
            await ctx.send_followup(f"Not allowed to give {role.mention}")

        channel = self.bot.get_channel(int(channel_id))
        count = 0
        for member in channel.members:
            await member.add_roles(role)
            count += 1

        await ctx.send_followup(f"Give {role.mention} Done. Total `{count}`.")


def setup(bot):
    bot.add_cog(Main(bot))

