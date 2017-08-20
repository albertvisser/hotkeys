# -*- coding: UTF-8 -*-
"""hotkeys.py - PyQt5 version

    main gui (choicebook)
    importeert de verschillende applicatiemodules
    hierin wordt het menu gedefinieerd en de functies die daarbij horen
    het idee is dat de menuopties wanneer nodig uitgegrijsd zijn en dat
        in de routines wordt uitgevraagd wat te doen bij welke applicatie
    voor wat betreft de instellingen:
        taalkeuze: op dit niveau
        paden: op applicatie niveau (in betreffende csv file)
"""
from __future__ import print_function
import os
import sys
## import shutil
import string
import functools
import importlib
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
import PyQt5.QtCore as core

import editor.hotkeys_constants as hkc
CONF = 'editor.hotkey_config'  # default configuration file
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# shared (menu) functions


def show_message(win, message_id='', text=''):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id>
    """
    if message_id:
        text = win.captions[message_id]
    elif not text:
        text = win.captions['I_NOMSG']
    qtw.QMessageBox.information(win, win.title, text)
    return


def ask_question(win, message_id='', text=''):
    """toon de vraag geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    (Yes als True, No als False) na sluiten van de dialoog
    """
    if message_id:
        text = win.captions[message_id]
    elif not text:
        text = win.captions['I_NOMSG']
    ok = qtw.QMessageBox.question(win, win.title, text,
                                  qtw.QMessageBox.Yes | qtw.QMessageBox.No,
                                  qtw.QMessageBox.Yes)
    return ok == qtw.QMessageBox.Yes


def m_read(self):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    if not self.page.settings:
        show_message(self, 'I_ADDSET')
        return
    if not self.page.modified:
        if not ask_question(self, 'Q_NOCHG'):
            return
    self.page.readkeys()
    self.page.populate_list()


def m_save(self):
    """(menu) callback voor het terugschrijven van de hotkeys

    vraagt eerst of het ok is om de hotkeys weg te schrijven
    vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
    """
    if not self.page.modified:
        if not ask_question(self, 'Q_NOCHG'):
            return
    try:
        self.page.savekeys()
    except AttributeError:
        show_message(self, 'I_DEFSAV')
        return
    show_message(self, 'I_RSTRT')


def m_loc(self):
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    # self.ini["plugins"] bevat de lijst met tools en csv locaties
    current_programs = [x for x, y in self.ini["plugins"]]
    current_paths = [y for x, y in self.ini["plugins"]]
    ok = FilesDialog(self).exec_()
    if ok == qtw.QDialog.Accepted:
        selection = self.book.sel.currentIndex()
        hkc.modify_settings(self.ini)

        # update the screen(s)
        # clear the selector and the stackedwidget while pairing up programs and windows
        # that need to be kept or replaced
        hlpdict = {}
        self.book.sel.clear()
        current_items = reversed([(x, y) for x, y in enumerate(current_programs)])
        new_programs = [x for x, y in self.ini["plugins"]]
        new_paths = [y for x, y in self.ini["plugins"]]
        for indx, program in current_items:  # we need to do this in reverse
            win = self.book.pnl.widget(indx)
            self.book.pnl.removeWidget(win)
            if program in new_programs:
                hlpdict[program] = win  # keep the widget
            else:
                win.close()  # lose the widget
        # add new ones, modify existing or leave them alone
        for indx, program in enumerate(new_programs):
            if program in current_programs:
                # compare the new and the existing path
                old_loc = current_paths[current_programs.index(program)]
                new_loc = new_paths[new_programs.index(program)]
                if new_loc == old_loc:  # unchanged
                    win = hlpdict[program]
                else:  # take data from different location
                    win = HotkeyPanel(self.book, new_loc)
            else:  # new entry
                win = HotkeyPanel(self.book, new_paths[indx])
            self.book.sel.addItem(program)
            self.book.pnl.addWidget(win)
        if self.last_added:
            selection = self.book.sel.findText(self.last_added)
        if selection > len(self.ini['plugins']) - 1:
            selection -= 1
        self.book.sel.setCurrentIndex(selection)


def m_rebuild(self):
    """rebuild csv data from (updated) settings
    """
    if not self.page.settings:
        show_message(self, 'I_ADDSET')
        return
    try:
        newdata = self.page._keys.buildcsv(self)
    except AttributeError:
        ## raise
        show_message(self, 'I_DEFRBLD')
        return
    if newdata[0]:
        self.page.data = newdata[0]
        self.page.otherstuff = newdata[1]
        hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                     self.page.data, self.ini['lang'])
        self.page.populate_list()


def m_tool(self):
    """define tool-specific settings
    """
    if not self.page.settings:
        self.page.settings = {x: '' for x in hkc.csv_settingnames}
    old_redef = bool(int(self.page.settings[hkc.csv_redefsett]))
    dlg = ExtraSettingsDialog(self).exec_()
    if dlg == qtw.QDialog.Accepted:
        hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                     self.page.data, self.ini['lang'])
        test_redef = bool(int(self.page.settings[hkc.csv_redefsett]))
        test_dets = bool(int(self.page.settings[hkc.csv_detsett]))
        test_rbld = bool(int(self.page.settings[hkc.csv_rbldsett]))
        self._menuitems['M_SAVE'].setEnabled(test_redef)
        self._menuitems['M_RBLD'].setEnabled(test_rbld)
        indx = self.book.sel.currentIndex()
        win = self.book.pnl.widget(indx)
        if test_dets != self.page.has_extrapanel:
            self.page.has_extrapanel = test_dets
            newwin = HotkeyPanel(self.book, self.book.plugins[indx][1])
            self.book.pnl.insertWidget(indx, newwin)
            self.book.pnl.setCurrentIndex(indx)
            self.book.pnl.removeWidget(win)
        elif test_redef != old_redef and test_dets:
            win = self.book.pnl.currentWidget()
            win.set_extrascreen_editable(test_redef)


def m_col(self):
    """define tool-specific settings: column properties
    """
    if not self.page.settings:
        show_message(self, 'I_ADDSET')
        return
    dlg = ColumnSettingsDialog(self).exec_()
    if dlg == qtw.QDialog.Accepted:
        new_pagedata = {}
        for key, value in self.page.data.items():
            newvalue = []
            for colinf in self.page.column_info:
                test = colinf[-1]
                if test == 'new':
                    newvalue.append('')
                else:
                    newvalue.append(value[test])
            new_pagedata[key] = newvalue
        self.page.data = new_pagedata
        self.page.column_info = [x[:-1] for x in self.page.column_info]

        hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                     self.page.data, self.ini['lang'])
        if not self.page.data:
            return
        hdr = qtw.QTreeWidgetItem()
        self.page.p0list.setHeaderItem(hdr)
        self.page.p0list.setHeaderLabels([self.captions[col[0]] for col in
                                          self.page.column_info])
        hdr = self.page.p0list.header()
        hdr.setSectionsClickable(True)
        for indx, col in enumerate(self.page.column_info):
            hdr.resizeSection(indx, col[1])
        hdr.setStretchLastSection(True)
        self.page.populate_list()


def m_entry(self):
    """manual entry of keyboard shortcuts
    """
    if not all((self.page.settings, self.page.column_info)):
        show_message(self, 'I_ADDCOL')
        return
    dlg = EntryDialog(self).exec_()
    if dlg == qtw.QDialog.Accepted:
        if self.page.data:
            hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                         self.page.data, self.ini['lang'])
            self.page.populate_list()


def m_lang(self):
    """(menu) callback voor taalkeuze

    past de settings aan en leest het geselecteerde language file
    """
    # bepaal welke language files er beschikbaar zijn
    choices = [x for x in os.listdir(hkc.HERELANG)
               if os.path.splitext(x)[1] == ".lng"]
    # bepaal welke er momenteel geactiveerd is
    oldlang = self.ini['lang']
    indx = choices.index(oldlang) if oldlang in choices else 0
    lang, ok = qtw.QInputDialog.getItem(self, self.title, self.captions["P_SELLNG"],
                                        choices, current=indx, editable=False)
    if ok:
        hkc.change_setting('lang', oldlang, lang, self.ini['filename'])
        self.ini['lang'] = lang
        self.readcaptions(lang)
        self.setcaptions()


def m_about(self):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    show_message(self, text='\n'.join(self.captions['T_ABOUT'].format(
        self.captions['T_SHORT'], hkc.VRS, hkc.AUTH,
        self.captions['T_LONG']).split(' / ')))


def m_pref(self):
    """mogelijkheid bieden om een tool op te geven dat default getoond wordt
    """
    oldpref = self.ini.get("initial", None)
    oldmode = self.ini.get("startup", None)
    self.prefs = oldmode, oldpref
    ok = InitialToolDialog(self).exec_()
    if ok == qtw.QDialog.Accepted:
        mode, pref = self.prefs
        print('in m_pref: {}, {}'.format(mode, pref))
        if mode:
            self.ini['startup'] = mode
            hkc.change_setting('startup', oldmode, mode, self.ini['filename'])
        if mode == 'Fixed':
            self.ini['initial'] = pref
            hkc.change_setting('initial', oldpref, pref, self.ini['filename'])


def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.exit()


# application classes (dialog)


class InitialToolDialog(qtw.QDialog):
    """dialog to define which tool to show on startup
    """
    def __init__(self, parent):
        self.parent = parent
        oldmode, oldpref = self.parent.prefs
        choices = [x[0] for x in self.parent.ini["plugins"]]
        indx = choices.index(oldpref) if oldpref in choices else 0
        super().__init__()
        self.setWindowTitle(self.parent.title)
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(qtw.QLabel(self.parent.captions["M_PREF"], self))
        hbox = qtw.QHBoxLayout()
        self.check_fixed = qtw.QRadioButton(self.parent.captions["T_FIXED"], self)
        self.check_fixed.setChecked(oldmode == hkc.mode_f)
        hbox.addWidget(self.check_fixed)
        self.sel_fixed = qtw.QComboBox(self)
        self.sel_fixed.addItems(choices)
        self.sel_fixed.setEditable(True)
        self.sel_fixed.setCurrentIndex(indx)
        hbox.addWidget(self.sel_fixed)
        hbox.addStretch()
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        self.check_remember = qtw.QRadioButton(self.parent.captions["T_RMBR"], self)
        self.check_remember.setChecked(oldmode == hkc.mode_r)
        hbox.addWidget(self.check_remember)
        hbox.addStretch()
        vbox.addLayout(hbox)
        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(buttonbox)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def accept(self):
        """confirm dialog
        """
        if self.check_fixed.isChecked():
            mode = hkc.mode_f
        elif self.check_remember.isChecked():
            mode = hkc.mode_r
        else:
            mode = None
        pref = self.sel_fixed.currentText()
        self.parent.prefs = mode, pref
        print('in initialtooldialog: {}, {}'.format(mode, pref))
        super().accept()


class FileBrowseButton(qtw.QFrame):
    """Combination widget showing a text field and a button
    making it possible to either manually enter a filename or select
    one using a FileDialog
    """
    def __init__(self, parent, text="", level_down=False):
        self.parent = parent.parent
        if level_down:
            self.parent = self.parent.parent
        self.startdir = ''
        if text:
            self.startdir = os.path.dirname(text)
        super().__init__(parent)
        self.setFrameStyle(qtw.QFrame.Panel | qtw.QFrame.Raised)
        vbox = qtw.QVBoxLayout()
        box = qtw.QHBoxLayout()
        self.input = qtw.QLineEdit(text, self)
        self.input.setMinimumWidth(200)
        box.addWidget(self.input)
        caption = self.parent.captions['C_BRWS']
        self.button = qtw.QPushButton(caption, self, clicked=self.browse)
        box.addWidget(self.button)
        vbox.addLayout(box)
        self.setLayout(vbox)

    def browse(self):
        """callback for button
        """
        startdir = str(self.input.text()) or os.getcwd()
        path = qtw.QFileDialog.getOpenFileName(self,
                                               self.parent.captions['C_SELFIL'], startdir)
        if path[0]:
            self.input.setText(path[0])


class SetupDialog(qtw.QDialog):
    """dialoog voor het opzetten van een csv bestand

    geeft de mogelijkheid om alvast wat instellingen vast te leggen en zorgt er
    tevens voor dat het correcte formaat gebruikt wordt
    """
    def __init__(self, parent, name):
        self.parent = parent
        super().__init__()
        self.setWindowTitle(self.parent.parent.captions['T_INICSV'])

        grid = qtw.QGridLayout()

        text = qtw.QLabel(self.parent.parent.captions['T_NAMOF'].format(
            self.parent.parent.captions['S_PLGNAM'].lower(),
            self.parent.parent.captions['T_ISMADE']), self)
        self.t_program = qtw.QLineEdit('editor.plugins.{}_keys'.format(
            name.lower()), self)
        grid.addWidget(text, 1, 0, 1, 3)
        grid.addWidget(self.t_program, 1, 3)  # , 1, 1)
        text = qtw.QLabel(self.parent.parent.captions['S_PNLNAM'], self)
        self.t_title = qtw.QLineEdit(name + ' hotkeys', self)
        grid.addWidget(text, 2, 0, 1, 3)
        grid.addWidget(self.t_title, 2, 3)  # , 1, 1)
        self.c_rebuild = qtw.QCheckBox(self.parent.parent.captions['T_MAKE'].format(
            self.parent.parent.captions['S_RBLD']), self)
        grid.addWidget(self.c_rebuild, 3, 0, 1, 4)
        self.c_details = qtw.QCheckBox(self.parent.parent.captions['S_DETS'])
        grid.addWidget(self.c_details, 4, 0, 1, 4)
        self.c_redef = qtw.QCheckBox(self.parent.parent.captions['T_MAKE'].format(
            self.parent.parent.captions['S_RSAV']), self)
        grid.addWidget(self.c_redef, 5, 0, 1, 4)
        text = qtw.QLabel(self.parent.parent.captions['Q_SAVLOC'], self)
        grid.addWidget(text, 6, 0, 1, 2)
        self.t_loc = FileBrowseButton(self, text=os.path.join(
                                      'editor', 'plugins', name + "_hotkeys.csv"),
                                      level_down=True)
        grid.addWidget(self.t_loc, 6, 2, 1, 3)

        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        box = qtw.QVBoxLayout()
        box.addStretch()
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(grid)
        hbox.addStretch()
        box.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(buttonbox)
        hbox.addStretch()
        box.addLayout(hbox)
        box.addStretch()
        self.setLayout(box)

    def accept(self):
        """
        set self.parent.loc to the chosen filename
        write the settings to this file along with some sample data
        """
        loc = self.t_loc.input.text()
        if loc == "":
            show_message(self.parent, 'I_NEEDNAME')
            return
        self.parent.loc = loc
        self.parent.data = [self.t_program.text(), self.t_title.text(),
                            int(self.c_rebuild.isChecked()), int(self.c_details.isChecked()),
                            int(self.c_redef.isChecked())]
        super().accept()


class ColumnSettingsDialog(qtw.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent):
        self.parent = parent
        self.initializing = True
        super().__init__(parent)

        self.sizer = qtw.QVBoxLayout()
        text = self.parent.captions['T_COLSET'].format(
            self.parent.page.settings[hkc.csv_pnlsett])
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addSpacing(41)
        hsizer.addWidget(qtw.QLabel(self.parent.captions['C_TTL'], self),
                         alignment=core.Qt.AlignHCenter | core.Qt.AlignVCenter)
        hsizer.addSpacing(102)  # 82)
        hsizer.addWidget(qtw.QLabel(self.parent.captions['C_WID'], self),
                         alignment=core.Qt.AlignVCenter)
        hsizer.addSpacing(8)  # 84)
        hsizer.addWidget(qtw.QLabel(self.parent.captions['C_IND'], self),
                         alignment=core.Qt.AlignVCenter)
        hsizer.addWidget(qtw.QLabel(self.parent.captions['C_SEQ'], self),
                         alignment=core.Qt.AlignVCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        pnl = qtw.QFrame(self)
        self.scrl = qtw.QScrollArea(self)
        self.scrl.setWidget(pnl)
        self.scrl.setAlignment(core.Qt.AlignBottom)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()
        self.gsizer = qtw.QVBoxLayout()
        self.rownum = 0  # indicates the number of rows in the gridlayout
        self.data, self.checks = [], []
        self.col_textids, self.col_names, self.last_textid = \
            hkc.read_columntitledata(self)
        for ix, item in enumerate(self.parent.page.column_info):
            item.append(ix)
            self.add_row(*item)
        box = qtw.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(self.scrl)

        buttonbox = qtw.QDialogButtonBox()
        btn = buttonbox.addButton(self.parent.captions['C_ADDCOL'],
                                  qtw.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_column)
        btn = buttonbox.addButton(self.parent.captions['C_REMCOL'],
                                  qtw.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.remove_columns)
        buttonbox.addButton(qtw.QDialogButtonBox.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)
        self.initializing = False

    def exec_(self):
        """reimplementation to prevent dialog from showing in some cases
        """
        if self.last_textid == '099':
            # TODO: rethink this
            show_message(self.parent, text="Can't perform this function: "
                                           "no language text identifiers below 100 left")
            self.reject()
        else:
            return super().exec_()

    def add_row(self, name='', width='', is_flag=False, colno=''):
        """create a row for defining column settings
        """
        self.rownum += 1
        rownum = self.rownum
        colnum = 0
        check = qtw.QCheckBox(self)
        ghsizer = qtw.QHBoxLayout()
        ghsizer.addWidget(check, rownum)
        self.checks.append(check)
        colnum += 1
        w_name = qtw.QComboBox(self)
        w_name.addItems(self.col_names)
        w_name.setEditable(True)
        if name:
            w_name.setCurrentIndex(self.col_textids.index(name))
        else:
            w_name.clearEditText()
        ghsizer.addWidget(w_name, rownum)
        colnum += 1
        hsizer = qtw.QHBoxLayout()
        hsizer.addSpacing(20)
        w_width = qtw.QSpinBox(self)
        w_width.setMaximum(999)
        if width:
            w_width.setValue(width)
        w_width.setFixedWidth(48)
        hsizer.addWidget(w_width)
        hsizer.addSpacing(20)
        ghsizer.addLayout(hsizer, rownum)
        colnum += 1
        hsizer = qtw.QHBoxLayout()
        hsizer.addSpacing(40)
        w_flag = qtw.QCheckBox(self)
        w_flag.setChecked(is_flag)
        w_flag.setFixedWidth(32)
        hsizer.addWidget(w_flag)
        hsizer.addSpacing(24)
        ghsizer.addLayout(hsizer, rownum)
        colnum += 1
        hsizer = qtw.QHBoxLayout()
        hsizer.addSpacing(68)
        val = self.rownum if colno == '' else colno + 1
        w_colno = qtw.QSpinBox(self)
        w_colno.setMinimum(1)
        w_colno.setMaximum(99)
        w_colno.setValue(val)
        w_colno.setFixedWidth(36)
        hsizer.addWidget(w_colno)
        hsizer.addStretch()
        ghsizer.addLayout(hsizer, rownum)
        self.gsizer.addLayout(ghsizer)
        old_colno = "new" if colno == '' else colno
        self.data.append((w_name, w_width, w_colno, w_flag, old_colno))
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 62)
        vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        """remove a column settings row
        """
        self.rownum -= 1
        check = self.checks[rownum]
        for widgets in self.data[rownum:]:
            w_colno = widgets[2]
            w_colno.setValue(w_colno.value() - 1)
        w_name, w_width, w_colno, w_flag, _ = self.data[rownum]
        for widget in check, w_name, w_width, w_colno, w_flag:
            self.gsizer.removeWidget(widget)
            widget.close()
        self.gsizer.removeItem(self.gsizer.itemAt(rownum))
        self.checks.pop(rownum)
        self.data.pop(rownum)

    def add_column(self):
        """nieuwe rij aanmaken in self.gsizer"""
        self.add_row()

    def remove_columns(self):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        test = [x.isChecked() for x in self.checks]
        checked = [x for x, y in enumerate(test) if y]
        if not any(test):
            return
        if ask_question(self.parent, 'Q_REMCOL'):
            for row in reversed(checked):
                self.delete_row(row)

    def accept(self):
        """save the changed settings and leave
        """
        column_info, new_titles = [], []
        lastcol = -1
        for ix, value in enumerate(sorted(self.data, key=lambda x: x[2].value())):
            w_name, w_width, w_colno, w_flag, old_colno = value
            if w_colno.value() == lastcol:
                show_message(self.parent, 'I_DPLCOL')
                return
            lastcol = w_colno.value()
            name = w_name.currentText()
            if name in self.col_names:
                name = self.col_textids[self.col_names.index(name)]
            else:
                self.last_textid = "{:0>3}".format(int(self.last_textid) + 1)
                new_titles.append((self.last_textid, name))
                name = self.last_textid
            column_info.append([name, int(w_width.text()), w_flag.isChecked(),
                                old_colno])
        if new_titles:
            hkc.add_columntitledata(new_titles)
        self.parent.page.column_info = column_info
        for id_, name in new_titles:
            self.parent.captions[id_] = name
            self.parent.page.captions[id_] = name
        super().accept()


class ExtraSettingsDialog(qtw.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        ## self.resize(680, 400)

        self.sizer = qtw.QVBoxLayout()

        pnl = qtw.QFrame()
        vsizer = qtw.QVBoxLayout()

        hsizer = qtw.QHBoxLayout()
        text = qtw.QLabel(self.parent.captions['S_PLGNAM'], self)
        self.t_program = qtw.QLineEdit(self.parent.page.settings[hkc.csv_plgsett], self)
        hsizer.addWidget(text)
        hsizer.addWidget(self.t_program)
        vsizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        text = qtw.QLabel(self.parent.captions['S_PNLNAM'], self)
        self.t_title = qtw.QLineEdit(self.parent.page.settings[hkc.csv_pnlsett], self)
        hsizer.addWidget(text)
        hsizer.addWidget(self.t_title)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        self.c_rebuild = qtw.QCheckBox(self.parent.captions['T_MAKE'].format(
            self.parent.captions['S_RBLD']), self)
        if self.parent.page.settings[hkc.csv_rbldsett] == '1':
            self.c_rebuild.toggle()
        hsizer.addWidget(self.c_rebuild)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        self.c_showdet = qtw.QCheckBox(self.parent.captions['S_DETS'], self)
        try:
            if self.parent.page.settings[hkc.csv_detsett] == '1':
                self.c_showdet.toggle()
        except KeyError:
            pass
        hsizer.addWidget(self.c_showdet)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        self.c_redef = qtw.QCheckBox(self.parent.captions['T_MAKE'].format(
            self.parent.captions['S_RSAV']), self)
        if self.parent.page.settings[hkc.csv_redefsett] == '1':
            self.c_redef.toggle()
        hsizer.addWidget(self.c_redef)
        vsizer.addLayout(hsizer)
        pnl.setLayout(vsizer)
        pnl.setFrameStyle(qtw.QFrame.Box | qtw.QFrame.Raised)
        self.sizer.addWidget(pnl)

        pnl = qtw.QFrame(self)
        vsizer = qtw.QVBoxLayout()
        text = self.parent.captions['T_XTRASET'].format(
            self.parent.page.settings[hkc.csv_pnlsett])
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addSpacing(41)
        hsizer.addWidget(qtw.QLabel(self.parent.captions['C_NAM'], self),
                         alignment=core.Qt.AlignHCenter)
        hsizer.addSpacing(52)
        hsizer.addWidget(qtw.QLabel(self.parent.captions['C_VAL'], self),
                         alignment=core.Qt.AlignHCenter)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)

        pnl2 = qtw.QFrame(self)
        self.scrl = qtw.QScrollArea(self)
        self.scrl.setWidget(pnl2)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()

        self.gsizer = qtw.QGridLayout()
        rownum = 0
        self.rownum = rownum
        self.data, self.checks = [], []
        print([x for x in self.parent.page.settings.keys()])
        for name, value in self.parent.page.settings.items():
            if name not in hkc.csv_settingnames and name != 'extra':
                desc = self.parent.page.settings['extra'][name]
                self.add_row(name, value, desc)
        pnl2.setLayout(self.gsizer)
        pnl.setFrameStyle(qtw.QFrame.Box)
        self.scrl.ensureVisible(0, 0)
        vsizer.addWidget(self.scrl)

        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        btn = qtw.QPushButton(self.parent.captions['C_ADDSET'], self)
        btn.clicked.connect(self.add_setting)
        hsizer.addWidget(btn)
        btn = qtw.QPushButton(self.parent.captions['C_REMSET'], self)
        btn.clicked.connect(self.remove_settings)
        hsizer.addWidget(btn)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)
        pnl.setLayout(vsizer)
        pnl.setFrameStyle(qtw.QFrame.Box | qtw.QFrame.Raised)
        self.sizer.addWidget(pnl)

        buttonbox = qtw.QDialogButtonBox()
        btn = buttonbox.addButton(qtw.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(qtw.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)

    def add_row(self, name='', value='', desc=''):
        """add a row for defining a setting (name, value)
        """
        ## if value:
            ## value, desc = value
        ## else:
            ## desc = ''
        self.rownum += 1
        colnum = 0
        check = qtw.QCheckBox(self)
        self.gsizer.addWidget(check, self.rownum, colnum)
        self.checks.append(check)
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
        self.data.append((w_name, w_value, w_desc))
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 62)
        vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        """delete a setting definition row
        """
        check = self.checks[rownum]
        w_name, w_value, w_desc = self.data[rownum]
        for widget in check, w_name, w_value, w_desc:
            self.gsizer.removeWidget(widget)
            widget.close()
        self.checks.pop(rownum)
        self.data.pop(rownum)

    def add_setting(self):
        """nieuwe rij aanmaken in self.gsizer"""
        self.add_row()

    def remove_settings(self):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        test = [x.isChecked() for x in self.checks]
        checked = [x for x, y in enumerate(test) if y]
        if any(test):
            if ask_question(self.parent, 'Q_REMSET'):
                for row in reversed(checked):
                    self.delete_row(row)

    def accept(self):
        """update settings and leave
        """
        self.parent.page.settings[hkc.csv_plgsett] = self.t_program.text()
        self.parent.page.settings[hkc.csv_pnlsett] = self.t_title.text()
        value = '1' if self.c_rebuild.isChecked() else '0'
        self.parent.page.settings[hkc.csv_rbldsett] = value
        ## try:
            ## oms = self.parent.page.settings[hkc.csv_detsett]    # oms variable not used?
        ## except KeyError:
            ## oms = self.parent.captions['T_BOOL'].format(
                ## self.parent.captions['S_DETS'])
        value = '1' if self.c_showdet.isChecked() else '0'
        self.parent.page.settings[hkc.csv_detsett] = value
        value = '1' if self.c_redef.isChecked() else '0'
        self.parent.page.settings[hkc.csv_redefsett] = value

        settingsdict, settdescdict = {}, {}
        for w_name, w_value, w_desc in self.data:
            ## settingsdict[w_name.text()] = (w_value.text(), w_desc.text())
            settingsdict[w_name.text()] = w_value.text()
            settdescdict[w_name.text()] = w_desc.text()
        todelete = []
        for setting in self.parent.page.settings:
            if setting not in hkc.csv_settingnames:
                todelete.append(setting)
        for setting in todelete:
            del self.parent.page.settings[setting]
        self.parent.page.settings.update(settingsdict)
        self.parent.page.settings['extra'] = settdescdict

        super().accept()


class DeleteDialog(qtw.QDialog):
    """dialog for deleting a tool from the collection
    """
    def __init__(self, parent):
        self.parent = parent
        self.last_added = ''
        super().__init__(parent)
        self.sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(self.parent.parent.captions['Q_REMPRG'], self)
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        check = qtw.QCheckBox(self.parent.parent.captions['Q_REMCSV'], self)
        hsizer.addWidget(check)
        self.remove_keydefs = check
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        check = qtw.QCheckBox(self.parent.parent.captions['Q_REMPLG'], self)
        hsizer.addWidget(check)
        self.remove_plugin = check
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.sizer.addWidget(buttonbox)
        self.setLayout(self.sizer)

    def accept(self):
        """send settings to parent and leave
        """
        self.parent.remove_data = self.remove_keydefs.isChecked()
        self.parent.remove_code = self.remove_plugin.isChecked()
        qtw.QDialog.accept(self)


class FilesDialog(qtw.QDialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, parent):
        self.parent = parent
        self.last_added = ''
        self.code_to_remove = []
        self.data_to_remove = []
        super().__init__(parent)
        self.resize(680, 400)

        self.sizer = qtw.QVBoxLayout()
        text = '\n'.join((self.parent.captions['T_TOOLS'].split(' / ')))
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addSpacing(36)
        hsizer.addWidget(qtw.QLabel(self.parent.captions['C_PRGNAM'], self),
                         alignment=core.Qt.AlignHCenter | core.Qt.AlignVCenter)
        hsizer.addSpacing(84)
        hsizer.addWidget(qtw.QLabel(self.parent.captions['C_CSVLOC'], self),
                         alignment=core.Qt.AlignVCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        pnl = qtw.QFrame(self)
        self.scrl = qtw.QScrollArea(self)
        self.scrl.setWidget(pnl)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()
        self.gsizer = qtw.QGridLayout()
        rownum = 0
        self.rownum = rownum
        self.checks = []
        self.paths = []
        self.data = []
        self.pathdata = {}
        for name, path in self.parent.ini["plugins"]:
            self.add_row(name, path)
        box = qtw.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(self.scrl)

        buttonbox = qtw.QDialogButtonBox()
        btn = buttonbox.addButton(self.parent.captions['C_ADDPRG'],
                                  qtw.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_program)
        btn = buttonbox.addButton(self.parent.captions['C_REMPRG'],
                                  qtw.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.remove_programs)
        buttonbox.addButton(qtw.QDialogButtonBox.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)

    def add_row(self, name, path=''):
        """create a row for defining a file location
        """
        self.rownum += 1
        colnum = 0
        check = qtw.QCheckBox(name, self)
        self.gsizer.addWidget(check, self.rownum, colnum)
        self.checks.append(check)
        colnum += 1
        browse = FileBrowseButton(self, text=path)
        self.gsizer.addWidget(browse, self.rownum, colnum)
        self.paths.append((name, browse))
        if self.data:
            self.pathdata[name] = self.data
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 52)
        vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        """remove a tool location definition row
        """
        check = self.checks[rownum]
        _, win = self.paths[rownum]
        self.gsizer.removeWidget(check)
        check.close()
        self.gsizer.removeWidget(win)
        win.close()
        self.checks.pop(rownum)
        self.paths.pop(rownum)

    def add_program(self):
        """nieuwe rij aanmaken in self.gsizer"""
        self.data = []
        newtool, ok = qtw.QInputDialog.getText(self, self.parent.title,
                                               self.parent.captions['P_NEWPRG'])
        if ok:
            if newtool == "":
                show_message(self.parent, 'I_NEEDNAME')
                return
            self.last_added = newtool
            self.loc = ""
            if ask_question(self.parent, 'P_INICSV'):
                ok = SetupDialog(self, newtool).exec_()
                ## print(self.data)
            self.add_row(newtool, path=self.loc)

    def remove_programs(self):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        checked = [(x, y.text()) for x, y in enumerate(self.checks)
                   if y.isChecked()]
        if checked:
            dlg = DeleteDialog(self).exec_()
            if dlg == qtw.QDialog.Accepted:
                for row, name in reversed(checked):
                    try:
                        csv_name, prg_name = self.parent.pluginfiles[name]
                    except KeyError:
                        csv_name, prg_name = self.parent.ini['plugins'], None
                    if self.remove_data:
                        if csv_name:
                            self.data_to_remove.append(csv_name)
                    if self.remove_code:
                        if prg_name:
                            self.code_to_remove.append(prg_name)
                    self.delete_row(row)

    def accept(self):
        """send updates to parent and leave
        """
        if self.last_added not in [x[0] for x in self.paths]:
            self.last_added = ''
        self.parent.last_added = self.last_added
        for filename in self.code_to_remove:
            os.remove(filename)
        for filename in self.data_to_remove:
            os.remove(filename)
        self.parent.ini["plugins"] = hkc.update_paths(self.paths, self.pathdata,
                                                      self.parent.ini["lang"])
        super().accept()


class EntryDialog(qtw.QDialog):
    """Dialog for Manual Entry
    """
    def __init__(self, parent):
        self.parent = parent
        self.captions = self.parent.captions

        super().__init__(parent)
        self.resize(680, 400)

        # use self.parent.page.column_info to define grid
        names, widths = [], []
        for row in self.parent.page.column_info:
            names.append(self.captions[row[0]])
            widths.append(row[1])

        # use self.parent.page.data to populate grid
        self.data = self.parent.page.data

        self.p0list = qtw.QTableWidget(self)
        self.p0list.setColumnCount(len(names))
        self.p0list.setHorizontalHeaderLabels(names)
        p0hdr = self.p0list.horizontalHeader()
        for indx, wid in enumerate(widths):
            p0hdr.resizeSection(indx, wid)
        num_rows = 0
        for rowkey, row in self.data.items():
            self.p0list.insertRow(num_rows)
            for i, element in enumerate(row):
                new_item = qtw.QTableWidgetItem()
                new_item.setText(element)
                self.p0list.setItem(num_rows, i, new_item)
            num_rows += 1
        self.numrows = num_rows

        self.sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(self.p0list)
        self.sizer.addLayout(hsizer)

        buttonbox = qtw.QDialogButtonBox()
        btn = buttonbox.addButton(self.captions['C_ADDKEY'],
                                  qtw.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_key)
        btn = buttonbox.addButton(self.captions['C_REMKEY'],
                                  qtw.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.delete_key)
        buttonbox.addButton(qtw.QDialogButtonBox.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)

    def add_key(self):
        "add a line to the grid"
        self.p0list.insertRow(self.numrows)
        for i in range(self.p0list.columnCount()):
            new_item = qtw.QTableWidgetItem()
            new_item.setText("")
            self.p0list.setItem(self.numrows, i, new_item)
        self.numrows += 1
        ## self.p0list.scrollToItem(new_item)
        self.p0list.scrollToBottom()

    def delete_key(self):
        "remove selected line(s) from the grid"
        selected_rows = []
        for item in self.p0list.selectedRanges():
            for increment in range(item.rowCount()):
                selected_rows.append(item.topRow() + increment)
        for row in reversed(sorted(selected_rows)):
            self.p0list.removeRow(row)

    def accept(self):
        """send updates to parent and leave
        """
        new_values = {}
        for rowid in range(self.p0list.rowCount()):
            value = []
            for colid in range(self.p0list.columnCount()):
                try:
                    value.append(self.p0list.item(rowid, colid).text())
                except AttributeError:
                    value.append('')
            if value != [''] * self.p0list.columnCount():
                new_values[len(new_values)] = value
        self.parent.page.data = new_values
        super().accept()

# general callbacks (I think)


def on_text(self, ted, text):
    """on changing a text entry
    """
    if self._initializing_screen:
        return
    text = str(text)    # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan de
                        # callback soms fout? Of is het Py3 vs Py2?
    hlp = ted.text()
    if text != hlp:
        text = hlp
    if 'C_KEY' in self.fields:
        if text == self._origdata[self.ix_key]:
            self.defchanged = True
            self.b_save.setEnabled(True)
        elif ted.text() == self._origdata[self.ix_key]:
            self.defchanged = False
            self.b_save.setEnabled(False)


def on_combobox(self, cb, text):
    """callback op het gebruik van een combobox

    zorgt ervoor dat de buttons ge(de)activeerd worden
    """
    if self._initializing_screen:
        return
    text = str(text)    # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan de
                        # callback soms fout? Of is het Py3 vs Py2?
    hlp = cb.currentText()
    if text != hlp:
        text = hlp
    self.defchanged = False
    try:
        test_key = bool(self.cmb_key)
    except AttributeError:
        test_key = False
    try:
        test_cmd = bool(self.cmb_commando)
    except AttributeError:
        test_cmd = False
    try:
        test_cnx = bool(self.cmb_context)
    except AttributeError:
        test_cnx = False
    if test_key and cb == self.cmb_key:
        keyitemindex = self.ix_key
        if text != self._origdata[keyitemindex]:
            self._newdata[keyitemindex] = text
            if not self.initializing_keydef:
                self.defchanged = True
                if 'C_CMD' in self.fields:
                    self.b_save.setEnabled(True)
        elif str(self.cmb_commando.currentText()) == self._origdata[cmditemindex]:  # UNDEF
            self.defchanged = False
            if 'C_CMD' in self.fields:
                self.b_save.setEnabled(False)
    elif test_cnx and cb == self.cmb_context:
        if text != self._origdata[self.ix_cntxt]:
            context = self._origdata[self.ix_cntxt] = self.cmb_context.currentText()
            self.cmb_commando.clear()
            actionslist = self.contextactionsdict[context]
            self.cmb_commando.addItems(actionslist)
            if not self.initializing_keydef:
                self.defchanged = True
                if 'C_CMD' in self.fields:
                    self.b_save.setEnabled(True)
        elif str(self.cmb_commando.currentText()) == self._origdata[self.ix_cntxt]:
            self.defchanged = False
            if 'C_CMD' in self.fields:
                self.b_save.setEnabled(False)
    elif test_cmd and cb == self.cmb_commando:
        cmditemindex = self.ix_cmd
        if text != self._origdata[cmditemindex]:
            self._newdata[cmditemindex] = text
            try:
                self.txt_oms.setText(self.descriptions[text])
            except KeyError:
                self.txt_oms.setText(self.captions['M_NODESC'])
            if not self.initializing_keydef:
                self.defchanged = True
                if 'C_CMD' in self.fields:
                    self.b_save.setEnabled(True)
        elif str(self.cmb_key.currentText()) == self._origdata[cmditemindex]:
            if 'C_CMD' in self.fields:
                self.b_save.setEnabled(False)
    else:
        try:
            self._keys.on_combobox(self, cb, text)  # user exit
        except AttributeError:
            pass


def on_checkbox(self, cb, state):
    """callback op het gebruik van een checkbox
    """
    if self._initializing_screen:
        return
    ## state = bool(state)
    for win, indx in zip(
            (self.cb_shift, self.cb_ctrl, self.cb_alt, self.cb_win),
            self.ix_mods):
        if cb == win and state != self._origdata[indx]:
            self._newdata[indx] = state
            if not self.initializing_keydef:
                self.defchanged = True
                if 'C_CMD' in self.fields:
                    self.b_save.setEnabled(True)
    else:   # else without break statement
        states = [self.cb_shift.isChecked(), self.cb_ctrl.isChecked(),
                  self.cb_alt.isChecked(), self.cb_win.isChecked()]
        if states == [self._origdata[x] for x in self.ix_mods]:
            self.defchanged = False
            if 'C_CMD' in self.fields:
                self.b_save.setEnabled(False)

# application classes (main screen and subscreens)


class HotkeyPanel(qtw.QFrame):
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
        self._initializing_screen = True
        self.modified = False

        super().__init__(parent)
        self.parent = parent  # .parent()
        self.captions = self.parent.parent.captions
        self.has_extrapanel = False

        nodata = ''
        try:
            self.settings, self.column_info, self.data = hkc.readcsv(self.pad)
        except ValueError as e:
            nodata = self.captions['I_NOSET'].format(e, self.pad)
        except FileNotFoundError:
            nodata = self.captions['I_NOSETFIL'].format(self.pad)
        if nodata:
            self.settings, self.column_info, self.data = {}, [], {}
        self.otherstuff = {}  # ruimte voor zaken als een lijst met mogelijke commando's

        if not self.settings or not self.column_info:
            tmp = ":\n\n" + nodata if nodata else ""
            nodata = self.captions['I_NODATA'] + tmp
        else:
            modulename = self.settings[hkc.csv_plgsett]
            try:
                self._keys = importlib.import_module(modulename)
            except ImportError:
                nodata = self.captions['I_NODATA'].replace('data', 'plugin code')
        if nodata:
            _sizer = qtw.QVBoxLayout()
            hsizer = qtw.QHBoxLayout()
            hsizer.addStretch()
            hsizer.addWidget(qtw.QLabel(nodata, self))
            hsizer.addStretch()
            _sizer.addLayout(hsizer)
            self.setLayout(_sizer)
            self.title = self.parent.parent.title
            return

        self.p0list = qtw.QTreeWidget(self)
        try:
            self.parent.page = self
            self.otherstuff = self._keys.buildcsv(parent, showinfo=False)[1]
        except AttributeError:
            pass

        try:
            self.has_extrapanel = bool(int(self.settings[hkc.csv_detsett]))
        except KeyError:
            pass

        self.title = self.settings["PanelName"]

        # self.has_extrapanel controleert extra initialisaties en het opbouwen van de rest van de GUI
        # het vullen van veldwaarden hierin gebeurt als gevolg van het vullen
        # van de eerste rij in de listbox, daarom moet deze het laatst
        # self.otherstuff = self._keys.getotherstuff()
        if self.has_extrapanel:
            self.fields = [x[0] for x in self.column_info]
            self.add_extra_attributes()
            self.add_extra_fields()

        self._sizer = qtw.QVBoxLayout()
        if self.column_info:
            self.p0list.setSortingEnabled(True)
            self.p0list.setHeaderLabels([self.captions[col[0]] for col in
                                         self.column_info])
            self.p0list.setAlternatingRowColors(True)
            self.p0list.currentItemChanged.connect(self.on_item_selected)
            hdr = self.p0list.header()
            hdr.setSectionsClickable(True)
            for indx, col in enumerate(self.column_info):
                hdr.resizeSection(indx, col[1])
            hdr.setStretchLastSection(True)
            self.populate_list()
            sizer1 = qtw.QHBoxLayout()
            sizer1.addWidget(self.p0list)
            self._sizer.addLayout(sizer1)

        # indien van toepassing: toevoegen van de rest van de GUI aan de layout
        if self.has_extrapanel:
            self.layout_extra_fields(self._sizer)

        self.setLayout(self._sizer)
        self._initializing_screen = False
        self.filtertext = ''

    def readkeys(self):
        "(re)read the data for the keydef list"
        self.data = hkc.readcsv(self.pad)[2]

    def savekeys(self):
        """save modified keydef back

        allows saving back to csv without (?) saving to the tool settings
        """
        self.parent.data = self.data
        try:
            self._keys.savekeys(self)
        except AttributeError:
            pass
        hkc.writecsv(self.pad, self.settings, self.column_info, self.data,
                     self.parent.parent.ini['lang'])
        self.set_title(modified=False)

    def set_title(self, modified=None):
        """set title and adapt to modified flag
        if modified flag is not supplied, use its current state
        """
        # is this of any use? does this window has its own title?
        if modified is not None:
            self.modified = False
        title = self.title
        if self.modified:
            title += ' ' + self.captions["T_MOD"]
        self.setWindowTitle(title)

    def setcaptions(self):
        """update captions according to selected language
        """
        self.set_title()
        if self.has_extrapanel:
            self.captions_extra_fields()
        if self.data:
            self.populate_list()

    def populate_list(self, pos=0):
        """vullen van de list control
        """
        self.p0list.clear()
        items = self.data.items()
        if items is None or len(items) == 0:
            return

        for key, data in items:
            try:
                int(key)
            except ValueError:
                continue
            new_item = qtw.QTreeWidgetItem()
            new_item.setData(0, core.Qt.UserRole, key)
            for indx, col in enumerate(self.column_info):
                is_soort = col[2]
                value = data[indx]
                if is_soort:
                    value = 'C_DFLT' if value == 'S' else 'C_RDEF'
                    value = self.captions[value]
                new_item.setText(indx, value)
            self.p0list.addTopLevelItem(new_item)
            self.p0list.setCurrentItem(self.p0list.topLevelItem(pos))

    def exit(self):
        """processing triggered by exit button
        """
        if self.modified:
            ok = qtw.QMessageBox.question(self, self.parent.title,
                                          self.parent.captions['Q_SAVXIT'],
                                          qtw.QMessageBox.Yes | qtw.QMessageBox.No |
                                          qtw.QMessageBox.Cancel)
            if ok == qtw.QMessageBox.Yes:
                self.savekeys()
            elif ok == qtw.QMessageBox.Cancel:
                return False
        return True

    def add_extra_attributes(self):
        """pertaining to details for selected keydef, to make editing possible
        """
        self.init_origdata = []
        ix_item = 0
        if 'C_KEY' in self.fields:
            self.init_origdata.append('')
            self.ix_key = ix_item
            ix_item += 1
            self.keylist = [x for x in string.ascii_uppercase] + \
                [x for x in string.digits] + ["F" + str(i) for i in range(1, 13)] + \
                hkc.named_keys + \
                ['.', ',', '+', '=', '-', '`', '[', ']', '\\', ';', "'", '/']
        if 'C_MODS' in self.fields:
            self.init_origdata += [False, False, False, False]
            self.ix_mods = []
            for _ in range(4):
                self.ix_mods.append(ix_item)
                ix_item += 1
        if 'C_CNTXT' in self.fields:
            self.init_origdata.append('')
            self.ix_cntxt = ix_item
            ix_item += 1
        if 'C_CMD' in self.fields:
            self.init_origdata.append('')
            self.ix_cmd = ix_item
            ix_item += 1
        self.contextslist = []
        self.commandslist = []
        try:
            self._keys.add_extra_attributes(self)  # user exit
        except AttributeError:
            pass
        if self.keylist:
            self.keylist.sort()

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        self.screenfields = []
        self._box = box = qtw.QFrame(self)
        frameheight = 90
        try:
            frameheight = self._keys.get_frameheight()  # user exit
        except AttributeError:
            pass
        box.setMaximumHeight(frameheight)

        if 'C_KEY' in self.fields:
            self.lbl_key = qtw.QLabel(self.captions['C_KTXT'] + " ", box)
            if self.keylist is None:
                ted = qtw.QLineEdit(box)
                ted.setMaximumWidth(90)
                ted.textChanged[str].connect(functools.partial(on_text, self, ted, str))
                self.screenfields.append(ted)
                self.txt_key = ted
            else:
                cb = qtw.QComboBox(box)
                cb.setMaximumWidth(90)
                cb.addItems(self.keylist)  # niet sorteren
                cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
                                                                      self, cb, str))
                self.screenfields.append(cb)
                self.cmb_key = cb

        if 'C_MODS' in self.fields:
            for ix, x in enumerate(('M_CTRL', 'M_ALT', 'M_SHFT', 'M_WIN')):
                cb = qtw.QCheckBox(self.captions[x].join(("+ ", "")), box)
                cb.setChecked(False)
                self.screenfields.append(cb)
                cb.stateChanged.connect(functools.partial(on_checkbox, self, cb))
                if ix == 0:
                    self.cb_ctrl = cb
                elif ix == 1:
                    self.cb_alt = cb
                elif ix == 2:
                    self.cb_shift = cb
                elif ix == 3:
                    self.cb_win = cb

        if 'C_CNTXT' in self.fields:
            self.lbl_context = qtw.QLabel(self.captions['C_CNTXT'], box)
            cb = qtw.QComboBox(box)
            cb.addItems(self.contextslist)
            cb.setMaximumWidth(110)
            cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
                                                                  self, cb, str))
            self.screenfields.append(cb)
            self.cmb_context = cb

        if 'C_CMD' in self.fields:
            self.txt_cmd = qtw.QLabel(self.captions['C_CTXT'] + " ", box)
            cb = qtw.QComboBox(self)
            cb.setMaximumWidth(150)
            if 'C_CNTXT' not in self.fields:  # load on choosing context
                cb.addItems(self.commandslist)
            cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
                                                                  self, cb, str))
            self.screenfields.append(cb)
            self.cmb_commando = cb

        self.b_save = qtw.QPushButton(self.captions['C_SAVE'], box)
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(self.on_update)
        self.b_del = qtw.QPushButton(self.captions['C_DEL'], box)
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(self.on_delete)
        self._savestates = (False, False)

        if 'C_DESC' in self.fields:
            self.txt_oms = qtw.QTextEdit(box)
            self.txt_oms.setReadOnly(True)

        try:
            self._keys.add_extra_fields(self, box)  # user exit
        except AttributeError:
            pass

        self.set_extrascreen_editable(bool(int(self.settings['RedefineKeys'])))

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
        if 'C_KEY' in self.fields:
            sizer3 = qtw.QHBoxLayout()
            sizer3.addWidget(self.lbl_key)
            if self.keylist is None:
                sizer3.addWidget(self.txt_key)
            else:
                sizer3.addWidget(self.cmb_key)
            sizer3.addStretch()
            sizer2.addLayout(sizer3)

        if 'C_MODS' in self.fields:
            sizer3 = qtw.QHBoxLayout()
            sizer3.addWidget(self.cb_ctrl)
            sizer3.addWidget(self.cb_alt)
            sizer3.addWidget(self.cb_shift)
            sizer3.addWidget(self.cb_win)
            sizer3.addStretch()
            sizer2.addLayout(sizer3)

        sizer1.addLayout(sizer2)
        sizer1.addStretch()
        if 'C_CNTXT' in self.fields:
            sizer2 = qtw.QHBoxLayout()
            sizer2.addWidget(self.lbl_context)
            sizer2.addWidget(self.cmb_context)
            sizer1.addLayout(sizer2)

        if 'C_CMD' in self.fields:
            sizer2 = qtw.QHBoxLayout()
            sizer2.addWidget(self.txt_cmd)
            sizer2.addWidget(self.cmb_commando)
            sizer1.addLayout(sizer2)

        sizer1.addWidget(self.b_save)
        sizer1.addWidget(self.b_del)

        bsizer.addLayout(sizer1)
        sizer1 = qtw.QHBoxLayout()
        if 'C_DESC' in self.fields:
            sizer2 = qtw.QVBoxLayout()
            sizer2.addWidget(self.txt_oms)
            sizer1.addLayout(sizer2, 2)

        try:
            self._keys.layout_extra_fields(self, sizer1)  # user exit
        except AttributeError:
            pass

        bsizer.addLayout(sizer1)

        self._box.setLayout(bsizer)
        sizer.addWidget(self._box)

    def captions_extra_fields(self):
        """to be called on changing the language
        """
        if 'C_KEY' in self.fields:
            self.lbl_key.setText(self.captions['C_KTXT'])
        if 'C_MODS' in self.fields:
            self.cb_win.setText(self.captions['M_WIN'].join(("+", "  ")))
            self.cb_ctrl.setText(self.captions['M_CTRL'].join(("+", "  ")))
            self.cb_alt.setText(self.captions['M_ALT'].join(("+", "  ")))
            self.cb_shift.setText(self.captions['M_SHFT'].join(("+", "  ")))
        if 'C_CNTXT' in self.fields:
            self.lbl_context.setText(self.captions['C_CNTXT'])
        if 'C_CMD' in self.fields:
            self.txt_cmd.setText(self.captions['C_CTXT'])
        self.b_save.setText(self.captions['C_SAVE'])
        self.b_del.setText(self.captions['C_DEL'])
        try:
            self._keys.captions_extra_fields(self)  # user exit
        except AttributeError:
            pass

    def on_item_selected(self, newitem, olditem):
        """callback on selection of an item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        if not self.has_extrapanel:
            return
        if not newitem:  # bv. bij p0list.clear()
            return
        self.initializing_keydef = True
        if self._initializing_screen:
            self.refresh_extrascreen(newitem)
            self.initializing_keydef = False
            return
        other_item = other_cntxt = other_cmd = False
        if 'C_KEYS' in self.fields:
            origkey = self._origdata[self.ix_key]
            key = self._newdata[self.ix_key]
            other_item = key != origkey
        if 'C_MODS' in self.fields:
            origmods = ''.join([y for x, y in zip(self.ix_mods, ('WCAS'))
                                if self._origdata[x]])
            mods = ''.join([y for x, y in zip(self.ix_mods, ('WCAS'))
                            if self._newdata[x]])
            other_item = other_item or mods != origmods
        if 'C_CMD' in self.fields:
            origcmd = self._origdata[self.ix_cmd]
            cmnd = self._newdata[self.ix_cmd]
            other_cmd = cmnd != origcmd
        if 'C_CNTXT' in self.fields:
            origcntxt = self._origdata[self.ix_cntxt]
            context = self._newdata[self.ix_cntxt]
            other_cntxt = context != origcntxt
        cursor_moved = True if newitem != olditem and olditem is not None else False
        any_change = other_item or other_cmd or other_cntxt
        found = False
        for number, item in self.data.items():
            keymatch = modmatch = cntxtmatch = True
            if 'C_KEYS' in self.fields and item[0] != key:
                keymatch = False
            if 'C_MODS' in self.fields and item[1] != mods:
                modmatch = False
            if 'C_CNTXT' in self.fields and item[2] != context:
                cntxtmatch = False
            if keymatch and modmatch and cntxtmatch:
                found = True
                indx = number
                break
        make_change = False
        if any_change:
            if cursor_moved:
                make_change = ask_question(self, "Q_SAVCHG")
            elif other_item:
                if found:
                    make_change = ask_question(self, "Q_DPLKEY")
                else:
                    make_change = True
            else:
                make_change = True
        # note this only works for one specific plugin (tcmdrkys) I think
        # which is no problem as long as I don't modify keydefs
        if make_change:
            item = self.p0list.currentItem()
            pos = self.p0list.indexOfTopLevelItem(item)
            if found:
                self.data[indx] = (key, mods, 'U', cmnd, self.omsdict[cmnd])
            else:
                newdata = [x for x in self.data.values()]
                # TODO: fix error when modifying TC keydef
                # UnboundLocalError: local variable 'key' referenced before assignment
                newvalue = (key, mods, 'U', cmnd, self.omsdict[cmnd])
                newdata.append(newvalue)
                newdata.sort()
                for x, y in enumerate(newdata):
                    if y == newvalue:
                        indx = x
                    self.data[x] = y
            self.modified = True
            self._origdata = self.init_origdata
            if 'C_KEY' in self.fields:
                self._origdata[self.ix_key] = key
            if 'C_MODS' in self.fields:
                for mod, indx in zip(('WCAS'), self.ix_mods):
                    self._origdata[indx] = mod in mods
            if 'C_CMD' in self.fields:
                self._origdata[self.ix_cmd] = cmnd
            if 'C_CNTXT' in self.fields:
                self._origdata[self.ix_cntxt] = context
            try:
                self._keys.on_extra_selected(self, item)  # user exit
            except AttributeError:
                pass
            newitem = self.p0list.topLevelItem(pos)
            self.populate_list(pos)    # refresh
        self.refresh_extrascreen(newitem)
        self.initializing_keydef = False

    def on_update(self):
        """callback for editing kb shortcut
        """
        self.do_modification()
        self.p0list.setFocus()

    def on_delete(self):
        """callback for deleting kb shortcut
        """
        self.do_modification(delete=True)
        self.p0list.setFocus()

    def refresh_extrascreen(self, selitem):
        """show new values after changing kb shortcut
        """
        if not selitem:  # bv. bij p0list.clear()
            return
        seli = selitem.data(0, core.Qt.UserRole)
        if sys.version < '3':
            seli = seli.toPyObject()
        keydefdata = self.data[seli]
        if 'C_CMD' in self.fields:
            self.b_save.setEnabled(False)
            self.b_del.setEnabled(False)
        self._origdata = self.init_origdata[:]
        for indx, item in enumerate(keydefdata):
            if self.column_info[indx][0] == 'C_KEY':
                key = item
                if self.keylist is None:
                    self.txt_key.setText(key)
                else:
                    ix = self.keylist.index(key)
                    self.cmb_key.setCurrentIndex(ix)
                self._origdata[self.ix_key] = key
            elif self.column_info[indx][0] == 'C_MODS':
                mods = item
                self.cb_shift.setChecked(False)
                self.cb_ctrl.setChecked(False)
                self.cb_alt.setChecked(False)
                self.cb_win.setChecked(False)
                for x, y, z in zip('SCAW', self.ix_mods, (self.cb_shift, self.cb_ctrl,
                                                          self.cb_alt, self.cb_win)):
                    if x in mods:
                        self._origdata[y] = True
                        z.setChecked(True)
            elif self.column_info[indx][0] == 'C_TYPE':
                soort = item
                if soort == 'U':
                    self.b_del.setEnabled(True)
            elif self.column_info[indx][0] == 'C_CNTXT':
                context = item
                ix = self.contextslist.index(context)
                self.cmb_context.setCurrentIndex(ix)
                self._origdata[self.ix_cntxt] = context
            elif self.column_info[indx][0] == 'C_CMD':
                command = item
                if 'C_CNTXT' in self.fields:
                    self.cmb_commando.clear()
                    context = self.cmb_context.currentText()
                    actionslist = self.contextactionsdict[context]
                    self.cmb_commando.addItems(actionslist)
                    ix = actionslist.index(command)
                else:
                    ix = self.commandslist.index(command)
                self.cmb_commando.setCurrentIndex(ix)
                self._origdata[self.ix_cmd] = command
            elif self.column_info[indx][0] == 'C_DESC':
                oms = item
                self.txt_oms.setText(oms)
            else:
                try:
                    self._keys.vul_extra_details(self, indx, item)  # user exit
                except AttributeError:
                    pass
        self._newdata = self._origdata[:]

    def do_modification(self, delete=False):  # TODO
        """currently this only works for tcmdrkys
        """
        print("Aanpassen uitgezet, werkt nog niet voor alles")
        return
        item = self.p0list.currentItem()
        pos = self.p0list.indexOfTopLevelItem(item)
        if delete:
            indx = item.data(0, core.Qt.UserRole)
            if sys.version < '3':
                indx = int(indx.toPyObject())
            if self.captions["{:03}".format(indx)] == 'C_TYPE':
                if self.data[indx][1] == "S":  # can't delete standard key
                    show_message(self.parent, 'I_STDDEF')
                    return
            elif self.captions["{:03}".format(indx)] == 'C_KEY':
                if self.data[indx][0] in self.defkeys:  # restore standard if any
                    cmnd = self.defkeys[self.data[indx][0]]
                    if cmnd in self.omsdict:
                        oms = self.omsdict[cmnd]
                    else:
                        oms, cmnd = cmnd, ""
                    self.data[indx] = (key, 'S', cmnd, oms)  # key UNDEF
                else:
                    del self.data[indx]
                    ## pos -= 1
            self.b_save.setEnabled(False)
            self.b_del.setEnabled(False)
            self.set_title(modified=True)
            self.populate_list(pos)    # refresh
        else:
            self.on_item_selected(item, item)  # , from_update=True)


