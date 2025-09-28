import discord, datetime, requests
from zoneinfo import ZoneInfo


class LogEmbed:
    def __init__(self, game):
        self.game = game
        self.timestamp = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))

    def getThumbURL(self):
        try:
            APP_ID = self.game.application_id   # type: ignore
        except:
            return None
        
        try:
            url = f"https://discord.com/api/v10/applications/{APP_ID}/rpc"
            response = requests.get(url)
            return f"https://cdn.discordapp.com/app-icons/{APP_ID}/{response.json()['icon']}.png"
        except:
            return None


    def stopPlaying(self):
        elapsed = int((self.timestamp - self.game.created_at).total_seconds())     # type: ignore
        hr, elapsed = divmod(elapsed, 3600)
        min, sec = divmod(elapsed, 60)
        units = [(hr, "시간"), (min, "분"), (sec, "초")]
        formatted = " ".join([f"{num}{unit}" for num, unit in units if num])
        if not formatted: formatted = "??? "

        embed = discord.Embed(description=f"{formatted}동안 플레이함",
                              color=discord.Color.brand_red(),
                              timestamp=self.timestamp)
        embed.set_author(name=self.game.name,
                         icon_url= self.getThumbURL())    
        embed.set_footer(text="LOG")
        return embed

    def startPlaying(self):
        embed = discord.Embed(description=f"<t:{int(self.timestamp.timestamp())}:R>에 플레이 시작",
                              color=discord.Color.brand_green(),
                              timestamp=self.timestamp)
        embed.set_author(name=self.game.name,
                         icon_url=self.getThumbURL())    
        embed.set_footer(text="LOG")
        return embed