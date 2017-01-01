import asyncio
import settings
from history_manager import HistoryManager

class Timer():
    def __init__(self, config, gui_connection=None):
        self.config = config
        self.gui_connection = gui_connection

        self.init_config()
        self.init_parameters()
        if self.GUI == "qt":
            self.init_gui_qt()

        self.history_file = HistoryManager()
        self.history_file.write_message('open program')

        self.start_work()

    def init_config(self):
        self.GUI = settings.read_parameter(self.config, ['EXECUTION', 'gui'])
        self.WORK_TIME = settings.read_parameter(self.config, ['TIME', 'work_time'], 'int')
        self.TIME_OF_SHORT_BREAK = settings.read_parameter(self.config,
                                                           ['TIME', 'time_of_short_break'], 'int')
        self.TIME_OF_LONG_BREAK = settings.read_parameter(self.config,
                                                          ['TIME', 'time_of_long_break'], 'int')
        self.WORK_TIME_WHEN_POSTPONE_BREAK = settings.read_parameter(self.config,
                                                                     ['TIME', 'work_time_when_postpone_break'],
                                                                     'int')
        self.NUMBER_OF_SHORT_BREAKS = settings.read_parameter(self.config,
                                                              ['BREAKS', 'number_of_short_breaks'],
                                                              'int')
        self.DEFAULT_STATE = settings.read_parameter(self.config, ['EXECUTION', 'state'])

    def init_gui_qt(self):
        self.gui_connection.skipBreak.connect(self.skip_break)
        self.gui_connection.pauseOrResumeTimer.connect(self.pause_or_resume)
        self.gui_connection.postponeBreak.connect(self.postpone_break)
        self.gui_connection.startBreak.connect(self.start_break)
        self.gui_connection.closeApp.connect(self.end)
        self.gui_connection.lockScreen.connect(self.lock_screen)
        self.gui_connection.breakComp.connect(self.break_at_comp)

    def init_parameters(self):
        self.current_state = self.DEFAULT_STATE
        self.gui_state = self.current_state
        self.count_short_breaks = 0
        self.is_pause = False
        self.is_active = False

    def start_work(self):
        self.history_file.write_message('start work')
        self.is_work_time = True
        self.left_time = self.WORK_TIME
        self.all_time = self.WORK_TIME

    def lock_screen(self):
        self.history_file.write_message('lock screen')

    def break_at_comp(self):
        self.history_file.write_message('break at the computer')

    def postpone_break(self):
        self.history_file.write_message('postpone break')
        if self.count_short_breaks > 0:
            self.count_short_breaks -= 1
        self.left_time = self.WORK_TIME_WHEN_POSTPONE_BREAK
        self.all_time = self.WORK_TIME_WHEN_POSTPONE_BREAK
        self.is_work_time = True

    def skip_break(self):
        self.history_file.write_message('skip break')
        if self.count_short_breaks > 0:
            self.count_short_breaks -= 1
        self.start_work()

    def start(self):
        self.is_active = True

    def end(self):
        self.history_file.write_message('close program')
        self.is_active = False

    def pause_or_resume(self):
        if self.is_pause:
            self.history_file.write_message('resume program')
            self.is_pause = False
        else:
            self.history_file.write_message('pause program')
            self.is_pause = True

    def start_break(self):
        # start break
        if self.count_short_breaks < self.NUMBER_OF_SHORT_BREAKS:
            self.history_file.write_message('start short break')
            self.left_time = self.TIME_OF_SHORT_BREAK
            self.all_time = self.TIME_OF_SHORT_BREAK
            self.count_short_breaks += 1
        else:
            self.history_file.write_message('start long break')
            self.left_time = self.TIME_OF_LONG_BREAK
            self.all_time = self.TIME_OF_LONG_BREAK
            self.count_short_breaks = 0
        self.is_work_time = False

    async def makeStep(self):
        if self.GUI == "qt":
            self.gui_connection.whatTime.emit(self.left_time, self.all_time)

        if self.is_pause:
            pass
        elif self.is_work_time:
            if self.left_time == 0:
                self.start_break()
                if self.GUI == "qt":
                    self.gui_connection.isWorkTime.emit(False)
            self.left_time -= 1
        else:
            if self.left_time == 0:
                self.start_work()
                if self.GUI == "qt":
                    self.gui_connection.isWorkTime.emit(True)
            self.left_time -= 1

        #if self.current_state != self.gui_state:
            #if self.GUI == "qt":
                #self.gui_connection.changeState.emit(self.current_state)
            #self.gui_state = self.current_state

        await asyncio.sleep(1)

async def timer(config, gui_connection=None):
    timer = Timer(config, gui_connection)
    timer.start()
    while timer.is_active:
        await timer.makeStep()
        #print(timer.left_time)
