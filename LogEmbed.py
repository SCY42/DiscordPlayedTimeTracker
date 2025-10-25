import discord, datetime, requests
from zoneinfo import ZoneInfo
from Pippins import GAMER_PIPPINS


class LogEmbed:
    def __init__(self, game: discord.Game):
        self.game = game

    def getThumbURL(self):
        try:
            APP_ID = self.game.application_id   # type: ignore
            GAMER_PIPPINS.logger.info(f"`{self.game.name}`의 앱 ID 취득 성공.")
        except:
            GAMER_PIPPINS.logger.warning(f"`{self.game.name}`의 앱 ID 취득 실패.")
            return None
        
        try:
            url = f"https://discord.com/api/v10/applications/{APP_ID}/rpc"
            response = requests.get(url)
            GAMER_PIPPINS.logger.info(f"`{self.game.name}`의 앱 아이콘 취득 성공.")
            return f"https://cdn.discordapp.com/app-icons/{APP_ID}/{response.json()['icon']}.png"
        except:
            GAMER_PIPPINS.logger.warning(f"`{self.game.name}`의 앱 아이콘 취득 실패.")
            return None


    def stopPlaying(self, seconds):
        hr, seconds = divmod(seconds, 3600)
        min, sec = divmod(seconds, 60)
        units = [(hr, "시간"), (min, "분"), (sec, "초")]
        formatted = " ".join([f"{num}{unit}" for num, unit in units if num])
        if not formatted:
            formatted = "??? "
            GAMER_PIPPINS.logger.warning(f"`{self.game.name}`의 플레이 시간이 0초로 기록됨.")

        embed = discord.Embed(description=f"{formatted}동안 플레이함",
                              color=discord.Color.brand_red(),
                              timestamp=datetime.datetime.now(tz=ZoneInfo("Asia/Seoul")))
        embed.set_author(name=self.game.name,
                         icon_url= self.getThumbURL())    
        embed.set_footer(text="LOG")
        return embed


    def startPlaying(self, timestamp: datetime.datetime):
        embed = discord.Embed(description=f"<t:{int(timestamp.timestamp())}:R>에 플레이 시작",
                              color=discord.Color.brand_green(),
                              timestamp=timestamp)
        embed.set_author(name=self.game.name,
                         icon_url=self.getThumbURL())    
        embed.set_footer(text="LOG")
        return embed