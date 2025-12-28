import asyncio, discord
from gamer_pippins.config import ConfigManager
from gamer_pippins.logger import MyLogger
from gamer_pippins.logger.consumer import debugConsumer, infoConsumer, warningConsumer, errorConsumer


async def loadLogger():
    """
    큐, 컨슈머 초기화
    """
    debugQueue, infoQueue, warningQueue, errorQueue = MyLogger.handler.getQueues()
    tasks = [
        asyncio.create_task(debugConsumer(debugQueue)),
        asyncio.create_task(infoConsumer(infoQueue)),
        asyncio.create_task(warningConsumer(warningQueue)),
        asyncio.create_task(errorConsumer(errorQueue))
    ]


async def sendOnlineLog():
    """
    인포 로그와 동일한 형식의 임베드 메시지를 전송
    """
    icon = "https://cdn.discordapp.com/emojis/1431071558348312676.png"
    embed = discord.Embed(title="INFO", description="게이머 피핀스 온라인!", color=0x6CD0D0)
    embed.set_author(name="LOG", icon_url=icon)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1419672385937739817/1434065315716796457/PippinsCheer.gif?ex=690b9626&is=690a44a6&hm=37317b52f88b6af9ac1e4787a0c094108e1bad35a963177beef78211790b955e&")
    await ConfigManager.systemChannel.send(embed=embed)