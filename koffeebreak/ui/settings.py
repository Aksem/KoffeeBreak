from PyQt5.QtWidgets import QDialog
from ui.forms import settings_form
import settings as settings_file

class SettingsDialog(QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()
        self.ui = settings_form.Ui_Dialog()
        self.ui.setupUi(self)
        self.load_settings()
        
        ##conections
        self.ui.closePushButton.clicked.connect(self.close)
        self.ui.savePushButton.clicked.connect(self.save_settings)
        self.ui.DefaultPushButton.clicked.connect(self.return_to_default)

    def load_settings(self):
        self.settings = settings_file.read()

        self.ui.shortBreakSpinBox.setValue(
            int(self.settings['TIME']['short_break']))
        self.ui.shortWorkSpinBox.setValue(
            int(self.settings['TIME']['work_time']))
        self.ui.longBreakSpinBox.setValue(
            int(self.settings['TIME']['long_break']))
        self.ui.shortsBreaksSpinBox.setValue(
            int(self.settings['TIME']['shorts_before_long']))
    
    def save_settings(self):
        self.settings['TIME']['short_break'] = str(self.ui.shortBreakSpinBox.value())
        self.settings['TIME']['short_work'] = str(self.ui.shortWorkSpinBox.value())
        self.settings['TIME']['long_break'] = str(self.ui.longBreakSpinBox.value())
        self.settings['TIME']['shorts_before_long'] = str(
            self.ui.shortsBreaksSpinBox.value())
        settings_file.write(self.settings)
        self.ui.statusLabel.setText('Saved successfully.')

    def return_to_default(self):
        settings_file.set_default(self.settings)
        self.load_settings()
