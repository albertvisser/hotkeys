"""HotKeys plugin for Double Commander PyQt5 version

gebaseerd op versie 0.8
"""
from __future__ import print_function

import os
import collections
import shutil
import csv
import xml.etree.ElementTree as ET
import bs4 as bs  # import BeautifulSoup
from ..gui import (show_cancel_message, get_file_to_open, get_file_to_save, show_dialog,
                   ask_ync_question)
from .dckeys_gui import add_extra_fields, layout_extra_fields, DcCompleteDialog

CONFPATH = '/home/albert/.config/doublecmd'
DOCSPATH = '/usr/share/doublecmd/doc/en'
HERE = os.path.dirname(__file__)

instructions = """\
Instructions for rebuilding the keyboard shortcut definitions


The keydefs are stored in a file called shortcuts.scf,
located in ~/.config/doublecmd.
For convenience sake, you can store this name in a setting
named DC_PATH so that the buildcsv and savekeys functions
don't have to ask for a filename every time.

Two extra settings are used to extract the default mappings
and the command definitions from the help files: DC_KEYS and
DC_CMDS respectively.

Two more settings are used to store and extract information
that is needed but not (yet) provided in the above files:
DC_DESC for missing descriptions and DC_MATCH for keydefs
that can't be automatically matched to internal commands.
These can be entered using extra dialogs that will be
presented following this message.

Inside Double Commander, in Configuration > Options > Hot keys,
it's (theoretically) possible to select the shortcuts file, so
support for using a name different from the DC_PATH setting is
present.
Do you want to select the shortcuts file yourself (choose "No"
to stick to the DC_PATH setting)?"
"""


def _shorten_mods(modifier_list):
    """replace modifier names with their first letters and in a fixed sequence
    """
    result = ''
    for values, outval in ((('Ctrl', 'CTRL', 'CLTR'), 'C'), (('Alt', 'ALT'), 'A'),
                           (('Shift', 'SHIFT'), 'S'), (('WinKey',), 'W')):
        for test in values:
            if test in modifier_list:
                result += outval
                break
    # if 'Ctrl' in modifier_list or 'CTRL' in modifier_list:
    #     result += 'C'
    # if 'Alt' in modifier_list or 'ALT' in modifier_list:
    #     result += 'A'
    # if 'Shift' in modifier_list or 'SHIFT' in modifier_list:
    #     result += 'S'
    # if 'WinKey' in modifier_list:
    #     result += 'W'
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


def get_keydefs(data):
    """huidige keydefs afleiden

    input:
        met ElementTree ingelezen data volgens pad zoals opgegeven in DC_PATH
        (shortcuts.scf in de settings directory)
    resultaat:
        een mapping met key = een volgnummer, value = een tuple van keyname,
            modifiers, context, command, parameter en controls
        een mapping met key = een tuple van keyname, modifiers en value = een tuple
            van context en command

    """
    keydata = collections.OrderedDict()
    keydata_2 = {}
    all_contexts = set()
    all_controls = set()
    key = 0
    root = data.getroot()
    for form in list(root.find('Hotkeys')):
        context = form.get('Name')
        all_contexts.add(context)
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
                all_controls.add(controls)
            else:
                controls = []
                for control in test:
                    controls.append(control.text)
                    all_controls.add(control.text)
                controls = ';'.join(controls)
            key += 1
            keydata[key] = (keyname, modifiers, context, command, parameter, controls)
            keydata_2[(keyname, modifiers, context)] = command

    return keydata, keydata_2, all_contexts, all_controls


def get_stdkeys(soup):
    """determine standard keys

    input:
        met BeautifulSoup ingelezen data volgens pad zoals opgegeven in DC_KEYS
        (shortcuts.html in de docs directory)
    resultaat:
        een mapping met key = een tuple van keyname, modifiers en value = een tuple
            van context en omschrijving
        een list met mogelijke contexts
    """
    stdkeys = {}
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
            if keynames:
                for name, mods in keynames:
                    stdkeys[(_translate_keynames(name), mods, context)] = oms

    return stdkeys, contexts_list


