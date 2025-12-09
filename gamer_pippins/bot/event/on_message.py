from discord.ext.commands import Cog
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import discord


# WARN resolve import TREE


class MessageListener(Cog):
    def __init__(self, bot: discord.Client):
        self.bot = bot


@Cog.listener()
async def on_message(self, msg: discord.Message):
    if msg.content == "싱크":
        await msg.channel.send("싱크!")
        try:
            await TREE.sync()
            self.logger.info("트리에 싱크함.")
        except: self.logger.warning("트리에 싱크할 수 없었음.")