class ChoiceBook(qtw.QFrame):
    """ Als QTabwidget, maar met selector in plaats van tabs
    """
    def __init__(self, parent, plugins):
        self.plugins = plugins
        self.parent = parent
        super().__init__(parent)
        self.sel = qtw.QComboBox(self)
        self.sel.currentIndexChanged.connect(self.on_page_changed)
        self.find = qtw.QComboBox(self)
        self.find.setMinimumContentsLength(20)
        self.find.setEditable(True)
        self.find.editTextChanged.connect(self.on_text_changed)
        self.b_next = qtw.QPushButton("", self)
        self.b_next.clicked.connect(self.find_next)
        self.b_next.setEnabled(False)
        self.b_prev = qtw.QPushButton('', self)
        self.b_prev.clicked.connect(self.find_prev)
        self.b_prev.setEnabled(False)
        self.b_filter = qtw.QPushButton(self.parent.captions['C_FILTER'], self)
        self.b_filter.clicked.connect(self.filter)
        self.b_filter.setEnabled(False)
        self.filter_on = False
        self.pnl = qtw.QStackedWidget(self)
        for txt, loc in self.plugins:
            if not os.path.exists(loc):
                loc = os.path.join(BASE, loc)
            win = HotkeyPanel(self, loc)
            self.pnl.addWidget(win)
            if not all((win.settings, win.column_info, win.data)):
                fl = ''
            else:
                fl = win._keys.__file__
            self.parent.pluginfiles[txt] = (loc, fl)
            self.sel.addItem(txt)
        self.b_exit = qtw.QPushButton(self.parent.captions['C_EXIT'], self)
        self.b_exit.clicked.connect(self.parent.exit)

        box = qtw.QVBoxLayout()
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addSpacing(10)
        self.sel_text = qtw.QLabel("", self)
        hbox.addWidget(self.sel_text)
        hbox.addWidget(self.sel)
        hbox.addStretch()
        self.find_text = qtw.QLabel("", self)
        hbox.addWidget(self.find_text)
        hbox.addWidget(self.find)
        hbox.addWidget(self.b_filter)
        hbox.addWidget(self.b_next)
        hbox.addWidget(self.b_prev)
        hbox.addSpacing(10)
        vbox.addLayout(hbox)
        box.addLayout(vbox)
        hbox = qtw.QVBoxLayout()
        hbox.addWidget(self.pnl)
        box.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.b_exit)
        hbox.addStretch()
        box.addLayout(hbox)

        self.setLayout(box)
        self.setcaptions()

    def setcaptions(self):
        """update captions according to selected language
        """
        self.b_next.setText(self.parent.captions['C_NEXT'])
        self.b_prev.setText(self.parent.captions['C_PREV'])
        self.sel_text.setText(self.parent.captions['C_SELPRG'])
        self.find_text.setText(self.parent.captions['C_FIND'])
        if self.filter_on:
            self.b_filter.setText(self.parent.captions['C_FLTOFF'])
        else:
            self.b_filter.setText(self.parent.captions['C_FILTER'])
        self.b_exit.setText(self.parent.captions['C_EXIT'])

    def on_page_changed(self, indx):
        """callback for change in tool page
        """
        page = self.pnl.currentWidget()
        if page is None:
            return
        self.parent.sb.showMessage(self.parent.captions["M_DESC"].format(
            self.sel.currentText()))
        if page.modified:
            ok = page.exit()
            if not ok:
                return
        self.pnl.setCurrentIndex(indx)
        self.parent.page = self.pnl.currentWidget()  # change to new selection
        self.parent.setup_menu()
        if not all((self.parent.page.settings, self.parent.page.column_info,
                    self.parent.page.data)):
            return
        if self.parent.page.filtertext:
            self.find.setEditText(self.parent.page.filtertext)
            self.b_filter.setText(self.parent.captions['C_FLTOFF'])
            self.b_filter.setEnabled(True)
        else:
            self.find.setEditText('')
            self.find.setEnabled(True)
            self.b_next.setEnabled(False)
            self.b_prev.setEnabled(False)
            self.b_filter.setEnabled(False)

    def on_text_changed(self, text):
        """callback for change in search text
        """
        page = self.parent.page  # self.pnl.currentWidget()
        for ix, item in enumerate(page.column_info):
            if item[0] == 'C_DESC':
                col = ix
                break
        self.items_found = page.p0list.findItems(text, core.Qt.MatchContains, col)
        self.b_next.setEnabled(False)
        self.b_prev.setEnabled(False)
        self.b_filter.setEnabled(False)
        if self.items_found:
            page.p0list.setCurrentItem(self.items_found[0])
            self.founditem = 0
            if len(self.items_found) < len(self.parent.page.data.items()):
                self.b_next.setEnabled(True)
                self.b_filter.setEnabled(True)
            self.parent.sb.showMessage(self.parent.captions["I_#FOUND"].format(
                len(self.items_found)))
        else:
            self.parent.sb.showMessage(self.parent.captions["I_NOTFND"].format(text))

    def find_next(self):
        """to next search result
        """
        self.b_prev.setEnabled(True)
        if self.founditem < len(self.items_found) - 1:
            self.founditem += 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])
        else:
            self.parent.sb.showMessage(self.parent.captions["I_NONXT"])
            self.b_next.setEnabled(False)

    def find_prev(self):
        """to previous search result
        """
        self.b_next.setEnabled(True)
        if self.founditem == 0:
            self.parent.sb.showMessage(self.parent.captions["I_NOPRV"])
            self.b_prev.setEnabled(False)
        else:
            self.founditem -= 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])

    def filter(self):
        """filter shown items according to search text
        """
        if not self.items_found:
            return
        state = str(self.b_filter.text())
        text = str(self.find.currentText())
        item = self.parent.page.p0list.currentItem()
        self.reposition = item.text(0), item.text(1)
        if state == self.parent.captions['C_FILTER']:
            state = self.parent.captions['C_FLTOFF']
            self.filter_on = True
            self.parent.page.filtertext = text
            self.parent.page.olddata = self.parent.page.data
            self.parent.page.data = {ix: item for ix, item in enumerate(
                self.parent.page.data.values()) if text.upper() in item[-1].upper()}
            self.b_next.setEnabled(False)
            self.b_prev.setEnabled(False)
            self.find.setEnabled(False)
        else:       # self.filter_on == True
            state = self.parent.captions['C_FILTER']
            self.filter_on = False
            self.parent.page.filtertext = ''
            self.parent.page.data = self.parent.page.olddata
            self.b_next.setEnabled(True)
            self.b_prev.setEnabled(True)
            self.find.setEnabled(True)
        self.parent.page.populate_list()
        for ix in range(self.parent.page.p0list.topLevelItemCount()):
            item = self.parent.page.p0list.topLevelItem(ix)
            if (item.text(0), item.text(1)) == self.reposition:
                self.parent.page.p0list.setCurrentItem(item)
                break
        self.b_filter.setText(state)
        if self.parent.page.data == self.parent.page.olddata:
            self.on_text_changed(text)  # reselect items_found after setting filter to off


