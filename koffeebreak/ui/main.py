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
        self.gui_connection.whatTime.connect(self.setTime)

        #init settings dialog
        self.settings_dialog = settings.SettingsDialog()
        self.break_screen = break_screen.BreakWindow(self.gui_connection)
        self.is_pause = False

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
        self.pauseOrResumeAction = QAction(QIcon().fromTheme('media-playback-pause'),
                                  "Pause program",self,
                                  triggered=self.pauseOrResumeProgram)
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
        self.trayIconMenu.addAction(self.pauseOrResumeAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setToolTip('KoffeeBreak')
        self.trayIcon.activated.connect(self.showTime)

    def showTime(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            print(QSystemTrayIcon.Trigger)
            self.trayIcon.showMessage('KoffeeBreak','Left: %02d:%02d' % (divmod(self.time, 60)), QSystemTrayIcon.NoIcon)

    def setTrayIcon(self, iconName):
        icon = QIcon().fromTheme('koffeebreak-' + iconName)
        self.trayIcon.setIcon(icon)

    def start_break(self):
        self.gui_connection.startBreak.emit()
        self.break_screen.showFullScreen()

    def changeState(self, state):
        self.current_state = state
        self.setTrayIcon(state)
        if state == "break-1-4":
            pass
        elif state == "break-2-4":
            pass
        elif state == "break-3-4":
            pass
        elif state == "break-full":
            if (not self.break_screen.isVisible()):
                self.break_screen.showFullScreen()
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
            try:
                self.break_screen.close()
            except:
                pass

    def setTime(self, time):
        self.time = time
        if self.time == 60 and self.current_state.startswith('work'):
            if self.trayIcon.isVisible():
                self.trayIcon.showMessage('KoffeeBreak', 'One minute left to break')
        elif self.time == 60 and self.current_state.startswith('break') and not self.break_screen.isVisible():
            if self.trayIcon.isVisible():
                self.trayIcon.showMessage('KoffeeBreak', 'One minute left to work')

    def pauseOrResumeProgram(self):
        self.gui_connection.pauseOrResumeTimer.emit()
        if self.is_pause:
            self.pauseOrResumeAction.setIcon(QIcon().fromTheme('media-playback-pause'))
            self.pauseOrResumeAction.setText('Pause program')
            self.is_pause = False
        else:
            self.pauseOrResumeAction.setIcon(QIcon().fromTheme('media-playback-start'))
            self.pauseOrResumeAction.setText('Resume program')
            self.is_pause = True

    def close_app(self):
        self.gui_connection.closeApp.emit()
        #QApplication.instance().quit()
