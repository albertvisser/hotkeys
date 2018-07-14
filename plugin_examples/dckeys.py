"""HotKeys plugin for Double Commander PyQt5 version

gebaseerd op versie 0.7
matcht met de .1 versies n de dc_data directory
"""
from __future__ import print_function

import os
## import sys
## import string
import collections
import functools
import shutil
import xml.etree.ElementTree as ET
import bs4 as bs  # import BeautifulSoup
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
## import PyQt5.QtCore as core
from .completedialog import DcCompleteDialog

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
        keyname = test[-1]
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
    # read the key definitions file
    data = ET.parse(path)

    # (re)build the definitions for the csv file
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

    return keydata, keydata_2   # , all_contexts, all_controls


def get_stdkeys(path):
    """determine standard keys

    keyname moet nog verder opgesplitst worden, in elk geval de modifiers nog apart
    en sommige kunnen meer combo's (gescheiden door komma's) bevatten
    NB splitsen op + geeft soms onjuist resultaat (bv bij Num +)

    input:
        pad (zoals opgegeven in DC_KEYS -- shortcuts.html in de docs directory)
    resultaat:
        een mapping met key = een tuple van keyname, modifiers en value = een tuple
            van context en omschrijving
        een list met mogelijke contexts

    NB onderstaande staan vermeld in docs/shortcuts.html en komen toch niet in het
    csv file terecht - vermoedelijk omdat hier geen commando bij vermeld staat2
    waardoor ze niet gekoppeld worden
        Keydef,Backspace, , ,Main, , , ,Go to parent directory
        Keydef,Enter,S, ,Main, , , ,execute command in terminal (choose in options)
        Keydef,F4,A, ,Main, , , ,Exit
        Keydef,Insert, , ,Main, , , ,Select item
        Keydef,Left, , ,Main, , , ,Go to parent directory
        Keydef,Right, , ,Main, , , ,Go into directory
        Keydef,Space, , ,Main, , , ,Select item
        Keydef,Tab, , ,Main, , , ,switch between panels
        Keydef,Tab,S, ,Main, , , ,"switch between panels, other way"
         (deze heb ik zelf toegevoegd
         raar overigens dat ik die key wel in het nieuwe file krijg:
        Keydef,Tab,S, ,Main,cm_NextGroup, , ,
         maar dat deze in de preferences niet is terug te vinden)
    """
    try:
        with open(path) as doc:
            soup = bs.BeautifulSoup(doc)
    except FileNotFoundError:
        raise

    stdkeys = collections.defaultdict(list)
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
                    keynames = parse_keytext(test[0].text)  # kan meer dan 1 key / keycombo bevatten
                else:
                    oms = col.text  # zelfde omschrijving als uit cmd's ? Heb ik deze nodig?
            for name, mods in keynames:
                stdkeys[(_translate_keynames(name), mods)].append((context, oms))

    return stdkeys


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
    cmddict = {}
    dflt_assign = collections.defaultdict(list)  # kan wrschl een gewone dict zijn?

    with open(path) as doc:
        soup = bs.BeautifulSoup(doc)

    div = soup.find_all('div', class_='CHAPTER')[0]
    tbody = div.select('div > table > tbody > tr')

    for row in tbody:
        command = defkey = oms = ''
        for col in row.find_all('td', recursive=False):
            ## test = col.select('tt > div > a')
            test = col.select('tt > div')
            if test:
                command = test[0].a.text
                defkey = test[1].text
            else:
                # I could use the entire text and pass everything to an editing screen
                # but for now just split off the first part
                oms = col.get_text().split('\n')[0]
                ## oms = ''
                ## for item in col.contents:
                    ## if isinstance(item, bs.Tag):
                        ## if item.name == 'br':
                            ## break
                        ## else:
                            ## oms += item.text
                    ## else:
                        ## oms += str(item)
        if defkey:
            allkeys = parse_keytext(defkey)
            for key, mods in allkeys:
                test = (_translate_keynames(key), mods)
                dflt_assign[test].append((command, oms))  # command)
                if oms == '':
                    for context, desc in stdkeys[test]:
                        if context == 'main window':
                            oms = desc
                            break

        cmddict[command] = oms

    return cmddict, dflt_assign


