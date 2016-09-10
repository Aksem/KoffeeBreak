from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QSystemTrayIcon,
                             QMessageBox, QAction, QMenu)
from PyQt5.QtCore import QObject, pyqtSignal, Qt

from ui import settings, break_screen

class Communicate(QObject):
    changeIcon = pyqtSignal()

class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        
        #init settings dialog
        self.settings_dialog = settings.SettingsDialog()
        
        self.createActions()
        self.createTrayIcon()
        self.setTrayIcon('work-full')
        self.trayIcon.show()
        self.setWindowTitle("KoffeeBreak")
        
    def createActions(self):
        self.openAction = QAction(QIcon().fromTheme('document-open'),
                                  "Open", self,
                                  triggered=self.showNormal)
        self.takeBreakAction = QAction(QIcon().fromTheme("koffebreak-break-full"),
                                  "Take a break", self,
                                  triggered=self.start_break)
        self.pauseAction = QAction(QIcon().fromTheme('media-playback-pause'),
                                  "Pause program",self)
        self.settingsAction = QAction(QIcon().fromTheme('configure'),
                                  "Settings", self,
                                  triggered=self.settings_dialog.show)
        self.quitAction = QAction(QIcon().fromTheme('application-exit'),
                                  "Quit", self, triggered=self.close_app)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.openAction)
        self.trayIconMenu.addAction(self.settingsAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.takeBreakAction)
        self.trayIconMenu.addAction(self.pauseAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def setTrayIcon(self, iconName):
        icon = QIcon().fromTheme('koffebreak-' + iconName)
        self.trayIcon.setIcon(icon)
        
    def start_break(self):
        self.break_screen = break_screen.BreakWindow()
    
    def changeState(self, state):
        self.setTrayIcon(state)
        if state == "break-1-4":
            self.trayIcon.showMessage("Break-1-4", "content")

    def close_app(self):
        QApplication.instance().quit()
