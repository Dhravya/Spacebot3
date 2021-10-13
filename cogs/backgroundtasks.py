from click import command
import discord
from discord.ext import commands
from discord.ext import tasks

import random, asyncio, json, io
from functools import reduce
import asyncpraw
from datetime import datetime
from otherfiles import canvas

class Suicide(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label="Click Here", url="https://suicide.org"))

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.topggpy = bot.topggpy
        self.session = bot.httpsession
        self.reddit = bot.reddit
        self.statuses = bot.statuses
        self.do_fotd.start()
        self.do_qotd.start()
        self.bot.loop.create_task(self.changingPresence())
        self.do_reddit_feed.start()
        self.update_stats.start()
    
    async def check_voted(self, userid):
        return await self.bot.topggpy.get_user_vote(userid)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("------")
        channel = self.bot.get_channel(893465721982562355)
        message = await channel.fetch_message(channel.last_message_id)
        await message.attachments[0].save("otherfiles/data/db/database.json")
        print("Got the file")
        # await bot.change_presence(activity = discord.Game(name=f"on {len(bot.guilds)} servers | .help"))


    @commands.Cog.listener()
    async def on_message(self,message):
        name = message.author
        if message.author == self.bot.user:
            return

        if message.content.startswith("deez"):
            await message.channel.send(f"deez nuts in {name}s mouth")
        if "kill myself" in message.content.lower() or "suicide" in message.content.lower():
            em = discord.Embed(
                colour=discord.Colour.dark_red(),
                title="Suicide is no joke!",
                description="""There are people who care for you... and suicide is not a solution for ANYTHING.
            \nPlease go to this website for suicide helpline. """,
                url="http://www.suicide.org",
            )
            await message.channel.send(embed=em, view=Suicide())


    @tasks.loop(minutes=10)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update the server count."""
        try:
            await self.bot.topggpy.post_guild_count()
            chan = self.bot.get_channel(893465721982562355)
            await chan.send(f"Posted server count ({self.bot.topggpy.guild_count})")
        except Exception as e:
            print(f"Failed to post server count\n{e.__class__.__name__}: {e}")
        d = self.bot.get_channel(893465721982562355)
        await d.send(
            file=discord.File("otherfiles/data/db/database.json", filename="database.json")
        )

    async def changingPresence(self):
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            status = random.choice(self.bot.statuses)
            await self.bot.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(5)

    @tasks.loop(minutes=0.5)
    async def do_reddit_feed(self):
        await self.bot.wait_until_ready()

        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)

        channels_feed_list = reduce(
            lambda x, y: {**x, **y},
            (
                x
                for v in db["servers"].values()
                if (x := v.get("settings", {}).get("feeds", {}).get("redditfeed", 0))
            ),
            {},
        )
        channels = channels_feed_list.keys()

        for channel in channels:
            channelid = int(channel)

            id = db["servers"][str(self.bot.get_channel(channelid).guild.id)]["settings"][
                "feeds"
            ]["Last_reddit_post"][str(channelid)]
            subredditname = channels_feed_list[channel]
            subreddit = await self.reddit.subreddit(subredditname)
            async for submission in subreddit.new(limit=1):
                if not submission.over_18 and submission.id != id:
                    name = submission.title
                    url = submission.url

                    em = discord.Embed(
                        colour=discord.Colour.blurple(),
                        title=name,
                        url=f"https://reddit.com/{submission.id}",
                    )
                    if "comment" in url:
                        url = submission.selftext
                        em.description = url
                    elif "v.redd.it" in url:
                        em.description = url
                        continue
                    else:
                        em.set_image(url=url)
                    await subreddit.load()
                    em.set_author(
                        name=submission.author,
                        icon_url="https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?auto=webp&s=38648ef0dc2c3fce76d5e1d8639234d8da0152b2",
                    )
                    em.set_footer(
                        text=f"Taken from r/{subreddit}, Score = {submission.score}",
                        icon_url=subreddit.icon_img,
                    )

                    target_channel = self.bot.get_channel(channelid)
                    await target_channel.send(embed=em)
                    db["servers"][str(self.bot.get_channel(channelid).guild.id)]["settings"][
                        "feeds"
                    ]["Last_reddit_post"][str(channelid)] = submission.id
                    with open("otherfiles/data/db/database.json", "w") as f:
                        json.dump(db, f, indent=4)


    @tasks.loop(seconds=2)  # checks for the time every 2 seconds
    async def do_qotd(self):

        dt = datetime.utcnow()  # this gets the time right now in UTC time

        if dt.hour == 12 and dt.minute == 5 and dt.second == 0:
            with open("otherfiles/data/db/database.json", "r") as f:
                db = json.load(f)
            truth_file = open("otherfiles/data/truths.txt", mode="r", encoding="utf8")
            truth_file_facts = truth_file.read().split("\n")
            truth_file.close()

            for i in truth_file_facts:
                if i == "":
                    truth_file_facts.remove(i)
            question = random.choice(truth_file_facts)
            em = discord.Embed(
                title="Question of the day!",
                description=question,
                colour=discord.Colour.blue(),
                timestamp=dt,
            )
            for server in db["servers"]:
                try:
                    channel = self.bot.get_channel(
                        int(db["servers"][server]["settings"]["qotd"])
                    )
                    await channel.send(embed=em)
                except:
                    pass


    @tasks.loop(seconds=2)  # checks for the time every 2 seconds
    async def do_fotd(self):

        dt = datetime.utcnow()  # this gets the time right now in UTC time
        if dt.hour == 12 and dt.minute == 2 and dt.second == 0:
            with open("otherfiles/data/db/database.json", "r") as f:
                db = json.load(f)
            fact_file = open("otherfiles/data/facts.txt", mode="r", encoding="utf8")
            facts = fact_file.read().split("\n")
            fact_file.close()

            for i in facts:
                if i == "":
                    facts.remove(i)
            question = random.choice(facts)
            em = discord.Embed(
                title="Fact of the day!",
                description=question,
                colour=discord.Colour.blue(),
                timestamp=dt,
            )
            for server in db["servers"]:
                try:
                    channel = self.bot.get_channel(
                        int(db["servers"][server]["settings"]["fotd"])
                    )
                    await channel.send(embed=em)
                except:
                    pass

    @commands.Cog.listener()
    async def on_guild_join(guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return await channel.send(
                    "Hey there! Thank you for adding me!\nMy prefix is `.`\nStart by typing `.help`\nTo use all my features, make sure to give me the following perms:\n~ `Manage Server`, `Kick`, `Ban`, `Manage emojis`, `Manage roles`, `Send messages`, `embed links`, `attach files`, `add reactions`, `use external emojis`, `manage messages`\nVoice channel: connect, speak."
                )


    @commands.Cog.listener()
    async def on_member_join(member):
        print(f"{member} left the server")
        sys_channel = member.guild.system_channel
        if sys_channel:
            data = await canvas.member_banner(
                "Welcome",
                str(member),
                str(member.avatar.url.with_format("png").with_size(256)),
            )
            with io.BytesIO() as img:
                data.save(img, "PNG")
                img.seek(0)
                try:
                    await sys_channel.send(
                        content=member.mention,
                        file=discord.File(fp=img, filename="welcome.png"),
                    )
                except Exception as e:
                    print(e)
        else:
            print("Couldnt send")


    @commands.Cog.listener()
    async def on_member_remove(member):
        sys_channel = member.guild.system_channel
        if sys_channel:
            data = await canvas.member_banner(
                "Bye Bye",
                str(member),
                str(member.avatar.url.with_format("png").with_size(256)),
            )
            with io.BytesIO() as img:
                data.save(img, "PNG")
                img.seek(0)
                try:
                    await sys_channel.send(file=discord.File(fp=img, filename="leave.png"))
                except discord.Forbidden:
                    print("Forbidden")
        else:
            print("Couldnt send")

def setup(bot):
  bot.add_cog(BackgroundTasks(bot))