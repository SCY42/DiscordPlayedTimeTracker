def getChannelFromID(self, id: int, type: str):
    user = self.USERID_CHANNEL.get(str(id))
    if not user:
        return False
    
    channelID = user[type]
    return self.get_channel(channelID)