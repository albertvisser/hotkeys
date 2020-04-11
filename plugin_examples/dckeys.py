"""HotKeys plugin for Double Commander PyQt5 version

gebaseerd op versie 0.8
"""
from __future__ import print_function

import os
import sys
## import string
import collections
import functools
import shutil
import xml.etree.ElementTree as ET
import bs4 as bs  # import BeautifulSoup
from ..gui import show_cancel_message, get_file_to_open, get_file_to_save, show_dialog
from .dckeys_gui import add_extra_fields, layout_extra_fields, DcCompleteDialog


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
it's (theoretically) possible to select the shortcuts file, so support for using
a name different from the DC_PATH setting is present.
"""


def _shorten_mods(modifier_list):
    result = ''
    if 'Ctrl' in modifier_list:
        result += 'C'
    if 'Alt' in modifier_list:
        result += 'A'
    if 'Shift' in modifier_list:
        result += 'S'
    if 'WinKey' in modifier_list:
        result += 'W'
    return result


def _translate_keynames(inp):
    "translate cursor keys as shown in html to notation in xml"
    convert = {'↑': 'Up', '↓': 'Down', '←': 'Left', '→': 'Right',
               'Delete': 'Del', 'PgDown': 'PgDn'}
    try:
        return convert[inp.strip()]
    except KeyError:
        return inp.strip()


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
        keyname = test[-1].title()
        modifiers = test[:-1]
        # correct for + key
        if keyname == '':
            keyname = '+'
            if modifiers[-1] == '':  # + key not on numpad
                modifiers.pop()
            elif modifiers[-1] == 'Num ':  # + key on numpad
                keyname = modifiers.pop() + keyname
        retval.append((keyname, _shorten_mods(modifiers)))

    return retval


def get_keydefs(path):
    """huidige keydefs afleiden

    input:
        pad (zoals opgegeven in DC_PATH -- shortcuts.scf in de settings directory)
    resultaat:
        een mapping met key = een volgnummer, value = een tuple van keyname,
            modifiers, context, command, parameter en controls
        een mapping met key = een tuple van keyname, modifiers en value = een tuple
            van context en command

    """
    data = ET.parse(path)

    keydata = collections.OrderedDict()
    keydata_2 = collections.defaultdict(list)
    ## all_contexts = set()
    ## all_controls = set()
    key = 0
    root = data.getroot()
    for form in list(root.find('Hotkeys')):
        context = form.get('Name')
        ## all_contexts.add(context)
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
            ## test = hotkey.find('Param')
            test = hotkey.findall('Param')
            if test is None:
                parameter = ''
            else:
                parameter = ";".join([param.text for param in test])
            ## test = hotkey.find('Control')
            test = hotkey.findall('Control')
            if test is None:
                controls = ''
                ## all_controls.add(controls)
            else:
                controls = []
                for control in test:
                    controls.append(control.text)
                    ## all_controls.add(control.text)
                controls = ';'.join(controls)
            key += 1
            keydata[key] = (keyname, modifiers, context, command, parameter, controls)
            keydata_2[(keyname, modifiers)].append((context, command))

    return keydata, keydata_2


def get_stdkeys(path):
    """determine standard keys

    input:
        pad (zoals opgegeven in DC_KEYS -- shortcuts.html in de docs directory)
    resultaat:
        een mapping met key = een tuple van keyname, modifiers en value = een tuple
            van context en omschrijving
        een list met mogelijke contexts
    """
    with open(path) as doc:
        soup = bs.BeautifulSoup(doc, 'lxml')

    stdkeys = collections.defaultdict(list)
    # newsoup = soup.find('div', class_='dchelpage')
    sections = soup.find_all('div')
    contexts_list = []
    for div in sections:

        context = div.select("h2 a")
        if not context:
            continue

        context = context[0]['name']
        if context in ("warning", "options"):
            continue
        contexts_list.append(context)

        tbody = div.select('table tr')

        for row in tbody:
            if 'class' in row.attrs:
                continue
            keynames = ()
            for col in row.select('td'):
                ## if col['class'] == 'varcell':
                if 'class' in col.attrs and 'varcell' in col['class']:
                    keynames = parse_keytext(col.div.text)  # kan meer dan 1 key / keycombo bevatten
                ## elif 'hintcell' in col['class']:
                    ## print('hintcell')
                else:
                    oms = col.get_text()
                ## test = col.select('tt')
                ## if test:
                    ## keynames = parse_keytext(test[0].text)  # kan meer dan 1 key / keycombo bevatten
                ## else:
                    ## oms = col.text  # zelfde omschrijving als uit cmd's ? Heb ik deze nodig?
        if keynames:
            for name, mods in keynames:
                stdkeys[(_translate_keynames(name), mods)].append((context, oms))

    return stdkeys, contexts_list


def get_cmddict(path, stdkeys):
    """build dictionary of commands with descriptions

    input:
        pad (zoals opgegeven in DC_CMDS -- cmds.html in de docs directory)
    resultaat:
        een mapping met key = commandonaam en value = een tekst (de omschrijving)
        een mapping met key = een tuple van keyname, modifiers en value = een list
            (eigenlijk set) van commandonamen (meestal 1?)
        een mapping met key = commandonaam en value = een list van tuples van
            naam, waardebereik en omschrijving
        een mapping met key = categorie en value = een list van commandonamen
    """
    with open(path) as doc:
        soup = bs.BeautifulSoup(doc, 'lxml')

    ## newsoup = soup.find('div', class_='dchelpage')
    newsoup = soup.select('div[class="dchelpage"]')[0]

    categories = {}
    cmddict, dflt_assign, cmdparms = {}, {}, {}
    for div in newsoup.children:
        if not div.name or div.name != 'div':
            continue
        for hx in div.children:
            if not hx.name or hx.name != 'h2':
                continue
            for a in hx.children:
                if a.name == 'a':
                    cat = a['name']
                    if cat.startswith('cat'):
                        cat = cat[3:]
                        cd, da, cp, cl = analyze_keydefs(div, cat)
                        cmddict.update(cd)
                        dflt_assign.update(da)
                        cmdparms.update(cp)
                        categories[cat] = cl
    return cmddict, dflt_assign, cmdparms, categories


def get_toolbarcmds(path):
    """lees de zelfgedefinieerde toolbar items

    om deze te kunnen koppelen aan de betreffende keyboard shortcuts
    """
    data = ET.parse(path)
    root = data.getroot()
    tbcmddict = collections.defaultdict(list)
    for toolbar in list(root.find('Toolbars')):
        for row in list(toolbar):
            for item in row.findall('Program'):
                key = item.find('ID').text
                desc = item.find('Hint').text
                cmd = item.find('Command').text
                parm = item.find('Params').text
                tbcmddict[key] = (desc, cmd, parm)
    return tbcmddict

def analyze_keydefs(root, cat_name):
    """build the data for a specific category (corresponds with a section in the
    html)
    """
    cmddict, cmdparms = {}, {}
    dflt_assign = collections.defaultdict(set)
    command_list = []

    for tbl in root.children:
        if not tbl.name or tbl.name != 'table':
            continue
        for row in tbl.children:
            if not row.name or row.name != 'tr':
                continue
            if 'class' in row.attrs and row['class'] in ('rowcategorytitle',
                                                         'rowsubtitle'):
                continue
            command, defkey, params, desctable = '', '', [], []

            for col in row.children:
                if not col.name or col.name != 'td':
                    continue
                if 'class' not in col.attrs:
                    continue

                if "cmdcell" in col['class']:
                    ## print([x.name for x in col.children])
                    ## for item in col.findall('div', recursive=False):
                    for item in col.children:
                        if not item.name or item.name != 'div':
                            continue
                        if 'cmdname' in item['class']:
                            command = item.a.text
                        elif 'longcmdname' in item['class']:
                            command = item.a.text
                        elif 'shrtctkey' in item['class']:
                            defkey = item.text
                elif "cmdhintcell" in col['class']:
                    desctable = []
                    for item in col.children:
                        ## if command == 'cm_DirHistory':
                            ## print(item.name, end=', ')
                        if not item.name:
                            desctable.append(item)
                        elif item.name != 'table':
                            desctable.append(item.get_text())
                        elif "innercmddesc" in item['class']:
                            for line in item.children:
                                if line.name != 'tr': continue
                                name = value = desc = ''
                                for cell in line.children:
                                    if cell.name != 'td': continue
                                    if 'class' not in cell.attrs:
                                        desctable.append(cell.text)
                                        continue
                                    if "innerdescparamcell" in cell['class']:
                                        name = cell.get_text()
                                    elif "innerdescvaluecell" in cell['class']:
                                        value = cell.get_text()
                                    elif "innerdescdesccell" in cell['class']:
                                        desc = cell.get_text()
                                params.append((name, value, desc))
                        ## else:
                            ## print(item)

            cmddesc = ' '.join([x.strip() for x in desctable if x.strip()])
            ## print('command:', command, defkey, params)
            ## print('oms:', cmddesc)
            ## print('---')
            if defkey:
                allkeys = parse_keytext(defkey)
                ## print(allkeys)
                for key, mods in allkeys:
                    test = (_translate_keynames(key), mods)
                    dflt_assign[test].add(command)  # command, cmddesc)
                    ## if cmddesc == '':
                        ## for context, desc in stdkeys[test]:
                            ## if context == 'main window':
                                ## oms = desc
                                ## break

            if command:
                command_list.append(command)
                cmddict[command] = cmddesc   # .replace('\n', '')
                if params:
                    cmdparms[command] = params

    return cmddict, dflt_assign, cmdparms, command_list


def buildcsv(page, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand

    input: het door de plugin gegenereerde scherm en een indicatie of het getoond
        moet worden
    returns: een mapping voor het csv file en een aantal hulptabellen

    """
    initial = '/home/albert/.config/doublecmd/shortcuts.scf'
    dc_keys = '/usr/share/doublecmd/doc/en/shortcuts.html'
    # or http://doublecmd.github.io/doc/en/shortcuts.html
    dc_cmds = '/usr/share/doublecmd/doc/en/cmds.html'
    # or http://doublecmd.github.io/doc/en/cmds.html
    dc_desc = os.path.join(os.path.dirname(__file__), 'descs.csv')
    dc_desc_h = ''
    dc_sett = '/home/albert/.config/doublecmd/doublecmd.xml'

    shortcuts = collections.OrderedDict()
    has_path = False
    initial = page.settings['DC_PATH']
    has_path = True
    dc_keys = page.settings['DC_KEYS']
    dc_cmds = page.settings['DC_CMDS']
    dc_desc_h = page.settings['DC_DESC']
    dc_sett = page.settings['DC_SETT']
    # except KeyError:    # TODO: save defaults as settings
    #     pass
    if dc_desc_h:
        dc_desc = dc_desc_h
    if showinfo and not has_path:
        ok = show_cancel_message(page, text=instructions)
        if not ok:
            # geeft (soms) segfault
            return
        kbfile = get_file_to_open(page, extension='SCF files (*.scf)', start=initial)
    else:
        kbfile = initial
    if not kbfile:
        return

    if dc_keys.startswith('http'):
        if not os.path.exists('/tmp/dc_files/shortcuts.html'):
            import subprocess
            subprocess.run(['wget', '-i', dc_keys, '-P', '/tmp/dc_files', '-nc'])
        dc_keys = os.path.join('/tmp/dc_files', os.path.split(dc_keys)[-1])
        dc_cmds = os.path.join('/tmp/dc_files', os.path.split(dc_cmds)[-1])

    # map toetscombinatie, context, commandonaam, argumenten en venster op een
    # gezamenlijke sleutel (volgnummer)
    # map tevens context + commando op een toetscombinatie
    keydata, definedkeys = get_keydefs(kbfile)            # alles

    # map omschrijvingen op standaard toets definities
    stdkeys, context_list = get_stdkeys(dc_keys)

    # lees gegevens tbv sneltoetsen voor zelfgedefinieerde toolbar buttons
    tbcmddict = get_toolbarcmds(dc_sett)

    # map omschrijvingen op commandonamen door de toets definities waar deze op gemapt
    # zijn te vergelijken
    cmddict, defaults, params, catdict = get_cmddict(dc_cmds, stdkeys)
    tobecompleted = {}
    for key, value in keydata.items():
        templist = list(value)
        templist.insert(2, ('X' if value != stdkeys[key] else ''))  # standard / customized
        try:
            oms = cmddict[value[3]]
        except KeyError:
            # let op: hier ontstaan ook nieuwe cmddict entries
            oms = cmddict[value[3]] = tobecompleted[value[3]] = ''
        templist.append(oms)
        # map omschrijving op toolbaritem indien van toepassing
        if templist[4] == 'cm_ExecuteToolbarItem':
            itemid = templist[5].split('=', 1)[1]
            oms, cmd, parm = tbcmddict[itemid]
            templist[7] = '{} ({} {})'.format(oms, cmd, parm)
        shortcuts[key] = tuple(templist)

    # stuur dialoog aan om beschrijvingen aan te vullen
    descfile = dc_desc
    omsdict = tobecompleted
    if showinfo:
        page.dialog_data = {'descfile': descfile, 'omsdict': omsdict}
        if show_dialog(page, DcCompleteDialog):
            # opslaan vindt plaats in de dialoog, maar de data teruggeven scheelt weer I/O
            # zoals de dialoog nu aangestuurd wordt worden de omschrijvingen opgeslagen
            #   met volgnummers in plaats van commandonaam als key
            omsdict = page.dialog_data  # page.gui.dialog_data
    # invullen in shortcuts en cmddict
    for key, value in shortcuts.items():
        for cmnd, desc in omsdict.items():
            if value[4] == cmnd:
                itemlist = list(value)
                itemlist[-1] = desc
                shortcuts[key] = tuple(itemlist)
                cmddict.update(omsdict)

    # geen idee of ik deze nog ergens uit kan afleiden
    only_for = ['', 'Command Line', 'Files Panel', 'Quick Search']
    contexts = ['Main', 'Copy/Move Dialog', 'Differ', 'Edit Comment Dialog', 'Viewer']

    return shortcuts, {'stdkeys': stdkeys, 'defaults': defaults, 'cmddict': cmddict,
                       'restrictions': only_for, 'contexts': contexts, 'definedkeys': definedkeys,
                       'context_list': context_list, 'cmdparms': params, 'catdict': catdict}


