import asyncio
import settings
import history

class Timer():
    def __init__(self, config, gui_connection=None):
        self.config = config
        self.gui_connection = gui_connection

        self.init_config()
        if self.GUI == "qt":
            self.init_gui_qt()
        self.init_parameters()

        self.history_file = history.History()
        self.history_file.write('Open program')

        self.start_work()

    def init_config(self):
        self.GUI = settings.read_parameter(self.config, ['EXECUTION', 'gui'])
        self.WORK_TIME = settings.read_parameter(self.config, ['TIME', 'work_time'], 'int')
        self.TIME_OF_SHORT_BREAK = settings.read_parameter(self.config, ['TIME', 'time_of_short_break'], 'int')
        self.TIME_OF_LONG_BREAK = settings.read_parameter(self.config, ['TIME', 'time_of_long_break'], 'int')
        self.WORK_TIME_WHEN_POSTPONE_BREAK = settings.read_parameter(self.config, ['TIME', 'work_time_when_postpone_break'], 'int')
        self.NUMBER_OF_SHORT_BREAKS = settings.read_parameter(self.config, ['BREAKS', 'number_of_short_breaks'], 'int')
        self.DEFAULT_STATE = settings.read_parameter(self.config, ['EXECUTION', 'state'])

    def init_gui_qt(self):
        self.gui_connection.skipBreak.connect(self.skipBreak)
        self.gui_connection.pauseTimer.connect(self.pause)
        self.gui_connection.postponeBreak.connect(self.postponeBreak)
        self.gui_connection.startBreak.connect(self.start_break)

    def init_parameters(self):
        self.current_state = self.DEFAULT_STATE
        self.gui_state = self.current_state
        self.left_time = self.WORK_TIME
        self.all_time = self.WORK_TIME
        self.count_short_breaks = 0
        self.is_work_time = True

    def postponeBreak(self):
        self.history_file.write('Postpone break')
        if (not self.count_short_breaks == 0):
            self.count_short_breaks -=1
        else:
            self.count_short_breaks = 3
        self.left_time = self.WORK_TIME_WHEN_POSTPONE_BREAK
        self.all_time = self.WORK_TIME_WHEN_POSTPONE_BREAK
        self.is_work_time = True

    def skipBreak(self):
        self.history_file.write('Skip break')
        if (not self.count_short_breaks == 0):
            self.count_short_breaks -=1
        else:
            self.count_short_breaks = 3
        self.start_work()

    def start_work(self):
        self.history_file.write('Start work')
        self.is_work_time = True
        self.left_time = self.WORK_TIME
        self.all_time = self.WORK_TIME

    def start_or_resume(self):
        self.isActive = True

    def pause(self):
        self.history_file.write('Pause program')
        self.isActive = False

    def start_break(self):
        # start break
        if self.count_short_breaks < self.NUMBER_OF_SHORT_BREAKS:
            self.history_file.write('Start short break')
            self.left_time = self.TIME_OF_SHORT_BREAK
            self.all_time = self.TIME_OF_SHORT_BREAK
            self.count_short_breaks += 1
        else:
            self.history_file.write('Start long break')
            self.left_time = self.TIME_OF_LONG_BREAK
            self.all_time = self.TIME_OF_LONG_BREAK
            self.count_short_breaks = 0
        self.is_work_time = False

    async def makeStep(self):
        if self.GUI == "qt":
            self.gui_connection.whatTime.emit(self.left_time)

        percent = self.left_time/self.all_time * 100
        if self.is_work_time:
            if percent <= 100 and percent > 87.5:
                self.current_state = 'work-full'
            elif percent <= 87.5 and percent > 75:
                self.current_state = 'work-7-8'
            elif percent <= 75 and percent > 62.5:
                self.current_state = 'work-6-8'
            elif percent <= 62.5 and percent > 50:
                self.current_state = 'work-5-8'
            elif percent <= 50 and percent > 37.5:
                self.current_state = 'work-4-8'
            elif percent <= 37.5 and percent > 25:
                self.current_state = 'work-3-8'
            elif percent <= 25 and percent > 12.5:
                self.current_state = 'work-2-8'
            elif percent <=12.5 and percent > 0:
                self.current_state = 'work-1-8'
            else:
                self.current_state = 'work-1-8'
                self.start_break()
        else:
            if percent <= 100 and percent > 75:
                self.current_state = 'break-full'
            elif percent <= 75 and percent > 50:
                self.current_state = 'break-3-4'
            elif percent <= 50 and percent > 25:
                self.current_state = 'break-2-4'
            elif percent <= 25 and percent > 0:
                self.current_state = 'break-1-4'
            else:
                self.current_state = 'break-1-4'
                self.start_work()

        if self.current_state != self.gui_state:
            if self.GUI == "qt":
                self.gui_connection.changeState.emit(self.current_state)
            self.gui_state = self.current_state

        self.left_time -= 1
        await asyncio.sleep(1)

async def timer(loop, config, gui_connection=None):
    timer = Timer(config, gui_connection)
    timer.start_or_resume()
    while timer.isActive:
        await timer.makeStep()
        print(timer.left_time)
