import watch
from pathlib import Path
paths = [Path('~/projects/PatternMonitor/source/tests.py').expanduser()]

for change in watch.changes('^def\s+(?P<func_name>[a-zA-Z]+)\((?P<params>.*)\):$', *paths):
    print(change)
