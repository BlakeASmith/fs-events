import watch
from pathlib import Path

for event in watch.changes('^.*$', Path('~/projects/PatternMonitor/source/tests.py').expanduser()):
    print(event)

