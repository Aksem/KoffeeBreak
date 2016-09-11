from PyQt5.QtCore import pyqtSignal, QObject

class qSignal(QObject):
    changeState = pyqtSignal(object)
    whatTime = pyqtSignal()
    timeIs = pyqtSignal(object)
    closeApp = pyqtSignal()
