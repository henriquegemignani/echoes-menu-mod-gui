import shutil
from pathlib import Path
from typing import List

from randovania import get_data_path
from randovania.games.prime import iso_packager, claris_randomizer
from randovania.interface_common import status_update_lib
from randovania.interface_common.status_update_lib import ProgressUpdateCallable


def find_game_files_path():
    return get_data_path().joinpath("extracted_game")


def unpack_iso(input_iso: Path,
               progress_update: ProgressUpdateCallable,
               ):
    """
    Unpacks the given ISO to the files listed in options
    :param input_iso:
    :param options:
    :param progress_update:
    :return:
    """
    game_files_path = find_game_files_path()
    shutil.rmtree(game_files_path)

    iso_packager.unpack_iso(
        iso=input_iso,
        game_files_path=game_files_path,
        progress_update=progress_update,
    )


def apply_menu_mod(progress_update: ProgressUpdateCallable):
    """
    Applies the given LayoutDescription to the files listed in options
    :param progress_update:
    :return:
    """
    game_files_path = find_game_files_path()

    status_update = status_update_lib.create_progress_update_from_successive_messages(progress_update, 400)
    claris_randomizer.add_menu_mod_to_files(game_root=game_files_path,
                                            status_update=status_update)


def pack_iso(output_iso: Path,
             progress_update: ProgressUpdateCallable,
             ):
    """
    Unpacks the files listed in options to the given path
    :param output_iso:
    :param progress_update:
    :return:
    """
    game_files_path = find_game_files_path()

    iso_packager.pack_iso(
        iso=output_iso,
        game_files_path=game_files_path,
        disable_attract_if_necessary=True,
        progress_update=progress_update,
    )


def patch_iso(updaters: List[ProgressUpdateCallable],
              input_iso: Path,
              output_iso: Path,
              ):

    # Unpack ISO
    unpack_iso(input_iso=input_iso,
               progress_update=updaters[0])

    # Patch ISO
    apply_menu_mod(progress_update=updaters[1])

    # Pack ISO
    pack_iso(output_iso=output_iso,
             progress_update=updaters[2])

    shutil.rmtree(find_game_files_path())
