from inotify.adapters import Inotify
from inotify.constants import IN_CLOSE_WRITE
from pathlib import Path
from difflib import Differ
from pprint import pprint
from itertools import zip_longest, product
import re
from hashlib import md5
from collections import namedtuple


def files_in(*paths):
    """expand each of the given paths
    Args:
        paths (str): any number of paths to files or directories

    Returns:
        list: the absolute paths of all files found by expanding
        the given paths (not including directories)
    """
    print(paths)
    abs_paths = [Path(p).expanduser() for p in paths]
    filepaths = [([p] if p.is_file() else list(files_in(*p.iterdir()))) for p in abs_paths]
    return [f for li in filepaths for f in li]

def writes(*filepaths):
    """a generator for file change events

    Args:
        filepaths (str): any number of file paths to be
            monitored. Relative or absolute paths accepted.
            if a path leads to a directory all files in the
            directory will be monitored.

    Returns:
        yields the absolute path to the file that has been written to
    """
    filepaths = files_in(*filepaths)

    files = {}
    for path in filepaths:
        dir, name = str(path.parent), path.name
        files[dir] = [name] if dir not in files.keys() else  files[dir].append(name)

    i = Inotify()
    for dir in files.keys():
        i.add_watch(path_unicode=dir, mask = IN_CLOSE_WRITE)

    for event in i.event_gen(yield_nones=False):
        _, types, path, filename = event
        if filename in files[path] and 'IN_ISDIR' not in types:
            yield Path(path, filename)

def hashfile_path(f):
    """get the path to the hashfile corresponding to the given file path"""
    return Path('/tmp/watch_{}'.format(f.name))

def hash(s):
    """compute the md5 hash for a string"""
    return md5(s).hexdigest()

def hashes(strings):
    """create a dictionary with the md5 hash of the string
    as the key and the sring as the value"""
    return [hash(s.encode()) for s in strings]

def matches(pattern, string):
    return [match for match in re.findall(pattern, string, re.MULTILINE) if match != '']

def changes(pattern, *filepaths):
    """generator for changes to maches of pattern in
    the specified files """
    # cache the hashes of each match in each file
    for p in files_in(*filepaths):
        try:
            match_list = matches(pattern, p.read_text())
        except UnicodeDecodeError: "could not read file"
        with open(hashfile_path(p), 'w') as hashfile:
            for hash in hashes(match_list):
                print(hash, file=hashfile)

    for updated in writes(*filepaths):
        yield updated
        # collect cached hashes
        old_hashes  = [hash.strip() for hash
                in hashfile_path(updated).read_text().split('\n')
                if hash != '']
        # find matches in the updated file and compute hashes
        match_list  = matches(pattern, updated.read_text())
        hash_list   = hashes(match_list)

        # hash not one of the cached hashes -> item added
        added   = [(i+1, 'added', match_list[i]) for i, md5
                in enumerate(hash_list) if md5 not in old_hashes]

        # cached hash not one of the new hashes -> item removed
        removed = [(i+1, 'removed') for (i, md5)
                in enumerate(old_hashes) if md5 not in hash_list]

        moved   = [(new_ind+1, 'moved', match, old_ind+1)
                for new_ind, match in enumerate(match_list)
                for old_ind, old_md5 in enumerate(old_hashes)
                if old_ind != new_ind and old_md5 == hash_list[new_ind]]

        yield from added + removed + moved

        with open(hashfile_path(updated), 'w') as hashfile:
            for hash in hash_list: print(hash, file=hashfile)

for change in changes('^.*$', '~/projects'):
    print(change)








