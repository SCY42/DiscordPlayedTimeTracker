from discord.ext.commands import Cog
from gamer_pippins.logger import MyLogger
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamer_pippins.bot.bot import Pippins
    import discord


class MessageListener(Cog):
    def __init__(self, bot: "Pippins"):
        self.bot = bot


    @Cog.listener()
    async def on_message(self, msg: "discord.Message"):
        if msg.content == "싱크":
            await msg.channel.send("싱크!")
            try:
                await self.bot.tree.sync()
                MyLogger.logger.info("트리에 싱크함.")
            except: MyLogger.logger.warning("트리에 싱크할 수 없었음.")