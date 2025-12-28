import logging, discord
from .queues import MyQueues


class MultiHandler(logging.Handler):
    def __init__(self, channel: discord.TextChannel):
        super().__init__()
        self.channel = channel
        self.queues = MyQueues()
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