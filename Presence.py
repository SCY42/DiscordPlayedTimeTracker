import discord
from LogEmbed import LogEmbed
from StatEmbed import StatEmbed
from Pippins import GAMER_PIPPINS, TREE


@GAMER_PIPPINS.event
async def on_presence_update(before, after):
    if before != GAMER_PIPPINS.USER_42 or before.guild != GAMER_PIPPINS.GAMING_LOG_GUILD:
        return

    gamesBefore = [game for game in before.activities if game.type == discord.ActivityType.playing \
                   and game.name not in [_game["name"] for _game in GAMER_PIPPINS.BLACKLIST]]
    gamesAfter = [game for game in after.activities if game.type == discord.ActivityType.playing \
                  and game.name not in [_game["name"] for _game in GAMER_PIPPINS.BLACKLIST]]

    stoppedPlaying = [game for game in gamesBefore if game.name not in [_game.name for _game in gamesAfter]]
    startedPlaying = [game for game in gamesAfter if game.name not in [_game.name for _game in gamesBefore]]

    if not (stoppedPlaying or startedPlaying):
        return
    
    if stoppedPlaying:
        for game in stoppedPlaying:
            await GAMER_PIPPINS.LOG_CHANNEL.send(embed=LogEmbed(game).stopPlaying())

            async for msg in GAMER_PIPPINS.STATISTICS_CHANNEL.history(limit=1):
                embed, isNewMsg = StatEmbed(msg.embeds[0], game).getEmbed()
                if isNewMsg:
                    await GAMER_PIPPINS.STATISTICS_CHANNEL.send(embed=embed)
                else:
                    await msg.edit(embed=embed)


    if startedPlaying:
        for game in startedPlaying:
            await GAMER_PIPPINS.LOG_CHANNEL.send(embed=LogEmbed(game).startPlaying())