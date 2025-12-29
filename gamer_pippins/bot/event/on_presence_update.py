import discord, datetime
from discord.ext.commands import Cog
from zoneinfo import ZoneInfo
from gamer_pippins.view.embed import LogStartEmbed, LogStopEmbed, StatEmbed
from gamer_pippins.trackers.manage_now_playing import delFromNowPlaying, addToNowPlaying
from gamer_pippins.utils import getChannelFromID
from gamer_pippins.config import ConfigManager
from gamer_pippins.logger import MyLogger
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from bot import Pippins


class PresenceListener(Cog):
    def __init__(self, bot: "Pippins"):
        self.bot = bot
        

    @Cog.listener(name="on_presence_update")
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        if before.guild != ConfigManager.gamingGuild:
            return
        
        timestamp = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))
        
        logChannel = getChannelFromID(before.id, "log")
        if not logChannel: return

        statChannel = getChannelFromID(before.id, "stat")

        gamesBefore = [game for game in before.activities if game.type == discord.ActivityType.playing \
                    and game.name not in [_game["name"] for _game in ConfigManager.blacklist[str(before.id)]]]
        gamesAfter = [game for game in after.activities if game.type == discord.ActivityType.playing \
                    and game.name not in [_game["name"] for _game in ConfigManager.blacklist[str(before.id)]]]

        stoppedPlaying = [game for game in gamesBefore if game.name not in [_game.name for _game in gamesAfter]]
        startedPlaying = [game for game in gamesAfter if game.name not in [_game.name for _game in gamesBefore]]

        if not (stoppedPlaying or startedPlaying):
            return

        logText = f"===== `{before.display_name}`의 활동 상태 업데이트됨 =====\n\n" \
        + f"gamesBefore: `{gamesBefore}`\n" \
        + f"gamesAfter: `{gamesAfter}`\n" \
        + f"stoppedPlaying: `{stoppedPlaying}`\n" \
        + f"startedPlaying: `{startedPlaying}`"
        MyLogger.logger.info(logText)
        
        if stoppedPlaying:
            for game in stoppedPlaying:
                timestamp, seconds = delFromNowPlaying(before, game)

                await logChannel.send(embed=LogStopEmbed(game.name, seconds).getEmbed())   # type: ignore

                msgExists = False
                async for msg in statChannel.history(limit=1):  # type: ignore
                    msgExists = True
                    embed, isNewMsg = StatEmbed(msg.embeds[0], game, timestamp).getEmbed()
                    if isNewMsg:
                        await statChannel.send(embed=embed) # type: ignore
                    else:
                        await msg.edit(embed=embed)
                if not msgExists:
                    embed, _ = StatEmbed(None, game, timestamp).getEmbed()
                    await statChannel.send(embed=embed) # type: ignore

        if startedPlaying:
            for game in startedPlaying:
                addToNowPlaying(before, str(game.name))
                await logChannel.send(embed=LogStartEmbed(game.name, timestamp).getEmbed())  # type: ignore