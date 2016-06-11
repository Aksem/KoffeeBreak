from PyQt5.QtWidgets import QDialog
#from ui.forms import break_screen_form
from forms import break_screen_form

class BreakWindow(QDialog):
    def __init__(self):
        super(BreakWindow, self).__init__()
        self.ui = break_screen_form.Ui_Form()
        self.ui.setupUi(self)
        self.showFullScreen()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    win = BreakWindow()
    sys.exit(app.exec_())
