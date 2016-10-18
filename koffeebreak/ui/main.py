from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QSystemTrayIcon,
                             QMessageBox, QAction, QMenu, QMainWindow)
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QTimer

from ui import settings, break_screen

from ui.forms import main_form

from statistic_manager import StatisticManager
from datetime import timedelta, datetime

class Window(QMainWindow):
    def __init__(self, gui_connection):
        super(Window, self).__init__()
        self.ui = main_form.Ui_mainWindow()
        self.ui.setupUi(self)

        self.ui.close_pushButton.clicked.connect(self.close)
        self.ui.reset_pushButton.clicked.connect(self.reset)

        self.gui_connection = gui_connection
        self.gui_connection.changeState.connect(self.changeState)
        self.gui_connection.whatTime.connect(self.setTime)
        self.gui_connection.updateHistory.connect(self.update)

        #init settings dialog
        self.settings_dialog = settings.SettingsDialog()
        #init break screen
        self.break_screen = break_screen.BreakWindow(self.gui_connection)

        self.createActions()
        self.createTrayIcon()
        self.setTrayIcon('work-full')
        self.trayIcon.show()

        self.is_pause = False

        self.statistic_file = StatisticManager()
        self.init_timer()

    def createActions(self):
        self.openAction = QAction(QIcon().fromTheme('document-open'),
                                  "Open", self,
                                  triggered=self.show_window)
        self.takeBreakAction = QAction(QIcon().fromTheme("koffeebreak-break-full"),
                                  "Take a break", self,
                                  triggered=self.start_break)
        self.showBreakScreenAction = QAction("Show break screen", self,
                                  triggered=self.show_break_screen, visible = False)
        self.postponeBreakAction = QAction("Postpone break", self,
                                  triggered=self.postpone_break, visible = False)
        self.skipBreakAction = QAction("Skip break", self,
                                  triggered=self.skip_break, visible = False)
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
        self.trayIconMenu.addAction(self.showBreakScreenAction)
        self.trayIconMenu.addAction(self.postponeBreakAction)
        self.trayIconMenu.addAction(self.skipBreakAction)
        self.trayIconMenu.addAction(self.takeBreakAction)
        self.trayIconMenu.addAction(self.pauseOrResumeAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def showTime(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            print(QSystemTrayIcon.Trigger)
            self.trayIcon.showMessage('KoffeeBreak','Left: %02d:%02d' % (divmod(self.time, 60)), QSystemTrayIcon.NoIcon)

    def setTrayIcon(self, iconName):
        icon = QIcon().fromTheme('koffeebreak-' + iconName)
        self.trayIcon.setIcon(icon)

    def update_labels(self):
        self.statistic_time, short_break, long_break = self.statistic_file.return_statistic()
        self.ui.allTime_lbl.setText(str(self.statistic_time[0]))
        self.ui.workTime_lbl.setText(str(self.statistic_time[1]))
        self.ui.shortBreakTime_lbl.setText(str(self.statistic_time[2]))
        self.ui.longBreakTime_lbl.setText(str(self.statistic_time[3]))
        self.ui.numberOfShortBreak_lbl.setText(str(short_break[0]))
        self.ui.numberOfShortBreakComp_lbl.setText(str(short_break[1]))
        self.ui.numberOfPostponedShortBreaks_lbl.setText(str(short_break[2]))
        self.ui.numberOfSkippededShortBreaks_lbl.setText(str(short_break[3]))
        self.ui.numberOfLongBreak_lbl.setText(str(long_break[0]))
        self.ui.numberOfLongBreak_lbl.setText(str(long_break[1]))
        self.ui.numberOfPostponedLongBreaks_lbl.setText(str(long_break[2]))
        self.ui.numberOfSkippededLongBreaks_lbl.setText(str(long_break[3]))

    def update(self):
        if self.isVisible():
            self.statistic_file.reload()
            self.state = self.statistic_file.current_state()
            self.update_labels()

    def init_timer(self):
        self.timeTimer = QTimer()
        self.timeTimer.setInterval(1000)
        self.timeTimer.timeout.connect(self.updateTime)

    def show_window(self):
        self.statistic_file.read_history()
        self.update_labels()
        self.state = self.statistic_file.current_state()
        timer = self.statistic_file.current_start_timer()
        delta = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') - timer
        self.updateTime(delta)
        self.show()
        self.timeTimer.start()

    def updateTime(self, delta = timedelta(seconds = 1)):
        self.state = self.statistic_file.current_state()
        self.statistic_time[0] += delta
        if self.state == 'start work':
            self.statistic_time[1] += delta
        elif self.state == 'start short break':
            self.statistic_time[2] += delta
        elif self.state == 'start short break':
            self.statistic_time[3] += delta
        self.updateTimeLabels()

    def updateTimeLabels(self):
        self.ui.allTime_lbl.setText(str(self.statistic_time[0]))
        self.ui.workTime_lbl.setText(str(self.statistic_time[1]))
        self.ui.shortBreakTime_lbl.setText(str(self.statistic_time[2]))
        self.ui.longBreakTime_lbl.setText(str(self.statistic_time[3]))

    def close(self, event):
        self.timeTimer.stop()
        self.hide()

    def reset(self):
        self.statistic_file.reset_all()
        self.statistic_file.read_history()
        self.update_labels()
        self.state = self.statistic_file.current_state()

    def show_break_screen(self):
        self.break_screen.showFullScreen()

    def start_break(self):
        if self.takeBreakAction.isVisible:
            self.gui_connection.startBreak.emit()
            self.break_screen.showFullScreen()

    def postpone_break(self):
        self.gui_connection.postponeBreak.emit()

    def skip_break(self):
        self.gui_connection.skipBreak.emit()

    def setVisibleBreakAction(self):
        self.postponeBreakAction.setVisible(True)
        self.skipBreakAction.setVisible(True)
        self.showBreakScreenAction.setVisible(True)

    def setUnvisibleBreakAction(self):
        self.postponeBreakAction.setVisible(False)
        self.skipBreakAction.setVisible(False)
        self.showBreakScreenAction.setVisible(False)

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
            self.takeBreakAction.setVisible(False)
            self.setVisibleBreakAction()
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
            self.takeBreakAction.setVisible(True)
            self.setUnvisibleBreakAction()
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
        self.trayIcon.setToolTip('Left: %02d:%02d' % (divmod(self.time, 60)))

    def pauseOrResumeProgram(self):
        self.gui_connection.pauseOrResumeTimer.emit()
        if self.is_pause:
            self.pauseOrResumeAction.setIcon(QIcon().fromTheme('media-playback-pause'))
            self.pauseOrResumeAction.setText('Pause program')
            self.is_pause = False
            self.takeBreakAction.setVisible(True)
            self.setVisibleBreakAction()
        else:
            self.pauseOrResumeAction.setIcon(QIcon().fromTheme('media-playback-start'))
            self.pauseOrResumeAction.setText('Resume program')
            self.is_pause = True
            self.takeBreakAction.setVisible(False)
            self.setUnvisibleBreakAction()


    def close_app(self):
        self.gui_connection.closeApp.emit()
        #QApplication.instance().quit()
