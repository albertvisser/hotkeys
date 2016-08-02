# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import string
## import datetime
from xml.etree import ElementTree as ET
import csv
import shutil
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

## C_SAVE, C_DEL, C_KTXT, C_CTXT = '010', '011', '018', '019'
## M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
## # constants for column names
## C_KEY, C_TYPE, C_CMD, C_DESC, C_MODS = '001', '002', '003', '004', '043'
## C_CODE, C_CNTXT, C_PLAT, C_FEAT = '046', '047', '048', '049'
## C_PARMS, C_CTRL, C_MNU = '090', '091', '092'
PATHS = ('TC_PAD', 'UC_PAD', 'CI_PAD', 'KB_PAD', 'HK_PAD')

def keymods(x):
    """hulp bij omzetten wincmd.ini definitie in standaard definitie
    """
    m = {'A': 'Alt','C':'Ctrl','S':'Shift', 'W': 'Win'}
    if x == "NUM +":
        y = ''
        keyc = x
    else:
        y = x.split('+', 1)
        keyc = y[-1]
    keyc = keyc.replace(" ","").capitalize()
    if len(y) > 1:
        mods = [z[0] for z in y[0]]
        keyc = ' + '.join((keyc,''.join(mods)))
    return keyc

def keymods2(x):
    """hulp bij omzetten keyboard.txt definitie in standaard definitie
    """
    extra = ""
    if x[-1] == "+":
        x = x[:-1]
        extra = "+"
    mods = ""
    h = x.split("+",1)
    while len(h) > 1:
        ## if h[0] in ('SHIFT','ALT','CTRL'):
        if h[0] in ('CTRL', 'ALT','SHIFT'):
            mods += h[0][0]
        h = h[1].split("+",1)
    keyc = h[0].replace(" ","").capitalize() + extra
    if keyc == '\\':
        keyc = 'OEM_US\\|'
    ## keyc = ' + '.join((keyc,mods))
    return keyc, mods

def defaultcommands(root):
    """mapping uit totalcmd.inc omzetten in een Python dict
    """
    cmdict = {'': {"oms": "no command available"}}
    with open(root) as _in:
        for x in _in:
            h = x.strip()
            if h == '' or h[0] == '[' or h[0] == ';':
                continue
            cm_naam, rest = h.split('=',1)
            cm_num, cm_oms = rest.split(';',1)
            cmdictitem = {"oms": cm_oms}
            if int(cm_num) > 0:
                cmdictitem["number"] = cm_num
            if " <" in cm_naam:
                cm_naam, argsitem = cm_naam.split(' <')
                cmdictitem['args'] = argsitem.split('>')[0]
            cmdict[cm_naam] = cmdictitem
    return cmdict

def usercommands(root):
    """definities uit usercmd.ini omzetten in een Python dict compatible met die
    voor de standaard commando's
    """
    ucmdict = {}
    em_name, em_value = "", ""
    with open(root) as _in:
        for x in _in:
            if x.startswith("["):
                if em_name:
                    ucmdict[em_name] = em_value
                em_name = x[1:].split("]")[0] # x[1:-1] had ook gekund maar dit is safer
                em_value = {}
            elif x.startswith("cmd"):
                em_value["cmd"] = x.strip().split("=")[1]
            elif x.startswith("menu"):
                em_value["oms"] = x.strip().split("=")[1]
            elif x.startswith("param"):
                em_value["args"] = x.strip().split("=")[1]
        ucmdict[em_name] = em_value
    return ucmdict

