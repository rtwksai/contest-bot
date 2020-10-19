#!/usr/bin/python3
from config import *
import discord
from discord.ext import commands
import json
import os

bot = commands.Bot(command_prefix=prefix)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

try:
    bot.run(token)
except Exception as e:
    print(f'Error when logging in: {e}')