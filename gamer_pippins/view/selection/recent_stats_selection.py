class RecentStatsSelection(discord.ui.Select):
    async def getLatestStatGames(self):
        games = []

        async for msg in GAMER_PIPPINS.getChannelFromID(self.userID, "stat").history(limit=1):   # type: ignore
            embedDict = msg.embeds[0].to_dict()
            if embedDict.get("fields") is None:
                GAMER_PIPPINS.logger.info(f"유저 아이디 `{self.userID}`의 최신 통계에 항목 없음.")
                return False
            games = [field["name"] for field in embedDict.get("fields")]    # type: ignore
            GAMER_PIPPINS.logger.debug(f"유저 아이디 `{self.userID}`의 최신 통계에서 `{games}` 취득함.")

        return [discord.SelectOption(label="선택 취소하기!", emoji="🚫", value="SELECTION_CANCELLED")] \
             + [discord.SelectOption(label=name) if name else discord.SelectOption(label="???") for name in games]
    
    
    async def init(self, view: discord.ui.View, userID: str):
        self.parentView = view
        self.userID = userID
        options = await self.getLatestStatGames()
        if options is False:
            super().__init__(placeholder="제일 최근의 통계에 기록된 게임 목록",
                             options=[discord.SelectOption(label="앗?! 제일 최근의 통계가 비어 있어!", emoji="🚫", value="SELECTION_CANCELLED")])
            GAMER_PIPPINS.logger.info("빈 선택 UI 생성됨.")
        else:
            super().__init__(placeholder="제일 최근의 통계에 기록된 게임 목록", options=options)   # type: ignore
            GAMER_PIPPINS.logger.info("정상적인 선택 UI 생성됨.")

    
    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.message.edit(view=self.parentView) # type: ignore
        GAMER_PIPPINS.logger.info(f"메시지 뷰 비활성화됨. ({interaction.message.jump_url})") # type: ignore

        if self.values[0] == "SELECTION_CANCELLED":
            await interaction.response.send_message("블랙리스트 추가를 취소했어!") # type: ignore
            return

        append_blacklist(self.userID, self.values)
        await interaction.response.send_message(f"블랙리스트에 {', '.join([f'`{value}`' for value in self.values])}이(가) 추가됐어!\n제일 최근 통계에서 {', '.join([f'`{value}`' for value in self.values])}을(를) 삭제할래?", view=statDeleteConfirmView(self.values)) # type: ignore
