import discord, os, json
import discord.ext.commands as discomm
from dotenv import load_dotenv
from gamer_pippins.config import ConfigManager


class Pippins(discomm.Bot):
    def __init__(self):
        super().__init__(command_prefix="42/", intents = discord.Intents.all())


    async def on_ready(self):
        print("내부 캐시 준비 중...")
        await self.wait_until_ready()

        self.loadGuilds()
        import gamer_pippins.bot.event.on_ready as onReady
        await onReady.loadLogger()
        await onReady.sendOnlineLog()

        print("게이머 피핀스 온라인!")


    def loadGuilds(self):
        """
        봇이 이용할 길드와 채널을 로드해 ConfigManager에 넘김
        """
        with open("gamer_pippins/config/server_id.json", 'r', encoding="UTF-8") as f:
            d: dict[str, int] = json.load(f)
            gamingGuild: "discord.Guild" = self.get_guild(int(d["guildID"]))                          # type: ignore
            systemChannel: "discord.TextChannel" = gamingGuild.get_channel(int(d["systemChannelID"])) # type: ignore
        ConfigManager.setGuildInfo(gamingGuild, systemChannel)


    def runBot(self):
        print("봇 토큰 전달 중...")
        load_dotenv("../.env")
        super().run(os.environ.get("TESTER_PIPPINS_TOKEN")) # type: ignore


GAMER_PIPPINS = Pippins()