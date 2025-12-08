import logging
from multihandler import MultiHandler


class MyLogger():
    def __init__(self, channel):
        self.logger = logging.getLogger("PippinsLogger")
        self.logger.setLevel(logging.WARNING)
        self.handler = MultiHandler(channel)
        self.handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(self.handler)


    def getHandler(self):
        return self.handler
    
    
    def getLogger(self):
        return self.logger