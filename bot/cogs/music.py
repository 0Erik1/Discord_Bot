import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os

ytdl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extract_flat': False,
    'ignoreerrors': True,
}

ytdl = youtube_dl.YoutubeDL(ytdl_opts)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url):
        if not ctx.voice_client:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Entre em um canal de voz primeiro!")
                return

        voice_client = ctx.voice_client

        # Baixa o áudio
        info = ytdl.extract_info(url, download=True)
        filename = ytdl.prepare_filename(info)  # caminho do arquivo baixado

        # Função para apagar o arquivo depois que terminar
        def after_playing(error):
            try:
                os.remove(filename)
            except Exception as e:
                print(f"Erro ao remover arquivo: {e}")

        # Toca o arquivo
        source = discord.FFmpegPCMAudio(filename)
        voice_client.play(source, after=after_playing)

        await ctx.send(f"Tocando agora: {info['title']}")

    @commands.command()
    async def stop(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Música parada!")
        else:
            await ctx.send("Não há música tocando agora.")

    @commands.command()
    async def skip(self, ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.send("Música pulada!")
        else:
            await ctx.send("Não há música tocando para pular.")

async def setup(bot):
    await bot.add_cog(Music(bot))
