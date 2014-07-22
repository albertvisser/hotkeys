# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import csv
import shutil
import xml.etree.ElementTree as ET

def savekeys(pad):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    """
    pass


def getkeyname(value):
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
    mods = ''
    if element.attrib['Ctrl'] == '1':
        mods += 'C'
    if element.attrib['Alt'] == '1':
        mods += 'A'
    if element.attrib['Shift'] == '1':
        mods += 'S'
    return mods

def gethotkey(element):
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

def buildcsv():
    """
    In het huidige definities bestand zitten twee schema's,
    de ene heeft kenmerk SAPGUI en de andere VS 98 like
    en voor beiden worden drie CSV files aangemaakt
    een en ander moet nog uitgebreid worden met settings en column headers
    """
    commands = {}
    hotkeys = []
    with open('ABAP Editorkeymap.xml') as _in:
        tree = ET.ElementTree(file=_in)
    root = tree.getroot()
    for element in list(root):
        if element.tag in ('HOTKEYSCHEMA', 'HOTKEYSCHEMA.bak'):
            for keys in [gethotkey(sub) for sub in list(element)]:
                for num, cmd, oms, mods, value in keys:
                    commands[num] = [cmd, oms]
                    hotkeys.append((value, mods, num))
            with open(element.attrib["name"] + '_commands.csv', 'w') as _out:
                for key in sorted(commands.keys()):
                    cmd, oms = commands[key]
                    _out.write(';'.join((key, cmd, '"{}"'.format(oms))) + '\n')
            with open(element.attrib["name"] + '_hotkeys.csv', 'w') as _out:
                for hotkey in hotkeys:
                    if hotkey[0]: # only write if there's a key defined
                        _out.write(';'.join(hotkey) + '\n')
            with open(element.attrib["name"] + '_hotkeys_2.csv', 'w') as _out:
                for hotkey in sorted(hotkeys):
                    if hotkey[0]: # only write if there's a key defined
                        value, mods, num = hotkey
                        cmd, oms = commands[num]
                        _out.write(';'.join((getkeyname(value), mods, cmd, oms)
                            ) + '\n')

