Taskwarrior Timecrimes
======================

Travel back in time and undo your duplicate tasks' creation.

**WARNING**: This has only barely been tested, and although it did
work as expected for the use case I wrote it for, the command it
generates *might* be incorrect.  Do read through the prompts
carefully, and use this at your own risk!


Installation
------------

Install using ``pip``::

    pip install taskwarrior-timecrimes

Use
---

Just run the following command in a shell::

    taskwarrior_timecrimes

You'll be presented with a list of dates having recent changes.
After selecting the date that you'd like the duplicated recurrences
to be deleted from, the command you can run to delete those tasks
will be generated and printed to the console so you can run it yourself.
