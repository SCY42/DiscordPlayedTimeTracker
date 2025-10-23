import discord, os, json, Logger, asyncio
from dotenv import load_dotenv


class Pippins(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.BLACKLIST: dict[str, list[dict[str, str]]] = {}
        with open("userID_channel.json", 'r', encoding="utf8") as f:
            self.USERID_CHANNEL: dict[str, dict[str, int]] = json.load(f)


    async def on_ready(self):
        print("내부 캐시 준비 중...")
        await self.wait_until_ready()

        self.GAMING_LOG_GUILD: discord.Guild = self.get_guild(1408875641071472783)                          # type: ignore
        self.USER_42: discord.Member = self.GAMING_LOG_GUILD.get_member(513676568745213953)                 # type: ignore
        self.STAT_CHANNEL: discord.TextChannel = self.GAMING_LOG_GUILD.get_channel(1408876560077033552)     # type: ignore
        self.LOG_CHANNEL: discord.TextChannel = self.GAMING_LOG_GUILD.get_channel(1408876545749160056)      # type: ignore
        self.SYSTEM_CHANNEL: discord.TextChannel = self.GAMING_LOG_GUILD.get_channel(1427623274589847592)   # type: ignore

        self.myLogger = Logger.MyLogger(self.SYSTEM_CHANNEL)
        self.logger = self.myLogger.getLogger()
        debugQueue, infoQueue, warningQueue, errorQueue = self.myLogger.getHandler().getQueues()

        tasks = [
            asyncio.create_task(Logger.debugConsumer(debugQueue)),
            asyncio.create_task(Logger.infoConsumer(infoQueue)),
            asyncio.create_task(Logger.warningConsumer(warningQueue)),
            asyncio.create_task(Logger.errorConsumer(errorQueue)),
        ]

        print("게이머 피핀스 온라인!")


    async def on_message(self, msg: discord.Message):
        if msg.content == "싱크":
            await msg.channel.send("싱크!")
            await TREE.sync()

        # elif msg.content == "커맨드":
        #     commands = [f"`{cmd.name}`" for cmd in TREE._get_all_commands()]
        #     if commands:
        #         await msg.channel.send(", ".join(commands))
        #     else:
        #         await msg.channel.send("커맨드가 없어!")


    def runBot(self):
        print("봇 토큰 전달 중...")
        load_dotenv("../.env")
        super().run(os.environ.get("GAMER_PIPPINS_TOKEN")) # type: ignore


    def getChannelFromID(self, id: int, type: str):
        user = self.USERID_CHANNEL.get(str(id))
        if not user:
            return False
        
        channelID = user[type]
        return self.get_channel(channelID)


GAMER_PIPPINS = Pippins()
TREE = discord.app_commands.CommandTree(GAMER_PIPPINS)