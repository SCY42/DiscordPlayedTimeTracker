import discord, datetime, re
from zoneinfo import ZoneInfo
from Pippins import GAMER_PIPPINS


ICON_MONDAY = "https://cdn.discordapp.com/emojis/1409429972556316672.png"
ICON_TUESDAY = "https://cdn.discordapp.com/emojis/1409430005691322418.png"
ICON_WEDNESDAY = "https://cdn.discordapp.com/emojis/1409430012087631892.png"
ICON_THURSDAY = "https://cdn.discordapp.com/emojis/1409430023550668844.png"
ICON_FRIDAY = "https://cdn.discordapp.com/emojis/1409430031440150588.png"
ICON_SATURDAY = "https://cdn.discordapp.com/emojis/1409430039287824394.png"
ICON_SUNDAY = "https://cdn.discordapp.com/emojis/1409430046766137454.png"

WEEKDAY_ICONS = (ICON_MONDAY, ICON_TUESDAY, ICON_WEDNESDAY, ICON_THURSDAY, ICON_FRIDAY, ICON_SATURDAY, ICON_SUNDAY)

class StatEmbed:
    def __init__(self, existingEmbed, updatedGame, timestamp) -> None:
        if existingEmbed is not None:
            self.existingEmbedDict: dict = existingEmbed.to_dict()
        else:
            self.existingEmbedDict = None   # type: ignore
        self.isNew = False

        self.updatedGame = updatedGame
        self.now = datetime.datetime.now(tz=ZoneInfo("Asia/Seoul"))

        if timestamp is not None:               # now playing 정보가 있음
            self.startTime = timestamp
        elif updatedGame.start is not None:     # now playing 정보는 없고 게임 시작 시간 정보는 있음
            self.startTime = updatedGame.start
        else:                                   # now playing 정보도 게임 시작 시간 정보도 없음
            self.startTime = self.now           # 0초 처리

        self.playtimeSeconds = int((self.now - self.startTime).total_seconds())

        self.createNewEmbedDict()
        self.setFields(self._isTodaysStat())  # type: ignore
        self.setColor()
        self.setTitle()


    def createNewEmbedDict(self) -> None:
        self.newEmbedDict = dict()
        self.newEmbedDict["footer"] = { "text": "마지막 업데이트" }
        self.newEmbedDict["author"] = { "name": f"{self.startTime.year}년 {self.startTime.month}월 {self.startTime.day}일",
                                        "icon_url": WEEKDAY_ICONS[self.startTime.weekday()] }
        self.newEmbedDict["fields"] = []
        self.newEmbedDict["flags"] = 0
        self.newEmbedDict["color"] = None
        self.newEmbedDict["timestamp"] = str(self.now)
        self.newEmbedDict["type"] = "rich"
        self.newEmbedDict["title"] = ""


    def _isTodaysStat(self) -> bool:
        if self.existingEmbedDict is None:
            return False
        
        GAMER_PIPPINS.logger.debug(f"기존 통계 임베드 날짜: `{self.existingEmbedDict['author']['name']}`\n게임 시작 날짜: `{self.startTime.year}년 {self.startTime.month}월 {self.startTime.day}일`")
        return self.existingEmbedDict["author"]["name"] == f"{self.startTime.year}년 {self.startTime.month}월 {self.startTime.day}일"


    @staticmethod
    def _stringToSeconds(string) -> int:
        hours, minutes, seconds = 0, 0, 0
        h = re.search(r'(\d+)시간', string)
        m = re.search(r'(\d+)분', string)
        s = re.search(r'(\d+)초', string)

        if h: hours = int(h.group(1))
        if m: minutes = int(m.group(1))
        if s: seconds = int(s.group(1))

        result = hours * 3600 + minutes * 60 + seconds
        GAMER_PIPPINS.logger.debug(f"문자열 `{string}`가 정수 `{result}`로 변환됨.")
        return result


    @staticmethod
    def _SecondsToString(seconds) -> str:
        h, seconds = divmod(seconds, 3600)
        m, s = divmod(seconds, 60)

        if not (h or m or s):
            return "0초"

        parts = [(h, "시간"), (m, "분"), (s, "초")]
        result = " ".join([f"{part[0]}{part[1]}" for part in parts if part[0]])
        GAMER_PIPPINS.logger.debug(f"정수 `{seconds}`가 문자열 `{result}`로 변환됨.")
        return result


    def setFields(self, isToday) -> None:
        if not isToday:
            self.newEmbedDict["fields"].append({
                "inline": False,
                "name": self.updatedGame.name,
                "value": self._SecondsToString(self.playtimeSeconds)
            })
            self.isNew = True
        
        else:
            fields = self.existingEmbedDict.get("fields")
            if fields is None:
                fields = [{
                    "inline": False,
                    "name": self.updatedGame.name,
                    "value": self._SecondsToString(self.playtimeSeconds)
                }]
            else:
                for field in fields:
                    if field["name"] == self.updatedGame.name:
                        field["value"] = self._SecondsToString(self._stringToSeconds(field["value"]) + self.playtimeSeconds)
                        break
                else:
                    fields.append({
                        "inline": False,
                        "name": self.updatedGame.name,
                        "value": self._SecondsToString(self.playtimeSeconds)
                    })
                
            fields.sort(key=lambda x: self._stringToSeconds(x["value"]), reverse=True)
            self.newEmbedDict["fields"] = fields


    def _getTotalSeconds(self) -> int:
        return sum([self._stringToSeconds(field["value"]) for field in self.newEmbedDict["fields"]])


    def setColor(self) -> None:
        HUE_RED, HUE_GREEN = 0, 138
        MAX_SEC = 5 * 60 * 60
        sec = self._getTotalSeconds()

        # 최대 플레이 시간(5시간)에 대한 총 플레이 시간의 비율 (0~1)
        # 비율이 1일 때 hue 0, 0일 때 138

        hue = HUE_GREEN + int((HUE_RED - HUE_GREEN) * min(sec / MAX_SEC, 1))
        color = discord.Color.from_hsv(hue / 360, 0.72, 0.93).value
        self.newEmbedDict["color"] = color


    def setTitle(self) -> None:
        sec = self._getTotalSeconds()
        self.newEmbedDict["title"] = f"플레이 시간 통계 | {self._SecondsToString(sec)}"


    def getEmbed(self) -> tuple[discord.Embed, bool]:
        return discord.Embed.from_dict(self.newEmbedDict), self.isNew
