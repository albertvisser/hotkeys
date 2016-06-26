# -*- coding: UTF-8 -*-
import collections
import json
"""
See example_app_keys.py for a description of the plugin API.
Only define the functions that need to be defined, for everything
that's not in here the default code in the main program will be used.
"""
## lees /home/albert/.config/opera-developer/Preferences met een json parser
## Onder het hoofdniveau Keybindings subniveau Basic zit een dictionary met
## key = commando en value is een list met keyboard shortcuts
        ## "Back":["Alt+Left","Ctrl+Left"],
        ## "BasicPrint":["Ctrl+Shift+P"],
## geen idee of er ergens een command list is
## aan de settings te zien is alles dat er is gedefinieerd
def getkey(keystr):
    endsinplus = False
    if keystr.endswith('+'):
        keystr = keystr[:-1]
        endsinplus = True
    parts = keystr.split('+')
    if endsinplus:
        parts[-1] += '+'
    mods = ''
    if 'Ctrl' in parts:
        mods += 'C'
    if 'Alt' in parts:
        mods += 'A'
    if 'Shift' in parts:
        mods += 'S'
    return mods, parts[-1]


def buildcsv(parent):
    opprefs = '/home/albert/.config/opera-developer/Preferences'
    shortcuts = collections.OrderedDict()
    commandlist = []
    with open(opprefs, encoding='UTF-8') as _in:
        data = json.load(_in)
    keydict = data['Keybindings']['Basic']
    number = 0
    for cmdstr, value in keydict.items():
        commandlist.append(cmdstr)
        for hotkey in value:
            number += 1
            mod, key = getkey(hotkey)
            shortcuts[number] = (key, mod, 'Basic', cmdstr)
    return shortcuts, {'commands': commandlist}
