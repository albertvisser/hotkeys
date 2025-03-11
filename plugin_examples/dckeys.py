"""HotKeys plugin for Double Commander

gebaseerd op versie 0.8
"""
import os
import collections
import subprocess
import shutil
import csv
import xml.etree.ElementTree as ET
import bs4 as bs  # import BeautifulSoup
from ..gui import (show_cancel_message, get_file_to_open, get_file_to_save, show_dialog,
                   show_message, ask_ync_question)
from .dckeys_gui import layout_extra_fields, DcCompleteDialog

CONFPATH = '/home/albert/.config/doublecmd'
# DOCSPATH = '/usr/share/doublecmd/doc/en'
DOCSPATH = 'https:/doublecmd.github.io/doc/en'
HERE = os.path.dirname(__file__)
TEMPLOC = '/tmp/dc_files'
DCVER = "0.6.6 beta"
KBVER = "20"

instructions = """\
Instructions for rebuilding the keyboard shortcut definitions


The keydefs are stored in a file called shortcuts.scf,
located in ~/.config/doublecmd.
For convenience sake, you can store this name in a setting
named DC_PATH so that the build_data and savekeys functions
don't have to ask for a filename every time.

Two extra settings are used to extract the default mappings
and the command definitions from the help files: DC_KEYS and
DC_CMDS respectively.

A setting named DC_DESC is used to store and extract some
command descriptions that are not (yet) provided in the above
files. These can be entered using an extra dialog that is
presented following this message.

Inside Double Commander, in Configuration > Options > Hot keys,
it's (theoretically) possible to select the shortcuts file, so
support for using a name different from the DC_PATH setting is
present.
Do you want to select the shortcuts file yourself (choose "No"
to stick to the DC_PATH setting)?
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
    convert = {'↑': 'Up', '↓': 'Down', '←': 'Left', '→': 'Right', 'Delete': 'Del', 'С': 'C',
               'Pgdown': 'PgDn', 'Pgup': 'PgUp', 'Num *': 'Num*', 'Num +': 'Num+', 'Num -': 'Num-'}
    try:
        return convert[inp.strip()]
    except KeyError:
        return inp.strip()


def get_data_from_xml(filename):
    "gegevens in xml bestand bewerkbaar maken"
    return ET.parse(filename)


def get_data_from_html(filename):
    "gegevens in html bestand bewerkbaar maken"
    with open(filename) as doc:
        soup = bs.BeautifulSoup(doc, 'lxml')
    return soup


def get_data_from_csv(filename):
    "gegevens uit csv bestand lezen en bewerkbaar maken"
    result = []
    with open(filename) as _in:
        rdr = csv.reader(_in)
        result = list(rdr)  # [line for line in rdr]
    return result


def save_list_to_csv(data, filename):
    "gegevens omzetten in csv formaat en opslaan"
    if os.path.exists(filename):
        shutil.copyfile(filename, filename + '~')
    with open(filename, 'w') as _out:
        writer = csv.writer(_out)
        for line in data:
            writer.writerow(line)


def parse_keytext(text):
    """leid keynamen en modifiers op uit tekst

    geeft een list terug van keynaam - modifier-list paren
    """
    retval = []

    # uitzondering op het onderstaande
    # tekst is "Esc, Q (or with any combination Ctrl, Shift, Alt)"
    if text.startswith('Esc, Q ('):  # uitgeprobeerd: toevoeging klopt niet (bij mij)
        return [('Esc', ''), ('Q', '')]
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


def analyze_keydefs(root):  # , cat_name):
    """build the data for a specific category (corresponds with a section in the html)

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
            if 'class' in row.attrs and ('rowcategorytitle' in row['class']
                                         or 'rowsubtitle' in row['class']):
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
                        if 'cmdname' in item['class'] or 'longcmdname' in item['class']:
                            command = item.a.text.strip('.')
                        elif 'shrtctkey' in item['class']:
                            defkey = item.text
                elif "cmdhintcell" in col['class']:
                    desctable = []
                    for item in col.children:
                        # if command == 'cm_DirHistory':
                        #     print(item.name, end=', ')
                        if not item.name:
                            desctable.append(item)
                        elif item.name != 'table':
                            desctable.append(' '.join([x.strip()
                                                       for x in item.get_text().split('\n')]))
                        elif "innercmddesc" in item['class']:
                            for line in item.children:
                                if line.name != 'tr':
                                    continue
                                name = value = desc = ''
                                for cell in line.children:
                                    if cell.name != 'td':
                                        continue
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
                        # else:
                        #     print(item)

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


