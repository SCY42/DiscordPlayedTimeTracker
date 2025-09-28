import discord, os
from dotenv import load_dotenv


class Pippins(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())
        self.BLACKLIST = []
        # self.tree = discord.app_commands.CommandTree(self)s


    async def on_ready(self):
        self.GAMING_LOG_GUILD: discord.Guild = self.get_guild(1408875641071472783) # type: ignore
        self.USER_42: discord.Member = self.GAMING_LOG_GUILD.get_member(513676568745213953) # type: ignore
        self.STATISTICS_CHANNEL: discord.TextChannel = self.GAMING_LOG_GUILD.get_channel(1408876560077033552) # type: ignore
        self.LOG_CHANNEL: discord.TextChannel = self.GAMING_LOG_GUILD.get_channel(1408876545749160056) # type: ignore

        print("게이밍 피핀스 온라인!")


    async def on_message(self, msg: discord.Message):
        if msg.content == "싱크":
            await msg.channel.send("싱크!")
            await TREE.sync()

        if msg.content == "커맨드":
            commands = [f"`{cmd.name}`" for cmd in TREE._get_all_commands()]
            if commands:
                await msg.channel.send(", ".join(commands))
            else:
                await msg.channel.send("커맨드가 없어!")


    def runBot(self):
        load_dotenv()
        super().run(os.environ.get("BOT_TOKEN")) # type: ignore


GAMER_PIPPINS = Pippins()
TREE = discord.app_commands.CommandTree(GAMER_PIPPINS)