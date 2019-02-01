import os
from typing import Optional

from PySide2.QtCore import QUrl, Signal
from PySide2.QtGui import QDesktopServices
from PySide2.QtWidgets import QMainWindow, QAction, QFileDialog

from randovania import VERSION
from randovania.gui import common_qt_lib
from randovania.gui.background_task_mixin import BackgroundTaskMixin
from randovania.gui.common_qt_lib import set_default_window_icon
from randovania.gui.mainwindow_ui import Ui_MainWindow
from randovania.interface_common.update_checker import get_latest_version


class MainWindow(QMainWindow, Ui_MainWindow, BackgroundTaskMixin):
    newer_version_signal = Signal(str, str)
    options_changed_signal = Signal()
    is_preview_mode: bool = False

    menu_new_version: Optional[QAction] = None
    _current_version_url: Optional[str] = None

    @property
    def _tab_widget(self):
        return self.tabWidget

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Echoes Menu Mod GUI {}".format(VERSION))
        self.setAcceptDrops(True)
        set_default_window_icon(self)

        # Buttons
        self.select_input_iso_button.clicked.connect(self._prompt_input_iso)
        self.select_output_iso_button.clicked.connect(self._prompt_output_iso)
        self.apply_mod_button.clicked.connect(self._apply_menu_mod)

        # Signals
        self.newer_version_signal.connect(self.display_new_version)
        self.background_tasks_button_lock_signal.connect(self.enable_buttons_with_background_tasks)
        self.progress_update_signal.connect(self.update_progress)
        self.stop_background_process_button.clicked.connect(self.stop_background_process)

        get_latest_version(self.newer_version_signal.emit)

    def closeEvent(self, event):
        self.stop_background_process()
        super().closeEvent(event)

    def dragEnterEvent(self, event):
        for url in event.mimeData().urls():
            if os.path.splitext(url.toLocalFile())[1] == ".iso":
                event.acceptProposedAction()
                return

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            iso_path = url.toLocalFile()
            if os.path.splitext(iso_path)[1] == ".iso":
                self.input_iso_edit.setText(iso_path)
                return

    def display_new_version(self, new_version: str, new_version_url: str):
        if self.menu_new_version is None:
            self.menu_new_version = QAction("", self)
            self.menu_new_version.triggered.connect(self.open_version_link)
            self.menu_bar.addAction(self.menu_new_version)

        self.menu_new_version.setText("New version available: {}".format(new_version))
        self._current_version_url = new_version_url

    def open_version_link(self):
        if self._current_version_url is None:
            raise RuntimeError("Called open_version_link, but _current_version_url is None")

        QDesktopServices.openUrl(QUrl(self._current_version_url))

    # ISO

    def _prompt_input_iso(self):
        input_iso = common_qt_lib.prompt_user_for_input_iso(self)
        if input_iso is not None:
            self.input_iso_edit.setText(str(input_iso))
            if self.output_iso_edit.text() == "":
                self.output_iso_edit.setText(str(input_iso.parent.joinpath("Echoes Menu Mod.iso")))

    def _prompt_output_iso(self):
        open_result = QFileDialog.getSaveFileName(self, caption="Select the path for the Menu Mod ISO.", filter="*.iso")
        if not open_result or open_result == ("", ""):
            return

        self.output_iso_edit.setText(open_result[0])

    def _apply_menu_mod(self):
        pass

    # Background Process

    def enable_buttons_with_background_tasks(self, value: bool):
        self.stop_background_process_button.setEnabled(not value)

    def update_progress(self, message: str, percentage: int):
        self.progress_label.setText(message)
        if "Aborted" in message:
            percentage = 0
        if percentage >= 0:
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(percentage)
        else:
            self.progress_bar.setRange(0, 0)
