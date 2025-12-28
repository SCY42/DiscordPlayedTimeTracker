import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import discord


class ConfigManager:
    @classmethod
    def __init__(cls):
        with open("gamer_pippins/config/blacklist.json", 'r', encoding="UTF-8") as f:
            cls.blacklist: dict = json.load(f)

        with open("gamer_pippins/config/custom_icon.json", 'r', encoding="UTF-8") as f:
            cls.customIcon: dict = json.load(f)

        with open("gamer_pippins/config/emoji.json", 'r', encoding="UTF-8") as f:
            cls.emoji: dict = json.load(f)

        with open("gamer_pippins/config/now_playing.json", 'r', encoding="UTF-8") as f:
            cls.nowPlaying: dict = json.load(f)

        with open("gamer_pippins/config/userid_channel.json", 'r', encoding="UTF-8") as f:
            cls.userid2Channel: dict = json.load(f)

        with open("gamer_pippins/config/weekday_icons.txt", 'r', encoding="UTF-8") as f:
            cls.weekdayIcons: list[str] = f.readlines()


    @staticmethod
    def setGuildInfo(gamingGuild, systemChannel):
        ConfigManager.gamingGuild: "discord.Guild" = gamingGuild
        ConfigManager.systemChannel: "discord.TextChannel" = systemChannel


# ConfigManager()