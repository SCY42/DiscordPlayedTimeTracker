import json, datetime
from zoneinfo import ZoneInfo
from gamer_pippins.bot.bot import GAMER_PIPPINS


def load_blacklist():
    success = False
    try:
        with open("blacklist.json", 'r', encoding="utf8") as f:
            GAMER_PIPPINS.BLACKLIST = json.load(f)
        success = True
    finally:
        if success and "logger" in GAMER_PIPPINS.__dict__: GAMER_PIPPINS.logger.info("블랙리스트 성공적으로 로드됨.")


# TODO 모듈 불러올 때 블랙리스트를 로드하는 다른 방법 고안하기
load_blacklist()


def save_blacklist():
    success = False
    try:
        with open("blacklist.json", 'w', encoding="utf8") as f:
            for blacklist in GAMER_PIPPINS.BLACKLIST.values():
                print([date_to_int(entry["date"]) for entry in blacklist])
                blacklist.sort(key=lambda x: date_to_int(x["date"]), reverse=True)
                print(GAMER_PIPPINS.BLACKLIST)
            json.dump(GAMER_PIPPINS.BLACKLIST, f, indent=4)
    finally:
        if success: GAMER_PIPPINS.logger.info("블랙리스트 성공적으로 덤프됨.")


def append_blacklist(userID: str, gamesToAppend: list[str]):
    load_blacklist()
    now = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))
    GAMER_PIPPINS.logger.debug(f"now: `{now}`")

    for gameName in gamesToAppend:
        for entry in GAMER_PIPPINS.BLACKLIST[userID]:
            if entry["name"] == gameName:
                entry["date"] = f"{now.year}년 {now.month}월 {now.day}일"
                GAMER_PIPPINS.logger.info(f"유저 아이디 `{userID}`의 기존 블랙리스트에서 `{gameName}` 검색됨. 날짜 덮어씀.")
                break
        else:
            GAMER_PIPPINS.BLACKLIST[userID].append({"name": gameName, "date": f"{now.year}년 {now.month}월 {now.day}일"})
            GAMER_PIPPINS.logger.info(f"유저 아이디 `{userID}`의 기존 블랙리스트에서 `{gameName}` 검색되지 않음. 새로운 항목 생성.")
    
    save_blacklist()


def remove_blacklist(userID: str, gamesToRemove: list[str]):
    load_blacklist()

    for gameName in gamesToRemove:
        for entry in GAMER_PIPPINS.BLACKLIST[userID]:
            if entry["name"] == gameName:
                GAMER_PIPPINS.BLACKLIST[userID].remove(entry)
                GAMER_PIPPINS.logger.info(f"유저 아이디 `{userID}`의 기존 블랙리스트에서 `{gameName}` 검색됨. 항목 삭제됨.")
        else:
            GAMER_PIPPINS.logger.info(f"유저 아이디 `{userID}`의 기존 블랙리스트에서 `{gameName}` 검색되지 않음. 삭제된 항목 없음.")


    save_blacklist()