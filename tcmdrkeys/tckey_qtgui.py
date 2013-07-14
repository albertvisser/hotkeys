# -*- coding: UTF-8 -*-

from __future__ import print_function
import sys
import os
import string
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import tcmdrkys
## import datetime

HERE = os.path.abspath(os.path.dirname(__file__))
TTL = "A hotkey editor"
VRS = "1.1.x"
AUTH = "(C) 2008 Albert Visser"
INI = "tckey_config.py"
WIN = True if sys.platform == "win32" else False
LIN = True if sys.platform == 'linux2' else False

# voorziening voor starten op usb-stick onder Windows (drive letters in config aanpassen)
if WIN and __file__ != "tckey_gui.py":
    drive = os.path.splitdrive(os.getcwd())[0] + "\\"
    with open(INI) as f_in:
        lines = f_in.readlines()
    for line in lines:
        if line.startswith('TC_PAD='):
            olddrive = line[7:10]
            break
    if olddrive.upper() != drive.upper():
        bak = INI + ".bak"
        if os.path.exists(bak):
            os.remove(bak)
        os.rename(INI,bak)
        with open(INI,"w") as f_out:
            for line in lines:
                if olddrive.lower() in line:
                    f_out.write(line.replace(olddrive.lower(),drive.upper()))
                elif olddrive.upper() in line:
                    f_out.write(line.replace(olddrive.upper(),drive.upper()))
                else:
                    f_out.write(line)

#--- dit zit ook in hotkeys.py
# constanten voor  captions en dergelijke 9correspondeert met nummers in language files)
C_KEY, C_MOD, C_SRT, C_CMD, C_OMS = '001', '043', '002', '003', '004'
C_DFLT, C_RDEF = '005', '006'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
C_SAVE, C_DEL, C_EXIT, C_KTXT, C_CTXT ='010', '011', '012', '018', '019'
M_APP, M_READ, M_SAVE, M_USER, M_EXIT = '200', '201', '202', '203', '209'
M_SETT, M_LOC, M_LANG, M_HELP, M_ABOUT = '210', '211', '212', '290', '299'
C_MENU = (
    (M_APP,(M_READ, M_SAVE, M_USER, -1 , M_EXIT)),
    (M_SETT,(M_LOC,M_LANG)),
    (M_HELP,(M_ABOUT,))
    )
NOT_IMPLEMENTED = '404'
#----

#--- deze functies zitten ook in hotkeys_qt.py
def show_message(self, message_id, caption_id='000'): #TODO
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    ok = gui.QMessageBox.question(self, self.captions[caption_id],
        self.captions[message_id], gui.QMessageBox.Yes |
        gui.QMessageBox.No | gui.QMessageBox.Cancel)
    return ok # ahum deze staat zo geen ok of cancel toe

def m_read(self):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    doit = True
    if not self.page.modified:
        doit = False
        h = show_message(self, '041')
        if h == gui.QMessageBox.Yes:
            doit = True
    if doit:
        self.page.readkeys()
        self.page.populate_list()

def m_save(self):
    """(menu) callback voor het terugschrijven van de hotkeys

    vraagt eerst of het ok is om de hotkeys weg te schrijven
    vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
    """
    if not self.page.modified:
        h = show_message(self, '041')
        if h != gui.QMessageBox.Yes:
            return
    self.page.savekeys()
    if self.page.ini.restart:
        h = show_message(self, '026')
        if h == gui.QMessageBox.Yes:
            os.system(self.page.ini.restart)
    else:
        gui.QMessageBox.information(self, self.captions['000'], self.captions['037'])

def m_user(self):
    """(menu) callback voor een nog niet geïmplementeerde actie"""
    return self.captions[NOT_IMPLEMENTED]

def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.exit()

def m_loc(self):
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    if self.page.modified:
        h = show_message(self, '025')
        if h == gui.QMessageBox.Yes:
            self.page.savekeys()
        elif h == gui.QMessageBox.Cancel:
            return
    paths = self.page.ini.paden
    if self.page.ini.restart:
        paths.append(self.page.ini.restart)
    else:
        paths.append('')
    captions = [self.captions[x] for x in (
        '028','029','030','031','032','033','039','038','040'
        )]
    ok = FilesDialog(self, self.captions["000"], paths, captions).exec_()
    if ok == gui.QDialog.Accepted:
        paden, restarter = self.paden[:-1], self.paden[-1]
        self.page.ini.set("paden", paden)

