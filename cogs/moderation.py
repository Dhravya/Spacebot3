import discord
from discord.ext import commands
from otherfiles import checks
from pytimeparse.timeparse import timeparse
import json


class Moderation(commands.Cog):
    """Commands for managing Discord servers."""

    def __init__(self, bot):
        self.bot = bot

    @checks.can_kick()
    @commands.command()
    async def kick(self, ctx, user: discord.Member):
        """Kicks a user from the server."""
        if ctx.author == user:
            return await ctx.send("You cannot kick yourself.")
        await user.kick()
        embed = discord.Embed(
            title=f"User {user.name} has been kicked.", color=0x00FF00
        )
        embed.add_field(name="Goodbye!", value=":boot:")
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)

    @checks.can_ban()
    @commands.command()
    async def ban(self, ctx, user: discord.Member):
        """Bans a user from the server."""
        if ctx.author == user:
            return await ctx.send("You cannot ban yourself.")
        await user.ban()
        embed = discord.Embed(
            title=f"User {user.name} has been banned.", color=0x00FF00
        )
        embed.add_field(name="Goodbye!", value=":hammer:")
        embed.set_thumbnail(url=user.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.message.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                    read_messages=False,
                )
        embed = discord.Embed(
            title="muted",
            description=f"{member.mention} was muted ",
            colour=discord.Colour.light_gray(),
        )
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f" you have been muted from: {guild.name} reason: {reason}")

    @checks.can_mute()
    @commands.command()
    async def unmute(self, ctx, user: discord.Member):
        """Unmutes a user."""
        rolem = discord.utils.get(ctx.guild.roles, name="Muted")
        if rolem not in user.roles:
            return await ctx.send("User is not muted.")
        embed = discord.Embed(
            title=f"User {user.name} has been unmuted.", color=0x00FF00
        )
        embed.add_field(name="Welcome back!", value=":open_mouth:")
        # embed.set_thumbnail(url= user.avatar.url)
        await ctx.send(embed=embed)
        await user.remove_roles(rolem)
        await self.bot.mongoIO.unmuteUser(user, ctx.guild)

    @checks.can_managemsg()
    @commands.command()
    async def prune(self, ctx, count: int):
        """Deletes a specified amount of messages. (Max 100)"""
        count = max(1, min(count, 100))
        await ctx.message.channel.purge(limit=count, bulk=True)

    @checks.can_managemsg()
    @commands.command()
    async def clean(self, ctx):
        """Cleans the chat of the bot's messages."""

        def is_me(m):
            return m.author == self.bot.user

        await ctx.message.channel.purge(limit=100, check=is_me)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a members and deletes their messages."""
        await member.ban(reason=f"Softban - {reason}")
        await member.unban(reason="Softban unban.")
        await ctx.send(f"Done. {member.name} was softbanned.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.Member, *, reason: str):
        """Warn a member via DMs"""
        warning = (
            f"You have been warned in **{ctx.guild}** by **{ctx.author}** for {reason}"
        )
        if not reason:
            warning = f"You have been warned in **{ctx.guild}** by **{ctx.author}**"
        try:
            await user.send(warning)
        except discord.Forbidden:
            return await ctx.send(
                "The user has disabled DMs for this guild or blocked the bot."
            )
        await ctx.send(f"**{user}** has been **warned**")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def wordcensor(self, ctx, *, word):
        """Censors a word on the server"""
        await ctx.send("...")
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)

        db["servers"][str(ctx.guild.id)]["settings"]["filtered_words"].append(word)
        with open("otherfiles/data/db/database.json", "w") as f:
            json.dump(db, f, indent=4)
        await ctx.send("success")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def removecensor(self, ctx, *, word):
        """Remove censored words"""
        await ctx.send("...")
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)

        db["servers"][str(ctx.guild.id)]["settings"]["filtered_words"].remove(word)
        with open("otherfiles/data/db/database.json", "w") as f:
            json.dump(db, f, indent=4)
        await ctx.send("success")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def censoredwords(self, ctx):
        """Censors a word on the server"""
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
        await ctx.send(
            f"List of mentioned words: {db['servers'][str(ctx.guild.id)]['settings']['filtered_words']}"
        )

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def qotd(self, ctx, channel: discord.TextChannel = None):
        """Enables the question of the day to be sent to the respective channel
        This is a great way to keep the server active!"""
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
        if channel == None:
            channel = ctx.channel
        db["servers"][str(ctx.guild.id)]["settings"]["qotd"] = str(channel.id)
        with open("otherfiles/data/db/database.json", "w") as f:
            json.dump(db, f, indent=4)
        await ctx.send(f"Successfully enabled quotd for channel {channel.mention}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def fotd(self, ctx, channel: discord.TextChannel = None):
        """Enables the fact of the day to be sent to the respective channel
        This is a great way to keep the server active!"""
        with open("otherfiles/data/db/database.json", "r") as f:
            db = json.load(f)
        if channel == None:
            channel = ctx.channel
        db["servers"][str(ctx.guild.id)]["settings"]["fotd"] = str(channel.id)
        with open("otherfiles/data/db/database.json", "w") as f:
            json.dump(db, f, indent=4)
        await ctx.send(f"Successfully enabled fotc for channel {channel.mention}")

def setup(bot):
  bot.add_cog(Moderation(bot))