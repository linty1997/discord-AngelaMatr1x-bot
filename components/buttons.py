import discord
from core.sql import UserDB


# class LeaderBoardView(discord.ui.View):  # TODO: 暫不弄網頁, 用 discord ui 代替
#     def __init__(self):
#         super().__init__(timeout=None)
#         button = discord.ui.Button(label="Go to Leaderboard",
#                                    url="https://google.com",
#                                    style=discord.ButtonStyle.link,
#                                    emoji="<a:Matr1x:1076090808773644308>")
#         self.add_item(button)


class LeaderBoardView(discord.ui.View):  # TODO: Leader board button
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="Leader board",
                                   style=discord.ButtonStyle.green,
                                   emoji='<a:Zeal:1076090858807496754>',
                                   custom_id="leader_board_btn")

        button.callback = self.button_callback
        self.leaderboard_selector = None
        self.pages = []
        self.next_button = None
        self.previous_button = None
        self.page = 1
        self.val = None
        self.add_item(button)

    async def button_callback(self, interaction):
        await interaction.response.defer(ephemeral=True, invisible=False)
        self.leaderboard_selector = discord.ui.Select(placeholder='Select leaderboard type',
                                                      options=[
                                                          discord.SelectOption(label='Fraction', value='fraction',
                                                                               emoji='<a:Zeal:1076090858807496754>'),
                                                          discord.SelectOption(label='Old Fraction',
                                                                               value='old_fraction',
                                                                               emoji='<a:Hope:1076090847478681601>')
                                                      ], custom_id="leader_board")
        self.leaderboard_selector.callback = self.leaderboard_selector_callback
        self.clear_items()
        self.add_item(self.leaderboard_selector)
        await interaction.followup.send(view=self)

    async def leaderboard_selector_callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, invisible=False)
        user_db = UserDB(interaction)
        self.val = self.leaderboard_selector.values[0]
        db_data = await user_db.get_leader_board(old=self.leaderboard_selector.values[0] == 'old_fraction')

        self.pages = [db_data[i:i + 10] for i in range(0, len(db_data), 10)]

        self.next_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="⏩", custom_id="next")
        self.previous_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="⏪",
                                                 custom_id="previous")

        self.next_button.callback = self.next_page
        self.previous_button.callback = self.previous_page

        self.clear_items()
        self.add_item(self.previous_button)
        self.add_item(self.next_button)

        self.page = 1
        await interaction.followup.send(embed=self.create_embed(self.val), view=self)

    async def next_page(self, interaction: discord.Interaction):
        if self.page != len(self.pages):
            self.page += 1
            await interaction.response.edit_message(embed=self.create_embed(self.val), view=self)

    async def previous_page(self, interaction: discord.Interaction):
        if self.page > 1:
            self.page -= 1
            await interaction.response.edit_message(embed=self.create_embed(self.val), view=self)

    def create_embed(self, val):
        embed = discord.Embed(title="Leaderboard")

        for index, item in enumerate(self.pages[self.page - 1], start=(self.page - 1) * 10 + 1):
            embed.add_field(name=f"No.{index}",
                            value=f"{item.name}: {item.fraction if val == 'fraction' else item.old_fraction} ",
                            inline=False)

        embed.set_footer(text=f"Page {self.page}/{len(self.pages)}")

        return embed


class CheckInView(discord.ui.View):  # TODO: Check-in button
    def __init__(self, emoji='<a:check2:1070937444226191381>'):
        super().__init__(timeout=None)
        button = discord.ui.Button(label="Check-in",
                                   style=discord.ButtonStyle.primary,
                                   emoji=emoji,
                                   custom_id="check_in")
        button.callback = self.button_callback
        self.add_item(button)

    async def button_callback(self, interaction):
        await interaction.response.defer(ephemeral=True, invisible=False)
        user_db = UserDB(interaction)
        message = await user_db.update_user_sign_in(interaction.user)
        await interaction.followup.send(message)
