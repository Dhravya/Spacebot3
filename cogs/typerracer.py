import asyncio, textwrap, discord
from difflib import SequenceMatcher
from functools import partial
from io import BytesIO
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands


class Typeracing(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self._font = None
        self.session = bot.httpsession

    async def get_quote(self) -> Tuple[str, str]:
       
        async with self.session.get("https://api.quotable.io/random") as resp:
            resp = await resp.json()
            return resp["content"], resp["author"]

    @property
    def font(self) -> ImageFont:
        if self._font is None:
            self._font = ImageFont.truetype(
                f"otherfiles/data/Menlo.ttf", encoding="unic"
            )
        return self._font

    def generate_image(self, text: str, color: discord.Color) -> discord.File:
        margin = 20
        newline = 10

        wrapped = textwrap.wrap(text, width=35)
        text = "\n".join(line.strip() for line in wrapped)

        img_width = self.font.getsize(max(wrapped, key=len))[0] + 2 * margin
        img_height = 20 * len(wrapped) + (len(wrapped) - 1) * newline + 2 * margin

        with Image.new("RGBA", (img_width, img_height)) as im:
            draw = ImageDraw.Draw(im)
            draw.multiline_text(
                (margin, margin),
                text,
                spacing=newline,
                font=self.font,
                fill=color.to_rgb(),
            )

            buffer = BytesIO()
            im.save(buffer, "PNG")
            buffer.seek(0)

        return buffer

    async def render_typerace(self, text: str, color: discord.Color) -> discord.File:
        func = partial(self.generate_image, text, color)
        task = self.bot.loop.run_in_executor(None, func)
        try:
            return await asyncio.wait_for(task, timeout=60)
        except asyncio.TimeoutError:
            raise commands.UserFeedbackCheckFailure(
                "An error occurred while generating this image. Try again later."
            )

    @commands.command(aliases=["tr"])
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.max_concurrency(1, commands.BucketType.channel)
    async def typerace(self, ctx: commands.Context) -> None:
        """
        Begin a typing race!
        Credits to Cats3153.
        """
        try:
            quote, author = await self.get_quote()
        except KeyError:
            raise commands.UserFeedbackCheckFailure(
                "Could not fetch quote. Please try again later."
            )

        color = discord.Color.random()
        img = await self.render_typerace(quote, color)
        embed = discord.Embed(color=color)
        embed.set_image(url="attachment://typerace.png")
        if author:
            embed.set_footer(text=f"~ {author}")

        msg = await ctx.send(file=discord.File(img, "typerace.png"), embed=embed)
        acc: Optional[float] = None

        def check(m: discord.Message) -> bool:
            if m.channel != ctx.channel or m.author.bot or not m.content:
                return False  # if satisfied, skip accuracy check and return
            content = " ".join(m.content.split())  # remove duplicate spaces
            accuracy = SequenceMatcher(None, quote, content).ratio()

            if accuracy >= 0.95:
                nonlocal acc
                acc = accuracy * 100
                return True
            return False

        ref = msg.to_reference(fail_if_not_exists=False)
        try:
            winner = await ctx.bot.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            embed = discord.Embed(
                color=discord.Color.blurple(),
                description=f"No one typed the [sentence]({msg.jump_url}) in time.",
            )
            return await ctx.send(embed=embed, reference=ref)

        seconds = (winner.created_at - msg.created_at).total_seconds()
        winner_ref = winner.to_reference(fail_if_not_exists=False)
        wpm = (len(quote) / 5) / (seconds / 60) * (acc / 100)
        description = (
            f"{winner.author.mention} typed the [sentence]({msg.jump_url}) in `{seconds:.2f}s` "
            f"with **{acc:.2f}%** accuracy. (**{wpm:.1f} WPM**)"
        )
        embed = discord.Embed(color=winner.author.color, description=description)
        await ctx.send(embed=embed, reference=winner_ref)

def setup(bot):
  bot.add_cog(Typeracing(bot))