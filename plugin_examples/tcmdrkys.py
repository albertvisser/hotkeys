# -*- coding: utf-8 -*-
"""Hotkeys plugin for Total Commander
"""
from __future__ import print_function
import os
## import sys
## import string
## import datetime
from xml.etree import ElementTree as ET
import csv
## import shutil
import functools
import logging
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
logging.basicConfig(filename='/home/albert/projects/hotkeys/editor/logs/tcmdrkeys.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
DFLT_TCLOC = "C:/totalcmd"
PATHS = ('TC_PAD', 'UC_PAD', 'CI_PAD', 'KB_PAD', 'HK_PAD')
OKICON = '/usr/share/icons/Adwaita/16x16/emblems/emblem-ok-symbolic.symbolic.png'


def log(message):
    "write to log"
    logging.info(message)


def read_lines(fn):
    "return lines read from file"
    result = []
    try:
        with open(fn) as f_in:
            result = f_in.readlines()
    except UnicodeDecodeError:
        with open(fn, encoding='latin-1') as f_in:
            result = f_in.readlines()
    return result


def keymods(x):
    """hulp bij omzetten wincmd.ini definitie in standaard definitie
    """
    ## m = {'A': 'Alt', 'C': 'Ctrl', 'S': 'Shift', 'W': 'Win'}
    if x == "NUM +":
        y = ''
        keyc = x
    else:
        y = x.split('+', 1)
        keyc = y[-1]
    keyc = keyc.replace(" ", "").capitalize()
    if len(y) > 1:
        mods = [z[0] for z in y[0]]
        keyc = ' + '.join((keyc, ''.join(mods)))
    return keyc


def keymods2(x):
    """hulp bij omzetten keyboard.txt definitie in standaard definitie
    """
    extra = ""
    if x[-1] == "+":
        x = x[:-1]
        extra = "+"
    mods = ""
    h = x.split("+", 1)
    while len(h) > 1:
        ## if h[0] in ('SHIFT','ALT','CTRL'):
        if h[0] in ('CTRL', 'ALT', 'SHIFT'):
            mods += h[0][0]
        h = h[1].split("+", 1)
    keyc = h[0].replace(" ", "").capitalize() + extra
    if keyc == '\\':
        keyc = 'OEM_US\\|'
    ## keyc = ' + '.join((keyc,mods))
    mods = mods.replace('SC', 'CS')
    return keyc, mods


def defaultcommands(root):
    """mapping uit totalcmd.inc omzetten in een Python dict
    """
    cmdict = {'': {"oms": "no command available"}}
    for x in read_lines(root):
        h = x.strip()
        if h == '' or h[0] == '[' or h[0] == ';':
            continue
        cm_naam, rest = h.split('=', 1)
        cm_num, cm_oms = rest.split(';', 1)
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
    for x in read_lines(root):
        if x.startswith("["):
            if em_name:
                ucmdict[em_name] = em_value
            em_name = x[1:].split("]")[0]  # x[1:-1] had ook gekund maar dit is safer
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
    ky = []
    ky_desc = ''
    join_keys = False
    temp = read_lines(root)
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
                        ky[y[0] + 1] = "+".join((s2, y[1]))
            elif deel1.endswith(" or"):
                ky = [deel1[:-3], ""]
                join_keys = True
            else:
                ky = [deel1]
    if len(ky) > 0:
        for k in ky:
            h = k.rsplit('+', 1)
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
    for line in read_lines(root):
        line = line.rstrip()
        ## linesplit = line.split("=")
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
    ## defkeys = cl.defkeys
    ## kys = cl.keydict.keys()
    ## kys.sort()
    data = {}
    for ix, hotkey in enumerate(sorted(cl.keydict.keys())):
        try:
            ky, mod = hotkey.split(" + ")
        except ValueError:
            ky, mod = hotkey, ""
        srt, desc, cmd = cl.keydict[hotkey]
        data[ix] = (ky, mod, srt, cmd, desc)
    return cl.cmdict, cl.omsdict, cl.defkeys, data


def savekeys(parent):
    """schrijft de listbox data terug via een tckeys object
    """
    paden = [parent.settings[x] for x in PATHS]
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
            self.tcloc = tc_dir[0]  # plaats van wincmd.ini
        except IndexError:
            self.tcloc = DFLT_TCLOC
        try:
            self.ucloc = tc_dir[1]  # plaats van usercmd.ini
        except IndexError:
            pass
        if not self.ucloc:
            self.ucloc = self.tcloc
        try:
            self.ciloc = tc_dir[2]  # plaats van totalcmd.inc
        except IndexError:
            pass
        if not self.ciloc:
            self.ciloc = self.tcloc
        try:
            self.ktloc = tc_dir[3]  # plaats van keyboard.txt
        except IndexError:
            pass
        if not self.ktloc:
            self.ktloc = self.tcloc
        try:
            self.hkloc = tc_dir[4]  # plaats van tc_hotkeys.csv
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
        self.cmdict = defaultcommands(self.ciloc)
        with open("cmdict.txt", "w") as _out:
            print(self.cmdict, file=_out)
        ucmdict = usercommands(self.ucloc)
        with open("usercmdict.txt", "w") as _out:
            print(ucmdict, file=_out)
        self.omsdict = {}
        # deze zijn hier aangevuld met de zaken uit usercommands
        defkeys = {}
        for x, y in defaultkeys(self.hkloc):
            defkeys[x] = self.cmdict[y].strip()
        # de nummers die ik in y wil hebben zitten in de vierde kolom alleen dan zijn het de
        # strings m.a.w. dit kan helemaal niet
        self.keydict = {}
        for key, oms in keyboardtext(self.ktloc):   # UNDEF keyboardtext - should be a function
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
            self.keydict[k] = ("U", self.omsdict[action], action)

    def turn_into_xml(self):
        """zet de gegevens uit keydict om in xml en schrijft ze weg
        """
        kys = self.keydict.keys()
        kys.sort()
        root = ET.Element("keys")
        for x in kys:
            h = ET.SubElement(root, "hotkey", naam=x, soort=self.keydict[x][0])
            k = ET.SubElement(h, "cmd")
            k.text = self.keydict[x][2]
            k = ET.SubElement(h, "oms")
            k.text = self.keydict[x][1]
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.tcloc, "tcmdrkeys.xml"))

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
                    ## win_geschreven = True
                    for newline in shortcutswin:
                        f_out.write(newline)
                if schrijfdoor:
                    f_out.write(line)
            if not shortcuts_geschreven and len(shortcuts) > 0:
                for newline in shortcuts:
                    f_out.write(newline)
            if not win_geschreven and len(shortcuts) > 0:
                for newline in shortcutswin:
                    f_out.write(newline)


