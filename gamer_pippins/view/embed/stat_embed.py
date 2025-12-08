import discord, datetime, re
from zoneinfo import ZoneInfo
from gamer_pippins.bot.bot import GAMER_PIPPINS


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
        self.setFields(self.isTodaysStat())    # type: ignore
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


    def isTodaysStat(self) -> bool:
        if self.existingEmbedDict is None:
            return False
        
        GAMER_PIPPINS.logger.debug(f"기존 통계 임베드 날짜: `{self.existingEmbedDict['author']['name']}`\n게임 시작 날짜: `{self.startTime.year}년 {self.startTime.month}월 {self.startTime.day}일`")
        return self.existingEmbedDict["author"]["name"] == f"{self.startTime.year}년 {self.startTime.month}월 {self.startTime.day}일"


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


    def getTotalSeconds(self) -> int:
        return sum([stringToSeconds(field["value"]) for field in self.newEmbedDict["fields"]])


    def setColor(self) -> None:
        HUE_RED, HUE_GREEN = 0, 138
        MAX_SEC = 5 * 60 * 60
        sec = self.getTotalSeconds()

        # 최대 플레이 시간(5시간)에 대한 총 플레이 시간의 비율 (0~1)
        # 비율이 1일 때 hue 0, 0일 때 138
        # TODO 5시간 초과 시 명도 감소

        hue = HUE_GREEN + int((HUE_RED - HUE_GREEN) * min(sec / MAX_SEC, 1))
        color = discord.Color.from_hsv(hue / 360, 0.72, 0.93).value
        self.newEmbedDict["color"] = color


    def setTitle(self) -> None:
        sec = self.getTotalSeconds()
        self.newEmbedDict["title"] = f"플레이 시간 통계 | {self._SecondsToString(sec)}"


    def getEmbed(self) -> tuple[discord.Embed, bool]:
        return discord.Embed.from_dict(self.newEmbedDict), self.isNew
