from gamer_pippins.logger import MyLogger


def secondsToString(seconds) -> str:
    h, seconds = divmod(seconds, 3600)
    m, s = divmod(seconds, 60)

    if not (h or m or s):
        return "0초"

    parts = [(h, "시간"), (m, "분"), (s, "초")]
    result = " ".join([f"{part[0]}{part[1]}" for part in parts if part[0]])
    MyLogger.logger.debug(f"정수 `{seconds}`가 문자열 `{result}`로 변환됨.")
    return result