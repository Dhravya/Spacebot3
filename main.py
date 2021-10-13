import aiohttp
import discord
from discord.ext import commands
from discord.ext import tasks
from otherfiles import utils

import asyncio, os, asyncpraw
from rich.traceback import install
install()
import topgg

dbl_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijg4MTg2MjY3NDA1MTM5MTQ5OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjMyODE5MzIxfQ.V9YXVaMhHMnztsoyzv40iH1IC00Y7eqbHWkgFG1V0Ak"  # set this to your bot's Top.gg token

# intents.members = True
bot = commands.Bot(command_prefix=(utils.get_prefix), description="""SpaceBot has many utility and fun commands that you can use! Also comes with music player!""", intents=discord.Intents.default(), case_insensitive=True)
bot.remove_command("help")


bot.topggpy = topgg.DBLClient(bot, dbl_token, autopost=True, post_shard_count=True)
bot.statuses =  [
    f"on 100 servers | .help",
    f"with 8000+ members | .help",
    "Vote for me on top.gg! | .vote",
    "Listen to songs!!! | .play",
]
bot.reddit = asyncpraw.Reddit(
        client_id="SwiSNW8bR-yGZ3N0ThTIIw",
        client_secret="v04mt8iI5nuw1D6GzR9Ckg1KI5h0Eg",
        user_agent="Spacebot")

async def session(bot):
    bot.httpsession = aiohttp.ClientSession()

asyncio.get_event_loop().run_until_complete(session(bot))

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(
    "ODgxODYyNjc0MDUxMzkxNDk5.YSzAnQ.ZcbzZ9D6cnnUJMnj63E6OBXxa3I"
)

