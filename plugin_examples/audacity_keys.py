# -*- coding: UTF-8 -*-
import sys
import shutil
import xml.etree.ElementTree as ET
import collections
import functools
import string
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

C_SAVE, C_DEL, C_KTXT, C_CTXT = '010', '011', '018', '019'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
# constants for column names
C_KEY, C_TYPE, C_CMD, C_DESC, C_MODS = '001', '002', '003', '004', '043'
C_CODE, C_CNTXT, C_PLAT, C_FEAT = '046', '047', '048', '049'
C_PARMS, C_CTRL, C_MNU = '090', '091', '092'

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
        initial = parent.page.settings['AC_KEYS'][0]
    except KeyError:
        initial = ''

    if showinfo:
        ok = gui.QMessageBox.information(parent, parent.captions['000'],
            instructions, gui.QMessageBox.Ok | gui.QMessageBox.Cancel)
        if ok == gui.QMessageBox.Cancel:
            return

        gui.QFileDialog.getOpenFileName(parent, parent.captions['059'],
                directory=initial, filter='XML files (*.xml)')

    else:
        kbfile = initial

    if not kbfile:
        return

    tree = ET.parse(kbfile)
    root = tree.getroot()
    data = []
    key = 0
    commandlist = {}
    for item in root.findall('command'):
        line = []
        keydef = item.get('key', default = '')
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

def on_combobox(self, cb, text):
    """callback op het gebruik van een combobox

    zorgt ervoor dat de buttons ge(de)activeerd worden
    """
    if self.initializing:
        return
    text = str(text) # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan de
                     # callback soms fout?
    hlp = cb.currentText()
    if text != hlp:
        text = hlp
    ## print(self._origdata)
    self.defchanged = False
    keyitemindex = 0
    cmditemindex = 5
    if cb == self.cmb_key:
        if text != self._origdata[keyitemindex]:
            self._newdata[keyitemindex] = text
            self.defchanged = True
            self.b_save.setEnabled(True)
        elif str(self.cmb_commando.currentText()) == self._origdata[cmditemindex]:
            self.b_save.setEnabled(False)
    elif cb == self.cmb_commando:
        if text != self._origdata[cmditemindex]:
            self._newdata[cmditemindex] = text
            self.defchanged = True
            try:
                self.txt_oms.setText(self.commandsdict[text])
            except KeyError:
                self.txt_oms.setText('(Geen omschrijving beschikbaar)')
            self.b_save.setEnabled(True)
        elif str(self.cmb_key.currentText()) == self._origdata[keyitemindex]:
            self.b_save.setEnabled(False)
    ## print(self._origdata)
    ## print(self._newdata)

def on_checkbox(self, cb, state):
    state = bool(state)
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
    return
    self.aanpassen()
    self.parent.p0list.setFocus()

def on_delete(self):
    return
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
        self._origdata = ["", False, False, False, False, ""]
        self._newdata = self._origdata[:]

        self.keylist = [x for x in string.ascii_uppercase] + \
            [x for x in string.digits] + ["F" + str(i) for i in range(1,13)] + \
            ['NumEnter'] + \
            [self.parent.captions[str(x)] for x in range(100,121)] + \
            ['.', ',', '+', '-', '`', '[', ']', '\\', ';', "'", '/']
        self.commandsdict = self.parent.otherstuff['commands']
        self.commandslist = sorted(self.commandsdict.keys())

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        self._box = box = gui.QFrame(self)
        box.setMaximumHeight(90)
        self.txt_key = gui.QLabel(self.parent.captions[C_KTXT] + " ", box)
        cb = gui.QComboBox(box)
        cb.setMaximumWidth(90)
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
        cb = gui.QComboBox(self)
        cb.setMaximumWidth(150)
        cb.addItems(self.commandslist) # only load on choosing a context
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_commando = cb

        self.b_save = gui.QPushButton(self.parent.captions[C_SAVE], box) ##, (120, 45))
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(functools.partial(on_update, self))
        self.b_del = gui.QPushButton(self.parent.captions[C_DEL], box) #, size= (50,-1)) ##, (120, 45))
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(functools.partial(on_delete, self))

        self.txt_oms = gui.QTextEdit(box)
        if not self.parent.settings['RedefineKeys'][0] == '1':
            for widget in self.children():
                widget.setEnabled(False)
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
        sizer1.addStretch()
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
        sizer1.addLayout(sizer2, 2)

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

    def on_item_selected(self, newitem, olditem): # olditem, newitem):
        """callback on selection of an item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
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
        ## key, mods, command, oms = self.parent.data[seli]
        keydefdata = self.parent.data[seli]
        self.b_save.setEnabled(False)
        self.b_del.setEnabled(False)
        ## if soort == 'U':
            ## self.b_del.setEnabled(True)
        ## self._origdata = [key, False, False, False, False, command]
        self._origdata = ['', False, False, False, False, '']
        for indx, item in enumerate(keydefdata):
            if self.parent.column_info[indx][0] == C_KEY:
                key = item
                ix = self.keylist.index(key)
                self.cmb_key.setCurrentIndex(ix)
                ## self.cmb_key.setEditText(key)
                self._origdata[0] = key
            elif self.parent.column_info[indx][0] == C_MODS:
                mods = item
                self.cb_shift.setChecked(False)
                self.cb_ctrl.setChecked(False)
                self.cb_alt.setChecked(False)
                self.cb_win.setChecked(False)
                for x, y, z in zip('SCAW',(1, 2, 3, 4), (self.cb_shift,
                        self.cb_ctrl, self.cb_alt, self.cb_win)):
                    if x in mods:
                        self._origdata[y] = True
                        z.setChecked(True)
            elif self.parent.column_info[indx][0] == C_CMD:
                command = item
                self.initializing = True
                ix = self.commandslist.index(command)
                self.cmb_commando.setCurrentIndex(ix)
                self.initializing = False
                self._origdata[5] = command
            elif self.parent.column_info[indx][0] == C_DESC:
                oms = item
                self.txt_oms.setText(oms)
        self._newdata = self._origdata[:]


    def aanpassen(self, delete=False): # TODO
        print('aanpassen called')
        return
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
