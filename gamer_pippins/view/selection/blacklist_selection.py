class BlacklistSelection(discord.ui.Select):
    async def getCancelPlusBlacklistOptions(self):
        self.blacklist = [discord.SelectOption(label="선택 취소하기!", emoji="🚫", value="SELECTION_CANCELLED")] \
                       + [discord.SelectOption(label=name) if name else discord.SelectOption(label="???") \
                          for name in [entry["name"] for entry in GAMER_PIPPINS.BLACKLIST[self.userID]]]

    async def init(self, view: discord.ui.View, userID: str):
        self.parentView = view
        self.userID = userID
        load_blacklist()
        await self.getCancelPlusBlacklistOptions()
        super().__init__(placeholder="블랙리스트에 등록된 게임 목록", options=self.blacklist)

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.message.edit(view=self.parentView) # type: ignore
        GAMER_PIPPINS.logger.info(f"메시지 뷰 비활성화됨. ({interaction.message.jump_url})") # type: ignore

        if self.values[0] == "SELECTION_CANCELLED":
            await interaction.response.send_message("블랙리스트 삭제를 취소했어!") # type: ignore
            return

        remove_blacklist(self.userID, self.values)
        await interaction.response.send_message(f"블랙리스트에서 {', '.join([f'`{value}`' for value in self.values])}이(가) 삭제됐어!") # type: ignore