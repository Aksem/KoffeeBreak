import asyncio
import settings

class Timer():
    def __init__(self, config, gui_connection=None):
        self.config = config
        self.gui_connection = gui_connection
        
        self.init_config()
        if self.GUI == "qt":
            self.init_gui_qt()
        self.init_parameters()
    
    def init_config(self):
        self.GUI = settings.read_parameter(self.config, ['EXECUTION', 'gui'])
        self.WORK_TIME = settings.read_parameter(self.config, ['TIME', 'work_time'], 'int')
        self.SHORT_BREAK_TIME = settings.read_parameter(self.config, ['TIME', 'short_break'], 'int')
        self.LONG_BREAK_TIME = settings.read_parameter(self.config, ['TIME', 'long_break'], 'int')
        self.NUMBER_OF_SHORT_BREAKS = settings.read_parameter(self.config, ['BREAKS', 'number_of_short_breaks'], 'int')
        self.DEFAULT_STATE = settings.read_parameter(self.config, ['EXECUTION', 'state'])
    
    def init_gui_qt(self):
        self.gui_connection.whatTime.connect(self.timeRemain)
        self.gui_connection.skipBreak.connect(self.skipBreak)
        self.gui_connection.pauseTimer.connect(self.pause)
    
    def init_parameters(self):
        self.current_state = self.DEFAULT_STATE
        self.gui_state = self.current_state
        self.left_time = self.WORK_TIME
        self.all_time = self.WORK_TIME
        self.count_short_breaks = 0
        self.is_work_time = True
    
    def timeRemain(self):
            self.gui_connection.timeIs.emit(left_time)
    
    def skipBreak(self):
        self.is_work_time = True
        self.left_time = self.WORK_TIME
    
    def start_or_resume(self):
        self.isActive = True
    
    def pause(self):
        self.isActive = False
        
    async def makeStep(self):
        self.left_time -= 1
        await asyncio.sleep(1)

        percentage = self.left_time/self.all_time * 100
        if self.is_work_time:
            if percentage <= 100 and percentage > 87.5:
                self.current_state = 'work-full'
            elif percentage <= 87.5 and percentage > 75:
                self.current_state = 'work-7-8'
            elif percentage <= 75 and percentage > 62.5:
                self.current_state = 'work-6-8'
            elif percentage <= 62.5 and percentage > 50:
                self.current_state = 'work-5-8'
            elif percentage <= 50 and percentage > 37.5:
                self.current_state = 'work-4-8'
            elif percentage <= 37.5 and percentage > 25:
                self.current_state = 'work-3-8'
            elif percentage <= 25 and percentage > 12.5:
                self.current_state = 'work-2-8'
            elif percentage <=12.5 and percentage > 0:
                self.current_state = 'work-1-8'
            else:
                self.current_state = 'work-1-8'
                self.is_work_time = False
                if self.count_short_breaks < self.NUMBER_OF_SHORT_BREAKS:
                    self.left_time = self.SHORT_BREAK_TIME
                    self.all_time = self.SHORT_BREAK_TIME
                    self.count_short_breaks += 1
                else:
                    self.left_time = self.LONG_BREAK_TIME
                    self.all_time = self.LONG_BREAK_TIME
                    self.count_short_breaks = 0
        else:
            if percentage <= 100 and percentage > 75:
                self.current_state = 'break-full'
            elif percentage <= 75 and percentage > 50:
                self.current_state = 'break-3-4'
            elif percentage <= 50 and percentage > 25:
                self.current_state = 'break-2-4'
            elif percentage <= 25 and percentage > 0:
                self.current_state = 'break-1-4'
            else:
                self.current_state = 'break-1-4'
                self.is_work_time = True
                self.left_time = WORK_TIME
                self.all_time = WORK_TIME

        if self.current_state != self.gui_state:
            self.gui_connection.changeState.emit(self.current_state)
            self.gui_state = self.current_state

async def timer(loop, config, gui_connection=None):
    timer = Timer(config, gui_connection)
    timer.start_or_resume()
    while timer.isActive:
        await timer.makeStep()
        print(timer.left_time)
