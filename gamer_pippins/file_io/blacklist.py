import json, datetime
from zoneinfo import ZoneInfo
from gamer_pippins.utils import dateToInt
from gamer_pippins.config import ConfigManager
from gamer_pippins.logger import MyLogger


def load_blacklist():
    success = False
    try:
        with open("gamer_pippins/config/blacklist.json", 'r', encoding="utf8") as f:
            ConfigManager.blacklist = json.load(f)
        success = True
    finally:
        if success: MyLogger.logger.info("블랙리스트 성공적으로 로드됨.")


load_blacklist()


def save_blacklist():
    success = False
    try:
        with open("gamer_pippins./config/blacklist.json", 'w', encoding="utf8") as f:
            for blacklist in ConfigManager.blacklist.values():
                blacklist.sort(key=lambda x: dateToInt(x["date"]), reverse=True)
            json.dump(ConfigManager.blacklist, f, indent=4)
    finally:
        if success: MyLogger.logger.info("블랙리스트 성공적으로 덤프됨.")


def append_blacklist(userID: str, gamesToAppend: list[str]):
    load_blacklist()
    now = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))
    MyLogger.logger.debug(f"now: `{now}`")

    for gameName in gamesToAppend:
        for entry in ConfigManager.blacklist[userID]:
            if entry["name"] == gameName:
                entry["date"] = f"{now.year}년 {now.month}월 {now.day}일"
                MyLogger.logger.info(f"유저 아이디 `{userID}`의 기존 블랙리스트에서 `{gameName}` 검색됨. 날짜 덮어씀.")
                break
        else:
            ConfigManager.blacklist[userID].append({"name": gameName, "date": f"{now.year}년 {now.month}월 {now.day}일"})
            MyLogger.logger.info(f"유저 아이디 `{userID}`의 기존 블랙리스트에서 `{gameName}` 검색되지 않음. 새로운 항목 생성.")
    
    save_blacklist()


def remove_blacklist(userID: str, gamesToRemove: list[str]):
    load_blacklist()

    for gameName in gamesToRemove:
        for entry in ConfigManager.blacklist[userID]:
            if entry["name"] == gameName:
                ConfigManager.blacklist[userID].remove(entry)
                MyLogger.logger.info(f"유저 아이디 `{userID}`의 기존 블랙리스트에서 `{gameName}` 검색됨. 항목 삭제됨.")
        else:
            MyLogger.logger.info(f"유저 아이디 `{userID}`의 기존 블랙리스트에서 `{gameName}` 검색되지 않음. 삭제된 항목 없음.")

    save_blacklist()