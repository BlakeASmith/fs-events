"""Expose file system events as generators"""
from inotify.adapters import Inotify
from inotify.constants import IN_CLOSE_WRITE
from pathlib import Path
from itertools import groupby
from fsevents.config import *

def writes(*abs_paths):
    """a generator for file write events

    Args:
        *abs_paths (pathlib.Path): the paths the monitored files.

    Yields:
         :pathlib.Path: The absolute path of each file which has been written to

    """

    # group files by the directory they are in
    files = {str(dir):[p.name for p in list(paths)] for dir, paths
            in groupby(sorted(abs_paths), lambda p: p.parent)}

    # it is easier to watch the directory containing the file as often
    # when files are changed they are deleted and recreated or moved
    i = Inotify()
    for dir in files.keys(): i.add_watch(path_unicode=dir, mask = IN_CLOSE_WRITE)

    yield from (Path(dir, name)
            for (_, types, dir, name)
            in i.event_gen(yield_nones=False)
            if name in files[dir] and 'IN_ISDIR' not in types)