def defaultkeys(root):
    """keydefs lezen uit keyboard.txt - mapping maken van deze op ...
    vooralsnog alleen omschrijving
    """
    data = {}
    i = 0
    ky = []
    join_keys = False
    with open(root) as f_in:
        temp = f_in.readlines()
    for x in temp[6:]:
        x = x.rstrip()
        if x == "":
            break
        ## if len(x) < 24:
            ## continue
        deel1 = x[:23].strip()
        deel2 = x[23:].strip()
        if deel1 == '':
            ky_desc += " " + deel2
        elif join_keys:
            join_keys = False
            ky_desc += " " + deel2
            ky[1] = deel1
        else:
            if len(ky) > 0:
                for k in ky:
                    h = k.rsplit('+', 1)
                    ## print(h)
                    if '/' in h[-1] and not h[-1].endswith('/'):
                        hlp = h[-1].split('/')
                        for it in hlp:
                            data[keymods2('+'.join((h[0], it)))] = {"oms": ky_desc}
                    else:
                        data[keymods2(k)] = {"oms": ky_desc}
            ky_desc = deel2
            if " or " in deel1:
                ky = deel1.split(" or ")
                s2 = "+".join(ky[0].split("+")[:-1])
                if s2 != "":
                    for y in enumerate(ky[1:]):
                        ky[y[0]+1] = "+".join((s2,y[1]))
            elif deel1.endswith(" or"):
                ky = [deel1[:-3],""]
                join_keys = True
            else:
                ky = [deel1,]
    if len(ky) > 0:
        for k in ky:
            h = k.rsplit('+',1)
            if '/' in h[-1] and not h[-1].endswith('/'):
                hlp = h[-1].split('/')
                for it in hlp:
                    data[keymods2('+'.join((h[0], it)))] = {"oms": ky_desc}
            else:
                data[keymods2(k)] = {"oms": ky_desc}
    return data

def userkeys(root):
    """user key definities uit wincmd.ini lezen - mapping maken van deze op...
    vooralsnog alleen commandonaam
    """
    data = {}
    in_user = in_win = False
    ## with open(os.path.join(root,"wincmd.ini")) as f_in:
    with open(root) as f_in:
        for line in f_in:
            line = line.rstrip()
            linesplit = line.split("=")
            ## for symbol in ('+', '-', '/', '*'):
                ## if linesplit[0].endswith(symbol):
                    ## linesplit[0] = linesplit[0][:-1] + 'NUM' + linesplit[0][-1]
            if line.startswith("["):
                in_user = in_win = False
                if line.startswith("[Shortcuts]"):
                    in_user = True
                elif line.startswith("[ShortcutsWin]"):
                    in_win = True
            elif in_user or in_win:
                key, cmd = line.split('=')
                try:
                    mods, key = key.split('+')
                except ValueError:
                    mods = ''
                if in_win:
                    mods += 'W'
                data[(key, mods)] = {'cm_name': cmd}
            ## elif in_win:
                ## key, cmd = line.split('=')
                    ## if not '+' in key:
                        ## key = '+' + key
                    ## key = 'W' + key
                    ## data[key] = {'cm_name': cmd}
    return data

def readkeys(data):
    """lees key definities vanuit tckeys object

    geeft dictionaries terug met commando's, omschrijvingen en listbox data
    """
    cl = TCKeys(*data)
    cl.read()
    defkeys = cl.defkeys
    ## kys = cl.keydict.keys()
    ## kys.sort()
    data = {}
    for ix, hotkey in enumerate(sorted(cl.keydict.keys())):
        try:
            ky, mod = hotkey.split(" + ")
        except ValueError:
            ky,mod = hotkey,""
        srt, desc, cmd = cl.keydict[hotkey]
        data[ix] = (ky, mod, srt, cmd, desc)
    return cl.cmdict, cl.omsdict, cl.defkeys, data

def savekeys(parent):
    """schrijft de listbox data terug via een tckeys object
    """
    paden = [parent.settings[x][0] for x in ('TC_PAD', 'UC_PAD', 'CI_PAD', 'KB_PAD',
        'HK_PAD')]
    cl = TCKeys(*paden)
    for val in parent.data.values():
        ky, mod, srt, cmd, desc = val
        hotkey = " + ".join((ky, mod)) if mod != '' else ky
        cl.keydict[hotkey] = (srt, desc, cmd)
    ## for x,y in cl.keydict.items():
        ## print(x,y)
    cl.write()

