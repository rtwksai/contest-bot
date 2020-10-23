#!/usr/bin/python3
from datetime import datetime
import json, os, requests, sys
import asyncio
from utils import utility
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class Codeforces:
    def __init__(self, url):
        self.url = url
        self.scheduler = AsyncIOScheduler()
        self.loop = asyncio.get_event_loop()

    def get_contests(self):
        r = requests.get(self.url)
        contest = r.json()['result']
        self.contests = []
        for c in contest:
            if(c['phase'] != 'FINISHED' and c['phase'] != 'PENDING_SYSTEM_TEST'):
                self.contests.append(c)
        self.contests = sorted(self.contests, key = lambda i: i['startTimeSeconds'])
        return self.contests

    # Notification is sent 48 hrs before the event date on the channel.
    # This method just returns the valid list of contests which are eligible for notifications
    def get_valid_contests(self, contest_list):
        self.notify_contests = []
        for c in contest_list:
            if(c['relativeTimeSeconds'] > 3600*24*(-1)*2):
                self.notify_contests.append(c)
            else:
                break
        return self.notify_contests                

    # Reminder is sent 24 hrs before the event time on the channel.
    def send_reminder(self):
        self.remind = []
        for c in self.contests:
            if(c['relativeTimeSeconds'] > 3600*24*(-1) and c['relativeTimeSeconds'] < 3600*5*(-1)):
                self.remind.append(c)
        return self.remind

    # async def async_sendNotifications(self, ctx):
    #     while True:
    #         contest_list = self.get_contests()

    #         for contest in self.get_valid_contests(contest_list):
    #             name = "Contest: "+str(contest['id'])
    #             value = contest['name']
    #             date = datetime.fromtimestamp(contest['startTimeSeconds'])
    #             a.create_embed(name, value, date)
    #             x = a.get_embed()
    #             await ctx.send(embed=x)
            
    #         await asyncio.sleep(5*60)

    async def async_sendNotifications(self, ctx):
        contest_list = self.get_contests()
        print(contest_list)
        for contest in self.get_valid_contests(contest_list):
            print("ABC")
            title="Codeforces"
            url="https://codeforces.com/contests"
            description="List of upcoming contests on Codeforces"
            t_url="https://sta.codeforces.com/s/78793/favicon-32x32.png"

            a = utility.Embeds(title, url, description, t_url)
            name = "Contest: "+str(contest['id'])
            value = contest['name']
            date = datetime.fromtimestamp(contest['startTimeSeconds'])
            a.create_embed(name, value, date)
            x = a.get_embed()
            await ctx.send(embed=x)
        

    def sendNotifications(self, ctx):
        try:
            self.scheduler.add_job(self.async_sendNotifications, 'interval', args = [ctx], seconds=2*60)
            self.scheduler.start()
            self.loop.run_forever()
        except KeyboardInterrupt:
            loop.close()



    # def set_noti_timings(self, relativeTimeSeconds, c):



