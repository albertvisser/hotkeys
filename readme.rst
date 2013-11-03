Hotkeys
=======

formerly called Tcmdrkeys was named after a file manager for Windows that is
one of the few programs I found worth buying a license for.

Originally I started this because I didn't like both the way you can view the
shortcut keys in TC and the way you can change them very much.

Another fan had written something like that as part of a suite of settings editors
("Ultra TC Editors", for menu, toolbar, user commands en so also hotkeys) but
surprise surprise, neither their design or their operation would really click
with me.

I didn't use it very often, and when he changed this suite to a shareware
version with a nag screen I quit using it altogether.
But it came with a file where all the key combinations were listed, based upon
various readme and settings files and I could use that to base my own version on.

As a side project, to be independent of that file, I wrote a program to do that
collection and matching myself. So it's basically a two-step progress: use the
collection utility (I named it tcmerge.py) to combine the readme and settings files
into a csv file, and use the editing utilty (tckeys.py) to view and change the keys
and write them back into the settings files. The collection part is not meant to be
used regularly, in fact you only need it when the standard definitions in TC change
which shouldn't be that often.

While I was doing this, it occurred to me that I could apply the same process
(make a tool for displaying and changing shortcut key combinations) to other
favourite programs of mine and have one interface in which to show them all.

Since then I made a variant for VI (only showing the keys), first as a standalone
version and then as part of a multi-tool version, as a way to find out how to do
this. And then I was able to convert the Total Commander version so that it could
be incorporated into the multi-tool version too.

In the mean time I gathered specs so I could to do this for other applications.
For instance my favourite web browser Opera also has got load of shortcuts all over
the place but I lack the overview (their interface seems kind of chaotic too)
and that's just what this tool is meant to bring me:
an overview in the way that works for me.

And since then, I've made versions for SciTE, Opera, Double Commander (my TC
replacement on Linux) and in the process restructured the whole thing
so I need to write as little code as possible for adding a new tool
to the collection. I'm also in the process of writing an add-on to generate new
plugins.

The purpose of having a tool like this is not just to show the shortcuts (help files
and menus do that too) but to be able to change the order in which they are
displayed, so that I can sort on purpose or context instead of just on base key.
