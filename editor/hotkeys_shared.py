# -*- coding: UTF-8 -*-

from __future__ import print_function
import os
import shutil
import sys
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
HERE = os.path.abspath(os.path.dirname(__file__))
## try:
    ## HOME = os.environ('HOME')
## except KeyError:
    ## HOME = os.environ('USERPROFILE') # Windows
CONF = os.path.join(HERE, 'hotkey_config.py')
TTL = "A hotkey viewer/editor"
VRS = "1.1.x"
AUTH = "(C) 2008-2013 Albert Visser"
XTRA = '''originally built for Total Commander,
extended for use within
all  your favourite applications'''
WIN = True if sys.platform == "win32" else False
## LIN = True if sys.platform == 'linux2' else False
LIN = True if os.name == 'posix' else False

# voorziening voor starten op usb-stick onder Windows (drive letters in config aanpassen)
def check_driveletter():
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

# constanten voor  captions en dergelijke (correspondeert met nummers in language files)
# *** toegesneden op TC verplaatsen naar TC plugin? ***
C_KEY, C_MOD, C_SRT, C_CMD, C_OMS = '001', '043', '002', '003', '004'
C_DFLT, C_RDEF = '005', '006'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
C_SAVE, C_DEL, C_EXIT, C_KTXT, C_CTXT ='010', '011', '012', '018', '019'
M_APP, M_READ, M_SAVE, M_USER, M_EXIT = '200', '201', '202', '203', '209'
M_SETT, M_LOC, M_LANG, M_HELP, M_ABOUT = '210', '211', '212', '290', '299'
NOT_IMPLEMENTED = '404'

# default menu structure
DFLT_MENU = (
    (M_APP, (M_EXIT,)),
    (M_SETT, (M_LANG,)),
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

def m_user(self):
    """(menu) callback voor een nog niet geïmplementeerde actie"""
    return self.captions[NOT_IMPLEMENTED]

def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.exit()

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
        "{}\nversion {}\n{}\n{}".format(TTL, VRS, AUTH, XTRA))

# dispatch table for  menu callbacks (de functies zelf zitten in hotkeys_shared)
DFLT_MENU_FUNC = {
    M_LANG: m_lang,
    M_EXIT: m_exit,
    M_ABOUT: m_about,
}

class HotkeyPanel(gui.QFrame):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    definieert feitelijk een "custom widget"
    coldata is een list of tuple van 4-tuples die achtereenvolgens aangeven
    de kolomtitel, de breedte, de index op self.data en of het een soort aangeeft
    """
    def __init__(self, parent, coldata, **kwargs):

        _ini = kwargs['ini']
        # switch om het gedrag van bepaalde routines tijdens initialisatie te beïnvloeden
        self._initializing = True

        gui.QFrame.__init__(self, parent)
        self.parent = parent.parent()
        self.column_info = coldata
        self.captions = self.parent.captions
        if _ini:
            self.ini = self._keys.Settings(_ini) # 1 pad + language instelling
        self.readkeys()
        self.modified = False

        # gelegenheid voor extra initialisaties en het opbouwen van de rest van de GUI
        # het vullen van veldwaarden hierin gebeurt als gevolg van het vullen
        # van de eerste rij in de listbox, daarom moet deze het laatst
        self.add_extra_fields()

        self._sizer = gui.QVBoxLayout()
        if self.column_info:
            self.p0list = gui.QTreeWidget(self)
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
        self.layout_extra_fields()

        self.setLayout(self._sizer)
        self._initializing = False

    def add_extra_fields(self):
        "define other widgets to be used in the panel"
        pass

    def layout_extra_fields(self):
        "add extra widgets to self._sizer"
        pass

    def captions_extra_fields(self):
        "refresh captions for extra widgets"
        pass

    def on_item_selected(self, olditem, newitem):
        "callback for list selection"
        pass

    def readkeys(self):
        "read the data for the keydef list"
        self.data = self._keys.readkeys(self.ini.pad)

    def savekeys(self, pad=None):
        "save modified keydef back"
        if not pad:
            pad = self.ini.pad
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
        self.p0list.clear()
        items = self.data.items()
        if items is None or len(items) == 0:
            return

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

    def exit(self):
        if self.modified:
            ok = show_message(self, '025')
            if ok == gui.QMessageBox.Yes:
                self.page.savekeys()
            elif ok == gui.QMessageBox.Cancel:
                return False
        return True

# base class for panel viewers
class MainWindow(gui.QMainWindow):
    """Hoofdscherm van de applicatie"""
    def __init__(self, args=None, **kwargs):

        wid = 800 if LIN else 688
        hig = 594
        gui.QMainWindow.__init__(self)
        try:
            self.title = kwargs['title']
        except KeyError:
            self.title = 'Hotkeys'
        self.setWindowTitle(self.title)
        self.resize(wid, hig)
        self.sb = self.statusBar()
        self.sb.showMessage('Welcome to {}!'.format(self.title))

        #~ self.SetIcon(gui.QIcon("task.ico",gui.QBITMAP_TYPE_ICO))
        ## self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))

        self.menu_bar = self.menuBar()
        self.ini = {'filename': CONF}
        with open(self.ini['filename']) as _in:
            for line in _in:
                if line.startswith('LANG'):
                    self.ini['lang'] = line.strip().split('=')[1]
        if 'lang' not in self.ini:
            self.ini['lang'] = 'english.lng'
        self.readcaptions(self.ini['lang']) # set up defaults

        try:
            menus = kwargs['menus']
        except KeyError:
            menus = DFLT_MENU
        try:
            funcs = kwargs['funcs']
        except KeyError:
            funcs = DFLT_MENU_FUNC
        self.setup_menu(menus, funcs)

        pnl = gui.QWidget(self)
        self.page = MyPanel(pnl, args)
        sizer_v = gui.QVBoxLayout()
        sizer_h = gui.QHBoxLayout()
        sizer_h.addWidget(self.page)
        sizer_v.addLayout(sizer_h)
        self.b_exit = gui.QPushButton(self.captions[C_EXIT], self)
        self.b_exit.clicked.connect(self.exit)
        sizer_h = gui.QHBoxLayout()
        sizer_h.addStretch()
        sizer_h.addWidget(self.b_exit)
        sizer_h.addStretch()
        sizer_v.addLayout(sizer_h)
        pnl.setLayout(sizer_v)

        self.setCentralWidget(pnl)
        self.setcaptions()
        self.show()
        if len(self.page.data) == 0:
            gui.QMessageBox.information(self, self.captions['000'],
                self.captions["042"])

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
                    menu.addAction(act)
            self._menuitems.append(menu)
        self._menu_func = funcs

    def on_menu(self, actionid):
        text = self._menu_func[actionid](self)
        if text:
            gui.QMessageBox.information(self, text, self.captions["000"])

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
        self.book.b_next.setText(self.captions['014'])
        self.book.b_prev.setText(self.captions['015'])
        self.book.sel_text.setText(self.captions['050'])
        self.book.find_text.setText(self.captions['051'])
        self.b_exit.setText(self.captions[C_EXIT])
        self.page.setcaptions()

