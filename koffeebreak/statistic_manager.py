import re
import os
from datetime import datetime, timedelta

class StatisticManager():
    def __init__(self):
        self.CACHE_DIRECTORY = os.getenv('HOME') + '/.cache/KoffeeBreak/'
        self.HISTORY_FILE = self.CACHE_DIRECTORY + 'history.txt'

        self.reset()

        self.start_timer = datetime.strptime('1900-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.previous_state = None

    def reset(self):
        self.all_time = timedelta()
        self.work_time = timedelta()
        self.short_break_time = timedelta()
        self.long_break_time = timedelta()

        self.number_of_short_breaks = 0
        self.number_of_short_breaks_at_the_comp = 0
        self.number_of_postponed_short_breaks = 0
        self.number_of_skipped_short_breaks = 0

        self.number_of_long_breaks = 0
        self.number_of_long_breaks_at_the_comp = 0
        self.number_of_postponed_long_breaks = 0
        self.number_of_skipped_long_breaks = 0

    def was_work_time(self):
        delta = self.time - self.start_timer
        self.all_time += delta
        self.work_time += delta

    def was_short_break(self):
        delta = self.time - self.start_timer
        self.all_time += delta
        self.short_break_time += delta

    def was_long_break(self):
        delta = self.time - self.start_timer
        self.all_time += delta
        self.long_break_time += delta

    def add_state(self, message):
        self.str_time, self.ms = message.split(' - ')
        self.time = datetime.strptime(self.date + ' ' + self.str_time, '%Y-%m-%d %H:%M:%S')
        if self.ms == 'open program':
            self.previous_state = 'open program'
        elif self.ms == 'start work':
            if self.previous_state == 'start short break':
                self.was_short_break()
            elif self.previous_state == 'start long break':
                self.was_long_break()
            self.start_timer = self.time
            self.previous_state = self.ms
        elif self.ms == 'start short break':
            if self.previous_state == 'start work':
                self.was_work_time()
            self.previous_state = self.ms
            self.start_timer = self.time
            self.number_of_short_breaks += 1
        elif self.ms == 'start long break':
            if self.previous_state == 'start work':
                self.was_work_time()
            self.previous_state = self.ms
            self.start_timer = self.time
            self.number_of_long_breaks += 1
        elif self.ms == 'postpone break':
            if self.previous_state == 'start short break':
                self.number_of_short_breaks -= 1
                self.number_of_postponed_short_breaks += 1
            elif self.previous_state == 'start long break':
                self.number_of_long_breaks -= 1
                self.number_of_postponed_long_breaks += 1
        elif self.ms == 'skip break':
            if self.previous_state == 'start short break':
                self.number_of_short_breaks -= 1
                self.number_of_skipped_short_breaks += 1
            elif self.previous_state == 'start long break':
                self.number_of_long_breaks -= 1
                self.number_of_skipped_long_breaks += 1
        elif self.ms == 'break at the computer':
            if self.previous_state == 'start short break':
                self.number_of_short_breaks_at_the_comp += 1
            elif self.previous_state == 'start long break':
                self.number_of_long_breaks_at_the_comp += 1
        elif self.ms == 'pause program':
            if self.previous_state == 'start work':
                self.was_work_time()
            elif self.previous_state == 'start short break':
                self.was_short_break()
            elif self.previous_state == 'start long break':
                self.was_long_break()
        elif self.ms == 'resume program':
            self.start_timer = self.time
        elif self.ms == 'close program':
            if self.previous_state == 'start work':
                self.was_work_time()
            if self.previous_state == 'start short break':
                self.was_short_break()
            if self.previous_state == 'start long break':
                self.was_long_break()

    def create_statistic_of_day(self, day):
        self.date = day[0:10]
        for message in re.findall("(\d{2}:\d{2}:\d{2} - .+)", day):
            self.add_state(message)

    def reload(self):
        with open(self.HISTORY_FILE) as f:
            self.history = f.read().split(self.str_time + ' - ' + self.ms)[1]
        for date in re.findall('\d{4}-\d{2}-\d{2}', self.history):
            self.date = date
        for message in re.findall('(\d{2}:\d{2}:\d{2} - .+)', self.history):
            self.add_state(message)

    def get_statistic(self):
        return [self.all_time, self.work_time, self.short_break_time,
                self.long_break_time], [self.number_of_short_breaks, self.number_of_short_breaks_at_the_comp,
                self.number_of_postponed_short_breaks, self.number_of_skipped_short_breaks], [self.number_of_long_breaks, self.number_of_long_breaks_at_the_comp,
                self.number_of_postponed_long_breaks, self.number_of_skipped_long_breaks]

    def current_state(self):
        return self.previous_state

    def current_start_timer(self):
        return self.start_timer

    def reset_all(self):
        if os.path.isfile(self.HISTORY_FILE):
            os.remove(self.HISTORY_FILE)

    def read_history(self, number_of_days = None):
        self.reset()
        if os.path.isfile(self.HISTORY_FILE):
            with open(self.HISTORY_FILE) as f:
                self.history = f.read().split('~ ')[1:]
            for day in self.history:
                self.create_statistic_of_day(day)
