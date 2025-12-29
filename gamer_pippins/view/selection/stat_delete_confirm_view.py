import discord
from gamer_pippins.view.button import StatDeleteYesButton, StatDeleteNoButton


class StatDeleteConfirmView(discord.ui.View):
    def __init__(self, games: list[str]):
        super().__init__(timeout=None)
        self.add_item(StatDeleteYesButton(games, self))
        self.add_item(StatDeleteNoButton(games, self))