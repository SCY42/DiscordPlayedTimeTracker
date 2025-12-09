import discord, datetime, requests
from zoneinfo import ZoneInfo
from gamer_pippins.bot.bot import GAMER_PIPPINS
from gamer_pippins.utils.get_game_icon_url import getGameIconUrl


# TODO 뜯어온 메서드 알맞게 수정
class LogStartEmbed:
    def __init__(self, gameName: str, timestamp: datetime.datetime):
        embed = discord.Embed(description=f"<t:{int(timestamp.timestamp())}:R>에 플레이 시작",
                              color=discord.Color.brand_green(),
                              timestamp=timestamp)
        embed.set_author(name=gameName,
                         icon_url=getGameIconUrl(gameName))    
        embed.set_footer(text="LOG")
        return embed