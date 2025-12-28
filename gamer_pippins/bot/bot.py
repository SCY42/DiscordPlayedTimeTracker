import discord, os, asyncio
import discord.ext.commands as discomm
from dotenv import load_dotenv
from log.logger import MyLogger
from log.consumer import *
from event.on_error import ErrorListener
from event.on_message import MessageListener
from event.on_presence_update import PresenceListener
from command.blacklist_management import BlacklistManagementCog
from config.config_manager import ConfigManager


class Pippins(discomm.Bot):
    def __init__(self):
        super().__init__(command_prefix="42/", intents = discord.Intents.all())


    def runBot(self):
        print("봇 토큰 전달 중...")
        load_dotenv("../.env")
        super().run(os.environ.get("GAMER_PIPPINS_TOKEN")) # type: ignore


    async def on_ready(self):
        print("내부 캐시 준비 중...")
        await self.wait_until_ready()

        self.loadGuilds()
        self.loadLoggers()
        await self.loadCogs()
        await self.sendOnlineLog()

        print("게이머 피핀스 온라인!")


    def loadGuilds(self):
        """
        봇이 이용할 길드와 채널을 로드해 ConfigManager에 넘김
        """
        with open("server_id.json", 'r', encoding="UTF-8") as f:
            d: dict[str, int] = json.load(f)
        gamingGuild: discord.Guild = self.get_guild(int(d.get("guildID")))                          # type: ignore
        systemChannel: discord.TextChannel = gamingGuild.get_channel(int(d.get("systemChannelID"))) # type: ignore
        ConfigManager.setGuildInfo(gamingGuild, systemChannel)


    def loadLoggers(self):
        """
        봇의 로거를 로드하고, 디버그·인포·워닝·에러 컨슈머를 태스크로 등록
        """
        self.myLogger = MyLogger(ConfigManager.systemChannel)
        self.logger = MyLogger.logger
        debugQueue, infoQueue, warningQueue, errorQueue = MyLogger.handler.getQueues()

        tasks = (
            asyncio.create_task(debugConsumer(debugQueue)),
            asyncio.create_task(infoConsumer(infoQueue)),
            asyncio.create_task(warningConsumer(warningQueue)),
            asyncio.create_task(errorConsumer(errorQueue)),
        )

    
    async def loadCogs(self):
        """
        이벤트, 커맨드 코그를 로드
        """
        await self.add_cog(ErrorListener(self))
        await self.add_cog(MessageListener(self))
        await self.add_cog(PresenceListener(self))
        await self.add_cog(BlacklistManagementCog(self))

    
    async def sendOnlineLog(self):
        """
        인포 로그와 동일한 형식의 임베드 메시지를 전송
        """
        icon = "https://cdn.discordapp.com/emojis/1431071558348312676.png"
        embed = discord.Embed(title="INFO", description="게이머 피핀스 온라인!", color=0x6CD0D0)
        embed.set_author(name="LOG", icon_url=icon)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1419672385937739817/1434065315716796457/PippinsCheer.gif?ex=690b9626&is=690a44a6&hm=37317b52f88b6af9ac1e4787a0c094108e1bad35a963177beef78211790b955e&")
        await ConfigManager.systemChannel.send(embed=embed)


GAMER_PIPPINS = Pippins()
TREE = discord.app_commands.CommandTree(GAMER_PIPPINS)