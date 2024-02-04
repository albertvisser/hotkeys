"""HotKeys main program - gui specific code - Qt version
"""
import sys
import contextlib
import functools
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
import PyQt5.QtCore as core
from editor import shared


class DummyPage(qtw.QFrame):
    "simulate some hotkeypanel functionality"
    def __init__(self, parent, message):
        super().__init__(parent)
        sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(qtw.QLabel(message, self))
        hsizer.addStretch()
        sizer.addLayout(hsizer)
        self.setLayout(sizer)

    def exit(self):
        """simulate processing triggered by exit button
        """
        return True


class SingleDataInterface(qtw.QFrame):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    definieert feitelijk een "custom widget"
    """
    def __init__(self, parent, master):
        super().__init__(parent)
        self.parent = parent  # .parent()
        self.master = master

    def setup_empty_screen(self, nodata, title):
        """build a subscreen with only a message
        """
        sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(qtw.QLabel(nodata, self))
        hsizer.addStretch()
        sizer.addLayout(hsizer)
        self.setLayout(sizer)
        self.title = title

    def setup_list(self):
        """add the list widget to the interface
        """
        self.p0list = qtw.QTreeWidget(self)
        sizer = qtw.QVBoxLayout()
        if self.master.column_info:
            self.p0list.setHeaderLabels([self.master.captions[col[0]] for col in
                                         self.master.column_info])
            self.p0list.setAlternatingRowColors(True)
            self.p0list.currentItemChanged.connect(self.on_item_selected)
            hdr = self.p0list.header()
            hdr.setSectionsClickable(True)
            for indx, col in enumerate(self.master.column_info):
                if indx <= len(self.master.column_info):
                    hdr.resizeSection(indx, col[1])
            hdr.setStretchLastSection(True)
            self.master.populate_list()
            self.p0list.setSortingEnabled(True)
            sizer1 = qtw.QHBoxLayout()
            sizer1.addWidget(self.p0list)
            sizer.addLayout(sizer1)

        # indien van toepassing: toevoegen van de rest van de GUI aan de layout
        if self.master.has_extrapanel:
            self.layout_extra_fields(sizer)

        self.setLayout(sizer)
        shared.log(self.master.otherstuff)
        self.set_listselection(0)

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        self.screenfields = []
        self._box = box = qtw.QFrame(self)
        frameheight = 90
        # try:
        if hasattr(self.master.reader, 'get_frameheight'):
            frameheight = self.master.reader.get_frameheight()  # user exit
        # except AttributeError:
        #     shared.log_exc()
        box.setMaximumHeight(frameheight)

        if 'C_KEY' in self.master.fields:
            self.lbl_key = qtw.QLabel(self.master.captions['C_KTXT'] + " ", box)
            if self.master.keylist is None:
                ted = qtw.QLineEdit(box)
                ted.setMaximumWidth(90)
                ted.textChanged[str].connect(functools.partial(self.master.on_text, ted, str))
                self.screenfields.append(ted)
                self.txt_key = ted
            else:
                cb = qtw.QComboBox(box)
                cb.setMaximumWidth(90)
                cb.addItems(self.master.keylist)  # niet sorteren
                cb.currentIndexChanged[str].connect(functools.partial(self.master.on_combobox, cb,
                                                                      str))
                self.screenfields.append(cb)
                self.cmb_key = cb

        if 'C_MODS' in self.master.fields:
            for ix, x in enumerate(('M_CTRL', 'M_ALT', 'M_SHFT', 'M_WIN')):
                cb = qtw.QCheckBox(self.master.captions[x].join(("+ ", "")), box)
                cb.setChecked(False)
                self.screenfields.append(cb)
                cb.stateChanged.connect(functools.partial(self.master.on_checkbox, cb))
                if ix == 0:
                    self.cb_ctrl = cb
                elif ix == 1:
                    self.cb_alt = cb
                elif ix == 2:
                    self.cb_shift = cb
                elif ix == 3:
                    self.cb_win = cb

        if 'C_CNTXT' in self.master.fields:
            self.lbl_context = qtw.QLabel(self.master.captions['C_CNTXT'], box)
            cb = qtw.QComboBox(box)
            cb.addItems(self.master.contextslist)
            cb.setMaximumWidth(110)
            cb.currentIndexChanged[str].connect(functools.partial(self.master.on_combobox, cb, str))
            self.screenfields.append(cb)
            self.cmb_context = cb

        if 'C_CMD' in self.master.fields:
            self.txt_cmd = qtw.QLabel(self.master.captions['C_CTXT'] + " ", box)
            cb = qtw.QComboBox(self)
            cb.setMaximumWidth(150)
            if 'C_CNTXT' not in self.master.fields:  # load on choosing context
                cb.addItems(self.master.commandslist)
            cb.currentIndexChanged[str].connect(functools.partial(self.master.on_combobox, cb, str))
            self.screenfields.append(cb)
            self.cmb_commando = cb

        if 'C_PARMS' in self.master.fields:
            self.lbl_parms = qtw.QLabel(self.master.captions['C_PARMS'], box)
            self.txt_parms = qtw.QLineEdit(box)
            self.txt_parms.setMaximumWidth(280)
            self.screenfields.append(self.txt_parms)

        if 'C_CTRL' in self.master.fields:
            self.lbl_controls = qtw.QLabel(self.master.captions['C_CTRL'], box)
            cb = qtw.QComboBox(box)
            cb.addItems(self.master.controlslist)
            cb.currentIndexChanged[str].connect(functools.partial(self.master.on_combobox, cb, str))
            self.screenfields.append(cb)
            self.cmb_controls = cb

        if 'C_BPARMS' in self.master.fields:
            self.pre_parms_label = qtw.QLabel(box)
            self.pre_parms_text = qtw.QLineEdit(box)
            self.screenfields.append(self.pre_parms_text)

        if 'C_APARMS' in self.master.fields:
            self.post_parms_label = qtw.QLabel(box)
            self.post_parms_text = qtw.QLineEdit(box)
            self.screenfields.append(self.post_parms_text)

        if 'C_FEAT' in self.master.fields:
            self.feature_label = qtw.QLabel(box)
            self.feature_select = qtw.QComboBox(box)
            self.feature_select.addItems(self.master.featurelist)
            self.screenfields.append(self.feature_select)

        if 'C_DESC' in self.master.fields:
            self.txt_oms = qtw.QTextEdit(box)
            self.txt_oms.setReadOnly(True)

        self.b_save = qtw.QPushButton(self.master.captions['C_SAVE'], box)
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(self.on_update)
        self.b_del = qtw.QPushButton(self.master.captions['C_DEL'], box)
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(self.on_delete)
        self._savestates = (False, False)

    def set_extrascreen_editable(self, switch):
        """open up fields in extra screen when applicable
        """
        for widget in self.screenfields:
            widget.setEnabled(switch)
        ## if 'C_CMD' in self.fields:
        if switch:
            state_s, state_d = self._savestates
        else:
            self._savestates = (self.b_save.isEnabled(), self.b_del.isEnabled())
            state_s, state_d = False, False
        self.b_save.setEnabled(state_s)
        self.b_del.setEnabled(state_d)

    def layout_extra_fields(self, sizer):
        """add the extra fields to the layout
        """
        bsizer = qtw.QVBoxLayout()

        sizer1 = qtw.QHBoxLayout()
        sizer2 = qtw.QHBoxLayout()
        if 'C_KEY' in self.master.fields:
            sizer3 = qtw.QHBoxLayout()
            sizer3.addWidget(self.lbl_key)
            if self.master.keylist is None:
                sizer3.addWidget(self.txt_key)
            else:
                sizer3.addWidget(self.cmb_key)
            sizer3.addStretch()
            sizer2.addLayout(sizer3)

        if 'C_MODS' in self.master.fields:
            sizer3 = qtw.QHBoxLayout()
            sizer3.addWidget(self.cb_ctrl)
            sizer3.addWidget(self.cb_alt)
            sizer3.addWidget(self.cb_shift)
            sizer3.addWidget(self.cb_win)
            sizer3.addStretch()
            sizer2.addLayout(sizer3)

        sizer1.addLayout(sizer2)
        sizer1.addStretch()
        if 'C_CNTXT' in self.master.fields:
            sizer2 = qtw.QHBoxLayout()
            sizer2.addWidget(self.lbl_context)
            sizer2.addWidget(self.cmb_context)
            sizer1.addLayout(sizer2)

        if 'C_CMD' in self.master.fields:
            sizer2 = qtw.QHBoxLayout()
            sizer2.addWidget(self.txt_cmd)
            sizer2.addWidget(self.cmb_commando)
            sizer1.addLayout(sizer2)

        # try:
        if hasattr(self.master.reader, 'extra_fields_topline'):
            self.master.reader.layout_extra_fields_topline(self, sizer1)  # user exit
        # except AttributeError:
        #     shared.log_exc()

        sizer1.addWidget(self.b_save)
        sizer1.addWidget(self.b_del)
        bsizer.addLayout(sizer1)

        # try:
        #    test = self.master.reader.layout_extra_fields_nextline
        # except AttributeError:
        #     shared.log_exc()
        # else:
        if hasattr(self.master.reader, 'extra_fields_nextline'):
            sizer1 = qtw.QHBoxLayout()
            self.master.reader.layout_extra_fields_nextline(self, sizer1)  # user exit
            bsizer.addLayout(sizer1)

        sizer1 = qtw.QHBoxLayout()
        if 'C_DESC' in self.master.fields:
            sizer2 = qtw.QVBoxLayout()
            sizer2.addWidget(self.txt_oms)
            sizer1.addLayout(sizer2, 2)

        # try:
        if hasattr(self.master.reader, 'extra_fields'):
            self.master.reader.layout_extra_fields(self, sizer1)  # user exit
        # except AttributeError:
        #    shared.log_exc()

        bsizer.addLayout(sizer1)

        self._box.setLayout(bsizer)
        sizer.addWidget(self._box)

    def resize_if_necessary(self):
        """to be called on changing the language
        """
        # for compatibility: no actions needed here

    def on_item_selected(self, newitem, olditem):
        """callback on selection of an item
        """
        if newitem and self.master.has_extrapanel:
            self.master.process_changed_selection(newitem, olditem)

    def on_update(self):
        """callback for editing kb shortcut
        """
        self.master.apply_changes()
        self.p0list.setFocus()

    def on_delete(self):
        """callback for deleting kb shortcut
        """
        self.master.apply_deletion()
        self.p0list.setFocus()

    # hulproutine t.b.v. managen column properties

    def update_columns(self, oldcount, newcount):
        "delete and insert columns"
        return  # wx code, not sure if I need this
        hlp = oldcount
        while hlp > newcount:
            self.p0list.DeleteColumn(0)
            hlp -= 1
        hlp = newcount
        while hlp > oldcount:
            self.p0list.AppendColumn()
            hlp -= 1

    def refresh_headers(self, headers):
        "apply changes in the column headers"
        self.p0list.setColumnCount(len(headers))
        self.p0list.setHeaderLabels(headers)
        hdr = self.p0list.header()
        hdr.setSectionsClickable(True)
        for indx, col in enumerate(self.master.column_info):
            hdr.resizeSection(indx, col[1])
        hdr.setStretchLastSection(True)

# -- helper methods (called from master class) --
    def set_title(self, title):
        "set screen title"
        self.master.parent.parent.gui.setWindowTitle(title)

    def clear_list(self):
        "reset listcontrol"
        self.p0list.clear()

    def build_listitem(self, key):
        "create a new item for the list"
        new_item = qtw.QTreeWidgetItem()
        new_item.setData(0, core.Qt.UserRole, key)
        return new_item

    def set_listitemtext(self, item, indx, value):
        "set the text for a list item"
        item.setText(indx, value)
        item.setToolTip(indx, value)

    def add_listitem(self, new_item):
        "add an item to the list"
        self.p0list.addTopLevelItem(new_item)

    def set_listselection(self, pos):
        "highlight the selected item in the list"
        self.p0list.setCurrentItem(self.p0list.topLevelItem(pos))

    def getfirstitem(self):
        "return first item in list"
        return self.p0list.topLevelItem(0)

    # used by on_text
    def get_widget_text(self, ted, text):
        "return the text entered in a textfield"
        text = str(text)    # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan
                            # de callback soms fout? Of is het Py3 vs Py2?
        hlp = ted.text()
        if text != hlp:
            text = hlp
        return text

    def enable_save(self, state):
        "make save button accessible"
        self.b_save.setEnabled(state)

    # used by on_combobox
    def get_choice_value(self, cb, dummy, text):
        "return the value chosen in a combobox (and the widget itself)"
        return cb, text

    def get_combobox_text(self, cb):
        "return the text entered/selected in a combobox"
        return cb.currentText()

    def init_combobox(self, cb, choices=None):
        "initialize combobox to a set of new values"
        cb.clear()
        if choices is not None:
            cb.addItems(choices)

    def set_label_text(self, lbl, value):
        "set the text for a label / static text"
        lbl.setText(value)

    def set_textfield_value(self, txt, value):
        "set the text for a textfield"
        txt.setText(value)

    # used by on_checkbox
    def get_check_value(self, cb, state):
        "return the state set in a checkbox (and the widget itself)"
        return cb, state

    def get_checkbox_state(self, cb):
        "return the state set in a checkbox (without the widget)"
        return cb.isChecked()

    # used by on_item_selected
    def get_keydef_at_position(self, pos):
        "return the index of a given keydef entry"
        return self.p0list.topLevelItem(pos)

    # used by refresh_extrascreen
    def enable_delete(self, state):
        "make delete button accessible"
        self.b_del.setEnabled(state)

    def get_itemdata(self, item):
        "return the data associated with a listitem"
        return item.data(0, core.Qt.UserRole)

    def set_checkbox_state(self, cb, state):
        "set the state for a checkbox"
        cb.setChecked(state)

    def set_combobox_string(self, cmb, value, valuelist):
        "set the selection for a combobox"
        try:
            ix = valuelist.index(value)
        except ValueError:
            return
        cmb.setCurrentIndex(ix)

    def get_combobox_selection(self, cmb):
        "get the selection for a combobox"
        return cmb.currentText()

    # used by apply_changes en apply_deletion
    def get_selected_keydef(self):
        "return the currently selected keydef"
        return self.p0list.currentItem()

    def get_keydef_position(self, item):
        "return the index of a given keydef entry"
        return self.p0list.indexOfTopLevelItem(item)


class TabbedInterface(qtw.QFrame):
    """ Als QTabwidget, maar met selector in plaats van tabs
    """
    def __init__(self, parent, master):
        super().__init__(parent)
        self.parent = parent
        self.master = master

    def setup_selector(self):
        "create the selector"
        self.sel = qtw.QComboBox(self)
        self.sel.currentIndexChanged.connect(self.master.on_page_changed)
        self.pnl = qtw.QStackedWidget(self)

    def setup_search(self):
        "add the search-related widgets to the interface"
        self.find_loc = qtw.QComboBox(self)
        self.find_loc.setMinimumContentsLength(5)
        self.find_loc.setEditable(False)
        self.find = qtw.QComboBox(self)
        self.find.setMinimumContentsLength(20)
        self.find.setEditable(True)
        self.find.editTextChanged.connect(self.master.on_text_changed)
        self.b_next = qtw.QPushButton("", self)
        self.b_next.clicked.connect(self.master.find_next)
        self.b_next.setEnabled(False)
        self.b_prev = qtw.QPushButton('', self)
        self.b_prev.clicked.connect(self.master.find_prev)
        self.b_prev.setEnabled(False)
        self.b_filter = qtw.QPushButton(self.parent.editor.captions['C_FILTER'], self)
        self.b_filter.clicked.connect(self.master.filter)
        self.b_filter.setEnabled(False)
        self.filter_on = False

    def add_subscreen(self, win):
        "add a screen to the tabbed widget"
        self.pnl.addWidget(win.gui)

    def add_to_selector(self, txt):
        "add an option to the selector"
        self.sel.addItem(txt)

    def format_screen(self):
        "realize the screen"
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addSpacing(10)
        self.sel_text = qtw.QLabel("", self)
        hbox.addWidget(self.sel_text)
        hbox.addWidget(self.sel)
        hbox.addStretch()
        self.find_text = qtw.QLabel("", self)
        hbox.addWidget(self.find_text)
        hbox.addWidget(self.find_loc)
        hbox.addWidget(qtw.QLabel(":", self))
        hbox.addWidget(self.find)
        hbox.addWidget(self.b_filter)
        hbox.addWidget(self.b_next)
        hbox.addWidget(self.b_prev)
        hbox.addSpacing(10)
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        hbox.addWidget(self.pnl)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setcaptions()

    def setcaptions(self):
        """update captions according to selected language
        """
        self.b_next.setText(self.parent.editor.captions['C_NEXT'])
        self.b_prev.setText(self.parent.editor.captions['C_PREV'])
        self.sel_text.setText(self.parent.editor.captions['C_SELPRG'])
        self.find_text.setText(self.parent.editor.captions['C_FIND'])
        if self.filter_on:
            self.b_filter.setText(self.parent.editor.captions['C_FLTOFF'])
        else:
            self.b_filter.setText(self.parent.editor.captions['C_FILTER'])
        with contextlib.suppress(AttributeError):  # exit button bestaat nog niet bij initialisatie
            self.parent.b_exit.setText(self.parent.editor.captions['C_EXIT'])

    # used by on_page_changed
    def get_panel(self):
        "return the currently selected panel's index"
        return self.pnl.currentWidget()

    def get_selected_tool(self):
        "return the currently selected panel's name"
        return self.sel.currentText()

    def set_selected_panel(self, indx):
        "set the index of the panel to be selected"
        self.pnl.setCurrentIndex(indx)

    def update_search(self, items):
        "refresh the search-related widgets"
        self.find_loc.clear()
        self.find_loc.addItems(items)
        self.find_loc.setCurrentText(items[-1])
        if self.master.page.filtertext:
            self.find.setEditText(self.master.page.filtertext)
            self.b_filter.setText(self.parent.captions['C_FLTOFF'])
            self.enable_search_buttons(filter=True)
        else:
            self.find.setEditText('')
            self.find.setEnabled(True)
            self.init_search_buttons()

    # used by on_text_changed
    def get_search_col(self):
        "return the currently selected search column"
        return self.find_loc.currentText()

    def find_items(self, page, text):
        "return the items that contain the text to search for"
        return page.gui.p0list.findItems(text, core.Qt.MatchContains, self.master.zoekcol)

    def init_search_buttons(self):
        "set the search-related buttons to their initial values (i.e. disabled)"
        self.enable_search_buttons(next=False, prev=False, filter=False)

    def set_selected_keydef_item(self, page, index):
        "select a search result in the list"
        item = self.master.items_found[index]
        page.gui.p0list.setCurrentItem(item)
        page.gui.p0list.scrollToItem(item)

    def enable_search_buttons(self, next=None, prev=None, filter=None):
        "set the appropriate search-related button(s) to the given value)s)"
        if next is not None:
            self.b_next.setEnabled(next)
        if prev is not None:
            self.b_prev.setEnabled(prev)
        if filter is not None:
            self.b_filter.setEnabled(filter)

    # used by filter
    def get_filter_state_text(self):
        "return the current text of the filter button"
        return str(self.b_filter.text())

    def get_search_text(self):
        "return the text to search for"
        return str(self.find.currentText())

    def get_found_keydef_position(self):
        "return the position marker of the current search result"
        item = self.master.page.gui.p0list.currentItem()
        return item.text(0), item.text(1)

    def enable_search_text(self, value):
        "block or unblock entering/selecting a search text"
        self.find.setEnabled(value)

    def set_found_keydef_position(self):
        "find the next search rel=sult acoording to position marker(?)"
        for ix in range(self.master.page.gui.p0list.topLevelItemCount()):
            item = self.master.page.gui.p0list.topLevelItem(ix)
            if (item.text(0), item.text(1)) == self.master.reposition:
                self.master.page.gui.p0list.setCurrentItem(item)
                break

    def set_filter_state_text(self, state):
        "set the text for the filter button"
        self.b_filter.setText(state)

    # hulproutines t.b.v. managen bestandslocaties

    def get_selected_index(self):
        "get index of selected item"
        return self.sel.currentIndex()

    def clear_selector(self):
        "reset selector"
        self.sel.clear()

    def remove_tool(self, indx, program, program_list):
        """remove a tool from the confguration"""
        win = self.pnl.widget(indx)
        self.pnl.removeWidget(win)
        if program in program_list:
            return win.master  # keep the widget (will be re-added)
        win.close()  # lose the widget
        return None

    def add_tool(self, program, win):
        "add a tool to the configuration"
        self.add_subscreen(win)
        self.add_to_selector(program)

    def get_new_selection(self, item):
        "find the index to set the new selection to"
        return self.sel.findText(item)

    def set_selected_tool(self, selection):
        "set the new selection index"
        self.sel.setCurrentIndex(selection)

    # hulproutines t.b.v. managen tool specifieke settings

    def get_selected_panel(self):
        "return index and handle of the selected panel"
        indx = self.sel.currentIndex()
        win = self.pnl.widget(indx)
        return indx, win

    def replace_panel(self, indx, win, newwin):
        "replace a panel with a modified version"
        self.pnl.insertWidget(indx, newwin)
        self.pnl.setCurrentIndex(indx)
        self.pnl.removeWidget(win)

    def set_panel_editable(self, test_redef):
        "(re)set editability of the current panel"
        win = self.pnl.currentWidget()
        win.set_extrascreen_editable(test_redef)

    # hulproutine t.b.v. managen column properties

    def refresh_locs(self, headers):
        "apply changes in the selector for `search in column`"
        self.find_loc.clear()
        self.find_loc.addItems(headers)

    # hulpfunctie t.b.v. afsluiten: bepalen te onthouden tool

    def get_selected_text(self):
        "get text of selected item"
        return self.sel.currentText()


class Gui(qtw.QMainWindow):
    """Main GUI"""
    def __init__(self, parent=None):
        self.editor = parent
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        # self.init_gui()
        wid = 1140 if shared.LIN else 688
        hig = 594
        self.resize(wid, hig)
        self.sb = self.statusBar()
        self.menu_bar = self.menuBar()
        self.menuitems = {}  # []

    def resize_empty_screen(self, wid, hig):
        """full size not needed for a single message
        """
        self.resize(wid, hig)

    def go(self):
        "build and show the interface"
        frm = qtw.QFrame(self)
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(self.editor.book.gui)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        self.b_exit = qtw.QPushButton(self.editor.captions['C_EXIT'], self)
        self.b_exit.clicked.connect(self.editor.exit)
        self.b_exit.setDefault(True)
        hbox.addWidget(self.b_exit)
        hbox.addStretch()
        vbox.addLayout(hbox)
        frm.setLayout(vbox)
        self.setCentralWidget(frm)
        self.show()
        sys.exit(self.app.exec_())

    def set_window_title(self, title):
        "show a title in the title bar"
        self.setWindowTitle(title)

    def statusbar_message(self, message):
        "show a message in the statusbar"
        self.sb.showMessage(message)

    def setup_tabs(self):
        "add the tabbed widget to the interface"
        self.setCentralWidget(self.editor.book.gui)

    def setup_menu(self):
        """build menus and actions
        """
        self.menu_bar.clear()
        # self.menuitems = {}  # []
        for title, items in self.editor.get_menudata():
            menu = self.menu_bar.addMenu(self.editor.captions[title])
            self.menuitems[title] = menu
            for sel in items:
                if sel == -1:
                    menu.addSeparator()
                else:
                    sel, values = sel
                    callback, shortcut = values
                    if callable(callback):
                        act = self.create_menuaction(sel, callback, shortcut)
                        menu.addAction(act)
                        self.menuitems[sel] = act
                    else:
                        submenu = menu.addMenu(self.editor.captions[sel])
                        self.menuitems[sel] = submenu
                        for subsel, values in callback:
                            callback, shortcut = values
                            act = self.create_menuaction(subsel, callback, shortcut)
                            submenu.addAction(act)
                            self.menuitems[sel] = act

    def create_menuaction(self, sel, callback, shortcut):
        """return created action w. some special cases
        """
        act = qtw.QAction(self.editor.captions[sel], self)
        ## act.triggered.connect(functools.partial(callback, self))
        act.triggered.connect(callback)
        act.setShortcut(shortcut)
        if sel == 'M_READ' and not self.editor.book.page.data:
            act.setEnabled(False)
        if sel == 'M_RBLD':
            try:
                act.setEnabled(bool(int(self.editor.book.page.settings[shared.SettType.RBLD.value])))
            except KeyError:
                act.setEnabled(False)
        elif sel == 'M_SAVE':
            try:
                act.setEnabled(bool(int(self.editor.book.page.settings[shared.SettType.RDEF.value])))
            except KeyError:
                act.setEnabled(False)
        return act

    def setcaptions(self):
        "set title for menuitem or action"
        for menu, item in self.menuitems.items():
            try:
                item.setTitle(self.editor.captions[menu])
            except AttributeError:
                item.setText(self.editor.captions[menu])

    # hulproutine t.b.v. managen tool specifieke settings

    def modify_menuitem(self, caption, setting):
        "enable/disable menu option identified by caption"
        self.menuitems[caption].setEnabled(setting)
