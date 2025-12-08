import discord, datetime
from embed.log_embed import LogEmbed
from embed.stat_embed import StatEmbed
from gamer_pippins.bot.bot import GAMER_PIPPINS
from zoneinfo import ZoneInfo


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