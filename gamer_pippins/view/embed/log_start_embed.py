import discord, datetime
from gamer_pippins.utils import getGameIconUrl


class LogStartEmbed:
    def __init__(self, gameName: str, timestamp: datetime.datetime):
        embed = discord.Embed(description=f"<t:{int(timestamp.timestamp())}:R>에 플레이 시작",
                              color=discord.Color.brand_green(),
                              timestamp=timestamp)
        embed.set_author(name=gameName,
                         icon_url=getGameIconUrl(gameName))    
        embed.set_footer(text="LOG")
        self.embed = embed

    
    def getEmbed(self):
        return self.embed