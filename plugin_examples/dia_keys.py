# -*- coding: UTF-8 -*-
"""
See example_app_keys.py for a description of the plugin API.
Only define the functions that need to be defined, for everything
that's not in here the default code in the main program will be used.
"""
import collections
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
from .read_gtkaccel import read_keydefs_and_stuff

def buildcsv(parent, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    shortcuts = collections.OrderedDict()

    try:
        initial = parent.page.settings['DIA_KEYS'][0]
    except KeyError:
        initial = ''
    if showinfo:
        kbfile = gui.QFileDialog.getOpenFileName(parent, parent.captions['059'],
            directory=initial)
    else:
        kbfile = initial
    if not kbfile:
        return

    stuffdict = read_keydefs_and_stuff(kbfile)
    keydefs = stuffdict.pop('keydefs')
    actions = stuffdict['actions']

    lastkey, used = 0, {}
    for key, mods, command in keydefs:
        lastkey += 1
        context, action = actions[command]
        description = ''
        shortcuts[str(lastkey)] = (key, mods, context, action, description)

    return shortcuts, stuffdict
