"""functions relating to pattern matching"""
from re import finditer, MULTILINE

def match(pattern, string):
    return [match for match in finditer(pattern, string, MULTILINE) if match != '']
