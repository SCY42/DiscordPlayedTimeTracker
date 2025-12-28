import json
from gamer_pippins.config import ConfigManager
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gamer_pippins.bot import Pippins
    import discord


def loadGuilds(bot: "Pippins"):
    """
    봇이 이용할 길드와 채널을 로드해 ConfigManager에 넘김
    """
    with open("gamer_pippins/config/server_id.json", 'r', encoding="UTF-8") as f:
        d: dict[str, int] = json.load(f)
        gamingGuild: "discord.Guild" = bot.get_guild(int(d["guildID"]))                          # type: ignore
        systemChannel: "discord.TextChannel" = gamingGuild.get_channel(int(d["systemChannelID"])) # type: ignore
    ConfigManager.setGuildInfo(gamingGuild, systemChannel)