def _translate_keyname(inp):
    """helper function to convert text from settings into text for this app
    """
    convert = {'Pgup': 'PgUp', 'Pgdn': 'PgDn', 'Period': '.', 'Comma': ',',
               'Plus': '+', 'Minus': '-', 'Backtick/Tilde': '`',
               'Brackets open': '[', 'Brackets close': ']', 'Backslash/Pipe': '\\',
               'Semicolon/colon': ';', 'Apostrophe/Quote': "'",
               'Slash/Questionmark': '/', 'OEM_US\|': '\\'}
    if inp in convert:
        out = convert[inp]
    else:
        out = inp
    return out


def buildcsv(parent, showinfo=True):
    """implementation of generic function to build the csv file
    """
    if showinfo:
        dlg = TCMergeDialog(parent)
        paths = [parent.page.settings[x] for x in reversed(PATHS[:4])]
        paths.append(parent.page.pad)
        dlg.load_files(paths)
        ## dlg.load_files((
            ## parent.page.settings['KB_PAD'][0],
            ## parent.page.settings['CI_PAD'][0],
            ## parent.page.settings['UC_PAD'][0],
            ## parent.page.settings['TC_PAD'][0],
            ## parent.page.pad))
        ok = dlg.exec_()
        if ok == qtw.QDialog.Accepted:
            shortcuts = parent.tempdata
        else:
            shortcuts = []
    else:
        shortcuts = []
    return shortcuts, {}


