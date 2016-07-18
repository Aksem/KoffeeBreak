from PyQt5.QtWidgets import QDialog, QWidget
from PyQt5.QtCore import Qt
from ui.forms import break_screen_form
#from forms import break_screen_form

class BreakWindow(QWidget):
    def __init__(self):
        super(BreakWindow, self).__init__()
        self.ui = break_screen_form.Ui_mainWidget()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setParent(None)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = BreakWindow()
    sys.exit(app.exec_())
