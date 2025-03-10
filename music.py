import discord
from discord.ext import commands
from yt_dlp import YoutubeDL

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #all the music related stuff
        self.is_playing = False

        # 2d array containing [song, channel]
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio[ext=m4a]'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

     #searching the item on youtube
    def search_yt(self, url):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info(url, download=False)
                #print(info)
            except Exception: 
                return False
        i = 0
        for item in info['formats']:
            if item['acodec'] != 'none' and (item['ext'] == 'opus' or item['ext'] == 'm4a'):
                break
            else:
                i += 1

        if info['formats'][i]['ext'] != 'opus':
            i = 0
            for item in info['formats']:
                if item['acodec'] != 'none' and item['ext'] == 'm4a':
                    break
                else:
                    i += 1

        if info['formats'][i]['ext'] != 'm4a':
            i = 0
            for item in info['formats']:
                if item['acodec'] != 'none' and item['ext'] == 'mp3':
                    break
                else:
                    i += 1

        return {'source': info['formats'][i]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            #get the first url
            m_url = self.music_queue[0][0]['source']
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']
            #try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #print(self.music_queue)
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def p(self, ctx, url):
        print("play command used - " + str(ctx.message.author))
        role = discord.utils.get(ctx.guild.roles, id=859297043507576862)
        if role in ctx.message.author.roles:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.message.add_reaction('❌')
                #you need to be connected so that the bot knows where to go
                await ctx.send("Please enter a voice channel and try again.")
            else:
                song = self.search_yt(url)
                if type(song) == type(True):
                    await ctx.message.add_reaction('❌')
                    await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
                else:
                    if self.is_playing == True:
                        await ctx.message.add_reaction('✅')
                        await ctx.send("Song added to the queue")
                    self.music_queue.append([song, voice_channel])
                    if self.is_playing == False:
                        await ctx.message.add_reaction('✅')
                        await self.play_music()

    @commands.command(name="queue", help="Displays the current songs in queue")
    async def q(self, ctx):
        print("queue command used - " + str(ctx.message.author))
        role = discord.utils.get(ctx.guild.roles, id=859297043507576862)
        if role in ctx.message.author.roles:
            retval = ""
            for i in range(0, len(self.music_queue)):
                retval += str(i+1) + ". " + self.music_queue[i][0]['title'] + "\n"
            if retval != "":
                await ctx.message.add_reaction('✅')
                await ctx.send(retval)
            else:
                await ctx.send("No music in queue")

    @commands.command(name="skip", help="Skips song")
    async def skip(self, ctx):
        print("skip command used - " + str(ctx.message.author))
        role = discord.utils.get(ctx.guild.roles, id=859297043507576862)
        if role in ctx.message.author.roles:
            if self.vc != "" and self.vc:
                self.vc.pause()
                #try to play next in the queue if it exists
                await self.play_music()
                await ctx.message.add_reaction('✅')
            
    @commands.command(name="disconnect", help="Disconnecting bot from VC")
    async def dc(self, ctx):
        print("disconnect command used - " + str(ctx.message.author))
        role = discord.utils.get(ctx.guild.roles, id=859297043507576862)
        if role in ctx.message.author.roles:
            await ctx.message.add_reaction('✅')
            await self.vc.disconnect()
    
    @commands.command(name="pause", help="Pausing the music")
    async def pause(self, ctx):
        print("pause command used - " + str(ctx.message.author))
        role = discord.utils.get(ctx.guild.roles, id=859297043507576862)
        if role in ctx.message.author.roles:
            await ctx.message.add_reaction('✅')
            self.vc.pause()

    @commands.command(name="resume", help="Resuming the music")
    async def resume(self, ctx):
        print("pause command used - " + str(ctx.message.author))
        role = discord.utils.get(ctx.guild.roles, id=859297043507576862)
        if role in ctx.message.author.roles:
            await ctx.message.add_reaction('✅')
            self.vc.resume()

    @commands.command(name="clear", help="clears queue")
    async def clear(self, ctx):
        print("clear command used - " + str(ctx.message.author))
        role = discord.utils.get(ctx.guild.roles, id=859297043507576862)
        if role in ctx.message.author.roles:
            await ctx.message.add_reaction('✅')
            self.music_queue = []

def setup(bot):
    bot.add_cog(Music(bot))