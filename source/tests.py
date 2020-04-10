import watch
from pathlib import Path
paths = [Path('~/projects/PatternMonitor/source/tests.py').expanduser()]

for change in watch.changes('^((\S+)\s)*$', *paths):
    print(change)

