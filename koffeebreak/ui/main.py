from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QSystemTrayIcon,
                             QMessageBox, QAction, QMenu)
from PyQt5.QtCore import QObject, pyqtSignal, Qt

from ui import settings, timer_thread, break_screen

class Communicate(QObject):
    changeIcon = pyqtSignal()

class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        ## timer thread set up
        self.q_data_protocol = timer_thread.qDataProtocol()
        self.qThread = timer_thread.qWorkThread(self.q_data_protocol)
        self.qThread.start()
        self.qThread.q_data_protocol.changeIcon.connect(self.setIcon)
        
        #init settings dialog
        self.settings_dialog = settings.SettingsDialog()
        
        self.createActions()
        self.createTrayIcon()
        self.setIcon('break-1-4')
        self.trayIcon.show()
        self.setWindowTitle("KoffeeBreak")

    def changeIcon(self):
        print(1)
    def createActions(self):
        self.openAction = QAction(QIcon("img/icons/break-1-4.svg"),"Open",
                                  self, triggered=self.showNormal)
        self.takeBreakAction = QAction("Take a break", self,
                                  triggered=self.start_break)
        self.pauseAction = QAction("Pause program", self)
        self.settingsAction = QAction("Settings", self,
                                  triggered=self.settings_dialog.show)
        self.quitAction = QAction("Quit", self,
                                  triggered=self.close_app)

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

    def setIcon(self, iconName):
        icon = QIcon('img/icons/' + iconName + '.svg')
        self.trayIcon.setIcon(icon)

    def start_break(self):
        self.break_screen = break_screen.BreakWindow()

    def close_app(self):
        self.qThread.timerThread.stopEvent = True
        self.qThread.terminate()
        QApplication.instance().quit()

def start_qt_app():
    import sys
    app = QApplication(sys.argv)
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                             "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)
    
    window = Window()
    sys.exit(app.exec_())
