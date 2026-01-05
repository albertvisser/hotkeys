"""HotKeys main program - gui specific code - Qt version
"""
import os
import sys
import functools
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as gui
import PyQt6.QtCore as core
from editor import shared


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

    def get_selected_panel(self):
        "return the currently selected panel"
        return self._pnl.currentWidget()

    def set_selected_panel(self, indx):
        "set the index of the panel to be selected"
        self._pnl.setCurrentIndex(indx)

    def get_panel(self, indx):
        "return handle of the indicated panel"
        # indx = self.sel.currentIndex()
        win = self._pnl.widget(indx)
        return win

    def replace_panel(self, indx, win, newwin):
        "replace a panel with a modified version"
        self._pnl.insertWidget(indx, newwin)
        self._pnl.setCurrentIndex(indx)
        self._pnl.removeWidget(win)

    def enable_widget(self, widget, state):
        "make the specified widget usable (or not)"
        widget.setEnabled(state)

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

    def get_search_col(self, cmb):
        "return the currently selected search column"
        return cmb.currentText()

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

    def remove_tool(self, indx, program, program_list):
        """remove a tool from the confguration"""
        win = self._pnl.widget(indx)
        self._pnl.removeWidget(win)
        if program in program_list:
            return win.master   # keep the widget (will be re-added)
        win.close()             # lose the widget
        return None             # explicit return to accentuate difference


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


def show_message(win, message_id='', text='', args=None):
    """toon een boodschap in een dialoog

    args is bedoeld voor als er teksten in de message moeten orden geformatteerd
    """
    text = shared.get_text(win, message_id, text, args)
    qtw.QMessageBox.information(win, shared.get_title(win), text)


def show_cancel_message(win, message_id='', text='', args=None):
    """als de vorige, maar met de mogelijkheid 'Cancel' te kiezen

    daarom retourneert deze functie ook een boolean
    """
    text = shared.get_text(win, message_id, text, args)
    ok = qtw.QMessageBox.information(win, shared.get_title(win), text,
                                     qtw.QMessageBox.StandardButton.Ok
                                     | qtw.QMessageBox.StandardButton.Cancel)
    return ok == qtw.QMessageBox.StandardButton.Ok


def ask_question(win, message_id='', text='', args=None):
    """toon een vraag in een dialoog en retourneer het antwoord (Yes als True, No als False)
    na sluiten van de dialoog
    """
    text = shared.get_text(win, message_id, text, args)
    ok = qtw.QMessageBox.question(win, shared.get_title(win), text,
                                  qtw.QMessageBox.StandardButton.Yes
                                  | qtw.QMessageBox.StandardButton.No,
                                  qtw.QMessageBox.StandardButton.Yes)
    return ok == qtw.QMessageBox.StandardButton.Yes


def ask_ync_question(win, message_id='', text='', args=None):
    """toon een vraag in een dialoog met drie mogelijkheden en retourneer het antwoord
    (Yes als (True, False), No als (False, False) en Cancel als (False, True)
    na sluiten van de dialoog
    """
    text = shared.get_text(win, message_id, text, args)
    ok = qtw.QMessageBox.question(win, shared.get_title(win), text,
                                  qtw.QMessageBox.StandardButton.Yes
                                  | qtw.QMessageBox.StandardButton.No
                                  | qtw.QMessageBox.StandardButton.Cancel)
    return ok == qtw.QMessageBox.StandardButton.Yes, ok == qtw.QMessageBox.StandardButton.Cancel


def get_textinput(win, text, prompt):
    """toon een dialoog waarin een regel tekst kan worden opgegeven en retourneer het antwoord
    (de opgegeven tekst en True bij OK) na sluiten van de dialoog
    """
    text, ok = qtw.QInputDialog.getText(win, 'Application Title', prompt, text=text)
    return text, ok == qtw.QDialog.DialogCode.Accepted


def get_choice(win, title, caption, choices, current):
    """toon een dialoog waarin een waarde gekozen kan worden uit een lijst en retourneer het
    antwoord (de geselecteerde waarde en True bij OK) na sluiten van de dialoog
    """
    return qtw.QInputDialog.getItem(win, title, caption, choices, current, editable=False)


