import sys, traceback, json
from discord.ext.commands import Cog
from gamer_pippins.logger import MyLogger


class ErrorListener(Cog):
    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        e = sys.exception()

        if e:
            eType = type(e).__name__ + ": " + str(e)
            tb = e.__traceback__
            msg = traceback.format_exc()
            frames = traceback.extract_tb(tb)
            frame = frames[-1]
            nameOfFile = frame.filename.split("\\")[-1]
            cause = f"Function `{frame.name}` in File `{nameOfFile}`"
            data = {"e": eType, "tb": msg, "cause": cause}
        else:
            data = {"e": "Not an Error", "tb": "Empty TraceBack", "cause": "None"}
            
        serialized = json.dumps(data)
        MyLogger.logger.error(serialized)