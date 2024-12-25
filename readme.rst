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

And then of course, to be able to apply changes where possible.
For that, part of the screen can be used to define custom fields to show and edit
details of a shortcut key definition.

To customize for a new tool, you have to add a plugin for it. At the moment
this mechanism consists of a Python module that can contain some functions to be
called by the main program, and a file containing the keyboard definitions and
some tool-specifc settings. These can be generated in basic form from within the
program and then customized by hand. 

Initially the new plugin is just an empty python module. 
It can be extended to contain functions that (re)generate the keydef portion
of the definitions file from the tool's configuration files, 
and to write modified keydefs back to them.
It's also meant for customisation of the editor part of this program (the lower part of the screen).

A couple of plugins - that I made for the tools that I use - is included,
as well as an empty (in the sense that it does nothing) plugin containing various explanations.
To use the included plugins, you don't need to copy them to the editor/plugins subdirectory,
you can just (sym)link them.


Usage
-----

Simply call ``start.py`` in the top directory.
Use ``toolkit.py`` in the program directory (``editor``) to define which gui toolkit to use.

I started out using csv files for the keyboard definitions and other settings, because other tools
like this one did that too I guess. 
Later I found it a bit too complicated so I simplified it and switched to a json format (for the tool itself as well as for the plugin keydef data).


Requirements
------------

- Python
- PyQt(6) or wxPython (Phoenix) for the GUI part
- the built in json module for creating and reading the definition files
- plugins may use BeautifulSoup (and lxml) for parsing HTML help files