def buildcsv(parent, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand

    input: het door de plugin gegenereerde scherm en een indicatie of het getoond
        moet worden
    returns: een mapping voor het csv file en een dict met aantal hulptabellen
        of bij een fout een toepasselijke foutmelding (1 parameter ipv 2)

    # parse shortcuts.scf into keydata and definedkeys:
    #   keydata[key] = (keyname, modifiers, context, command, parameter, controls)
    #   definedkeys[(keyname, modifiers)].append((context, command))
    # parse shortcuts.html into stdkeys
    #   # stdkeys[(_translate_keynames(name), mods)].append((context, oms))
    # use stdkeys to parse cmds.html into cmddict and defaults
    #   # cmddict[command] = oms
    #   # defaults[(_translate_keynames(key), mods)].append((command, oms))
    # use keydata and cmddict to create shortcuts dict
    """
    try:
        parent.page
    except AttributeError:
        has_page = False
    else:
        has_page = True

    initial = '/home/albert/.config/doublecmd/shortcuts.scf'
    dc_keys = '/usr/share/doublecmd/doc/en/shortcuts.html'
    dc_cmds = '/usr/share/doublecmd/doc/en/cmds.html'
    dc_desc = ''

    shortcuts = collections.OrderedDict()
    has_path = False
    has_descpath = os.path.exists(dc_desc)
    if has_page:
        try:
            initial = parent.page.settings['DC_PATH']
            has_path = True
            dc_keys = parent.page.settings['DC_KEYS']
            dc_cmds = parent.page.settings['DC_CMDS']
            dc_desc = parent.page.settings['DC_DESC']
            has_descpath = True
        except KeyError:
            pass

    if showinfo and not has_path:
        ok = qtw.QMessageBox.information(parent, parent.title, instructions,
                                         qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        if ok == qtw.QMessageBox.Cancel:
            return {}, {}
        kbfile = qtw.QFileDialog.getOpenFileName(parent, parent.captions['C_SELFIL'],
                                                 directory=initial,
                                                 filter='SCF files (*.scf)')[0]
    else:
        kbfile = initial
    if not kbfile:
        return 'No path to shortcut definitions given'

    initial = os.path.dirname(__file__)
    if showinfo and not has_descpath:
        message = 'Descriptions file `{}` does not exist, redefine?'.format(dc_desc)
        ok = qtw.QMessageBox.information(parent, parent.title, message,
                                         qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        if ok == qtw.QMessageBox.Cancel:
            return {}, {}
        dc_desc = qtw.QFileDialog.getOpenFileName(parent, parent.captions['C_SELFIL'],
                                                  directory=initial,
                                                  filter='CSV files (*.csv)')[0]
        if dc_desc:
            parent.page.settings['DC_DESC'] = dc_desc
            parent.page.settings['extra']['DC_DESC'] = 'path to descriptions file'
    ## else:
        ## kbfile = initial
    ## if not dc_desc:
        ## return {}, {}

    # map toetscombinatie, context, commandonaam, argumenten en venster op een
    # gezamenlijke sleutel (volgnummer)
    # map tevens context + commando op een toetscombinatie
    ## keydata, definedkeys, contexts, controls = get_keydefs(kbfile)            # alles
    keydata, definedkeys = get_keydefs(kbfile)            # alles

    # map omschrijvingen op standaard toets definities
    stdkeys = get_stdkeys(dc_keys)

    # map omschrijvingen op commandonamen door de toets definities waar deze op gemapt
    # zijn te vergelijken
    # ## cmddict, defaults, params, catdict = get_cmddict(dc_cmds, stdkeys) ##
    # ## dit /\ is een 0.8 wijziging, werkt die misschien nu ook al?                   ##
    cmddict, defaults = get_cmddict(dc_cmds, stdkeys)
    ## return keydata, {'stdkeys': stdkeys, 'defaults': defaults,
                       ## 'cmddict': cmddict, 'definedkeys': definedkeys}
    tobecompleted = {}
    # WIP: complete this stuff (commented out for now).
    # alternatively, we can do this /after/ building the shortcuts list
    # But I think this is a better place
    # compare mappings in stdkeys and defaults to see if any are missing
    # stdkeys: maps key + mods to context + description
    # defaults: maps key+mods to cm_code _ description
    # but stdkeys is input for getting defaults??
    # ## # if descriptions are missing, simply add them; otherwise we need to choose which one
    # ## # to use (the longest?)
    # ## with open('dc_cmddict_before', 'w') as _o:
    #     ## for x, y in sorted(cmddict.items()):
    #         ## print(x, y, file=_o)
    # ## # if any empty ones are left, feed them to the dialog
    # ## tobecompleted = {x: y for x, y in cmddict.items() if y == ''}
    # ## with open('tobecompleted', 'w') as _o:
    #     ## for x, y in sorted(tobecompleted.items()):
    #         ## print(x, y, file=_o)
    # ## cmddocsfile = '/home/albert/.config/doublecmd/extratexts'
    # ## if has_page:
    #     ## try:
    #         ## cmddocsfile = parent.page.settings['DC_DESC']
    #     ## except KeyError:
    #         ## pass
    # ## if showinfo:
    #     ## parent.complete_data = {'data': tobecompleted, 'dc_text': cmddocsfile}
    #     ## dlg = CompleteDialog(parent).exec_()
    #     ## if dlg == qtw.QDialog.accepted:
    #         ## tobecompleted = parent.complete_data['data']
    #         ## cmddocsfile = parent.complete_data['dc_text']
    #         ## parent.page.settings['DC_DESC'] = (cmddocsfile,
    #             ## "File containing command descriptions that aren't in cmds.html")
    for key, value in keydata.items():
        templist = list(value)
        val = ''  # standard / customized
        # if keydef_from_keydata != keydef_from_stdkeys:
        #     value = 'X'
        templist.insert(2, val)
        try:
            oms = cmddict[value[3]]
        except KeyError:
            # let op: hier ontstaan ook nieuwe cmddict entries
            oms = cmddict[value[3]] = tobecompleted[value[3]] = ''
        templist.append(oms)
        shortcuts[key] = tuple(templist)

    """een probleempje (iets om iets aan te doen in elk geval):
    in de interne aanpas dialoog en in het shift F12 tool heb ik drie commando's
    cm_CloseTab, cm_CloseAllTabs en cm_CloseDuplicateTabs. In de html zitten alleen
    de eerste twee en heten ze Remove... in plaats van Close...
    """
    # # hier zijn pas entries ontstaan zonder omschrijving
    # #mogelijk omdat commando's in het scf file en de html niet overeenkoen
    #
    # ## if tobecompleted:
    #
    #     ## # open dialog to complete missing descriptions (as above)
    #     ## # afterwards: fill in completed descriptions
    #     ## for key, value in tobecompleted:
    #         ## if value:
    #             ## cmddict[key] = tobecompleted[key]
    #     ## for key, value in shortcuts

    ## print("vóór dialoog:\n", tobecompleted)
    ## print(dc_desc)
    # stuur dialoog aan om beschrijvingen aan te vullen
    descfile = dc_desc
    omsdict = tobecompleted
    if showinfo and dc_desc:
        dlg = DcCompleteDialog(parent, descfile, omsdict).exec_()
        if dlg == qtw.QDialog.Accepted:
            # opslaan vindt plaats in de dialoog, maar de data teruggeven scheelt weer I/O
            # zoals de dialoog nu aangestuurd wordt worden de omschrijcingen opgeslagen
            #   met volgnummers in plaats van commandonaam als key
            omsdict = parent.dialog_data
    ## print('resultaat na dialoog:\n', omsdict)
    # invullen in shortcuts en cmddict
    for key, value in shortcuts.items():
        for cmnd, desc in omsdict.items():
            if value[4] == cmnd:
                itemlist = list(value)
                itemlist[-1] = desc
                shortcuts[key] = tuple(itemlist)
                cmddict.update(omsdict)

    only_for = ['', 'Command Line', 'Files Panel', 'Quick Search']
    contexts = ['Main', 'Copy/Move Dialog', 'Differ', 'Edit Comment Dialog',
                'Viewer']
    return shortcuts, {'stdkeys': stdkeys, 'defaults': defaults,
                       'cmddict': cmddict, 'restrictions': only_for,
                       'contexts': contexts, 'definedkeys': definedkeys}
                       # , 'manual_cmdoms': tobecompleted}
# omschrijvingen o.m. in cmddict? Maar wel iets bijhouden voor het geval niet aanwezig

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


def savekeys(parent):
    """schrijf de gegevens terug
    """
    ok = qtw.QMessageBox.information(parent, parent.title, how_to_save,
                                     qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
    if ok == qtw.QMessageBox.Cancel:
        return
    kbfile = qtw.QFileDialog.getSaveFileName(parent, parent.captions['C_SELFIL'],
                                             directory=parent.settings['DC_PATH'],
                                             filter='SCF files (*.scf)')
    if not kbfile:
        return
    root = ET.Element('doublecmd', DCVersion="0.6.6 beta")
    head = ET.SubElement(root, 'Hotkeys', Version="20")
    oldform = ''
    for item in sorted(parent.data.values(), key=lambda x: x[3]):
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

# stuff for gui elements


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
    hlp = cb.currentText()
    if text != hlp:
        text = hlp
    win.defchanged = False
    if cb == win.cmb_controls:
        if text != win._origdata[win.ix_controls]:
            win._newdata[win.ix_controls] = text
            win.defchanged = True
            win.b_save.setEnabled(True)
        elif str(win.cmb_controls.currentText()) == win._origdata[win.ix_controls]:
            win.b_save.setEnabled(False)


def add_extra_fields(win, box):
    """fields showing details for selected keydef, to make editing possible
    """
    win.lbl_parms = qtw.QLabel(box)
    win.txt_parms = qtw.QLineEdit(box)
    win.txt_parms.setMaximumWidth(280)
    win.screenfields.append(win.txt_parms)
    win.ix_parms = 7
    win.lbl_controls = qtw.QLabel(box)
    cb = qtw.QComboBox(box)
    cb.addItems(win.controlslist)
    cb.currentIndexChanged[str].connect(functools.partial(on_combobox, win, cb, str))
    win.screenfields.append(cb)
    win.cmb_controls = cb
    win.ix_controls = 8


def layout_extra_fields(win, layout):
    """add the extra fields to the layout
    """
    sizer2 = qtw.QGridLayout()
    line = 0
    sizer2.addWidget(win.lbl_parms, line, 0)
    sizer2.addWidget(win.txt_parms, line, 1)
    line += 1
    sizer2.addWidget(win.lbl_controls, line, 0)
    sizer3 = qtw.QHBoxLayout()
    sizer3.addWidget(win.cmb_controls)
    sizer3.addStretch()
    sizer2.addLayout(sizer3, line, 1)
    layout.addLayout(sizer2, 1)


def captions_extra_fields(win):
    """to be called on changing the language
    """
    win.lbl_parms.setText(win.captions['C_PARMS'] + ':')
    win.lbl_controls.setText(win.captions['C_CTRL'] + ':')


def on_extra_selected(win, newdata):
    """callback on selection of an item

    velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
    win._origdata[win.ix_parms] = newdata[win.ix_parms]
    win._origdata[win.ix_controls] = newdata[win.ix_controls]


def vul_extra_details(win, indx, item):
    """refresh nonstandard fields on details screen
    """
    if win.column_info[indx][0] == 'C_PARMS':
        win.txt_parms.setText(item)
        win._origdata[win.ix_parms] = item
    elif win.parent.column_info[indx][0] == 'C_CTRL':
        ix = win.controlslist.index(item)  # TODO: adapt for multiple values
        win.cmb_controls.setCurrentIndex(ix)
        win._origdata[win.ix_controls] = item

#
