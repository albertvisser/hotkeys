"""Hotkeys plugin for Total Commander - PyQt specific code
"""
# TODO: ombouwen en gui-onafhanlkelijke onderdelen uitlichten
import os
import csv
# import functools
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
# import editor.shared as shared
from .tcmdrkys_shared import PATHS, defaultkeys, defaultcommands, translate_keyname
OKICON = '/usr/share/icons/Adwaita/16x16/emblems/emblem-ok-symbolic.symbolic.png'


def send_mergedialog(page):
    """show the dialog for connecting commands to keyboard shortcuts
    """
    dlg = TcMergeDialog(page)
    paths = [page.settings[x] for x in reversed(PATHS[:4])]
    paths.append(page.pad)
    dlg.load_files(paths)
    ## dlg.load_files((
        ## parent.page.settings['KB_PAD'][0],
        ## parent.page.settings['CI_PAD'][0],
        ## parent.page.settings['UC_PAD'][0],
        ## parent.page.settings['TC_PAD'][0],
        ## parent.page.pad))
    ok = dlg.exec_()
    return ok == qtw.QDialog.Accepted


class TcMergeDialog(qtw.QDialog):
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
        super().__init__(parent.gui)
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
                item = self.listkeys.findItems(keytext, core.Qt.MatchFixedString, 0)[0]
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
            qtw.QMessageBox.information(self, "Delete entry", "Choose an item to " "delete")
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
            qtw.QMessageBox.information(self, 'Find text', 'Please enter text to search for')
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
        test = self.findnextitem(self.findkeytext, self.keysearch, self.listkeys, self.keyresults)
        if test:
            self.keysearch, self.keyresults = test

    def findprevkey(self):
        "find previous matching key item"
        test = self.findprevitem(self.findkeytext, self.keysearch, self.listkeys, self.keyresults)
        if test:
            self.keysearch, self.keyresults = test

    def findnextcmd(self):
        "find next matching command item"
        test = self.findnextitem(self.findcmdtext, self.cmdsearch, self.listcmds, self.cmdresults)
        if test:
            self.cmdsearch, self.cmdresults = test

    def findprevcmd(self):
        "find previous matching command item"
        test = self.findprevitem(self.findcmdtext, self.cmdsearch, self.listcmds, self.cmdresults)
        if test:
            self.cmdsearch, self.cmdresults = test

    def reset_all(self):
        """remove all associations
        """
        self.listlinks.clear()
        self.load_keys()  # to reset all indicators

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
            shortcuts[ix] = (translate_keyname(key), mods, 'S', cmd, desc)
        self.parent().tempdata = shortcuts
        super().accept()
