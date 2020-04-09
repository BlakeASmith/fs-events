"""A library for detecting changes within files"""
from inotify.adapters import Inotify
from inotify.constants import IN_CLOSE_WRITE
from pathlib import Path
from itertools import groupby
from regexutils import *
from hashutils import *
from config import *

def writes(*abs_paths):
    """a generator for file change events

    Args:
        *abs_paths: the absolute paths to all the files
            to be monitored. Strings or pathlib.Path accepted

    Yields:
         :pathlib.Path: The absolute path of each file which has been written to

    """
    files = {str(dir):[p.name for p in list(paths)] for dir, paths
            in groupby(sorted(abs_paths), lambda p: p.parent)}

    # it is easier to watch the directory containing the file as often
    # when files are changed they are deleted and recreated or moved
    i = Inotify()
    for dir in files.keys():
        i.add_watch(path_unicode=dir, mask = IN_CLOSE_WRITE)

    yield from (Path(dir, name) for (_, masks, dir, name) in i.event_gen(yield_nones=False)
            if name in files[dir] and 'IN_ISDIR' not in masks)

class PatternChange:
    """This is a class"""
    pass

def changes(pattern, *abs_paths):
    """a generator for detecting changes to regex patterns
    within a set of files

    Args:
        param1 (str): the regex pattern to match
        *abs_paths: the absolute paths to the files to be monitored

    Yields:
        :watch.PatternChange: the `PatternChange` object representing the change
    """
    # cache the hashes of each match for each watched file
    for p in abs_paths:
        hashes = hashes_of(*match(pattern, p.read_text()))
        hashfile_path(p).write_text('\n'.join(hashes))

    for updated in writes(*abs_paths):
        # collect cached hashes
        old_hashes  = [hash.strip() for hash
                in hashfile_path(updated).read_text().split('\n')
                if hash != '']

        # find matches in the updated file and compute hashes
        matches  = match(pattern, updated.read_text())
        hashes   = hashes_of(*matches)

        # hash not one of the cached hashes -> item added
        added   = [(i+1, 'added', matches[i]) for i, md5
                in enumerate(hashes) if md5 not in old_hashes]

        # cached hash not one of the new hashes -> item removed
        removed = [(i+1, 'removed') for (i, md5)
                in enumerate(old_hashes) if md5 not in hashes]

        moved   = [(new_ind+1, 'moved', match, old_ind+1)
                for new_ind, match in enumerate(matches)
                for old_ind, old_md5 in enumerate(old_hashes)
                if old_ind != new_ind and old_md5 == hashes[new_ind]]

        yield from added + removed + moved

        hashfile_path(updated).write_text("\n".join(hashes))
