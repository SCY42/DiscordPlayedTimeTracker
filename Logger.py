import discord, logging, asyncio


async def debugConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        await channel.send(f"[Debug] {msg}")


async def infoConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        await channel.send(f"[Info] {msg}")


async def warningConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        await channel.send(f"[Warning] {msg}")


async def errorConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        await channel.send(f"[Error] {msg}")
  

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
            self.errorQueue.put_nowait((log_entry, self.channel))


class MyLogger():
    def __init__(self, channel):
        self.logger = logging.getLogger("PippinsLogger")
        self.logger.setLevel(logging.DEBUG)
        self.handler = MultiHandler(channel)
        self.handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(self.handler)


    def logError(self):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                try: return func(*args, **kwargs)
                except Exception as e:
                    self.logger.error(e)
                return wrapper
            return decorator
        

    def logErrorAsync(self):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                try: return await func(*args, **kwargs)
                except Exception as e:
                    self.logger.error(e)
                return wrapper
            return decorator
        

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