from subprocess import Popen, PIPE

from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from ui.forms import break_screen_form

class BreakWindow(QWidget):
    def __init__(self, gui_connection):
        super(BreakWindow, self).__init__()
        self.ui = break_screen_form.Ui_mainWidget()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.setParent(None)
        #self.setAttribute(Qt.WA_NoSystemBackground)
        #self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()
        self.gui_connection = gui_connection
        
        self.ui.lockScreen_pushButton.clicked.connect(self.lockScreen)
        self.ui.breakComp_pushButton.clicked.connect(self.close)
        self.ui.skipBreak_pushButton.clicked.connect(self.skipBreak)
    
    def skipBreak(self):
        self.gui_connection.skipBreak.emit()
        self.close()
        
    def lockScreen(self):
        # Popen with stdout for logs in future
        with Popen(['qdbus', 'org.freedesktop.ScreenSaver', '/ScreenSaver',
                    'Lock'], stdout=PIPE, universal_newlines=True) as proc:
            self.close()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = BreakWindow()
    sys.exit(app.exec_())
