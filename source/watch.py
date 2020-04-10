"""A library for detecting changes within files"""
from inotify.adapters import Inotify
from inotify.constants import IN_CLOSE_WRITE
from pathlib import Path
from itertools import groupby, product
from regexutils import *
from hashutils import *
from config import *

def writes(*abs_paths):
    """a generator for file change events

    Args:
        *abs_paths: the absolute paths to all the files
            to be monitored. Strings or `pathlib.Path` accepted

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

def changes(pattern, *abs_paths, yield_sames=False):
    """a generator for detecting changes to regex patterns
    within a set of files

    Args:
        param1 (str): the regex pattern to match
        *abs_paths: the absolute paths to the files to be monitored
        yield_sames (bool): if True a match appearing in the same
            place (relative to other matches) will be treated as a
            'none' change. This way there will be one yield for every
            match in a file each time the file is written to

    Yields:
        a tuple of one of the following forms

        ('added', match_number, match_text)
        ('removed', previous_match_number, match_text)
        ('moved', (previous_match_number, match_number), match_text)
        ('none', match_number, match_text)

        where:
            match_number (int): the index of the match in the
                the list of all matches within the file

            previous_match_number (int): the index of the match
                in the list of all matches in the file, prior to
                the change

            match_text (str): the text which was changed

            match_hash (str): the hash of the match. Computed by
                `hashutils.hash(str)`

    """
    # cache the matches
    for p in abs_paths:
        matches = match(pattern, p.read_text())
        cache_file(p).write_text('\n'.join(matches))

    for updated in writes(*abs_paths):
        # collect cached matches
        cached  = match(pattern, cache_file(updated).read_text())
        # find matches in the updated file
        matches = match(pattern, updated.read_text())

        # associate each match to it's index in the list of matches
        cached_index = {match:i+1 for i, match in enumerate(cached)}
        new_index    = {match:i+1 for i, match in enumerate(matches)}

        added   = set(matches) - set(cached)
        removed = set(cached)  - set(matches)
        still   = set(cached)  & set(matches)

        moved = set([match for match in still
            if cached_index[match] != new_index[match]])

        same  = [('none', new_index[match], match) for match in (still - moved)]
        moved = [('moved', (cached_index[match], new_index[match]), match) for match in moved]
        added   = [('added', new_index[match], match) for match in added]
        removed = [('removed', cached_index[match], match) for match in removed]

        changes = sorted(added + removed + moved)
        if yield_sames: changes += sorted(same)
        yield from changes

        cache_file(updated).write_text("\n".join(matches))
