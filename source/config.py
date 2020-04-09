"""internal configuration of the project"""
from pathlib import Path

def hashfile_path(f):
    """create a path and filename for the hashfile associated
    to the given file

    Args:
        param1 (pathlib.Path): a path to a file

    Returns:
        The path to the files associated hashfile
    """
    return Path('/tmp/watch_{}'.format(f.name))
