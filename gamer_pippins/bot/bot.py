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

        print("길드 로드 중...")
        self.loadGuilds()
        
        print("로거 로드 중...")
        import gamer_pippins.bot.event.on_ready as onReady
        await onReady.loadLogger()

        print("코그 장착 중...")
        from gamer_pippins.bot.event import MessageListener, PresenceListener
        from gamer_pippins.command import BlacklistManagementCog

        await GAMER_PIPPINS.add_cog(MessageListener(GAMER_PIPPINS), override=True)
        await GAMER_PIPPINS.add_cog(PresenceListener(GAMER_PIPPINS), override=True)
        await GAMER_PIPPINS.add_cog(BlacklistManagementCog(GAMER_PIPPINS), override=True)

        from gamer_pippins.bot.event.on_error import onError
        @self.event
        async def on_error(event, *args, **kwargs):
            await onError()
        
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