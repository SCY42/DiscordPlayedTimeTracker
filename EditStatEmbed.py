import discord
from Pippins import GAMER_PIPPINS
from StatEmbed import StatEmbed


async def deleteEntry(games: list[str]) -> bool:
    message = None
    embed = None
    result = False

    async for msg in GAMER_PIPPINS.statChannel.history(limit=1):
        message = msg
        embed = msg.embeds[0]

    if not message or not embed: return result

    embedDict = embed.to_dict()
    fields = embedDict.get("fields")
    
    if not fields: return result

    for field in fields:
        if field["name"] in games:
            fields.remove(field)
            result = True

    totalSec = sum([StatEmbed._stringToSeconds(field["value"]) for field in fields])
    embedDict["title"] = f"플레이 시간 통계 | {StatEmbed._SecondsToString(totalSec)}"

    embed = discord.Embed.from_dict(embedDict)
    await message.edit(embed=embed)
    return result