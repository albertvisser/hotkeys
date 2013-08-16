Hotkey Popup
============

...is probably a better name than Tcmdrkeys as this collection is momentarily
called. It's named after a file manager for Windows that is one of the few programs
I found worth buying a license for.

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

As a side project, to be independent of that file I wrote a program to do that
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

In the mean time I've gathered specs so I can to do this for other applications.
Like for Opera, I know there are a lot but I lack the overview (their interface
is kind of chaotic to) and that's just what this tool is meant to bring me:
an overview in the way that works for me.



 ---

 Het nut om in elk geval een Hotkey Popup variant (alleen tonen, niet wijzigen)
 van deze applicatie te maken is niet zozeer het tonen van wat er is
 (dat kun je met een help file ook) maar om het on the fly
 op een andere manier te ordenen, bv, snel switchen van gesorteerd op soort
 functionaliteit naar op toetscombinatie

Het leek me nuttig om een variant te maken waarmee ik dit ook voor andere tools kon
en
