# -*- coding: UTF-8 -*-

"""
See example_app_keys.py for a description of the plugin API.
Only define the functions that need to be defined, for everything
that's not in here the default code in the main program will be used.
"""
import collections
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
from .read_gtkaccel import read_keydefs

def buildcsv(parent):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    shortcuts = collections.OrderedDict()

    try:
        initial = parent.page.settings['BE_PATH'][0]
    except KeyError:
        initial = ''
    kbfile = gui.QFileDialog.getOpenFileName(parent, parent.captions['059'],
        directory=initial)
    if not kbfile:
        return

    keydefs, actions, others = read_keydefs(kbfile)
    ## for ix, item in enumerate(actions):
        ## key, mods, cmd = item
        ## shortcuts[ix + 1] = (key, mods, actions[cmd])
    lastkey, used = 0, {}
    for key, mods, command in keydefs:
        lastkey += 1
        shortcuts[str(lastkey)] = (key, mods, actions[command])
        ## used[command] = '' # can't pop these from actions because the may have been reused
    ## for key in actions:
        ## if key in used: continue
        ## lastkey += 1
        ## shortcuts[str(lastkey)] = ('', '', actions[key])
    return shortcuts, {'actions': actions, 'others': others}
