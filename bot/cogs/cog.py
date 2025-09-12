import discord
from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def teste(self,ctx):
        await ctx.send("testado meu chapa!")

async def setup(bot):
    await bot.add_cog(Cog(bot))