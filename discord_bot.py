import os

import discord
from discord.ext import commands

from utils import settings

bot = commands.Bot(command_prefix='!', description="A bot to post/update a Steam Server server status in real time.",
                   case_insensitive=True)
config = settings.get('main.json')

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print(f"{discord.utils.oauth_url(bot.user.id)}&permissions=84992")
    game = discord.Game(config['STATUS'])
    await bot.change_presence(activity=game)


bot.run(config['TOKEN'])
