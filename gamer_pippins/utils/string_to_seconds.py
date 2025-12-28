import re
from gamer_pippins.logger import MyLogger


def stringToSeconds(string) -> int:
    hours, minutes, seconds = 0, 0, 0
    h = re.search(r'(\d+)시간', string)
    m = re.search(r'(\d+)분', string)
    s = re.search(r'(\d+)초', string)

    if h: hours = int(h.group(1))
    if m: minutes = int(m.group(1))
    if s: seconds = int(s.group(1))

    result = hours * 3600 + minutes * 60 + seconds
    MyLogger.logger.debug(f"문자열 `{string}`가 정수 `{result}`로 변환됨.")
    return result