#!/usr/bin/python3
import discord
from discord.ext import commands
from utils import cf, utility
from datetime import datetime
import time
import asyncio

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "https://codeforces.com/api/contest.list"
        self.title="Codeforces"
        self.url="https://codeforces.com/contests"
        self.t_url="https://sta.codeforces.com/s/78793/favicon-32x32.png"
    
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
        c = cf.Codeforces(self.api_url)
        result = c.get_contests()
        description="List of upcoming contests on Codeforces"

        a = utility.Embeds(self.title, self.url, description, self.t_url)

        for contest in result[:count]:
            name = "Contest: "+str(contest['id'])
            value = contest['name']
            date = datetime.fromtimestamp(contest['startTimeSeconds'])
            a.create_embed(name, value, date)
            embed = a.get_embed()

        await ctx.author.send(embed=embed)

    @commands.command(name = 'notify')
    async def notify_contest(self, ctx):
        c = cf.Codeforces(self.api_url)
        c.notification_scheduler(ctx)


    @commands.command(name = 'remind')
    async def remind_contest(self, ctx, id=None, when_to_remind = "0:0:0"):
        '''Reminds you about the contest you asked a reminder for
        Usage: -remind id
        -remind id [hours:mins:secs]
        Example: -remind 1442
        -remind 1433 3
        -remind 1444 3:12
        -remind 1454 3:4:19

        The contest id can be found out by doing cfnext or from the automatic notifications in the channel.
        '''

        time_list = str(when_to_remind).split(':')
        h = int(time_list[0]) if len(time_list) == 1 else 0
        m = int(time_list[1]) if(len(time_list) == 2) else 0
        s = int(time_list[2]) if(len(time_list) == 3) else 0
        when_to_remind = (h*60*60)+(m*60)+(s)

        c = cf.Codeforces(self.api_url)
        contest = c.find_contest(id)
        print(contest)

        if(when_to_remind > abs(contest['relativeTimeSeconds'])):
            await ctx.author.send('Oops looks like contest would have begun before the mentioned time')
        elif(m>60 or s>60):
            await ctx.author.send('Oops you might want to check time once more')            
        else:
            await asyncio.sleep(contest['relativeTimeSeconds']*(-1) - when_to_remind)

        title="Codeforces Contest Reminder"
        description="Contest begins in {0}".format(time.strftime("%H hours, %M minutes, %S seconds",
                                                    time.gmtime(abs(contest['relativeTimeSeconds']))))
        a = utility.Embeds(title, self.url, description, self.t_url, 0xF93A2F)

        name = "Contest: "+str(contest['id'])
        value = contest['name']
        date = datetime.fromtimestamp(contest['startTimeSeconds'])
        a.create_embed(name, value, date)
        embed = a.get_embed()

        await ctx.author.send(embed=embed)

def setup(bot):
    bot.add_cog(Commands(bot))