class TCMergeDialog(qtw.QDialog):
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
        super().__init__(parent)
        self.setWindowTitle("TCCM")
        self.okicon = gui.QIcon(OKICON)
        self.resize(1000, 600)

        self.listkeys = qtw.QTreeWidget(self)
        self.listkeys.setColumnCount(2)
        self.listkeys.setHeaderLabels(['Key', 'Description'])
        self.listkeys.setMouseTracking(True)
        self.listkeys.itemEntered.connect(self.popuptext)
        self.listcmds = qtw.QTreeWidget(self)
        self.listcmds.setColumnCount(2)
        self.listcmds.setHeaderLabels(['Command', 'Description'])
        self.listcmds.setMouseTracking(True)
        self.listcmds.itemEntered.connect(self.popuptext)
        self.listlinks = qtw.QTreeWidget(self)
        self.listlinks.setColumnCount(2)
        self.listlinks.setHeaderLabels(['Key', 'Command'])

        self.findkeytext = qtw.QLineEdit(self)
        self.nextkey = qtw.QPushButton('&Next', self)
        self.nextkey.setMaximumWidth(50)
        self.nextkey.clicked.connect(self.findnextkey)
        self.prevkey = qtw.QPushButton('&Prev', self)
        self.prevkey.setMaximumWidth(50)
        self.prevkey.clicked.connect(self.findprevkey)
        self.findcmdtext = qtw.QLineEdit(self)
        self.nextcmd = qtw.QPushButton('Ne&xt', self)
        self.nextcmd.setMaximumWidth(50)
        self.nextcmd.clicked.connect(self.findnextcmd)
        self.prevcmd = qtw.QPushButton('Pre&v', self)
        self.prevcmd.setMaximumWidth(50)
        self.prevcmd.clicked.connect(self.findprevcmd)

        self.btn_link = qtw.QPushButton("&+ Add/Replace Link", self)
        self.btn_link.clicked.connect(self.make_link)
        ## self.btn_edit = qtw.QButton(pnl,-1,"&Modify Link")
        ## self.btn_edit.Bind(qtw.QEVT_BUTTON,self.edit_link)
        self.btn_delete = qtw.QPushButton("&- Discard Link", self)
        self.btn_delete.clicked.connect(self.delete_link)

        self.btn_load = qtw.QPushButton("&Load Links", self)
        self.btn_load.clicked.connect(self.load_links)
        self.btn_clear = qtw.QPushButton("&Clear All", self)
        self.btn_clear.clicked.connect(self.reset_all)
        self.btn_save = qtw.QPushButton("&Save Links", self)
        self.btn_save.clicked.connect(self.save_links)
        self.btn_quit = qtw.QPushButton("&Afsluiten", self)
        self.btn_quit.clicked.connect(self.reject)
        self.btn_build = qtw.QPushButton("&Build CSV", self)
        self.btn_build.clicked.connect(self.accept)

        for text, callback, keyseq in (
                ('keylist', self.focuskeylist, 'Ctrl+1'),
                ('cmdlist', self.focuscmdlist, 'Ctrl+2'),
                ('findkey', self.focusfindkey, 'Ctrl+F'),
                ('nextkey', self.findnextkey, 'Ctrl+N'),
                ('prevkey', self.findprevkey, 'Ctrl+P'),
                ('findcmd', self.focusfindcmd, 'Ctrl+Shift+F'),
                ('nextcmd', self.findnextcmd, 'Ctrl+Shift+N'),
                ('prevcmd', self.findprevcmd, 'Ctrl+Shift+P'),
                ('addlink', self.make_link, 'Ctrl++'),
                ('remlink', self.delete_link, 'Del'),
                ('load', self.load_links, 'Ctrl+L'),
                ('clear', self.reset_all, 'Ctrl+Del'),
                ('save', self.accept, 'Ctrl+S'),
                ('quit', self.close, 'Ctrl+Q')):
            act = qtw.QAction(text, self)
            act.triggered.connect(callback)
            act.setShortcut(keyseq)
            self.addAction(act)

        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.listkeys)
        hbox.addWidget(self.listcmds)
        hbox.addWidget(self.listlinks)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox2 = qtw.QHBoxLayout()
        hbox2.addWidget(qtw.QLabel('Find text:', self))
        hbox2.addWidget(self.findkeytext)
        hbox2.addWidget(self.nextkey)
        hbox2.addWidget(self.prevkey)
        hbox2.addStretch()
        hbox.addLayout(hbox2)
        hbox2 = qtw.QHBoxLayout()
        hbox2.addWidget(qtw.QLabel('Find text:', self))
        hbox2.addWidget(self.findcmdtext)
        hbox2.addWidget(self.nextcmd)
        hbox2.addWidget(self.prevcmd)
        hbox2.addStretch()
        hbox.addLayout(hbox2)
        hbox2 = qtw.QHBoxLayout()
        hbox2.addStretch()
        hbox2.addWidget(self.btn_link)
        hbox2.addWidget(self.btn_delete)
        hbox2.addStretch()
        hbox.addLayout(hbox2)
        vbox.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.btn_load)
        hbox.addWidget(self.btn_clear)
        hbox.addWidget(self.btn_save)
        hbox.addWidget(self.btn_quit)
        hbox.addWidget(self.btn_build)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.keysearch = self.cmdsearch = ''
        self.keyresults, self.cmdresults = [], []

    def load_files(self, files):
        """load definitions from the various input files"""
        self.keyspad = files[0]
        self.cmdspad = files[1]
        self.linkspad = os.path.join(os.path.dirname(__file__),
                                     'tc_default_hotkeys_mapped.csv')
        self.load_keys()
        self.load_commands()

        ## # user commands (should be added to right list box?)
        ## self.usrdict, self.uomsdict = usercommands(files[2])

        ## # user defined keys (should be added to left list box?)
        ## self.usrkeys = dict(userkeys(files[3]))
        self.listlinks.clear()

    def load_keys(self):
        """load keyboard definitions"""

        # keycombinations
        # fill list box
        self.keydict = defaultkeys(self.keyspad)  # dict(keyboardtext(pad))
        self.listkeys.clear()
        self.keydata, self.keytexts = [], []
        for key, value in sorted(self.keydict.items()):
            new = qtw.QTreeWidgetItem()
            new.setText(0, ' '.join(key))
            new.setData(0, core.Qt.UserRole, key)
            new.setText(1, value['oms'])
            self.listkeys.addTopLevelItem(new)
            self.keydata.append(key)
            self.keytexts.append(value['oms'])

    def load_commands(self):
        """load command definitions"""
        # commands
        # fill list box
        self.cmddict = defaultcommands(self.cmdspad)
        self.listcmds.clear()
        self.cmddata, self.cmdtexts = [], []
        for key, value in sorted(self.cmddict.items()):
            new = qtw.QTreeWidgetItem()
            new.setText(0, key)
            new.setText(1, value['oms'])
            self.listcmds.addTopLevelItem(new)
            self.cmddata.append(key)
            self.cmdtexts.append(value['oms'])

    def load_links(self):
        "load keydefs from temp file"
        self.reset_all()
        try:
            _in = open(self.linkspad, 'r')
        except FileNotFoundError:
            qtw.QMessageBox.information(self, 'Load data', "No saved data found")
            return

        with _in:
            rdr = csv.reader(_in)
            lines = [row for row in rdr]
        for key, mods, command in sorted(lines):
            keytext = ' '.join((key, mods))
            new = qtw.QTreeWidgetItem()
            new.setText(0, keytext)
            new.setData(0, core.Qt.UserRole, (key, mods))
            new.setText(1, command)
            self.listlinks.addTopLevelItem(new)
            try:
                item = self.listkeys.findItems(keytext,
                    core.Qt.MatchFixedString, 0)[0]
            except IndexError:
                # geen item - geen vermelding in KEYBOARD.TXT, wel bekend in hotkeys.hky
                pass
            item.setIcon(0, self.okicon)

    def focuskeylist(self):
        "Enter search phrase"
        self.listkeys.setFocus()

    def focuscmdlist(self):
        "Enter search phrase"
        self.listcmds.setFocus()

    def focusfindkey(self):
        "Enter search phrase"
        self.findkeytext.setFocus()

    def focusfindcmd(self):
        "Enter search phrase"
        self.findcmdtext.setFocus()

    def popuptext(self, item, colno):
        "show complete text of description if moused over"
        if colno == 1:
            item.setToolTip(colno, item.text(colno))

    def make_link(self):
        """connect the choices
        """
        keychoice = self.listkeys.currentItem()
        keytext, key = keychoice.text(0), keychoice.data(0, core.Qt.UserRole)
        cmdchoice = self.listcmds.currentItem()
        cmdtext = cmdchoice.text(0)

        # let op: als link al bestaat: vervangen, niet toevoegen
        found = False
        for ix in range(self.listlinks.topLevelItemCount()):
            item = self.listlinks.topLevelItem(ix)
            if item.text(0) == keytext:
                found = True
                break
        if not found:
            item = qtw.QTreeWidgetItem()
            item.setText(0, keytext)
            item.setData(0, core.Qt.UserRole, key)
            self.listlinks.addTopLevelItem(item)
        item.setText(1, cmdtext)
        ## item.setText(2, gekozen_cmd)
        ## item.setText(3, gekozen_oms)
        ## if found:
        self.listlinks.scrollTo(self.listlinks.indexFromItem(item))
        ## else:
        ## if not found:
            ## self.listlinks.scrollToBottom()
        keychoice.setIcon(0, self.okicon)

    def delete_link(self):
        """remove an association
        """
        item = self.listlinks.currentItem()
        if not item:
            qtw.QMessageBox.information(self, "Delete entry", "Choose an item to "
                "delete")
            return
        ok = qtw.QMessageBox.question(self, "Delete entry", "Really delete?",
                                      qtw.QMessageBox.Yes | qtw.QMessageBox.No,
                                      defaultButton=qtw.QMessageBox.Yes)
        if ok == qtw.QMessageBox.Yes:
            ix = self.listlinks.indexOfTopLevelItem(item)
            item = self.listlinks.takeTopLevelItem(ix)
            find = item.text(0)
            ## self.listkeys.finditems(find, core.Qt.MatchExactly, 0)
            item = self.listkeys.findItems(find, core.Qt.MatchFixedString, 0)[0]
            # beetje omslachtige manier van een icon verwijderen bij een TreeWidgetItem!
            newitem = qtw.QTreeWidgetItem()
            newitem.setText(0, item.text(0))
            newitem.setData(0, core.Qt.UserRole, item.data(0, core.Qt.UserRole))
            newitem.setText(1, item.text(1))
            ix = self.listkeys.indexOfTopLevelItem(item)
            self.listkeys.takeTopLevelItem(ix)
            self.listkeys.insertTopLevelItem(ix, newitem)

    def finditem(self, input, search, list, results):
        "check if search string has changed"
        to_find = input.text()
        if not to_find:
            qtw.QMessageBox.information(self, 'Find text',
                'Please enter text to search for')
            return None, None, None
        newsearch = to_find != search
        if newsearch:
            search = to_find
            results = list.findItems(search, core.Qt.MatchContains, 1)
        return newsearch, search, results

    def findnextitem(self, input, search, list, results):
        "search forward"
        newsearch, search, results = self.finditem(input, search, list, results)
        if not search:
            return
        current = list.currentItem()
        if not current:
            current = list.topLevelItem(0)
        if newsearch:
            # positioneren na huidige en klaar
            for item in results:
                if item.text(0) > current.text(0):
                    list.setCurrentItem(item)
                    return search, results
        else:
            # huidige zoeken in resultatenlijst, positioneren op volgende
            newix = results.index(current) + 1
            if newix < len(results):
                list.setCurrentItem(results[newix])
            else:
                list.setCurrentItem(results[0])
            return
        qtw.QMessageBox.information(self, 'Find text', 'No (next) item found')

    def findprevitem(self, input, search, list, results):
        "search backward"
        newsearch, search, results = self.finditem(input, search, list, results)
        if not search:
            return
        current = list.currentItem()
        if not current:
            current = list.topLevelItem(list.topLevelItemCount() - 1)
        if newsearch:
            # positioneren vóór huidige en klaar
            for item in reversed(results):
                if item.text(0) < current.text(0):
                    list.setCurrentItem(item)
                    return search, results
        else:
            # huidige zoeken in resultatenlijst, positioneren op vorige
            newix = results.index(current) - 1
            if newix >= 0:
                list.setCurrentItem(results[newix])
            else:
                list.setCurrentItem(results[-1])
            return
        qtw.QMessageBox.information(self, 'Find text', 'No previous item found')

    def findnextkey(self):
        "find next matching key item"
        test = self.findnextitem(self.findkeytext, self.keysearch, self.listkeys,
            self.keyresults)
        if test:
            self.keysearch, self.keyresults = test

    def findprevkey(self):
        "find previous matching key item"
        test = self.findprevitem(self.findkeytext, self.keysearch, self.listkeys,
            self.keyresults)
        if test:
            self.keysearch, self.keyresults = test

    def findnextcmd(self):
        "find next matching command item"
        test = self.findnextitem(self.findcmdtext, self.cmdsearch, self.listcmds,
            self.cmdresults)
        if test:
            self.cmdsearch, self.cmdresults = test

    def findprevcmd(self):
        "find previous matching command item"
        test = self.findprevitem(self.findcmdtext, self.cmdsearch, self.listcmds,
            self.cmdresults)
        if test:
            self.cmdsearch, self.cmdresults = test

    def reset_all(self):
        """remove all associations
        """
        self.listlinks.clear()
        self.load_keys() # to reset all indicators

    def save_links(self):
        """save the changes to a temp file
        """
        num_items = self.listlinks.topLevelItemCount()
        if num_items == 0:
            qtw.QMessageBox.information(self, 'Save data', 'No data to save')
            return
        with open(self.linkspad, "w") as _out:
            writer = csv.writer(_out)
            for ix in range(num_items):
                item = self.listlinks.topLevelItem(ix)
                try:
                    key, mods = item.data(0, core.Qt.UserRole)
                except ValueError:
                    key, mods = item.data(0, core.Qt.UserRole), ''
                    print(key)
                writer.writerow((key, mods, item.text(1)))
        qtw.QMessageBox.information(self, 'Save data', 'Data saved')

    def accept(self):
        """confirm the changes

        don't save to file; just assign to a global variable
        """
        shortcuts = {}
        for ix in range(self.listlinks.topLevelItemCount()):
            item = self.listlinks.topLevelItem(ix)
            key, mods = item.data(0, core.Qt.UserRole)
            cmd = item.text(1)
            if cmd:
                desc = self.cmddict[cmd]['oms']
            else:
                desc = self.keydict[(key, mods)]['oms']
            shortcuts[ix] = (_translate_keyname(key), mods, 'S', cmd, desc)
        self.parent().tempdata = shortcuts
        super().accept()