class TCKeys(object):
    """stel gegevens samen vanuit de diverse bestanden

    kijkt naar de aangegeven locaties tenzij ze niet zijn ingesteld,
    dan wordt de standaard programma locatie gebruikt
    """
    def __init__(self, *tc_dir):
        self.ucloc = self.ciloc = self.ktloc = self.hkloc = ''
        try:
            self.tcloc = tc_dir[0] # plaats van wincmd.ini
        except IndexError:
            self.tcloc = "C:/totalcmd" # default
        try:
            self.ucloc = tc_dir[1] # plaats van usercmd.ini
        except IndexError:
            pass
        if not self.ucloc:
            self.ucloc = self.tcloc
        try:
            self.ciloc = tc_dir[2] # plaats van totalcmd.inc
        except IndexError:
            pass
        if not self.ciloc:
            self.ciloc = self.tcloc
        try:
            self.ktloc = tc_dir[3] # plaats van keyboard.txt
        except IndexError:
            pass
        if not self.ktloc:
            self.ktloc = self.tcloc
        try:
            self.hkloc = tc_dir[4] # plaats van tc_hotkeys.csv
        except IndexError:
            pass
        if not self.hkloc:
            self.hkloc = self.tcloc
        self.keydict = {}

    def read(self):
        """leest de gegevens uit de bestanden

        de gegevens worden omgezet in dictionaries
        die attributen zijn van deze class
        """
        cmdict = defaultcommands(self.ciloc)
        with open("cmdict.txt","w") as _out:
            print(cmdict, file=_out)
        ucmdict = usercommands(self.ucloc)
        with open("usercmdict.txt","w") as _out:
            print(self.ucmdict, file=_out)
        # deze zijn hier aangevuld met de zaken uit usercommands
        defkeys = {}
        for x, y in defaultkeys(self.hkloc):
            defkeys[x] = self.cmdict[y].strip()
        # de nummers die ik in y wil hebben zitten in de vierde kolom alleen dan zijn het de
        # strings m.a.w. dit kan helemaal niet
        self.keydict = {}
        for key, oms in keyboardtext(self.ktloc):
            ## print(key, oms)
            if key in defkeys:
                cm = defkeys[key]
            else:
                cm = ""
                defkeys[key] = oms
                if key == "Backspace":
                    try:
                        del defkeys["Back"]
                    except KeyError:
                        pass
            self.keydict[key] = ("S", oms, cm)
        self.defkeys = defkeys
        ## f = open("defkeys.txt","w")
        ## for x in self.defkeys:
            ## f.write("%s:: %s\n" % (x,defkeys[x]))
        ## f.close()
        for key, action in userkeys(self.tcloc):
            k = keymods(key)
            self.keydict[k] = ("U", omsdict[action], action)

    def turn_into_xml(self):
        """zet de gegevens uit keydict om in xml en schrijft ze weg
        """
        kys = self.keydict.keys()
        kys.sort()
        root = ET.Element("keys")
        for x in kys:
            h = ET.SubElement(root,"hotkey",naam=x,soort=self.keydict[x][0])
            k = ET.SubElement(h,"cmd")
            k.text = self.keydict[x][2]
            k = ET.SubElement(h,"oms")
            k.text = self.keydict[x][1]
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.tcloc,"tcmdrkeys.xml"))

    def write(self):
        """schrijf de gegevens terug naar waar ze terecht moeten komen
        """
        shortcuts, shortcutswin = [], []
        for key, item in self.keydict.items():
            ## print(key, item)
            if item[0] != 'U':
                continue
            test = [x for x in reversed(key.split())]
            ## print(test)
            if len(test) == 1:
                shortcuts.append('{}={}\n'.format(test[0], item[2]))
            elif 'W' in test[0]:
                if 'W+' in test[0]:
                    test[0] = test[0].replace('W+', '')
                else:
                    test[0] = test[0].replace('W', '')
                shortcutswin.append('{}={}\n'.format(''.join(test), item[2]))
            else:
                shortcuts.append('{}={}\n'.format(''.join(test), item[2]))

        fn = os.path.join(self.tcloc, 'wincmd.ini')
        fno = fn + ".bak"
        os.rename(fn, fno)
        schrijfdoor, shortcuts_geschreven, win_geschreven = True, False, False
        with open(fno) as f_in, open(fn, 'w') as f_out:
            for line in f_in:
                if not schrijfdoor and line.strip()[0] == "[":
                    schrijfdoor = True
                elif line.strip() == '[Shortcuts]':
                    f_out.write(line)
                    schrijfdoor = False
                    shortcuts_geschreven = True
                    for newline in shortcuts:
                        f_out.write(newline)
                elif line.strip() == '[ShortcutsWin]':
                    f_out.write(line)
                    schrijfdoor = False
                    win_geschreven = True
                    for newline in shortcutswin:
                        f_out.write(newline)
                if schrijfdoor:
                    f_out.write(line)
            if not shortcuts_geschreven and len(shortcuts) > 0:
                for newline in shortcuts:
                    f_out.write(newline)
            if not shortcuts_geschreven and len(shortcuts) > 0:
                for newline in shortcutswin:
                    f_out.write(newline)

