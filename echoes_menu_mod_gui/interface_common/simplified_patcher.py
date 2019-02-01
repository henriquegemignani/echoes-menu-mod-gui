import shutil
from pathlib import Path
from typing import List

from echoes_menu_mod_gui import get_data_path
from echoes_menu_mod_gui.games.prime import iso_packager, claris_menu_mod
from echoes_menu_mod_gui.games.prime.banner_patcher import patch_game_name_and_id
from echoes_menu_mod_gui.interface_common import status_update_lib
from echoes_menu_mod_gui.interface_common.status_update_lib import ProgressUpdateCallable


def find_game_files_path():
    return get_data_path().joinpath("extracted_game")


def unpack_iso(input_iso: Path,
               progress_update: ProgressUpdateCallable,
               ):
    """
    Unpacks the given ISO to the files listed in options
    :param input_iso:
    :param progress_update:
    :return:
    """
    game_files_path = find_game_files_path()
    if game_files_path.exists():
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
    claris_menu_mod.add_menu_mod_to_files(game_root=game_files_path,
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


def patch_iso(progress_update: ProgressUpdateCallable,
              input_iso: Path,
              output_iso: Path,
              ):
    game_files_path = find_game_files_path()
    updaters = status_update_lib.split_progress_update(
        progress_update,
        3
    )

    # Unpack ISO
    unpack_iso(input_iso=input_iso,
               progress_update=updaters[0])

    # Patch ISO
    apply_menu_mod(progress_update=updaters[1])

    # Change Title
    patch_game_name_and_id(game_files_path, "Metroid Prime 2: Menu Mod")

    # Pack ISO
    pack_iso(output_iso=output_iso,
             progress_update=updaters[2])

    shutil.rmtree(game_files_path)
