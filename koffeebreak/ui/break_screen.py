from subprocess import Popen, PIPE

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from ui.forms import break_screen_form

class BreakWindow(QWidget):
    def __init__(self, gui_connection):
        super(BreakWindow, self).__init__()
        self.ui = break_screen_form.Ui_mainWidget()
        self.ui.setupUi(self)

        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setParent(None)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.gui_connection = gui_connection
        self.gui_connection.whatTime.connect(self.setTime)
        self.gui_connection.changeState.connect(self.changeState)

        self.ui.lockScreen_pushButton.clicked.connect(self.lockScreen)
        self.ui.breakComp_pushButton.clicked.connect(self.breakComp)
        self.ui.skipBreak_pushButton.clicked.connect(self.skipBreak)
        self.ui.postponeBreak_pushButton.clicked.connect(self.postponeBreak)

    def changeState(self, state):
        pixmap = QIcon().fromTheme('koffeebreak-' + state).pixmap(self.ui.icon_label.height())
        self.ui.icon_label.setPixmap(pixmap)

    def lockScreen(self):
        self.gui_connection.lockScreen.emit()
        # Popen with stdout for logs in future
        with Popen(['qdbus', 'org.freedesktop.ScreenSaver', '/ScreenSaver',
                    'Lock'], stdout=PIPE, universal_newlines=True) as proc:
            self.close()

    def breakComp(self):
        self.gui_connection.breakComp.emit()
        self.close()

    def setTime(self, time):
        self.ui.leftTime_label.setText('%02d:%02d' % (divmod(time, 60)))

    def skipBreak(self):
        self.gui_connection.skipBreak.emit()
        self.close()

    def postponeBreak(self):
        self.gui_connection.postponeBreak.emit()
        self.close()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = BreakWindow()
    sys.exit(app.exec_())
