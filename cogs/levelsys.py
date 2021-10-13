import discord
import json
from discord.ext import commands
from random import randint


class Levelling(commands.Cog, name="Levelling", description="Useful stuff"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # self.bot.topggpy = topgg.DBLClient(self.bot, db["servers"]l_token)

    # def check_voted(self,userid):
    #     return self.bot.topggpy.get_user_vote(userid)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:

            if not message.guild:
                return
            # if not message.author.id == 512885190251642891: return
            with open("otherfiles/data/db/database.json", "r") as f:
                db = json.load(f)

            await self.update_data(db, message.author, message.guild)
            await self.add_experience(db, message.author, randint(2, 8), message.guild)
            await self.level_up(db, message.author, message.channel, message.guild)

            words = db["servers"][str(message.guild.id)
                                  ]["settings"]["filtered_words"]

            with open("otherfiles/data/db/database.json", "w") as f:
                json.dump(db, f, indent=4)
            # if not message.channel == 882249128699117628: return

            for word in words:
                if word in message.content.lower():

                    await message.delete()
                    return

    async def update_data(self, db, user, server):
        if not "servers" in db.keys():
            db["servers"] = {}
            print("made a servers thingy idk")
        try:
            if not str(server.id) in db["servers"]:
                db["servers"][str(server.id)] = {}
                db["servers"][str(server.id)]["settings"] = {}
                db["servers"][str(server.id)]["settings"]["levelon"] = True
                db["servers"][str(server.id)
                              ]["settings"]["level_channel"] = None
                db["servers"][str(server.id)
                              ]["settings"]["filtered_words"] = []
                db["servers"][str(server.id)]["users"] = {}
                if db["servers"][str(server.id)]["settings"]["levelon"] != True:
                    return
                if not str(user.id) in db["servers"][str(server.id)]:
                    db["servers"][str(server.id)]["users"][str(user.id)] = {}
                    db["servers"][str(server.id)]["users"][str(
                        user.id)]["experience"] = 0
                    db["servers"][str(server.id)]["users"][str(
                        user.id)]["level"] = 1
            elif not str(user.id) in db["servers"][str(server.id)]["users"]:
                db["servers"][str(server.id)]["users"][str(user.id)] = {}
                db["servers"][str(server.id)]["users"][str(
                    user.id)]["experience"] = 0
                db["servers"][str(server.id)]["users"][str(
                    user.id)]["level"] = 1
        except:
            pass

    async def add_experience(self, db, user, exp, server):
        if db["servers"][str(server.id)]["settings"]["levelon"] == True:
            db["servers"][str(user.guild.id)]["users"][str(user.id)][
                "experience"
            ] += exp

    async def level_up(self, db, user, channel, server):
        if db["servers"][str(server.id)]["settings"]["levelon"] == True:
            experience = db["servers"][str(user.guild.id)]["users"][str(user.id)][
                "experience"
            ]
            lvl_start = db["servers"][str(user.guild.id)]["users"][str(user.id)][
                "level"
            ]
            lvl_end = int((experience // 42) ** 0.6)
            # MEE6 : xp_to_desired_level = 5 / 6 * desired_level * (2 * desired_level * desired_level + 27 * desired_level + 91)
            if lvl_start < lvl_end:
                try:
                    try:
                        if (
                            db["servers"][str(server.id)
                                          ]["settings"]["level_channel"]
                            == None
                        ):
                            try:
                                try:
                                    if db["servers"][str(str(user.guild.id))]["users"][str(user.id)]["level_pings"] == False:
                                        await channel.send(
                                            "{} has leveled up to Level {}".format(
                                            user.name, lvl_end
                                        )
                                        )
                                    else:
                                        await channel.send(
                                            "{} has leveled up to Level {}".format(
                                                user.mention, lvl_end
                                            )
                                        )
                                except KeyError:
                                    db["servers"][str(str(user.guild.id))]["users"][str(user.id)]["level_pings"] = True
                                    await channel.send(
                                        "{} has leveled up to Level {}".format(
                                            user.mention, lvl_end
                                        )
                                    )
                            except:
                                pass
                        else:
                            targetchannel = self.bot.get_channel(
                                int(
                                    db["servers"][str(server.id)]["settings"][
                                        "level_channel"
                                    ]
                                )
                            )
                            try:
                                try:
                                    if db["servers"][str(str(user.guild.id))]["users"][str(user.id)]["level_pings"] == False:
                                        await targetchannel.send(
                                            "{} has leveled up to Level {}".format(
                                                user.name, lvl_end
                                            ))
                                except KeyError:
                                    db["servers"][str(str(user.guild.id))]["users"][str(user.id)]["level_pings"] = True
                                    await targetchannel.send(
                                        "{} has leveled up to Level {}".format(
                                            user.mention, lvl_end
                                        ))

                            except:
                                pass
                        db["servers"][str(user.guild.id)]["users"][str(user.id)][
                            "level"
                        ] = lvl_end
                    except KeyError:
                        print(KeyError)
                        db["servers"][str(server.id)
                                      ]["settings"]["level_channel"] = None
                except:
                    pass

    @commands.command(aliases=["rank", "lvl"])
    async def level(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.message.author
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
            stats = db["servers"][str(ctx.guild.id)]["users"][str(member.id)]

        if stats is None:
            embed = discord.Embed(
                description="You haven't sent any messages, no rank.")
            await ctx.channel.send(embed=embed)
        else:
            exp = stats["experience"]
            lvl = stats["level"]
            rank = 0
            boxes = int((exp / (200 * ((1 / 2) * lvl))) * 10)

        rankings = sorted(
            db["servers"][str(ctx.guild.id)]["users"].items(),
            key=lambda x: x[1]["experience"],
            reverse=True,
        )
        for x in rankings:
            rank += 1
            if member.id in x:
                break

        lvl_end = int((exp // 42) ** 0.6)
        embed = discord.Embed(title="{}s level stats!".format(member.name))
        embed.add_field(name="Name", value=member.mention, inline=True)
        embed.add_field(name="XP", value=exp, inline=True)
        embed.add_field(name="Level", value=lvl, inline=True)
        embed.add_field(
            name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True
        )
        embed.add_field(
            name="Progress", value=boxes * "🟦" + (20 - boxes) * "⬜", inline=False
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
        rankings = sorted(
            db["servers"][str(ctx.guild.id)]["users"].items(),
            key=lambda x: x[1]["experience"],
            reverse=True,
        )

        i = 1
        embed = discord.Embed(title="Rankings")
        for x in rankings:
            try:

                temp = ctx.message.guild.get_member(int(x[0]))
                print(temp)
                tempexp = x[0]["experience"]
                embed.add_field(
                    name=f"{i}: {temp.name}",
                    value=f"Total Exp: {tempexp}",
                    inline=False,
                )
                i += 1
            except:
                pass
            if i == 11:
                break
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def disable_lvl(self, ctx):
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
        db["servers"][str(ctx.guild.id)]["settings"]["levelon"] = False
        with open("otherfiles/data/db/database.json", "w") as f:
            json.dump(db, f, indent=4)
            await ctx.send(
                f"Successfully disabled levelling for server {ctx.guild.name}"
            )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def enable_lvl(self, ctx):
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
        db["servers"][str(ctx.guild.id)]["settings"]["levelon"] = True
        with open("otherfiles/data/db/database.json", "w") as f:
            json.dump(db, f, indent=4)
            await ctx.send(
                f"Successfully enabled levelling for server {ctx.guild.name}"
            )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def level_channel(self, ctx, channel: discord.TextChannel):
        """Set the level messages to be only sent in a specific channel!"""
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
        db["servers"][str(ctx.guild.id)]["settings"]["level_channel"] = str(
            channel.id)
        with open("otherfiles/data/db/database.json", "w") as f:
            json.dump(db, f, indent=4)
            await ctx.send(f"All levelup messages will now be sent to #{channel.name}.")

    @commands.command()
    async def disable_level_ping(self, ctx):
        """Annoyed by the pings? Disable them using this command."""
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
        db["servers"][str(ctx.guild.id)]["users"][str(ctx.author.id)]["level_pings"] = False
        with open("otherfiles/data/db/database.json", "w") as f:
            json.dump(db, f, indent=4)
            await ctx.send(f"You will not be annoyed with constant levelling pings now..")

    @commands.command()
    async def enable_level_ping(self, ctx):
        """Wanna get notified when you level up? enable level pings."""
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
        db["servers"][str(ctx.guild.id)]["users"][str(ctx.author.id)]["level_pings"] = False
        with open("otherfiles/data/db/database.json", "w") as f:
            json.dump(db, f, indent=4)
            await ctx.send(f"Levelling pings have been re-enabled..")
    
def setup(bot):
    bot.add_cog(Levelling(bot))
