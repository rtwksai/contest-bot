#!/usr/bin/python3
import discord
from discord.ext import commands
from utils import cf

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self, ctx):
        '''This command returns the ping.
        Usage: -ping
        '''
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)} ms')

    @commands.command(name = 'cfnext')
    async def next_codeforces(self, ctx, count=3):
        '''Messages 3 nearest contests on CF
        Usage: -cfnext 
               -cfnext [count]
        '''
        url = "https://codeforces.com/api/contest.list"
        c = cf.Codeforces(url)
        result = c.getContests()
        for contest in result[:len(result)-count-1:-1]:
            await ctx.author.send(f"{contest['name']}")

def setup(bot):
    bot.add_cog(Commands(bot))