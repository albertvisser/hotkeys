"""HotKeys plugin for Audacity
"""
import os.path
import shutil
import xml.etree.ElementTree as ET
from ..gui import show_cancel_message, get_file_to_open, get_file_to_save

INSTRUCTIONS = """\
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
    return convert.get(inp, inp)


def build_data(page, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het keydef bestand
    """
    otherstuff = {}
    initial = page.settings.get('AC_KEYS', '')

    kbfile = ''
    if showinfo:
        ok = show_cancel_message(page.gui, text=INSTRUCTIONS)
        if ok:
            kbfile = get_file_to_open(page.gui, extension='XML files (*.xml)', start=initial)
            # if kbfile:
            #     page.settings['AC_KEYS'] = kbfile
    else:
        kbfile = initial
    if not kbfile:
        return {}, {}

    tree = ET.parse(kbfile)
    shortcuts, otherstuff['commands'] = build_commandlist(tree.getroot())
    return shortcuts, otherstuff


def build_commandlist(root):
    "build the list of commands"
    shortcuts = {}
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
            shortcuts[key] = (_translate_keyname(keyname), keymods, cmd_name, cmd_label)
        commandlist[cmd_name] = cmd_label
    return shortcuts, commandlist


how_to_save = """\
Instructions to load the changed definitions back into Audacity.

First you need to save the definitions.

After that, it might be sufficient to (re)start Audacity.
Otherwise, select Edit > Preferences from the menu (or press Ctrl-P)
and go to "Keyboard".
Push the "Import" button and select the file you just saved.

Now press "OK" to build and save the keyboard definitions file
or "Cancel" to return to the main program.
"""


def savekeys(parent):
    """schrijf de gegevens terug
    """
    ok = show_cancel_message(parent, text=how_to_save)
    if not ok:
        return

    kbfile = parent.settings.get('AC_KEYS', '')
    if not kbfile:
        initial = os.path.expanduser('~/.config/Audacity-keys.xml')
        kbfile = get_file_to_save(parent, extension='XML files (*.xml)', start=initial)
        parent.settings['AC_KEYS'] = kbfile

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

    if os.path.exists(kbfile):
        shutil.copyfile(kbfile, kbfile + '.bak')
    ET.ElementTree(root).write(kbfile, encoding="UTF-8")


def add_extra_attributes(win):
    """specifics for extra panel
    """
    win.keylist.append('NumEnter')
    win.descriptions = win.otherstuff['commands']
    win.commandslist = sorted(win.descriptions.keys())

# end
