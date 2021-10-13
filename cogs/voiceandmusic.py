import asyncio, functools, itertools, math, random
import spotipy, youtube_dl, discord, lyricsgenius

from spotipy.oauth2 import SpotifyClientCredentials

from async_timeout import timeout
from discord.ext import commands

from otherfiles.utils import voteembed, Votelink

genius = lyricsgenius.Genius(
    "H-KtNuYpHYXoBJqkt_uScjLamVMBmPOUqinXD2fAS9ictcy2c83ZeeCUHPJticwe"
)

import ctypes
import ctypes.util

youtube_dl.utils.bug_reports_message = lambda: ""

spotipy_id = "1a9ad94e37d24cf4b517e868699dfa46"
spotipy_secret = "42ecbec11b4a48b1944dc8b028b619c2"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=spotipy_id, client_secret=spotipy_secret
    )
)

try:
    print("ctypes - Find opus:")
    a = ctypes.util.find_library("opus")
    print(a)

    print("Discord - Load Opus:")
    b = discord.opus.load_opus(a)
    print(b)

    print("Discord - Is loaded:")
    c = discord.opus.is_loaded()
    print(c)
except:
    pass


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class Utils:
    def getCurrentMemoryUsage(self):
        with open("/proc/self/status") as f:
            memusage = f.read().split("VmRSS:")[1].split("\n")[0][:-3]
            memusage = int(memusage)
            return memusage / 1024

    def get_size(self, bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

class Spotify:
    def getTrackID(self, track):
        track = sp.track(track)
        return track["id"]

    def getPlaylistTrackIDs(self, playlist_id):
        ids = []
        playlist = sp.playlist(playlist_id)
        for item in playlist["tracks"]["items"]:
            track = item["track"]
            ids.append(track["id"])
        return ids

    def getAlbum(self, album_id):
        album = sp.album_tracks(album_id)
        ids = []
        for item in album["items"]:
            ids.append(item["id"])
        return ids

    def getTrackFeatures(self, id):
        meta = sp.track(id)
        features = sp.audio_features(id)
        name = meta["name"]
        album = meta["album"]["name"]
        artist = meta["album"]["artists"][0]["name"]
        return f"{artist} - {name}-{album}"

    def getalbumID(self, id):
        return sp.album(id)


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
    }

    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(
        self,
        ctx: commands.Context,
        source: discord.FFmpegPCMAudio,
        *,
        data: dict,
        volume: float = 0.5,
    ):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get("uploader")
        self.uploader_url = data.get("uploader_url")
        date = data.get("upload_date")
        self.upload_date = date[6:8] + "." + date[4:6] + "." + date[0:4]
        self.title = data.get("title")
        self.thumbnail = data.get("thumbnail")
        self.description = data.get("description")
        self.duration = self.parse_duration(int(data.get("duration")))
        self.tags = data.get("tags")
        self.url = data.get("webpage_url")
        self.views = data.get("view_count")
        self.likes = data.get("like_count")
        self.dislikes = data.get("dislike_count")
        self.stream_url = data.get("url")

    def __str__(self):
        return "**{0.title}** by **{0.uploader}**".format(self)

    @classmethod
    async def create_source(
        cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None
    ):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(
            cls.ytdl.extract_info, search, download=False, process=False
        )
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError("Couldn't find anything that matches `{}`".format(search))

        if "entries" not in data:
            process_info = data
        else:
            process_info = None
            for entry in data["entries"]:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError(
                    "Couldn't find anything that matches `{}`".format(search)
                )

        webpage_url = process_info["webpage_url"]
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError("Couldn't fetch `{}`".format(webpage_url))

        if "entries" not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info["entries"].pop(0)
                except IndexError:
                    raise YTDLError(
                        "Couldn't retrieve any matches for `{}`".format(webpage_url)
                    )

        return cls(
            ctx, discord.FFmpegPCMAudio(info["url"], **cls.FFMPEG_OPTIONS), data=info
        )

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append("{} days".format(days))
        if hours > 0:
            duration.append("{} hours".format(hours))
        if minutes > 0:
            duration.append("{} minutes".format(minutes))
        if seconds > 0:
            duration.append("{} seconds".format(seconds))

        return ", ".join(duration)


