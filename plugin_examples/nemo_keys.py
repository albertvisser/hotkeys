"""Hotkeys plugin for Nemo File Manager
"""
## import os.path
## import shutil
## import csv
import collections
data = """\
T;C;File;New Tab
N;C;File;New Window
N;CS;File;Create New Folder
Return;A;File;Properties
Q;C;File;Close All Windows
W;C;File;Close
Z;C;Edit;Undo
Y;C;Edit;Redo
X;C;Edit;Cut
C;C;Edit;Copy
V;C;Edit;Paste
A;C;Edit;Select All
S;C;Edit;Select Items Matching...
I;CS;Edit;Invert Selection
M;C;Edit;Make Links
F2;;Edit;Rename
P;A;Edit;Plugins
R;C;View;Reload
F9;;View;Show sidebar (toggle)
F3;;View;Extra Pane (toggle)
L;C;View;Toggle Location Entry
H;C;View;Show Hidden Files (toggle)
+;C;View;Zoom In
-;C;View;Zoom Out
0;C;View;Normal Size
1;C;View;Icons
2;C;View;List
3;C;View;Compact
Up;A;Go;Open Parent
Left;A;Go;Back
Right;A;Go;Forward
Home;A;Go;Home
F;C;Go;Search For Files
D;C;Bookmarks;Add Bookmark
B;C;Bookmarks;Edit Bookmark
F1;;Help;All Topics
"""


def buildcsv(parent, showinfo=True):
    """read keydefs from input
    """
    keydefs = {}
    defaultkeys = {}
    commands = collections.defaultdict(list)
    count = 0
    for line in data.split('\n'):
        if not line or line.startswith('#'):
            continue
        section, key, mods, command = line.split(';')
        if key:
            defaultkeys[(key, mods)] = command
        commands[section].append(command)
        count += 1
        keydefs[count] = (section, key, mods, command, '')

    return keydefs, {'commands': commands, 'defaultkeys': defaultkeys}
