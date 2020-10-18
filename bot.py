#!/usr/bin/python3

from config import *
import discord
from discord.ext import commands
import json
import os

# Create this config file on setup
# Make an automated script to set it up
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(prefix):
        # await message.channel.send('Hello!')
        print('Received message from {0}'.format(message.author))

bot.run(token)