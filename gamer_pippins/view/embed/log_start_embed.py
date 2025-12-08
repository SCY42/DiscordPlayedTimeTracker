import discord, datetime, requests
from zoneinfo import ZoneInfo
from gamer_pippins.bot.bot import GAMER_PIPPINS


# TODO 뜯어온 메서드 알맞게 수정
class LogStartEmbed:
    def startPlaying(self, timestamp: datetime.datetime):
        embed = discord.Embed(description=f"<t:{int(timestamp.timestamp())}:R>에 플레이 시작",
                              color=discord.Color.brand_green(),
                              timestamp=timestamp)
        embed.set_author(name=self.game.name,
                         icon_url=self.getThumbURL())    
        embed.set_footer(text="LOG")
        return embed