how_to_save = """\
Instructions to load the changed definitions back into Double Commander.


After you've saved the definitions to a .scf file, go to
Configuration > Options > Hot keys, and select it in the
top left selector.

You may have to close and reopen the dialog to see the changes.
"""


def build_shortcut(key, mods):
    """return text for key combo
    """
    mod2str = (('C', 'Ctrl+'), ('S', 'Shift+'), ('A', 'Alt+'), ('W', 'WinKey+'))
    result = ''
    for x, y in mod2str:
        if x in mods:
            result += y
    key = key.capitalize()
    return result + key


def savekeys(page):
    """schrijf de gegevens terug
    """
    ok = show_cancel_message(page, text=how_to_save)
    if not ok:
        return
    kbfile = get_file_to_save(page, extension='SCF files (*.scf)', start=page.settings['DC_PATH'])
    if not kbfile:
        return
    root = ET.Element('doublecmd', DCVersion="0.6.6 beta")
    head = ET.SubElement(root, 'Hotkeys', Version="20")
    oldform = ''
    for item in sorted(page.data.values(), key=lambda x: x[3]):
        key, mods, kind, context, cmnd, parm, ctrl, desc = item
        if context != oldform:
            newform = ET.SubElement(head, 'Form', Name=context)
            oldform = context
        hotkey = ET.SubElement(newform, 'Hotkey')
        shortcut = ET.SubElement(hotkey, 'Shortcut')
        shortcut.text = build_shortcut(key, mods)
        command = ET.SubElement(hotkey, 'Command')
        command.text = cmnd
        if parm:
            param = ET.SubElement(hotkey, 'Param')
            param.text = parm
        if ctrl:
            control = ET.SubElement(hotkey, 'Control')
            control.text = ctrl
    shutil.copyfile(kbfile, kbfile + '.bak')
    ET.ElementTree(root).write(kbfile, encoding="UTF-8", xml_declaration=True)


