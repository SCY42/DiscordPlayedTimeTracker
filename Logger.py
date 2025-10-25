import discord, logging, asyncio, json


async def debugConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        icon = "https://cdn.discordapp.com/emojis/1431071556590633010.png"

        embed = discord.Embed(title="DEBUG", description=msg, color=0xD387AB)
        embed.set_author(name="LOG", icon_url=icon)

        await channel.send(embed=embed)


async def infoConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        icon = "https://cdn.discordapp.com/emojis/1431071558348312676.png"
        embed = discord.Embed(title="INFO", description=msg, color=0x6CD0D0)
        embed.set_author(name="LOG", icon_url=icon)

        await channel.send(embed=embed)


async def warningConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        icon = "https://cdn.discordapp.com/emojis/1431071554833350778.png"
        embed = discord.Embed(title="WARNING", description=msg, color=0xFFBE00)
        embed.set_author(name="LOG", icon_url=icon)

        await channel.send(embed=embed)


async def errorConsumer(queue: asyncio.Queue):
    while True:
        msg, channel = await queue.get()
        d = json.loads(msg)
        e, tb, cause = d["e"], d["tb"], d["cause"]
        
        icon = "https://cdn.discordapp.com/emojis/1431071559942148126.png"
        embed = discord.Embed(title="ERROR", description=f"`{e}`", color=0xE34234)
        embed.set_author(name="LOG", icon_url=icon)
        embed.add_field(name="Cause", value=cause, inline=False)
        embed.add_field(name="Traceback", value=f"```{tb}```", inline=False)

        await channel.send("<@513676568745213953>")
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
            self.errorQueue.put_nowait((log_entry, self.channel))


class MyLogger():
    def __init__(self, channel):
        self.logger = logging.getLogger("PippinsLogger")
        self.logger.setLevel(logging.DEBUG)
        self.handler = MultiHandler(channel)
        self.handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(self.handler)


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