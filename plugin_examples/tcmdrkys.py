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



def _translate_keyname(inp):
    convert = {'Pgup': 'PgUp', 'Pgdn': 'PgDn', 'Period' : '.', 'Comma': ',',
        'Plus': '+', 'Minus': '-', 'Backtick/Tilde': '`', 'Brackets open': '[',
        'Brackets close': ']', 'Backslash/Pipe': '\\', 'Semicolon/colon': ';',
        'Apostrophe/Quote': "'", 'Slash/Questionmark': '/'}
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


def add_extra_attributes(win):
    win.keylist += ['Pause', 'Smaller/Greater', 'OEM_FR!']
    ## ['PAUSE', 'OEM_.', 'OEM_,', 'OEM_+', 'OEM_-', 'OEM_</>', 'OEM_US`~',
    ## 'OEM_US[{', 'OEM_US]}', 'OEM_US\\|', 'OEM_US;:', "OEM_US'" + '"',
    ## 'OEM_US/?', 'OEM_FR!']

    win.mag_weg = True
    win.newfile = win.newitem = False
    win.oldsort = -1
    win.idlist = win.actlist = win.alist = []
    paden = [win.settings[x][0] for x in PATHS[:4]] + [win.pad]
    ## self.cmdict, self.omsdict, self.defkeys, _ = readkeys(paden)
    win.descriptions = {}
    win.cmdict = defaultcommands(win.settings['CI_PAD'][0])
    win.descriptions.update({x: y['oms'] for x, y in win.cmdict.items()})
    win.ucmdict = usercommands(win.settings['UC_PAD'][0])
    win.descriptions.update({x: y['oms'] for x, y in win.ucmdict.items()})
    win.defkeys = defaultkeys(win.settings['KB_PAD'][0])
    win.udefkeys = userkeys(win.settings['TC_PAD'][0])

    win.commandslist = list(win.cmdict.keys()) + list(win.ucmdict.keys())

def get_frameheight():
    return 110
