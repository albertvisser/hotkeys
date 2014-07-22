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

C_SAVE, C_DEL, C_KTXT, C_CTXT ='010', '011', '018', '019'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
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
        if h[0] in ('SHIFT','ALT','CTRL'):
            mods += h[0][0]
        h = h[1].split("+",1)
    keyc = h[0].replace(" ","").capitalize() + extra
    if keyc == '\\':
        keyc = 'OEM_US\\|'
    if mods != "":
        keyc = ' + '.join((keyc,mods))
    return keyc

def keyboardtext(root):
    """definities uit keyboard.txt omzetten in standaard definities
    """
    data = []
    i = 0
    ky = []
    join_keys = False
    with open(os.path.join(root,'KEYBOARD.TXT')) as f_in:
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
                            data.append((keymods2('+'.join((h[0], it))), ky_desc))
                    else:
                        data.append((keymods2(k), ky_desc))
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
            ## print ky,ky_desc
    if len(ky) > 0:
        for k in ky:
            h = k.rsplit('+',1)
            if '/' in h[-1] and not h[-1].endswith('/'):
                hlp = h[-1].split('/')
                for it in hlp:
                    data.append((keymods2('+'.join((h[0], it))), ky_desc))
            else:
                data.append((keymods2(k), ky_desc))
    ## f = open("keyboard_keys.txt","w")
    ## for x,y in data:
        ## f.write("%s:: %s\n" % (x,y))
    ## f.close()
    return data

def defaultcommands(root):
    """definities uit totalcmd.inc omzetten in standaard definites

    geeft commandonamen en omschrijvingen terug in dictionaries met commandonummer
    als sleutel
    """
    omsdict = {'': "no command available"}
    cmdict = {'': ''}
    with open(os.path.join(root,'TOTALCMD.INC')) as _in:
        for x in _in:
            h = x.strip()
            if h == '' or h[0] == '[' or h[0] == ';':
                continue
            cm_naam, rest = h.split('=',1)
            cm_num, cm_oms = rest.split(';',1)
            if int(cm_num) > 0:
                cmdict[cm_num] = cm_naam
                omsdict[cm_naam] = cm_oms # c[1] is omschrijving
    return cmdict, omsdict

def usercommands(root, cmdict=None, omsdict=None):
    """definities uit usercmd.ini omzetten in standaard definities

    vult cmdict en omsdict aan en retourneert ze
    """
    if cmdict is None:
        cmdict = {}
    if omsdict is None:
        omsdict = {}
    s0 = ""
    with open(os.path.join(root,"usercmd.ini")) as _in:
        for x in _in:
            if x.startswith("["):
                if s0 != "":
                    omsdict[s0] = c1
                s0 = x[1:].split("]")[0]
                c1 = ""
            elif x.startswith("cmd") and c1 == "":
                c1 = x.strip().split("=")[1]
            elif x.startswith("menu"):
                c1 = x.strip().split("=")[1]
        omsdict[s0] = c1
    ## print "na lezen usercmd.ini",datetime.datetime.today()
    ## f = open("cmdict.txt","w")
    ## for x in cmdict:
        ## f.write("%s:: %s\n" % (x,cmdict[x]))
    ## f.close()
    ## f = open("omsdict.txt","w")
    ## for x in omsdict:
        ## f.write("%s:: %s\n" % (x,omsdict[x]))
    ## f.close()
    return cmdict,omsdict

def defaultkeys(root):
    """definities lezen uit TC_hotkeys.csv (mijn eigen omzetter - in plaats van die
    die bij Ultra TC Editors meekomt
    """
    data = []
    ## for x in file(os.path.join(root,"tc default hotkeys.hky")):
        ## if x[0] == ";":
            ## continue
        ## elif "=" in x:
            ## y = x[:-1].split("=")
            ## #~ print y
            ## for z in y[1:]:
                ## #~ print z
                ## q = z.split(" + ")
                ## q[-1] = q[-1].replace(" ","")
                ## if len(q) == 1:
                    ## key = q[0].capitalize()
                ## else:
                    ## key = "".join([w.strip()[0] for w in q[:-1]])
                    ## key = " + ".join((q[-1].capitalize(),key))
                ## #~ print datakey
                ## data.append((key,y[0]))
    ## #~ f = open("defaultkeys.txt","w")
    ## #~ for x,y in data:
    ## #~     f.write("%s:: %s\n" % (x,y))
    ## #~ f.close()
    try:
        rdr = csv.reader(open(os.path.join(root,"TC_hotkeys.csv"), 'r'))
    except IOError:
        rdr = []
    for row in rdr:
        data.append((row[0], row[1]))
        ## data = [(row[0],row[1]) for row in rdr]
    return data

