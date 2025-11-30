import discord, os, json, Logger, asyncio, traceback, sys, json
from dotenv import load_dotenv
from datetime import datetime


class Pippins(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.BLACKLIST: dict[str, list[dict[str, str]]] = {}
        self.NOW_PLAYING: dict[str, list[tuple[str, datetime]]] = {}
        self.CUSTOM_GAME_ICONS: dict[str, str] = {
            "CLIP STUDIO PAINT": "https://cdn.discordapp.com/emojis/1444620730225524807.png",
        }
        with open("userID_channel.json", 'r', encoding="utf8") as f:
            self.USERID_CHANNEL: dict[str, dict[str, int]] = json.load(f)


    async def on_ready(self):
        print("내부 캐시 준비 중...")
        await self.wait_until_ready()

        self.GAMING_LOG_GUILD: discord.Guild = self.get_guild(1408875641071472783)                          # type: ignore
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

        icon = "https://cdn.discordapp.com/emojis/1431071558348312676.png"
        embed = discord.Embed(title="INFO", description="게이머 피핀스 온라인!", color=0x6CD0D0)
        embed.set_author(name="LOG", icon_url=icon)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1419672385937739817/1434065315716796457/PippinsCheer.gif?ex=690b9626&is=690a44a6&hm=37317b52f88b6af9ac1e4787a0c094108e1bad35a963177beef78211790b955e&")
        await self.SYSTEM_CHANNEL.send(embed=embed)

        print("게이머 피핀스 온라인!")


    async def on_message(self, msg: discord.Message):
        if msg.content == "싱크":
            await msg.channel.send("싱크!")
            try:
                await TREE.sync()
                self.logger.info("트리에 싱크함.")
            except: self.logger.warning("트리에 싱크할 수 없었음.")


    async def on_error(self, event, *args, **kwargs):
        e = sys.exception()

        if e:
            eType = type(e).__name__ + ": " + str(e)
            tb = e.__traceback__
            msg = traceback.format_exc()
            frames = traceback.extract_tb(tb)
            frame = frames[-1]
            nameOfFile = frame.filename.split("\\")[-1]
            cause = f"Function `{frame.name}` in File `{nameOfFile}`"
            data = {"e": eType, "tb": msg, "cause": cause}
        else:
            data = {"e": "Not an Error", "tb": "Empty TraceBack", "cause": "None"}
            
        serialized = json.dumps(data)
        self.logger.error(serialized)


    def runBot(self):
        print("봇 토큰 전달 중...")
        load_dotenv("../.env")
        super().run(os.environ.get("TESTER_PIPPINS_TOKEN")) # type: ignore


    def getChannelFromID(self, id: int, type: str):
        user = self.USERID_CHANNEL.get(str(id))
        if not user:
            return False
        
        channelID = user[type]
        return self.get_channel(channelID)


GAMER_PIPPINS = Pippins()
TREE = discord.app_commands.CommandTree(GAMER_PIPPINS)