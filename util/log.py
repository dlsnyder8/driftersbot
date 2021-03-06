# TODO: Load this cog in bot.py
import discord
from discord import channel
from discord.embeds import Embed
from discord.ext import commands
from discord.utils import get
from util import checks
import database as db
import api
import asyncio
import time
import logging
from datetime import datetime, timezone


logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


async def test(self, ctx, desc: str):
    await self.genlog(ctx, title="testing", desc=desc)


async def log(bot, title: str, desc: str):
    channel = bot.get_channel(790666439673643028)
    embed = discord.Embed(
        title=title,
        description=desc,
        timestamp=datetime.now(timezone.utc),
        color=0x00ff00
    )

    await channel.send(embed=embed)


async def flylog2(bot, title: str, desc: str):
    channel = bot.get_channel(770177350758563850)
    embed = discord.Embed(
        title=title,
        description=desc,
        timestamp=datetime.now(timezone.utc),
        color=0x00ff00
    )

    await channel.send(embed=embed)


async def flylog3(bot, embed):
    channel = bot.get_channel(770177350758563850)
    await channel.send(embed=embed)


async def flylog(bot, title: str, desc: str, userid):
    channel = bot.get_channel(770177350758563850)  # Actual log channel
    # channel = bot.get_channel(868565628695494716) #shit-code-only channel
    embed = discord.Embed(
        title=title,
        description=desc,
        timestamp=datetime.now(timezone.utc),
        color=0x008e64
    )
    embed.set_footer(text=f"ID: {userid}")
    await channel.send(embed=embed)

# for logging roles given and removed


async def driftlog(bot, title: str, desc: str, userid=0):
    channel = bot.get_channel(861312536913117186)  # Actual log channel
    # channel = bot.get_channel(868565628695494716) #shit-code-only channel
    embed = discord.Embed(
        title=title,
        description=desc,
        timestamp=datetime.now(timezone.utc),
        color=0x008e64
    )
    embed.set_footer(text=f"ID: {userid}")
    await channel.send(embed=embed)


async def driftlog2(bot, embed):
    channel = bot.get_channel(857518187884576808)
    await channel.send(embed=embed)


async def errorlog(bot, embed):
    channel = bot.get_channel(943599869795397642)

    await channel.send("<@332314562575597579>", embed=embed)
    return


async def errorlognoping(bot, embed):
    channel = bot.get_channel(943599869795397642)

    await channel.send("ERROR", embed=embed)
    return
