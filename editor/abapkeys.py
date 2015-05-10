# -*- coding: utf-8 -*-
"""
usage: abapkeys.py <csvfile>

This program takes the definitions in abap_hotkeys.py and builds from it
three csv files per editor mode (currently we have "SAPGUI" and "VS 98 like")

<mode>_commands.csv contains a list of command codes, names and descriptions
    and could be useful in an editing extension to list available possibilities
    (if it's complete)
<mode>_hotkeys.csv contains a list of key codes, modifiers and command codes
    perhaps we don't need this at all
<mode>_hotkeys_2.csv contains a list of keynames, modifiers, commands names and
    descriptions. The first two and the last are currently used in the CSV that
    services the GUI. This one contains more keydefs than are in the xml however,
    menu shortcuts are also included so some differentiation may be useful
"""
from __future__ import print_function
import os
import shutil
import xml.etree.ElementTree as ET
## from editor.hotkeys_qt import read_settings, readcsv, writecsv
import collections

def savekeys(pad):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    """
    pass


def getkeyname(value):
    '''translate keycode to key name
    '''
    keytext = {
        "8": "BackSpace",
        "9": "Tab",
        "13": "Enter",
        "32": "Space",
        "33": "PageUp",
        "34": "PageDown",
        "35": "End",
        "36": "Home",
        "37": "Left",
        "38": "Up",
        "39": "Right",
        "40": "Down",
        "45": "Insert",
        "46": "Delete",
        "106": "Num *",
        "107": "Num +",
        "109": "Num -",
        "111": "Num /",
        "226": "<",
    }

    if value in keytext:
        key = keytext[value]
    elif '111' < value < '123':
        key = 'F' + str(int(value) - 111)
    elif int(value) > 159:
        key = chr(int(value) - 128)
    elif value:
        key = chr(int(value))

    return key

def getmodifiers(element):
    '''interpret XML attributes to build modifier string
    '''

    mods = ''
    if element.attrib['Ctrl'] == '1':
        mods += 'C'
    if element.attrib['Alt'] == '1':
        mods += 'A'
    if element.attrib['Shift'] == '1':
        mods += 'S'

    return mods

def gethotkey(element):
    '''interpret XML elements/attributes to build key definition
    '''
    hotkey = []
    hotkey_id = element.attrib['id']

    for sub in list(element):
        if sub.tag == 'VerbID':
            hotkey_verb = sub.text
        elif sub.tag == 'Descr':
            hotkey_desc = sub.text
        elif sub.tag == 'Shortcut':
            hotkey_mods = getmodifiers(sub)
            hotkey_value = sub.attrib['Key']
            hotkey.append((hotkey_id, hotkey_verb, hotkey_desc, hotkey_mods,
                hotkey_value))

    if not hotkey:
        hotkey = [(hotkey_id, hotkey_verb, hotkey_desc, '', '')]

    return hotkey

def buildcsv(settings, parent=None):
    """
    In het huidige definities bestand zitten twee schema's (editor modes),
    eigenlijk is er maar één actief en dus belangrijk
    """
    commands = {}
    hotkeys = []
    shortcuts = collections.OrderedDict()

    with open(settings['AB_DEFS']) as _in:
        tree = ET.ElementTree(file=_in)
    root = tree.getroot()

    keynum = 0
    for element in list(root):

        ## if element.tag in ('HOTKEYSCHEMA', 'HOTKEYSCHEMA.bak'):
        if element.tag == 'HOTKEYSCHEMA':

            # read the defined keys
            for keys in [gethotkey(sub) for sub in list(element)]:
                for num, cmd, oms, mods, value in keys:
                    commands[num] = [cmd, oms]
                    hotkeys.append((value, mods, num))

            # build a list of used commands
            used_commands_list = []
            for key in sorted(commands.keys()):
                cmd, oms = commands[key]
                used_commands_list.append((key, cmd, oms))

            # build a list of keycode - command code combinations
            command_codes_list = []
            for hotkey in hotkeys:
                command_codes_list.append(hotkey)

            # build a list of key definitions with command and description
            for hotkey in sorted(hotkeys):
                value, mods, num = hotkey
                cmd, oms = commands[num]
                if hotkey[0]: # only write if there's a key defined
                    keydef = getkeyname(value)
                    keynum += 1
                    shortcuts[keynum] = [keydef, mods, cmd, oms]

    return shortcuts
