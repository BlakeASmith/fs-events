"""utilities for computing hashes"""
from hashlib import md5

def hashes_of(*strings):
    """compute hashes for all the given strings

    Args:
        *strings: the strings to compute hashes for

    Returns:
        a list of the hashes in the same order that the
        strings were given
    """
    return [hash(s) for s in strings]

def hash(s):
    """compute the md5 hash for a string"""
    return md5(s.encode()).hexdigest()



