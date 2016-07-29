# -*- coding: UTF-8 -*-
"""hotkeys.py

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
import shutil
import functools
import importlib
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

import editor.hotkeys_constants as hkc
#
# shared (menu) functions
#
def show_message(self, message_id='', text='', caption_id='000'):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    if message_id:
        text = self.captions[message_id]
    if not text:
        text = self.captions['026']
    ok = gui.QMessageBox.question(self, self.captions[caption_id], text,
        gui.QMessageBox.Yes | gui.QMessageBox.No | gui.QMessageBox.Cancel)
    return ok

def m_read(self):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    if not self.page.settings:
        gui.QMessageBox.information(self, self.captions['000'],
            self.captions['301'])
        return
    if not self.page.modified:
        doit = False
        h = show_message(self, '041')
        if h != gui.QMessageBox.Yes:
            return
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
    try:
        self.page.savekeys()
    except AttributeError:
        gui.QMessageBox.information(self, self.captions['000'],
            self.captions['303'])
        return
    gui.QMessageBox.information(self, self.captions['000'], self.captions['037'])

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
    if ok == gui.QDialog.Accepted:
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
        for indx, program in current_items: # we need to do this in reverse
            win = self.book.pnl.widget(indx)
            self.book.pnl.removeWidget(win)
            if program in new_programs:
                hlpdict[program] = win # keep the widget
            else:
                win.close() # lose the widget
        # add new ones, modify existing or leave them alone
        for indx, program in enumerate(new_programs):
            if program in current_programs:
                #compare the new and the existing path
                old_loc = current_paths[current_programs.index(program)]
                new_loc = new_paths[new_programs.index(program)]
                if new_loc == old_loc:  # unchanged
                    win = hlpdict[program]
                else: # take data from different location
                    win = HotkeyPanel(self.book, new_loc) or EmptyPanel(
                        self.book.pnl, self.captions["052"].format(program))
            else: # new entry
                win = HotkeyPanel(self.book, new_paths[indx]) or EmptyPanel(
                    self.book.pnl, self.captions["052"].format(program))
            self.book.sel.addItem(program)
            self.book.pnl.addWidget(win)
        if self.last_added:
            selection = self.book.sel.findText(self.last_added)
        if selection > len(self.ini['plugins']) - 1:
            selection -= 1
        self.book.sel.setCurrentIndex(selection)

def m_user(self):
    """(menu) callback voor een nog niet geïmplementeerde actie"""
    return self.captions[NOT_IMPLEMENTED]

def m_rebuild(self):

    if not self.page.settings:
        gui.QMessageBox.information(self, self.captions['000'],
            self.captions['301'])
        return
    try:
        newdata = self.page._keys.buildcsv(self)
    except AttributeError:
        gui.QMessageBox.information(self, self.captions['000'],
            self.captions['304'])
        return
    if newdata:
        self.page.data = newdata[0]
        self.page.otherstuff = newdata[1]
        hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
            self.page.data)
        self.page.populate_list()

def m_tool(self):
    """define tool-specific settings
    """
    if not self.page.settings:
        self.page.settings = {x: ('', hkc.csv_oms[x]) for x in hkc.csv_settingnames}
    dlg = ExtraSettingsDialog(self).exec_()
    if dlg == gui.QDialog.Accepted:
        hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
            self.page.data)
        self._menuitems[hkc.M_SAVE].setEnabled(bool(
            int(self.page.settings[hkc.csv_redefsett][0])))
        self._menuitems[hkc.M_RBLD].setEnabled(bool(
            int(self.page.settings[hkc.csv_rbldsett][0])))

def m_col(self):
    """define tool-specific settings: column properties
    """
    if not self.page.settings:
        gui.QMessageBox.information(self, self.captions['000'],
            self.captions['301'])
        return
    dlg = ColumnSettingsDialog(self).exec_()
    if dlg == gui.QDialog.Accepted:
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
            self.page.data)
        if not self.page.data:
            return
        hdr = gui.QTreeWidgetItem()
        self.page.p0list.setHeaderItem(hdr)
        self.page.p0list.setHeaderLabels([self.captions[col[0]] for col in
            self.page.column_info])
        hdr = self.page.p0list.header()
        hdr.setClickable(True)
        for indx, col in enumerate(self.page.column_info):
            hdr.resizeSection(indx, col[1])
        hdr.setStretchLastSection(True)
        self.page.populate_list()

def m_entry(self):
    if not all((self.page.settings, self.page.column_info)):
        gui.QMessageBox.information(self, self.captions['000'],
            self.captions['302'])
        return
    dlg = EntryDialog(self).exec_()
    if dlg == gui.QDialog.Accepted:
        if self.page.data:
            hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                self.page.data)
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
    lang, ok = gui.QInputDialog.getItem(self, self.captions["000"],
        self.captions["027"], choices, current=indx, editable=False)
    if ok:
        hkc.change_setting('lang', oldlang, lang, self.ini['filename'])
        self.ini['lang'] = lang
        self.readcaptions(lang)
        self.setcaptions()

def m_about(self):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    text = '\n'.join(self.captions['057'].format(self.captions['071'],
        hkc.VRS, hkc.AUTH, self.captions['072']).split(' / '))
    info = gui.QMessageBox.information(self, self.captions['000'], text)

def m_pref(self):
    "mogelijkheid bieden om een tool op te geven dat default getoond wordt"
    oldpref = self.ini.get("initial", None)
    oldmode = self.ini.get("startup", None)
    self.prefs = oldmode, oldpref
    ok = InitialToolDialog(self).exec_()
    if ok == gui.QDialog.Accepted:
        mode, pref = self.prefs
        if mode:
            self.ini['startup'] = mode
            hkc.change_setting('startup', oldmode, mode, self.ini['filename'])
        if mode == 'Fixed':
            self.ini['initial'] = pref
            hkc.change_setting('initial', oldpref, pref, self.ini['filename'])

def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.exit()

#
# application classes (screens and subscreens)
#
class InitialToolDialog(gui.QDialog):
    def __init__(self, parent):
        self.parent = parent
        oldmode, oldpref = self.parent.prefs
        choices = [x[0] for x in self.parent.ini["plugins"]]
        indx = choices.index(oldpref) if oldpref in choices else 0
        gui.QDialog.__init__(self)
        self.setWindowTitle(self.parent.captions['000'])
        vbox = gui.QVBoxLayout()
        vbox.addWidget(gui.QLabel(self.parent.captions["217"], self))
        hbox = gui.QHBoxLayout()
        self.check_fixed = gui.QRadioButton(self.parent.captions["text_f"], self)
        self.check_fixed.setChecked(oldmode == hkc.mode_f)
        hbox.addWidget(self.check_fixed)
        self.sel_fixed = gui.QComboBox(self)
        self.sel_fixed.addItems(choices)
        self.sel_fixed.setEditable(True)
        self.sel_fixed.setCurrentIndex(indx)
        hbox.addWidget(self.sel_fixed)
        hbox.addStretch()
        vbox.addLayout(hbox)
        hbox = gui.QHBoxLayout()
        self.check_remember = gui.QRadioButton(self.parent.captions["text_r"], self)
        self.check_remember.setChecked(oldmode == hkc.mode_r)
        hbox.addWidget(self.check_remember)
        hbox.addStretch()
        vbox.addLayout(hbox)
        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(buttonbox)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def accept(self):
        if self.check_fixed.isChecked():
            mode = hkc.mode_f
        elif self.check_remember.isChecked():
            mode = hkc.mode_r
        else:
            mode = None
        pref = self.sel_fixed.currentText()
        self.parent.prefs = mode, pref
        gui.QDialog.accept(self)

class FileBrowseButton(gui.QFrame):
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
        gui.QFrame.__init__(self, parent)
        self.setFrameStyle(gui.QFrame.Panel | gui.QFrame.Raised);
        vbox = gui.QVBoxLayout()
        box = gui.QHBoxLayout()
        self.input = gui.QLineEdit(text, self)
        self.input.setMinimumWidth(200)
        box.addWidget(self.input)
        caption = self.parent.captions['058']
        self.button = gui.QPushButton(caption, self, clicked=self.browse)
        box.addWidget(self.button)
        vbox.addLayout(box)
        self.setLayout(vbox)

    def browse(self):
        startdir = str(self.input.text()) or os.getcwd()
        path = gui.QFileDialog.getOpenFileName(self,
            self.parent.captions['059'], startdir)
        if path:
            self.input.setText(path)

class SetupDialog(gui.QDialog):
    """dialoog voor het opzetten van een csv bestand

    geeft de mogelijkheid om alvast wat instellingen vast te leggen en zorgt er
    tevens voor dat het correcte formaat gebruikt wordt
    """
    def __init__(self, parent, name):
        self.parent = parent
        gui.QDialog.__init__(self)
        self.setWindowTitle(self.parent.parent.captions['031'])

        grid = gui.QGridLayout()

        text = gui.QLabel(self.parent.parent.captions['032A'].format(
            self.parent.parent.captions['032'].lower()), self)
        self.t_program = gui.QLineEdit('editor.plugins.{}_keys'.format(
            name.lower()), self)
        grid.addWidget(text, 1, 0, 1, 3)
        grid.addWidget(self.t_program, 1, 3) #, 1, 1)
        text = gui.QLabel(self.parent.parent.captions['033'], self)
        self.t_title = gui.QLineEdit(name + ' hotkeys', self)
        grid.addWidget(text, 2, 0, 1, 3)
        grid.addWidget(self.t_title, 2, 3) #, 1, 1)
        self.c_rebuild = gui.QCheckBox(self.parent.parent.captions['034'], self)
        grid.addWidget(self.c_rebuild, 3, 1, 1, 3)
        self.c_redef = gui.QCheckBox(self.parent.parent.captions['035'], self)
        grid.addWidget(self.c_redef, 4, 1, 1, 3)
        ## grid.addSpacer(5, 0, 1, 3)
        text = gui.QLabel(self.parent.parent.captions['036'], self)
        grid.addWidget(text, 5, 0, 1, 2)
        self.t_loc = FileBrowseButton(self, text =
            os.path.join('editor', 'plugins', name + "_hotkeys.csv"),
            level_down=True)
        grid.addWidget(self.t_loc, 5, 2, 1, 3)

        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)

        box = gui.QVBoxLayout()
        box.addStretch()
        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addLayout(grid)
        hbox.addStretch()
        box.addLayout(hbox)
        hbox = gui.QHBoxLayout()
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
            gui.QMessageBox.information(self, self.parent.title,
                self.captions['038'])
            return
        self.parent.loc = loc
        self.parent.data = [self.t_program.text(), self.t_title.text(),
            int(self.c_rebuild.isChecked()), int(self.c_redef.isChecked())]
        gui.QDialog.accept(self)

class ColumnSettingsDialog(gui.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent):
        self.parent = parent
        self.initializing = True
        gui.QDialog.__init__(self, parent)

        self.sizer = gui.QVBoxLayout()
        text = self.parent.captions['079'].format(
            self.parent.page.settings[hkc.csv_pnlsett][0])
        hsizer = gui.QHBoxLayout()
        label = gui.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(41)
        hsizer.addWidget(gui.QLabel(self.parent.captions['080'], self),
            alignment = core.Qt.AlignHCenter | core.Qt.AlignVCenter)
        hsizer.addSpacing(102) #82)
        hsizer.addWidget(gui.QLabel(self.parent.captions['081'], self),
            alignment = core.Qt.AlignVCenter)
        hsizer.addSpacing(8) # 84)
        hsizer.addWidget(gui.QLabel(self.parent.captions['082'], self),
            alignment = core.Qt.AlignVCenter)
        hsizer.addWidget(gui.QLabel(self.parent.captions['086'], self),
            alignment = core.Qt.AlignVCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        pnl = gui.QFrame(self)
        self.scrl = gui.QScrollArea(self)
        self.scrl.setWidget(pnl)
        self.scrl.setAlignment(core.Qt.AlignBottom)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()
        self.gsizer = gui.QVBoxLayout()
        self.rownum = 0 # indicates the number of rows in the gridlayout
        self.data, self.checks = [], []
        self.col_textids, self.col_names, self.last_textid = \
            hkc.read_columntitledata(self)
        for ix, item in enumerate(self.parent.page.column_info):
            item.append(ix)
            self.add_row(*item)
        box = gui.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(self.scrl)

        buttonbox = gui.QDialogButtonBox()
        # should be: add setting
        btn = buttonbox.addButton(self.parent.captions['084'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_column)
        # should be: remove checked settings
        btn = buttonbox.addButton(self.parent.captions['085'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.remove_columns)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)
        self.initializing = False

    def exec_(self):
        if self.last_textid == '099':
            # TODO: rethink this
            gui.QMessageBox.information(self, self.parent.title, "Can't perform "
                "this function: no language text identifiers below 100 left")
            self.reject()
        else:
            return super().exec_()

    def add_row(self, name='', width='', is_flag=False, colno=''):
        self.rownum += 1
        rownum = self.rownum #  - self.deleted
        colnum = 0
        check = gui.QCheckBox(self)
        ghsizer = gui.QHBoxLayout()
        ghsizer.addWidget(check, rownum)
        self.checks.append(check)
        colnum += 1
        w_name = gui.QComboBox(self)
        w_name.addItems(self.col_names)
        w_name.setEditable(True)
        if name:
            w_name.setCurrentIndex(self.col_textids.index(name))
        else:
            w_name.clearEditText()
        ghsizer.addWidget(w_name, rownum)
        colnum += 1
        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(20)
        w_width = gui.QSpinBox(self)
        w_width.setMaximum(999)
        if width:
            w_width.setValue(width)
        w_width.setFixedWidth(48)
        hsizer.addWidget(w_width)
        hsizer.addSpacing(20)
        ghsizer.addLayout(hsizer, rownum)
        colnum += 1
        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(40)
        w_flag = gui.QCheckBox(self)
        w_flag.setChecked(is_flag)
        w_flag.setFixedWidth(32)
        hsizer.addWidget(w_flag)
        hsizer.addSpacing(24)
        ghsizer.addLayout(hsizer, rownum)
        colnum += 1
        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(68)
        val = self.rownum if colno == '' else colno + 1
        w_colno = gui.QSpinBox(self)
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
        vbar.setMaximum(vbar.maximum() + 31)
        vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        self.rownum -= 1
        check = self.checks[rownum]
        for widgets in self.data[rownum:]:
            w_colno = widgets[2]
            w_colno.setValue(w_colno.value() - 1)
        w_name, w_width, w_colno, w_flag, _ = self.data[rownum]
        for widget in check, w_name, w_width, w_colno, w_flag:
            self.gsizer.removeWidget(widget)
            widget.close() # destroy()
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
        ok = gui.QMessageBox.question(self, self.parent.title,
            self.parent.captions['083'],
            gui.QMessageBox.Yes | gui.QMessageBox.No)
        if gui.QMessageBox.Yes:
            for row in reversed(checked):
                self.delete_row(row)


    def accept(self):
        column_info, new_titles = [], []
        lastcol = -1
        for ix, value in enumerate(sorted(self.data,  key=lambda x: x[2].value())):
            w_name, w_width, w_colno, w_flag, old_colno = value
            if w_colno.value() == lastcol:
                gui.QMessageBox.critical(self, self.parent.title,
                    self.parent.captions['305'])
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
        gui.QDialog.accept(self)

class ExtraSettingsDialog(gui.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent):
        self.parent = parent
        gui.QDialog.__init__(self, parent)
        ## self.resize(680, 400)

        self.sizer = gui.QVBoxLayout()

        pnl = gui.QFrame()
        vsizer = gui.QVBoxLayout()

        hsizer = gui.QHBoxLayout()
        text = gui.QLabel(self.parent.captions['032'], self)
        self.t_program = gui.QLineEdit(self.parent.page.settings[hkc.csv_plgsett][0],
            self)
        hsizer.addWidget(text)
        hsizer.addWidget(self.t_program)
        vsizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        text = gui.QLabel(self.parent.captions['033'], self)
        self.t_title = gui.QLineEdit(self.parent.page.settings[hkc.csv_pnlsett][0],
            self)
        hsizer.addWidget(text)
        hsizer.addWidget(self.t_title)
        vsizer.addLayout(hsizer)
        hsizer = gui.QHBoxLayout()
        self.c_rebuild = gui.QCheckBox(self.parent.captions['034'], self)
        if self.parent.page.settings[hkc.csv_rbldsett][0] == '1':
            self.c_rebuild.toggle()
        hsizer.addWidget(self.c_rebuild)
        vsizer.addLayout(hsizer)
        hsizer = gui.QHBoxLayout()
        self.c_redef = gui.QCheckBox(self.parent.captions['035'], self)
        if self.parent.page.settings[hkc.csv_redefsett][0] == '1':
            self.c_redef.toggle()
        hsizer.addWidget(self.c_redef)
        vsizer.addLayout(hsizer)
        pnl.setLayout(vsizer)
        pnl.setFrameStyle(gui.QFrame.Box | gui.QFrame.Raised)
        self.sizer.addWidget(pnl)

        pnl = gui.QFrame(self)
        vsizer = gui.QVBoxLayout()
        text = self.parent.captions['073'].format(
            self.parent.page.settings[hkc.csv_pnlsett][0])
        hsizer = gui.QHBoxLayout()
        label = gui.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(41)
        hsizer.addWidget(gui.QLabel(self.parent.captions['074'], self),
            alignment = core.Qt.AlignHCenter)
        hsizer.addSpacing(52)
        hsizer.addWidget(gui.QLabel(self.parent.captions['075'], self),
            alignment = core.Qt.AlignHCenter)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)

        pnl2 = gui.QFrame(self)
        self.scrl = gui.QScrollArea(self)
        self.scrl.setWidget(pnl2)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()

        self.gsizer = gui.QGridLayout()
        rownum = colnum = 0
        self.rownum = rownum
        self.data, self.checks = [], []
        for name, value in self.parent.page.settings.items():
            if name not in hkc.csv_settingnames:
                self.add_row(name, value)
        pnl2.setLayout(self.gsizer)
        pnl.setFrameStyle(gui.QFrame.Box)
        self.scrl.ensureVisible(0,0)
        vsizer.addWidget(self.scrl)

        hsizer =  gui.QHBoxLayout()
        hsizer.addStretch()
        btn = gui.QPushButton(self.parent.captions['076'])
        btn.clicked.connect(self.add_setting)
        hsizer.addWidget(btn)
        btn = gui.QPushButton(self.parent.captions['077'])
        btn.clicked.connect(self.remove_settings)
        hsizer.addWidget(btn)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)
        pnl.setLayout(vsizer)
        pnl.setFrameStyle(gui.QFrame.Box | gui.QFrame.Raised)
        self.sizer.addWidget(pnl)

        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)

    def add_row(self, name='', value=''):
        if value:
            value, desc = value
        else:
            desc = ''
        self.rownum += 1
        colnum = 0
        check = gui.QCheckBox(self)
        self.gsizer.addWidget(check, self.rownum, colnum)
        self.checks.append(check)
        colnum += 1
        w_name = gui.QLineEdit(name, self)
        w_name.setFixedWidth(88)
        if name:
            w_name.setReadOnly(True)
        ## w_name.setMaxLength(50)
        self.gsizer.addWidget(w_name, self.rownum, colnum)
        colnum += 1
        w_value = gui.QLineEdit(value, self)
        self.gsizer.addWidget(w_value, self.rownum, colnum)
        self.rownum += 1
        w_desc = gui.QLineEdit(desc, self)
        self.gsizer.addWidget(w_desc, self.rownum, colnum)
        self.data.append((w_name, w_value, w_desc))
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 62)
        vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        check = self.checks[rownum]
        w_name, w_value, w_desc = self.data[rownum]
        for widget in check, w_name, w_value, w_desc:
            self.gsizer.removeWidget(widget)
            widget.close() # destroy()
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
            ok = gui.QMessageBox.question(self, self.parent.title,
                self.parent.captions['078'],
                gui.QMessageBox.Yes | gui.QMessageBox.No)
            if gui.QMessageBox.Yes:
                for row in reversed(checked):
                    self.delete_row(row)

    def accept(self):
        oms = self.parent.page.settings[hkc.csv_plgsett][1]
        self.parent.page.settings[hkc.csv_plgsett] = (self.t_program.text(), oms)
        oms = self.parent.page.settings[hkc.csv_pnlsett][1]
        self.parent.page.settings[hkc.csv_pnlsett] = (self.t_title.text(), oms)
        oms = self.parent.page.settings[hkc.csv_rbldsett][1]
        value = '1' if self.c_rebuild.isChecked() else '0'
        self.parent.page.settings[hkc.csv_rbldsett] = (value, oms)
        oms = self.parent.page.settings[hkc.csv_redefsett][1]
        value = '1' if self.c_redef.isChecked() else '0'
        self.parent.page.settings[hkc.csv_redefsett] = (value, oms)

        settingsdict = {}
        for w_name, w_value, w_desc in self.data:
            settingsdict[w_name.text()] = (w_value.text(), w_desc.text())
        for setting in self.parent.page.settings:
            if setting not in hkc.csv_settingnames:
                del self.parent.page.settings[setting]
        self.parent.page.settings.update(settingsdict)

        gui.QDialog.accept(self)

class DeleteDialog(gui.QDialog):

    def __init__(self, parent):
        self.parent = parent
        self.last_added = ''
        gui.QDialog.__init__(self, parent)
        self.sizer = gui.QVBoxLayout()
        hsizer = gui.QHBoxLayout()
        label = gui.QLabel(self.parent.parent.captions['065'], self)
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        check = gui.QCheckBox(self.parent.parent.captions['306'], self)
        hsizer.addWidget(check)
        self.remove_keydefs = check
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        check = gui.QCheckBox(self.parent.parent.captions['307'], self)
        hsizer.addWidget(check)
        self.remove_plugin = check
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        self.sizer.addWidget(buttonbox)
        self.setLayout(self.sizer)

    def accept(self):
        self.parent.remove_data = self.remove_keydefs.isChecked()
        self.parent.remove_code = self.remove_plugin.isChecked()
        gui.QDialog.accept(self)

class FilesDialog(gui.QDialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, parent):
        self.parent = parent
        self.last_added = ''
        self.code_to_remove = []
        self.data_to_remove = []
        gui.QDialog.__init__(self, parent)
        self.resize(680, 400)

        self.sizer = gui.QVBoxLayout()
        text = '\n'.join((self.parent.captions['069'], self.parent.captions['070']))
        hsizer = gui.QHBoxLayout()
        label = gui.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = gui.QHBoxLayout()
        hsizer.addSpacing(36)
        hsizer.addWidget(gui.QLabel(self.parent.captions['060'], self),
            alignment = core.Qt.AlignHCenter | core.Qt.AlignVCenter)
        hsizer.addSpacing(84)
        hsizer.addWidget(gui.QLabel(self.parent.captions['061'], self),
            alignment = core.Qt.AlignVCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        pnl = gui.QFrame(self)
        self.scrl = gui.QScrollArea(self)
        self.scrl.setWidget(pnl)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()
        self.gsizer = gui.QGridLayout()
        rownum = colnum = 0
        self.rownum = rownum
        self.checks = []
        self.paths = []
        self.data = [] #
        self.pathdata = {}
        for name, path in self.parent.ini["plugins"]:
            self.add_row(name, path)
        box = gui.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(self.scrl)

        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton(self.parent.captions['062'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_program)
        btn = buttonbox.addButton(self.parent.captions['063'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.remove_programs)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)

    def add_row(self, name, path=''):
        self.rownum += 1
        colnum = 0
        check = gui.QCheckBox(name, self)
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
        check = self.checks[rownum]
        _, win = self.paths[rownum]
        self.gsizer.removeWidget(check)
        check.close() # destroy()
        self.gsizer.removeWidget(win)
        win.close() # destroy()
        self.checks.pop(rownum)
        self.paths.pop(rownum)

    def add_program(self):
        """nieuwe rij aanmaken in self.gsizer"""
        self.data = []
        newtool, ok = gui.QInputDialog.getText(self, self.parent.title,
            self.parent.captions['064'])
        if ok:
            if newtool == "":
                gui.QMessageBox.information(self, self.parent.title,
                    self.parent.captions['038'])
                return
            self.last_added = newtool
            ok = gui.QMessageBox.question(self, self.parent.title,
                self.parent.captions['039'],
                gui.QMessageBox.Yes | gui.QMessageBox.No, gui.QMessageBox.Yes)
            self.loc = ""
            if ok == gui.QMessageBox.Yes:
                ok = SetupDialog(self, newtool).exec_()
            self.add_row(newtool, path=self.loc)

    def remove_programs(self):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        checked = [(x, y.text()) for x, y in enumerate(self.checks)
            if y.isChecked()]
        if checked:
            dlg = DeleteDialog(self).exec_()
            if dlg == gui.QDialog.Accepted:
                for row, name in reversed(checked):
                    try:
                        csv_name, prg_name = self.parent.pluginfiles[name]
                    except KeyError:
                        csv_name, prgname = self.parent.ini['plugins'], None
                    if self.remove_data:
                        if csv_name:
                            self.data_to_remove.append(csv_name)
                    if self.remove_code:
                        if prg_name:
                            self.code_to_remove.append(prg_name)
                    self.delete_row(row)

    def accept(self):
        if self.last_added not in [x[0] for x in self.paths]:
            self.last_added = ''
        self.parent.last_added = self.last_added
        for filename in self.code_to_remove:
            os.remove(filename)
        for filename in self.data_to_remove:
            os.remove(filename)
        self.parent.ini["plugins"] = hkc.update_paths(self.paths, self.pathdata)
        gui.QDialog.accept(self)

class EntryDialog(gui.QDialog):

    def __init__(self, parent):
        self.parent = parent
        self.captions = self.parent.captions

        gui.QDialog.__init__(self, parent)
        self.resize(680, 400)

        # use self.parent.page.column_info to define grid
        names, widths = [], []
        for row in self.parent.page.column_info:
            names.append(self.captions[row[0]])
            widths.append(row[1])

        # use self.parent.page.data to populate grid
        self.data = self.parent.page.data

        self.p0list = gui.QTableWidget(self)
        self.p0list.setColumnCount(len(names))
        self.p0list.setHorizontalHeaderLabels(names)
        p0hdr = self.p0list.horizontalHeader()
        for indx, wid in enumerate(widths):
            p0hdr.resizeSection(indx, wid)
        num_rows = 0
        for rowkey, row in self.data.items():
            self.p0list.insertRow(num_rows)
            for i, element in enumerate(row):
                new_item = gui.QTableWidgetItem()
                new_item.setText(element)
                self.p0list.setItem(num_rows, i, new_item)
            num_rows += 1
        self.numrows = num_rows

        self.sizer = gui.QVBoxLayout()
        hsizer = gui.QHBoxLayout()
        hsizer.addWidget(self.p0list)
        self.sizer.addLayout(hsizer)

        buttonbox = gui.QDialogButtonBox()
        btn = buttonbox.addButton(self.captions['087'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.add_key)
        btn = buttonbox.addButton(self.captions['088'],
            gui.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.delete_key)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Ok)
        btn = buttonbox.addButton(gui.QDialogButtonBox.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = gui.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)

    def add_key(self):
        "add a line to the grid"
        self.p0list.insertRow(self.numrows)
        for i in range(self.p0list.columnCount()):
            new_item = gui.QTableWidgetItem()
            new_item.setText("")
            self.p0list.setItem(self.numrows, i, new_item)
        self.numrows += 1

    def delete_key(self):
        "remove selected line(s) from the grid"
        selected_rows = []
        for item in self.p0list.selectedRanges():
            for increment in range(item.rowCount()):
                selected_rows.append(item.topRow() + increment)
        for row in reversed(sorted(selected_rows)):
            self.p0list.removeRow(row)

    def accept(self):
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
        gui.QDialog.accept(self)


class DummyPanel(gui.QFrame):
    """
    Reimplement this class when a block of fields is needed in the screen
    to show details about the selected key and make it possible to change
    its definition
    """
    def __init__(self, parent):
        gui.QFrame.__init__(self)
        self.parent = parent
        self.initializing = False

    def add_extra_attributes(self):
        """
        Define extra instance attributes if needed
        """
        pass

    def add_extra_fields(self):
        """define other widgets to be used in the panel
        needed for showing details subpanel
        """
        pass

    def layout_extra_fields(self, sizer):
        """add extra widgets to self._sizer
        needed for showing details subpanel
        """
        pass

    def captions_extra_fields(self):
        """refresh captions for extra widgets
        needed for showing details subpanel
        """
        pass

    def vuldetails(self, value):
        """
        copy details of the selected key definition to the subpanel
        """
        pass

    def on_item_selected(self, olditem, newitem):
        """callback for list selection
        needed for copying details to subpanel
        """
        pass

    def aanpassen(self, delete=False):
        """
        copying details to the list after updating the subpanel
        """
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
        self.modified = False

        gui.QFrame.__init__(self, parent)
        self.parent = parent # .parent()
        self.captions = self.parent.parent.captions

        try:
            self.settings, self.column_info, self.data = hkc.readcsv(self.pad)
        except FileNotFoundError:
            self.settings, self.column_info, self.data = {}, [], {}
        self.otherstuff = {} # ruimte voor zaken als een lijst met mogelijke commando's

        nodata = False
        if not self.settings or not self.column_info:
            nodata = self.captions['044']
        else:
            modulename = self.settings[hkc.csv_plgsett][0]
            try:
                self._keys = importlib.import_module(modulename)
            except ImportError:
                nodata = self.captions['044'].replace('data', 'plugin code')
        if nodata:
            _sizer = gui.QVBoxLayout()
            hsizer = gui.QHBoxLayout()
            hsizer.addStretch()
            hsizer.addWidget(gui.QLabel(nodata, self))
            hsizer.addStretch()
            _sizer.addLayout(hsizer)
            self.setLayout(_sizer)
            return
        self.p0list = gui.QTreeWidget(self)
        try:
            self.parent.page = self
            self.otherstuff = self._keys.buildcsv(parent, showinfo=False)[1]
            ## with open('{}.otherstuff'.format(modulename), 'w') as _o:
                ## for item, value in self.otherstuff.items():
                    ## print(item, '→', value, file=_o)
        except AttributeError:
            pass
        try:
            self._panel = self._keys.MyPanel(self)
        except AttributeError:
            self._panel = DummyPanel(self)
        self.title = self.settings["PanelName"][0]

        # gelegenheid voor extra initialisaties en het opbouwen van de rest van de GUI
        # het vullen van veldwaarden hierin gebeurt als gevolg van het vullen
        # van de eerste rij in de listbox, daarom moet deze het laatst
        # self.otherstuff = self._keys.getotherstuff()
        self._panel.add_extra_attributes()
        self._panel.add_extra_fields()

        self._sizer = gui.QVBoxLayout()
        if self.column_info:
            self.p0list.setSortingEnabled(True)
            self.p0list.setHeaderLabels([self.captions[col[0]] for col in
                self.column_info])
            self.p0list.setAlternatingRowColors(True)
            self.p0list.currentItemChanged.connect(self._panel.on_item_selected)
            hdr = self.p0list.header()
            hdr.setClickable(True)
            for indx, col in enumerate(self.column_info):
                hdr.resizeSection(indx, col[1])
            hdr.setStretchLastSection(True)
            self.populate_list()
            sizer1 = gui.QHBoxLayout()
            sizer1.addWidget(self.p0list)
            self._sizer.addLayout(sizer1)

        # indien van toepassing: toevoegen van de rest van de GUI aan de layout
        self._panel.layout_extra_fields(self._sizer)

        self.setLayout(self._sizer)
        self._initializing = False
        self.filtertext = ''

    def readkeys(self):
        "(re)read the data for the keydef list"
        self.data = hkc.readcsv(self.pad)[2]

    def savekeys(self):
        "save modified keydef back"
        self.parent.data = self.data
        self._keys.savekeys(self)
        hkc.writecsv(self.pad, self.settings, self.column_info, self.data)
        self.modified = False
        self.setWindowTitle(self.captions["000"])

    def setcaptions(self):
        title = self.captions["000"]
        if self.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)

        if all((self.settings, self.column_info, self.data)):
            self._panel.captions_extra_fields()
        if self.data:
            self.populate_list()

    def populate_list(self, pos=0):
        """vullen van de list control
        """
        self.p0list.clear()
        items = self.data.items()
        if items is None or len(items) == 0:
            return

        self._panel.initializing = True
        for key, data in items:
            new_item = gui.QTreeWidgetItem()
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
        self._panel.initializing = False

    def exit(self):
        if self.modified:
            ok = show_message(self, '025')
            if ok == gui.QMessageBox.Yes:
                self.savekeys()
            elif ok == gui.QMessageBox.Cancel:
                return False
        return True

class EmptyPanel(HotkeyPanel):

    def __init__(self, parent, title="default_title"):

        coldata = ()
        self._txt = "default"
        HotkeyPanel.__init__(self, parent, coldata, ini="",
            title=title)

    def add_extra_fields(self):
        self.txt = gui.QLabel(self._txt, self)

    def layout_extra_fields(self):
        self._sizer.addWidget(self.txt)

    def readkeys(self):
        self.data = {}

    def savekeys(self):
        pass

class ChoiceBook(gui.QFrame):
    """ Als QTabwidget, maar met selector in plaats van tabs
    """
    def __init__(self, parent, plugins):
        self.plugins = plugins
        self.parent = parent
        gui.QFrame.__init__(self, parent)
        self.sel = gui.QComboBox(self)
        self.sel.currentIndexChanged.connect(self.on_page_changed)
        self.find = gui.QComboBox(self)
        self.find.setMinimumContentsLength(20)
        self.find.setEditable(True)
        self.find.editTextChanged.connect(self.on_text_changed)
        self.b_next = gui.QPushButton("", self)
        self.b_next.clicked.connect(self.find_next)
        self.b_next.setEnabled(False)
        self.b_prev = gui.QPushButton('', self)
        self.b_prev.clicked.connect(self.find_prev)
        self.b_prev.setEnabled(False)
        self.b_filter = gui.QPushButton(self.parent.captions['C_FILTER'], self)
        self.b_filter.clicked.connect(self.filter)
        self.b_filter.setEnabled(False)
        self.filter_on = False
        self.pnl = gui.QStackedWidget(self)
        for txt, loc in self.plugins:
            win = HotkeyPanel(self, loc)
            self.pnl.addWidget(win)
            if not all((win.settings, win.column_info, win.data)):
                fl = ''
            else:
                fl = win._keys.__file__
            self.parent.pluginfiles[txt] = (loc, fl)
            self.sel.addItem(txt)

        self.b_exit = gui.QPushButton(self.parent.captions['C_EXIT'], self)
        self.b_exit.clicked.connect(self.parent.exit)

        box = gui.QVBoxLayout()
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        hbox.addSpacing(10)
        self.sel_text = gui.QLabel("", self)
        hbox.addWidget(self.sel_text)
        hbox.addWidget(self.sel)
        hbox.addStretch()
        self.find_text = gui.QLabel("", self)
        hbox.addWidget(self.find_text)
        hbox.addWidget(self.find)
        hbox.addWidget(self.b_filter)
        hbox.addWidget(self.b_next)
        hbox.addWidget(self.b_prev)
        hbox.addSpacing(10)
        vbox.addLayout(hbox)
        box.addLayout(vbox)
        hbox = gui.QVBoxLayout()
        hbox.addWidget(self.pnl)
        box.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.b_exit)
        hbox.addStretch()
        box.addLayout(hbox)

        self.setLayout(box)
        self.setcaptions()

    def setcaptions(self):
        self.b_next.setText(self.parent.captions['C_NEXT'])
        self.b_prev.setText(self.parent.captions['C_PREV'])
        self.sel_text.setText(self.parent.captions['C_SEL'])
        self.find_text.setText(self.parent.captions['C_FIND'])
        if self.filter_on:
            self.b_filter.setText(self.parent.captions['C_FLTOFF'])
        else:
            self.b_filter.setText(self.parent.captions['C_FILTER'])
        self.b_exit.setText(self.parent.captions['C_EXIT'])

    def on_page_changed(self, indx):
        page = self.pnl.currentWidget() ## self.parent().page
        if page is None:
            return
        self.parent.sb.showMessage(self.parent.captions["053"].format(
            self.sel.currentText()))
        if page.modified:
            ok = page.exit()
            if not ok:
                return
        self.pnl.setCurrentIndex(indx)
        self.parent.page = self.pnl.currentWidget() # change to new selection
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
        page = self.parent.page # self.pnl.currentWidget()
        col = page.p0list.columnCount() - 1
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
            self.parent.sb.showMessage(self.parent.captions["067"].format(
                len(self.items_found)))
        else:
            self.parent.sb.showMessage(self.parent.captions["054"].format(text))

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
        item = self.parent.page.p0list.currentItem()
        self.reposition = item.text(0), item.text(1)
        if state == self.parent.captions['FILTER']:
            state = self.parent.captions['FLTOFF']
            self.filter_on = True
            self.parent.page.filtertext = text
            self.parent.page.olddata = self.parent.page.data
            self.parent.page.data = {ix: item for ix, item in enumerate(
                self.parent.page.data.values()) if text.upper() in item[-1].upper()}
            self.b_next.setEnabled(False)
            self.b_prev.setEnabled(False)
            self.find.setEnabled(False)
        else:       # self.filter_on == True
            state = self.parent.captions['FILTER']
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
            self.on_text_changed(text) # reselect items_found after setting filter to off

class MainFrame(gui.QMainWindow):
    """Hoofdscherm van de applicatie
    """
    def __init__(self, args):

        wid = 860 if hkc.LIN else 688
        hig = 594
        gui.QMainWindow.__init__(self)
        self.resize(wid, hig)
        self.sb = self.statusBar()

        self.menu_bar = self.menuBar()
        self.ini = hkc.read_settings(hkc.CONF)
        self.pluginfiles = {}

        self.readcaptions(self.ini['lang']) # set up defaults
        self.title = self.captions["000"]
        self.setWindowTitle(self.title)
        self.sb.showMessage(self.captions["089"].format(self.captions["000"]))
        self.book = ChoiceBook(self, self.ini['plugins']) # , size= (600, 700))
        self.setCentralWidget(self.book)
        self.page = self.book.pnl.currentWidget()
        start = 0
        if 'initial' in self.ini:
            start = [x for x, y in self.ini['plugins']].index(self.ini['initial'])
        self.book.sel.setCurrentIndex(start)
        self.setcaptions()
        self.show()

    def setup_menu(self):
        self.menu_bar.clear()
        self._menus = (
            ('M_APP', (
                ('M_SETT', ((
                    ('M_LOC', (m_loc, 'Ctrl+F')),
                    ('M_LANG', (m_lang, 'Ctrl+L')),
                    ('M_PREF', (m_pref, '')),
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
        self._menuitems = {} # []
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
        act = gui.QAction(self.captions[sel], self)
        act.triggered.connect(functools.partial(callback, self))
        act.setShortcut(shortcut)
        if sel == 'M_READ':
            if not self.page.data:
                act.setEnabled(False)
        if sel == 'M_RBLD':
            try:
                act.setEnabled(bool(int(self.page.settings[hkc.csv_rbldsett][0])))
            except KeyError:
                act.setEnabled(False)
        elif sel == 'M_SAVE':
            try:
                act.setEnabled(bool(int(self.page.settings[hkc.csv_redefsett][0])))
            except KeyError:
                act.setEnabled(False)
        return act

    def exit(self,e=None):
        if not self.page.exit():
            return
        self.close()

    def close(self):
        if self.ini['initial'] not in self.ini['plugins']:
            if self.ini.get("startup", None) == hkc.mode_f:
                oldpref = self.ini["startup"]
                pref = self.ini['startup'] = hkc.mode_r
                hkc.change_setting('startup', oldpref, pref, self.ini['filename'])
        if self.ini.get("startup", None) == hkc.mode_r:
            oldpref = self.ini.get('initial', None)
            pref = self.book.sel.currentText()
            hkc.change_setting('initial', oldpref, pref, self.ini['filename'])
        gui.QMainWindow.close(self)


    def readcaptions(self, lang):
        self.captions = {}
        with open(os.path.join(hkc.HERELANG, lang)) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value

    def setcaptions(self):
        title = self.captions["000"]
        if self.page.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)
        for menu, item in self._menuitems.items():
            try:
                item.setTitle(self.captions[menu])
            except AttributeError:
                item.setText(self.captions[menu])
        self.book.setcaptions()
        self.page.setcaptions()

def main(args=None):
    app = gui.QApplication(sys.argv)
    frame = MainFrame(args)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv[1:])
