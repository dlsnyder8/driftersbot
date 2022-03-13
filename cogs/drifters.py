import discord
from discord.embeds import Embed
from discord.ext import commands, tasks
from util import checks, log
import api
import logging
import database as db
from discord.ext.commands.cooldowns import BucketType


logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

drifters = [1158]
guild_role = 847242243232628737
acquaintance = 847272102955319306
dyl = 332314562575597579


class Drifters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.driftcheck.start()

    @commands.group(aliases=['d'], hidden=True)
    async def Drifters(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @checks.is_verified()
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 60, BucketType.user)
    async def join(self, ctx):
        if ctx.author._roles.has(guild_role):

            if not await db.in_fly(ctx.author.id):
                smmoid = await db.get_smmoid(ctx.author.id)
                profile = await api.get_all(smmoid)
                try:
                    guildid = profile["guild"]["id"]
                except KeyError:
                    await ctx.send("You are not in a guild, and you are definitely not in Drifters")
                    return
                await db.fly_add(ctx.author.id, smmoid, guildid)
                await ctx.send("Added to database :P")
                return

            await ctx.send("You already have the Drifters role :)")
            return

        smmoid = await db.get_smmoid(ctx.author.id)

        # get guild from profile (get_all())
        profile = await api.get_all(smmoid)
        try:
            guildid = profile["guild"]["id"]
        except KeyError as e:
            await ctx.send("You are not in a guild")
            return

        # if user is in a fly guild....
        if guildid in drifters or ctx.author.id == dyl:

            if not await db.in_fly(ctx.author.id):
                await db.fly_add(ctx.author.id, smmoid, guildid)

            roles_given = ""
            try:
                ingamename = profile["name"]
            except Exception as e:
                await ctx.send(e)

            # add roles
            await ctx.author.add_roles(ctx.guild.get_role(guild_role))
            await ctx.author.remove_roles(ctx.guild.get_role(acquaintance))
            await ctx.send(f"Welcome to Friendly :)\nYou can run `{ctx.prefix}fly eligibility` (`{ctx.prefix}f e` for short) to check your eligibility for specific roles (more info in <#710305444194680893>)")
            roles_given += f"<@&{guild_role}>"

            await log.driftlog(self.bot, f"{ingamename} has joined Drifters", f"**Roles given to** {ctx.author.mention}\n{roles_given}", ctx.author.id)
            channel = self.bot.get_channel(853507312773627934)
            if ctx.author.id != dyl:
                await channel.send(f"Welcome {ctx.author.mention} to the Friendliest guild in SimpleMMO!")

            channel2 = self.bot.get_channel(857518187884576808)
            await channel2.send(f"~adminlink {ctx.author.id} {smmoid}")

        else:
            await ctx.send("You are not in Drifters.")
            return

    # @tasks.loop(hours=3)
    async def driftcheck(self):
        await log(self.bot, "Drifters Check Started", "Drifters guild members are being checked")
        await log.driftlog(self.bot, "Drifters Check Started", "Drifters guild members are being checked")
        guild = self.bot.get_guild(846122329661767720)

        role = guild.get_role(guild_role)
        members = role.members
        not_in_fly = 0
        not_linked = 0
        total = 0

        fly1 = await api.guild_members(1158)

        allmembers = fly1
        listUsers = []
        notlinked = []

        for member in members:
            total += 1
            if await db.islinked(member.id):
                smmoid = await db.get_smmoid(member.id)

                if smmoid in allmembers:
                    pass

                # Has Friendly role, but not in Friendly.
                else:
                    listUsers.append(f"{member.mention}")
                    not_in_fly += 1
                    memberroles = ""
                    for role in member.roles:
                        memberroles += f"{role.mention}\n"

                    await member.remove_roles(role, reason="User left Drifters")
                    await member.add_roles(guild.get_role(acquaintance))

            # Commented out to give people time to link
            else:
                # unlinked. remove roles
                not_linked += 1
                notlinked.append(f"{member.mention}")
            #     await member.remove_roles(role, reason="User didn't link to the bot")
            #     await member.add_roles(guild.get_role(acquaintance))

        splitUsers = [listUsers[i:i+33]
                      for i in range(0, len(listUsers), 33)]
        if len(splitUsers) != 0:
            embed = Embed(
                title="Users with Drifters role removed"
            )
            for split in splitUsers:
                embed.add_field(name="Users", value=' '.join(split))

        splitted = [notlinked[i:i+33]
                    for i in range(0, len(listUsers), 33)]
        if len(splitted) != 0:
            embed2 = Embed(
                title="Users Not linked"
            )
            for split in splitted:
                embed2.add_field(name="Users", value=' '.join(split))

        log.driftlog2(self.bot, embed)
        log.driftlog2(self.bot, embed2)

    @driftcheck.before_loop
    async def before_driftcheck(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=1)
    async def stat_update(self):
        await log.log(self.bot, "Task Started", "Events Stats are being updated")
        stat_convert = {"pvp": "user_kills", "step": "steps",
                        "npc": "npc_kills", "level": "level"}
        all_events = await db.active_events()

        for event in all_events:

            participants = await db.get_participants(event.id)

            for participant in participants:

                smmoid = await db.get_smmoid(participant.discordid)
                profile = await api.get_all(smmoid)
                await db.update_stat(event.id,
                                     participant.discordid,
                                     profile[stat_convert[event.type]])

    @stat_update.before_loop
    async def before_stat_update(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Drifters(bot))
    print("Drifters Cog Loaded")
