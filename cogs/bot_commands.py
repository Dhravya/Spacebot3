import discord
from discord.ext import commands
import json
from otherfiles.utils import Invite

class BotCommands(commands.Cog):
    @commands.group(invoke_without_command=True)
    async def help(self,ctx, text:str=''):
        class HelpLinks(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(discord.ui.Button(label="Join the server for chill and hangout!", url='https://discord.gg/Ws4Q42QjY3'))
                self.add_item(discord.ui.Button(label="Website", url='https://bit.ly/spacebot-discord'))
                self.add_item(discord.ui.Button(label="Vote on topgg", url='https://top.gg/bot/881862674051391499/vote',row=2))
                self.add_item(discord.ui.Button(label="Commands page", url='https://dhravyashah.gitbook.io/spacebot',row=2))
        if not text == '':
            try:
                cmd =self.bot.get_command(text)
            except:
                pass

            if cmd:
                print(cmd.description)
                em = discord.Embed(title=f"Help for .{cmd.name}", description=f'{cmd.cog_name}\n{cmd.clean_params}\n {cmd.help}',color=discord.Colour.random())
                return await ctx.send(embed=em)
            elif cmd == None:
                try:
                    cogf = self.bot.get_cog(text)
                    if cogf:
                        return await ctx.send(embed = discord.Embed(colour=discord.Colour.dark_red() ,title=cogf.__cog_name__, description=f"{cogf.description}\n☹️There are too many commands to be displayed here.\nGet help on this cog [on the commands page.](https://dhravyashah.gitbook.io/commands/{text})"))
                    elif cogf == None:
                        return await ctx.send(f"No cog or command {text} found.")
                except Exception as e:
                    return await ctx.send()

        em = discord.Embed(title='🔴 ***SPACEBOT HELP***',
        description=
        """
        > I'm a feature-packed bot with tons of commands. 
        > Spacebot is one of the best multipurpose bots with
        > Fun, Utility, Games, Music, Moderation and Levelling!

        ⚠️ *NEW FEATURES* - DISCOMEGLE AND LEVELLING COMMANDS!
        > *DM* the bot `joinpool` to be added in the pool of users.
        > converse with strangers annonymously!

        > You can now disable levelling pings using `.disable_level_ping`
        > Levelling can be turned off server-wide using `.disable_lvl`

        [Get a detailed list of commands here](https://dhravyashah.gitbook.io/)

        Get commands list using `.help commands`
        ```Invite me using the .invite command!```

        Because of the [upsurge](https://i.imgur.com/EWcyyD7.png) in the number of servers, spacebot is running low on memory.
        __*Help Spacebot stay alive!*__ [Donate here- ko-fi.com/spacebot](https://ko-fi.com/spacebot)""")
        em.set_image(url='https://cdn.discordapp.com/attachments/896097659646017596/896326689141968896/standard.gif')
        em.set_footer(text="Have a suggestion or feedback? Use the .suggestdev command")
        em.color = discord.Colour.blue()
        try:
            await ctx.send(embed=em, view = HelpLinks())
        except discord.Forbidden:
            await ctx.send("I don't have permission to send embeds here :disappointed_relieved:")

    @help.command(name="commands")
    async def give_commands(self,ctx):
        em = discord.Embed(title='SpaceBot commands!', description="[Get a detailed list of commands here](https://dhravyashah.gitbook.io/)\nGive feedback using the .suggestdev command")
        with open('help.json', 'r') as help_file:
            data = json.load(help_file)
        data = data['short']
        for key in data:
            em.add_field(name=key, value=data[key])
        em.colour = discord.Colour.blurple()
        await ctx.send(embed=em)

    @commands.command(aliases=["devs", "developer"])
    async def dev(self, ctx):
        embed = discord.Embed(
            title=f"Dhravya Shah", description=f"SpaceDoggo", color=15105570
        )
        embed.add_field(
            name="Biography", value="Hello Greetings from me :smile: ", inline=False
        )
        embed.add_field(name="Twitter", value="twitter.com/dhravyashah", inline=False)
        embed.add_field(name="GitHub", value="github.com/dhravya", inline=False)
        user = "SpaceDoggo#7777"
        embed.set_author(
            name="Developer Information",
        )
        embed.set_footer(text="Command invoked by {}".format(ctx.message.author.name))
        await ctx.send(embed=embed)

    @commands.command(description="Invite our bot to your server!!")
    async def invite(self, ctx):

        await ctx.send("***Add SpaceBot to your server now!***", view=Invite())

    @commands.command()
    async def suggestdev(self, ctx, *, suggestion):
        channel = self.bot.get_channel(883645856123867185)
        embed = discord.Embed(
            colour=discord.Color.blurple(),
            title=f"{ctx.author} Suggested:",
            description=suggestion,
        )
        await ctx.send("Suggestion sent! Thank You!", embed=embed)
        suggested = await channel.send(embed=embed)
        await suggested.add_reaction("👍")
        await suggested.add_reaction("👎")


    @commands.command()
    async def vote(self, ctx):
        em = discord.Embed(
            title="Support Spacebot!😃🥰",
            description="Here's the vote link! https://top.gg/bot/881862674051391499/vote \nBy the way, thanks for voting :)",
        )
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(BotCommands(bot))