def get_file_to_open(win, oms='', extension='', start=''):
    """toon een dialoog waarmee een file geopend kan worden om te lezen
    """
    what = shared.get_open_title(win, 'C_SELFIL', oms)
    fname, ok = qtw.QFileDialog.getOpenFileName(win, what, directory=start, filter=extension)
    return fname


def get_file_to_save(win, oms='', extension='', start=''):
    """toon een dialoog waarmee een file geopend kan worden om te schrijven
    """
    what = shared.get_open_title(win, 'C_SELFIL', oms)
    fname, ok = qtw.QFileDialog.getSaveFileName(win, what, filter=extension)
    return fname


def show_dialog(dlg):
    "show a dialog and return confirmation"
    ok = dlg.exec()
    return ok == qtw.QDialog.DialogCode.Accepted


class InitialToolDialogGui(qtw.QDialog):
    """dialog to define which tool to show on startup
    """
    def __init__(self, master, parent, title):
        self.master = master
        super().__init__(parent)
        self.setWindowTitle(title)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)

    def add_text(self, text):
        "display some text on a line"
        self.vbox.addWidget(qtw.QLabel(text, self))

    def add_radiobutton_line(self, text, checked, choices=None, indx=0):
        "display a radiobutton and optionally a combobox on a line"
        hbox = qtw.QHBoxLayout()
        rb = qtw.QRadioButton(text, self)
        rb.setChecked(checked)
        hbox.addWidget(rb)
        cmb = ''
        if choices is not None:
            cmb = qtw.QComboBox(self)
            cmb.addItems(choices)
            cmb.setCurrentIndex(indx)
            cmb.setEditable(True)
            hbox.addWidget(cmb)
        hbox.addStretch()
        self.vbox.addLayout(hbox)
        return rb, cmb

    def add_okcancel_buttons(self):
        "add action buttons to the dialog"
        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(buttonbox)
        hbox.addStretch()
        self.vbox.addLayout(hbox)

    def get_radiobutton_value(self, rb):
        "return the button state"
        return rb.isChecked()

    def get_combobox_value(self, cmb):
        "return the selected/entered text"
        return cmb.currentText()

    def accept(self):
        """send updates to parent and leave
        """
        self.master.confirm()
        super().accept()


