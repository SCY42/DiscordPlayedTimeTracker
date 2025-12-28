from gamer_pippins.bot.bot import GAMER_PIPPINS


GAMER_PIPPINS.runBot()


import asyncio
from gamer_pippins.bot.event import ErrorListener, MessageListener, PresenceListener
from gamer_pippins.command import BlacklistManagementCog

asyncio.run(GAMER_PIPPINS.add_cog(ErrorListener(GAMER_PIPPINS)))
asyncio.run(GAMER_PIPPINS.add_cog(MessageListener(GAMER_PIPPINS)))
asyncio.run(GAMER_PIPPINS.add_cog(PresenceListener(GAMER_PIPPINS)))

asyncio.run(GAMER_PIPPINS.add_cog(BlacklistManagementCog(GAMER_PIPPINS)))