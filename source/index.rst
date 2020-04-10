.. PatternMonitor documentation master file, created by
   sphinx-quickstart on Thu Apr  9 08:59:47 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the fs-events docs!
==========================================

fs-events is a python library for capturing file system events
as generators. It uses inotify [LINK HERE] to monitor events and
does not require polling


Examples
=========================================
.. code-block:: python
        :linenos:

        # do something every time a file is written to
        path = Path('~/path/to/file').expanduser()
        for changed_file in fsevents.writes(path):
                dosomething(changed_file)


fsevents module
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. automodule:: fsevents
        :members:

Utils
===========================================
.. automodule:: pathutils
        :members:



