#!/usr/bin/python3
from config import *
import discord
from discord.ext import commands
import json
import os

# Create this config file on setup
# Make an automated script to set it up
bot = commands.Bot(command_prefix=prefix)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@load.error
async def load_error(ctx, error):
    if(isinstance(error, commands.MissingRequiredArgument)):
        await ctx.send(f'Please specify the COG to load\nCorrect Usage: `-load <cog name>`')

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

@unload.error
async def load_error(ctx, error):
    if(isinstance(error, commands.MissingRequiredArgument)):
        await ctx.send(f'Please specify the COG to unload\n Correct Usage: `-unload <cog name>`')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token)