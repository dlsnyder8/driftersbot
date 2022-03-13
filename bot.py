import os
from discord.ext import commands, tasks
import discord
from discord import Intents, errors, Embed
from discord.ext.commands.core import check
import database as db
import random
import string
import api
from util import checks, log
import asyncio
from datetime import datetime


import config


import logging

# Logging setup?
logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


dev = False


TOKEN = config.TOKEN
DEV_TOKEN = config.DEV_TOKEN

if TOKEN is None or DEV_TOKEN is None:
    print("Bot Token not found in .env folder")
    quit()

if dev is True:
    TOKEN = DEV_TOKEN

# Set discord intents
intents = Intents.all()
game = discord.Game("Contact dyl#8008 with questions")

if not dev:
    bot = commands.Bot(command_prefix='-', intents=intents,
                       activity=game)
else:
    bot = commands.Bot(command_prefix='&&', intents=intents,
                       activity=game)
###########################
#     Local Variables     #

smmo_server = 444067492013408266
test_server = 538144211866746883
fly_server = 710258284661178418


dyl = 332314562575597579


server = smmo_server  # Change this to which ever server the bot is mainly in
bot.server = server

if not dev:

    for f in os.listdir('./cogs'):
        if f.endswith('.py'):
            bot.load_extension(f'cogs.{f[:-3]}')

else:
    # bot.load_extension('cogs.event')
    for f in os.listdir('./cogs'):
        if f.endswith('.py'):
            bot.load_extension(f'cogs.{f[:-3]}')


@bot.event
async def on_ready():

    print(f'{bot.user.name} has connected to Discord')
    await log.errorlognoping(bot, embed=discord.Embed(title="Bot Started", description="The bot has been restarted"))
    print(f"Tasks have been started")


@checks.is_owner()
@bot.command(aliases=["kill"], hidden=True)
async def restart(ctx):
    await ctx.send("Senpai, why you kill me :3")

    await bot.close()



@bot.command(description="Connects your Discord account with your SMMO account", usage="[SMMO-ID]")
async def verify(ctx, *args):
    # needs 1 arg, smmo id
    if len(args) != 1:
        await ctx.send(embed=Embed(title="Verification Process",
                                   description="1) Please find your SMMO ID by running `+us YourNameHere` or navigating to your profile on web app and getting the 4-6 digits in the url\n2) Run `&verify SMMOID`\n3) Add the verification key to your motto, then run `&verify SMMOID` again"))
        return

    smmoid = args[0]

    try:
        smmoid = int(smmoid)
    except:
        await ctx.send("Argument must be a number")
        return

    # check if verified
    if(await db.is_verified(smmoid)):
        await ctx.send("This account has already been linked to a Discord account.")
        return

    if(await db.islinked(ctx.author.id) is True):
        await ctx.send(embed=Embed(title="Already Linked", description=f"Your account is already linked to an SMMO account. If you need to remove this, contact <@{dyl}> on Discord."))
        return

    # check if has verification key in db
    key = await db.verif_key(smmoid, ctx.author.id)
    if(key is not None):

        profile = await api.get_all(smmoid)
        motto = profile['motto']

        if motto is None:
            await ctx.send(f'Something went wrong. Please contact <@{dyl}> on Discord for help')
            return
        if(key in motto):
            await db.update_verified(smmoid, True)

            await ctx.send('You are now verified! You can remove the verification key from your motto.')
            return

        await ctx.reply(f"Verification Failed. You are trying to connect your account to {profile['name']}. Your verification key is: `{key}`")
        await ctx.send(f'Please add this to your motto and run `{ctx.prefix}verify {smmoid}` again!\n <https://web.simple-mmo.com/changemotto>')
        return

    else:
        # key in DB, but someone else tried to add it. Generate new key
        if(await db.key_init(smmoid) is not None):
            await ctx.send("Someone tried to verify with your ID. Resetting key....")
            letters = string.ascii_letters
            key = "SMMO-" + ''.join(random.choice(letters)
                                    for i in range(8))
            await db.update_pleb(smmoid, ctx.author.id, key)
            await ctx.reply(f'Your new verification key is: `{key}`')
            await ctx.send(f'Please add this to your motto and run `{ctx.prefix}verify {smmoid}` again!\n <https://web.simple-mmo.com/changemotto>')
            return

        # no key in db, generate and add
        # generate verification key, add to db, tell user to add to profile and run command again
        else:
            letters = string.ascii_letters
            key = "SMMO-" + ''.join(random.choice(letters)
                                    for i in range(8))
            await db.add_new_pleb(smmoid, ctx.author.id, key)
            await ctx.reply(f'Your verification key is: `{key}` \nPlease add this to your motto and run `{ctx.prefix}verify {smmoid}` again!\n <https://web.simple-mmo.com/changemotto>')
            return


bot.run(TOKEN)
