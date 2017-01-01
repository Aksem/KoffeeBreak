import os
import sys
import re
from datetime import datetime, timedelta

class HistoryManager():
    def __init__(self):
        self.CACHE_DIRECTORY = self.user_cache_dir('KoffeeBreak')
        self.HISTORY_FILE = os.path.join(self.CACHE_DIRECTORY, 'history.txt')
        if not os.path.exists(self.CACHE_DIRECTORY):
            os.makedirs(self.CACHE_DIRECTORY)
        self.last_message = None
        self.last_date = None

    @staticmethod
    def user_cache_dir(appname=None):
        system = sys.platform
        if system.startswith('win'):
            pass
        elif system.startswith('darwin'):
            path = os.path.expanduser('~/Library/Caches')
            if appname:
                path = os.path.join(path, appname)
        else:
            path = os.getenv('XDG_CACHE_HOME', os.path.expanduser('~/.cache'))
            if appname:
                path = os.path.join(path, appname)
        return path

    def get_last_date(self):
        if os.path.isfile(self.HISTORY_FILE):
            with open(self.HISTORY_FILE) as history_file:
                date = history_file.read().rsplit('~ ', 1)[1][:10]
                return datetime.date(datetime.strptime(date, '%Y-%m-%d'))
        else:
            return None

    def get_first_date(self):
        if os.path.isfile(self.HISTORY_FILE):
            with open(self.HISTORY_FILE) as history_file:
                date = history_file.read(12)
            return datetime.date(datetime.strptime(date, '~ %Y-%m-%d'))
        else:
            return None

    def get_history(self):
        if os.path.exists(self.HISTORY_FILE):
            with open(self.HISTORY_FILE, 'r') as history_file:
                return history_file.read().split('~ ')[1:]
        else:
            return None

    def reset(self):
        if os.path.isfile(self.HISTORY_FILE):
            os.remove(self.HISTORY_FILE)

    def get_statistic(self, number_of_days=None):
        start_timer = datetime.strptime('1900-01-01 00:00:00',
                                        '%Y-%m-%d %H:%M:%S')
        previous_state = None

        time = {
            'all': timedelta(),
            'work': timedelta(),
            'short break': timedelta(),
            'long break': timedelta()}
        short_break = {
            'count': 0,
            'at the computer': 0,
            'postponed': 0,
            'skipped': 0}
        long_break = {
            'count': 0,
            'at the computer': 0,
            'postponed': 0,
            'skipped': 0}

        days = self.get_history()

        if days == None:
            return time, short_break, long_break

        if number_of_days:
            date = datetime.strftime(datetime.now() - timedelta(days=number_of_days),
                                     '%Y-%m-%d')
            new_days = list()
            for day in days:
                if day[0:10] > date:
                    new_days.append(day)
            days = new_days

        for day in days:
            for event in re.findall(r'(\d{2}:\d{2}:\d{2} - .+)', day):
                str_time, message = event.split(' - ')
                message_time = datetime.strptime(day[0:10] + ' ' + str_time,
                                                 '%Y-%m-%d %H:%M:%S')
                if message == 'open program':
                    pass
                elif message == 'start work':
                    if previous_state == 'start short break':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['short break'] += delta
                    elif previous_state == 'start long break':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['long break'] += delta
                    start_timer = message_time
                    previous_state = message
                elif message == 'start short break':
                    if previous_state == 'start work':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['work'] += delta
                    previous_state = message
                    start_timer = message_time
                    short_break['count'] += 1
                elif message == 'start long break':
                    if previous_state == 'start work':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['work'] += delta
                    previous_state = message
                    start_timer = message_time
                    long_break['count'] += 1
                elif message == 'postpone break':
                    if previous_state == 'start short break':
                        short_break['count'] -= 1
                        short_break['postponed'] += 1
                    elif previous_state == 'start long break':
                        long_break['count'] -= 1
                        long_break['postponed'] += 1
                elif message == 'skip break':
                    if previous_state == 'start short break':
                        short_break['count'] -= 1
                        short_break['skipped'] += 1
                    elif previous_state == 'start long break':
                        long_break['count'] -= 1
                        long_break['skipped'] += 1
                elif message == 'break at the computer':
                    if previous_state == 'start short break':
                        short_break['at the computer'] += 1
                    elif previous_state == 'start long break':
                        long_break['at the computer'] += 1
                elif message == 'pause program':
                    if previous_state == 'start work':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['work'] += delta
                    elif previous_state == 'start short break':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['short break'] += delta
                    elif previous_state == 'start long break':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['long break'] += delta
                elif message == 'resume program':
                    start_timer = message_time
                elif message == 'close program':
                    if previous_state == 'start work':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['work'] += delta
                    if previous_state == 'start short break':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['short break'] += delta
                    if previous_state == 'start long break':
                        delta = message_time - start_timer
                        time['all'] += delta
                        time['long break'] += delta

        # add the difference between current time and the last time in history
        delta = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  '%Y-%m-%d %H:%M:%S') - start_timer
        time['all'] += delta
        if previous_state == 'start work':
            time['work'] += delta
        elif previous_state == 'start short break':
            time['short break'] += delta
        elif previous_state == 'start long break':
            time['long break'] += delta

        # return as 3 dictionaries: time, short break, long break
        return time, short_break, long_break

    def get_number_of_days(self):
        date = self.get_first_date()
        if date == None:
            return 0
        delta = datetime.date(datetime.now()) - date
        return delta.days + 1 # because YYYY.MM.10 - YYYY.MM.8 = 3 days

    def write_message(self, message):
        current_time = datetime.now()
        current_date = datetime.date(current_time)
        if not self.last_message == message:
            if not self.last_date:
                self.last_date = self.get_last_date()
            if (self.last_date != current_date
                    or not os.path.isfile(self.HISTORY_FILE)):
                self.last_date = current_date
                with open(self.HISTORY_FILE, 'a') as history_file:
                    print('~', self.last_date, file=history_file)
            with open(self.HISTORY_FILE, 'a') as history_file:
                print(datetime.time(current_time).strftime('%H:%M:%S'), '-',
                      message, file=history_file)
            self.last_message = message
