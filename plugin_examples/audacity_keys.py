# -*- coding: UTF-8 -*-
"""HotKeys plugin for Audacity
"""
## import sys
import shutil
import xml.etree.ElementTree as ET
import collections
## import functools
## import string
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
## import PyQt5.QtCore as core

instructions = """\
Instructions for rebuilding the key binding definitions


Step 1: Open Audacity, Select Edit > Preferences from the menu
(or press Ctrl-P) and go to "Keyboard".
There you can push a button to Export the key bindings to a file.
Remember where you saved it for step 2 (if you define a setting
named AC_KEYS in the Settings > Tool Specific > Misc dialog
this step will automatically pick it up).

Step 2: Open the key bindings file and have it read the definitions.


You can now take the time to perform step 1.
Press "OK" to continue with step 2 or "Cancel" to return to the main program.
"""


def _translate_keyname(inp):
    """map key names in settings file to key names in HotKeys
    """
    convert = {'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
               'Page_up': 'PgUp', 'Page_down': 'PgDn', 'NUMPAD_ENTER': 'NumEnter'}
    if inp in convert:
        out = convert[inp]
    else:
        out = inp
    return out


def buildcsv(parent, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    shortcuts = collections.OrderedDict()
    otherstuff = {}

    try:
        initial = parent.page.settings['AC_KEYS']
    except KeyError:
        initial = ''

    kbfile = ''
    if showinfo:
        ok = qtw.QMessageBox.information(parent, parent.title, instructions,
                                         qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        if ok == qtw.QMessageBox.Ok:
            kbfile = qtw.QFileDialog.getOpenFileName(
                parent, parent.captions['C_SELFIL'], directory=initial,
                filter='XML files (*.xml)')[0]
    else:
        kbfile = initial
    if not kbfile:
        return [], []

    tree = ET.parse(kbfile)
    root = tree.getroot()
    ## data = []
    key = 0
    commandlist = {}
    for item in root.findall('command'):
        ## line = []
        keydef = item.get('key', default='')
        if keydef.endswith('+'):
            parts = keydef[:-1].split('+')
            parts[-1] += '+'
        else:
            parts = keydef.split('+')
        keyname = parts[-1] if keydef else ''
        keymods = ''
        if len(parts) > 1:
            keymods = ''.join([x[0] for x in parts[:-1]])
        cmd_name = item.get('name')
        cmd_label = item.get('label')
        if keyname:
            key += 1
            shortcuts[key] = (_translate_keyname(keyname), keymods, cmd_name,
                              cmd_label)
        commandlist[cmd_name] = cmd_label
    otherstuff['commands'] = commandlist
    return shortcuts, otherstuff

how_to_save = """\
Instructions to load the changed definitions back into Audacity.

First you need to save the definitions, we'll get to that shortly.

After that, perhaps it's sufficient to (re)start Audacity. Otherwise,
select Edit > Preferences from the menu (or press Ctrl-P) and go to
"Keyboard".
Push the "Import" button and select the file you just saved.

Now press "OK" to build and save the keyboard definitions file
or "Cancel" to return to the main program.
"""


def savekeys(parent):
    """schrijf de gegevens terug
    """
    ok = qtw.QMessageBox.information(parent, parent.title, how_to_save,
                                     qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
    if ok == qtw.QMessageBox.Cancel:
        return

    try:
        kbfile = parent.settings['AC_KEYS']
    except KeyError:
        kbfile = qtw.QFileDialog.getSaveFileName(parent, parent.captions['C_SELFIL'],
                                                 filter='XML files (*.xml)')

    root = ET.Element('audacitykeyboard')
    root.set('audacityversion', "2.0.5")
    for key, mods, name, label in parent.data.values():
        new = ET.SubElement(root, 'command')
        new.set('name', name)
        new.set('label', label)
        if 'S' in mods:
            key = 'Shift+' + key
        if 'A' in mods:
            key = 'Alt+' + key
        if 'C' in mods:
            key = 'Ctrl+' + key
        new.set('key', key)

    shutil.copyfile(kbfile, kbfile + '.bak')
    ET.ElementTree(root).write(kbfile, encoding="UTF-8")


def add_extra_attributes(win):
    """specifics for extra panel
    """
    win.keylist.append('NumEnter')
    win.descriptions = win.otherstuff['commands']
    win.commandslist = sorted(win.descriptions.keys())

# end
