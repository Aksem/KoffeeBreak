import asyncio
from timer import timer

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
    
    window = Window()
    with loop:
        loop.run_until_complete(timer(loop, 300))

start_qt_app()
