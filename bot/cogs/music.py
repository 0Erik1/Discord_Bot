import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os
import glob

ytdl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extract_flat': False,
    'ignoreerrors': True,
    'outtmpl': 'bot/data/songs/%(title)s.%(ext)s',
    'max_filesize': 50*1024*1024
}

ytdl = youtube_dl.YoutubeDL(ytdl_opts)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.index = 0

    @commands.command()
    async def play(self, ctx, url):

        # Função para apagar o arquivo depois que terminar
        def after_playing(error):
            if error:
                print("erro ao tocar a musica")

            self.index +=1
            if self.index < len(self.queue):
                info = ytdl.extract_info(self.queue[self.index], download=True) #sempre baixa o atual
                filename = ytdl.prepare_filename(info)  # caminho do arquivo baixado
            
                # toca a música
                source = discord.FFmpegPCMAudio(filename)
                voice_client.play(source, after=after_playing)
            else:
                folder = "bot/data/songs"

                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        
        #verifica se está em um canal para conectar
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Entre em um canal de voz primeiro!")
                return

        voice_client = ctx.voice_client
        self.queue.append(url) #adiciona url a lista

        if not voice_client.is_playing():

            info = ytdl.extract_info(url, download=False)
            if "duration" in info and info["duration"] > 600:  # 600 segundos = 10 minutos
                await ctx.send("O áudio é muito longo! Máximo permitido: 10 minutos.")
                return

            # Baixa o áudio
            info = ytdl.extract_info(self.queue[self.index], download=True) #sempre baixa o atual
            filename = ytdl.prepare_filename(info)  # caminho do arquivo baixado

            # toca a música
            source = discord.FFmpegPCMAudio(filename)
            voice_client.play(source, after=after_playing)
            await ctx.send(f"Tocando agora: {info['title']}")

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Música parada!")

            folder = "bot/data/songs"

            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            await ctx.send("Não há música tocando agora.")

    # @commands.command()
    # async def skip(self, ctx):
    #     voice_client = ctx.voice_client
    #     if voice_client and voice_client.is_playing():
    #         self.index += 1
            
    #         await ctx.send("Música pulada!")
    #     else:
    #         await ctx.send("Não há música tocando para pular.")

async def setup(bot):
    await bot.add_cog(Music(bot))
