import discord, json, datetime
from zoneinfo import ZoneInfo
from Pippins import GAMER_PIPPINS, TREE
from EditStatEmbed import deleteEntry


def load_blacklist():
    with open("blacklist.json", 'r', encoding="utf8") as f:
        GAMER_PIPPINS.BLACKLIST = json.load(f)


load_blacklist()


def save_blacklist():
    with open("blacklist.json", 'w', encoding="utf8") as f:
        for blacklist in GAMER_PIPPINS.BLACKLIST.values():
            blacklist.sort(key=lambda x: x["date"], reverse=True)
        json.dump(GAMER_PIPPINS.BLACKLIST, f, indent=4)


def append_blacklist(userID: str, gamesToAppend: list[str]):
    load_blacklist()
    now = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))

    for gameName in gamesToAppend:
        for entry in GAMER_PIPPINS.BLACKLIST[userID]:
            if entry["name"] == gameName:
                entry["date"] = f"{now.year}년 {now.month}월 {now.day}일"
                break
        else:
            GAMER_PIPPINS.BLACKLIST[userID].append({"name": gameName, "date": f"{now.year}년 {now.month}월 {now.day}일"})
    
    save_blacklist()


def remove_blacklist(userID: str, gamesToRemove: list[str]):
    load_blacklist()

    for gameName in gamesToRemove:
        for entry in GAMER_PIPPINS.BLACKLIST[userID]:
            if entry["name"] == gameName:
                GAMER_PIPPINS.BLACKLIST[userID].remove(entry)

    save_blacklist()


class RecentStatsSelection(discord.ui.Select):
    async def getLatestStatGames(self):
        games = []

        async for msg in GAMER_PIPPINS.getChannelFromID(self.userID, "stat").history(limit=1):   # type: ignore
            embedDict = msg.embeds[0].to_dict()
            if embedDict.get("fields") is None:
                return False
            games = [field["name"] for field in embedDict.get("fields")]    # type: ignore

        return [discord.SelectOption(label="선택 취소하기!", emoji="🚫", value="SELECTION_CANCELLED")] \
             + [discord.SelectOption(label=name) if name else discord.SelectOption(label="???") for name in games]
    
    
    async def init(self, view: discord.ui.View, userID: str):
        self.parentView = view
        self.userID = userID
        options = await self.getLatestStatGames()
        if options is False:
            super().__init__(placeholder="제일 최근의 통계에 기록된 게임 목록",
                             options=[discord.SelectOption(label="앗?! 제일 최근의 통계가 비어 있어!", emoji="🚫", value="SELECTION_CANCELLED")])
        else:
            super().__init__(placeholder="제일 최근의 통계에 기록된 게임 목록", options=options)   # type: ignore

    
    async def callback(self, interaction: discord.Interaction):
        self.disabled = True
        await interaction.message.edit(view=self.parentView) # type: ignore

        if self.values[0] == "SELECTION_CANCELLED":
            await interaction.response.send_message("블랙리스트 추가를 취소했어!") # type: ignore
            return

        append_blacklist(self.userID, self.values)
        await interaction.response.send_message(f"블랙리스트에 {', '.join([f'`{value}`' for value in self.values])}이(가) 추가됐어!\n제일 최근 통계에서 {', '.join([f'`{value}`' for value in self.values])}을(를) 삭제할래?", view=statDeleteConfirmView(self.values)) # type: ignore


class RecentStatsSelectionView(discord.ui.View):
    async def init(self, userID: str):
        super().__init__()
        sel = RecentStatsSelection()
        await sel.init(self, userID)
        self.add_item(sel)


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

        if self.values[0] == "SELECTION_CANCELLED":
            await interaction.response.send_message("블랙리스트 삭제를 취소했어!") # type: ignore
            return

        remove_blacklist(self.userID, self.values)
        await interaction.response.send_message(f"블랙리스트에서 {', '.join([f'`{value}`' for value in self.values])}이(가) 삭제됐어!") # type: ignore


class BlacklistSelectionView(discord.ui.View):
    async def init(self, userID: str):
        super().__init__()
        sel = BlacklistSelection()
        await sel.init(self, userID)
        self.add_item(sel)


class StatDeleteYesButton(discord.ui.Button):
    def __init__(self, games: list[str], parentView: discord.ui.View):
        super().__init__(
            style = discord.ButtonStyle.primary,
            emoji = "<:pippinsHappy:1422640037404741704>",
            label = "응"
        ) 
        self.games = games
        self.parentView = parentView

    async def callback(self, interaction: discord.Interaction):
        await disableEveryItem(interaction.message, self.parentView)    # type: ignore
        success = await deleteEntry(self.games)
        if success:
            await interaction.response.send_message(f"최근 통계에서 {', '.join([f'`{game}`' for game in self.games])}을 삭제했어!")
        else:
            await interaction.response.send_message(f"이런! 최근 통계에 {', '.join([f'`{game}`' for game in self.games])}이 없잖아?")


class StatDeleteNoButton(discord.ui.Button):
    def __init__(self, games: list[str], parentView: discord.ui.View):
        super().__init__(
            style = discord.ButtonStyle.secondary,
            emoji = "<:pippinsSad:1422640022766485596>",
            label = "아니"
        )
        self.games = games
        self.parentView = parentView

    async def callback(self, interaction: discord.Interaction):
        await disableEveryItem(interaction.message, self.parentView)    # type: ignore
        await interaction.response.send_message(f"최근 통계에서 {', '.join([f'`{game}`' for game in self.games])}을 유지했어!")


def statDeleteConfirmView(games: list[str]):
    view = discord.ui.View()
    view.add_item(StatDeleteYesButton(games, view))
    view.add_item(StatDeleteNoButton(games, view))

    return view


async def disableEveryItem(msg: discord.Message, view: discord.ui.View):
    for item in view.children:
        item.disabled = True    # type: ignore
    
    await msg.edit(view=view)


@TREE.command(name="블랙리스트_확인", description="로그와 통계에서 제외될 블랙리스트를 확인해!")
async def viewBlacklist(i: discord.Interaction):
    load_blacklist()
    embed = discord.Embed(title="<:cross:1421630412022743040>블랙리스트")
    userID = str(i.user.id)

    if GAMER_PIPPINS.BLACKLIST[userID]:
        for game in GAMER_PIPPINS.BLACKLIST[userID]:
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
    await view.init(str(i.user.id))
    await i.response.send_message(view=view)


@TREE.command(name="블랙리스트_직접_추가", description="블랙리스트에 추가할 게임의 이름을 직접 입력해!")
@discord.app_commands.describe(game="정확하게 적어야 되는 거 알지?")
async def addBlacklistManual(interaction: discord.Interaction, game: str):
    append_blacklist(str(interaction.user.id), [game])
    await interaction.response.send_message(content=f"블랙리스트에 `{game}`이(가) 추가됐어!\n제일 최근 통계에서 `{game}`을(를) 삭제할래?", view=statDeleteConfirmView([game]))


@TREE.command(name="블랙리스트_제거", description="블랙리스트에서 게임을 제거해!")
async def removeBlacklist(i: discord.Interaction):
    view = BlacklistSelectionView()
    await view.init(str(i.user.id))
    options = [entry["name"] for entry in GAMER_PIPPINS.BLACKLIST[str(i.user.id)]]

    if not options:
        await i.response.send_message("블랙리스트가 비어 있어!")
    else:
        await i.response.send_message(view=view)