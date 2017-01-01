from PyQt5.QtWidgets import QDialog, QMessageBox, QStyle
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt
from ui.forms import settings_form
import settings as settings_file

class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.ui = settings_form.Ui_Dialog()
        self.ui.setupUi(self)
        self.load_settings()

        #conections
        self.ui.closePushButton.clicked.connect(self.close)
        self.ui.savePushButton.clicked.connect(self.save_settings)
        self.ui.defaultPushButton.clicked.connect(self.return_to_default)

        #self.setAttribute(Qt.WA_DeleteOnClose)

        self.is_saved = True

        self.ui.workTimeSpinBox.valueChanged.connect(self.value_changed)
        self.ui.timeOfShortBreakSpinBox.valueChanged.connect(self.value_changed)
        self.ui.timeOfLongBreakSpinBox.valueChanged.connect(self.value_changed)
        self.ui.workTimeWhenPostponeBreakSpinBox.valueChanged.connect(self.value_changed)
        self.ui.numberOfShortsBreaksSpinBox.valueChanged.connect(self.value_changed)

    def load_settings(self):
        self.settings = settings_file.read()

        self.ui.workTimeSpinBox.setValue(
            int(self.settings['TIME']['work_time']) / 60)
        self.ui.timeOfShortBreakSpinBox.setValue(
            int(self.settings['TIME']['time_of_short_break']) / 60)
        self.ui.timeOfLongBreakSpinBox.setValue(
            int(self.settings['TIME']['time_of_long_break']) / 60)
        self.ui.workTimeWhenPostponeBreakSpinBox.setValue(
            int(self.settings['TIME']['work_time_when_postpone_break']) / 60)
        self.ui.numberOfShortsBreaksSpinBox.setValue(
            int(self.settings['BREAKS']['number_of_short_breaks']))

    def save_settings(self):
        self.settings['TIME']['time_of_short_break'] = str(self.ui.timeOfShortBreakSpinBox.value())
        self.settings['TIME']['time_of_long_break'] = str(self.ui.timeOfLongBreakSpinBox.value())
        self.settings['TIME']['work_time'] = str(self.ui.workTimeSpinBox.value())
        self.settings['TIME']['work_time_when_postpone_break'] = str(
                        self.ui.numberOfShortsBreaksSpinBox.value())
        self.settings['BREAKS']['number_of_short_breaks'] = str(
                        self.ui.numberOfShortsBreaksSpinBox.value())
        settings_file.write(self.settings)
        self.ui.statusLabel.setText('To apply changes, please, restart application')
        self.is_saved = True
        timer = QTimer()
        timer.singleShot(2000, self.clearStatus)

    def clearStatus(self):
        self.ui.statusLabel.clear()

    def return_to_default(self):
        settings_file.set_default()
        self.load_settings()
        self.ui.statusLabel.clear()

    def value_changed(self):
        self.is_saved = False

    def closeEvent(self, event):
        if self.is_saved:
            event.accept()
        else:
            popup = QMessageBox(self)
            popup.setIcon(QMessageBox.Warning)
            popup.setText('The settings have been changed')
            popup.setInformativeText('Do you want to save the changes or discard them?')
            popup.setStandardButtons(QMessageBox.Save |
                                     QMessageBox.Discard |
                                     QMessageBox.Cancel)

            popup.setDefaultButton(QMessageBox.Save)
            answer = popup.exec_()
            if answer == QMessageBox.Save:
                self.save_settings()
                event.accept()
            elif answer == QMessageBox.Discard:
                self.load_settings()
                self.is_saved = True
                event.accept()
            elif answer == QMessageBox.Cancel:
                event.ignore()
