import sys
from argparse import ArgumentParser

from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QMessageBox

from echoes_menu_mod_gui.gui.main_window import MainWindow


def catch_exceptions(t, val, tb):
    QMessageBox.critical(None,
                         "An exception was raised",
                         "An unhandled Exception occurred:\n{}".format(val))
    old_hook(t, val, tb)


old_hook = sys.excepthook


def show_main_window(app: QApplication, args):
    main_window = MainWindow()
    app.main_window = main_window
    main_window.show()


def run(args):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)

    sys.excepthook = catch_exceptions
    show_main_window(app, args)

    sys.exit(app.exec_())


def create_subparsers(sub_parsers):
    parser: ArgumentParser = sub_parsers.add_parser(
        "gui",
        help="Run the Graphical User Interface"
    )
    parser.set_defaults(func=run)
