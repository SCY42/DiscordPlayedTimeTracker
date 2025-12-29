import discord, asyncio, json


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

        await channel.send(content="<@513676568745213953>", embed=embed)