class FilesDialogGui(qtw.QDialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, master, parent, title):
        # self.parent = parent
        self.master = master
        self.title = title
        # self.last_added = ''
        self.code_to_remove = []
        self.data_to_remove = []
        super().__init__(parent)
        self.resize(680, 400)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.setLayout(self.sizer)

    def add_explanation(self, text):
        "add instructional text at the top of the display"
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def add_captions(self, captiondefs):
        "add titles for the columns in the scrolledarea"
        hsizer = qtw.QHBoxLayout()
        for text, margin in captiondefs:
            hsizer.addSpacing(margin)
            hsizer.addWidget(qtw.QLabel(text, self),
                             alignment=core.Qt.AlignmentFlag.AlignHCenter
                             | core.Qt.AlignmentFlag.AlignVCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def add_locationbrowserarea(self):
        "add a scrollarea for showing plugin location definitions"
        pnl = qtw.QFrame(self)
        scroller = qtw.QScrollArea(self)
        scroller.setWidget(pnl)
        scroller.setWidgetResizable(True)
        self.bar = scroller.verticalScrollBar()
        self.gsizer = qtw.QGridLayout()
        self.rownum = 0
        box = qtw.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(scroller)
        return scroller

    def finish_browserarea(self):
        "stuff to do now that the area is filled up"
        # wx variant needs this to get the dimensions right

    def add_buttons(self, buttondefs):
        "add a strip with buttons to the display"
        buttonbox = qtw.QDialogButtonBox()
        for text, callback in buttondefs:
            if text == 'ok':
                btn = buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
            elif text == 'cancel':
                btn = buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
            else:
                btn = buttonbox.addButton(text, qtw.QDialogButtonBox.ButtonRole.ActionRole)
            btn.clicked.connect(callback)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def finish_display(self):
        "stuff to do now that the display is built"
        # wx variant needs this to get the dimensions right

    def add_row(self, name, path='', buttoncaption="", dialogtitle="", tooltiptext=""):
        """create a row for defining a file location
        """
        self.rownum += 1
        colnum = 0
        check = qtw.QCheckBox(name, self)
        self.gsizer.addWidget(check, self.rownum, colnum)
        colnum += 1
        browse = FileBrowseButton(self, text=path, buttoncaption=buttoncaption,
                                  dialogtitle=dialogtitle, tooltiptext=tooltiptext)
        self.gsizer.addWidget(browse, self.rownum, colnum)
        # vbar = self.scrl.verticalScrollBar()
        # vbar.setMaximum(vbar.maximum() + 52)
        self.bar.setMaximum(self.bar.maximum() + 52)
        # vbar.setValue(vbar.maximum())
        self.bar.setValue(self.bar.maximum())
        return check, browse

    def delete_row(self, rownum, check, browse):
        """remove a tool location definition row
        """
        # rownum is not used by the qt variant
        self.gsizer.removeWidget(check)
        check.close()
        self.gsizer.removeWidget(browse)
        browse.close()

    def get_browser_value(self, browser):
        "return the text entered/selected in the browser widget"
        return browser.input.text()

    def accept(self):
        """send updates to parent and leave
        """
        ok = self.master.confirm()
        if ok:
            super().accept()


class FileBrowseButton(qtw.QFrame):
    """Combination widget showing a text field and a button
    making it possible to either manually enter a filename or select one using a FileDialog
    """
    def __init__(self, parent, text="", buttoncaption="", dialogtitle="", tooltiptext=""):
        self.startdir = ''
        self.dialogtitle = dialogtitle
        if text:
            self.startdir = os.path.dirname(text)
        super().__init__(parent)
        self.setFrameStyle(qtw.QFrame.Shape.Panel | qtw.QFrame.Shadow.Raised)
        vbox = qtw.QVBoxLayout()
        box = qtw.QHBoxLayout()
        self.input = qtw.QLineEdit(text, self)
        self.input.setMinimumWidth(200)
        box.addWidget(self.input)
        button = qtw.QPushButton(buttoncaption, self, clicked=self.browse)
        box.addWidget(button)
        vbox.addLayout(box)
        self.setLayout(vbox)

    def browse(self):
        """callback for button
        """
        startdir = str(self.input.text()) or str(shared.HERE / 'plugins')
        path = qtw.QFileDialog.getOpenFileName(self, self.dialogtitle, startdir)
        if path[0]:
            self.input.setText(path[0])


class SetupDialogGui(qtw.QDialog):
    """dialoog voor het opzetten van een keydef bestand

    geeft de mogelijkheid om alvast wat instellingen vast te leggen en zorgt er
    tevens voor dat het correcte formaat gebruikt wordt
    """
    def __init__(self, master, parent, title):  # name):
        super().__init__(parent)
        self.master = master
        # self.parent = parent
        self.setWindowTitle(title)
        self.vbox = qtw.QVBoxLayout()
        self.setLayout(self.vbox)
        # self.vbox.addStretch()
        # hbox = qtw.QHBoxLayout()
        # hbox.addStretch()
        self.grid = qtw.QGridLayout()
        self.lineno = -1
        # hbox.addLayout(self.grid)
        # hbox.addStretch()
        # self.vbox.addLayout(hbox)
        self.vbox.addLayout(self.grid)

    def add_textinput_line(self, text, suggest):
        "add a line with some text and a text input box to the display"
        self.lineno += 1
        self.grid.addWidget(qtw.QLabel(text, self), self.lineno, 0, 1, 3)
        ted = qtw.QLineEdit(suggest, self)
        return ted

    def add_checkbox_line(self, text):
        "add a line with a checkbox to the display"
        self.lineno += 1
        cb = qtw.QCheckBox(text, self)
        self.grid.addWidget(cb, self.lineno, 0, 1, 4)
        return cb

    def add_filebrowse_line(self, text, suggest, buttoncaption="", dialogtitle="", tooltiptext=""):
        "add a line with some text and a file selector to the display"
        self.lineno += 1
        self.grid.addWidget(qtw.QLabel(text, self), self.lineno, 0, 1, 2)
        fbb = FileBrowseButton(self, text=suggest, buttoncaption=buttoncaption,
                               dialogtitle=dialogtitle, tooltiptext=tooltiptext)
        self.grid.addWidget(fbb, self.lineno, 2, 1, 3)
        return fbb

    def add_okcancel_buttons(self):
        "add a minimal button strip to the display"
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hbox.addWidget(buttonbox)
        hbox.addStretch()
        self.vbox.addLayout(hbox)
        # self.vbox.addStretch()

    def get_textinput_value(self, ted):
        "return the text entered in an input field"
        return ted.text()

    def get_checkbox_value(self, cb):
        "return the state of a checkbox"
        return cb.isChecked()

    def get_filebrowse_value(self, fbb):
        "return the value entered/seected in a file browser"
        return fbb.input.text()

    def accept(self):
        """re-implemented to call validation routine
        """
        ok = self.master.confirm()
        if ok:
            super().accept()


class DeleteDialogGui(qtw.QDialog):
    """dialog for deleting a tool from the collection
    """
    def __init__(self, master, parent, title):
        self.master = master
        # self.parent = parent
        super().__init__(parent)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.setLayout(self.sizer)

    def add_text_line(self, text):
        "add a line with some text to the display"
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(text, self)
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def add_checkbox_line(self, text):
        "add a line with a checkbox to the display"
        hsizer = qtw.QHBoxLayout()
        check = qtw.QCheckBox(text, self)
        hsizer.addWidget(check)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        return check

    def add_okcancel_buttons(self):
        "add a line with a minimal set of buttons to the display"
        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.sizer.addWidget(buttonbox)

    def get_checkbox_value(self, cb):
        "return the state of a checkbox"
        return cb.isChecked()

    def accept(self):
        """send settings to parent and leave
        """
        self.master.confirm()
        qtw.QDialog.accept(self)


class ColumnSettingsDialogGui(qtw.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, master, parent, title):
        # self.parent = parent
        self.master = master
        # self.initializing = True  # als deze tbv add_row is dan naar main
        super().__init__(parent)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.setLayout(self.sizer)
        # self.initializing = False

    def add_explanation(self, text):
        "add instructional text at the top of the display"
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def add_captions(self, captiondefs):
        "add titles for the columns in the scrolledarea"
        hsizer = qtw.QHBoxLayout()
        for text, margin in captiondefs:
            hsizer.addSpacing(margin)
            hsizer.addWidget(qtw.QLabel(text, self),
                             alignment=core.Qt.AlignmentFlag.AlignHCenter
                             | core.Qt.AlignmentFlag.AlignVCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def add_columndefs_area(self):
        "add a scrollarea for showing column definitions"
        pnl = qtw.QFrame(self)
        scroller = qtw.QScrollArea(self)
        scroller.setWidget(pnl)
        scroller.setAlignment(core.Qt.AlignmentFlag.AlignBottom)
        scroller.setWidgetResizable(True)
        self.bar = scroller.verticalScrollBar()
        self.gsizer = qtw.QGridLayout()
        rownum = 0
        self.rownum = rownum
        box = qtw.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(scroller)
        return scroller  # misschien gsizer ook teruggeven

    def add_buttons(self, buttondefs):
        "add a strip with buttons to the display"
        buttonbox = qtw.QDialogButtonBox()
        for text, callback in buttondefs:
            if text == 'ok':
                btn = buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
            elif text == 'cancel':
                btn = buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
            else:
                btn = buttonbox.addButton(text, qtw.QDialogButtonBox.ButtonRole.ActionRole)
            btn.clicked.connect(callback)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def finalize_columndefs_area(self, scroller):
        "stuff to do when the area is filled up"
        # wx variant needs this to get the dimensions right

    def add_checkbox_to_line(self, row, col, text, width, before, after):
        "add a checkbox to the screen line"
        # if col == 0:
        #     self.rowsizer = qtw.QHBoxLayout()
        hsizer = qtw.QHBoxLayout()
        if before:
            hsizer.addSpacing(before)
        cb = qtw.QCheckBox(self)
        if width:
            cb.setFixedWidth(width)
        hsizer.addWidget(cb)
        if after:
            hsizer.addSpacing(after)
        # self.rowsizer.addLayout(hsizer)  # , rownum)
        self.gsizer.addLayout(hsizer, row, col)
        return cb

    def add_combobox_to_line(self, row, col, values, selected):
        "add a combobox to the screen line"
        cmb = qtw.QComboBox(self)
        cmb.addItems(values)
        cmb.setEditable(True)
        cmb.editTextChanged.connect(self.on_text_changed)
        if selected:
            cmb.setCurrentIndex(selected - 1)
        # else:
        #     cmb.clearEditText()
        # self.rowsizer.addWidget(cmb)  #, rownum)
        self.gsizer.addWidget(cmb, row, col)
        return cmb

    def add_spinbox_to_line(self, row, col, value, range, width, margins):
        "add a spinbox to the screen line"
        minval, maxval = range
        before, after = margins
        hsizer = qtw.QHBoxLayout()
        if before:
            hsizer.addSpacing(before)
        sb = qtw.QSpinBox(self)
        if minval:
            sb.setMinimum(minval)
        sb.setMaximum(maxval)
        if value:
            sb.setValue(value)
        sb.setFixedWidth(width)
        hsizer.addWidget(sb)
        if after:
            hsizer.addSpacing(after)
        else:
            hsizer.addStretch()
        # self.rowsizer.addLayout(hsizer)  # , rownum)
        self.gsizer.addLayout(hsizer, row, col)
        return sb

    def finalize_line(self, *args):
        "stuff to do now that the line is built"
        # wx variant needs this to get the dimensions right
        # self.gsizer.addLayout(self.rowsizer)
        self.bar.setMaximum(self.bar.maximum() + 62)
        self.bar.setValue(self.bar.maximum())

    def adapt_column_index(self, removed_widget, current_widget):
        """maak alle kolomnummers die groter zijn dan het net verwijderde
        1 kleiner
        """
        if current_widget.value() > removed_widget.value():
            current_widget.setValue(current_widget.value() - 1)

    def delete_row(self, rownum, check, widgets):
        """remove a column settings row
        """
        self.rownum -= 1
        # w_name, w_width, w_colno, w_flag, _ = self.data[rownum]
        for widget in [check] + widgets[:4]:
            self.gsizer.removeWidget(widget)
            widget.close()
        self.gsizer.removeItem(self.gsizer.itemAt(rownum))

    def on_text_changed(self, text):
        "adjust column width based on length of column title"
        for name, width, *ignore_the_rest in self.master.data:
            column_text = name.currentText()
            if column_text == text:
                width.setValue(10 * len(text))
                break

    def get_checkbox_value(self, cb):
        "return the state of a checkbox"
        return cb.isChecked()

    def get_combobox_value(self, cmb):
        "return the state of a combobox"
        return cmb.currentText()

    def get_spinbox_value(self, sb):
        "return the state of a spinbox"
        return sb.value()

    def accept(self):
        """save the changed settings and leave
        """
        ok = self.master.confirm()
        if ok:
            super().accept()


class NewColumnsDialogGui(qtw.QDialog):
    """dialoog voor aanmaken nieuwe kolom-ids
    """
    def __init__(self, master, parent, title):
        # self.parent = parent
        self.master = master
        self.initializing = True
        super().__init__(parent)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.gsizer = qtw.QGridLayout()
        self.sizer.addLayout(self.gsizer)
        self.setLayout(self.sizer)
        self.initializing = False

    def add_explanation(self, text):
        "add instructional text at the top of the display"
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(qtw.QLabel(text, self))
        self.sizer.addLayout(hsizer)

    def add_titles(self, titles):
        """maak een kop voor de id en een kop voor elke taal die ondersteund wordt
        """
        row = 0
        col = -1
        for name in titles:
            col += 1
            self.gsizer.addWidget(qtw.QLabel(name, self), row, col)

    def add_text_entry(self, text, row, col, enabled):
        "add a text entry field to a specfied location in the display grid"
        entry = qtw.QLineEdit(text, self)
        entry.setEnabled(enabled)
        self.gsizer.addWidget(entry, row, col)
        return entry

    def add_okcancel_buttons(self):
        "add a minimal button strip to the display"
        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def get_textentry_value(self, ted):
        "return the text entered in an input field"
        return ted.text()

    def accept(self):
        """save the changed settings and leave
        """
        ok = self.master.confirm()
        if ok:
            super().accept()


class ExtraSettingsDialogGui(qtw.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, master, parent, title):
        # self.parent = parent
        self.master = master
        super().__init__(parent)
        ## self.resize(680, 400)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.setLayout(self.sizer)

    def start_block(self):
        "start a new block of input items"
        pnl = qtw.QFrame()
        vsizer = qtw.QVBoxLayout()
        pnl.setLayout(vsizer)
        pnl.setFrameStyle(qtw.QFrame.Shape.Box | qtw.QFrame.Shadow.Raised)
        self.sizer.addWidget(pnl)
        return vsizer

    def add_textinput_line(self, vsizer, labeltext, inputsuggestion):
        "add a line with some text and an input field to the block"
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(qtw.QLabel(labeltext, self))
        field = qtw.QLineEdit(inputsuggestion, self)
        hsizer.addWidget(field)
        vsizer.addLayout(hsizer)
        return field

    def add_checkbox_line(self, vsizer, caption, value):
        "add a line with a checkbox to the block and return the checkbox"
        hsizer = qtw.QHBoxLayout()
        cb = qtw.QCheckBox(caption, self)
        cb.setChecked(value)
        hsizer.addWidget(cb)
        vsizer.addLayout(hsizer)
        return cb

    def add_text_line(self, vsizer, text):
        "add a line with sone text (centered) to the block"
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(qtw.QLabel(text, self))
        hsizer.addStretch()
        vsizer.addLayout(hsizer)

    def add_titles(self, vsizer, headerdefs):
        "add a line with headers for the data columns to the block"
        hsizer = qtw.QHBoxLayout()
        for margin, text in headerdefs:
            hsizer.addSpacing(margin)
            hsizer.addWidget(qtw.QLabel(text, self), alignment=core.Qt.AlignmentFlag.AlignHCenter)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)

    def add_inputarea(self, vsizer):
        "add a scrollarea for the settings definitions to the block"
        pnl = qtw.QFrame(self)
        scrl = qtw.QScrollArea(self)
        scrl.setWidget(pnl)
        scrl.setWidgetResizable(True)
        self.bar = scrl.verticalScrollBar()
        self.gsizer = qtw.QGridLayout()
        rownum = 0
        self.rownum = rownum
        pnl.setLayout(self.gsizer)
        pnl.setFrameStyle(qtw.QFrame.Shape.Box)
        scrl.ensureVisible(0, 0)
        vsizer.addWidget(scrl)
        return scrl

    def add_buttons(self, vsizer, buttondefs):
        "add a line with action buttons to the block"
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        for text, callback in buttondefs:
            btn = qtw.QPushButton(text, self)
            btn.clicked.connect(callback)
            hsizer.addWidget(btn)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)

    def add_okcancel_buttons(self):
        "add a minimal button strip to the bottom of the display"
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def add_row(self, name, value, desc):
        """add a row for defining a setting (name, value)
        """
        self.rownum += 1
        colnum = 0
        check = qtw.QCheckBox(self)
        self.gsizer.addWidget(check, self.rownum, colnum)
        # self.checks.append(check)
        colnum += 1
        w_name = qtw.QLineEdit(name, self)
        w_name.setFixedWidth(88)
        if name:
            w_name.setReadOnly(True)
        ## w_name.setMaxLength(50)
        self.gsizer.addWidget(w_name, self.rownum, colnum)
        colnum += 1
        w_value = qtw.QLineEdit(value, self)
        self.gsizer.addWidget(w_value, self.rownum, colnum)
        self.rownum += 1
        w_desc = qtw.QLineEdit(desc, self)
        self.gsizer.addWidget(w_desc, self.rownum, colnum)
        # self.data.append((w_name, w_value, w_desc))
        self.bar.setMaximum(self.bar.maximum() + 62)
        self.bar.setValue(self.bar.maximum())
        return check, w_name, w_value, w_desc

    def delete_row(self, rowindex, fields):
        """delete a setting definition row
        """
        # rowindex is for api-compliance
        for widget in fields:
            self.gsizer.removeWidget(widget)
            widget.close()

    def get_checkbox_value(self, cb):
        "return the state of the given checkbox"
        return cb.isChecked()

    def get_textinput_value(self, ted):
        "return the text entered in the given input field"
        return ted.text()

    def set_checkbox_value(self, cb, value):
        "set the state of the given checkbox"
        cb.setChecked(value)

    def accept(self):
        """update settings and leave
        """
        ok = self.master.confirm()
        if ok:
            super().accept()


