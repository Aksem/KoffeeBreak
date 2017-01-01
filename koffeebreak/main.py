#!/usr/bin/env python3

"""Main starting point for KoffeeBreak.  Contains the main() entry point."""

import asyncio
import argparse
import sys

from timer import timer
import settings

def start_qt_app(config):
    import sys
    from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMessageBox
    from quamash import QEventLoop
    from ui.main import Window
    from ui.qt_gui_connection import qSignal
    app = QApplication(sys.argv)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, "Systray",
                             "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)

    gui_connection = qSignal()
    window = Window(gui_connection)

    with loop:
        #asyncio.run_coroutine_threadsafe(timer(loop, config, gui_connection), loop)
        try:
            loop.run_until_complete(timer(config, gui_connection))
        except asyncio.CancelledError:
            pass

def version_callback():
    # TODO: find a way to get version from egg-info(pkg-resources don`t work :c )
    raise SystemExit

def main():
    parser = argparse.ArgumentParser(description="KoffeeBreak",
                                     epilog='Please make choice')

    parser.add_argument('-g', '--gui', default='qt', choices=['qt', 'none'],
                        help='set type of gui')
    # parser.add_argument('-v', '--version',
    #                     help="show program's version number and exit")
    args = parser.parse_args()

    config = settings.read()
    if args.gui == "none":
        config['EXECUTION']['gui'] = "none"
    elif args.gui == "qt":
        config['EXECUTION']['gui'] = "qt"

    if settings.read_parameter(config, ['EXECUTION', 'gui']) == 'qt':
        start_qt_app(config)

if __name__ == "__main__":
    main()