def add_extra_attributes(win):
    """define stuff needed to make editing in the subscreen possible
    """
    win.keylist += ['Pause', 'Smaller/Greater', 'OEM_FR!']
    ## ['PAUSE', 'OEM_.', 'OEM_,', 'OEM_+', 'OEM_-', 'OEM_</>', 'OEM_US`~',
    ## 'OEM_US[{', 'OEM_US]}', 'OEM_US\\|', 'OEM_US;:', "OEM_US'" + '"',
    ## 'OEM_US/?', 'OEM_FR!']

    win.mag_weg = True
    win.newfile = win.newitem = False
    win.oldsort = -1
    win.idlist = win.actlist = win.alist = []
    ## paden = [win.settings[x][0] for x in PATHS[:4]] + [win.pad]
    ## self.cmdict, self.omsdict, self.defkeys, _ = readkeys(paden)
    win.descriptions = {}
    win.cmdict = defaultcommands(win.settings['CI_PAD'])
    win.descriptions.update({x: y['oms'] for x, y in win.cmdict.items()})
    win.ucmdict = usercommands(win.settings['UC_PAD'])
    win.descriptions.update({x: y['oms'] for x, y in win.ucmdict.items()})
    win.defkeys = defaultkeys(win.settings['KB_PAD'])
    win.udefkeys = userkeys(win.settings['TC_PAD'])

    win.commandslist = list(win.cmdict.keys()) + list(win.ucmdict.keys())


def get_frameheight():
    """return standard height for the subscreen
    """
    return 110
