import discord, logging, asyncio, traceback, sys


async def debugConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        icon = "https://cdn.discordapp.com/emojis/1431071556590633010.png"

        embed = discord.Embed(title="DEBUG", description=msg)
        embed.set_author(name="LOG", icon_url=icon)

        await channel.send(embed=embed)


async def infoConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        icon = "https://cdn.discordapp.com/emojis/1431071558348312676.png"
        embed = discord.Embed(title="INFO", description=msg)
        embed.set_author(name="LOG", icon_url=icon)

        await channel.send(embed=embed)


async def warningConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        icon = "https://cdn.discordapp.com/emojis/1431071554833350778.png"
        embed = discord.Embed(title="WARNING", description=msg)
        embed.set_author(name="LOG", icon_url=icon)

        await channel.send(embed=embed)


async def errorConsumer(queue: asyncio.Queue):
    while True:
        e, tb, channel = await queue.get()
        icon = "https://cdn.discordapp.com/emojis/1431071559942148126.png"
        embed = discord.Embed(title="ERROR", description=f"{e}")
        embed.set_author(name="LOG", icon_url=icon)
        embed.add_field(name="Traceback", value=f"```{tb}```")

        await channel.send(embed=embed)
  

class MultiHandler(logging.Handler):
    def __init__(self, channel: discord.TextChannel):
        super().__init__()
        self.channel = channel
        self.queues = myQueues()
        self.debugQueue, self.infoQueue, self.warningQueue, self.errorQueue = self.queues.getQueues()


    def getQueues(self):
        return self.queues.getQueues()


    def emit(self, record):
        log_entry = self.format(record)

        if record.levelno == logging.DEBUG:
            self.debugQueue.put_nowait((log_entry, self.channel))
        elif record.levelno == logging.INFO:
            self.infoQueue.put_nowait((log_entry, self.channel))
        elif record.levelno == logging.WARNING:
            self.warningQueue.put_nowait((log_entry, self.channel))
        elif record.levelno == logging.ERROR:
            if record.exc_info and record.exc_info[0]:
                e = record.exc_info[0].__name__ + ": " + str(record.exc_info[1])
                tb = str(record.exc_info[2])
                self.errorQueue.put_nowait((e, tb, self.channel))
            else:
                self.errorQueue.put_nowait(("Not an Error", "(Empty Traceback)", self.channel))


class MyLogger():
    def __init__(self, channel):
        self.logger = logging.getLogger("PippinsLogger")
        self.logger.setLevel(logging.DEBUG)
        self.handler = MultiHandler(channel)
        self.handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(self.handler)


    # def logError(self):
    #     def decorator(func):
    #         async def wrapper(*args, **kwargs):
    #             try: return func(*args, **kwargs)
    #             except Exception as e:
    #                 self.logger.error(e)
    #             return wrapper
    #         return decorator
        

    # def logErrorAsync(self):
    #     def decorator(func):
    #         async def wrapper(*args, **kwargs):
    #             try: return await func(*args, **kwargs)
    #             except Exception as e:
    #                 self.logger.error(e)
    #             return wrapper
    #         return decorator
        

    def getHandler(self):
        return self.handler
    
    def getLogger(self):
        return self.logger
    
    
class myQueues():
    def __init__(self):
        self.debugQueue = asyncio.Queue()
        self.infoQueue = asyncio.Queue()
        self.warningQueue = asyncio.Queue()
        self.errorQueue = asyncio.Queue()
    
    def getQueues(self):
        return self.debugQueue, self.infoQueue, self.warningQueue, self.errorQueue