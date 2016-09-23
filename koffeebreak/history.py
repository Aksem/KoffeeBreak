import os
from datetime import datetime

class History():
    def __init__(self):
        self.CACHE_DIRECTORY = os.getenv('HOME') + '/.cache/KoffeeBreak/'
        if not os.path.exists(self.CACHE_DIRECTORY):
            os.makedirs(self.CACHE_DIRECTORY)
        self.HISTORY_FILE = self.CACHE_DIRECTORY + 'history.txt'
        if (os.path.isfile(self.HISTORY_FILE)):
            with open(self.HISTORY_FILE) as f:
                for line in reversed(f.readlines()):
                    if line[0] == '$':
                        date = list(map(int, line[2::].split('-')))
                        self.last_date = datetime.date(datetime(date[0], date[1], date[2]))
                        break
        else:
            self.last_date = None

    def write(self, message):
        if (not self.last_date == datetime.date(datetime.now())):
            self.last_date = datetime.date(datetime.now())
            with open(self.HISTORY_FILE, 'a') as f:
                print('$', self.last_date, file=f)
        with open(self.HISTORY_FILE, 'a') as f:
            print(datetime.time(datetime.now()), '- ' + message, file=f)