def on_combobox(self, cb, text):
    """callback op het gebruik van een combobox

    zorgt ervoor dat de buttons ge(de)activeerd worden
    """
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
                self.txt_oms.setText(self.omsdict[text])
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
    self.aanpassen()
    self.parent.p0list.setFocus()

def on_delete(self):
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
        self._origdata = ["", False, False, False, False, ""]
        self._newdata = self._origdata[:]
        self.keylist = [x for x in string.ascii_uppercase] + \
            [x for x in string.digits] + ["F" + str(i) for i in range(1,13)] + \
            [self.parent.captions[str(x)] for x in range(100,121)] + \
            ['Pause', 'Period', 'Comma', 'Plus', 'Minus', 'Smaller/Greater',
            'Backtick/Tilde', 'Brackets open', 'Brackets close', 'Backslash/Pipe',
            'Semicolon/colon', 'Apostrophe/Quote', 'Slash/Questionmark', 'OEM_FR!']
            ## ['PAUSE', 'OEM_.', 'OEM_,', 'OEM_+', 'OEM_-', 'OEM_</>', 'OEM_US`~',
            ## 'OEM_US[{', 'OEM_US]}', 'OEM_US\\|', 'OEM_US;:', "OEM_US'" + '"',
            ## 'OEM_US/?', 'OEM_FR!']
        self.mag_weg = True
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        paden = [self.parent.settings[x][0] for x in PATHS[:4]] + [self.parent.pad]
        ## self.cmdict, self.omsdict, self.defkeys, _ = readkeys(paden)
        self.omsdict = {}
        self.cmdict = defaultcommands(self.parent.settings['CI_PAD'][0])
        self.omsdict.update({x: y['oms'] for x, y in self.cmdict.items()})
        self.ucmdict = usercommands(self.parent.settings['UC_PAD'][0])
        self.omsdict.update({x: y['oms'] for x, y in self.ucmdict.items()})
        self.defkeys = defaultkeys(self.parent.settings['KB_PAD'][0])
        self.udefkeys = userkeys(self.parent.settings['TC_PAD'][0])

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        self._box = box = gui.QFrame(self)
        box.setFrameShape(gui.QFrame.StyledPanel)
        box.setMaximumHeight(110)
        self.txt_key = gui.QLabel(self.parent.captions['C_KTXT'] + " ", box)
        cb = gui.QComboBox(box)
        cb.setMaximumWidth(90)
        cb.addItems(self.keylist)
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_key = cb

        for x in ('M_CTRL', 'M_ALT', 'M_SHFT', 'M_WIN'):
            cb = gui.QCheckBox(self.parent.captions[x].join(("+","  ")), box) #, (65, 60), (150, 20), gui.QNO_BORDER)
            cb.setChecked(False)
            cb.stateChanged.connect(functools.partial(on_checkbox, self, cb))
            if x == 'M_CTRL':
                self.cb_ctrl = cb
            elif x == 'M_ALT':
                self.cb_alt = cb
            elif x == 'M_SHFT':
                self.cb_shift = cb
            elif x == 'M_WIN':
                self.cb_win = cb

        self.txt_cmd = gui.QLabel(self.parent.captions['C_CTXT'] + " ", box)
        self.commandlist = list(self.cmdict.keys()) + list(self.ucmdict.keys())
        self.commandlist.sort()
        cb = gui.QComboBox(self)
        cb.setMaximumWidth(150)
        cb.addItems(self.commandlist)
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_commando = cb

        self.b_save = gui.QPushButton(self.parent.captions['C_SAVE'], box) ##, (120, 45))
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(functools.partial(on_update, self))
        self.b_del = gui.QPushButton(self.parent.captions['C_DEL'], box) #, size= (50,-1)) ##, (120, 45))
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(functools.partial(on_delete, self))

        self.txt_oms = gui.QTextEdit(box)
        self.txt_oms.setMaximumHeight(40)
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
        sizer3.addWidget(self.cb_win)
        sizer3.addWidget(self.cb_ctrl)
        sizer3.addWidget(self.cb_alt)
        sizer3.addWidget(self.cb_shift)
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
        sizer1.addWidget(self.txt_oms)
        bsizer.addLayout(sizer1)
        self._box.setLayout(bsizer)
        sizer.addWidget(self._box)

    def captions_extra_fields(self):
        """to be called on changing the language
        """
        self.cb_win.setText(self.parent.captions['M_WIN'].join(("+", "  ")))
        self.cb_ctrl.setText(self.parent.captions['M_CTRL'].join(("+", "  ")))
        self.cb_alt.setText(self.parent.captions['M_ALT'].join(("+", "  ")))
        self.cb_shift.setText(self.parent.captions['M_SHFT'].join(("+", "  ")))
        self.b_save.setText(self.parent.captions['C_SAVE'])
        self.b_del.setText(self.parent.captions['C_DEL'])
        self.txt_key.setText(self.parent.captions['C_KTXT'])
        self.txt_cmd.setText(self.parent.captions['C_CTXT'])

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
        ## print(self.parent.data[seli])
        ## key, mods, soort, cmd, oms = self.parent.data[seli]
        keydefdata = self.parent.data[seli]
        self.b_save.setEnabled(False)
        self.b_del.setEnabled(False)
        self._origdata = ['', False, False, False, False, '']
        for indx, item in enumerate(keydefdata):
            if self.parent.column_info[indx][0] == 'C_KEY':
                key = item
                ix = self.keylist.index(key)
                self.cmb_key.setCurrentIndex(ix)
                ## self.cmb_key.setEditText(key)
                self._origdata[0] = key
            elif self.parent.column_info[indx][0] == 'C_MODS':
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
            elif self.parent.column_info[indx][0] == 'C_TYPE':
                soort = item
                if soort == 'U':
                    self.b_del.setEnabled(True)
            elif self.parent.column_info[indx][0] == 'C_CMD':
                command = item
                ix = self.commandlist.index(command)
                self.cmb_commando.setCurrentIndex(ix)
                self._origdata[5] = command
            elif self.parent.column_info[indx][0] == 'C_DESC':
                oms = item
                self.txt_oms.setText(oms)
        self._newdata = self._origdata[:]
        ## print('Na vuldetails:', self._origdata, self._newdata)

    def aanpassen(self, delete=False): # TODO
        print('aanpassen called')
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

