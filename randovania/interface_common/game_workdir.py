from pathlib import Path


def validate_game_files_path(game_files_path: Path):
    if not game_files_path.is_dir():
        raise ValueError("Not a directory")

    required_files = ["default.dol", "FrontEnd.pak", "Metroid1.pak", "Metroid2.pak"]
    missing_files = [(game_files_path / required_file).is_file()
                     for required_file in required_files]

    if not all(missing_files):
        raise ValueError("Is not a valid game folder. Missing files: {}".format([
            filename for filename, exists in zip(required_files, missing_files)
            if not exists
        ]))
