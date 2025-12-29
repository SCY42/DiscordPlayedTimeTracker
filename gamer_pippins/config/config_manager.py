import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import discord


class ConfigManager:
    with open("gamer_pippins/config/blacklist.json", 'r', encoding="UTF-8") as f:
        blacklist: dict = json.load(f)

    with open("gamer_pippins/config/custom_icon.json", 'r', encoding="UTF-8") as f:
        customIcon: dict = json.load(f)

    with open("gamer_pippins/config/emoji.json", 'r', encoding="UTF-8") as f:
        emoji: dict = json.load(f)

    with open("gamer_pippins/config/now_playing.json", 'r', encoding="UTF-8") as f:
        nowPlaying: dict = json.load(f)

    with open("gamer_pippins/config/userid_channel.json", 'r', encoding="UTF-8") as f:
        userid2Channel: dict[str, dict[str, int]] = json.load(f)

    with open("gamer_pippins/config/weekday_icons.txt", 'r', encoding="UTF-8") as f:
        weekdayIcons: list[str] = f.readlines()


    @staticmethod
    def setGuildInfo(gamingGuild, systemChannel):
        ConfigManager.gamingGuild: "discord.Guild" = gamingGuild
        ConfigManager.systemChannel: "discord.TextChannel" = systemChannel