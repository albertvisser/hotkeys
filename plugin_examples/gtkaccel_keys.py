# -*- coding: UTF-8 -*-
"""basic plugin for tool using a gtkaccel_map
"""
import sys
import collections
import functools
import string
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
from .read_gtkaccel import read_keydefs_and_stuff

settname = ''

def _translate_keyname(inp):
    convert = {'Equal': '=', 'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
        'Page_up': 'PgUp', 'Page_down': 'PgDn'}
    if inp in convert:
        out = convert[inp]
    else:
        out = inp
    return out

def buildcsv(settname, parent, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    shortcuts = collections.OrderedDict()

    try:
        initial = parent.page.settings[settname][0]
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
    omsdict = stuffdict['descriptions']

    lastkey, used = 0, {}
    for key, mods, command in keydefs:
        lastkey += 1
        context, action = actions[command]
        description = omsdict[command]
        shortcuts[str(lastkey)] = (_translate_keyname(key), mods, context, action,
            description)

    return shortcuts, stuffdict

# specifics for extra panel
def add_extra_attributes(win):
    win.keylist += ['Num' + x for x in string.digits] + ['>', '<']
    win.contextslist = win.otherstuff['contexts']
    win.contextactionsdict = win.otherstuff['actionscontext']
    win.actionslist = win.otherstuff['actions']
    win.descriptions = win.otherstuff['descriptions']
    try:
        win.otherslist = win.otherstuff['others']
    except KeyError:
        pass
    else:
        win.othersdict = win.otherstuff['othercontext']
        win.otherskeys = win.otherstuff['otherkeys']
#
