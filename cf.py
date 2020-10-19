#!/usr/bin/python3
from datetime import datetime
import json, os, requests, sys

class Codeforces:
    def __init__(self, url):
        self.url = url

    def getContests(self):
        r = requests.get(self.url)
        contest = r.json()['result']
        self.contests = []
        for c in contest:
            if(c['phase'] != 'FINISHED' or 'PENDING_SYSTEM_TEST'):
                self.contests.append(c)
        return self.contests

    # Notification is sent 48 hrs before the event date.
    def sendNotif(self):
        self.notify = []
        notify_buffer = 2
        for c in self.contests:
            if(c['relativeTimeSeconds'] <= 3600*24*(-1)*(notify_buffer-1) and c['relativeTimeSeconds'] > 3600*24*(notify_buffer)*(-1)):
                self.notify.append(c)
        return self.notify                

    # Reminder is sent 24 hrs before the event time.
    def sendReminder(self):
        self.remind = []
        for c in self.contests:
            if(c['relativeTimeSeconds'] > 3600*24*(-1) and c['relativeTimeSeconds'] < 3600*5*(-1)):
                self.remind.append(c)
        return self.remind 


url = "https://codeforces.com/api/contest.list"
cf = Codeforces(url)
cf.getContests()
cf.sendNotif()
cf.sendReminder()