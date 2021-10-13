import datetime, time, asyncio, sys, requests
from psutil import virtual_memory, cpu_percent, cpu_freq
from speedtest import Speedtest
from otherfiles import checks
import discord
from discord.ext import commands


class CogNotFoundError(Exception):
    pass


class CogLoadError(Exception):
    pass


class NoSetupError(CogLoadError):
    pass


class CogUnloadError(Exception):
    pass


class OwnerUnloadWithoutReloadError(CogUnloadError):
    pass


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global startTime
        startTime = time.time()
        print("yo done")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(error.original)

    async def cog_before_invoke(self, ctx):
        """Check for bot owner"""
        if ctx.author.id == 512885190251642891:
            isOwner = True
        if not isOwner:
            raise commands.CommandInvokeError(
                "Only bot owner is permitted to use this command :man_technologist_tone1:"
            )
        return isOwner

    @checks.is_admin()
    @commands.command(name="speedtest", hidden=True)
    async def speed_test(self, ctx):
        """Speedtest"""
        async with ctx.typing():
            s = Speedtest()
            print("assigned")
            s.get_best_server()
            print("got server")
            s.download()
            print("calculated download")
            s.upload()
            print("calculated upload")
            s = s.results.dict()
            print("made dictionary")

            await ctx.send(
                f"Ping: `{s['ping']}ms`\nDownload: `{round(s['download']/10**6, 3)} Mbits/s`\nUpload: `{round(s['upload']/10**6, 3)} Mbits/s`\nServer: `{s['server']['sponsor']}, {s['server']['name']}, {s['server']['country']}`\nBot: `{s['client']['isp']}({s['client']['ip']}) {s['client']['country']} {s['client']['isprating']}`"
            )

    @commands.command(name="botinfo", aliases=["botstats", "status"], hidden=True)
    async def botstats(self, ctx):
        """Bot stats."""
        # Uptime
        if not ctx.message.author.id == 512885190251642891:
            return await ctx.send("this command isnt for you")
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
        # Embed
        em = discord.Embed(color=0x4FFCFA)
        print("embed made")
        em.set_author(name=f"{self.bot.user} Stats:", icon_url=self.bot.user.avatar.url)
        em.add_field(name=":crossed_swords: Servers", value=f"`{len(self.bot.guilds)}`")
        em.add_field(name="uptime", value=uptime)
        mem = virtual_memory()
        mem_usage = f"{mem.percent} % {mem.used / 1024 ** 2:.2f} MiB"
        em.add_field(name=":floppy_disk: Memory usage", value=f"`{mem_usage}`")
        cpu_usage = f"{cpu_percent(1)} % {cpu_freq().current / 1000:.2f} Ghz"
        em.add_field(name=":desktop: CPU usage", value=f"`{cpu_usage}`")

        try:
            await ctx.send(embed=em)
        except Exception:
            await ctx.send(
                "I don't have permission to send embeds here :disappointed_relieved:"
            )

    @commands.command(hidden=True)
    async def milestones(self, ctx):
        """Shows you in how many servers the bot is."""
        stats = await ctx.send("Getting stats, this may take a while.")

        uniquemembers = []
        servercount = len(self.bot.guilds)
        channelcount = len(list(self.bot.get_all_channels()))
        membercount = len(list(self.bot.get_all_members()))
        for member in list(self.bot.get_all_members()):
            if member.name not in uniquemembers:
                uniquemembers.append(member.name)
        uniquemembercount = len(uniquemembers)
        statsmsg = "I am currently in **{}** servers with **{}** channels, **{}** members of which **{}** unique.".format(
            servercount, channelcount, membercount, uniquemembercount
        )
        await stats.edit(statsmsg)
        # start of servercount milestones
        await asyncio.sleep(0.3)
        if servercount >= 10:
            statsmsg = statsmsg + "\n\n:white_check_mark: Reach 10 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 10 servers."
        if servercount >= 50:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 50 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 50 servers."
        if servercount >= 100:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 100 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 100 servers."
        if servercount >= 500:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 500 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 500 servers."
        if servercount >= 1000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 1000 servers."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 1000 servers."
        await stats.edit(statsmsg)
        # start of channelcount milestones
        await asyncio.sleep(0.3)
        if channelcount >= 10:
            statsmsg = statsmsg + "\n\n:white_check_mark: Reach 10 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 10 channels."
        if channelcount >= 50:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 50 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 50 channels."
        if channelcount >= 100:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 100 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 100 channels."
        if channelcount >= 500:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 500 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 500 channels."
        if channelcount >= 1000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 1000 channels."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 1000 channels."
        await stats.edit(statsmsg)
        # start of membercount milestones
        await asyncio.sleep(0.3)
        if membercount >= 1000:
            statsmsg = statsmsg + "\n\n:white_check_mark: Reach 1000 members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 1000 members."
        if membercount >= 5000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 5000 members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 5000 members."
        if membercount >= 10000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 10000 members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 10000 members."
        if membercount >= 50000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 50000 members."
        else:
            statsmsg = statsmsg + "\n:negative_squared_cross_mark: Reach 50000 members."
        if membercount >= 100000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 100000 members."
        else:
            statsmsg = (
                statsmsg + "\n:negative_squared_cross_mark: Reach 100000 members.\n"
            )
        await stats.edit(statsmsg)
        # start of uniquemembercount milestones
        await asyncio.sleep(0.3)
        if uniquemembercount >= 1000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 1000 unique members."
        else:
            statsmsg = (
                statsmsg + "\n:negative_squared_cross_mark: Reach 1000 unique members."
            )
        if uniquemembercount >= 5000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 5000 unique members."
        else:
            statsmsg = (
                statsmsg + "\n:negative_squared_cross_mark: Reach 5000 unique members."
            )
        if uniquemembercount >= 10000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 10000 unique members."
        else:
            statsmsg = (
                statsmsg + "\n:negative_squared_cross_mark: Reach 10000 unique members."
            )
        if uniquemembercount >= 50000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 50000 unique members."
        else:
            statsmsg = (
                statsmsg + "\n:negative_squared_cross_mark: Reach 50000 unique members."
            )
        if uniquemembercount >= 100000:
            statsmsg = statsmsg + "\n:white_check_mark: Reach 100000 unique members."
        else:
            statsmsg = (
                statsmsg
                + "\n:negative_squared_cross_mark: Reach 100000 unique members."
            )
        await stats.edit(statsmsg)

    @commands.command(hidden=True)
    async def getguilds(self, ctx):
        if ctx.author.id == 512885190251642891:
            listofids = []
            for guild in self.bot.guilds:
                listofids.append(f"*{guild.name}* - `{guild.id}`")
            serverstring = ""
            for server in listofids:
                serverstring += server + "\n"
            em = discord.Embed(title="Bot Guilds", description=serverstring)
            await ctx.send(embed=em)

    @commands.command(hidden=True)
    async def pulljson(self, ctx, id):
        if ctx.author.id == 512885190251642891:
            response = requests.request("GET", f"https://jsonkeeper.com/b/{id}")
        with open("otherfiles/data/db/database.json", "w") as f:
            f.write(str(response))

    @commands.command(name='reload', hidden=True)
    async def _reload(self,ctx, *, module : str):
        """Reloads a module."""
        if not ctx.message.author.id == 512885190251642891:
            return await ctx.send("this command isnt for you")
        try:
            self.bot.load_extension(module)
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    async def getBackup(self,ctx):
        if not ctx.message.author.id == 512885190251642891:
            return await ctx.send("this command isnt for you")
        log_channel = self.bot.get_channel(893465721982562355)
        await log_channel.send(
            file=discord.File(
                "otherfiles/data/db/database.json", filename="levelbackup.json"
            )
        )

    @commands.command(hidden=True)
    async def customstatusadd(self,ctx, *, status):
        await self.bot.wait_until_ready()
        if not ctx.message.author.id == 512885190251642891:
            return await ctx.send("this command isnt for you")
        self.bot.statuses.append(status)
        await ctx.send(f"Custom status {status} added")
        log_channel = self.bot.get_channel(893465721982562355)
        await log_channel.send(self.bot.statuses)


    @commands.command(hidden=True)
    async def customstatusremove(self,ctx, *, remove):
        await self.bot.wait_until_ready()
        if not ctx.message.author.id == 512885190251642891:
            return await ctx.send("this command isnt for you")
        try:
            self.bot.statuses.remove(remove)
            await ctx.send(f"Status `{remove}` removed!!")
        except:
            await ctx.send("There is no status with that name!")
        log_channel = self.bot.get_channel(893465721982562355)
        await log_channel.send(self.bot.statuses)

def setup(bot):
    bot.add_cog(Debug(bot))