class EntryDialogGui(qtw.QDialog):
    """Dialog for Manual Entry
    """
    def __init__(self, master, parent, title):
        # self.parent = parent
        self.master = master
        super().__init__(parent)
        self.resize(680, 400)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.setLayout(self.sizer)

    def add_table_to_display(self, headerdefs):
        "add a table containing the data to edit to the display"
        hsizer = qtw.QHBoxLayout()
        p0list = qtw.QTableWidget(self)

        p0list.setColumnCount(len(headerdefs))
        p0list.setHorizontalHeaderLabels([x[0] for x in headerdefs])
        p0hdr = p0list.horizontalHeader()
        for indx, wid in enumerate([x[1] for x in headerdefs]):
            p0hdr.resizeSection(indx, wid)

        hsizer.addWidget(p0list)
        self.sizer.addLayout(hsizer)
        return p0list

    def add_buttons(self, buttondefs):
        "add a strip with buttons to the display"
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        buttonbox = qtw.QDialogButtonBox()
        for text, callback in buttondefs:
            if text == 'ok':
                btn = buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Save)
            elif text == 'cancel':
                btn = buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
            else:
                btn = buttonbox.addButton(text, qtw.QDialogButtonBox.ButtonRole.ActionRole)
            btn.clicked.connect(callback)
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def add_row(self, p0list, newrow, values):
        "add a row to the table"
        num_rows = p0list.rowCount()
        p0list.insertRow(newrow)
        for i, element in enumerate(values):
            new_item = qtw.QTableWidgetItem()
            new_item.setText(element)
            p0list.setItem(num_rows, i, new_item)
        p0list.scrollToBottom()

    # voorlopig nog even als gui methode
    def delete_key(self, p0list):
        "remove selected line(s) from the grid"
        selected_rows = []
        for item in p0list.selectedRanges():
            for increment in range(item.rowCount()):
                selected_rows.append(item.topRow() + increment)
        for row in reversed(sorted(selected_rows)):
            p0list.removeRow(row)

    def get_table_columns(self, p0list):
        "return the number of columns in the table"
        return p0list.columnCount()

    def get_tableitem_value(self, p0list, rowid, colid):
        "return the value entered in a table cell"
        return p0list.item(rowid, colid).text()

    def accept(self):
        """send updates to parent and leave
        """
        self.master.confirm()
        super().accept()


