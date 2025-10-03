import discord
from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def teste(self,ctx):
        await ctx.send("testado meu chapa!")

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("Você precisa estar em um canal de voz!")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("O bot não está em nenhum canal!")
async def setup(bot):
    await bot.add_cog(Cog(bot))