def userkeys(root):
    """user key definities uit wincmd.ini lezen
    """
    data = []
    in_user = in_win = False
    with open(os.path.join(root,"wincmd.ini")) as f_in:
        for x in f_in:
            x = x.rstrip()
            y = x.split("=")
            for h in ('+', '-', '/', '*'):
                if y[0].endswith(h):
                    y[0] = y[0][:-1] + 'NUM' + y[0][-1]
            if in_user:
                if x.startswith("["):
                    in_user = False
                else:
                    data.append(y)
            elif in_win:
                if x.startswith("["):
                    in_win = False
                else:
                    if '+' in y[0]:
                        y[0] = 'W' + y[0]
                    else:
                        y[0] = 'W+' + y[0]
                    data.append(y)
            elif x.startswith("[Shortcuts]"):
                in_user = True
            elif x.startswith("[ShortcutsWin]"):
                in_win = True
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

def savekeys(settings, data):
    """schrijft de listbox data terug via een tckeys object
    """
    paden = [settings[x][0] for x in ('TC_PAD', 'UC_PAD', 'CI_PAD', 'KB_PAD',
        'HK_PAD')]
    cl = TCKeys(*paden)
    for val in data.values():
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
        cmdict, omsdict = defaultcommands(self.ciloc)
        self.cmdict, self.omsdict = usercommands(self.ucloc, cmdict, omsdict)
        defkeys = {}
        for x, y in defaultkeys(self.hkloc):
            defkeys[x] = self.cmdict[y].strip()
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

    def add_extra_attributes(self):
        self._origdata = ["", False, False, False, False, ""]
        self._newdata = self._origdata[:]
        self.mag_weg = True
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        paden = [self.parent.settings[x][0] for x in PATHS]
        self.cmdict, self.omsdict, self.defkeys, _ = readkeys(paden)

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        self._box = box = gui.QFrame(self)
        box.setFrameShape(gui.QFrame.StyledPanel)
        box.setMaximumHeight(90)
        self.txt_key = gui.QLabel(self.parent.captions[C_KTXT] + " ", box)
        self.keylist = [x for x in string.ascii_uppercase] + \
            [x for x in string.digits] + ["F" + str(i) for i in range(1,13)] + \
            [self.parent.captions[str(x)] for x in range(100,121)] + \
            ['Pause', 'Period', 'Comma', 'Plus', 'Minus', 'Smaller/Greater',
            'Backtick/Tilde', 'Brackets open', 'Brackets close', 'Backslash/Pipe',
            'Semicolon/colon', 'Apostrophe/Quote', 'Slash/Questionmark', 'OEM_FR!']
            ## ['PAUSE', 'OEM_.', 'OEM_,', 'OEM_+', 'OEM_-', 'OEM_</>', 'OEM_US`~',
            ## 'OEM_US[{', 'OEM_US]}', 'OEM_US\\|', 'OEM_US;:', "OEM_US'" + '"',
            ## 'OEM_US/?', 'OEM_FR!']
        not_found = []
        for key, value in self.parent.data.items():
            if value[0] not in self.keylist:
                ## print(value)
                not_found.append(key)
        for key in not_found:
            del self.parent.data[key]
        cb = gui.QComboBox(box)
        cb.addItems(self.keylist)
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_key = cb

        for x in (M_CTRL, M_ALT, M_SHFT, M_WIN):
            cb = gui.QCheckBox(self.parent.captions[x].join(("+","  ")), box) #, (65, 60), (150, 20), gui.QNO_BORDER)
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
        self.commandlist = [x for x in self.omsdict.keys()]
        self.commandlist.sort()
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

        self.txt_oms = gui.QTextEdit(box)
        self.txt_oms.setMaximumHeight(40)
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
        ## print(self.parent.data[seli])
        key, mods, soort, cmd, oms = self.parent.data[seli]
        self.b_save.setEnabled(False)
        self.b_del.setEnabled(False)
        if soort == 'U':
            self.b_del.setEnabled(True)
        self._origdata = [key, False, False, False, False, cmd]
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
        self.txt_oms.setText(oms)
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




