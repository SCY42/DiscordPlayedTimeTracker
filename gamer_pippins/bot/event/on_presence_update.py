import datetime
from zoneinfo import ZoneInfo


@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
    if before.guild != GAMER_PIPPINS.GAMING_LOG_GUILD:
        return
    
    timestamp = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))
    
    logChannel = GAMER_PIPPINS.getChannelFromID(before.id, "log")
    if not logChannel: return

    statChannel = GAMER_PIPPINS.getChannelFromID(before.id, "stat")

    gamesBefore = [game for game in before.activities if game.type == discord.ActivityType.playing \
                   and game.name not in [_game["name"] for _game in GAMER_PIPPINS.BLACKLIST[str(before.id)]]]
    gamesAfter = [game for game in after.activities if game.type == discord.ActivityType.playing \
                  and game.name not in [_game["name"] for _game in GAMER_PIPPINS.BLACKLIST[str(before.id)]]]

    stoppedPlaying = [game for game in gamesBefore if game.name not in [_game.name for _game in gamesAfter]]
    startedPlaying = [game for game in gamesAfter if game.name not in [_game.name for _game in gamesBefore]]

    if not (stoppedPlaying or startedPlaying):
        return

    logText = f"===== `{before.display_name}`의 활동 상태 업데이트됨 =====\n\n" \
    + f"gamesBefore: `{gamesBefore}`\n" \
    + f"gamesAfter: `{gamesAfter}`\n" \
    + f"stoppedPlaying: `{stoppedPlaying}`\n" \
    + f"startedPlaying: `{startedPlaying}`"
    GAMER_PIPPINS.logger.info(logText)
    
    if stoppedPlaying:
        for game in stoppedPlaying:
            timestamp, seconds = delFromNP(before, game)

            await logChannel.send(embed=LogEmbed(game).stopPlaying(seconds))   # type: ignore

            msgExists = False
            async for msg in statChannel.history(limit=1):  # type: ignore
                msgExists = True
                embed, isNewMsg = StatEmbed(msg.embeds[0], game, timestamp).getEmbed()
                if isNewMsg:
                    await statChannel.send(embed=embed) # type: ignore
                else:
                    await msg.edit(embed=embed)
            if not msgExists:
                embed, _ = StatEmbed(None, game, timestamp).getEmbed()
                await statChannel.send(embed=embed) # type: ignore

    if startedPlaying:
        for game in startedPlaying:
            addToNP(before, str(game.name))
            await logChannel.send(embed=LogEmbed(game).startPlaying(timestamp))  # type: ignore