#!/usr/bin/python3
import discord
from discord.ext import commands
from utils import cf, utility
from datetime import datetime

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
        api_url = "https://codeforces.com/api/contest.list"
        c = cf.Codeforces(api_url)
        result = c.get_contests()

        title="Codeforces"
        url="https://codeforces.com/contests"
        description="List of upcoming contests on Codeforces"
        t_url="https://sta.codeforces.com/s/78793/favicon-32x32.png"

        a = utility.Embeds(title, url, description, t_url)

        for contest in result[:count]:
            name = "Contest: "+str(contest['id'])
            value = contest['name']
            date = datetime.fromtimestamp(contest['startTimeSeconds'])
            a.create_embed(name, value, date)
            x = a.get_embed()

        await ctx.author.send(embed=x)

def setup(bot):
    bot.add_cog(Commands(bot))