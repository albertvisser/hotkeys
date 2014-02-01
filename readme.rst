Hotkeys
=======

All kinds of apps have shotcut keys, and if you're lucky also a place
where you can get an overview of them all together and maybe even change them.

I thought it would be nice to have an all-in-one interface like this for all the tools
I use frequently so I built it.

The purpose of having a tool like this is not just to show the shortcuts (help files
and menus do that too) but to be able to change the order in which they are
displayed, so that I can sort on purpose or context instead of just on base key.

And then of course, be able to apply changes where possible.

For each plugin a tool to build a csv file from a specific tool's configuration
can also be devised (and one is),
but of course these files can also be created by hand (and most of them currently
are).

Usage
-----

Simply call ``hotkeys.py`` in the top directory.

To customize for a new tool, you have to add a plugin for it.
This mechanism is currently being redesigned.

Requirements
------------

- Python
- PyQt4 for the current (Python 3) version
- wxPython for the previous version (not up to date with the latest developments)
- the built in csv module for creating and reading the csv files
