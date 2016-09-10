import asyncio
from timer import timer
import settings

def start_qt_app():
    import sys
    from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox
    from quamash import QEventLoop
    from ui.main import Window
    app = QApplication(sys.argv)
    
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                             "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)
    
    state = 'work-full'
    
    window = Window()
    
    configDict = settings.read()
    
    with loop:
        loop.run_until_complete(timer(loop, int(configDict['TIME']['short_work']), configDict, state))

if __name__ == "__main__":
    start_qt_app()
