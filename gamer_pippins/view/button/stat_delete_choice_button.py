import discord
from gamer_pippins.view.embed import deleteEntry
from gamer_pippins.utils import disableEveryItem


class StatDeleteYesButton(discord.ui.Button):
    def __init__(self, games: list[str], parentView: discord.ui.View):
        super().__init__(
            style = discord.ButtonStyle.primary,
            emoji = "<:PippinsHappy:1447391841111511181>",
            label = "응"
        ) 
        self.games = games
        self.parentView = parentView

    async def callback(self, interaction: discord.Interaction):
        await disableEveryItem(interaction.message, self.parentView)    # type: ignore
        success = await deleteEntry(interaction.user, self.games)
        if success:
            await interaction.response.send_message(f"최근 통계에서 {', '.join([f'`{game}`' for game in self.games])}을 삭제했어!")
        else:
            await interaction.response.send_message(f"이런! 최근 통계에 {', '.join([f'`{game}`' for game in self.games])}이(가) 없잖아?")


class StatDeleteNoButton(discord.ui.Button):
    def __init__(self, games: list[str], parentView: discord.ui.View):
        super().__init__(
            style = discord.ButtonStyle.secondary,
            emoji = "<:PippinsSad:1447391843473031258>",
            label = "아니"
        )
        self.games = games
        self.parentView = parentView

    async def callback(self, interaction: discord.Interaction):
        await disableEveryItem(interaction.message, self.parentView)    # type: ignore
        await interaction.response.send_message(f"최근 통계에서 {', '.join([f'`{game}`' for game in self.games])}을 유지했어!")