def m_lang(self):
    """(menu) callback voor taalkeuze

    past de settings aan en leest het geselecteerde language file
    """
    choices = [x for x in os.listdir(HERE) if os.path.splitext(x)[1] == ".lng"]
    indx = choices.index(self.page.ini.lang) if self.page.ini.lang in choices else 0
    lang, ok = gui.QInputDialog.getItem(self, self.captions["027"],
        self.captions["000"], choices, current=indx, editable=False)
    if ok:
        self.page.ini.set('lang', str(lang))
        self.page.readcaptions()
        self.page.setcaptions()

def m_about(self):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    info = gui.QMessageBox.about(self,  self.captions['000'],
        "\n\n".join((TTL, 'version ' + VRS, AUTH)))

# dispatch table for  menu callbacks
MENU_FUNC = {
    M_READ: m_read,
    M_SAVE: m_save,
    M_USER: m_user,
    M_EXIT: m_exit,
    M_LOC: m_loc,
    M_LANG: m_lang,
    M_ABOUT: m_about,
}
#----

class TCPanel(gui.QWidget):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    definieert feitelijk een "custom widget"
    """
    def __init__(self, parent, args=None, can_exit=False): # , top):

        self.parent = parent
        self._goback = False
        self._initializing = True
        self.can_exit = can_exit
        self.captions = {}
        self.data = []
        self.ini = tcmdrkys.TckSettings(INI)
        if self.ini.paden[0] == '':
            self.ini.lang = 'english.lng'
        self.readcaptions()
        self.modified = False
        self._origdata = ["", False, False, False, False, ""]
        self._newdata = self._origdata[:]
        self.mag_weg = True
        if args:
            self.fpad = args[0]
            ext = os.path.splitext(self.fpad)[1]
            if ext == "" and not os.path.isdir(self.fpad):
                self.fpad += ".xml"
            elif ext != ".xml":
                self.fpad = ""
        else:
            self.fpad  = ""
        self.dirname,self.filename = os.path.split(self.fpad)
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        self.readkeys()

        gui.QWidget.__init__(self, parent)
        ## self.top = top

        titles, widths = [], []
        for key, width in ((C_KEY, 70),
                (C_MOD, 90),
                (C_SRT, 80),
                (C_CMD, 160),
                (C_OMS, 452)):
            titles.append(self.captions[key])
            widths.append(width)
        self.p0list = gui.QTreeWidget(self)
        self.p0list.setSortingEnabled(True)
        self.p0list.setHeaderLabels(titles)
        self.p0list.setAlternatingRowColors(True)
        self.p0list.currentItemChanged.connect(self.on_item_selected) # 2 params
        self.p0hdr = self.p0list.header()
        self.p0hdr.setClickable(True)
        for indx, wid in enumerate(widths):
            self.p0hdr.resizeSection(indx, wid)
        self.p0hdr.setStretchLastSection(True)

        box = gui.QFrame(self)
        box.setFrameShape(gui.QFrame.StyledPanel)
        box.setMaximumHeight(90)
        self.txt_key = gui.QLabel(self.captions[C_KTXT] + " ", box)
        self.keylist = [x for x in string.ascii_uppercase] + \
            [x for x in string.digits] + [x for x in string.punctuation] + \
            ["F" + str(i) for i in range(1,13)] + \
            [self.captions[str(x)] for x in range(100,121)]
        for item in self.data.values():
            if item[0] not in self.keylist:
                print(item)
        cb = gui.QComboBox(box)
        cb.addItems(self.keylist)
        cb.currentIndexChanged[str].connect(functools.partial(self.on_combobox, cb))
        self.cmb_key = cb

        for x in (M_CTRL, M_ALT, M_SHFT, M_WIN):
            cb = gui.QCheckBox(self.captions[x].join(("+","  ")), box) #, (65, 60), (150, 20), gui.QNO_BORDER)
            cb.setChecked(False)
            cb.stateChanged.connect(functools.partial(self.on_checkbox, cb))
            if x == M_CTRL:
                self.cb_ctrl = cb
            elif x == M_ALT:
                self.cb_alt = cb
            elif x == M_SHFT:
                self.cb_shift = cb
            elif x == M_WIN:
                self.cb_win = cb

        self.txt_cmd = gui.QLabel(self.captions[C_CTXT] + " ", box)
        self.commandlist = [x for x in self.omsdict.keys()]
        self.commandlist.sort()
        cb = gui.QComboBox(self)
        cb.addItems(self.commandlist)
        cb.currentIndexChanged[str].connect(functools.partial(self.on_combobox, cb))
        self.cmb_commando = cb

        self.b_save = gui.QPushButton(self.captions[C_SAVE], box) ##, (120, 45))
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(self.on_update)
        self.b_del = gui.QPushButton(self.captions[C_DEL], box) #, size= (50,-1)) ##, (120, 45))
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(self.on_delete)

        self.txt_oms = gui.QTextEdit(box)
        self.txt_oms.setMaximumHeight(40)
        self.txt_oms.setReadOnly(True)

        self.populate_list()

        if can_exit:
            self.b_exit = gui.QPushButton(self.captions[C_EXIT], self)
            self.b_exit.clicked.connect(self.parent.exit)

    # --- schermen opbouwen: layout -----------------------------------------------------------------------------------------
        sizer0 = gui.QVBoxLayout()
        sizer1 = gui.QHBoxLayout()
        sizer1.addWidget(self.p0list)
        sizer0.addLayout(sizer1)

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
        box.setLayout(bsizer)
        sizer0.addWidget(box)

        if can_exit:
            sizer2 = gui.QHBoxLayout()
            sizer2.addStretch()
            sizer2.addWidget(self.b_exit)
            sizer2.addStretch()
            sizer0.addLayout(sizer2)
        self.setLayout(sizer0)
        self._initializing = False

    def readkeys(self):
        self.cmdict, self.omsdict, self.defkeys, self.data = tcmdrkys.readkeys(
            self.ini.paden)

    def savekeys(self):
        tcmdrkys.savekeys(self.ini.tcpad, self.data)
        self.modified = False
        self.setWindowTitle(self.captions["000"])

    def readcaptions(self):
        with open(os.path.join(HERE, self.ini.lang)) as _in:
            for x in _in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key,value = x.strip().split(None,1)
                self.captions[key] = value

    def setcaptions(self):
        if self.can_exit:
            self.parent.setcaptions()
        self.cb_win.setText(self.captions[M_WIN].join(("+", "  ")))
        self.cb_ctrl.setText(self.captions[M_CTRL].join(("+", "  ")))
        self.cb_alt.setText(self.captions[M_ALT].join(("+", "  ")))
        self.cb_shift.setText(self.captions[M_SHFT].join(("+", "  ")))
        self.b_save.setText(self.captions[C_SAVE])
        self.b_del.setText(self.captions[C_DEL])
        self.b_exit.setText(self.captions[C_EXIT])
        self.txt_key.setText(self.captions[C_KTXT])
        self.txt_cmd.setText(self.captions[C_CTXT])
        self.populate_list()

    def vuldetails(self, selitem):  # let op: aangepast (gebruik zip)
        print('vuldetails called')
        if not selitem: # bv. bij p0list.clear()
            return
        seli = selitem.data(0, core.Qt.UserRole)
        if sys.version < '3':
            seli = seli.toPyObject()
        key, mods, soort, cmd, oms = self.data[seli]
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

    def aanpassen(self, delete=False): # TODO
        print('aanpassen called')
        item = self.p0list.currentItem()
        pos = self.p0list.indexOfTopLevelItem(item)
        if delete:
            indx = item.data(0, core.Qt.UserRole)
            if sys.version < '3':
                indx = int(indx.toPyObject())
            if self.data[indx][1] == "S": # can't delete standard key
                gui.QMessageBox.information(self, self.captions["000"],
                    self.captions['024'])
                return
            else:
                if self.data[indx][0] in self.defkeys: # restore standard if any
                    cmd = self.defkeys[self.data[indx][0]]
                    if cmd in self.omsdict:
                        oms = self.omsdict[cmd]
                    else:
                        oms = cmd
                        cmd = ""
                    self.data[indx] = (key, 'S', cmd, oms)
                else:
                    del self.data[indx]
                    ## pos -= 1
            self.b_save.setEnabled(False)
            self.b_del.setEnabled(False)
            self.modified = True
            self.parent.setWindowTitle(' '.join((self.captions["000"],
                self.captions['017'])))
            print('item deleted, pos is', pos)
            self.populate_list(pos)    # refresh
        else:
            self.on_item_selected(item, item) # , from_update=True)

    def populate_list(self, pos=0):
        """vullen van de list control
        """
        self.p0list.clear()
        items = self.data.items()
        if items is None or len(items) == 0:
            return

        for key, data in items:
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, data[0])
            new_item.setData(0, core.Qt.UserRole, key) # data[0])
            new_item.setText(1, data[1])
            soort = C_DFLT if data[2] == "S" else C_RDEF
            new_item.setText(2, self.captions[soort])
            new_item.setText(3, data[3])
            new_item.setText(4, data[4])
            self.p0list.addTopLevelItem(new_item)
        item = self.p0list.topLevelItem(pos)
        self.p0list.setCurrentItem(self.p0list.topLevelItem(pos))

    def on_item_selected(self, newitem, olditem): # , from_update=False):
        """callback op het selecteren van een item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        if not newitem: # bv. bij p0list.clear()
            return
        if self._initializing:
            self.vuldetails(newitem)
            return
        print('itemselected called', newitem.text(0))
        if olditem is not None:
            print('old item was', olditem.text(0))
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
        for number, item in self.data.items():
            if key == item[0] == key and item[1] == mods:
                gevonden = True
                indx = number
                break
        print(cursor_moved, other_item, other_cmd, gevonden)
        doit = False
        if any_change:
            if cursor_moved:
                h = gui.QMessageBox.question(self,
                    self.captions["000"], self.captions["020"],
                    gui.QMessageBox.Yes | gui.QMessageBox.No)
                doit = True if h == gui.QMessageBox.Yes else False
            elif other_item:
                if gevonden:
                    ok = gui.QMessageBox.question(self,
                        self.captions["000"], self.captions["045"],
                        gui.QMessageBox.Yes | gui.QMessageBox.No)
                    doit = True if ok == gui.QMessageBox.Yes else False
                else:
                    doit = True
            else:
                doit = True
        if doit:
            item = self.p0list.currentItem()
            pos = self.p0list.indexOfTopLevelItem(item)
            if gevonden:
                self.data[indx] = (key, mods, 'U', cmd, self.omsdict[cmd])
            else:
                newdata = self.data.values()
                newvalue = (key, mods, 'U', cmd, self.omsdict[cmd])
                newdata.append(newvalue)
                newdata.sort()
                for x, y in enumerate(newdata):
                    if y == newvalue:
                        indx = x
                    self.data[x] = y
            self.modified = True
            self._origdata = [key, False, False, False, False, cmd]
            for mod, indx in zip(('WCAS'),(4, 2, 3, 1)):
                self._origdata[indx] = mod in mods
            self.populate_list(pos)    # refresh
            newitem = self.p0list.topLevelItem(pos)
        self.vuldetails(newitem)

    def keyprint(self, evt):
        pass

    def on_combobox(self, cb, text):
        """callback op het gebruik van een combobox

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        text = str(text)
        print('on combobox:', text)
        print(self._origdata)
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
        print(self._origdata)
        print(self._newdata)

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
        print('on checkbox:', indx, state)
        print(self._origdata)
        print(self._newdata)

    def on_update(self):
        self.aanpassen()
        self.p0list.setFocus()

    def on_delete(self):
        self.aanpassen(delete=True)
        self.p0list.setFocus()


class FileBrowseButton(gui.QWidget):
    def __init__(self, parent, getdirectory=False):
        self.startdir = self.caption = ''
        self.getdir = getdirectory
        gui.QWidget.__init__(self, parent)
        vbox = gui.QVBoxLayout()
        box = gui.QHBoxLayout()
        self.label = gui.QLabel('Enter a {}:'.format('directory' if self.getdir
            else 'file'), self)
        box.addWidget(self.label)
        box.addStretch()
        self.input = gui.QLineEdit(self)
        self.input.setMinimumWidth(200)
        box.addWidget(self.input)
        self.button = gui.QPushButton('Select', self, clicked=self.browse)
        box.addWidget(self.button)
        vbox.addLayout(box)
        self.setLayout(vbox)

    def browse(self):
        caption = self.caption or 'Browse {}'.format('directories' if self.getdir
            else 'files')
        startdir = str(self.input.text()) or os.getcwd()
        if self.getdir:
            path = gui.QFileDialog.getExistingDirectory(self, caption, startdir)
        else:
            path = gui.QFileDialog.getOpenFileName(self, caption, startdir)
        if path:
            self.input.setText(path)

class FilesDialog(gui.QDialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, parent, title, locations, captions):
        self.parent = parent
        self.locations = locations
        self.captions = captions
        gui.QDialog.__init__(self, parent)
        self.resize=(350, 200)

        sizer = gui.QVBoxLayout()

        text = captions.pop(0)
        label = gui.QLabel(text, self)
        sizer.addWidget(label)

        buttons = []
        rstrcap2 = captions.pop()
        rstrcap = captions.pop()
        dircap = captions.pop()

        rstrloc = locations.pop()
        for i, x in enumerate(captions):
            if i < len(locations):
                dir = locations[i]
                strt = dir
            else:
                dir = locations[0]
                strt = ""

            fbb = FileBrowseButton(self, getdirectory=True)
            fbb.label.setText(x)
            fbb.caption = dircap % x
            fbb.input.setText(strt)
            sizer.addWidget(fbb)
            buttons.append(fbb)
        self.bTC,self.bUC,self.bCI,self.bKT,self.bHK = buttons

        if rstrloc:
            dir, naam = os.path.split(rstrloc)
        else:
            dir, naam = locations[0],''
        self.bRST = FileBrowseButton(self)
        self.bRST.label.setText(rstrcap)
        self.bRST.input.setText(naam)
        self.bRST.caption = rstrcap2
        sizer.addWidget(self.bRST)

        button_box = gui.QDialogButtonBox(gui.QDialogButtonBox.Ok |
            gui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        sizer.addWidget(button_box)
        self.setLayout(sizer)

    def accept(self):
        paden = [
            str(self.bTC.input.text()),
            str(self.bUC.input.text()),
            str(self.bCI.input.text()),
            str(self.bKT.input.text()),
            str(self.bHK.input.text()),
            str(self.bRST.input.text())
            ]
        fout = ''
        for i, pad in enumerate(paden):
            if pad != "":
                if i == 5:
                    if not os.path.exists(pad):
                        fout = self.parent.captions['036'] % naam
                else:
                    naam = self.captions[i]
                    if naam == 'Hotkeys.hky':
                        naam = 'tc default hotkeys.ohky'
                    if not os.path.exists(os.path.join(pad,naam)):
                        fout = self.parent.captions['035'] % naam
        if fout:
            gui.MessageBox.information(self, self.parent.captions["000"], fout)
            return
        self.parent.paden = paden
        return gui.QDialog.Accepted

class MainWindow(gui.QMainWindow):
    """Hoofdscherm van de applicatie"""
    def __init__(self, args):

        wid = 860 if LIN else 688
        gui.QMainWindow.__init__(self)
        self.setWindowTitle("tcmdrkeys")
        self.resize(wid, 594)
        self.sb = self.statusBar()

    # --- schermen opbouwen: controls plaatsen -----------------------------------------------------------------------------------------
        #~ self.SetIcon(gui.QIcon("task.ico",gui.QBITMAP_TYPE_ICO))
        ## self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))

        self.page = TCPanel(self, args, can_exit=True)
        self.setCentralWidget(self.page)
        self.captions = self.page.captions
        self.setWindowTitle(self.captions["000"])

        self.menu_bar = self.menuBar()
        self.menuitems = []
        for title, items in C_MENU:
            menu = self.menu_bar.addMenu(self.captions[title])
            self.menuitems.append(menu)
            for sel in items:
                if sel == -1:
                    menu.addSeparator()
                else:
                    act = gui.QAction(self.captions[sel], self)
                    act.triggered.connect(functools.partial(self.on_menu, sel))
                    menu.addAction(act)

        self.show()
        if len(self.page.data) == 0:
            dlg = gui.QMessageBox.information(self, self.captions["000"],
                self.captions['042'])

    def on_menu(self, id_):
        text = MENU_FUNC[id_](self)
        if text:
            dlg = gui.QMessageBox.information(self, self.captions["000"], text)

    def setcaptions(self):
        ## self.captions = self.page.captions
        title = self.captions["000"]
        if self.page.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)
        for indx, menu in enumerate(self.menuitems):
            menu.setTitle(self.captions[C_MENU[indx][0]])
            for indx2, action in enumerate(menu.actions()):
                hulp = C_MENU[indx][1][indx2]
                if hulp != -1:
                    action.setText(self.captions[hulp])

    def exit(self,e=None):
        if self.page.modified:
            ok = gui.QMessageBox.question(self, self.captions["000"],
                self.captions['025'], gui.QMessageBox.Yes | gui.QMessageBox.No |
                gui.QMessageBox.Cancel)
            if ok == gui.QMessageBox.Yes:
                self.page.savekeys()
            elif ok == gui.QMessageBox.Cancel:
                return
        self.close()

    def afdrukken(self): # TODO (niet geactiveerd?)
        self.css = ""
        if self.css != "":
            self.css = "".join(("<style>",self.css,"</style>"))
        self.text.insert(0,"".join(("<html><head><title>titel</title>",self.css,"</head><body>")))
        self.text.append("</body></html>")
        self.printer.Print("".join(self.text),self.hdr)
        return

def main(args=None):
    app = gui.QApplication(sys.argv)
    frame = MainWindow(args)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv[1:])
