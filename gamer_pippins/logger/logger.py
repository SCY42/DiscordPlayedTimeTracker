import logging
from .multihandler import MultiHandler
from .consumer import *
from gamer_pippins.config import ConfigManager


class MyLogger():
    @classmethod
    def __init__(cls, channel):
        cls.logger = logging.getLogger("PippinsLogger")
        cls.logger.setLevel(logging.WARNING)    # NOTE 필요에 따라 변경할 것
        cls.handler = MultiHandler(channel)
        cls.handler.setFormatter(logging.Formatter("%(message)s"))
        cls.logger.addHandler(cls.handler)

    
MyLogger(ConfigManager.systemChannel)