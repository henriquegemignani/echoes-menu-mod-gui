import subprocess
from pathlib import Path
from typing import Callable, List, Union

from echoes_menu_mod_gui import get_data_path

_USELESS_PICKUP_NAME = "Energy Transfer Module"


def _get_menu_mod_folder() -> Path:
    return get_data_path().joinpath("ClarisEchoesMenu")


def _get_menu_mod_path() -> Path:
    return _get_menu_mod_folder().joinpath("EchoesMenu.exe")


def _run_with_args(args: List[Union[str, Path]],
                   finish_string: str,
                   status_update: Callable[[str], None]):
    finished_updates = False

    new_args = [str(arg) for arg in args]
    print("Invoking external tool with: ", new_args)
    with subprocess.Popen(new_args, stdout=subprocess.PIPE, bufsize=0, universal_newlines=True) as process:
        try:
            for line in process.stdout:
                x = line.strip()
                if x:
                    print(x)
                    if not finished_updates:
                        status_update(x)
                        finished_updates = x == finish_string
        except Exception:
            process.kill()
            raise
    if not finished_updates:
        raise RuntimeError("External tool did not send '{}'. Did something happen?".format(finish_string))


def add_menu_mod_to_files(
        game_root: Path,
        status_update: Callable[[str], None],
):
    files_folder = game_root.joinpath("files")
    _run_with_args(
        [
            _get_menu_mod_path(),
            files_folder
        ],
        "Done!",
        status_update
    )


def disable_echoes_attract_videos(game_root: Path,
                                  status_update: Callable[[str], None],
                                  ):
    game_files = game_root.joinpath("files")
    args = [
        str(_get_menu_mod_folder().joinpath("DisableEchoesAttractVideos.exe")),
        str(game_files)
    ]
    with subprocess.Popen(args, stdout=subprocess.PIPE, bufsize=0, universal_newlines=True) as process:
        try:
            for line in process.stdout:
                x = line.strip()
                status_update(x)
        except Exception:
            process.kill()
            raise
