from PyQt5.QtCore import pyqtSignal, QObject

class qSignal(QObject):
    # emit when timer change state. transmit True or False
    isWorkTime = pyqtSignal(object)
    # transmit left time & all time of timer
    whatTime = pyqtSignal(object, object)

    closeApp = pyqtSignal()
    skipBreak = pyqtSignal()
    postponeBreak = pyqtSignal()
    pauseOrResumeTimer = pyqtSignal()
    startBreak = pyqtSignal()
    
    lockScreen = pyqtSignal()
    breakComp = pyqtSignal()
