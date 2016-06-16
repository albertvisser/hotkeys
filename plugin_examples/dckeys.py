# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import collections
import shutil
import xml.etree.ElementTree as ET
import bs4 as bs # import BeautifulSoup
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

instructions = """\
Instructions for rebuilding the keyboard shortcut definitions


The keydefs are stored in a file called shortcuts.scf, located in
~/.config/doublecmd. For convenience sake, store this name in a setting
named DC_PATH so the buildcsv and savekeys functions don't have to
ask for a filename every time.

Two extra settings are used to extract the default mappings and the
command definitions from the help files: DC_KEYS and DC_CMDS
respectively.

Inside Double Commander, in Configuration > Options > Hot keys,
it's possible to select the shortcuts file, so support for using
a name different from the DC_PATH setting is present.
"""

#    basic layout:
#    <doublecmd DCVersion="0.6.6 beta">
#      <Hotkeys Version="20">
#        <Form Name="Main">
#          <Hotkey>
#            <Shortcut>F1</Shortcut>
#            <Command>cm_RenameOnly</Command>
#
#    some commands can use parameters
#            <Command>cm_ExecuteToolbarItem</Command>
#            <Param>ToolItemID={BE39E7CB-3FC4-44DB-99FA-30415C9D8C50}</Param>
#    and/or other options:
#        <Shortcut>Shift+Del</Shortcut>
#        <Command>cm_Delete</Command>
#        <Param>trashcan=reversesetting</Param>
#        <Control>Files Panel</Control>

def _shorten_mods(modifier_list):
    result = ''
    if 'Ctrl' in modifier_list:
        result += 'C'
    if 'Alt' in modifier_list:
        result += 'A'
    if 'Shift' in modifier_list:
        result += 'S'
    return result

def _translate_keynames(inp):
    "translate cursor keys as shown in html to notation in xml"
    convert = {' ↑': 'Up', ' ↓': 'Down', ' ←': 'Left', ' →': 'Right'}
    return convert[inp] if inp in convert else inp

def parse_keytext(text):
    """leid keynamen en modifiers op uit tekst

    geeft een list terug van keynaam - modifier-list paren
    voorziet nog niet in , key al dan niet met modifiers
    """
    retval = []

    # split keycombos
    shortcuts = text.split(', ')
    for sc in shortcuts:

        # split for modifiers
        test = sc.split('+')
        keyname = test[-1]
        modifiers = test[:-1]

        # correct for + key
        if keyname == '':
            keyname = '+'
            if modifiers[-1] == '': # + key not on numpad
                modifiers.pop()
            elif modifiers[-1] == 'Num ': # + key on numpad
                keyname = modifiers.pop() + keyname

        retval.append((keyname, _shorten_mods(modifiers)))

    return retval

def get_keydefs(path):
    """
    huidige keydefs afleiden
    """

    # read the key definitions file
    data = ET.parse(path)

    # (re)build the definitions for the csv file
    keydata = collections.OrderedDict()
    key = 0
    root = data.getroot()
    for form in list(root.find('Hotkeys')):
        context = form.get('Name')
        for hotkey in form:
            shortcut = hotkey.find('Shortcut').text
            if shortcut.endswith('+'):
                parts = shortcut[:-1].split('+')
                parts[-1] += '+'
            else:
                parts = shortcut.split('+')
            keyname = parts[-1]
            modifiers = _shorten_mods(parts[:-1])
            command = hotkey.find('Command').text
            parameter = hotkey.find('Param')
            parameter = parameter.text if parameter is not None else ''
            control = hotkey.find('Control')
            control = control.text if control is not None else ''
            key += 1
            keydata[key] = (keyname, modifiers, context, command, parameter, control)

    return keydata


def get_stdkeys(path):
    """determine standard keys

    keyname moet nog verder opgesplitst worden, in elk geval de modifiers nog apart
    en sommige kunnen meer combo's (gescheiden door komma's) bevatten
    NB splitsen op + geeft soms onjuist resultaat (bv bij Num +)
    """

    with open(path) as doc:
        soup = bs.BeautifulSoup(doc)

    stdkeys = []
    sections = soup.find_all('div', class_='SECT1')
    for div in sections:

        context = div.select("h2 a")
        if not context:
            continue

        context = context[0]['name']

        tbody = div.select('table tbody tr')

        for row in tbody:
            for col in row.select('td'):
                test = col.select('tt')
                if test:
                    keynames = parse_keytext(test[0].text) # kan meer dan 1 key / keycombo bevatten
                else:
                    oms = col.text # zelfde omschrijving als uit cmd's ? Heb ik deze nodig?
            for name in keynames:
                stdkeys.append((_translate_keynames(name), context, oms))

    return stdkeys

def get_cmddict(path):

    with open(path) as doc:
        soup = bs.BeautifulSoup(doc)

    cmddict = {}
    div = soup.find_all('div', class_='CHAPTER')[0]
    tbody = div.select('div > table > tbody > tr')

    for row in tbody:
        command, oms = '', ''
        for col in row.find_all('td', recursive=False):
            test = col.select('tt > div > a')
            if test:
                command = test[0].text
            else:
                oms = ''
                for item in col.contents:
                    if isinstance(item, bs.Tag):
                        if item.name == 'br':
                            break
                        else:
                            oms += item.text
                    else:
                        oms += str(item)
        cmddict[command] = oms

    return cmddict


def buildcsv(parent):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    shortcuts = collections.OrderedDict()

    ok = gui.QMessageBox.information(parent, parent.captions['000'], instructions,
        gui.QMessageBox.Ok | gui.QMessageBox.Cancel)
    if ok == gui.QMessageBox.Cancel:
        return

    kbfile = gui.QFileDialog.getOpenFileName(parent, parent.captions['059'],
        directory=parent.page.settings['DC_PATH'][0], filter='SCF files (*.scf)')
    if not kbfile:
        return

    keydata = get_keydefs(kbfile)
    # to determine if keys have been redefined
    stdkeys = get_stdkeys(parent.page.settings['DC_KEYS'][0])
    # to find descriptions for commands
    cmddict = get_cmddict(parent.page.settings['DC_CMDS'][0])
    for key, value in keydata.items():
        templist = list(value)
        templist.insert(2, '') # standard / customized
        try:
            templist.append(cmddict[value[3]])
        except KeyError:
            templist.append('')
        print(templist)
        shortcuts[key] = tuple(templist)

    return shortcuts

how_to_save = """\
Instructions to load the changed definitions back into Double Commander.


After you've saved the definitions to a .scf file, go to
Configuration > Options > Hot keys, and select it in the
top left selector.


You may have to close and reopen the dialog to see the changes.
"""
def savekeys(parent):
    """schrijf de gegevens terug

    voorlopig nog niet mogelijk
    aangepaste keys samenstellen tot een user.shortcuts statement en dat
    invoegen in shortcuts.scf
    """

    ok = gui.QMessageBox.information(parent, parent.captions['000'], how_to_save,
        gui.QMessageBox.Ok | gui.QMessageBox.Cancel)
    ## if ok == gui.QMessageBox.Cancel:
        ## return
    return
    for key, mods, type_, context, command, descrption in parent.data.values():
        pass