def get_cmddict(soup):
    """build dictionary of commands with descriptions

    input:
        met BeautifulSoup ingelezen data volgens pad zoals opgegeven in DC_CMDS
        (cmds.html in de docs directory)
    resultaat:
        een mapping met key = commandonaam en value = een tekst (de omschrijving)
        een mapping met key = een tuple van keyname, modifiers en value = een list
            (eigenlijk set) van commandonamen (meestal 1?)
        een mapping met key = commandonaam en value = een list van tuples van
            naam, waardebereik en omschrijving
        een mapping met key = categorie en value = een list van commandonamen
    """
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
                        cd, da, cp, cl = analyze_keydefs(div)  # , cat)
                        cmddict.update(cd)
                        dflt_assign.update(da)
                        cmdparms.update(cp)
                        categories[cat] = cl
    return cmddict, dflt_assign, cmdparms, categories


def get_toolbarcmds(data):
    """lees de zelfgedefinieerde toolbar items

    input:
        met ElementTree ingelezen data volgens pad zoals opgegeven in DC_SETT
        (doublecmd.xml in de settings directory)
    resultaat:
        een mapping met key = de parameter voor cm_ToolBarCmd
        om de details in value te kunnen koppelen aan de betreffende keyboard shortcuts
    """
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


def analyze_keydefs(root):  # , cat_name):
    """build the data for a specific category (corresponds with a section in the
    html)

    input:
        met BeautifulSoup geparsede node data
    resultaat:
        gegevens om toe te voegen aan de output van get_cmddict
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
                    for item in col.children:
                        if not item.name or item.name != 'div':
                            continue
                        if 'cmdname' in item['class']:
                            command = item.a.text.strip('.')
                        elif 'longcmdname' in item['class']:
                            command = item.a.text.strip('.')
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

            cmddesc = ' '.join([x.strip() for x in desctable if x.strip()]).strip(' .')
            if defkey:
                allkeys = parse_keytext(defkey)
                for key, mods in allkeys:
                    test = (_translate_keynames(key), mods)
                    dflt_assign[test].add(command)  # (command, cmddesc))

            if command:
                command_list.append(command)
                cmddict[command] = cmddesc   # .replace('\n', '')
                if params:
                    cmdparms[command] = params

    return cmddict, dflt_assign, cmdparms, command_list


def get_shortcuts(keydata, stdkeys, definedkeys, cmddict, tbcmddict, defaults):
    """combineer keydata met gegevens uit de dictionaries met omschrijvingen

    bepaal tegelijkertijd of dit een standaard definitie is of een aangepaste
    """
    shortcuts = collections.OrderedDict()
    tobecompleted = {}
    tobematched = {}
    for key, value in keydata.items():
        templist = list(value)
        keycombo = tuple([value[0], value[1], value[2].lower().replace('main', 'main_window')])
        standard = 'S' if defaults.get(keycombo[:2]) == {value[3]} else ''
        desc = stdkeys.get(keycombo, '')
        if desc and value[3] in cmddict:
            if desc == cmddict[value[3]]:
                standard = 'S'
            else:
                tobematched[tuple(templist[:3])] = desc, value[3]  # voorgift
        templist.insert(2, standard)
        if templist[4] == 'cm_ExecuteToolbarItem':
            templist[2] = 'U'
            itemid = templist[5].split('=', 1)[1]
            oms, cmd, parm = tbcmddict[itemid]
            templist.append('{} ({} {})'.format(oms, cmd, parm))
        else:
            try:
                oms = cmddict[value[3]]
            except KeyError:
                # let op: hier ontstaan ook nieuwe cmddict entries
                oms = cmddict[value[3]] = tobecompleted[value[3]] = ''
            templist.append(oms)
        shortcuts[key] = tuple(templist)
    for stdkey, value in stdkeys.items():
        # definedkeys is een "dictionary versie" van keydata met dezelfde sleutel als stdkeys
        context = stdkey[2].split('_')[0].title()
        dictkey = tuple([stdkey[0], stdkey[1], context])
        if dictkey not in definedkeys:
            key += 1
            shortcuts[key] = (stdkey[0], stdkey[1], 'S', context, '', '', '', value)
    for value in shortcuts.values():
        dictkey = tuple([value[0], value[1], value[3]])
        if not value[2] and dictkey not in tobematched:
            tobematched[dictkey] = value[-1], ''   # geen voorgift
    return shortcuts, tobematched, tobecompleted, cmddict


def get_desc(page, showinfo, descdict, tobecompleted, cmddict):
    """load descriptions from file, update in dialog if requested, filter out stuff that's
    already in standard
    """
    if showinfo:
        # WIP: feed dialog with data instead of filename
        page.dialog_data = {'descdict': descdict, 'omsdict': tobecompleted}
        if show_dialog(page, DcCompleteDialog):
            descdict = page.dialog_data
    else:
        # print('eigen descriptions:', descdict)
        # print('dc commands:', cmddict)
        iter_ = list(descdict.keys())
        for key in iter_:
            # print(key)
            if key in cmddict and cmddict[key]:
                # print(cmddict[key])
                descdict.pop(key)
        # print('eigen descriptions na schonen:', descdict)
    return descdict


def update_from_descdict(cmddict, shortcuts, descdict):
    """add extra descriptions into keydefs and cmddict dictionaries
    """
    for key, value in shortcuts.items():
        for cmnd, desc in descdict.items():
            if value[4] == cmnd:
                itemlist = list(value)
                itemlist[-1] = desc
                shortcuts[key] = tuple(itemlist)
    cmddict.update(descdict)
    return cmddict, shortcuts


def match_stuff(page, showinfo, shortcuts, tobematched):
    """match commands from cmddict (?) to commands from descriptions (?)
    """
    for key, value in tobematched.items():
        keycombo, context = key[:2], key[2]
        for item in shortcuts.values():
            if keycombo == item[:2] and context == item[3] and not value[0]:
                tobematched[key] = (item[-1], value[1])

    # TODO build matcher dialog
    # if showinfo:
    #     page.dialog_data = {'matchfile': dc_match, 'matchict': tobematched}
    #     if show_dialog(page, DcMatchDialog):
    #         # opslaan vindt plaats in de dialoog, maar de data teruggeven scheelt weer I/O
    #         matchdict = page.dialog_data
    # for key, value in shortcuts.items():
    #     keydict = (value[0], value[1], value[3])
    #     if not value[2]:
    #         shortcuts[key][2] = matchdict[dictkey]
    return shortcuts, tobematched


def buildcsv(page, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand

    input: het door de plugin gegenereerde scherm en een indicatie of het getoond
        moet worden
    returns: een mapping voor het csv file en een aantal hulptabellen

    1. get keyboard definitions file name
    2. get names of other settings files
    3. map toetscombinatie, context, commandonaam, argumenten en venster op een
       gezamenlijke sleutel (volgnummer)
       map tevens context + commando op een toetscombinatie
    4. map omschrijvingen op standaard toets definities
    5. lees gegevens tbv sneltoetsen voor zelfgedefinieerde toolbar buttons
    6. map omschrijvingen op commandonamen door de toets definities waar deze op gemapt
       zijn te vergelijken
       tevens staan er wat default assignments in dit file beschreven
    7. vul definities aan en bepaal ontbrekende beschrijvingen
    8. stuur dialoog aan om beschrijvingen aan te vullen
    9. beschrijvingen aanvullen in shortcuts en cmddict
    10. beschrijvingen aanvullen in tobematched
    11. start matcher dialoog voor de entries die nog geen waarde voor "standard" hebben
        dan wel een dialoog waarin je kunt aangeven welke definities je zelf gemaakt hebt
        tobematched is een dictionary met sleutel key, modifiers en context
        de waarde bestaat uit een omschrijving en eventueel een commando dat waarschijnlijk
        hetgene is dat het moet zijn
    """
    initial = page.settings.get('DC_PATH', '')
    if initial:
        kbfile = initial
        new_setting = False
    else:
        initial = os.path.join(CONFPATH, 'shortcuts.scf')
        new_setting = True
    kbfile = initial
    if showinfo:
        # ok = show_cancel_message(page.gui, text=instructions)
        ok, cancel = ask_ync_question(page.gui, text=instructions)
        if cancel:
            return None
        if ok:
            kbfile = get_file_to_open(page.gui, extension='SCF files (*.scf)', start=initial)
    if not kbfile:
        return None
    if new_setting:
        page.settings['DC_PATH'] = kbfile

    dc_keys = page.settings.get('DC_KEYS', '')
    if not dc_keys:
        dc_keys = page_settings['DC_KEYS'] = os.path.join(DOCSPATH, 'shortcuts.html')
    dc_cmds = page.settings.get('DC_CMDS', '')
    if not dc_cmds:
        dc_cmds = page.settings['DC_CMDS'] = os.path.join(DOCSPATH, 'cmds.html')
    if dc_keys.startswith('http'):
        # http://doublecmd.github.io/doc/en/shortcuts.html
        # http://doublecmd.github.io/doc/en/cmds.html
        if not os.path.exists('/tmp/dc_files/shortcuts.html'):
            import subprocess
            subprocess.run(['wget', '-i', dc_keys, '-P', '/tmp/dc_files', '-nc'])
        dc_keys = os.path.join('/tmp/dc_files', os.path.basename(dc_keys))
        dc_cmds = os.path.join('/tmp/dc_files', os.path.basename(dc_cmds))
    dc_sett = page.settings.get('DC_SETT', '')
    if not dc_sett:
        dc_sett = page.settings['DC_SETT'] = os.path.join(CONFPATH, 'doublecmd.xml')
    dc_desc = page.settings.get('DC_DESC', '')
    if not dc_desc:
        dc_desc = page.settings['DC_DESC'] = os.path.join(HERE, 'dc_descs.csv')
    dc_match = page.settings.get('DC_MATCH', '')
    if not dc_match:
        dc_match = page.settings['DC_MATCH'] = os.path.join(HERE, 'dc_matches.csv')

    keydata, definedkeys, contexts, only_for = get_keydefs(ET.parse(kbfile))  #3

    with open(dc_keys) as doc:
        soup = bs.BeautifulSoup(doc, 'lxml')
    stdkeys, context_list = get_stdkeys(soup)  #4

    tbcmddict = get_toolbarcmds(ET.parse(dc_sett))  #5

    with open(dc_cmds) as doc:
        soup = bs.BeautifulSoup(doc, 'lxml')
    cmddict, defaults, params, catdict = get_cmddict(soup)  #6

    shortcuts, tobematched, tobecompleted, cmddict = get_shortcuts(keydata, stdkeys, definedkeys,
                                                                   cmddict, tbcmddict, defaults)  #7

    origdescdict = {}
    with open(dc_desc) as _in:
        rdr = csv.reader(_in)
        for key, oms in rdr:
            origdescdict[key] = oms
    descdict = get_desc(page, showinfo, origdescdict, tobecompleted, cmddict)       #8
    if descdict != origdescdict:
        if os.path.exists(dc_desc):
            shutil.copyfile(dc_desc, dc_desc + '~')
        with open(dc_desc, 'w') as _out:
            writer = csv.writer(_out)
            for key, value in new_data.items():
                if value:
                    writer.writerow((key, value))

    cmddict, shortcuts = update_from_descdict(cmddict, shortcuts, descdict)         #9

    shortcuts, tobematched = match_stuff(page, showinfo, shortcuts, tobematched)    #10, 11?

    only_for = list(only_for)
    contexts = list(contexts)
    for name in context_list:
        test = name.split('_')[0].title()
        if test not in contexts:
            contexts.append(test)

    return shortcuts, {'stdkeys': stdkeys, 'defaults': defaults, 'cmddict': cmddict,
                       'contexts': contexts, 'restrictions': only_for, 'cmdparms': params,
                       'catdict': catdict}


how_to_save = """\
Instructions to load the changed definitions back
into Double Commander.


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


def captions_extra_fields(gui):
    """to be called on changing the language
    """
    win = gui.master
    gui.set_label_text(gui.lbl_parms, win.captions['C_PARMS'])
    gui.set_label_text(gui.lbl_controls, win.captions['C_CTRL'])


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
