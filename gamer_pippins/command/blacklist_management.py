import discord
from discord.ext.commands import Cog
from gamer_pippins.config import ConfigManager
from gamer_pippins.file_io.blacklist import load_blacklist, append_blacklist
from gamer_pippins.view.selection import RecentStatsSelectionView, BlacklistSelectionView, StatDeleteConfirmView


class BlacklistManagementCog(Cog):
    def __init__(self, bot):
        self.bot = bot


    @discord.app_commands.command(name="블랙리스트_확인", description="로그와 통계에서 제외될 블랙리스트를 확인해!")
    async def viewBlacklist(self, i: discord.Interaction):
        load_blacklist()
        embed = discord.Embed(title="<:cross:1421630412022743040>블랙리스트")
        userID = str(i.user.id)

        if ConfigManager.blacklist[userID]:
            for game in ConfigManager.blacklist[userID]:
                embed.add_field(name=game["name"],
                                value=game["date"] + "에 등록됨",
                                inline=False)
        else:
            embed.add_field(name="블랙리스트가 비어 있어!",
                            value="블랙리스트에 포함된 게임은 로그와 통계에 기록되지 않아!")

        await i.response.send_message(embed=embed)


    @discord.app_commands.command(name="블랙리스트_추가", description="최근에 플레이한 게임들 중에서 블랙리스트에 추가할 것을 선택해!")
    async def addBlacklist(self, i: discord.Interaction):
        view = RecentStatsSelectionView()
        await view.init(str(i.user.id))
        await i.response.send_message(view=view)


    @discord.app_commands.command(name="블랙리스트_직접_추가", description="블랙리스트에 추가할 게임의 이름을 직접 입력해!")
    @discord.app_commands.describe(game="정확하게 적어야 되는 거 알지?")
    async def addBlacklistManual(self, interaction: discord.Interaction, game: str):
        append_blacklist(str(interaction.user.id), [game])
        await interaction.response.send_message(content=f"블랙리스트에 `{game}`이(가) 추가됐어!\n제일 최근 통계에서 `{game}`을(를) 삭제할래?",
                                                view=StatDeleteConfirmView([game]))


    @discord.app_commands.command(name="블랙리스트_제거", description="블랙리스트에서 게임을 제거해!")
    async def removeBlacklist(self, i: discord.Interaction):
        view = BlacklistSelectionView()
        await view.init(str(i.user.id))
        options = [entry["name"] for entry in ConfigManager.blacklist[str(i.user.id)]]

        if not options:
            await i.response.send_message("블랙리스트가 비어 있어!")
        else:
            await i.response.send_message(view=view)