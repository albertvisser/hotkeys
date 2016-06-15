# -*- coding: UTF-8 -*-
import collections
from .read_gtkaccel import read_keydefs

def buildcsv(parent):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    shortcuts = collections.OrderedDict()

    keydefs, actions = read_keydefs(parent.settings['BE_PATH'][0])
    for ix, item in enumerate(actions):
        key, mods, cmd = item
        shortcuts[ix + 1] = (key, mods, actions[cmd])

    return shortcuts

def savekeys(parent):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    aangepaste keys samenstellen tot gtk_accelmap entries en terugschrijven naar
    het file genoemd in settings['BE_PATH'][0]
    Geen idee of dat zomaar kan eerlijk gezegd
    """
    pass
