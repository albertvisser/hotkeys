# -*- coding: UTF-8 -*-
"""hotkeys.py

    main gui (choicebook)
    importeert de verschillende applicatiemodules
    hierin wordt het menu gedefinieerd en de functies die daarbij horen
    het idee is dat de menuopties wanneer nodig uitgegrijsd zijn en dat
        in de routines wordt uitgevraagd wat te doen bij welke applicatie
    voor wat betreft de instellingen:
        taalkeuze: op dit niveau
        paden: op applicatie niveau
"""
from __future__ import print_function
import os
import sys
import csv
import shutil
import functools
import importlib
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

HERE = os.path.abspath(os.path.dirname(__file__))
## try:
    ## HOME = os.environ('HOME')
## except KeyError:
    ## HOME = os.environ('USERPROFILE') # Windows
CONF = os.path.join(HERE, 'hotkey_config.py') # don't import, can be modified in runtime
TTL = "A hotkey viewer/editor"
VRS = "1.1.x"
AUTH = "(C) 2008-2014 Albert Visser"
XTRA = '''\
originally built for Total Commander,
extended for use with
all your favourite applications'''
WIN = True if sys.platform == "win32" else False
## LIN = True if sys.platform == 'linux2' else False
LIN = True if os.name == 'posix' else False

# constanten voor  captions en dergelijke (correspondeert met nummers in language files)
# *** toegesneden op TC verplaatsen naar TC plugin? ***
C_KEY, C_MOD, C_SRT, C_CMD, C_OMS = '001', '043', '002', '003', '004'
C_DFLT, C_RDEF = '005', '006'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
C_SAVE, C_DEL, C_EXIT, C_KTXT, C_CTXT ='010', '011', '012', '018', '019'
M_APP, M_READ, M_SAVE, M_RBLD, M_EXIT = '200', '201', '202', '203', '209'
M_SETT, M_LOC, M_LANG, M_HELP, M_ABOUT = '210', '211', '212', '290', '299'
NOT_IMPLEMENTED = '404'

# default menu structure
DFLT_MENU = (
    (M_APP, (M_READ, M_RBLD, M_SAVE, -1, M_EXIT,)),
    (M_SETT, (M_LOC, M_LANG,)),
    (M_HELP, (M_ABOUT,))
    )

# shared (menu) functions
def show_message(self, message_id, caption_id='000'):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    ok = gui.QMessageBox.question(self, self.captions[caption_id],
        self.captions[message_id], gui.QMessageBox.Yes |
        gui.QMessageBox.No | gui.QMessageBox.Cancel)
    return ok

def m_read(self):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    # TODO: zorgen dat het lezen (alleen) voor het huidige getoonde tool  gebeurt
    # 1. bepaal welk tool geselecteerd is
    # 2. bepaal welke csv hier bij hoort
    # 3. herlees de keydefs m.b.v. readcsv() - settings worden niet herlezen of herschreven
    # alternatie: bepaal welk panel voorstaat en roep diens readkeys methode aan
    # -- oh dat is wat hier gebeurt (facepalm)
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
    # TODO: zorgen dat het lezen (alleen) voor het huidige getoonde tool  gebeurt
    #             en dat menu optie alleen beschikbaar is voor waar terugschrijven mogelijk is
    if not self.page.modified:
        h = show_message(self, '041')
        if h != gui.QMessageBox.Yes:
            return
    self.page.savekeys()
    ## if self.page.ini.restart:
        ## h = show_message(self, '026')
        ## if h == gui.QMessageBox.Yes:
            ## os.system(self.page.ini.restart)
    ## else:
    gui.QMessageBox.information(self, self.captions['000'], self.captions['037'])

def m_loc(self):
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    # TODO: deze routine wijzigen zodat je hier de gebruikte plugins kunt definiëren met hun csv's
    # self.ini["plugins"] bevat de lijst met tools en csv locaties
    ok = FilesDialog(self).exec_()
    ## if ok == gui.QDialog.Accepted:
        ## paden, restarter = self.paden[:-1], self.paden[-1]
        ## self.page.ini.set("paden", paden)

