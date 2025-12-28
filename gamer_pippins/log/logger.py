import logging
from multihandler import MultiHandler


class MyLogger():
    def __init__(self, channel):
        MyLogger.logger = logging.getLogger("PippinsLogger")
        MyLogger.logger.setLevel(logging.WARNING)   # NOTE 필요에 따라 변경할 것
        MyLogger.handler = MultiHandler(channel)
        MyLogger.handler.setFormatter(logging.Formatter("%(message)s"))
        MyLogger.logger.addHandler(self.handler)