class Song:
    __slots__ = ("source", "requester")

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (
            discord.Embed(
                title="Now playing",
                description="```css\n{0.source.title}\n```".format(self),
                color=discord.Color.blurple(),
            )
            .add_field(name="Duration", value=self.source.duration)
            .add_field(name="Requested by", value=self.requester.mention)
            .add_field(
                name="Uploader",
                value="[{0.source.uploader}]({0.source.uploader_url})".format(self),
            )
            .add_field(name="URL", value="[Click]({0.source.url})".format(self))
            .set_thumbnail(url=self.source.thumbnail)
        )

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog, description="Music bot commands, basically groovy but no"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}
        self.bot.topggpy = bot.topggpy

    async def check_voted(self, userid):
        return await self.bot.topggpy.get_user_vote(userid)

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage(
                "This command can't be used in DM channels."
            )

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        await ctx.send("An error occurred: {}".format(str(error)))

    @commands.command(name="join", invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name="summon")
    async def _summon(
        self, ctx: commands.Context, *, channel: discord.VoiceChannel = None
    ):
        """Summons the bot to a voice channel.
        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError(
                "You are neither connected to a voice channel nor specified a channel to join."
            )

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name="leave", aliases=["disconnect", "dc"])
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send("Not connected to any voice channel.")

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name="volume")
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send("Nothing being played at the moment.")

        if 0 > volume > 100:
            return await ctx.send("Volume must be between 0 and 100")

        ctx.voice_state.volume = volume / 100
        await ctx.send("Volume of the player set to {}%".format(volume))

    @commands.command(name="now", aliases=["current", "playing", "np"])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name="pause")
    # @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction("⏯")

    @commands.command(name="resume")
    # @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction("⏯")
        else:
            await ctx.send("Nothing is paused right now")

    @commands.command(name="stop")
    # @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if not ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction("⏹")

    @commands.command(name="skip", aliases=["next"])
    async def _skip(self, ctx: commands.Context):
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send("Not playing any music right now...")

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction("⏭")
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction("⏭")
                ctx.voice_state.skip()
            else:
                await ctx.send(
                    "Skip vote added, currently at **{}/3**".format(total_votes)
                )

        else:
            await ctx.send("You have already voted to skip this song.")

    @commands.command(name="forceskip", aliases=["fs"])
    async def _forceskip(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            return await ctx.send("Not playing any music right now...")

        ctx.voice_state.skip()

    @commands.command(name="clear")
    async def _clear(self, ctx: commands.Context, member: discord.Member = None):
        if member == None:
            for i in enumerate(ctx.voice_state.songs):
                ctx.voice_state.songs.remove(i)
        else:
            for i in enumerate(ctx.voice_state.songs):
                if ctx.message.author == member:
                    ctx.voice_state.songs.remove(i)

    @commands.command(name="queue", aliases=["q"])
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        """Shows the player's queue.
        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Empty queue.")

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ""
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += "`{0}.` [**{1.source.title}**]({1.source.url})\n".format(
                i + 1, song
            )

        embed = discord.Embed(
            description="**{} tracks:**\n\n{}".format(len(ctx.voice_state.songs), queue)
        ).set_footer(text="Viewing page {}/{}".format(page, pages))
        await ctx.send(embed=embed)

    @commands.command(name= 'savequeue')
    async def _savequeue(self,ctx:commands.context,*,name = None):
        if name == None:
            name = str(f"{ctx.author.name}' playlist")
            status = await ctx.send(f"Name wasnt defined, defaulting to {name}")
        else:
            status = await ctx.send(f'Saving the current queue...')
        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue. Nothing saved.')
        await status.edit("this is the playlist that will be saved")
        await ctx.send(ctx.voice_state.songs)

    @commands.command(name="shuffle")
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if not await self.check_voted(ctx.author.id) == True:
            return await ctx.send(embed=voteembed, view=Votelink())

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Empty queue.")

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction("✅")

    @commands.command(name="lofi")
    async def _lofi(self, ctx: commands.Context):
        if not await self.check_voted(ctx.author.id) == True:
            return await ctx.send(embed=voteembed, view=Votelink())
        await ctx.invoke(
            await self._play(
                context=ctx, search="https://www.youtube.com/watch?v=5qap5aO4i9A"
            )
        )

    @commands.command(name="remove")
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send("Empty queue.")

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction("✅")

    @commands.command(name="loop")
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.
        Invoke this command again to unloop the song.
        [little broken, use .suggestdev <information> if it doesnt work]
        """
        if not await self.check_voted(ctx.author.id) == True:
            return await ctx.send(embed=voteembed, view=Votelink())
        if not ctx.voice_state.is_playing:
            return await ctx.send("Nothing being played at the moment.")

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction("✅")

    @commands.command(name="play", aliases=["p"])
    async def _play(self, ctx: commands.Context, *, search: str):
        """Plays a song.
        If there are songs in the queue, this will be queued until the
        other songs finished playing.
        This command automatically searches from various sites if no URL is provided.
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        if (
            "https://open.spotify.com/playlist/" in search
            or "spotify:playlist:" in search
        ):
            n = 0
            async with ctx.typing():
                try:
                    trackcount = 0
                    process = await ctx.send(f"Processing. . .")
                    ids = Spotify.getPlaylistTrackIDs(self, search)
                    tracks = []
                    message = await ctx.send("Getting all songs...")
                    message2 = await ctx.send("Getting songs")

                    for i in range(len(ids)):
                        track = Spotify.getTrackFeatures(self, ids[i])
                        tracks.append(track)
                    for track in tracks:
                        trackcount += 1
                        try:
                            source = await YTDLSource.create_source(
                                ctx, track, loop=self.bot.loop
                            )
                        except YTDLError as e:
                            await ctx.send(
                                "An error occurred while processing this request: {}".format(
                                    str(e)
                                )
                            )
                        else:
                            song = Song(source)
                            await message.edit("Enqueued {}".format(str(source)))
                            n += 1
                            await ctx.voice_state.songs.put(song)
                        await message2.edit(f":white_check_mark: Queued `{n}` songs")
                    await ctx.send("*Tracks Successfully Queued.✔")
                except Exception as err:
                    await ctx.send("Error!")
                    print(err)
        elif "https://open.spotify.com/album/" in search or "spotify:album:" in search:
            n = 0
            message = await ctx.send("Fetching album...")
            async with ctx.typing():
                process = await ctx.send(f"Processing. . .")
                try:
                    ids = Spotify.getAlbum(self, search)
                    tracks = []
                    for i in range(len(ids)):
                        track = Spotify.getTrackFeatures(self, ids[i])
                        tracks.append(track)
                    for track in tracks:
                        try:
                            source = await YTDLSource.create_source(
                                ctx, track, loop=self.bot.loop
                            )
                        except YTDLError as e:
                            await ctx.send(
                                "An error occurred while processing this request: {}".format(
                                    str(e)
                                )
                            )
                        else:
                            song = Song(source)
                            await message.edit("Enqueued {}".format(str(source)))
                            await ctx.voice_state.songs.put(song)
                            await process.edit(content="Album Succesfully Grabbed.")
                except Exception as err:
                    await ctx.send("Error!")
                    print(err)
        elif "https://open.spotify.com/track/" in search or "spotify:track:" in search:
            async with ctx.typing():
                process = await ctx.send(f"Processing. . .")
                msg = await ctx.send("Grabbing Tracks....")
                try:
                    ID = Spotify.getTrackID(self, search)
                    track = Spotify.getTrackFeatures(self, ID)
                    source = await YTDLSource.create_source(
                        ctx, track, loop=self.bot.loop
                    )
                    song = Song(source)
                    await msg.edit("Enqueued {}".format(str(source)))
                    await ctx.voice_state.songs.put(song)
                    await process.edit(content="Track Succesfully Grabbed.")
                except Exception as err:
                    await ctx.send("Error!")
                    print(err)

        else:
            async with ctx.typing():
                try:
                    source = await YTDLSource.create_source(
                        ctx, search, loop=self.bot.loop
                    )
                except YTDLError as e:
                    await ctx.send(
                        "An error occurred while processing this request: {}".format(
                            str(e)
                        )
                    )
                else:
                    song = Song(source)

                    await ctx.voice_state.songs.put(song)
                    message = await ctx.send("Song acquired")
                    await ctx.send("Enqueued {}".format(str(source)))

    @commands.command(name="lyrics")
    async def lyrics(self, ctx: commands.Context, *, song=None):

        if not await self.check_voted(ctx.author.id) == True:
            return await ctx.send(embed=voteembed, view=Votelink())

        if song == None:
            song = VoiceState.is_playing
            print(song)
        song = genius.search_song(song)
        e = discord.Embed(title=f"*Lyrics for {song}:", description=song.lyrics)
        await ctx.send(embed=e)

    @commands.command(name="star", aliases=["savetodm", "save", "savenow"])
    async def savetodm(self, ctx):
        if not await self.check_voted(ctx.author.id) == True:
            return await ctx.send(embed=voteembed, view=Votelink())

        await ctx.send("Playlist sent!! Check DMs")
        await ctx.author.send(embed=ctx.voice_state.current.create_embed())

    @lyrics.error
    async def do_repeat_handler(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to put in a song name!")

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError("You are not connected to any voice channel.")

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError("Bot is already in a voice channel.")


def setup(bot):
    bot.add_cog(Music(bot))
