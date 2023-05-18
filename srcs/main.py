import asyncio
import config
import discord
from discord.ext import commands

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="/", intents=intents)

    asyncio.run(bot.load_extension("cogs.kk_scheduler"))
    bot.run(config.TOKEN)

if __name__ == "__main__":
    main()
