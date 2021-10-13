import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import random, asyncio, json, humor_langs, aiohttp, requests
import akinator as ak
from typing import Optional
from urllib.parse import quote_plus
from otherfiles.utils import random_percentage, Votelink, voteembed

api_link = "https://evilinsult.com/generate_insult.php?lang=en&type=txt"
urlaco = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"

class Fun(
    commands.Cog, name="Fun", description="Fun stuff that no one will use"
):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.topggpy = bot.topggpy
        self.session = bot.httpsession

    def check_voted(self, userid):
        return self.bot.topggpy.get_user_vote(userid)

    @commands.command(
        description="Don't do this. The bot will insult you.", name="talk_rude"
    )
    async def talk_rude(self, ctx: commands.Context):
        """insults the sender... better not do this"""
        name = ctx.message.author.name
        insults = [
            f"I have no interest in talking to you, {name}",
            f"I'm stuck here talking to {name}. What has my life come to.",
            f"Don't you have anything else to do other than talking to me, {name}. I mean I'm not even a real person.",
            f"You talking to a bot makes your lack of friends evident, {name}.",
            f"Sorry, I don't think talking to you is worth my time, {name}"
            f"so, how does it feel to be a disappointment, {name}?",
        ]
        chosen = random.randint(0, len(insults))
        await ctx.send(insults[chosen])

    @commands.command(name="owofy")
    async def owofy(self, ctx: commands.Context, *, message):
        """Converts your message in UwUs. its not worth trying, trust me."""
        await ctx.send(
            f"<:uwupwease:885478700836094032> {humor_langs.owofy(message)} <:uwupwease:885478700836094032>"
        )

    @commands.command(name="britainify")
    async def britainify(self, ctx: commands.Context, *, message):
        """Can you pass me a bo'le o' wo'e'r"""
        await ctx.send(humor_langs.strong_british_accent(message))

    @commands.group(name="cool")
    async def cool(
        self, ctx: commands.Context, member: discord.Member, error=None
    ):

        if member.id == 512885190251642891:
            return await ctx.send(
                "***YOO ITS SPACEDOGGO THE COOLEST PERSON IN EXISTANCE. 1000% cool.\nHe is so cool he needs to go to hot places in order to not freeze. real struggle.*** \n(Not really please free me i am trapped inside a fking discord bot)"
            )

        f = random_percentage()
        # if ctx.invoked_subcommand is None and :
        #     await ctx.send('SpaceDoggo is my creator! he is 1000\%\ cool')
        if ctx.invoked_subcommand is None:
            await ctx.send(
                f"{member.mention} is {f} percent cool, at the moment, atleast".format(
                    ctx
                )
            )
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "inp":
                await ctx.send("You forgot to ask me *who* is cool!")

    @cool.command(name="bot")
    async def _bot(self, ctx: commands.Context):
        """Is the bot cool?"""
        await ctx.send("Yes, the bot is cool.")

    @commands.command(name="roast")
    async def roast(self, ctx: commands.Context, member: discord.Member):

        if not await self.check_voted(ctx.author.id) == True:
            return await ctx.send(embed=voteembed, view=Votelink())

        """the best feature of this bot, i would say, its still as useless as your life tho"""
        try:

            answerapi = requests.get(api_link).content.decode()
            await ctx.send(f" {answerapi},{member.mention}")

        except:
            await ctx.send(
                "try that again, but this time actually mention someone to roast (smh kids these days are dumb)"
            )

    @roast.error
    async def do_repeat_handler(self, ctx, error):

        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "try that again, but this time actually mention someone to roast (smh kids these days are dumb)"
            )

    @cool.error
    async def do_repeat_handler(self, ctx, error):

        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "try that again, but this time actually ask *who* is cool (smh kids these days are dumb)"
            )

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def darkjoke(self, ctx):
        """Read a random dark joke"""
        resp = await self.session.get(
            "https://v2.jokeapi.dev/joke/Dark?blacklistFlags=nsfw,religious,explicit&format=txt"
        )
        await ctx.send((await resp.content.read()).decode("utf-8 "))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dadjoke(self, ctx):
        """Read a random dad joke"""
        resp = await self.session.get(
            "https://icanhazdadjoke.com", headers={"Accept": "text/plain"}
        )
        await ctx.send((await resp.content.read()).decode("utf-8 "))

    @commands.command(
        brief="A *~~hidden~~* duck image command.",
        aliases=["duckmasteral", "quacky", "uck", "\U0001f986"],
        hidden=True,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def quack(self, ctx):  # You found a secret! Congradulations 🎉
        """A *~~hidden~~* duck image command.\nPowered by random-d.uk | Not secretly added by Duck <a:BongoCoding:806396390103187526>"""

        embed = discord.Embed(
            title="Quack Quack :duck:", color=discord.Color.orange()
        )
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        embed.set_footer(
            text="Powered by random-d.uk",
            icon_url="https://cdn.discordapp.com/avatars/426787835044036610/795ed0c0b2da8d6c37c071dc61e0c77f.png",
        )
        file = random.choice(["jpg", "gif"])
        if file == "jpg":
            embed.set_image(
                url=f"https://random-d.uk/api/{random.randint(1,191)}.jpg"
            )
        elif file == "gif":
            embed.set_image(
                url=f"https://random-d.uk/api/{random.randint(1,42)}.gif"
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def fact(self, ctx):
        """Generates a Random Fact"""
        if not await self.check_voted(ctx.author.id) == True:
            return await ctx.send(embed=voteembed, view=Votelink())

        start = "Did you know that "
        facts = [
            "Banging your head against a wall for one hour burns 150 calories.",
            "Snakes can help predict earthquakes.",
            "7% of American adults believe that chocolate milk comes from brown cows.",
            "If you lift a kangaroo’s tail off the ground it can’t hop.",
            "Bananas are curved because they grow towards the sun.",
            "Billy goats urinate on their own heads to smell more attractive to females.",
            "The inventor of the Frisbee was cremated and made into a Frisbee after he died.",
            "During your lifetime, you will produce enough saliva to fill two swimming pools.",
            "Polar bears could eat as many as 86 penguins in a single sitting…",
            "Heart attacks are more likely to happen on a Monday.",
            "In 2017 more people were killed from injuries caused by taking a selfie than by shark attacks.",
            "A lion’s roar can be heard from 5 miles away.",
            "The United States Navy has started using Xbox controllers for their periscopes.",
            "A sheep, a duck and a rooster were the first passengers in a hot air balloon.",
            "The average male gets bored of a shopping trip after 26 minutes.",
            "Recycling one glass jar saves enough energy to watch television for 3 hours.",
            "Approximately 10-20% of U.S. power outages are caused by squirrels.",
        ]

        fact_file = open("otherfiles/data/facts.txt", mode="r", encoding="utf8")
        fact_file_facts = fact_file.read().split("\n")
        fact_file.close()

        for i in fact_file_facts:
            if i == "":
                fact_file_facts.remove(i)

        facts = facts + fact_file_facts

        await ctx.send(start + random.choice(facts).lower())

    @commands.command(aliases=["8ball", "magicball", "enlightenme"])
    async def eightball(self, ctx, *, question):
        '''"The eight ball guides you in every part of you life"'''
        responses = [
            "It is certain",
            "Without a doubt",
            "You may rely on it",
            "Yes definitely",
            "It is decidedly so",
            "As I see it, yes",
            "Most likely",
            "Yes",
            "Outlook good",
            "Signs point to yes",
            "Reply hazy try again",
            "Better not tell you now",
            "Ask again later",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don’t count on it",
            "Outlook not so good",
            "My sources say no",
            "Very doubtful",
            "No",
        ]

        message = discord.Embed(title="8 Ball", colour=discord.Colour.orange())
        message.add_field(name="Question:", value=question, inline=False)
        message.add_field(
            name="Answer:", value=random.choice(responses), inline=False
        )
        await ctx.send(embed=message)

    @commands.command(name="slap")
    @commands.cooldown(1, 10, BucketType.user)
    async def slap_member(self, ctx, member: discord.Member):
        """when someone acts just wayy too dumb"""
        apikey = "54HUKXB98NY0"
        lmt = 50
        search_term = "slap"
        r = requests.get(
            "https://api.tenor.com/v1/h?q=%s&key=%s&limit=%s"
            % (search_term, apikey, lmt)
        )

        if r.status_code == 200:
            top_gifs = json.loads(r.content)
            uri = random.choice(random.choice(top_gifs["results"])["media"])[
                "gif"
            ]["url"]

        else:
            embed = discord.Embed(
                title=f"The site was unable to be reached. Please try again later",
                colour=discord.Colour.blurple(),
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title=f"{ctx.author.display_name} slapped {member.display_name}!",
            colour=discord.Colour.blurple(),
        )

        embed.set_image(url=uri)
        embed.set_footer(text="Powered by Tenor")
        await ctx.send(embed=embed)

    @slap_member.error
    async def do_repeat_hander(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("wait for 10 seconds!")

    @commands.command(name="hit", aliases=["punch"])
    @commands.cooldown(1, 10, BucketType.user)
    async def hit_member(self, ctx, member: discord.Member):
        """To settle a fight the violent way"""
        apikey = "54HUKXB98NY0"
        lmt = 50
        search_term = "punch"
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s"
            % (search_term, apikey, lmt)
        )

        if r.status_code == 200:
            top_gifs = json.loads(r.content)
            uri = random.choice(random.choice(top_gifs["results"])["media"])[
                "gif"
            ]["url"]

        else:
            embed = discord.Embed(
                title=f"The site was unable to be reached. Please try again later",
                colour=discord.Colour.blurple(),
            )
            return await ctx.send(embed=embed)

        embed = discord.Embed(
            title=f"{ctx.author.display_name} punched {member.display_name}!",
            colour=discord.Colour.blurple(),
        )

        embed.set_image(url=uri)
        embed.set_footer(text="Powered by Tenor")
        await ctx.send(embed=embed)

    @hit_member.error
    async def do_repeat_hander(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("wait for 10 seconds!")

    @commands.command(name="sus")
    @commands.cooldown(1, 10, BucketType.user)
    async def sus(self, ctx):
        """Sussu baka"""
        apikey = "54HUKXB98NY0"
        lmt = 50
        suslist = ["sus", "sussy baka"]
        search_term = random.choice(suslist)
        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s"
            % (search_term, apikey, lmt)
        )

        if r.status_code == 200:
            top_gifs = json.loads(r.content)
            uri = random.choice(random.choice(top_gifs["results"])["media"])[
                "gif"
            ]["url"]

        else:
            embed = discord.Embed(
                title=f"The site was unable to be reached. Please try again later",
                colour=discord.Colour.blurple(),
            )
            return await ctx.send(embed=embed)
        try:
            # await ctx.message.delete()
            await ctx.send(uri)
        except:
            await ctx.send(uri)
            await ctx.send(
                "for best experience, i need the permission to delete messages"
            )

    @sus.error
    async def do_repeat_hander(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("wait for 10 seconds!")

    @commands.command(name="tenor")
    @commands.cooldown(1, 10, BucketType.user)
    async def tenor(self, ctx, *, query):
        """Random gif from tenor"""
        apikey = "54HUKXB98NY0"
        lmt = 13

        r = requests.get(
            "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s"
            % (query, apikey, lmt)
        )

        if r.status_code == 200:
            top_gifs = json.loads(r.content)
            uri = random.choice(random.choice(top_gifs["results"])["media"])[
                "gif"
            ]["url"]

            await ctx.message.reply(uri)

        else:
            embed = discord.Embed(
                title=f"The site was unable to be reached. Please try again later",
                colour=discord.Colour.blurple(),
            )
            return await ctx.send(embed=embed)

    @tenor.error
    async def do_repeat_hander(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("wait for 10 seconds!")

    @commands.command(name="truth")
    async def truth(self, ctx):
        truth_file = open(
            "otherfiles/data/truths.txt", mode="r", encoding="utf8"
        )
        truth_file_facts = truth_file.read().split("\n")
        truth_file.close()

        for i in truth_file_facts:
            if i == "":
                truth_file_facts.remove(i)
        await ctx.send(random.choice(truth_file_facts).lower())

    @commands.command(name="dare")
    async def dare(self, ctx):

        dares_file = open(
            "otherfiles/data/dares.txt", mode="r", encoding="utf8"
        )
        dares_file_facts = dares_file.read().split("\n")
        dares_file.close()

        for i in dares_file_facts:
            if i == "":
                dares_file_facts.remove(i)
        await ctx.send(random.choice(dares_file_facts).lower())

    @commands.command(name="ai")
    @commands.cooldown(1, 4, BucketType.user)
    async def ai(self, ctx):

        if not await self.check_voted(ctx.author.id) == True:
            return await ctx.send(embed=voteembed, view=Votelink())

        headers = {
            "x-rapidapi-host": "acobot-brainshop-ai-v1.p.rapidapi.com",
            "x-rapidapi-key": "7325d25be5msh8c8c0d8b6d7b766p105501jsn153ee3a9e854",
        }

        def check(m):
            return m.author == ctx.author and not m.content.startswith(".")

        await ctx.send("Let's chat")
        while True:
            try:

                msg = await self.bot.wait_for(
                    "message", check=check, timeout=120.0
                )
            except asyncio.TimeoutError:
                return await ctx.send("Bye :wave:")
            else:
                if "bye" in msg.content.lower():
                    return await ctx.send("Bye :wave:")
                try:
                    async with ctx.typing():
                        response = requests.request(
                            "GET",
                            urlaco,
                            headers=headers,
                            params={
                                "bid": "178",
                                "key": "sX5A2PcYZbsN5EY6",
                                "uid": "mashape",
                                "msg": msg.content.lower(),
                            },
                        )
                        response = response.json()
                except Exception as e:
                    await ctx.send("Please repeat")
                    print(e)
                    continue
                await msg.reply(
                    response["cnt"]
                    .replace("Acobot", "Spacebot")
                    .replace("Aco", "Spacebot")
                )

    @commands.command(aliases=["xkcd", "comic"])
    async def randomcomic(self, ctx):
        """Get a comic from xkcd."""
        
        async with self.session.get(f"http://xkcd.com/info.0.json") as resp:
            data = await resp.json()
            currentcomic = data["num"]
        rand = random.randint(0, currentcomic)  # max = current comic
        async with self.session.get(
            f"http://xkcd.com/{rand}/info.0.json"
        ) as resp:
                data = await resp.json()
        em = discord.Embed(color=discord.Color.green())
        em.title = f"XKCD Number {data['num']}- \"{data['title']}\""
        em.set_footer(
            text=f"Published on {data['month']}/{data['day']}/{data['year']}"
        )
        em.set_image(url=data["img"])
        await ctx.send(embed=em)

    @commands.command(aliases=["numberfacts"])
    async def numberfact(self, ctx, number: int):
        """Get a fact about a number."""
        if not number:
            await ctx.send(f"Usage: `{ctx.prefix}numberfact <number>`")
            return
        try:
            async with self.session.get(
                f"http://numbersapi.com/{number}?json"
            ) as resp:
                file = await resp.json()
                fact = file["text"]
                await ctx.send(f"**Did you know?**\n*{fact}*")
        except KeyError:
            await ctx.send("No facts are available for that number.")

    @commands.command(aliases=["trump", "trumpquote"])
    async def asktrump(self, ctx, *, question):
        """Ask Donald Trump a question!"""
        async with self.session.get(
            f"https://api.whatdoestrumpthink.com/api/v1/quotes/personalized?q={question}"
        ) as resp:
            file = await resp.json()
        quote = file["message"]
        em = discord.Embed(color=discord.Color.green())
        em.title = "What does Trump say?"
        em.description = quote
        em.set_footer(
            text="Made possible by whatdoestrumpthink.com",
            icon_url="http://www.stickpng.com/assets/images/5841c17aa6515b1e0ad75aa1.png",
        )
        await ctx.send(embed=em)

    @commands.command()
    async def beer(
        self,
        ctx,
        user: discord.Member = None,
        *,
        reason: commands.clean_content = "",
    ):
        """Give someone a beer! 🍻"""
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(
                f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/"
            )

        beer_offer = (
            f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        )
        beer_offer = (
            beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        )
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if (
                m.message_id == msg.id
                and m.user_id == user.id
                and str(m.emoji) == "🍻"
            ):
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for(
                "raw_reaction_add", timeout=30.0, check=reaction_check
            )
            await msg.edit(
                content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻"
            )
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(
                f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;"
            )
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = (
                f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            )
            beer_offer = (
                beer_offer + f"\n\n**Reason:** {reason}"
                if reason
                else beer_offer
            )
            await msg.edit(content=beer_offer)

    @commands.command(aliases=["howhot", "hot"])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """Returns a random percent for how hot is a discord user"""
        user = user or ctx.author

        random.seed(user.id + 110)
        if user.id == 512885190251642891:
            return await ctx.send(
                "***YOO ITS SPACEDOGGO THE HOTTEST PERSON IN EXISTANCE. 1000% hot.*** \n(Not really please free me i am trapped inside a fking discord bot)"
            )
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 75:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command(aliases=["flip", "coin"])
    async def coinflip(self, ctx):
        """Coinflip!"""
        coinsides = ["Heads", "Tails"]
        await ctx.send(
            f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!"
        )

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """Press F to pay respect"""
        h = random.randint(0, 100)
        if h in range(0, 70):
            hearts = ["❤", "💛", "💚", "💙", "💜"]
        elif h == 100:
            hearts = ["[RARE]🖤", "[RARE]🤍"]
        else:
            hearts = ["💘", "❣", "💝", "💞"]
        reason = f"for **{text}** " if text else ""
        await ctx.send(
            f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}"
        )

    @commands.command(aliases=["aki"])
    async def akinator(self, ctx):
        await ctx.send("Akinator is here to guess!")

        def check(msg):
            return (
                msg.author == ctx.author
                and msg.channel == ctx.channel
                and msg.content.lower() in ["y", "n", "p", "b"]
            )

        try:
            aki = ak.Akinator()
            q = aki.start_game()
            while aki.progression <= 80:
                await ctx.send(q)
                await ctx.send("Your answer:(y/n/p/b)")
                msg = await self.bot.wait_for("message", check=check)
                if msg.content.lower() == "b":
                    try:
                        q = aki.back()
                    except ak.CantGoBackAnyFurther:
                        await ctx.send(e)
                        continue
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await ctx.send(e)
                        continue
            aki.win()
            await ctx.send(
                f"It's {aki.first_guess['name']} ({aki.first_guess['description']})! Was I correct?(y/n)\n{aki.first_guess['absolute_picture_path']}\n\t"
            )
            correct = await self.bot.wait_for("message", check=check)
            if correct.content.lower() == "y":
                await ctx.send("Yay\n")
            else:
                await ctx.send("Oof\n")
        except Exception as e:
            await ctx.send(e)

    @commands.command(help="Thank someone!")
    @commands.cooldown(2, 120, commands.BucketType.user)
    async def thank(
        self,
        ctx: commands.Context,
        user_: discord.Member = None,
        *,
        reason=None,
    ):
        prefix = ctx.clean_prefix
        if user_ is None:
            await ctx.send("Thank who? your mom?")
        if user_ == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("You cannot thank yourself! Idiot!")
        if user_.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.reply("You can't thank bots!\nThank real people!")

        if reason is None:
            reason = "being an amazing person!"
        if reason.lower().startswith("for "):
            reason = reason[4:]
        with open("otherfiles/data/db/database.json","r") as f:
            db = json.load(f)
        try:
            db["servers"][str(ctx.guild.id)]["users"][str(user_.id)]["thanks_count"] += 1
        except KeyError:
            db["servers"][str(ctx.guild.id)]["users"][str(user_.id)]["thanks_count"] = 1
        with open("otherfiles/data/db/database.json","w") as f:
            json.dump(db, f, indent=4)  

        return await ctx.reply(
            embed=discord.Embed(
                title=f":heart: Thank you!",
                description=f"Thank you {user_.mention} for {reason}",
            ).set_thumbnail(
                url="https://cdn.discordapp.com/emojis/856078862852161567.png?v=1"
            )
        )
        
    @commands.command(aliases =['thank_count','thankscount','thanks_count'])
    async def thankcount(self,ctx,user:discord.Member = None):
        if user == None:
            user = ctx.author
        with open("otherfiles/data/db/database.json","r") as f:
            db = json.load(f)
        try:
            thankscount = db["servers"][str(ctx.guild.id)]["users"][str(user.id)]["thanks_count"]
        except KeyError:
            thankscount = 0
        await ctx.send(f"{user.display_name} has been thanked {thankscount} times!")

    @commands.command()
    async def simprate(
        self,
        ctx: commands.Context,
        member: Optional[discord.Member],
        *,
        simpable: Optional[str],
    ):
        """Find out how much someone is simping for something."""
        member = member or ctx.author
        rate = random.choice(range(1, 100))
        emoji = self.bot.get_emoji(758821832169619467) or "😳"
        if simpable:
            message = f"{member.mention} is **{rate}**% simping for {simpable} {emoji}"
        else:
            message = f"{member.mention} is **{rate}**% simp {emoji}"
        await ctx.send(
            message, allowed_mentions=discord.AllowedMentions(users=False)
        )

    @commands.command()
    async def clownrate(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ):
        """Reveal someone's clownery."""
        member = member or ctx.author
        rate = random.choice(range(1, 100))
        emoji = self.bot.get_emoji(758821900808880138) or "🤡"
        message = f"{member.mention} is **{rate}**% clown {emoji}"
        await ctx.send(
            message, allowed_mentions=discord.AllowedMentions(users=False)
        )

    @commands.command(aliases=["iq"])
    async def iqrate(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ):
        """100% legit IQ test."""
        member = member or ctx.author
        random.seed(member.id + self.bot.user.id)
        if await self.bot.is_owner(member):
            iq = random.randint(200, 500)
        else:
            iq = random.randint(-10, 200)
        if iq >= 160:
            emoji = self.bot.get_emoji(758821860972036106) or "🧠"
        elif iq >= 100:
            emoji = self.bot.get_emoji(758821993768026142) or "🤯"
        else:
            emoji = self.bot.get_emoji(758821971319586838) or "😔"
        await ctx.send(
            f"{member.mention} has an IQ of {iq} {emoji}",
            allowed_mentions=discord.AllowedMentions(users=False),
        )

    @commands.command(aliases=["sanity"])
    async def sanitycheck(
        self, ctx: commands.Context, member: Optional[discord.Member]
    ):
        """Check your sanity."""
        member = member or ctx.author
        random.seed(str(member.id) + str(self.bot.user.id))
        sanity = random.randint(0, 100)
        await ctx.send(
            f"{member.mention} is {sanity}% sane today.",
        )

    @commands.command()
    async def rainbow(self, ctx, times: int, interval: float):
        """Make a happy rainbow!"""
        rainbow = await ctx.send(
            embed=discord.Embed(title="Rainbow!", color=discord.Color.red())
        )
        time = 0
        error = 0
        if interval < 1.4:
            interval = 1.5
        while times > time:
            time = time + 1
            color = "".join(
                [random.choice("0123456789ABCDEF") for x in range(6)]
            )
            color = int(color, 16)
            try:
                await rainbow.edit(
                    embed=discord.Embed(
                        title="Rainbow!", color=discord.Color(value=color)
                    )
                )
            except:
                if error < 1:
                    await ctx.send("An error occured, trying again.")
                    error = error + 1
                else:
                    await ctx.send("Another error occured, exiting.")
                    return

            await asyncio.sleep(interval)

    @commands.command(hidden=True)
    async def dahipuri(self, ctx):
        await ctx.send(
            "WOAH WOAH WOAH YOU FOUND A HIDDEN COMMAND\nContext: dahipuri is an indian fast food (my creator spacedoggo likes them a lot. https://g.co/kgs/fktGN6 for more info"
        )

    @commands.command(description="This command might get you banned")
    async def annoy(self, ctx, member: discord.Member = None, number: int = 5):
        """Usage: annoy @b1nzy#1337 50
        NOTICE: If you get banned, don't come back crying!"""
        if number > 5:
            number = 5
        member = member or ctx.author
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        if member != None:
            for x in range(number):
                await ctx.channel.trigger_typing()
                await ctx.send(member.mention)
                await asyncio.sleep(8)
        else:
            return await ctx.send(
                f"{ctx.author.mention}, I don't know how to use commands. Help!"
            )

def setup(bot):
  bot.add_cog(Fun(bot))