"""Hotkeys plugin for Total Commander - PyQt specific code
"""
import contextlib
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
# import editor.plugins.mergetool_shared as shared
OKICON = '/usr/share/icons/Adwaita/16x16/emblems/emblem-ok-symbolic.symbolic.png'
TODOICON = '/usr/share/icons/Adwaita/16x16/emblems/emblem-new.png'


# class MergeDialog(shared.MergeMixin, qtw.QDialog):
class MergeDialogGui(qtw.QDialog):
    """Dialoog om een gedocumenteerde toetscombinatie te koppelen aan een commando

    In het ene ini bestand staat namelijk toets + omschrijving en in het andere
    command + omschrijving en de omschrijvingen hoeven uiteraard niet 100% gelijk
    te zijn, dus moeten ze handmatig gekoppeld worden.
    """
    def __init__(self, master, parent):
        """Opbouwen van het scherm

        parent is een SingleDataInterface, master is MergeTool
        """
        self.master = master
        qtw.QDialog.__init__(self, parent)
        self.setWindowTitle("TCCM")
        self.okicon = gui.QIcon(OKICON)
        self.todoicon = gui.QIcon(TODOICON)
        self.resize(1500, 900)

    def init_display(self):
        "build the screen container"
        return qtw.QVBoxLayout()

    def add_row(self, screen):
        "create a horizontal subcontainer to add stuff into"
        sizer = qtw.QHBoxLayout()
        screen.addLayout(sizer)
        return sizer

    def add_col_to_row(self, row):
        "create a vertical subcontainer to add stuff into"
        sizer = qtw.QVBoxLayout()
        row.addLayout(sizer)
        return sizer

    def create_list(self, columns, callback):
        "create a listbox"
        listbox = qtw.QTreeWidget(self)
        listbox.setColumnCount(len(columns))
        listbox.setHeaderLabels(columns)
        listbox.setMouseTracking(True)  # t.b.v. drag&drop
        listbox.currentItemChanged.connect(callback)
        listbox.itemEntered.connect(self.popuptext)
        return listbox

    def create_findbutton(self, columns):
        "create a 'Find' combobox"
        control = qtw.QComboBox(self)
        control.setEditable(False)
        for text in columns:
            control.addItem('Find ' + text)
        control.setCurrentIndex(1)
        return control

    def create_text(self):
        "create a text field"
        return qtw.QLineEdit(self)

    def create_button(self, text, callback, size=0):
        "create a button"
        button = qtw.QPushButton(text, self)
        if size:
            button.setMaximumWidth(size)
        button.clicked.connect(callback)
        return button

    def add_row_to_col(self, col, *args, **kwargs):
        "create a horizontal subcontainer to add widgets to"
        sizer = qtw.QHBoxLayout()
        for arg in ('right_align', 'center'):
            if kwargs.get(arg, False) and len(args) > 1:
                sizer.addStretch()
        for item in args:
            sizer.addWidget(item)
        for arg in ('left_align', 'center'):
            if kwargs.get(arg, False) and len(args) > 1:
                sizer.addStretch()
        col.addLayout(sizer)

    # def create_row(self, *args, **kwargs):
    #     "create a row (horizontal line) of widgets"
    #     sizer = qtw.QHBoxLayout()
    #     for arg in ('right_align', 'center'):
    #         if kwargs.get(arg, False):
    #             sizer.addStretch()
    #     for item in args:
    #         sizer.addWidget(item)
    #     for arg in ('left_align', 'center'):
    #         if kwargs.get(arg, False):
    #             sizer.addStretch()
    #     return sizer

    # def create_column(self, *args, **kwargs):
    #     "create a column (vertical line) of widgets"
    #     sizer = qtw.QVBoxLayout()
    #     for arg in ('bottom_align', 'center'):
    #         if kwargs.get(arg, False):
    #             sizer.addStretch()
    #     for item in args:
    #         sizer.addWidget(item)
    #     for arg in ('top_align', 'center'):
    #         if kwargs.get(arg, False):
    #             sizer.addStretch()
    #     return sizer

    # def add_to_screen(self, parent, sizer, **kwargs):
    #     "add a row or column to the screen estate"
    #     parent.addLayout(sizer)

    def finalize_display(self, vbox):
        "add the layout to the window"
        self.setLayout(vbox)

    def create_hotkey(self, text, callback, keyseq, desc):
        "create shortcuts for actions"
        act = gui.QAction(text, self)
        act.triggered.connect(callback)
        act.setShortcut(keyseq)
        self.addAction(act)

    def clear_list(self, listbox):
        "initialize the list"
        listbox.clear()

    def get_listbox_count(self, listbox):
        "return the number of entries in the list"
        return listbox.topLevelItemCount()

    def add_listitem(self, listbox, keytext, command):
        "add an item to the list"
        new = qtw.QTreeWidgetItem()
        new.setText(0, keytext)
        new.setText(1, command)
        listbox.addTopLevelItem(new)
        return new

    def set_listitem_icon(self, listbox, item):
        "set the check image for a keycombo list item"
        item.setIcon(0, self.okicon)

    # def get_selected_key_data(self):
    #     "get the texts for the selected keycombo"
    #     keychoice = self.listkeys.currentItem()
    #     return keychoice, keychoice.text(0), keychoice.text(1)

    # def get_selected_cmd_data(self):
    #     "get the texts for the selected command"
    #     cmdchoice = self.listcmds.currentItem()
    #     return cmdchoice, cmdchoice.text(0)

    # def get_selected_matchitem(self):
    #     "get the selected mapping item"
    #     return self.listmatches.currentItem()

    def get_selected_listbox_data(self, listbox):
        "get the selected item and the texts for it"
        choice = listbox.currentItem()
        text0 = text1 = ''
        with contextlib.suppress(AttributeError):
            text0 = choice.text(0)
        with contextlib.suppress(AttributeError):
            text1 = choice.text(1)
        return choice, text0, text1

    # def find_in_listmatches(self, keytext):
    #     "find a keycombo in the mappings list"
    #     for ix in range(self.listmatches.topLevelItemCount()):
    #         item = self.listmatches.topLevelItem(ix)
    #         if item.text(0) == keytext:
    #             break
    #     else:
    #         item = None
    #     return item

    # def find_in_listkeys(self, keytext):
    #     "find a keycombo in the shortcuts list"
    #     for ix in range(self.listkeys.topLevelItemCount()):
    #         item = self.listkeys.topLevelItem(ix)
    #         if item.text(0) == keytext:
    #             break
    #     else:
    #         item = None
    #     return item

    def find_in_listbox(self, listbox, text):
        "find a text in a list (mainly for keycombos)"
        for ix in range(listbox.topLevelItemCount()):
            item = listbox.topLevelItem(ix)
            if item.text(0) == text:
                break
        else:
            item = None
        return item

    def replace_listbox_item(self, listbox, item, cmdtext):
        "replace the command in a mapping item"
        item.setText(1, cmdtext)

    def ensure_listitem_visible(self, listbox, item):
        "make sure the selected mapping can be viewed in the list"
        listbox.scrollToItem(listbox.indexFromItem(item))

    def remove_listbox_item(self, listbox, item):
        "delete a mapping from the list"
        ix = listbox.indexOfTopLevelItem(item)
        item = listbox.takeTopLevelItem(ix)

    def reset_listitem_icon(self, listbox, ix):
        "find the corresponding keycombo item and unset the check image"
        # beetje omslachtige manier van een icon verwijderen bij een TreeWidgetItem!
        item = listbox.topLevelItem(ix)
        # newitem = qtw.QTreeWidgetItem()
        # newitem.setText(0, item.text(0))
        # newitem.setText(1, item.text(1))
        # ix = self.listkeys.indexOfTopLevelItem(item)
        # self.listkeys.takeTopLevelItem(ix)
        # self.listkeys.insertTopLevelItem(ix, newitem)
        # alternatief: "default" icon
        item.setIcon(0, self.todoicon)

    # def focuskeylist(self):
    #     "shift focus for selecting a keycombo item"
    #     self.listkeys.setFocus()

    # def focuscmdlist(self):
    #     "shift focus for selecting a command item"
    #     self.listcmds.setFocus()

    # def focusmatchlist(self):
    #     "shift focus for selecting a mapping item"
    #     self.listmatches.setFocus()

    # def focusfindkey(self):
    #     "shift focus to enter a keycombo search phrase"
    #     self.findkeytext.setFocus()

    # def focusfindcmd(self):
    #     "shift focus to enter a command search phrase"
    #     self.findcmdtext.setFocus()

    def set_focus_to(self, widget):
        "shift focus to a specific screen element"
        widget.setFocus()

    def popuptext(self, item, colno):
        "show complete text of description if moused over"
        if colno == 1:
            item.setToolTip(colno, item.text(colno))

    def get_entry_text(self, win):
        "get a text entry field's text"
        return win.text()

    def get_search_choice(self, control):
        "return the selected item's index for the given list"
        return control.currentIndex()

    def find_listitems(self, win, search, in_col=1):
        "find all items in a list that contain text in a given column"
        return win.findItems(search, core.Qt.MatchFlag.MatchContains, in_col)   # 1)

    def get_selected_item(self, win):
        "get the selected item in a list"
        return win.currentItem()

    def get_first_item(self, win):
        "get the first item of a list"
        return win.topLevelItem(0)

    def get_last_item(self, win):
        "get the last item of a list"
        return win.topLevelItem(win.topLevelItemCount() - 1)

    def get_item_text(self, win, item, col):
        "get the text for a column of an item in one of the lists"
        return item.text(col)

    def set_selected_item(self, win, item):
        "set the selected item for on of the lists"
        # return list.currentItem() -- pardon?
        win.setCurrentItem(item)

    # def count_matches(self):
    #     "get the current number of mappings in the list"
    #     return self.listmatches.topLevelItemCount()

    # def matches_loaded(self):
    #    return self.listkeys.topLevelItemCount() > 0

    # def get_matchitem_data(self, ix):
    #     "get the texts for a mapping item"
    #     item = self.listmatches.topLevelItem(ix)
    #     return item.text(0), item.text(1)
