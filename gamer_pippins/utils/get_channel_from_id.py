from gamer_pippins.config.config_manager import ConfigManager


def getChannelFromID(id: int, type: str):
    user = ConfigManager.userid2Channel.get(str(id))
    if not user:
        return False
    
    channelID = user[type]
    return ConfigManager.gamingGuild.get_channel(channelID)