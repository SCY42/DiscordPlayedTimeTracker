import logging
from multihandler import MultiHandler


class MyLogger():
    def __init__(self, channel):
        MyLogger.logger = logging.getLogger("PippinsLogger")
        MyLogger.logger.setLevel(logging.WARNING)
        MyLogger.handler = MultiHandler(channel)
        MyLogger.handler.setFormatter(logging.Formatter("%(message)s"))
        MyLogger.logger.addHandler(self.handler)