# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
import string
import collections
import functools
import shutil
import xml.etree.ElementTree as ET
import bs4 as bs # import BeautifulSoup
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

C_SAVE, C_DEL, C_KTXT, C_CTXT = '010', '011', '018', '019'
C_PARMS, C_CTRL, C_CNTXT = '090', '091', '047'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'

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
            test = hotkey.find('Param')
            if test is None:
                parameter = ''
            else:
                parameter = ";".join([param.text for param in test])
            test = hotkey.find('Control')
            if test is None:
                controls = ''
            else:
                controls = ';'.join([control.text for control in test])
            key += 1
            keydata[key] = (keyname, modifiers, context, command, parameter,
                controls)

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

def get_cmddict(path, definedcommands):

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
        if command in definedcommands:
            definedcommands.remove(command)

    for command in definedcommands:
        cmddict[command] = ''

    return cmddict


def buildcsv(parent, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    initial = '/home/albert/.config/doublecmd/shortcuts.scf'
    dc_keys = '/usr/share/doublecmd/doc/en/shortcuts.html'
    dc_cmds = '/usr/share/doublecmd/doc/en/cmds.html'

    shortcuts = collections.OrderedDict()
    try:
        initial = parent.page.settings['DC_PATH'][0]
        dc_keys = parent.page.settings['DC_KEYS'][0]
        dc_cmds = parent.page.settings['DC_CMDS'][0]
    except (KeyError, AttributeError):
        pass
    if showinfo:
        ok = gui.QMessageBox.information(parent, parent.captions['000'],
            instructions, gui.QMessageBox.Ok | gui.QMessageBox.Cancel)
        if ok == gui.QMessageBox.Cancel:
            return
        kbfile = gui.QFileDialog.getOpenFileName(parent, parent.captions['059'],
            directory=initial, filter='SCF files (*.scf)')
    else:
        kbfile = initial
    if not kbfile:
        return

    keydata = get_keydefs(kbfile)
    definedcommands = set([x[3] for x in keydata.values()])
    # to determine if keys have been redefined
    stdkeys = get_stdkeys(dc_keys)
    # to find descriptions for commands
    cmddict = get_cmddict(dc_cmds, definedcommands)
    for key, value in keydata.items():
        templist = list(value)
        val = '' # standard / customized
        # if keydef_from_keydata != keydef_from_stdkeys:
        #     value = 'X'
        templist.insert(2, val)
        try:
            templist.append(cmddict[value[3]])
        except KeyError:
            continue # do not write unassigned commands
            ## templist.append('')
        ## print(templist)
        shortcuts[key] = tuple(templist)

    controls = ['', 'Command Line', 'Files Panel', 'Quick Search']
    contexts = ['Main', 'Copy/Move Dialog', 'Differ', 'Edit Comment Dialog',
        'Viewer']
    return shortcuts, {'stdkeys': stdkeys, 'cmddict': cmddict, 'controls': controls,
        'contexts': contexts}

how_to_save = """\
Instructions to load the changed definitions back into Double Commander.


After you've saved the definitions to a .scf file, go to
Configuration > Options > Hot keys, and select it in the
top left selector.

print
You may have to close and reopen the dialog to see the changes.
"""

def build_shortcut(key, mods):
    result = ''
    if 'C' in mods:
        result += 'Ctrl+'
    if 'S' in mods:
        result += 'Shift+'
    if 'A' in mods:
        result += 'Alt+'
    key = key.capitalize()
    if key == 'Pgup': key = 'PgUp'
    if key == 'Pgdn': key = 'PgDn'
    return result + key

def savekeys(parent):
    """schrijf de gegevens terug
    """

    ok = gui.QMessageBox.information(parent, parent.captions['000'], how_to_save,
        gui.QMessageBox.Ok | gui.QMessageBox.Cancel)
    if ok == gui.QMessageBox.Cancel:
        return

    kbfile = gui.QFileDialog.getSaveFileName(parent, parent.captions['059'],
        directory=parent.settings['DC_PATH'][0], filter='SCF files (*.scf)')
    if not kbfile:
        return

    root = ET.Element('doublecmd', DCVersion="0.6.6 beta")
    head = ET.SubElement(root, 'Hotkeys', Version="20")
    oldform = ''
    for item in sorted(parent.data.values(), key=lambda x: x[3]):
        key, mods, type_, context, cmnd, parm, ctrl, desc = item
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

# callbacks for gui elements
def on_combobox(self, cb, text):
    """callback op het gebruik van een combobox

    zorgt ervoor dat de buttons ge(de)activeerd worden
    """
    pass
    text = str(text) # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan de
                     # callback soms fout?
    hlp = cb.currentText()
    if text != hlp:
        text = hlp
    ## print(self._origdata)
    self.defchanged = False
    if cb == self.cmb_key:
        if text != self._origdata[0]:
            self._newdata[0] = text
            self.defchanged = True
            self.b_save.setEnabled(True)
        elif str(self.cmb_commando.currentText()) == self._origdata[5]:
            self.b_save.setEnabled(False)
    elif cb == self.cmb_commando:
        if text != self._origdata[5]:
            self._newdata[5] = text
            self.defchanged = True
            try:
                self.txt_oms.setText(self.omsdict[text])
            except KeyError:
                self.txt_oms.setText('(Geen omschrijving beschikbaar)')
            self.b_save.setEnabled(True)
        elif str(self.cmb_key.currentText()) == self._origdata[0]:
            self.b_save.setEnabled(False)
    ## print(self._origdata)
    ## print(self._newdata)

def on_checkbox(self, cb, state):
    state = bool(state)
    pass
    for win, indx in zip((self.cb_shift, self.cb_ctrl, self.cb_alt, self.cb_win),
            range(1,5)):
        if cb == win and state != self._origdata[indx]:
            self._newdata[indx] = state
            self.defchanged = True
            self.b_save.setEnabled(True)
    else:
        states = [bool(self.cb_shift.isChecked()), bool(self.cb_ctrl.isChecked()),
            bool(self.cb_alt.isChecked()), bool(self.cb_win.isChecked())]
        if states == self._origdata[1:5]:
            self.defchanged = False
            self.b_save.setEnabled(False)
    ## print('on checkbox:', indx, state)
    ## print(self._origdata)
    ## print(self._newdata)

def on_update(self):
    pass
    self.aanpassen()
    self.parent.p0list.setFocus()

def on_delete(self):
    pass
    self.aanpassen(delete=True)
    self.parent.p0list.setFocus()

class MyPanel(gui.QFrame):

    def __init__(self, parent):
        gui.QFrame.__init__(self)
        self.parent = parent
        self.initializing = False
        ## self.csvfile = self.parent.pad
        ## self.settings = self.parent.settings

    def add_extra_attributes(self):
         # key, mods, cmnd, params, controls
        self._origdata = ["", False, False, False, False, "", '', '', '']
        self._newdata = self._origdata[:]

        self.keylist = [x for x in string.ascii_uppercase] + \
            [x for x in string.digits] + ["F" + str(i) for i in range(1,13)] + \
            [self.parent.captions[str(x)] for x in range(100,121)] + \
            ['.', ',', '+', '-', '`', '[', ']', '\\', ';', "'", '/']
        self.commandsdict = self.parent.otherstuff['cmddict']
        self.commandlist = sorted(self.commandsdict.keys())
        self.contextslist = self.parent.otherstuff['contexts']
        self.controlslist = self.parent.otherstuff['controls']
        ## self.mag_weg = True
        ## self.newfile = self.newitem = False
        ## self.oldsort = -1
        ## self.idlist = self.actlist = self.alist = []
        ## paden = [self.parent.settings[x][0] for x in PATHS[:4]] + [self.parent.pad]
        ## # ## self.cmdict, self.omsdict, self.defkeys, _ = readkeys(paden)
        ## self.cmdict = defaultcommands(self.parent.settings['CI_PAD'][0])
        ## self.ucmdict = usercommands(self.parent.settings['UC_PAD'][0])
        ## self.defkeys = defaultkeys(self.parent.settings['KB_PAD'][0])
        ## self.udefkeys = userkeys(self.parent.settings['TC_PAD'][0])

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        self._box = box = gui.QFrame(self)
        ## box.setFrameShape(gui.QFrame.StyledPanel)
        box.setMaximumHeight(150)
        self.txt_key = gui.QLabel(self.parent.captions[C_KTXT] + " ", box)
        cb = gui.QComboBox(box)
        cb.addItems(self.keylist)
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_key = cb

        for x in (M_CTRL, M_ALT, M_SHFT, M_WIN):
            cb = gui.QCheckBox(self.parent.captions[x].join(("+ ","")), box)
            cb.setChecked(False)
            cb.stateChanged.connect(functools.partial(on_checkbox, self, cb))
            if x == M_CTRL:
                self.cb_ctrl = cb
            elif x == M_ALT:
                self.cb_alt = cb
            elif x == M_SHFT:
                self.cb_shift = cb
            elif x == M_WIN:
                self.cb_win = cb

        self.txt_cmd = gui.QLabel(self.parent.captions[C_CTXT] + " ", box)
        ## self.commandlist.sort()
        cb = gui.QComboBox(self)
        cb.addItems(self.commandlist)
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_commando = cb

        self.b_save = gui.QPushButton(self.parent.captions[C_SAVE], box) ##, (120, 45))
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(functools.partial(on_update, self))
        self.b_del = gui.QPushButton(self.parent.captions[C_DEL], box) #, size= (50,-1)) ##, (120, 45))
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(functools.partial(on_delete, self))

        self.lbl_parms = gui.QLabel(self.parent.captions[C_PARMS], box)
        self.txt_parms = gui.QLineEdit(box)
        self.txt_parms.setMaximumWidth(280)
        self.lbl_contexts = gui.QLabel(self.parent.captions[C_CNTXT], box)
        cb = gui.QComboBox(box)
        cb.addItems(self.contextslist)
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_contexts = cb
        self.lbl_controls = gui.QLabel(self.parent.captions[C_CTRL], box)
        cb = gui.QComboBox(box)
        cb.addItems(self.controlslist)
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_controls = cb

        self.txt_oms = gui.QTextEdit(box)
        ## self.txt_oms.setMaximumHeight(40)
        self.txt_oms.setReadOnly(True)

    def layout_extra_fields(self, sizer):
        """add the extra fields to the layout
        """
        bsizer = gui.QVBoxLayout()

        sizer1 = gui.QHBoxLayout()
        sizer2 = gui.QHBoxLayout()
        sizer3 = gui.QHBoxLayout()
        sizer3.addWidget(self.txt_key)
        sizer3.addWidget(self.cmb_key)
        sizer2.addLayout(sizer3)
        sizer3 = gui.QHBoxLayout()
        sizer3.addWidget(self.cb_ctrl)
        sizer3.addWidget(self.cb_alt)
        sizer3.addWidget(self.cb_shift)
        sizer3.addWidget(self.cb_win)
        sizer2.addLayout(sizer3)
        sizer1.addLayout(sizer2)
        sizer2 = gui.QHBoxLayout()
        sizer2.addWidget(self.txt_cmd)
        sizer2.addWidget(self.cmb_commando)
        sizer1.addLayout(sizer2)
        sizer1.addWidget(self.b_save)
        sizer1.addWidget(self.b_del)
        bsizer.addLayout(sizer1)

        sizer1 = gui.QHBoxLayout()
        sizer2 = gui.QVBoxLayout()
        sizer2.addWidget(self.txt_oms)
        ## bsizer.addLayout(sizer1)
        sizer1.addLayout(sizer2, 2)

        ## sizer1 = gui.QHBoxLayout()
        sizer2 = gui.QGridLayout()
        line = 0
        sizer2.addWidget(self.lbl_contexts, line, 0)
        sizer3 = gui.QHBoxLayout()
        sizer3.addWidget(self.cmb_contexts)
        sizer3.addStretch()
        sizer2.addLayout(sizer3, line, 1)
        line += 1
        sizer2.addWidget(self.lbl_parms, line, 0)
        sizer2.addWidget(self.txt_parms, line, 1)
        line += 1
        sizer2.addWidget(self.lbl_controls, line, 0)
        sizer3 = gui.QHBoxLayout()
        sizer3.addWidget(self.cmb_controls)
        sizer3.addStretch()
        sizer2.addLayout(sizer3, line, 1)
        sizer1.addLayout(sizer2, 1)

        bsizer.addLayout(sizer1)

        self._box.setLayout(bsizer)
        sizer.addWidget(self._box)

    def captions_extra_fields(self):
        """to be called on changing the language
        """
        self.cb_win.setText(self.parent.captions[M_WIN].join(("+", "  ")))
        self.cb_ctrl.setText(self.parent.captions[M_CTRL].join(("+", "  ")))
        self.cb_alt.setText(self.parent.captions[M_ALT].join(("+", "  ")))
        self.cb_shift.setText(self.parent.captions[M_SHFT].join(("+", "  ")))
        self.b_save.setText(self.parent.captions[C_SAVE])
        self.b_del.setText(self.parent.captions[C_DEL])
        self.txt_key.setText(self.parent.captions[C_KTXT])
        self.txt_cmd.setText(self.parent.captions[C_CTXT])
        self.lbl_parms.setText(self.parent.captions[C_PARMS])
        self.lbl_controls.setText(self.parent.captions[C_CTRL])
        self.lbl_contexts.setText(self.parent.captions[C_CNTXT])

    def on_item_selected(self, newitem, olditem): # olditem, newitem):
        """callback on selection of an item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        pass
        if not newitem: # bv. bij p0list.clear()
            return
        if self.initializing:
            self.vuldetails(newitem)
            return
        ## print('itemselected called', newitem.text(0))
        ## if olditem is not None:
            ## print('old item was', olditem.text(0))
        ## print('In itemselected:', self._origdata, self._newdata)
        origkey = self._origdata[0]
        origmods = ''.join([y for x, y in zip((4, 2, 3, 1),
            ('WCAS')) if self._origdata[x]])
        origcmd = self._origdata[5]
        key = self._newdata[0]
        mods = ''.join([y for x, y in zip((4, 2, 3, 1),
            ('WCAS')) if self._newdata[x]])
        cmd = self._newdata[5]
        cursor_moved = True if newitem != olditem and olditem is not None else False
        other_item = key != origkey or mods != origmods
        other_cmd = cmd != origcmd
        any_change = other_item or other_cmd
        gevonden = False
        for number, item in self.parent.data.items():
            if key == item[0] == key and item[1] == mods:
                gevonden = True
                indx = number
                break
        ## print(cursor_moved, other_item, other_cmd, gevonden)
        make_change = False
        if any_change:
            if cursor_moved:
                h = gui.QMessageBox.question(self,
                    self.parent.captions["000"], self.parent.captions["020"],
                    gui.QMessageBox.Yes | gui.QMessageBox.No)
                make_change = True if h == gui.QMessageBox.Yes else False
            elif other_item:
                if gevonden:
                    ok = gui.QMessageBox.question(self,
                        self.parent.captions["000"], self.parent.captions["045"],
                        gui.QMessageBox.Yes | gui.QMessageBox.No)
                    make_change = True if ok == gui.QMessageBox.Yes else False
                else:
                    make_change = True
            else:
                make_change = True
        if make_change:
            item = self.parent.p0list.currentItem()
            pos = self.parent.p0list.indexOfTopLevelItem(item)
            if gevonden:
                self.parent.data[indx] = (key, mods, 'U', cmd, self.omsdict[cmd])
            else:
                newdata = [x for x in self.parent.data.values()]
                newvalue = (key, mods, 'U', cmd, self.omsdict[cmd])
                newdata.append(newvalue)
                newdata.sort()
                for x, y in enumerate(newdata):
                    if y == newvalue:
                        indx = x
                    self.parent.data[x] = y
            self.parent.modified = True
            self._origdata = [key, False, False, False, False, cmd]
            for mod, indx in zip(('WCAS'),(4, 2, 3, 1)):
                self._origdata[indx] = mod in mods
            self.parent.populate_list(pos)    # refresh
            newitem = self.parent.p0list.topLevelItem(pos)
        self.vuldetails(newitem)

    def vuldetails(self, selitem):  # let op: aangepast (gebruik zip)
        if not selitem: # bv. bij p0list.clear()
            return
        seli = selitem.data(0, core.Qt.UserRole)
        if sys.version < '3':
            seli = seli.toPyObject()
        key, mods, soort, context, cmd, parms, controls, oms = self.parent.data[seli]
        self.b_save.setEnabled(False)
        self.b_del.setEnabled(False)
        if soort == 'U':
            self.b_del.setEnabled(True)
        self._origdata = [key, False, False, False, False, cmd, context, parms,
            controls]
        ix = self.keylist.index(key)
        self.cmb_key.setCurrentIndex(ix)
        self.cb_shift.setChecked(False)
        self.cb_ctrl.setChecked(False)
        self.cb_alt.setChecked(False)
        self.cb_win.setChecked(False)
        self.cmb_key.setEditText(key)
        for x, y, z in zip('SCAW',(1, 2, 3, 4), (self.cb_shift, self.cb_ctrl,
                self.cb_alt, self.cb_win)):
            if x in mods:
                self._origdata[y] = True
                z.setChecked(True)
        self._newdata = self._origdata[:]
        ix = self.commandlist.index(cmd)
        self.cmb_commando.setCurrentIndex(ix)
        ix = self.contextslist.index(context)
        self.cmb_contexts.setCurrentIndex(ix)
        ## self.cmb_contexts.setExitText(context)
        self.txt_parms.setText(parms)
        ix = self.controlslist.index(controls) # TODO: adapt for multiple values
        self.cmb_controls.setCurrentIndex(ix)
        ## self.cmb_controls.setExitText(controls)
        self.txt_oms.setText(oms)

    def aanpassen(self, delete=False): # TODO
        print('aanpassen called')
        pass
        item = self.parent.p0list.currentItem()
        pos = self.parent.p0list.indexOfTopLevelItem(item)
        if delete:
            indx = item.data(0, core.Qt.UserRole)
            if sys.version < '3':
                indx = int(indx.toPyObject())
            if self.parent.data[indx][1] == "S": # can't delete standard key
                gui.QMessageBox.information(self, self.parent.captions["000"],
                    self.parent.captions['024'])
                return
            else:
                if self.parent.data[indx][0] in self.defkeys: # restore standard if any
                    cmd = self.defkeys[self.parent.data[indx][0]]
                    if cmd in self.omsdict:
                        oms = self.omsdict[cmd]
                    else:
                        oms = cmd
                        cmd = ""
                    self.parent.data[indx] = (key, 'S', cmd, oms)
                else:
                    del self.parent.data[indx]
                    ## pos -= 1
            self.b_save.setEnabled(False)
            self.b_del.setEnabled(False)
            self.parent.modified = True
            self.parent.setWindowTitle(' '.join((self.parent.captions["000"],
                self.parent.captions['017'])))
            print('item deleted, pos is', pos)
            self.parent.populate_list(pos)    # refresh
        else:
            self.on_item_selected(item, item) # , from_update=True)

#
