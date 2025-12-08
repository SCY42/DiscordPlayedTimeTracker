import asyncio


class MyQueues():
    def __init__(self):
        self.debugQueue = asyncio.Queue()
        self.infoQueue = asyncio.Queue()
        self.warningQueue = asyncio.Queue()
        self.errorQueue = asyncio.Queue()
    
    def getQueues(self):
        return self.debugQueue, self.infoQueue, self.warningQueue, self.errorQueue