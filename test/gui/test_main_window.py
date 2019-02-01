from unittest.mock import MagicMock

import pytest

from echoes_menu_mod_gui.gui.main_window import MainWindow

pexpect = pytest.importorskip("pytestqt")


@pytest.fixture(name="default_main_window")
def _default_main_window() -> MainWindow:
    return MainWindow()


def test_drop_iso_event(default_main_window: MainWindow,
                        qtbot,
                        ):
    # Setup
    event = MagicMock()
    urls = [MagicMock(), MagicMock()]
    urls[0].toLocalFile.return_value = "directory/games/seed.json"
    urls[1].toLocalFile.return_value = "directory/games/game.iso"
    event.mimeData.return_value.urls.return_value = urls

    # Run
    default_main_window.dropEvent(event)

    # Assert
    assert default_main_window.input_iso_edit.text() == "directory/games/game.iso"


def test_drop_random_event(default_main_window: MainWindow,
                           qtbot,
                           ):
    # Setup
    event = MagicMock()
    urls = [MagicMock(), MagicMock()]
    urls[0].toLocalFile.return_value = "directory/games/seed.json"
    urls[1].toLocalFile.return_value = "directory/games/game.png"
    event.mimeData.return_value.urls.return_value = []

    # Run
    default_main_window.dropEvent(event)

    # Assert
    assert default_main_window.input_iso_edit.text() == ""