#
# stuff for gui elements
#
def add_extra_attributes(win):
    """stuff needed for redefining keyboard combos

    key, mods, cmnd, params, controls
    """
    win.init_origdata += ['', '']
    win.commandsdict = win.otherstuff['cmddict']
    win.commandslist = sorted(win.commandsdict.keys())
    win.descriptions = win.commandsdict  # is this correct?
    win.contextslist = win.otherstuff['contexts']
    # not entirely correct, but will have to do for now
    win.contextactionsdict = {x: win.commandslist for x in win.contextslist}
    win.controlslist = win.otherstuff['restrictions']


def get_frameheight():
    """return fixed height for extra panel
    """
    return 120


def on_combobox(win, cb, text):
    """callback from GUI
    """
    print('in dckeys on_combobox')
    hlp = win.gui.get_combobox_selection(cb)
    if text != hlp:
        text = hlp
    win.defchanged = False
    if cb == win.gui.cmb_controls:
        if text != win._origdata[win.gui.ix_controls]:
            win._newdata[win.gui.ix_controls] = text
            if not win.gui.initializing_keydef:
                win.defchanged = True
                if 'C_CMD' in win.fields:
                    win.gui.enable_save(True)
        elif win.gui.get_combobox_text(win.cmb_commando) == win._origdata[win.ix_cmd]:
            win.defchanged = False
            if 'C_CMD' in win.fields:
                win.gui.enable_save(False)


def captions_extra_fields(win):
    """to be called on changing the language
    """
    win.gui.set_label_text(win.gui.lbl_parms, win.captions['C_PARMS'])
    win.gui.set_label_text(win.gui.lbl_controls, win.captions['C_CTRL'])


def on_extra_selected(win, newdata):
    """callback on selection of an item

    velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
    win._origdata[win.ix_parms] = newdata[win.ix_parms]
    win._origdata[win.ix_controls] = newdata[win.ix_controls]


def vul_extra_details(win, indx, item):
    """refresh nonstandard fields on details screen
    """
    if win.column_info[indx][0] == 'C_PARMS':
        win.gui.set_textfield_value(win.gui.txt_parms, item)
        win._origdata[win.gui.ix_parms] = item
    elif win.column_info[indx][0] == 'C_CTRL':
        # ix = win.controlslist.index(item)  # TODO: adapt for multiple values
        win.gui.set_combobox_string(win.gui.cmb_controls, item, win.controlslist)
        win._origdata[win.gui.ix_controls] = item