def build_data(page, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand

    input: het door de plugin gegenereerde scherm en een indicatie of het getoond
        moet worden
    returns: een mapping voor het csv file en een aantal hulptabellen
    """
    builder = CsvBuilder(page, showinfo)
    kbfile, dc_keys, dc_cmds, dc_sett, dc_desc = builder.get_settings_pathnames()
    # breakpoint()
    if showinfo:
        while True:
            new_kbfile = builder.check_path_setting(kbfile)
            if new_kbfile and (not kbfile or new_kbfile != kbfile):
                kbfile = page.settings['DC_PATH'] = new_kbfile
            if kbfile:
                break
            show_message(builder.page.gui, text="You MUST provide a name for the settings file")
    # map toets + context op o.a. commando
    builder.get_keydefs(get_data_from_xml(kbfile))
    # map omschrijvingen op standaard toets definities
    builder.get_stdkeys(get_data_from_html(dc_keys))
    # lees gegevens tbv sneltoetsen voor zelfgedefinieerde toolbar buttons
    builder.get_toolbarcmds(get_data_from_xml(dc_sett))
    # map omschrijvingen op commandonamen
    builder.get_cmddict(get_data_from_html(dc_cmds))
    # alles samenvoegen
    builder.assemble_shortcuts()
    # stuur dialoog aan om beschrijvingen aan te vullen
    desclist = get_data_from_csv(dc_desc)
    newdesclist = builder.add_missing_descriptions(desclist)
    if newdesclist != desclist:
        save_list_to_csv(newdesclist, dc_desc)
    # op juiste formaat brengen
    builder.format_shortcuts()
    for name in builder.contexts_list:
        test = name.split('_')[0].title()
        # if test not in builder.contexts:
            # builder.contexts.append(test)
        builder.contexts.add(test)
    return builder.shortcuts, {'stdkeys': builder.stdkeys, 'defaults': builder.defaults,
                               'cmddict': builder.cmddict, 'contexts': sorted(builder.contexts),
                               'restrictions': sorted(builder.controls), 'cmdparms': builder.params,
                               'catdict': builder.catdict}


class CsvBuilder:
    """assemble data for csv file
    """
    def __init__(self, page, showinfo):
        self.page = page
        self.showinfo = showinfo
        self.definedkeys, self.stdkeys, self.cmddict, self.tbcmddict = {}, {}, {}, {}
        self.defaults, self.params, self.catdict, self.shortcuts = {}, {}, {}, {}
        self.contexts, self.controls, self.contexts_list = set(), set(), []
        # volgens het toolbar definition scherm zijn voor controls drie waarden mogelijk:
        self.controls = {'', 'Command Line', 'Files Panel', 'Quick Search'}
        self.tobematched, self.unlisted_cmds = {}, []

    def get_settings_pathnames(self):
        """get the paths for the settings files to read
        """
        kbfile = self.page.settings.get('DC_PATH', '')
        if not kbfile:
            kbfile = self.page.settings['DC_PATH'] = os.path.join(CONFPATH, 'shortcuts.scf')
        dc_keys = self.page.settings.get('DC_KEYS', '')
        if not dc_keys:
            dc_keys = self.page.settings['DC_KEYS'] = os.path.join(DOCSPATH, 'shortcuts.html')
        if dc_keys.startswith('http') and not os.path.exists(os.path.join(TEMPLOC, 'shortcuts.html')):
            # http://doublecmd.github.io/doc/en/shortcuts.html
            subprocess.run(['wget', dc_keys, '-P', TEMPLOC, '-nc'], check=False)
        dc_keys = os.path.join(TEMPLOC, os.path.basename(dc_keys))
        dc_cmds = self.page.settings.get('DC_CMDS', '')
        if not dc_cmds:
            dc_cmds = self.page.settings['DC_CMDS'] = os.path.join(DOCSPATH, 'cmds.html')
        if dc_cmds.startswith('http') and not os.path.exists(os.path.join(TEMPLOC, 'cmds.html')):
            # http://doublecmd.github.io/doc/en/cmds.html
            subprocess.run(['wget', dc_cmds, '-P', TEMPLOC, '-nc'], check=False)
        dc_cmds = os.path.join(TEMPLOC, os.path.basename(dc_cmds))
        dc_sett = self.page.settings.get('DC_SETT', '')
        if not dc_sett:
            dc_sett = self.page.settings['DC_SETT'] = os.path.join(CONFPATH, 'doublecmd.xml')
        dc_desc = self.page.settings.get('DC_DESC', '')
        if not dc_desc:
            dc_desc = self.page.settings['DC_DESC'] = os.path.join(HERE, 'dc_descs.csv')
        return kbfile, dc_keys, dc_cmds, dc_sett, dc_desc

    def check_path_setting(self, initial):
        """show instructions and ask for keyboard shortcuts file to use
        """
        kbfile = ''
        ok, cancel = ask_ync_question(self.page.gui, text=instructions)
        if ok:
            kbfile = get_file_to_open(self.page.gui, extension='SCF files (*.scf)',
                                      start=initial)  # self.kbfile)
        return kbfile

    def get_keydefs(self, data):
        """huidige keydefs afleiden

        input: met ElementTree ingelezen data volgens pad zoals opgegeven in DC_PATH
               (shortcuts.scf in de settings directory)
        resultaat: een mapping van een tuple van keyname, modifiers en context op een dictionary met
                       command string, parameter en controls
                   een lijst van alle gevonden contexten
                   een lijst van alle gevonden mogelijke controls
        """
        root = data.getroot()
        for form in list(root.find('Hotkeys')):
            ctx = form.get('Name')
            self.contexts.add(ctx)
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
                test = hotkey.findall('Param')
                # parameter = '' if test is None else ";".join([param.text for param in test])
                parameter = '' if not test else ";".join([param.text for param in test])
                test = hotkey.findall('Control')
                if not test:  # test is None: - findall geeft lege list i.p.v. None
                    ctrls = ''
                    self.controls.add('')
                else:
                    ctrls = []
                    for control in test:
                        ctrls.append(control.text)
                        self.controls.add(control.text)
                    ctrls = ';'.join(ctrls)
                self.definedkeys[(keyname, modifiers, ctx)] = {'cmd': command, 'param': parameter,
                                                               'ctrl': ctrls}

    def get_stdkeys(self, soup):
        """determine standard keys

        input: met BeautifulSoup ingelezen data volgens pad zoals opgegeven in DC_KEYS
               (shortcuts.html in de docs directory)
        resultaat: een mapping van een tuple van keyname, modifiers en context op omschrijving
                   een list met mogelijke contexts
        """
        # newsoup = soup.find('div', class_='dchelpage')
        sections = soup.find_all('div')
        for div in sections:
            context = div.select("h2 a")
            if not context:
                continue
            context = context[0]['name']
            if context in ("intro", "options"):
                continue
            context = context.replace('_window', '').title()
            self.contexts_list.append(context)
            tbody = div.select('table tr')
            for row in tbody:
                if 'class' in row.attrs:
                    continue
                keynames = ()
                for col in row.select('td'):
                    ## if col['class'] == 'varcell':
                    if 'class' in col.attrs and 'varcell' in col['class']:
                        keynames = parse_keytext(col.div.text)  # meer dan 1 key/keycombo mogelijk
                    ## elif 'hintcell' in col['class']:
                        ## print('hintcell')
                    else:
                        oms = '\n'.join([x.strip() for x in col.get_text().split('\n')])
                if keynames:
                    for name, mods in keynames:
                        self.stdkeys[(_translate_keynames(name), mods, context)] = oms

    def get_cmddict(self, soup):
        """build dictionary of commands with descriptions

        input: met BeautifulSoup ingelezen data volgens pad zoals opgegeven in DC_CMDS
               (cmds.html in de docs directory)
        resultaat: een mapping met key = commandonaam en value = een tekst (de omschrijving)
                   een mapping met key = een tuple van keyname, modifiers en value = een list
                       (eigenlijk set) van commandonamen (meestal 1?)
                   een mapping met key = commandonaam en value = een list van tuples van
                       naam, waardebereik en omschrijving
                   een mapping met key = categorie en value = een list van commandonamen
        """
        newsoup = soup.select('div[class="dchelpage"]')[0]
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
                            self.cmddict.update(cd)
                            self.defaults.update(da)
                            self.params.update(cp)
                            self.catdict[cat] = cl

    def get_toolbarcmds(self, data):
        """lees de zelfgedefinieerde toolbar items

        input:
            met ElementTree ingelezen data volgens pad zoals opgegeven in DC_SETT
            (doublecmd.xml in de settings directory)
        resultaat:
            een mapping met key = de parameter voor cm_ToolBarCmd
            om de details in value te kunnen koppelen aan de betreffende keyboard shortcuts
        """
        root = data.getroot()
        for toolbar in list(root.find('Toolbars')):
            toolbarid = toolbar.tag
            for row in list(toolbar):
                for item in row.findall('Program'):
                    key = item.find('ID').text
                    cmd = item.find('Command').text
                    test = item.find('Hint')
                    desc = test.text if test is not None else ''
                    test = item.find('Params')
                    parm = test.text if test is not None else ''
                    # self.tbcmddict[key] = (desc, cmd, parm)
                    self.tbcmddict[(toolbarid, key)] = (desc, cmd, parm)

    def add_missing_descriptions(self, desclist):
        """update missing descriptions in cmddict
        """
        if self.showinfo:
            self.page.dialog_data = {'descdict': dict(desclist), 'cmddict': self.cmddict}
            if show_dialog(self.page, DcCompleteDialog):
                desclist = list(self.page.dialog_data['descdict'].items())
        for command, description in desclist:
            if command not in self.cmddict or not self.cmddict[command]:
                self.cmddict[command] = description
        # self.desclist = desclist
        return desclist

    def assemble_shortcuts(self):
        """automatische mapping van bekende keycombo's op commando's d.m.v. gegevens uit de
        dictionaries met omschrijvingen

        bepaal tegelijkertijd of dit een standaard definitie is of een aangepaste

        en tenslotte: ombouwen naar een dictionary die in het csv bestand kan worden ingelezen
        """
        for key_in_context, definitions_dict in self.definedkeys.items():
            # bepalen of dit een standaard definitie is
            definitions_dict['standard'] = ''
            # we kunnen hiervoor kijken in defaults (bijproduct van het bepalen van cmddict)
            if self.defaults.get(key_in_context[:2]) == {definitions_dict['cmd']}:
                definitions_dict['standard'] = 'S'
            # maar het leeuwendeel zit eigenlijk in stdkeys, daar zitten tevens de omschrijvingen
            # in. In cmddict zitten ook omschrijvingen, deze kunnen verschillend zijn en in dat
            # geval worden die uit cmddict overgenomen
            stdkeys_oms = self.stdkeys.get(key_in_context, '')
            if stdkeys_oms:
                definitions_dict['desc'] = stdkeys_oms
                definitions_dict['standard'] = 'S'
            # toolbaritems zijn altijd eigen definities
            if definitions_dict['cmd'] == 'cm_ExecuteToolbarItem':
                definitions_dict['standard'] = 'U'
                # itemid = definitions_dict['param'].split('=', 1)[1]
                parmdict = {}
                parms = definitions_dict['param'].split(';')
                for parm in parms:
                    name, value = parm.split('=', 1)
                    parmdict[name] = value.replace('TfrmOptionsToolbar', 'MainToolbar')
                itemid = (parmdict['ToolBarID'], parmdict['ToolItemID'])
                oms, cmd, parm = self.tbcmddict[itemid]
                definitions_dict['desc'] = f'{oms} ({cmd} {parm})'
            else:
                # nu de omschrijving uit cmddict bekijken
                cmddict_oms = self.cmddict.get(definitions_dict['cmd'], None)
                if cmddict_oms is None:
                    self.unlisted_cmds.append(definitions_dict['cmd'])
                    cmddict_oms = ''
                # stdkeys_oms = definitions_dict.get('desc', '')
                if cmddict_oms and not stdkeys_oms:
                    # als nog geen omschrijving bekend dan overnemen
                    definitions_dict['desc'] = cmddict_oms
                    # definitions_dict['standard'] = 'S'
                elif not cmddict_oms:  # and stdkeys_oms:
                    # let op: hier ontstaan nieuwe of bijgewerkte cmddict entries
                    self.cmddict[definitions_dict['cmd']] = stdkeys_oms
                elif cmddict_oms != stdkeys_oms:
                    # omschrijving verschillend - verzamelen om te kijken welke we willen gebruiken?
                    self.tobematched[key_in_context] = {'stdkeys_oms': stdkeys_oms,
                                                        'cmddict_oms': cmddict_oms}
                    definitions_dict['desc'] = cmddict_oms
            self.shortcuts[key_in_context] = definitions_dict
        # nog even kijken naar wat er wel in stdkeys zit en niet in definedkeys
        for stdkey, value in self.stdkeys.items():
            if stdkey not in self.shortcuts:
                self.shortcuts[stdkey] = {'cmd': '', 'param': '', 'ctrl': '', 'standard': 'S',
                                          'desc': value}

    def format_shortcuts(self):
        "ingelezen keydefs omwerken naar het intern gebruikte formaat"
        new_shortcuts = {}
        keyseq = 0
        for keycombo, attrdict in self.shortcuts.items():
            keyseq += 1
            key, mods, context = keycombo
            # laatste controle met commands dictionary
            cmddict_desc = self.cmddict.get(attrdict['cmd'], '')
            shortcut_desc = attrdict.get('desc', '')
            if not cmddict_desc:
                self.unlisted_cmds.append(attrdict['cmd'])
            elif shortcut_desc != cmddict_desc:
                attrdict['desc'] = cmddict_desc
            new_shortcuts[keyseq] = (key, mods, attrdict['standard'], context, attrdict['cmd'],
                                     attrdict['param'], attrdict['ctrl'], attrdict.get('desc', ''))
        self.shortcuts = new_shortcuts


def update_otherstuff_inbound(otherstuff):
    """convert dict keys from space-separated string to key-modifier-context format
    """
    newstuff = {}
    for key, value in otherstuff['stdkeys'].items():
        newkey = key.split(' ')  # split explicitely on one space
        newstuff[tuple(newkey)] = value
    otherstuff['stdkeys'] = newstuff
    newstuff = {}
    for key, value in otherstuff['defaults'].items():
        newkey = key.split(' ')  # split explicitely on one space
        newstuff[tuple(newkey)] = value
    otherstuff['defaults'] = newstuff
    return otherstuff


def update_otherstuff_outbound(otherstuff):
    """modify dict keys from list to space-separated string to accomodate json format
    """
    newstuff = {}
    for key, value in otherstuff['stdkeys'].items():
        newkey = ' '.join(list(key))
        if isinstance(value, set):
            value = sorted(value)
        newstuff[newkey] = value
    otherstuff['stdkeys'] = newstuff
    newstuff = {}
    for key, value in otherstuff['defaults'].items():
        newkey = ' '.join(list(key))
        if isinstance(value, set):
            value = sorted(value)
        newstuff[newkey] = value
    otherstuff['defaults'] = newstuff
    return otherstuff


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
    root = ET.Element('doublecmd', DCVersion=DCVER)
    head = ET.SubElement(root, 'Hotkeys', Version=KBVER)
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
