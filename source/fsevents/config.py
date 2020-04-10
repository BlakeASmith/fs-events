"""internal configuration of the project"""
from pathlib import Path

def cache_file(f):
    """create a path and filename for the cache file associated
    to the given file

    Args:
        param1 (pathlib.Path): a path to a file

    Returns:
        The path to the files associated cache file
    """
    return Path('/tmp/watch_{}'.format(f.name))
