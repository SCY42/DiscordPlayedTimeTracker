from gamer_pippins.config import ConfigManager


def getChannelFromID(userID: int, type: str):
    user = ConfigManager.userid2Channel.get(str(userID))
    if not user:
        return False
    
    channelID = user[type]
    return ConfigManager.gamingGuild.get_channel(channelID)