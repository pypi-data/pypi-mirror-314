import shutil
from os.path import getsize
from pathlib import Path

import auto_dlp.file_locations as fs

_known_files = set()

def know_file(path: Path):
    _known_files.add(path.resolve(strict=True))


def _delete_file(path: Path, reason):
    print(f"Deleting {path} because: {reason}")

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()

# def is_known(path: Path, strict_resolve=True):
#     return path.resolve(strict=strict_resolve) in _known_files

def clean(file: Path):
    if file.resolve(strict=True) not in _known_files:
        _delete_file(file, reason="The file was not created by Auto-DLP")
        return

    if not file.is_dir():
        if getsize(file) == 0:
            _delete_file(file, reason="The file is empty")
        return

    for sub in file.iterdir():
        clean(sub)


def clean_all(config):
    for artist in config.artists:
        clean(fs.artist_dir(artist.name))
