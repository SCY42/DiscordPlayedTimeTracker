import json
from datetime import datetime


class JsonData:
    BLACKLIST: dict[str, list[dict[str, str]]] = {}
    NOW_PLAYING: dict[str, list[tuple[str, datetime]]] = {}
    EMOJI: dict[str, str] = {}
    CUSTOM_ICON: dict[str, str] = {}
    USERID_CHANNEL: dict[str, dict[str, int]] = {}

    with open("gamer_pippins/config/blacklist.json", 'r', encoding="utf8") as f:
        BLACKLIST = json.load(f)


    # TODO datetime 형태로 변환하기
    # TODO 로드 시점의 플레이 정보와의 충돌 처리하기
    with open("gamer_pippins/config/now_playing.json", 'r', encoding="utf8") as f:
        NOW_PLAYING = json.load(f)

    
    with open("gamer_pippins/config/emoji.json", 'r', encoding="utf8") as f:
        EMOJI = json.load(f)


    with open("gamer_pippins/config/custom_icon.json", 'r', encoding="utf8") as f:
        CUSTOM_ICON = json.load(f)


    with open("gamer_pippins/config/userid_channel.json", 'r', encoding="utf8") as f:
        USERID_CHANNEL = json.load(f)