def m_user(self):
    """(menu) callback voor een nog niet geïmplementeerde actie"""
    return self.captions[NOT_IMPLEMENTED]

def m_rebuild(self):
    print('rebuild option chosen')

def m_lang(self):
    """(menu) callback voor taalkeuze

    past de settings aan en leest het geselecteerde language file
    """
    # bepaal welke language files er beschikbaar zijn
    choices = [x for x in os.listdir(HERE) if os.path.splitext(x)[1] == ".lng"]
    # bepaal welke er momenteel geactiveerd is
    oldlang = self.ini['lang']
    indx = choices.index(oldlang) if oldlang in choices else 0
    lang, ok = gui.QInputDialog.getItem(self, self.captions["027"],
        self.captions["000"], choices, current=indx, editable=False)
    if ok:
        inifile = self.ini['filename']
        shutil.copyfile(inifile, inifile + '.bak')
        with open(inifile + '.bak') as _in, open(inifile, 'w') as _out:
            for line in _in:
                if line.startswith('LANG'):
                    line = line.replace(oldlang, lang)
                _out.write(line)
        self.ini['lang'] = lang
        self.readcaptions(lang)
        self.setcaptions()

def m_about(self):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    info = gui.QMessageBox.about(self,  self.captions['000'],
        self.captions['057'].format(TTL, VRS, AUTH, XTRA))

def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.exit()

# dispatch table for  menu callbacks
DFLT_MENU_FUNC = {
    M_READ: m_read,
    M_SAVE: m_save,
    M_RBLD: m_rebuild,
    M_LOC: m_loc,
    M_LANG: m_lang,
    M_EXIT: m_exit,
    M_ABOUT: m_about,
}

MENUS = {}
# list containing the plugins themselves
# -- moved to top-level config file - to be adapted by menu callback (m_loc)

def readcsv(pad):
    """lees het csv bestand op het aangegeven pad en geeft de inhoud terug

    retourneert dictionary van nummers met (voorlopig) 4-tuples
    """
    data = {}
    with open(pad, 'r') as _in:
        rdr = csv.reader(_in)
        key = 0
        coldata = []
        settings = {}
        for row in rdr:
            rowtype, rowdata = row[0], row[1:]
            if rowtype == 'Setting':
                name, value, oms = rowdata
                settings[name] = (value, oms)
            elif rowtype == 'Title':
                for item in rowdata:
                    coldata_item = ['', '', '', '', '']
                    coldata_item[1] = item
                    coldata.append(coldata_item)
            elif rowtype == 'Width':
                for ix, item in enumerate(rowdata):
                    coldata[ix][2] = int(item)
            elif rowtype == 'Seq':
                for ix, item in enumerate(rowdata):
                    coldata[ix][0] = int(item)
                    coldata[ix][3] = ix
            elif rowtype == 'is_type':
                for ix, item in enumerate(rowdata):
                    coldata[ix][4] = bool(int(item))
                coldata.sort()
                coldata = [x[1:] for x in coldata]
            elif rowtype == 'Keydef':
                key += 1
                data[key] = ([x.strip() for x in rowdata])
    return settings, coldata, data

class FileBrowseButton(gui.QWidget):
    def __init__(self, parent, text=""):
        self.startdir = ''
        if text:
            self.startdir = os.path.dirname(text)
        gui.QWidget.__init__(self, parent)
        vbox = gui.QVBoxLayout()
        box = gui.QHBoxLayout()
        self.input = gui.QLineEdit(text, self)
        self.input.setMinimumWidth(200)
        box.addWidget(self.input)
        self.button = gui.QPushButton(self.parent().parent.captions['058'], self,
            clicked=self.browse)
        box.addWidget(self.button)
        vbox.addLayout(box)
        self.setLayout(vbox)

    def browse(self):
        startdir = str(self.input.text()) or os.getcwd()
        path = gui.QFileDialog.getOpenFileName(self,
            self.parent.parent().captions['059'], startdir)
        if path:
            self.input.setText(path)

