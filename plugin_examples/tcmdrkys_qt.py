"""Hotkeys plugin for Total Commander - PyQt specific code
"""
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import editor.plugins.tcmdrkys_shared as shared
OKICON = '/usr/share/icons/Adwaita/16x16/emblems/emblem-ok-symbolic.symbolic.png'


class TcMergeDialog(shared.TcMergeMixin, qtw.QDialog):
    """Dialoog om een gedocumenteerde toetscombinatie te koppelen aan een commando

    In het ene ini bestand staat namelijk toets + omschrijving en in het andere
    command + omschrijving en de omschrijvingen hoeven uiteraard niet 100% gelijk
    te zijn, dus moeten ze handmatig gekoppeld worden. Vandaar de ietwat misleidende
    naam "links"
    """
    def __init__(self, parent, master):
        """Opbouwen van het scherm

        parent is een SingleDataInterface, master is een HotKeyPanel
        """
        shared.TcMergeMixin.__init__(self, master)
        qtw.QDialog.__init__(self, parent)
        self.setWindowTitle("TCCM")
        self.okicon = gui.QIcon(OKICON)
        self.resize(1000, 600)

        self.listkeys = qtw.QTreeWidget(self)
        self.listkeys.setColumnCount(2)
        self.listkeys.setHeaderLabels(['Key', 'Description'])
        self.listkeys.setMouseTracking(True)
        self.listkeys.itemEntered.connect(self.popuptext)

        self.findkeytext = qtw.QLineEdit(self)
        self.nextkey = qtw.QPushButton('&Next', self)
        self.nextkey.setMaximumWidth(50)
        self.nextkey.clicked.connect(self.findnextkey)
        self.prevkey = qtw.QPushButton('&Prev', self)
        self.prevkey.setMaximumWidth(50)
        self.prevkey.clicked.connect(self.findprevkey)

        self.listcmds = qtw.QTreeWidget(self)
        self.listcmds.setColumnCount(2)
        self.listcmds.setHeaderLabels(['Command', 'Description'])
        self.listcmds.setMouseTracking(True)
        self.listcmds.itemEntered.connect(self.popuptext)

        self.findcmdtext = qtw.QLineEdit(self)
        self.nextcmd = qtw.QPushButton('Ne&xt', self)
        self.nextcmd.setMaximumWidth(50)
        self.nextcmd.clicked.connect(self.findnextcmd)
        self.prevcmd = qtw.QPushButton('Pre&v', self)
        self.prevcmd.setMaximumWidth(50)
        self.prevcmd.clicked.connect(self.findprevcmd)

        self.listlinks = qtw.QTreeWidget(self)
        self.listlinks.setColumnCount(2)
        self.listlinks.setHeaderLabels(['Key', 'Command'])

        self.btn_link = qtw.QPushButton("&+ Add/Replace Link", self)
        self.btn_link.clicked.connect(self.make_link)
        self.btn_delete = qtw.QPushButton("&- Discard Link", self)
        self.btn_delete.clicked.connect(self.delete_link)

        self.btn_load = qtw.QPushButton("&Load Links", self)
        self.btn_load.clicked.connect(self.load_links)
        self.btn_clear = qtw.QPushButton("&Clear All", self)
        self.btn_clear.clicked.connect(self.reset_all)
        self.btn_save = qtw.QPushButton("&Save Links", self)
        self.btn_save.clicked.connect(self.save_links)
        self.btn_quit = qtw.QPushButton("&Afsluiten", self)
        self.btn_quit.clicked.connect(self.close)
        self.btn_build = qtw.QPushButton("&Build CSV", self)
        self.btn_build.clicked.connect(self.confirm)

        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()

        vbox2 = qtw.QVBoxLayout()
        vbox2.addWidget(self.listkeys)
        hbox2 = qtw.QHBoxLayout()
        hbox2.addWidget(qtw.QLabel('Find text:', self))
        hbox2.addWidget(self.findkeytext)
        hbox2.addWidget(self.nextkey)
        hbox2.addWidget(self.prevkey)
        hbox2.addStretch()
        vbox2.addLayout(hbox2)
        hbox.addLayout(vbox2)

        vbox2 = qtw.QVBoxLayout()
        vbox2.addWidget(self.listcmds)

        hbox2 = qtw.QHBoxLayout()
        hbox2.addWidget(qtw.QLabel('Find text:', self))
        hbox2.addWidget(self.findcmdtext)
        hbox2.addWidget(self.nextcmd)
        hbox2.addWidget(self.prevcmd)
        hbox2.addStretch()
        vbox2.addLayout(hbox2)
        hbox.addLayout(vbox2)

        vbox2 = qtw.QVBoxLayout()
        vbox2.addWidget(self.listlinks)

        hbox2 = qtw.QHBoxLayout()
        hbox2.addStretch()
        hbox2.addWidget(self.btn_link)
        hbox2.addWidget(self.btn_delete)
        hbox2.addStretch()
        vbox2.addLayout(hbox2)
        hbox.addLayout(vbox2)
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

        for text, callback, keyseq, desc in self.getshortcuts():
            act = qtw.QAction(text, self)
            act.triggered.connect(callback)
            act.setShortcut(keyseq)
            self.addAction(act)
        self.load_files()

    def clear_listkeys(self):
        "initialize the list of keycombos"
        self.listkeys.clear()

    def add_listkeys_item(self, key, value):
        "add an item to the list of keycombos"
        new = qtw.QTreeWidgetItem()
        new.setText(0, key)
        new.setText(1, value['oms'])
        self.listkeys.addTopLevelItem(new)

    def clear_listcmds(self):
        "initialize the list of mappable commands"
        self.listcmds.clear()

    def add_listcmds_item(self, key, value):
        "add an item to the list of mappable commands"
        new = qtw.QTreeWidgetItem()
        new.setText(0, key)
        new.setText(1, value['oms'])
        self.listcmds.addTopLevelItem(new)

    def clear_listlinks(self):
        "(re)initialize the list of mappings"
        self.listlinks.clear()
        for ix in range(self.listlinks.topLevelItemCount()):
            item = self.listlinks.topLevelItem(ix)
            self.reset_listitem_icon(listitem)

    def add_listlinks_item(self, keytext, command):
        "add an item to the list of mappings"
        new = qtw.QTreeWidgetItem()
        new.setText(0, keytext)
        new.setText(1, command)
        self.listlinks.addTopLevelItem(new)

    def set_listitem_icon(self, item):
        "set the check image for a keycombo list item"
        item.setIcon(0, self.okicon)

    def get_selected_key_data(self):
        "get the texts for the selected keycombo"
        keychoice = self.listkeys.currentItem()
        return keychoice, keychoice.text(0), keychoice.text(1)

    def get_selected_cmd_data(self):
        "get the texts for the selected command"
        cmdchoice = self.listcmds.currentItem()
        return cmdchoice, cmdchoice.text(0)

    def get_selected_linkitem(self):
        "get the selected mapping item"
        return self.listlinks.currentItem()

    def find_in_listlinks(self, keytext):
        "find a keycombo in the mappings list"
        for ix in range(self.listlinks.topLevelItemCount()):
            item = self.listlinks.topLevelItem(ix)
            if item.text(0) == keytext:
                break
        else:
            item = None
        return item

    def find_in_listkeys(self, keytext):
        "find a keycombo in the mappings list"
        for ix in range(self.listkeys.topLevelItemCount()):
            item = self.listkeys.topLevelItem(ix)
            if item.text(0) == keytext:
                break
        else:
            item = None
        return item

    def replace_linklist_item(self, item, cmdtext):
        "replace the command in a mapping item"
        item.setText(1, cmdtext)

    def ensure_item_visible(self, item):
        "make sure the selected mapping can be viewed in the list"
        self.listlinks.scrollTo(self.listlinks.indexFromItem(item))

    def remove_linkitem(self, item):
        "delete a mapping from the list"
        ix = self.listlinks.indexOfTopLevelItem(item)
        item = self.listlinks.takeTopLevelItem(ix)

    def reset_listitem_icon(self, item):
        "find the corresponding keycombo item and unset the check image"
        # beetje omslachtige manier van een icon verwijderen bij een TreeWidgetItem!
        newitem = qtw.QTreeWidgetItem()
        newitem.setText(0, item.text(0))
        newitem.setText(1, item.text(1))
        ix = self.listkeys.indexOfTopLevelItem(item)
        self.listkeys.takeTopLevelItem(ix)
        self.listkeys.insertTopLevelItem(ix, newitem)

    def focuskeylist(self):
        "shift focus for selecting a keycombo item"
        self.listkeys.setFocus()

    def focuscmdlist(self):
        "shift focus for selecting a command item"
        self.listcmds.setFocus()

    def focusfindkey(self):
        "shift focus to enter a keycombo search phrase"
        self.findkeytext.setFocus()

    def focusfindcmd(self):
        "shift focus to enter a command search phrase"
        self.findcmdtext.setFocus()

    def popuptext(self, item, colno):
        "show complete text of description if moused over"
        if colno == 1:
            item.setToolTip(colno, item.text(colno))

    def get_entry_text(self, win):
        "get a text entry field's text"
        return win.text()

    def find_listitems(self, win, search):
        "find all items in a list that contain a search text"
        return win.findItems(search, core.Qt.MatchContains, 1)

    def get_selected_item(self, win):
        "get the selected item in a list"
        return win.currentItem()

    def get_first_item(self, win):
        "get the first item of a list"
        return win.topLevelItem(0)

    def get_last_item(self, win):
        "get the last item of a list"
        return win.topLevelItem(list.topLevelItemCount() - 1)

    def get_item_text(self, win, item, col):
        "get the text for a column of an item in one of the lists"
        return item.text(col)

    def set_selected_item(self, win, item):
        "set the selected item for on of the lists"
        # return list.currentItem() -- pardon?
        win.setCurrentItem(item)

    def count_links(self):
        "get the current number of mappings in the list"
        return self.listlinks.topLevelItemCount()

    def get_linkitem_data(self, ix):
        "get the texts for a mapping item"
        item = self.listlinks.topLevelItem(ix)
        return item.text(0), item.text(1)