class CompleteDialogGui(qtw.QDialog):
    """Model dialog for entering / completing command descriptions
    """
    def __init__(self, master, parent, title):
        # self.parent = parent
        self.master = master
        super().__init__(parent)
        self.resize(1100, 700)
        self.setWindowTitle(title)
        self.sizer = qtw.QVBoxLayout()
        self.setLayout(self.sizer)

    def add_table_to_display(self, headerdefs):
        "add a teble containing the data to be edited to the display"
        hsizer = qtw.QHBoxLayout()
        p0list = qtw.QTableWidget(len(self.cmds), 3, self)
        p0list.setHorizontalHeaderLabels([x[0] for x in headerdefs])
        hdr = p0list.horizontalHeader()
        for width in [x[1] for x in headerdefs]:
            p0list.setColumnWidth(0, width)
        hdr.setStretchLastSection(True)
        hsizer.addWidget(self.p0list)
        self.sizer.addLayout(hsizer)
        return p0list

    def add_row(self, p0list, row, key, desc, olddesc):
        "vul de tabel met in te voeren gegevens"
        keyitem = qtw.QTableWidgetItem()
        keyitem.setText(key)
        p0list.setItem(row, 0, keyitem)
        descitem = qtw.QTableWidgetItem()
        descitem.setText(desc)
        descitem.setFlags(descitem.flags() ^ core.Qt.ItemFlag.ItemIsEditable)
        p0list.setItem(row, 1, descitem)
        olditem = qtw.QTableWidgetItem()
        olditem.setText(olddesc)
        olditem.setFlags(olditem.flags() ^ core.Qt.ItemFlag.ItemIsEditable)
        p0list.setItem(row, 2, olditem)
        return keyitem, descitem, olditem

    def add_okcancel_buttons(self):
        "add a minimal button strip to the display"
        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Save)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

    def set_focus_to_list(self, p0list):
        """set "cursor" on the first editable field
        """
        p0list.setCurrentCell(0, 1)  # self.p0list.setCurrentItem(itemAt(0,1))

    def accept(self):
        """confirm changes
        """
        self.master.confirm()
        qtw.QDialog.accept(self)
