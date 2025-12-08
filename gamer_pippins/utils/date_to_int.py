p = re.compile(r"(\d{4})년 (\d{1,2})월 (\d{1,2})일")

def date_to_int(date: str) -> int:
    y, m, d = p.findall(date)[0]
    n = int(y) * 10 ** 4 + int(m) * 10 ** 2 + int(d)
    GAMER_PIPPINS.logger.debug(f"날짜 문자열 `{date}`을 정수 `{n}`으로 변환함.")
    return n