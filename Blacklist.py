import discord, json, datetime
from zoneinfo import ZoneInfo
from Pippins import GAMER_PIPPINS, TREE


def load_blacklist():
    with open("blacklist/blacklist.json", 'r', encoding="utf8") as f:
        GAMER_PIPPINS.BLACKLIST = json.load(f)


load_blacklist()


def save_blacklist():
    with open("blacklist/blacklist.json", 'w', encoding="utf8") as f:
        GAMER_PIPPINS.BLACKLIST.sort(key=lambda x: x["date"], reverse=True)
        json.dump(GAMER_PIPPINS.BLACKLIST, f, indent=4)


def append_blacklist(gamesToAppend: list[str]):
    load_blacklist()
    now = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))

    for gameName in gamesToAppend:
        for entry in GAMER_PIPPINS.BLACKLIST:
            if entry["name"] == gameName:
                entry["date"] = f"{now.year}년 {now.month}월 {now.day}일"
                break
        else:
            GAMER_PIPPINS.BLACKLIST.append({"name": gameName, "date": f"{now.year}년 {now.month}월 {now.day}일"})
    
    save_blacklist()


def remove_blacklist(gamesToRemove: list[str]):
    load_blacklist()

    for gameName in gamesToRemove:
        for entry in GAMER_PIPPINS.BLACKLIST:
            if entry["name"] == gameName:
                GAMER_PIPPINS.BLACKLIST.remove(entry)

    save_blacklist()


class RecentStatsSelection(discord.ui.Select):
    async def getLatestStatGames(self):
        games = []

        async for msg in GAMER_PIPPINS.STATISTICS_CHANNEL.history(limit=1):
            games = [field["name"] for field in msg.embeds[0].to_dict()["fields"]] # type: ignore

        return [discord.SelectOption(label="선택 취소하기!", emoji="🚫", value="SELECTION_CANCELLED")] \
             + [discord.SelectOption(label=name) if name else discord.SelectOption(label="???") for name in games]
    
    
    async def init(self, view: discord.ui.View):
        self.parentView = view
        self.options = await self.getLatestStatGames()
        super().__init__(placeholder="제일 최근의 통계에 기록된 게임 목록", options=self.options)

    
    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.response.edit_message(view=self.parentView)

        if self.values[0] == "SELECTION_CANCELLED":
            await interaction.channel.send("블랙리스트 추가를 취소했어!") # type: ignore
            return

        append_blacklist(self.values)
        await interaction.channel.send("블랙리스트에 게임이 추가됐어!") # type: ignore


class RecentStatsSelectionView(discord.ui.View):
    async def init(self):
        super().__init__()
        sel = RecentStatsSelection()
        await sel.init(self)
        self.add_item(sel)


class BlacklistSelection(discord.ui.Select):
    async def getCancelPlusBlacklistOptions(self):
        self.blacklist = [discord.SelectOption(label="선택 취소하기!", emoji="🚫", value="SELECTION_CANCELLED")] \
                       + [discord.SelectOption(label=name) if name else discord.SelectOption(label="???") \
                          for name in [entry["name"] for entry in GAMER_PIPPINS.BLACKLIST]]

    async def init(self, view: discord.ui.View):
        self.parentView = view
        load_blacklist()
        await self.getCancelPlusBlacklistOptions()
        super().__init__(placeholder="블랙리스트에 등록된 게임 목록", options=self.blacklist)

    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.response.edit_message(view=self.parentView)

        if self.values[0] == "SELECTION_CANCELLED":
            await interaction.channel.send("블랙리스트 삭제를 취소했어!") # type: ignore
            return

        remove_blacklist(self.values)
        await interaction.channel.send("블랙리스트에서 게임이 삭제됐어!") # type: ignore


class BlacklistSelectionView(discord.ui.View):
    async def init(self):
        super().__init__()
        sel = BlacklistSelection()
        await sel.init(self)
        self.add_item(sel)


@TREE.command(name="블랙리스트_확인", description="로그와 통계에서 제외될 블랙리스트를 확인해!")
async def viewBlacklist(i: discord.Interaction):
    load_blacklist()
    embed = discord.Embed(title="<:cross:1421630412022743040>블랙리스트")

    if GAMER_PIPPINS.BLACKLIST:
        for game in GAMER_PIPPINS.BLACKLIST:
            embed.add_field(name=game["name"],
                            value=game["date"] + "에 등록됨",
                            inline=False)
    else:
        embed.add_field(name="블랙리스트가 비어 있어!",
                        value="블랙리스트에 포함된 게임은 로그와 통계에 기록되지 않아!")

    await i.response.send_message(embed=embed)


@TREE.command(name="블랙리스트_추가", description="최근에 플레이한 게임들 중에서 블랙리스트에 추가할 것을 선택해!")
async def addBlacklist(i: discord.Interaction):
    view = RecentStatsSelectionView()
    await view.init()
    await i.response.send_message(view=view)


@TREE.command(name="블랙리스트_직접_추가", description="블랙리스트에 추가할 게임의 이름을 직접 입력해!")
@discord.app_commands.describe(game="정확하게 적어야 되는 거 알지?")
async def addBlacklistManual(interaction: discord.Interaction, game: str):
# async def addBlacklistManual(i: discord.Interaction):
    append_blacklist([game])
    await interaction.response.send_message("블랙리스트가 업데이트됐어!")


@TREE.command(name="블랙리스트_제거", description="블랙리스트에서 게임을 제거해!")
async def removeBlacklist(i: discord.Interaction):
    view = BlacklistSelectionView()
    await view.init()
    options = [entry["name"] for entry in GAMER_PIPPINS.BLACKLIST]

    if not options:
        await i.response.send_message("블랙리스트가 비어 있어!")
    else:
        await i.response.send_message(view=view)