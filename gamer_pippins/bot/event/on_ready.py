import asyncio
from discord.ext.commands import Cog
from typing import TYPE_CHECKING
from logging.logger import MyLogger
from logging.consumer import *
if TYPE_CHECKING:
    import discord


class ReadyListener(Cog):
    def __init__(self, bot):
        self.bot = bot

            
    @Cog.listener()
    async def on_ready(self):
        print("내부 캐시 준비 중...")
        await self.bot.wait_until_ready()

        self.GAMING_LOG_GUILD: discord.Guild = self.bot.get_guild(1408875641071472783)                          # type: ignore
        self.SYSTEM_CHANNEL: discord.TextChannel = self.bot.GAMING_LOG_GUILD.get_channel(1427623274589847592)   # type: ignore
        self.myLogger = MyLogger(self.SYSTEM_CHANNEL)
        self.logger = MyLogger.logger
        debugQueue, infoQueue, warningQueue, errorQueue = MyLogger.handler.getQueues()

        tasks = [
            asyncio.create_task(debugConsumer(debugQueue)),
            asyncio.create_task(infoConsumer(infoQueue)),
            asyncio.create_task(warningConsumer(warningQueue)),
            asyncio.create_task(errorConsumer(errorQueue)),
        ]

        icon = "https://cdn.discordapp.com/emojis/1431071558348312676.png"
        embed = discord.Embed(title="INFO", description="게이머 피핀스 온라인!", color=0x6CD0D0)
        embed.set_author(name="LOG", icon_url=icon)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1419672385937739817/1434065315716796457/PippinsCheer.gif?ex=690b9626&is=690a44a6&hm=37317b52f88b6af9ac1e4787a0c094108e1bad35a963177beef78211790b955e&")
        await self.SYSTEM_CHANNEL.send(embed=embed)

        print("게이머 피핀스 온라인!")