#!/usr/bin/python3
from datetime import datetime
import json, os, requests, sys

class Codeforces:
    def __init__(self, url):
        self.url = url

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
    def send_notif(self, notify_buffer = 2):
        self.notify = []
        for c in self.contests:
            if(c['relativeTimeSeconds'] <= 3600*24*(-1)*(notify_buffer-1) and c['relativeTimeSeconds'] > 3600*24*(notify_buffer)*(-1)):
                self.notify.append(c)
        return self.notify                

    # Reminder is sent 24 hrs before the event time on the channel.
    def send_reminder(self):
        self.remind = []
        for c in self.contests:
            if(c['relativeTimeSeconds'] > 3600*24*(-1) and c['relativeTimeSeconds'] < 3600*5*(-1)):
                self.remind.append(c)
        return self.remind