import os
from datetime import datetime

class HistoryManager():
    def __init__(self):
        self.CACHE_DIRECTORY = os.getenv('HOME') + '/.cache/KoffeeBreak/'
        self.HISTORY_FILE = self.CACHE_DIRECTORY + 'history.txt'
        self.STATISTICS_FILE = self.CACHE_DIRECTORY + 'statistics.txt'
        if not os.path.exists(self.CACHE_DIRECTORY):
            os.makedirs(self.CACHE_DIRECTORY)
        self.last_message = None
        self.find_last_date()

    def find_last_date(self):
        if (os.path.isfile(self.HISTORY_FILE)):
            with open(self.HISTORY_FILE) as f:
                date = f.read().rsplit('~ ', 1)[1][:10]
                self.last_date = datetime.date(datetime.strptime(date, '%Y-%m-%d'))
        else:
            self.last_date = None

    def write_message(self, message):
        current_time = datetime.now()
        if not self.last_message == message:
            if (not self.last_date == datetime.date(current_time) or not os.path.isfile(self.HISTORY_FILE)):
                self.last_date = datetime.date(current_time)
                with open(self.HISTORY_FILE, 'a') as f:
                    print('~', self.last_date, file=f)
            with open(self.HISTORY_FILE, 'a') as f:
                print(datetime.time(current_time).strftime('%H:%M:%S'), '-', message, file=f)
        self.last_message = message
