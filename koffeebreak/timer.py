import time
import threading

class breakTimer():
    def __init__(self):
        self.start()

    def start(self):
        self.start_time = time.time()

    def actual(self):
        print(time.time() - self.start_time)
        return time.time() - self.start_time

class timerThread(threading.Thread):
    def __init__(self):
        super(timerThread, self).__init__()
        self.timer = breakTimer()
        self.changeState = threading.Event()
        self.state = "work-4-8"
        self.stopEvent = False

    def run(self):
        while True and not self.stopEvent:
            time.sleep(5)
            self.timer.actual()
            self.changeState.set()
            self.changeState.clear()
            
