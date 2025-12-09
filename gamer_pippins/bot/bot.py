import discord, os
from dotenv import load_dotenv
from datetime import datetime


class Pippins(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())


    def runBot(self):
        print("봇 토큰 전달 중...")
        load_dotenv("../.env")
        super().run(os.environ.get("GAMER_PIPPINS_TOKEN")) # type: ignore

# TODO Cog 장착하기


GAMER_PIPPINS = Pippins()
TREE = discord.app_commands.CommandTree(GAMER_PIPPINS)