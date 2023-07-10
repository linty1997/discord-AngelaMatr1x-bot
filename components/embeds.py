from datetime import datetime

import discord


class FractionEmbed:
    def __init__(self, ctx):
        self.ctx = ctx
        self.embed = discord.Embed(timestamp=datetime.now())
        self.embed.set_author(name=f"{self.ctx.user.name}",
                              icon_url=f"{self.ctx.user.avatar.url}")
        self.embed.set_footer(text="Good luck",
                              icon_url="https://cdn.discordapp.com/attachments/936669290977980507/1127687943532843048"
                                       "/20230710034839.png")
        self.points_emoji = "<a:Matr1xred:1076789485100093461>"

    async def leader_board(self, pages, page, val):
        self.embed.title = "Leaderboard"
        self.embed.colour = 0xbdf047
        for index, item in enumerate(pages[page - 1], start=(page - 1) * 10 + 1):
            self.embed.add_field(name=f"No.{index}",
                                 value=f"{item.name}: {item.fraction if val == 'fraction' else item.old_fraction} ",
                                 inline=False)

        self.embed.set_footer(text=f"Page {page}/{len(pages)}")
        return self.embed

    async def check_in(self, message, points, total_points):
        self.embed.description = message
        self.embed.colour = 0x39ea86
        self.embed.add_field(name=f"Get Fire Sparks {self.points_emoji}",
                             value=f"{points}",
                             inline=True)
        self.embed.add_field(name=f"Total Fire Sparks {self.points_emoji}",
                             value=f"{total_points}",
                             inline=True)

        return self.embed

    async def check_points(self, points):
        self.embed.colour = 0x478bf0
        self.embed.add_field(name=f"Total Fire Sparks {self.points_emoji}",
                             value=f"{points}",
                             inline=True)
        return self.embed
