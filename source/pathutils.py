"""functions relating to file paths and working with files"""

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