class FilesDialog(gui.QDialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, parent): #, title, locations, captions):
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        self.resize(680, 400)

        self.sizer = gui.QVBoxLayout()
        self.sizer.addStretch()
        text = '\n'.join((self.parent.captions['069'], self.parent.captions['070']))
        hsizer = gui.QHBoxLayout()
        label = gui.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        self.gsizer = gui.QGridLayout()
        rownum = colnum = 0
        self.gsizer.addWidget(gui.QLabel(self.parent.captions['060'], self),
            rownum, colnum, alignment = core.Qt.AlignHCenter | core.Qt.AlignVCenter)
        colnum += 1
        self.gsizer.addWidget(gui.QLabel(self.parent.captions['061'], self),
            rownum, colnum, alignment = core.Qt.AlignVCenter)

        self.rownum = rownum
        self.checks = []
        self.paths = []
        for name, path in self.parent.ini["plugins"]:
            self.add_row(name, path)
        self.sizer.addLayout(self.gsizer)

        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton(self.parent.captions['062'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_program)
        btn = buttonbox.addButton(self.parent.captions['063'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.remove_program)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.sizer.addStretch()
        self.setLayout(self.sizer)

    def add_row(self, name, path):
        self.rownum += 1
        colnum = 0
        check = gui.QCheckBox(name, self)
        self.gsizer.addWidget(check, self.rownum, colnum)
        self.checks.append(check)
        colnum += 1
        browse = FileBrowseButton(self, text=path)
        self.gsizer.addWidget(browse, self.rownum, colnum)
        self.paths.append((name, browse))

    def delete_row(self, rownum):
        print(rownum)

    def add_program(self):
        """nieuwe rij aanmaken in self.gsizer"""
        newtool, ok = gui.QInputDialog.getText(self, self.parent.title,
            self.parent.captions['064'])
        if ok:
            self.add_row(newtool, '')
            self.update()

    def remove_program(self):
        """alle aangevinkt items verwijderen uit self.gsizer"""
        test = [x.isChecked() for x in self.checks]
        checked = [x for x, y in enumerate(test) if y]
        print(test, checked)
        if any(test):
            ok = gui.QMessageBox.question(self, self.parent.title,
                self.parent.captions['065'],
                gui.QMessageBox.Yes | gui.QMessageBox.No)
            if gui.QMessageBox.Yes:
                for row in reversed(checked):
                    self.delete_row(row)

    def accept(self):
        self.parent.ini["plugins"] = [(name, path) for name, path in self.paths]
        return gui.QDialog.Accepted

class DummyPanel(gui.QFrame):

    def __init__(self):
        gui.QFrame.__init__(self)
        self.initializing = False

    def add_extra_attributes(self):
        pass

    def add_extra_fields(self):
        pass

    def layout_extra_fields(self, sizer):
        pass

    def captions_extra_fields(self):
        pass

    def vuldetails(self, value):
        pass

class HotkeyPanel(gui.QFrame):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    definieert feitelijk een "custom widget"
    coldata is een list of tuple van 4-tuples die achtereenvolgens aangeven
    de kolomtitel, de breedte, de index op self.data en of het een soort aangeeft
    verwacht dat de subclass van te voren een attribuut gedefinieerd heeft:
    _keys: de module om de settings te lezen
    """
    def __init__(self, parent, pad):

        self.pad = pad
        # switch om het gedrag van bepaalde routines tijdens initialisatie te beïnvloeden
        self._initializing = True

        gui.QFrame.__init__(self, parent)
        self.parent = parent # .parent()
        self.captions = self.parent.parent.captions
        self.settings, self.column_info, self.data = readcsv(self.pad)
        self.p0list = gui.QTreeWidget(self)
        modulename = "editor." + self.settings["PluginName"][0]
        self._keys = importlib.import_module(modulename)
        try:
            self._panel = self._keys.MyPanel()
        except AttributeError:
            self._panel = DummyPanel()
        self.title = self.settings["PanelName"][0]
        self._panel.settings = self.settings
        self._panel.captions = self.captions
        self._panel.data = self.data
        ## self.readkeys()
        self.modified = False

        # gelegenheid voor extra initialisaties en het opbouwen van de rest van de GUI
        # het vullen van veldwaarden hierin gebeurt als gevolg van het vullen
        # van de eerste rij in de listbox, daarom moet deze het laatst
        self.add_extra_attributes()
        self.add_extra_fields()

        self._sizer = gui.QVBoxLayout()
        if self.column_info:
            self.p0list.setSortingEnabled(True)
            self.p0list.setHeaderLabels([self.captions[col[0]] for col in
                self.column_info])
            self.p0list.setAlternatingRowColors(True)
            self.p0list.currentItemChanged.connect(self.on_item_selected)
            self.p0hdr = self.p0list.header()
            self.p0hdr.setClickable(True)
            for indx, col in enumerate(self.column_info):
                self.p0hdr.resizeSection(indx, col[1])
            self.p0hdr.setStretchLastSection(True)
            self.populate_list()
            sizer1 = gui.QHBoxLayout()
            sizer1.addWidget(self.p0list)
            self._sizer.addLayout(sizer1)

        # indien van toepassing (TC versie): toevoegen van de rest van de GUI aan de layout
        self.layout_extra_fields(self._sizer)

        self.setLayout(self._sizer)
        self._initializing = False
        self.filtertext = ''

    def add_extra_attributes(self):
        self._panel.add_extra_attributes()

    def add_extra_fields(self):
        """define other widgets to be used in the panel
        needed for showing details subpanel
        """
        # te definieren in de module die als self._keys geïmporteerd wordt
        self._panel.add_extra_fields()

    def layout_extra_fields(self, sizer):
        """add extra widgets to self._sizer
        needed for showing details subpanel
        """
        # te definieren in de module die als self._keys geïmporteerd wordt
        self._panel.layout_extra_fields(sizer)

    def captions_extra_fields(self):
        """refresh captions for extra widgets
        needed for showing details subpanel
        """
        # te definieren in de module die als self._keys geïmporteerd wordt
        self._panel.captions_extra_fields()

    def on_item_selected(self, olditem, newitem):
        "callback for list selection, needed for copying details to subpanel"
        try:
            self._panel.on_item_selected(olditem, newitem)
        except AttributeError:
            pass

    def vuldetails(self, selitem):
        try:
            self._panel.vuldetails(self, selitem)
        except AttributeError:
            pass
        # (re)implemented by TC, needed for copying details  to subpanel
        # --> define these in the "keys" file?

    def aanpassen(self, delete=False):
        pass
        # (re)implemented by TC, needed for updating and copying details  from subpanel
        # --> define these in the "keys" file?

    def readkeys(self):
        "(re)read the data for the keydef list"
        print('reading keys')
        self.data = readcsv(self.pad)[2]
        # a real reread like in TC_plugin is more complicated, but this should really be done
        # in a separate unit like TCMerge - or in some way built in here

    def savekeys(self, pad=None):
        "save modified keydef back"
        if not pad:
            pad = self.pad
        self._keys.savekeys(pad, self.data)
        self.modified = False
        self.setWindowTitle(self.captions["000"])

    def setcaptions(self):
        title = self.captions["000"]
        if self.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)

        # in de TC versie worden hier van de overige widgets de captions ingesteld
        self.captions_extra_fields()
        self.populate_list()

    def populate_list(self, pos=0):
        """vullen van de list control
        """
        print('populating list')
        self.p0list.clear()
        items = self.data.items()
        if items is None or len(items) == 0:
            return

        self._panel.initializing = True
        for key, data in items:
            new_item = gui.QTreeWidgetItem()
            new_item.setData(0, core.Qt.UserRole, key) # data[0])
            for indx, col in enumerate(self.column_info):
                from_indx, is_soort = col[2], col[3]
                value = data[from_indx]
                if is_soort:
                    value = C_DFLT if value == 'S' else C_RDEF
                    value = self.captions[value]
                new_item.setText(indx, value)
            self.p0list.addTopLevelItem(new_item)
            self.p0list.setCurrentItem(self.p0list.topLevelItem(pos))
        self._panel.initializing = False

    def exit(self):
        if self.modified:
            ok = show_message(self, '025')
            if ok == gui.QMessageBox.Yes:
                self.page.savekeys()
            elif ok == gui.QMessageBox.Cancel:
                return False
        return True

class ChoiceBook(gui.QFrame): #Widget):
    """ Als QTabwidget, maar met selector in plaats van tabs
    """
    def __init__(self, parent, plugins):
        ## gui.QWidget.__init__(self, parent)
        self.plugins = plugins
        self.parent = parent.parent()
        gui.QFrame.__init__(self, parent)
        self.sel = gui.QComboBox(self)
        self.sel.currentIndexChanged.connect(self.on_page_changed)
        self.find = gui.QComboBox(self)
        self.find.setMinimumContentsLength(20)
        self.find.setEditable(True)
        self.find.editTextChanged.connect(self.on_text_changed)
        self.b_next = gui.QPushButton(self.parent.captions["014"])
        self.b_next.clicked.connect(self.find_next)
        self.b_next.setEnabled(False)
        self.b_prev = gui.QPushButton(self.parent.captions["015"])
        self.b_prev.clicked.connect(self.find_prev)
        self.b_prev.setEnabled(False)
        self.b_filter = gui.QPushButton(self.parent.captions["068"])
        self.b_filter.clicked.connect(self.filter)
        self.b_filter.setEnabled(False)
        self.filter_on = False
        self.pnl = gui.QStackedWidget(self)
        for txt, loc in self.plugins:
            win = HotkeyPanel(self, loc)
            if win is None:
                self.pnl.addWidget(EmptyPanel(self.pnl,
                    self.parent.captions["052"].format(txt)))
            else:
                self.pnl.addWidget(win)
            self.sel.addItem(txt)
        box = gui.QVBoxLayout()
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        hbox.addSpacing(10)
        self.sel_text = gui.QLabel(self.parent.captions["050"], self)
        hbox.addWidget(self.sel_text)
        hbox.addWidget(self.sel)
        hbox.addStretch()
        self.find_text = gui.QLabel(self.parent.captions["051"], self)
        hbox.addWidget(self.find_text)
        hbox.addWidget(self.find)
        hbox.addWidget(self.b_filter)
        hbox.addWidget(self.b_next)
        hbox.addWidget(self.b_prev)
        ## hbox.addStretch()
        hbox.addSpacing(10)
        vbox.addLayout(hbox)
        box.addLayout(vbox)
        hbox = gui.QVBoxLayout()
        hbox.addWidget(self.pnl)
        box.addLayout(hbox)
        self.setLayout(box)

    def setcaptions(self):
        self.b_next.setText(self.parent.captions['014'])
        self.b_prev.setText(self.parent.captions['015'])
        self.sel_text.setText(self.parent.captions['050'])
        self.find_text.setText(self.parent.captions['051'])
        if self.filter_on:
            self.b_filter.setText(self.parent.captions["066"])
        else:
            self.b_filter.setText(self.parent.captions["068"])

    def on_page_changed(self, indx):
        ## print('page has changed to', indx)
        page = self.pnl.currentWidget() ## self.parent().page
        if page is None:
            return
        self.parent.sb.showMessage(self.parent.captions["053"].format(
            self.sel.currentText()))
        if page.modified:
            ok = page.exit()
            if not ok:
                # ook nog de vorige tekst in de combobox selecteren?
                return
        self.pnl.setCurrentIndex(indx)
        ## for x in MENUS.keys():
            ## print(x, PLUGINS[indx])
        ## if PLUGINS[indx] in MENUS:
            ## print(MENUS[PLUGINS[indx]])
        menus, funcs = MENUS.get(self.plugins[indx][0], (None, None))
        ## print(PLUGINS[indx], menus)
        if not menus:
            menus, funcs = DFLT_MENU, DFLT_MENU_FUNC
        self.parent.page = self.pnl.currentWidget()
        self.parent.setup_menu(menus, funcs)
        if self.parent.page.filtertext:
            self.find.setEditText(self.parent.page.filtertext)
            self.b_filter.setText(self.parent.captions["066"])
            self.b_filter.setEnabled(True)
        else:
            self.find.setEditText('')
            self.find.setEnabled(True)
            self.b_next.setEnabled(False)
            self.b_prev.setEnabled(False)
            self.b_filter.setEnabled(False)

    def on_text_changed(self, text):
        page = self.parent.page # self.pnl.currentWidget()
        col = page.p0list.columnCount() - 1
        self.items_found = page.p0list.findItems(text, core.Qt.MatchContains, col)
        self.b_next.setEnabled(False)
        self.b_prev.setEnabled(False)
        self.b_filter.setText('&Filter')
        self.b_filter.setEnabled(False)
        if self.items_found:
            page.p0list.setCurrentItem(self.items_found[0])
            self.founditem = 0
            if len(self.items_found) < len(self.parent.page.data.items()):
                self.b_next.setEnabled(True)
                self.b_filter.setEnabled(True)
            self.parent.sb.showMessage(self.parent.captions["067"].format(
                len(self.items_found)))
        else:
            self.parent.sb.showMessage(self.parent.captions["054"].format(
                text))

    def find_next(self):
        self.b_prev.setEnabled(True)
        if self.founditem < len(self.items_found) -1:
            self.founditem += 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])
        else:
            self.parent.sb.showMessage(self.parent.captions["055"])
            self.b_next.setEnabled(False)

    def find_prev(self):
        self.b_next.setEnabled(True)
        if self.founditem == 0:
            self.parent.sb.showMessage(self.parent.captions["056"])
            self.b_prev.setEnabled(False)
        else:
            self.founditem -= 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])

    def filter(self):
        if not self.items_found:
            return
        state = str(self.b_filter.text())
        text = str(self.find.currentText())
        if state == self.parent.captions['068']: # self.filter_on == False
            state = self.parent.captions['066']
            self.filter_on = True
            self.parent.page.filtertext = text
            self.parent.page.olddata = self.parent.page.data
            self.parent.page.olditems = self.items_found
            self.parent.page.data = {ix: item for ix, item in enumerate(
                self.parent.page.data.values()) if text.upper() in item[-1].upper()}
            self.b_next.setEnabled(False)
            self.b_prev.setEnabled(False)
            self.find.setEnabled(False)
        else:       # self.filter_on == False
            state = self.parent.captions['068']
            self.filter_on = False
            self.parent.page.filtertext = ''
            self.parent.page.data = self.parent.page.olddata
            self.b_next.setEnabled(True)
            self.b_prev.setEnabled(True)
            self.find.setEnabled(True)
        self.parent.page.populate_list()
        self.b_filter.setText(state)
        if self.parent.page.data == self.parent.page.olddata:
            self.items_found = self.parent.page.olditems

class MainFrame(gui.QMainWindow):
    """Hoofdscherm van de applicatie
    """
    def __init__(self, args):

        wid = 860 if LIN else 688
        hig = 594
        gui.QMainWindow.__init__(self)
        self.title = 'Hotkeys'
        self.setWindowTitle(self.title)
        self.resize(wid, hig)
        self.sb = self.statusBar()

        self.menu_bar = self.menuBar()
        self.ini = {'filename': CONF, 'plugins': []}
        with open(self.ini['filename']) as _in:
            read_plugins = False
            for line in _in:
                if read_plugins:
                    if line.strip() == ']':
                        read_plugins = False
                    elif line.strip().startswith('#'):
                        continue
                    else:
                        name, value = line.split(', ',1)
                        _, name = name.split('(')
                        value, _ = value.split(')')
                        self.ini['plugins'].append((name.strip('"'),
                            value.strip('"')))
                if line.startswith('PLUGINS'):
                    read_plugins = True
                elif line.startswith('LANG'):
                    self.ini['lang'] = line.strip().split('=')[1]
        if 'lang' not in self.ini:
            self.ini['lang'] = 'english.lng'
        self.readcaptions(self.ini['lang']) # set up defaults
        self.sb.showMessage('Welcome to {}!'.format(self.captions["000"]))
        pnl = gui.QWidget(self)
        self.book = ChoiceBook(pnl, self.ini['plugins']) # , size= (600, 700))
        sizer_v = gui.QVBoxLayout()
        sizer_h = gui.QHBoxLayout()
        sizer_h.addWidget(self.book)
        sizer_v.addLayout(sizer_h)
        self.b_exit = gui.QPushButton(self.captions[C_EXIT], pnl)
        self.b_exit.clicked.connect(self.exit)
        sizer_h = gui.QHBoxLayout()
        sizer_h.addStretch()
        sizer_h.addWidget(self.b_exit)
        sizer_h.addStretch()
        sizer_v.addLayout(sizer_h)
        pnl.setLayout(sizer_v)

        self.setCentralWidget(pnl)
        self.page = self.book.pnl.currentWidget()
        self.book.on_page_changed(0)
        self.book.setcaptions()
        self.setcaptions()
        self.show()

    def setup_menu(self, menus, funcs):
        self.menu_bar.clear()
        self._menus = menus
        self._menuitems = []
        for title, items in menus:
            menu = self.menu_bar.addMenu(self.captions[title])
            for sel in items:
                if sel == -1:
                    menu.addSeparator()
                else:
                    act = gui.QAction(self.captions[sel], self)
                    act.triggered.connect(functools.partial(self.on_menu, sel))
                    if sel == M_SAVE: # in (M_READ, M_SAVE):
                        act.setEnabled(bool(int(self.page.settings['RedefineKeys'][0])))
                    elif sel == M_RBLD:
                        act.setEnabled(bool(int(self.page.settings['RebuildCSV'][0])))
                    elif sel == M_EXIT:
                        act.setShortcut('Ctrl+Q')
                    menu.addAction(act)
            self._menuitems.append(menu)
        self._menu_func = funcs

    def on_menu(self, actionid):
        text = self._menu_func[actionid](self)
        if text:
            gui.QMessageBox.information(self, self.captions["000"], text)

    def exit(self,e=None):
        if not self.page.exit():
            return
        self.close()

    def readcaptions(self, lang):
        self.captions = {}
        with open(os.path.join(HERE, lang)) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value
        self.captions['000'] = self.title

    def setcaptions(self):
        title = self.captions["000"]
        if self.page.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)
        for indx, menu in enumerate(self._menuitems):
            menu.setTitle(self.captions[self._menus[indx][0]])
            for indx2, action in enumerate(menu.actions()):
                hulp = self._menus[indx][1][indx2]
                if hulp != -1:
                    action.setText(self.captions[hulp])
        self.b_exit.setText(self.captions[C_EXIT])
        self.book.setcaptions()
        self.page.setcaptions()

def main(args=None):
    app = gui.QApplication(sys.argv)
    ## redirect=True, filename="hotkeys.log")
    ## print '----------'
    frame = MainFrame(args)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv[1:])
