from discord.ext import commands
from components.buttons import LeaderBoardView, CheckInView
from core.sql import LogDB


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(LeaderBoardView())
        self.bot.add_view(CheckInView())

    @commands.Cog.listener()
    async def on_application_command_completion(self, ctx):
        user = ctx.author
        command = ctx.command.name
        command_options = ctx.selected_options
        event = f"Use command: {command}\n"

        for option in command_options:
            event += f"Option: {option['name']}-{option['value']}\n"

        await LogDB().add_log(user.id, event=event)


def setup(bot):
    bot.add_cog(Events(bot))

