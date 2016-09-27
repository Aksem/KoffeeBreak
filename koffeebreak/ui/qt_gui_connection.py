from PyQt5.QtCore import pyqtSignal, QObject

class qSignal(QObject):
    changeState = pyqtSignal(object)
    whatTime = pyqtSignal(object)
    closeApp = pyqtSignal()
    skipBreak = pyqtSignal()
    pauseOrResumeTimer = pyqtSignal()
    postponeBreak = pyqtSignal()
    startBreak = pyqtSignal()