class MainFrame(qtw.QMainWindow):
    """Hoofdscherm van de applicatie
    """
    def __init__(self, args):

        wid = 860 if hkc.LIN else 688
        hig = 594
        super().__init__()
        self.resize(wid, hig)
        self.sb = self.statusBar()

        self.menu_bar = self.menuBar()
        ini = args.conf or CONF
        self.ini = hkc.read_settings(ini)
        self.readcaptions(self.ini['lang'])  # set up defaults
        if self.ini['plugins'] == []:
            self.show_empty_screen()
            return

        self.pluginfiles = {}
        self.title = self.captions["T_MAIN"]
        self.setWindowTitle(self.title)
        self.sb.showMessage(self.captions["T_HELLO"].format(self.captions["T_MAIN"]))
        self.book = ChoiceBook(self, self.ini['plugins'])
        self.setCentralWidget(self.book)
        self.page = self.book.pnl.currentWidget()
        start = 0
        if 'initial' in self.ini and self.ini['initial'] != '':
            start = [x for x, y in self.ini['plugins']].index(self.ini['initial'])
        self.book.sel.setCurrentIndex(start)
        self.setcaptions()

    def show_empty_screen(self):
        """what to do when there's no data to show
        """
        text = qtw.QLabel(self.captions["EMPTY_CONFIG_TEXT"], self)
        self.setCentralWidget(text)
        self.resize(640, 80)
        self.show()

    def setup_menu(self):
        """build menus and actions
        """
        self.menu_bar.clear()
        self._menus = (
            ('M_APP', (
                ('M_SETT', ((
                    ('M_LOC', (m_loc, 'Ctrl+F')),
                    ('M_LANG', (m_lang, 'Ctrl+L')),
                    ('M_PREF', (m_pref, ''))
                ), '')),
                ('M_EXIT', (m_exit, 'Ctrl+Q')),
            )),
            ('M_TOOL', (
                ('M_SETT', ((
                    ('M_COL', (m_col, '')),
                    ('M_MISC', (m_tool, '')),
                    ('M_ENTR', (m_entry, '')),
                ), '')),
                ('M_READ', (m_read, 'Ctrl+R')),
                ('M_RBLD', (m_rebuild, 'Ctrl+B')),
                ('M_SAVE', (m_save, 'Ctrl+S')),
            )),
            ('M_HELP', (
                ('M_ABOUT', (m_about, 'Ctrl+H')),
            )))
        self._menuitems = {}  # []
        for title, items in self._menus:
            menu = self.menu_bar.addMenu(self.captions[title])
            self._menuitems[title] = menu
            for sel in items:
                if sel == -1:
                    menu.addSeparator()
                    continue
                else:
                    sel, values = sel
                    callback, shortcut = values
                    if callable(callback):
                        act = self.create_menuaction(sel, callback, shortcut)
                        menu.addAction(act)
                        self._menuitems[sel] = act
                    else:
                        submenu = menu.addMenu(self.captions[sel])
                        self._menuitems[sel] = submenu
                        for sel, values in callback:
                            callback, shortcut = values
                            act = self.create_menuaction(sel, callback, shortcut)
                            submenu.addAction(act)
                            self._menuitems[sel] = act

    def create_menuaction(self, sel, callback, shortcut):
        """return created action w. some special cases
        """
        act = qtw.QAction(self.captions[sel], self)
        act.triggered.connect(functools.partial(callback, self))
        act.setShortcut(shortcut)
        if sel == 'M_READ':
            if not self.page.data:
                act.setEnabled(False)
        if sel == 'M_RBLD':
            try:
                act.setEnabled(bool(int(self.page.settings[hkc.csv_rbldsett])))
            except KeyError:
                act.setEnabled(False)
        elif sel == 'M_SAVE':
            try:
                act.setEnabled(bool(int(self.page.settings[hkc.csv_redefsett])))
            except KeyError:
                act.setEnabled(False)
        return act

    def exit(self):  # , e=None):
        """quit the application
        """
        if not self.page.exit():
            return
        self.close()

    def close(self):
        """extra actions to perfrom on closing
        """
        ## print(self.ini)
        ## if 'initial' in self.ini and self.ini['initial'] not in self.ini['plugins']:
            ## if self.ini.get("startup", None) == hkc.mode_f:
                ## oldpref = self.ini["startup"]
                ## pref = self.ini['startup'] = hkc.mode_r
                ## hkc.change_setting('startup', oldpref, pref, self.ini['filename'])
        ## if self.ini.get("startup", None) == hkc.mode_r:
            ## oldpref = self.ini.get('initial', None)
            ## pref = self.book.sel.currentText()
            ## hkc.change_setting('initial', oldpref, pref, self.ini['filename'])
        super().close()

    def readcaptions(self, lang):
        """get captions from language file or settings
        """
        self.captions = hkc.readlang(lang)

    def set_title(self):
        """adjust title and modified flag
        """
        title = self.title
        if self.page.modified:
            title += ' ' + self.captions["T_MOD"]
        self.setWindowTitle(title)

    def setcaptions(self):
        """propagate captions to other parts of the application
        """
        self.set_title()
        for menu, item in self._menuitems.items():
            try:
                item.setTitle(self.captions[menu])
            except AttributeError:
                item.setText(self.captions[menu])
        self.book.setcaptions()
        self.page.setcaptions()


def main(args=None):
    """launch the application
    """
    app = qtw.QApplication(sys.argv)
    win = MainFrame(args)
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv[1:])
