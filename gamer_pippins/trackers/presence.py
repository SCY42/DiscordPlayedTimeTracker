import discord, datetime
from embeds.log_embed import LogEmbed
from embeds.stat_embed import StatEmbed
from gamer_pippins.bot.bot import GAMER_PIPPINS
from zoneinfo import ZoneInfo


@GAMER_PIPPINS.event
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


def addToNP(user: discord.Member, game: str):
    timestamp = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))
    userID = str(user.id)
    nowPlaying = GAMER_PIPPINS.NOW_PLAYING.get(userID)  # 유저가 플레이 중인 게임들의 리스트

    if nowPlaying is None or nowPlaying == []:  # 유저가 아무 게임도 플레이 중이 아님
        GAMER_PIPPINS.NOW_PLAYING[userID] = [(game, timestamp)]
    
    else:
        for session in nowPlaying:
            if session[0] == game:
                break   # 업데이트하지 않음
        else:
            nowPlaying.append((game, timestamp))    # 플레이 중에 추가


def delFromNP(user: discord.Member, game) -> tuple[datetime.datetime, int] | tuple[None, int]:
    now = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))
    userID = str(user.id)
    nowPlaying = GAMER_PIPPINS.NOW_PLAYING.get(userID)  # 유저가 플레이 중인 게임들의 리스트

    if nowPlaying is None or nowPlaying == []:  # 유저가 아무 게임도 플레이 중이 아님 (뭔가 잘못됨)
        GAMER_PIPPINS.logger.warning(f"`{game.name}` 세션이 종료되었지만, 플레이 시작 기록이 없음.")
        if game.start is None:
            seconds = 0
        else:
            seconds = int((now - game.start).total_seconds())
        return None, seconds

    else:
        for session in nowPlaying:
            if session[0] == game.name:
                seconds = int((now - session[1]).total_seconds())
                timestamp = session[1]
                nowPlaying.remove(session)  # 플레이 중에서 삭제
                return timestamp, seconds
        else:   
            GAMER_PIPPINS.logger.warning(f"`{game.name}` 세션이 종료되었지만, 플레이 시작 기록이 없음.")
            if game.start is None:
                seconds = 0
            else:
                seconds = int((now - game.start).total_seconds())
            return None, seconds

            


# TODO 게임 꺼지고 5초 후에 기록하기 (아이작 같은거 껐다켰다 좀 그만)