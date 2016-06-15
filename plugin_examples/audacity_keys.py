# -*- coding: UTF-8 -*-
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
import shutil
import xml.etree.ElementTree as ET
import collections
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

def buildcsv(parent):

    ok = gui.QMessageBox.information(parent, parent.captions['000'], instructions,
        gui.QMessageBox.Ok | gui.QMessageBox.Cancel)

    if ok == gui.QMessageBox.Cancel:
        return

    try:
        kbfile = parent.settings['AC_KEYS'][0]
    except KeyError:
        kbfile = gui.QFileDialog.getOpenFileName(parent, parent.captions['059'],
            filter='XML files (*.xml)')

    if not kbfile:
        return

    shortcuts = collections.OrderedDict()

    tree = ET.parse(kbfile)
    root = tree.getroot()
    data = []
    key = 0
    for item in root.findall('command'):
        line = []
        keydef = item.get('key').split('+')
        keyname = keydef[-1] if keydef else ''
        line.append(keyname)
        keymods = ''
        if len(keydef) > 1:
            keymods = ''.join([x[0] for x in keydef[:-1]])
        line.append(keymods)
        line.append(item.get('name'))
        line.append(item.get('label'))
        key += 1
        shortcuts[key] = line

    return shortcuts

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

    ok = gui.QMessageBox.information(parent, parent.captions['000'], how_to_save,
        gui.QMessageBox.Ok | gui.QMessageBox.Cancel)

    if ok == gui.QMessageBox.Cancel:
        return

    try:
        kbfile = parent.settings['AC_KEYS'][0]
    except KeyError:
        kbfile = gui.QFileDialog.getSaveFileName(parent, parent.captions['059'],
            filter='XML files (*.xml)')

    root = ET.Element('audacitykeyboard')
    root.set('audacityversion', "2.0.5")
    for key, mods, name, label in parent.data.values():
        new = ET.SubElement(root, 'command')
        new.set('name', name)
        new.set('label', label)
        if 'S' in mods: key = 'Shift+' + key
        if 'A' in mods: key = 'Alt+' + key
        if 'C' in mods: key = 'Ctrl+' + key
        new.set('key', key)

    shutil.copyfile(kbfile, kbfile + '.bak')
    ET.ElementTree(root).write(kbfile, encoding="UTF-8")
