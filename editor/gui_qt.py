"""HotKeys main program - gui specific code - Qt version
"""
import sys
import functools
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
from editor import shared


class SingleDataInterface(qtw.QFrame):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    definieert feitelijk een "custom widget"
    """
    def __init__(self, parent, master):
        super().__init__(parent)
        self.parent = parent  # .parent()
        self.master = master
        self._savestates = (False, False)
        # self.fieldhandler = FieldHandler(self)
        self._sizer = qtw.QVBoxLayout()

    def setup_empty_screen(self, nodata, title):
        """build a subscreen with only a message
        """
        # self._sizer = qtw.QVBoxLayout()
        self.title = title
        hsizer = qtw.QHBoxLayout()
        self._sizer.addLayout(hsizer)
        hsizer.addStretch()
        hsizer.addWidget(qtw.QLabel(nodata, self))
        hsizer.addStretch()

    def setup_list(self, colheaders, colwidths, callback):
        """add the list widget to the interface
        """
        sizer1 = qtw.QHBoxLayout()
        p0list = qtw.QTreeWidget(self)
        sizer1.addWidget(p0list)
        self._sizer.addLayout(sizer1)
        p0list.setHeaderLabels(colheaders)
        p0list.setAlternatingRowColors(True)
        p0list.currentItemChanged.connect(callback)
        hdr = p0list.header()
        hdr.setSectionsClickable(True)
        for indx, col in enumerate(colwidths):
            hdr.resizeSection(indx, col)
        hdr.setStretchLastSection(True)
        p0list.setSortingEnabled(True)
        return p0list

    def start_extrapanel(self, frameheight):
        "start a new area for screen widgets"
        self._frm = qtw.QFrame(self)
        # self._frm.setMaximumHeight(frameheight)
        # self._frm.setMinimumHeight(frameheight)
        # self._frm.resize(-1, frameheight)
        self._frm.setFixedHeight(frameheight)
        self._sizer.addWidget(self._frm)
        vbox = qtw.QVBoxLayout()
        self._frm.setLayout(vbox)
        # self._sizer.addWidget(self._frm)
        # vbox.addWidget(self._frm)
        # self._sizer.addLayout(vbox)
        return vbox

    def start_line(self, vbox):
        "start a new line of widgets in the given screen"
        hbox = qtw.QHBoxLayout()
        vbox.addLayout(hbox)
        return hbox

    def add_label_to_line(self, hbox, text, **kwargs):
        "add the given text to the given screen line"
        fld = qtw.QLabel(text, self._frm)
        hbox.addWidget(fld)
        return fld

    def add_textfield_to_line(self, hbox, width=None, callback=None, **kwargs):
        "add a field to enter text on the given screen line"
        fld = qtw.QLineEdit(self._frm)
        if width:
            fld.setMaximumWidth(width)
        if callback:
            fld.textChanged.connect(callback)
        hbox.addWidget(fld)
        return fld

    def add_combobox_to_line(self, hbox, items, width=None, **kwargs):
        "add a combobox with the given caption and a standard callback"
        cb = qtw.QComboBox(self._frm)
        if width:
            cb.setMaximumWidth(width)
        cb.addItems(items)
        cb.currentTextChanged[str].connect(functools.partial(self.master.on_combobox, cb, str))
        hbox.addWidget(cb)
        return cb

    def add_checkbox_to_line(self, hbox, text):
        "add a checkbox with the given caption and a standard callback"
        cb = qtw.QCheckBox(text, self._frm)
        cb.stateChanged.connect(functools.partial(self.master.on_checkbox, cb))
        hbox.addWidget(cb)
        return cb

    def add_separator_to_line(self, hbox):
        "separate the keydef from the definition"
        hbox.addStretch()

    def add_button_to_line(self, hbox, text, callback):
        "add a button with the given text and callback"
        btn = qtw.QPushButton(text, self._frm)
        btn.setEnabled(False)
        btn.clicked.connect(callback)
        hbox.addWidget(btn)
        return btn

    def add_descfield_to_line(self, hbox):  # , frameheight):
        "add a text field for the description"
        fld = qtw.QTextEdit(self._frm)
        # fld.setMaximumHeight(frameheight)
        # self._frm.setMinimumHeight(frameheight)
        fld.setReadOnly(True)
        hbox.addWidget(fld, 1)   # proportie wordt gebruikt om de eventuele extra kolom in te perken
        return fld

    def set_extrapanel_editable(self, screenfields, buttons, switch):
        """open up fields in extra screen when applicable
        """
        for widget in screenfields:
            widget.setEnabled(switch)
        if switch:
            state_s, state_d = self._savestates
        else:
            self._savestates = (buttons[0].isEnabled(), buttons[1].isEnabled())
            state_s, state_d = False, False
        buttons[0].setEnabled(state_s)
        buttons[1].setEnabled(state_d)

    def finalize_screen(self):
        "last actions to add the screen to the display"
        self.setLayout(self._sizer)

    def resize_if_necessary(self):
        """to be called on changing the language
        """
        # for compatibility: no actions needed here

    def on_item_selected(self, newitem, olditem):
        """callback on selection of an item
        """
        if newitem and self.master.has_extrapanel:
            self.master.process_changed_selection(newitem, olditem)

    def set_focus_to(self, widget):
        "set the field to start inputting data"
        widget.setFocus()

    def update_columns(self, p0list, oldcount, newcount):
        "delete and insert columns"
        p0list.setColumnCount(newcount)

    def refresh_headers(self, p0list, column_info):
        "apply changes in the column headers"
        p0list.setColumnCount(len(column_info))
        p0list.setHeaderLabels([x[0] for x in column_info])
        hdr = p0list.header()
        hdr.setSectionsClickable(True)
        for indx, col in enumerate(column_info):
            hdr.resizeSection(indx, col[1])
        hdr.setStretchLastSection(True)

    def set_title(self, title):
        "set screen title"
        self.master.parent.parent.gui.setWindowTitle(title)

    def clear_list(self, p0list):
        "reset listcontrol"
        p0list.clear()

    def build_listitem(self, key):
        "create a new item for the list"
        new_item = qtw.QTreeWidgetItem()
        new_item.setData(0, core.Qt.ItemDataRole.UserRole, key)
        return new_item

    def set_listitemtext(self, item, indx, value):
        "set the text for a list item"
        item.setText(indx, value)
        item.setToolTip(indx, value)
        # return item

    def add_listitem(self, p0list, new_item):
        "add an item to the list"
        p0list.addTopLevelItem(new_item)

    def set_listselection(self, p0list, pos):
        "highlight the selected item in the list"
        p0list.setCurrentItem(p0list.topLevelItem(pos))

    def getfirstitem(self, p0list):
        "return first item in list"
        return p0list.topLevelItem(0)

    def get_listitem_at_position(self, p0list, pos):
        "return the index of a given keydef entry"
        return p0list.topLevelItem(pos)

    def get_itemdata(self, item):
        "return the data associated with a listitem"
        return item.data(0, core.Qt.ItemDataRole.UserRole)

    def get_listbox_selection(self, p0list):
        "return the currently selected keydef and its position in the list"
        item = p0list.currentItem()
        return item, p0list.indexOfTopLevelItem(item)

    def get_listitem_position(self, p0list, item):
        "return the index of a given keydef entry"
        return p0list.indexOfTopLevelItem(item)

    def get_widget_text(self, ted, text):
        "return the text entered in a textfield"
        hlp = ted.text()
        if text != hlp:
            text = hlp
        return text

    def set_textfield_value(self, txt, value):
        "set the text for a textfield (LineEdit, ComboBox of TextEdit)"
        txt.setText(value)

    def enable_button(self, button, state):
        "make button accessible"
        button.setEnabled(state)

    def get_choice_value(self, cb, dummy, text):
        """return the value chosen in a combobox (and the widget itself)

        this method is used from within the partialed onchange callback
        """
        return cb, text

    def get_combobox_value(self, cb):
        "return the text entered/selected in a combobox"
        return cb.currentText()

    def init_combobox(self, cb, choices=None):
        "initialize combobox to a set of new values"
        cb.clear()
        if choices is not None:
            cb.addItems(choices)

    def set_combobox_string(self, cmb, value, valuelist):
        "set the selection for a combobox"
        try:
            ix = valuelist.index(value)
        except ValueError:
            return
        cmb.setCurrentIndex(ix)

    def set_label_text(self, lbl, value):
        "set the text for a label / static text"
        lbl.setText(value)

    def get_check_value(self, cb, state):
        """return the state set in a checkbox (and the widget itself)

        this method is used from within the partialed onchange callback
        """
        return cb, state

    def get_checkbox_state(self, cb):
        "return the state set in a checkbox (without the widget)"
        return cb.isChecked()

    def set_checkbox_state(self, cb, state):
        "set the state for a checkbox"
        cb.setChecked(state)


class TabbedInterface(qtw.QFrame):
    """Als QTabwidget, maar met selector in plaats van tabs
    """
    def __init__(self, parent, master):
        super().__init__(parent)
        self.parent = parent
        self.master = master

    def setup_selector(self, callback):
        "create the selector"
        sel = qtw.QComboBox(self)
        sel.currentIndexChanged.connect(callback)
        self._pnl = qtw.QStackedWidget(self)
        return sel

    def add_subscreen(self, win):
        "add a screen to the tabbed widget"
        self._pnl.addWidget(win)

    def add_to_selector(self, selector, text):
        "add an option to the selector"
        selector.addItem(text)

    def start_display(self):
        "build the screen container"
        vbox = qtw.QVBoxLayout()
        return vbox

    def start_line(self, vbox):
        "add a line to the screen container"
        hbox = qtw.QHBoxLayout()
        vbox.addLayout(hbox)
        return hbox

    def add_margin_to_line(self, hbox):
        "add the fixed margin"
        hbox.addSpacing(10)

    def add_text_to_line(self, hbox, text=""):
        "add a fixed text"
        text = qtw.QLabel(text, self)
        hbox.addWidget(text)
        return text

    def add_selector_to_line(self, hbox, widget):
        "add the book selector to the line"
        hbox.addWidget(widget)

    def add_combobox_to_line(self, hbox, minwidth=0, editable=False, callback=None):
        "add a combobox selector"
        cmb = qtw.QComboBox(self)
        if minwidth > 0:
            cmb.setMinimumContentsLength(minwidth)
        cmb.setEditable(editable)
        if callback:
            cmb.editTextChanged.connect(callback)
        hbox.addWidget(cmb)
        return cmb

    def add_separator_to_line(self, hbox):
        "separate the selector from the search-related widgets"
        hbox.addStretch()

    def add_button_to_line(self, hbox, text, callback, enabled):
        "add a button with the given text and callback "
        btn = qtw.QPushButton(text, self)
        btn.clicked.connect(callback)
        btn.setEnabled(enabled)
        hbox.addWidget(btn)
        return btn

    def add_list_to_line(self, hbox):
        "add the list with keydefs to the display"
        hbox.addWidget(self._pnl)

    def finalize_display(self, vbox):
        "realize the layout"
        self.setLayout(vbox)

    def setcaption(self, widget, caption):
        "set the given widget's caption (this is intended for label fields)"
        widget.setText(caption)

    def on_pagechange(self, pagenum):  # after_changing_page(self, event):
        """callback for change in tool page selector
        """
        self.master.on_page_changed(pagenum)

    # used by on_page_changed
    def get_panel(self):
        "return the currently selected panel's index"
        return self._pnl.currentWidget()

    # def get_selected_tool(self, selector):
    #     "return the currently selected panel's name"
    #     return selector.currentText()

    def get_selected_panel(self, indx):
        "return handle of the selected (indicated) panel"
        # indx = self.sel.currentIndex()
        win = self._pnl.widget(indx)
        return win

    def set_selected_panel(self, indx):
        "set the index of the panel to be selected"
        self._pnl.setCurrentIndex(indx)

    def replace_panel(self, indx, win, newwin):
        "replace a panel with a modified version"
        self._pnl.insertWidget(indx, newwin)
        self._pnl.setCurrentIndex(indx)
        self._pnl.removeWidget(win)

    # def set_panel_editable(self, test_redef):
    #     "(re)set editability of the current panel"
    #     win = self._pnl.currentWidget()
    #     win.set_extrascreen_editable(test_redef)

    def enable_widget(self, widget, state):
        "make the specified widget usable (or not)"
        widget.setEnabled(state)

    # def update_search_checkbox_items(self, cmb, items):
    def refresh_combobox(self, cmb, items=None):
        "refill the values for the given checkbox and select the last one"
        cmb.clear()
        if items:
            cmb.addItems(items)
            cmb.setCurrentText(items[-1])

    def get_combobox_value(self, cmb):
        "return the given combobox's value"
        return cmb.currentText()

    def set_combobox_text(self, cmb, text):
        "set the text for the given combobox"
        cmb.setEditText(text)
        if text:
            cmb.setEnabled(True)

    def get_combobox_index(self, cmb):
        "get index of selected item"
        return cmb.currentIndex()

    def on_textchange(self, text):
        """callback for change in search text selector
        """
        self.master.on_text_changed(text)

    # used by on_text_changed
    def get_search_col(self, cmb):
        "return the currently selected search column"
        return cmb.currentText()

    # def get_new_selection(self, item):
    def get_combobox_index_for_item(self, cb, item):
        "find the index to set the new selection to"
        # return self.sel.findText(item)
        return cb.findText(item)

    def set_combobox_index(self, selector, selection):
        "set the new selection index"
        selector.setCurrentIndex(selection)

    # used by filter
    def get_button_text(self, button):
        "return the current text of the filter button"
        return button.text()

    def set_button_text(self, button, state):
        "set the text for the filter button"
        button.setText(state)

    def find_items(self, p0list, zoekcol, text):
        "return the items that contain the text to search for"
        return p0list.findItems(text, core.Qt.MatchFlag.MatchContains, zoekcol)

    def set_selected_keydef_item(self, p0list, items, index):
        "select a search result in the list"
        item = items[index]
        p0list.setCurrentItem(item)
        p0list.scrollToItem(item)

    # def get_search_text(self):
    #     "return the text to search for"
    #     return self.find.currentText()

    def get_found_keydef_position(self, p0list):
        "return the position marker of the current search result"
        item = p0list.currentItem()
        return item.text(0), item.text(1)

    def set_found_keydef_position(self, p0list, pos):
        "find the next search rel=sult acoording to position marker(?)"
        for ix in range(p0list.topLevelItemCount()):
            item = p0list.topLevelItem(ix)
            if (item.text(0), item.text(1)) == pos:
                p0list.setCurrentItem(item)
                break

    # def clear_selector(self):
    #     "reset selector"
    #     self.sel.clear()

    def remove_tool(self, indx, program, program_list):
        """remove a tool from the confguration"""
        win = self._pnl.widget(indx)
        self._pnl.removeWidget(win)
        if program in program_list:
            return win.master   # keep the widget (will be re-added)
        win.close()             # lose the widget
        return None             # explicit return to accentuate difference

    # hulproutine t.b.v. managen column properties

    # def refresh_locs(self, headers):
    #     "apply changes in the selector for `search in column`"
    #     self.find_loc.clear()
    #     self.find_loc.addItems(headers)

    # hulpfunctie t.b.v. afsluiten: bepalen te onthouden tool

    # def get_selected_text(self):
    #     "get text of selected item"
    #     return self.sel.currentText()


class Gui(qtw.QMainWindow):
    """Main GUI"""
    def __init__(self, master):
        self.editor = master
        self.app = qtw.QApplication(sys.argv)
        super().__init__()
        # self.init_gui()
        wid = 1140 if shared.LIN else 688
        hig = 832
        self.resize(wid, hig)
        self.sb = self.statusBar()
        self.menu_bar = self.menuBar()
        self.menuitems = {}  # []

    def start_display(self):
        "setup the screen container"
        self._frm = qtw.QFrame(self)
        vbox = qtw.QVBoxLayout()
        return vbox

    def add_choicebook_to_display(self, vbox, bookgui):
        "main portion of the interface"
        vbox.addWidget(bookgui)

    def add_exitbutton_to_display(self, vbox, buttondef):
        "a single button at the bottom"
        text, callback = buttondef
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton(text, self)
        btn.clicked.connect(callback)
        btn.setDefault(True)
        hbox.addWidget(btn)
        hbox.addStretch()
        vbox.addLayout(hbox)
        return btn

    def go(self, vbox):
        "finish and show the interface"
        self._frm.setLayout(vbox)
        self.setCentralWidget(self._frm)
        self.show()
        sys.exit(self.app.exec())

    def set_window_title(self, title):
        "show a title in the title bar"
        self.setWindowTitle(title)

    def statusbar_message(self, message):
        "show a message in the statusbar"
        self.sb.showMessage(message)

    def setup_menu(self, minimal=False):
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
                            self.menuitems[subsel] = act
        if minimal:
            self.menuitems['M_TOOL'].setEnabled(False)

    def create_menuaction(self, sel, callback, shortcut):
        """return created action w. some special cases
        """
        act = gui.QAction(self.editor.captions[sel], self)
        ## act.triggered.connect(functools.partial(callback, self))
        act.triggered.connect(callback)
        act.setShortcut(shortcut)
        if sel == 'M_READ' and not self.editor.book.page.data:
            act.setEnabled(False)
        if sel == 'M_RBLD':
            # act.setEnabled(bool(int(self.editor.book.page.settings.get(shared.SettType.RBLD.value,
            #                                                            "0"))))
            # #1050 is bedoeld om dit te vereenvoudigen tot
            act.setEnabled(self.editor.book.page.settings.get(shared.SettType.RBLD.value, False))
        elif sel == 'M_SAVE':
            # act.setEnabled(bool(int(self.editor.book.page.settings.get(shared.SettType.RDEF.value,
            #                                                            "0"))))
            # #1050 is bedoeld om dit te vereenvoudigen tot
            act.setEnabled(self.editor.book.page.settings.get(shared.SettType.RDEF.value, False))
        return act

    def update_menutitles(self):
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
