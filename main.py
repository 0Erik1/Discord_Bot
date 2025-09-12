from bot.bot import *
from bot.cogs.cog import *
from settings import TOKEN
import asyncio

if __name__ == "__main__":
    bot = Bot()
    asyncio.run(bot.load_extension("bot.cogs.cog"))
    asyncio.run(bot.load_extension("bot.cogs.music"))
    bot.run(TOKEN)