"""functions relating to pattern matching"""
from re import *

def match(pattern, string):
    return [match for match in findall(pattern, string, MULTILINE) if match != '']
