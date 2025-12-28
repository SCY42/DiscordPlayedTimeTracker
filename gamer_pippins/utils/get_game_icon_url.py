import requests
from file_io.json_data import JsonData
from log.logger import MyLogger


def getGameIconUrl(gameName: str) -> str | None:
    if gameName in JsonData.CUSTOM_ICON.keys():
        return JsonData.CUSTOM_ICON[gameName]

    try:
        APP_ID = self.game.application_id   # type: ignore
        MyLogger.logger.info(f"`{gameName}`의 앱 ID 취득 성공.")
    except:
        MyLogger.logger.warning(f"`{gameName}`의 앱 ID 취득 실패.")
        return None
    
    try:
        url = f"https://discord.com/api/v10/applications/{APP_ID}/rpc"
        response = requests.get(url)
        MyLogger.logger.info(f"`{gameName}`의 앱 아이콘 취득 성공.")
        return f"https://cdn.discordapp.com/app-icons/{APP_ID}/{response.json()['icon']}.png"
    except:
        MyLogger.logger.warning(f"`{gameName}`의 앱 아이콘 취득 실패.")
        return None