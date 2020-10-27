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
        self.left = '⏪'
        self.right = '⏩'
        self.remind_3 = '3️⃣'
    
    @commands.command()
    async def ping(self, ctx):
        '''This command returns the ping.
        Usage: -ping
        '''
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)} ms')

    def predicate(self, message, l, r):
        def check(reaction, user):
            if reaction.message.id != message.id or user == self.bot.user:
                return False
            if l and reaction.emoji == self.left:
                return True
            if r and reaction.emoji == self.right:
                return True
            if reaction.emoji == self.remind_3:
                return True
            return False
        return check

    @commands.command(name = 'cfnext')
    async def next_codeforces(self, ctx, count=3):
        '''Messages 3 nearest contests on CF
        Usage: -cfnext 
               -cfnext [count]
        '''
        c = cf.Codeforces(self.api_url)
        result = c.get_contests()
        description="List of upcoming contests on Codeforces"

        messages = []
        contest_objects = result[:count]
        for contest in contest_objects:
            a = utility.Embeds(self.title, self.url, description, self.t_url)
            name = "Contest: "+str(contest['id'])
            value = contest['name']
            date = datetime.fromtimestamp(contest['startTimeSeconds'])
            a.create_embed(name, value, date)
            messages.append(a.get_embed())

        # await ctx.author.send(embed=embeds[1])

        index = 0
        msg = None
        action = ctx.author.send
        while True:
            res = await action(embed=messages[index])

            if res is not None:
                msg = res 
            l = index != 0
            r = index != len(messages) - 1

            await msg.add_reaction(self.left) 
            await msg.add_reaction(self.right)
            await msg.add_reaction(self.remind_3)

            react, user = await self.bot.wait_for('reaction_add', check=self.predicate(msg, l, r))
            
            if react.emoji == self.left:
                index -= 1

            elif react.emoji == self.right:
                index += 1

            elif react.emoji == self.remind_3:
                contest = contest_objects[index]
                when_to_remind = 135*60
                print("Hello")
                await asyncio.sleep(contest['relativeTimeSeconds']*(-1) - when_to_remind)
                print("After")
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

            action = msg.edit

    @commands.command(name = 'notify')
    async def notify_contest(self, ctx):
        c = cf.Codeforces(self.api_url)
        c.notification_scheduler(ctx)


    @commands.command(name = 'remind')
    async def remind_contest(self, ctx, when_to_remind = 95000, id=None):
        '''Reminds you about the contest you asked a reminder for
        Usage: -remind
        -remind [hours:mins:secs]
        Example: -remind
        -remind 3
        -remind 3:12
        -remind 3:4:19
        '''
        # time_list = str(when_to_remind).split(':')
        # h = int(time_list[0])
        # m = int(time_list[1])
        # s = int(time_list[2])
        # when_to_remind = (h*60*60)+(m*60)+(s)

        c = cf.Codeforces(self.api_url)
        contest = c.get_contests()[0]
        print(contest)

        # if(when_to_remind > abs(contest['relativeTimeSeconds'])):
        #     await ctx.author.send('Oops looks like contest would have begun before the mentioned time')
        # elif(m>60 or s>60):
        #     await ctx.author.send('Oops you might want to check time once more')            
        # else:
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