import json
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import discord


class ConfigManager:
    def __init__(self):
        with open("blacklist.json", 'r', encoding="UTF-8") as f:
            ConfigManager.blacklist: dict = json.load(f)

        with open("custom_icon.json", 'r', encoding="UTF-8") as f:
            ConfigManager.customIcon: dict = json.load(f)

        with open("emoji.json", 'r', encoding="UTF-8") as f:
            ConfigManager.emoji: dict = json.load(f)

        with open("now_playing.json", 'r', encoding="UTF-8") as f:
            ConfigManager.nowPlaying: dict = json.load(f)

        with open("userid_channel.json", 'r', encoding="UTF-8") as f:
            ConfigManager.userid2Channel: dict = json.load(f)


    @staticmethod
    def setGuildInfo(gamingGuild, systemChannel):
        ConfigManager.gamingGuild: discord.Guild = gamingGuild
        ConfigManager.systemChannel: discord.TextChannel = systemChannel