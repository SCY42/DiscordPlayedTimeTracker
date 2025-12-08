import json
from datetime import datetime


class JsonData:
    def __init__(self):
        self.BLACKLIST: dict[str, list[dict[str, str]]] = {}
        self.NOW_PLAYING: dict[str, list[tuple[str, datetime]]] = {}
        self.EMOJI: dict[str, str] = {}
        self.CUSTOM_ICON: dict[str, str] = {}
        self.USERID_CHANNEL: dict[str, dict[str, int]] = {}

        self.loadBlacklist()
        self.loadNowPlaying()
        self.loadUserIDChannel()
        self.loadCustomGameIcons()
        self.loadEmoji()

    
    def loadBlacklist(self):
        with open("gamer_pippins/config/blacklist.json", 'r', encoding="utf8") as f:
            self.BLACKLIST = json.load(f)


    def loadNowPlaying(self):
        # TODO datetime 형태로 변환하기
        # TODO 로드 시점의 플레이 정보와의 충돌 처리하기
        with open("gamer_pippins/config/now_playing.json", 'r', encoding="utf8") as f:
            self.NOW_PLAYING = json.load(f)

    
    def loadEmoji(self):
        with open("gamer_pippins/config/emoji.json", 'r', encoding="utf8") as f:
            self.EMOJI = json.load(f)


    def loadCustomGameIcons(self):
        with open("gamer_pippins/config/custom_icon.json", 'r', encoding="utf8") as f:
            self.CUSTOM_ICON = json.load(f)


    def loadUserIDChannel(self):
        with open("gamer_pippins/config/userid_channel.json", 'r', encoding="utf8") as f:
            self.USERID_CHANNEL = json.load(f)