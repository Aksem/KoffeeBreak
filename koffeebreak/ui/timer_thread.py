from PyQt5.QtCore import QThread, pyqtSignal, QObject
from timer import timerThread

class qDataProtocol(QObject):
    changeIcon = pyqtSignal(object)

class qWorkThread(QThread):
    def __init__(self, qDataProtocol):
        super(qWorkThread, self).__init__()
        self.timerThread = timerThread()
        self.q_data_protocol = qDataProtocol

    def run(self):
        self.timerThread.start()
        while True:
            if self.timerThread.changeState.wait():
                self.q_data_protocol.changeIcon.emit(self.timerThread.state)
    
    def _delete_(self):
        self.timerThread.stopEvent = True
        print('cloesd')
