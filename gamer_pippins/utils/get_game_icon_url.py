def getGameIconUrl(self):
    if self.game.name in GAMER_PIPPINS.CUSTOM_GAME_ICONS.keys():
        return GAMER_PIPPINS.CUSTOM_GAME_ICONS[self.game.name]

    try:
        APP_ID = self.game.application_id   # type: ignore
        GAMER_PIPPINS.logger.info(f"`{self.game.name}`의 앱 ID 취득 성공.")
    except:
        GAMER_PIPPINS.logger.warning(f"`{self.game.name}`의 앱 ID 취득 실패.")
        return None
    
    try:
        url = f"https://discord.com/api/v10/applications/{APP_ID}/rpc"
        response = requests.get(url)
        GAMER_PIPPINS.logger.info(f"`{self.game.name}`의 앱 아이콘 취득 성공.")
        return f"https://cdn.discordapp.com/app-icons/{APP_ID}/{response.json()['icon']}.png"
    except:
        GAMER_PIPPINS.logger.warning(f"`{self.game.name}`의 앱 아이콘 취득 실패.")
        return None