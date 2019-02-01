import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, call, ANY

import pytest

from randovania.games.prime import claris_menu_mod


class CustomException(Exception):
    @classmethod
    def do_raise(cls, x):
        raise CustomException("test exception")


@patch("subprocess.Popen", autospec=True)
def test_run_with_args_success(mock_popen: MagicMock,
                               ):
    # Setup
    args = [MagicMock(), MagicMock()]
    finish_string = "We are done!"
    status_update = MagicMock()
    process = mock_popen.return_value.__enter__.return_value
    process.stdout = [
        " line 1",
        "line 2 ",
        "   ",
        finish_string,
        " post line "
    ]

    # Run
    claris_menu_mod._run_with_args(args, finish_string, status_update)

    # Assert
    mock_popen.assert_called_once_with(
        [str(x) for x in args],
        stdout=subprocess.PIPE, bufsize=0, universal_newlines=True
    )
    status_update.assert_has_calls([
        call("line 1"),
        call("line 2"),
        call(finish_string),
    ])
    process.kill.assert_not_called()


@patch("subprocess.Popen", autospec=True)
def test_run_with_args_failure(mock_popen: MagicMock,
                               ):
    # Setup
    finish_string = "We are done!"
    process = mock_popen.return_value.__enter__.return_value
    process.stdout = [" line 1"]

    # Run
    with pytest.raises(CustomException):
        claris_menu_mod._run_with_args([], finish_string, CustomException.do_raise)

    # Assert
    mock_popen.assert_called_once_with([], stdout=subprocess.PIPE, bufsize=0, universal_newlines=True)
    process.kill.assert_called_once_with()


@patch("randovania.games.prime.claris_menu_mod._run_with_args", autospec=True)
@patch("randovania.games.prime.claris_menu_mod._get_menu_mod_path", autospec=True)
def test_add_menu_mod_to_files(mock_get_data_path: MagicMock,
                               mock_run_with_args: MagicMock,
                               tmpdir,
                               ):
    # Setup
    mock_get_data_path.return_value = Path("EchoesMenu.exe")
    game_root = Path(tmpdir.join("root"))
    status_update = MagicMock()
    game_root.joinpath("files").mkdir(parents=True)

    # Run
    claris_menu_mod.add_menu_mod_to_files(game_root, status_update)

    # Assert
    mock_run_with_args.assert_called_once_with(
        [Path("EchoesMenu.exe"),
         game_root.joinpath("files")],
        "Done!",
        status_update
    )


@patch("randovania.games.prime.claris_menu_mod._get_menu_mod_folder", autospec=True)
@patch("subprocess.Popen", autospec=True)
def test_disable_echoes_attract_videos_success(mock_popen: MagicMock,
                                               _get_menu_mod_folder: MagicMock,
                                               ):
    # Setup
    _get_menu_mod_folder.return_value = Path("randomizer_folder")
    game_root = Path("game_folder")
    status_update = MagicMock()

    process = mock_popen.return_value.__enter__.return_value
    process.stdout = [
        " line 1",
        "line 2 ",
        "   ",
        " line 3 "
    ]

    # Run
    claris_menu_mod.disable_echoes_attract_videos(game_root, status_update)

    # Assert
    _get_menu_mod_folder.assert_called_once_with()
    mock_popen.assert_called_once_with(
        [str(Path("randomizer_folder", "DisableEchoesAttractVideos.exe")),
         str(Path("game_folder", "files"))],
        stdout=subprocess.PIPE, bufsize=0, universal_newlines=True
    )
    status_update.assert_has_calls([
        call("line 1"),
        call("line 2"),
        call(""),
        call("line 3"),
    ])
    process.kill.assert_not_called()


@patch("randovania.games.prime.claris_menu_mod._get_menu_mod_folder", autospec=True)
@patch("subprocess.Popen", autospec=True)
def test_disable_echoes_attract_videos_failure(mock_popen: MagicMock,
                                               _get_menu_mod_folder: MagicMock,
                                               ):
    # Setup
    game_root = MagicMock()
    status_update = MagicMock(side_effect=CustomException.do_raise)
    process = mock_popen.return_value.__enter__.return_value
    process.stdout = [
        " line 1",
    ]

    # Run
    with pytest.raises(CustomException):
        claris_menu_mod.disable_echoes_attract_videos(game_root, status_update)

    # Assert
    _get_menu_mod_folder.assert_called_once_with()
    mock_popen.assert_called_once_with(ANY, stdout=subprocess.PIPE, bufsize=0, universal_newlines=True)
    status_update.assert_called_once_with("line 1")
    process.kill.assert_called_once_with()
