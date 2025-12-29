import discord
from gamer_pippins.logger import MyLogger
from gamer_pippins.utils import getChannelFromID, secondsToString, stringToSeconds
from gamer_pippins.config import ConfigManager


async def deleteEntry(user: discord.Member | discord.User, games: list[str]) -> bool:
    message = None
    embed = None
    result = False
    statChannel: discord.TextChannel = getChannelFromID(user.id, "stat")    # type: ignore

    async for msg in statChannel.history(limit=1):
        message = msg
        embed = msg.embeds[0]

    if not message:
        MyLogger.logger.info("통계 채널에 메시지 없음.")
        return result   # False
    
    if not embed:
        MyLogger.logger.info("통계 채널 최신 메시지에 임베드 없음.")
        return result   # False

    embedDict = embed.to_dict()
    fields = embedDict.get("fields")
    
    if not fields:
        MyLogger.logger.info("최신 통계에 항목 없음.")
        return result   # False

    for field in fields:
        if field["name"] in games:
            fields.remove(field)
            result = True
            MyLogger.logger.info(f"최신 통계에서 `{field['name']}` 발견 및 삭제.")
            break
    else:
        MyLogger.logger.info("최신 통계에서 삭제할 게임을 찾지 못함.")
        return result   # False

    totalSec = sum([stringToSeconds(field["value"]) for field in fields])
    embedDict["title"] = f"플레이 시간 통계 | {secondsToString(totalSec)}"

    embed = discord.Embed.from_dict(embedDict)
    await message.edit(embed=embed)
    MyLogger.logger.info(f"통계 임베드 수정됨. ({message.jump_url})")
    return result