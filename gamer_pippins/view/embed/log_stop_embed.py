# TODO 뜯어온 메서드 알맞게 수정
class LogStopEmbed:
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