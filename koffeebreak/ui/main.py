from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QSystemTrayIcon,
                             QMessageBox, QAction, QMenu)
from PyQt5.QtCore import QObject, pyqtSignal, Qt

from ui import settings, break_screen

class Window(QDialog):
    def __init__(self, gui_connection):
        super(Window, self).__init__()
        self.gui_connection = gui_connection
        self.gui_connection.changeState.connect(self.changeState)
        self.gui_connection.timeIs.connect(self.setTime)
        
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
        self.takeBreakAction = QAction(QIcon().fromTheme("koffeebreak-break-full"),
                                  "Take a break", self,
                                  triggered=self.start_break)
        self.pauseAction = QAction(QIcon().fromTheme('media-playback-pause'),
                                  "Pause program",self,
                                  triggered=self.pauseProgram)
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
        icon = QIcon().fromTheme('koffeebreak-' + iconName)
        self.trayIcon.setIcon(icon)
        
    def start_break(self):
        self.break_screen = break_screen.BreakWindow(self.gui_connection)
    
    def changeState(self, state):
        self.setTrayIcon(state)
        if state == "break-1-4":
            pass
            #self.gui_connection.whatTime.emit()
            #self.trayIcon.showMessage("Break-1-4", str(self.time))
        elif state == "break-2-4":
            pass
        elif state == "break-3-4":
            pass
        elif state == "break-full":
            self.start_break()
        elif state == "work-1-8":
            pass
        elif state == "work-2-8":
            pass
        elif state == "work-3-8":
            pass
        elif state == "work-4-8":
            pass
        elif state == "work-5-8":
            pass
        elif state == "work-6-8":
            pass
        elif state == "work-7-8":
            pass
        elif state == "work-full":
            self.break_screen.close() #add try if windows is closed
    
    def setTime(self, time):
        self.time = time
    
    def pauseProgram(self):
        self.gui_connection.pauseTimer.emit()
        
    def close_app(self):
        self.gui_connection.closeApp.emit()
        #QApplication.instance().quit()
