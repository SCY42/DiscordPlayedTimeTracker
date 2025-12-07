import discord
from gamer_pippins.bot.bot import GAMER_PIPPINS
from gamer_pippins.embeds.stat_embed import StatEmbed


async def deleteEntry(user: discord.Member | discord.User, games: list[str]) -> bool:
    message = None
    embed = None
    result = False
    statChannel: discord.TextChannel = GAMER_PIPPINS.get_channel(GAMER_PIPPINS.USERID_CHANNEL[str(user.id)]["stat"]) # type: ignore

    async for msg in statChannel.history(limit=1):
        message = msg
        embed = msg.embeds[0]

    if not message:
        GAMER_PIPPINS.logger.info("통계 채널에 메시지 없음.")
        return result   # False
    
    if not embed:
        GAMER_PIPPINS.logger.info("통계 채널 최신 메시지에 임베드 없음.")
        return result   # False

    embedDict = embed.to_dict()
    fields = embedDict.get("fields")
    
    if not fields:
        GAMER_PIPPINS.logger.info("최신 통계에 항목 없음.")
        return result   # False

    for field in fields:
        if field["name"] in games:
            fields.remove(field)
            result = True
            GAMER_PIPPINS.logger.info(f"최신 통계에서 `{field['name']}` 발견 및 삭제.")
            break
    else:
        GAMER_PIPPINS.logger.info("최신 통계에서 삭제할 게임을 찾지 못함.")
        return result   # False

    totalSec = sum([StatEmbed._stringToSeconds(field["value"]) for field in fields])
    embedDict["title"] = f"플레이 시간 통계 | {StatEmbed._SecondsToString(totalSec)}"

    embed = discord.Embed.from_dict(embedDict)
    await message.edit(embed=embed)
    GAMER_PIPPINS.logger.info(f"통계 임베드 수정됨. ({message.jump_url})")
    return result