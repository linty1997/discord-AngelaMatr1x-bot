from discord.commands import slash_command, Option, OptionChoice
from discord.ext import commands
from components.buttons import LeaderBoardView, CheckInView
from components.embeds import FractionEmbed
import discord

from core.sql import UserDB


class Fraction(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Set leader board.")
    @commands.has_permissions(administrator=True)
    async def set_leader_board(self, ctx, channel: discord.TextChannel):
        await ctx.defer(ephemeral=True)
        await channel.send("Leader Board", view=LeaderBoardView())
        await ctx.send_followup("Leader Board 設置完成", delete_after=5)

    @slash_command(description="Set check-in button.")
    @commands.has_permissions(administrator=True)
    async def set_check_in(self, ctx, channel: discord.TextChannel):
        await ctx.defer(ephemeral=True)
        await channel.send(view=CheckInView())
        await ctx.send_followup("Daily check-in 設置完成", delete_after=5)

    @slash_command(description="Check Total FIRE Sparks.")
    async def check_points(self, ctx, user: discord.Member = None):
        await ctx.defer(ephemeral=True)
        user_id = user.id if user else ctx.user.id
        points = await UserDB(ctx).get_user_fractions(user_id)
        embed = await FractionEmbed(ctx).check_points(points)
        await ctx.send_followup(embed=embed)

    @slash_command(description="Add user FIRE Sparks.")
    @commands.has_permissions(administrator=True)
    async def add_user_points(self, ctx, user: discord.Member, points: int):
        await ctx.defer(ephemeral=True)
        await UserDB(ctx).update_user_fraction(user, points)
        await ctx.send_followup(f"{user.mention} 獲得 `{points}` 點積分.")

    @slash_command(description="Add role FIRE Sparks.")
    @commands.has_permissions(administrator=True)
    async def add_role_points(self, ctx, role: discord.Role, points: int):
        await ctx.defer(ephemeral=True)
        for member in role.members:
            await UserDB(ctx).update_user_fraction(member, points)
        await ctx.send_followup(f"{role.mention} 獲得 `{points}` 點積分.")

    @slash_command(description="Remove user FIRE Sparks.")
    @commands.has_permissions(administrator=True)
    async def remove_user_points(self, ctx, user: discord.Member, points: int):
        await ctx.defer(ephemeral=True)
        await UserDB(ctx).update_user_fraction(user, -points)
        await ctx.send_followup(f"{user.mention} 刪除 `{points}` 點積分.")

    @slash_command(description="Remove role FIRE Sparks.")
    @commands.has_permissions(administrator=True)
    async def remove_role_points(self, ctx, role: discord.Role, points: int):
        await ctx.defer(ephemeral=True)
        for member in role.members:
            await UserDB(ctx).update_user_fraction(member, -points)
        await ctx.send_followup(f"{role.mention} 刪除 `{points}` 點積分.")

    @slash_command(description="Settle accounts.")
    @commands.has_permissions(administrator=True)
    async def settle_accounts(self, ctx, days: int = 30, points: int = 50):
        await ctx.defer(ephemeral=True)
        await UserDB(ctx).settle_accounts(days, points)
        await ctx.send_followup("`Done.`")


def setup(bot):
    bot.add_cog(Fraction(bot))
