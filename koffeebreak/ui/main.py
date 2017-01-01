from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QDialog, QSystemTrayIcon,
                             QMessageBox, QAction, QMenu, QMainWindow)
from PyQt5.QtCore import QObject, pyqtSignal, Qt

from ui.settings import SettingsDialog
from ui.break_screen import BreakWindow

from ui.forms import main_form

from history_manager import HistoryManager

class Window(QMainWindow):
    def __init__(self, gui_connection):
        super(Window, self).__init__()
        self.ui = main_form.Ui_mainWindow()
        self.ui.setupUi(self)

        self.ui.close_pushButton.clicked.connect(self.close)
        self.ui.reset_pushButton.clicked.connect(self.reset)
        self.ui.update_pushButton.clicked.connect(self.update)
        self.ui.numberOfDays_spinBox.valueChanged.connect(self.update)

        self.gui_connection = gui_connection
        self.gui_connection.whatTime.connect(self.setTime)
        self.gui_connection.isWorkTime.connect(self.setWorkTime)
        self.gui_connection.skipBreak.connect(self.startWork)

        self.break_screen = BreakWindow(self.gui_connection)
        self.settings = SettingsDialog()

        self.createActions()
        self.createTrayIcon()

        self.changeState('work-full')
        self.setWorkTime(True)
        self.trayIcon.show()

        self.is_pause = False

        self.history = HistoryManager()

    def update(self):
        self.ui.numberOfDays_spinBox.setMaximum(self.history.get_number_of_days())
        time, short_break, long_break = self.history.get_statistic(self.ui.numberOfDays_spinBox.value())
        self.ui.allTime_lbl.setText(str(time['all']))
        self.ui.workTime_lbl.setText(str(time['work']))
        self.ui.shortBreakTime_lbl.setText(str(time['short break']))
        self.ui.longBreakTime_lbl.setText(str(time['long break']))
        self.ui.numberOfShortBreak_lbl.setText(str(short_break['count']))
        self.ui.numberOfShortBreakComp_lbl.setText(str(short_break['at the computer']))
        self.ui.numberOfPostponedShortBreaks_lbl.setText(str(short_break['postponed']))
        self.ui.numberOfSkippededShortBreaks_lbl.setText(str(short_break['skipped']))
        self.ui.numberOfLongBreak_lbl.setText(str(long_break['count']))
        self.ui.numberOfLongBreakComp_lbl.setText(str(long_break['at the computer']))
        self.ui.numberOfPostponedLongBreaks_lbl.setText(str(long_break['postponed']))
        self.ui.numberOfSkippededLongBreaks_lbl.setText(str(long_break['skipped']))

    def showWindow(self):
        self.update()
        self.show()

    def reset(self):
        self.history.reset()
        self.update()

    def createActions(self):
        self.openAction = QAction(QIcon().fromTheme('document-open'),
                                  "Open", self,
                                  triggered=self.showWindow)
        self.takeBreakAction = QAction(QIcon().fromTheme("koffeebreak-break-full"),
                                       "Take a break", self,
                                       triggered=self.startBreak)
        self.showBreakScreenAction = QAction("Show break screen", self,
                                             triggered=self.showBreakScreen,
                                             visible = False)
        self.postponeBreakAction = QAction("Postpone break", self,
                                           triggered=self.postponeBreak,
                                           visible = False)
        self.skipBreakAction = QAction("Skip break", self,
                                       triggered=self.skipBreak,
                                       visible = False)
        self.pauseOrResumeAction = QAction(QIcon().fromTheme('media-playback-pause'),
                                           "Pause program",self,
                                           triggered=self.pauseOrResumeProgram)
        self.settingsAction = QAction(QIcon().fromTheme('configure'),
                                      "Settings", self,
                                      triggered=self.settings.show)
        self.quitAction = QAction(QIcon().fromTheme('application-exit'),
                                  "Quit", self, triggered=self.closeApp)

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
        self.trayIcon.activated.connect(self.showWindow)

    def setTrayIcon(self, iconName):
        icon = QIcon().fromTheme('koffeebreak-' + iconName)
        self.trayIcon.setIcon(icon)

    def showBreakScreen(self):
        self.break_screen.showFullScreen()

    def startBreak(self):
        self.gui_connection.startBreak.emit()
        self.setWorkTime(False)

    def startWork(self):
        self.setWorkTime(True)

    def setWorkTime(self, state):
        self.is_work_time = state

        if state == True:
            self.takeBreakAction.setVisible(True)
            self.setBreakAction(False)
            try:
                self.break_screen.close()
            except:
                pass
        else:
            self.takeBreakAction.setVisible(False)
            self.setBreakAction(True)
            if not self.break_screen.isVisible():
                self.showBreakScreen()

    def postponeBreak(self):
        self.gui_connection.postponeBreak.emit()

    def skipBreak(self):
        self.gui_connection.skipBreak.emit()

    def setBreakAction(self, visible):
        self.postponeBreakAction.setVisible(visible)
        self.skipBreakAction.setVisible(visible)
        self.showBreakScreenAction.setVisible(visible)

    def changeState(self, state):
        self.previous_state = state
        self.setTrayIcon(self.previous_state)
        self.break_screen.changeState(self.previous_state)
        # print(state)
        # if state == "break-1-4":
        #     pass
        # elif state == "break-2-4":
        #     pass
        # elif state == "break-3-4":
        #     pass
        # elif state == "break-full":
        #     pass
        #     # self.takeBreakAction.setVisible(False)
        #     # self.setBreakAction(True)
        #     # if not self.break_screen.isVisible():
        #     #     self.showBreakScreen()
        # elif state == "work-1-8":
        #     pass
        # elif state == "work-2-8":
        #     pass
        # elif state == "work-3-8":
        #     pass
        # elif state == "work-4-8":
        #     pass
        # elif state == "work-5-8":
        #     pass
        # elif state == "work-6-8":
        #     pass
        # elif state == "work-7-8":
        #     pass
        # elif state == "work-full":
        #     # self.takeBreakAction.setVisible(True)
        #     # self.setBreakAction(False)
        #     # try:
        #     #     self.break_screen.close()
        #     # except:
        #     #     pass
        #     pass

    def setToolTip(self, time):
        if self.left_time == 60 and self.previous_state.startswith('work'):
            if self.trayIcon.isVisible():
                self.trayIcon.showMessage('KoffeeBreak', 'One minute left to break')
        elif self.left_time == 60 and self.previous_state.startswith('break') and not self.break_screen.isVisible():
            if self.trayIcon.isVisible():
                self.trayIcon.showMessage('KoffeeBreak', 'One minute left to work')

        self.trayIcon.setToolTip('Left: %02d:%02d' % (divmod(self.left_time, 60)))

    def setTime(self, left_time, all_time):
        self.left_time = left_time
        self.all_time = all_time

        self.setToolTip(self.left_time)

        percent = self.left_time/self.all_time * 100

        if self.is_pause:
            if not self.previous_state.endswith('-pause'):
                self.currentstate += '-pause'
        elif self.is_work_time:
            if percent <= 100 and percent > 87.5:
                self.current_state = 'work-full'
            elif percent <= 87.5 and percent > 75:
                self.current_state = 'work-7-8'
            elif percent <= 75 and percent > 62.5:
                self.current_state = 'work-6-8'
            elif percent <= 62.5 and percent > 50:
                self.current_state = 'work-5-8'
            elif percent <= 50 and percent > 37.5:
                self.current_state = 'work-4-8'
            elif percent <= 37.5 and percent > 25:
                self.current_state = 'work-3-8'
            elif percent <= 25 and percent > 12.5:
                self.current_state = 'work-2-8'
            elif percent <= 12.5 and percent >= 0:
                self.current_state = 'work-1-8'
        else:
            if percent <= 100 and percent > 75:
                self.current_state = 'break-full'
            elif percent <= 75 and percent > 50:
                self.current_state = 'break-3-4'
            elif percent <= 50 and percent > 25:
                self.current_state = 'break-2-4'
            elif percent <= 25 and percent >= 0:
                self.current_state = 'break-1-4'

        if self.current_state != self.previous_state:
            self.changeState(self.current_state)

    def pauseOrResumeProgram(self):
        self.gui_connection.pauseOrResumeTimer.emit()
        if self.is_pause:
            self.pauseOrResumeAction.setIcon(QIcon().fromTheme('media-playback-pause'))
            self.pauseOrResumeAction.setText('Pause program')
            self.is_pause = False
            self.takeBreakAction.setVisible(True)
            if self.previous_state.startswith('break'):
                self.setBreakAction(True)
        else:
            self.pauseOrResumeAction.setIcon(QIcon().fromTheme('media-playback-start'))
            self.pauseOrResumeAction.setText('Resume program')
            self.is_pause = True
            self.takeBreakAction.setVisible(False)
            if self.previous_state.startswith('break'):
                self.setBreakAction(False)

    def closeApp(self):
        self.gui_connection.closeApp.emit()
        #QApplication.instance().quit()