def _translate_keyname(inp):
    convert = {'Pgup': 'PgUp', 'Pgdn': 'PgDn'}
    if inp in convert:
        out = convert[inp]
    else:
        out = inp
    return out

def buildcsv(parent, showinfo=True):

    if showinfo:
        dlg = TCMergeDialog(parent)
        dlg.load_files((
            parent.page.settings['KB_PAD'][0],
            parent.page.settings['CI_PAD'][0],
            parent.page.settings['UC_PAD'][0],
            parent.page.settings['TC_PAD'][0],
            parent.page.pad))
        ok = dlg.exec_()
        if ok == gui.QDialog.Accepted:
            shortcuts = parent.tempdata
        else:
            shortcuts = []
    else:
        shortcuts = []
    return shortcuts, {}

class TCMergeDialog(gui.QDialog):
    """Dialoog om een gedocumenteerde toetscombinatie te koppelen aan een commando

    In het ene ini bestand staat namelijk toets + omschrijving en in het andere
    command + omschrijving en de omschrijvingen hoeven uiteraard niet 100% gelijk
    te zijn, dus moeten ze handmatig gekoppeld worden. Vandaar de ietwat misleidende
    naam "links"
    """

    def __init__(self, parent):
        """Opbouwen van het scherm"""
        self.shortcuts = {}
        self.basedir = os.getcwd()
        gui.QDialog.__init__(self, parent)
        self.setWindowTitle("TCCM")
        self.resize(700,486)

        cb = gui.QComboBox(self)
        cb.setMinimumWidth(160)
        cb.currentIndexChanged[str].connect(functools.partial(self.on_choice, cb))
        te = gui.QTextEdit(self)
        te.setMaximumHeight(80)
        te.setReadOnly(True)
        self.cmb_key = cb
        self.txt_key = te
        cb = gui.QComboBox(self)
        cb.setMinimumWidth(160)
        cb.currentIndexChanged[str].connect(functools.partial(self.on_choice, cb))
        te = gui.QTextEdit(self)
        te.setMaximumHeight(80)
        te.setReadOnly(True)
        self.cmb_cmd = cb
        self.txt_cmd = te

        self.btn_link = gui.QPushButton("&+ Add/Replace Link", self)
        self.btn_link.clicked.connect(self.make_link)
        ## self.btn_edit = gui.QButton(pnl,-1,"&Modify Link")
        ## self.btn_edit.Bind(gui.QEVT_BUTTON,self.edit_link)
        self.btn_delete = gui.QPushButton("&- Discard Link", self)
        self.btn_delete.clicked.connect(self.delete_link)

        self.lst_links = gui.QTreeWidget(self)
        self.lst_links.resize(660,300)
        widths = (100, 60, 180, 300)
        self.lst_links.setHeaderLabels(("Key", "Modifier(s)","Type", "Command", "Description"))
        hdr = self.lst_links.header()
        hdr.setClickable(True)
        for indx, wid in enumerate(widths):
            hdr.resizeSection(indx, wid)
        hdr.setStretchLastSection(True)
        self.lst_links.currentItemChanged.connect(self.enable_edit)

        self.btn_save = gui.QPushButton("&Save Links", self)
        self.btn_save.clicked.connect(self.accept)
        self.btn_quit = gui.QPushButton("&Afsluiten", self)
        self.btn_quit.clicked.connect(self.reject)

        self.btn_link.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.btn_save.setEnabled(False)

        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.cmb_key)
        ## vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.txt_key)
        ## vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.cmb_cmd)
        ## vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.txt_cmd)
        ## vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.btn_link)
        hbox.addWidget(self.btn_delete)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.lst_links)
        hbox.addLayout(vbox2)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.btn_save)
        hbox.addWidget(self.btn_quit)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def load_files(self, files):
        """load definitions from the various input files"""

        # keycombinations
        pad = files[0]
        # fill list box
        self.keydict = defaultkeys(pad) # dict(keyboardtext(pad))
        self.cmb_key.clear()
        test = [' '.join(x) for x in sorted(self.keydict.keys())]
        self.cmb_key.addItems(test)
        self.cmb_key.setCurrentIndex(0)
        test = tuple(str(self.cmb_key.itemText(self.cmb_key.currentIndex())).split())
        # set text of first entry
        this = self.keydict[test]
        self.txt_key.setText(this["oms"])

        # commands
        pad = files[1]
        # fill list box
        self.cmddict = defaultcommands(pad)
        ## self.cmds = dict([reversed(x) for x in self.cmddict.items()])
        self.cmb_cmd.clear()
        test = sorted(self.cmddict.keys())
        self.cmb_cmd.addItems(test)
        ## self.cmb_cmd.insertItems(0, '')
        self.cmb_cmd.setCurrentIndex(0)
        ## # set text of first entry
        ## self.txt_cmd.setText('no command available') #self.omsdict[self.cmb_cmd.GetValue()])

        ## # user commands (should be added to right list box?)
        ## self.usrdict, self.uomsdict = usercommands(files[2])

        ## # user defined keys (should be added to left list box?)
        ## self.usrkeys = dict(userkeys(files[3]))

        self.data = []

        # keydefs from csv file
        # nogmaals: je moet hier een ander bestand lezen; ik wil hier alleen de defaults
        # en het csv file bevat ook de wijzigingen
        self.lst_links.clear()
        self.btn_link.setEnabled(True)
        rdr = csv.reader(open(files[4], 'r'))
        for row in rdr:
            if row[0] != 'Keydef':
                continue
            new = gui.QTreeWidgetItem(row[1:])
            self.lst_links.addTopLevelItem(new)
            ## ix = self.lst_links.InsertStringItem(sys.maxint,row[0])
            ## self.lst_links.SetStringItem(ix,1,row[1])
            ## self.lst_links.SetStringItem(ix,2,row[2])
            ## self.lst_links.SetStringItem(ix,3,row[3])
        self.btn_save.setEnabled(True)

    def on_choice(self, cb, text):
        text = str(text)
        ## self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)
        if cb == self.cmb_key:
            test = tuple(text.split())
            try:
                self.txt_key.setText(self.keydict[test]["oms"])
            except KeyError:
                self.txt_key.setText('no key description available')
        elif cb == self.cmb_cmd:
            try:
                self.txt_cmd.setText(self.cmddict[text]["oms"])
            except KeyError:
                self.txt_cmd.setText('no command description available')

    def get_entry(self):
        gekozen_key = str(self.cmb_key.currentText())
        gekozen_cmd = str(self.cmb_cmd.currentText())
        print(gekozen_key, gekozen_cmd)
        try:
            gekozen_oms = self.omsdict[gekozen_cmd]
        except KeyError:
            gekozen_cmd = ''
            gekozen_oms = self.keydict[gekozen_key]
            gekozen_code = ''
        else:
            gekozen_code = self.cmds[gekozen_cmd]
        return gekozen_key, gekozen_code, gekozen_cmd, gekozen_oms

    def make_link(self,evt):
        gekozen_key, gekozen_code, gekozen_cmd, gekozen_oms = self.get_entry()
        # let op: als link al bestaat: vervangen, niet toevoegen
        found = False
        for ix in range(self.lst_links.topLevelItemCount()):
            item = self.lst_links.topLevelItem(ix)
            if str(item.text(0)) == gekozen_key:
                found = True
                break
        if not found:
            item = gui.QTreeWidgetItem()
            item.setText(0, gekozen_key)
            self.lst_links.addTopLevelItem(item)
        item.setText(1,gekozen_code)
        item.setText(2,gekozen_cmd)
        item.setText(3,gekozen_oms)
        ## self.lst_links.EnsureVisible(ix)
        self.btn_save.setEnabled(True)

    def enable_edit(self, item, previtem):
        gekozen_key = ' '.join((str(item.text(0)), str(item.text(1))))
        gekozen_cmd = str(item.text(2))
        self.cmb_key.setCurrentIndex(sorted(self.keydict.keys()).index(gekozen_key)) # setEditText(gekozen_key)
        # let op: het volgende gaat niet werken als menu optie 1 nog niet is uitgevoerd
        self.txt_key.setText(self.keydict[gekozen_key])
        self.cmb_cmd.setCurrentIndex(sorted(self.omsdict.keys()).index(gekozen_cmd)) # setEditText(gekozen_cmd)
        try:
            self.txt_cmd.setText(self.omsdict[gekozen_cmd])
        except KeyError:
            self.txt_cmd.setText('no command available')
        ## self.btn_edit.Enable()
        self.btn_delete.setEnabled(True)

    ## def edit_link(self,evt):
        ## gekozen_key, gekozen_code, gekozen_cmd, gekozen_oms = self.get_entry()
        ## self.lst_links.SetStringItem(ix,0,gekozen_key)
        ## self.lst_links.SetStringItem(ix,1,gekozen_code)
        ## self.lst_links.SetStringItem(ix,2,gekozen_cmd)
        ## self.lst_links.SetStringItem(ix,3,gekozen_oms)
        ## self.ix = -1
        ## self.btn_edit.Disable()
        ## self.btn_delete.Disable()

    def delete_link(self, evt):
        ok = gui.QMessageBox.question(self, "Delete entry", "Really delete?",
            gui.QMessageBox.Yes | gui.QMessageBox.No,
            defaultButton = gui.QMessageBox.Yes)
        if ok == gui.QMessageBox.Yes:
            item = self.lst_links.currentItem()
            ix = self.lst_links.indexOfTopLevelItem(item)
            self.lst_links.takeTopLevelItem(ix)
            ## self.btn_edit.Disable()
            self.btn_delete.setEnabled(False)

    def reset_all(self,evt):
        self.lst_links.clear()
        self.btn_link.setEnabled(True)
        self.data = []

    def accept(self):
        # don't save to file; just assign to a global variable
        ## fname = gui.QFileDialog.getSaveFileName(self, "Save definition file",
            ## os.path.join(self.basedir, "TC_hotkeys.csv"), "csv files (*.csv)")
        ## if fname:
            ## wrtr = csv.writer(open(fname,"wb"))
            ## for ix in range(self.lst_links.topLevelItemCount()):
                ## item = self.lst_links.topLevelItem(ix)
                ## wrtr.writerow([str(item.text(x)) for x in range(4)])
        shortcuts = {}
        for ix in range(self.lst_links.topLevelItemCount()):
            item = self.lst_links.topLevelItem(ix)
            item[0] = _translate_keyname(item[0])
            shortcuts[ix] = [str(item.text(x)) for x in range(4)]
        self.parent().tempdata = shortcuts
        gui.QDialog.accept(self)

