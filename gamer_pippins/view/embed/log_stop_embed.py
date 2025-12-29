import discord, datetime
from zoneinfo import ZoneInfo
from gamer_pippins.logger import MyLogger
from gamer_pippins.utils import getGameIconUrl


class LogStopEmbed:
    def __init__(self, game, seconds):
        hr, seconds = divmod(seconds, 3600)
        min, sec = divmod(seconds, 60)
        units = [(hr, "시간"), (min, "분"), (sec, "초")]
        formatted = " ".join([f"{num}{unit}" for num, unit in units if num])
        if not formatted:
            formatted = "??? "
            MyLogger.logger.warning(f"`{game.name}`의 플레이 시간이 0초로 기록됨.")

        embed = discord.Embed(description=f"{formatted}동안 플레이함",
                                color=discord.Color.brand_red(),
                                timestamp=datetime.datetime.now(tz=ZoneInfo("Asia/Seoul")))
        embed.set_author(name=game.name,
                            icon_url= getGameIconUrl(game))    
        embed.set_footer(text="LOG")
        self.embed = embed


    def getEmbed(self):
        return self.embed