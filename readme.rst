Hotkeys
=======

All kinds of apps have shortcut keys, and if you're lucky also a place
where you can get an overview of them all together and maybe even change them.

I thought it would be nice to have an all-in-one interface for all the tools
I use frequently so I built this thingy. It's basically an organised list of
keyboard shortcut definitions.

The purpose of having a tool like this is not just to show the shortcuts (help files
and menus do that too) but to be able to change the order in which they are
displayed, so that I can sort on purpose or context instead of just on base key
making it easier to find a keydef if I need it, in whatever way I want to look for it.
That's why I also built search and filter facilities.

And then of course, be able to apply changes where possible.
For that, part of the screen can be used to define custom fields to show and edit
details of a shortcut key definition.

To customize for a new tool, you have to add a plugin for it. At the moment
this mechanism consists of a Python module that can contain some functions to be
called by the main program, and a csv file containing the keyboard definitions and
some tool-specifc settings. These can be generated in basic form from within the
program and then customized by hand, also from within the program.

Initially the plugin is just an empty python module. It can be extended to contain
functions that (re)generate the keydef portion of the CSV file from the
tool's configuration files, and to write modified keydefs back to them.
It's also meant for customisation of the editor part of this program.


Usage
-----

Simply call ``hotkeys.py`` in the top directory.


Requirements
------------

- Python
- PyQt4 for the GUI part
- the built in csv module for creating and reading the csv files
