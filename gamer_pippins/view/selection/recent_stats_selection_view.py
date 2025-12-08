class RecentStatsSelectionView(discord.ui.View):
    async def init(self, userID: str):
        super().__init__()
        sel = RecentStatsSelection()
        await sel.init(self, userID)
        self.add_item(sel)