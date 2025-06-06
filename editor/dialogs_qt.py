"""Dialog classes for hotkeys
"""
import os
import collections
import PyQt6.QtWidgets as qtw
## import PyQt6.QtGui as gui
import PyQt6.QtCore as core
from editor import shared


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


class InitialToolDialog(qtw.QDialog):
    """dialog to define which tool to show on startup
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        oldmode, oldpref = self.master.prefs
        choices = [x[0] for x in self.master.ini["plugins"]]
        indx = choices.index(oldpref) if oldpref in choices else 0
        super().__init__()
        self.setWindowTitle(self.master.title)
        vbox = qtw.QVBoxLayout()
        vbox.addWidget(qtw.QLabel(self.master.captions["M_PREF"], self))
        hbox = qtw.QHBoxLayout()
        self.check_fixed = qtw.QRadioButton(self.master.captions["T_FIXED"], self)
        self.check_fixed.setChecked(oldmode == shared.mode_f)
        hbox.addWidget(self.check_fixed)
        self.sel_fixed = qtw.QComboBox(self)
        self.sel_fixed.addItems(choices)
        self.sel_fixed.setEditable(True)
        self.sel_fixed.setCurrentIndex(indx)
        hbox.addWidget(self.sel_fixed)
        hbox.addStretch()
        vbox.addLayout(hbox)
        hbox = qtw.QHBoxLayout()
        self.check_remember = qtw.QRadioButton(self.master.captions["T_RMBR"], self)
        self.check_remember.setChecked(oldmode == shared.mode_r)
        hbox.addWidget(self.check_remember)
        hbox.addStretch()
        vbox.addLayout(hbox)
        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
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
        self.parent.master.accept_startupsettings(self.check_fixed.isChecked(),
                                                  self.check_remember.isChecked(),
                                                  self.sel_fixed.currentText())
        super().accept()


class FileBrowseButton(qtw.QFrame):
    """Combination widget showing a text field and a button
    making it possible to either manually enter a filename or select one using a FileDialog
    """
    def __init__(self, parent, text="", level_down=False):
        if level_down:
            self.parent = parent.parent.master
        else:
            self.parent = parent.master
        self.startdir = ''
        if text:
            self.startdir = os.path.dirname(text)
        super().__init__(parent)
        self.setWindowTitle(self.parent.title)
        self.setFrameStyle(qtw.QFrame.Shape.Panel | qtw.QFrame.Shadow.Raised)
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
        startdir = str(self.input.text()) or str(shared.HERE / 'plugins')
        path = qtw.QFileDialog.getOpenFileName(self, self.parent.captions['C_SELFIL'], startdir)
        if path[0]:
            self.input.setText(path[0])


class SetupDialog(qtw.QDialog):
    """dialoog voor het opzetten van een keydef bestand

    geeft de mogelijkheid om alvast wat instellingen vast te leggen en zorgt er
    tevens voor dat het correcte formaat gebruikt wordt
    """
    def __init__(self, parent, name):
        super().__init__()
        self.parent = parent
        self.setWindowTitle(self.parent.master.captions['T_INIKDEF'])

        grid = qtw.QGridLayout()

        text = qtw.QLabel(self.parent.master.captions['T_NAMOF'].format(
            self.parent.master.captions['S_PLGNAM'].lower(),
            self.parent.master.captions['T_ISMADE']), self)
        self.t_program = qtw.QLineEdit(f'editor.plugins.{name.lower()}_keys', self)
        grid.addWidget(text, 1, 0, 1, 3)
        grid.addWidget(self.t_program, 1, 3)  # , 1, 1)
        text = qtw.QLabel(self.parent.master.captions['S_PNLNAM'], self)
        self.t_title = qtw.QLineEdit(name + ' hotkeys', self)
        grid.addWidget(text, 2, 0, 1, 3)
        grid.addWidget(self.t_title, 2, 3)  # , 1, 1)
        self.c_rebuild = qtw.QCheckBox(self.parent.master.captions['T_MAKE'].format(
            self.parent.master.captions['S_RBLD']), self)
        grid.addWidget(self.c_rebuild, 3, 0, 1, 4)
        self.c_details = qtw.QCheckBox(self.parent.master.captions['S_DETS'])
        grid.addWidget(self.c_details, 4, 0, 1, 4)
        self.c_redef = qtw.QCheckBox(self.parent.master.captions['T_MAKE'].format(
            self.parent.master.captions['S_RSAV']), self)
        grid.addWidget(self.c_redef, 5, 0, 1, 4)
        text = qtw.QLabel(self.parent.master.captions['Q_SAVLOC'], self)
        grid.addWidget(text, 6, 0, 1, 2)
        suggest = os.path.join('editor', 'plugins', f"{name}_hotkeys.json")
        self.t_loc = FileBrowseButton(self, text=suggest, level_down=True)
        grid.addWidget(self.t_loc, 6, 2, 1, 3)

        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
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
        """set self.parent.loc to the chosen filename

        write the settings to this file along with some sample data - deferred to
        confirmation of the filesdialog
        """
        ok = self.parent.master.accept_pluginsettings(self.t_loc.input.text(),
                                                      self.t_program.text(),
                                                      self.t_title.text(),
                                                      self.c_rebuild.isChecked(),
                                                      self.c_details.isChecked(),
                                                      self.c_redef.isChecked())
        if ok:
            super().accept()


class DeleteDialog(qtw.QDialog):
    """dialog for deleting a tool from the collection
    """
    def __init__(self, parent):
        self.parent = parent
        self.parent.master.last_added = ''  # TODO uitzoeken: kan dit wel altijd
        super().__init__(parent)
        self.setWindowTitle(self.parent.master.title)
        self.sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(self.parent.master.captions['Q_REMPRG'], self)
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        check = qtw.QCheckBox(self.parent.master.captions['Q_REMKDEF'], self)
        hsizer.addWidget(check)
        self.remove_keydefs = check
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        check = qtw.QCheckBox(self.parent.master.captions['Q_REMPLG'], self)
        hsizer.addWidget(check)
        self.remove_plugin = check
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        buttonbox = qtw.QDialogButtonBox()
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
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
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        # self.title = self.master.title
        # self.last_added = ''
        self.code_to_remove = []
        self.data_to_remove = []
        super().__init__(parent)
        self.resize(680, 400)
        self.setWindowTitle(self.master.title)

        self.sizer = qtw.QVBoxLayout()
        text = '\n'.join(self.master.captions['T_TOOLS'].split(' / '))
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addSpacing(36)
        hsizer.addWidget(qtw.QLabel(self.master.captions['C_PRGNAM'], self),
                         alignment=core.Qt.AlignmentFlag.AlignHCenter
                         | core.Qt.AlignmentFlag.AlignVCenter)
        hsizer.addSpacing(84)
        hsizer.addWidget(qtw.QLabel(self.master.captions['C_KDEFLOC'], self),
                         alignment=core.Qt.AlignmentFlag.AlignVCenter)
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
        self.plugindata = []
        self.checks = []
        self.paths = []
        self.progs = []
        self.settingsdata = {}
        # settingsdata is een mapping van pluginnaam op een tuple van programmanaam en
        # andere settings (alleen als er een nieuw keydef file voor moet worden aangemaakt)
        for name, path in self.master.ini["plugins"]:
            self.add_row(name, path)
            self.settingsdata[name] = (self.master.pluginfiles[name],)
        box = qtw.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(self.scrl)

        buttonbox = qtw.QDialogButtonBox()
        btn = buttonbox.addButton(self.master.captions['C_ADDPRG'],
                                  qtw.QDialogButtonBox.ButtonRole.ActionRole)
        btn.clicked.connect(self.add_program)
        btn = buttonbox.addButton(self.master.captions['C_REMPRG'],
                                  qtw.QDialogButtonBox.ButtonRole.ActionRole)
        btn.clicked.connect(self.remove_programs)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
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
        # vbar = self.scrl.verticalScrollBar()
        # vbar.setMaximum(vbar.maximum() + 52)
        self.bar.setMaximum(self.bar.maximum() + 52)
        # vbar.setValue(vbar.maximum())
        self.bar.setValue(self.bar.maximum())

    def delete_row(self, rownum):
        """remove a tool location definition row
        """
        check = self.checks[rownum]
        name, win = self.paths[rownum]
        self.gsizer.removeWidget(check)
        check.close()
        self.gsizer.removeWidget(win)
        win.close()
        self.checks.pop(rownum)
        self.paths.pop(rownum)
        self.settingsdata.pop(name)

    def add_program(self):
        """nieuwe rij aanmaken in self.gsizer"""
        newtool, ok = get_textinput(self, '', self.master.captions['P_NEWPRG'])
        if ok:
            if newtool == "":
                show_message(self.parent, 'I_NEEDNAME')
                return
            self.master.last_added = newtool
            dataloc = prgloc = ""
            self.settingsdata[newtool] = (prgloc,)
            if ask_question(self.parent, 'P_INIKDEF'):
                ok = SetupDialog(self, newtool).exec()
                if ok:
                    self.settingsdata[newtool] = self.parent.data[1:]
                    prgloc = self.parent.data[1]
                    dataloc = self.parent.data[0]
            self.add_row(newtool, path=dataloc)

    def remove_programs(self):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        checked = [(x, y.text()) for x, y in enumerate(self.checks) if y.isChecked()]
        if checked:
            dlg = DeleteDialog(self).exec()
            if dlg == qtw.QDialog.DialogCode.Accepted:
                for row, name in reversed(checked):  # reversed niet nodig als ik checked niet aanpas
                    keydef_name, prg_name = '', ''
                    keydef_name = self.paths[row][1].input.text()
                    prg_name = self.settingsdata[name][0]
                    if self.remove_data and keydef_name:  # kan keydef_name wel leeg zijn?
                        self.data_to_remove.append(keydef_name)
                    if self.remove_code and prg_name:     # kan prg_name wel leeg zijn?
                        self.code_to_remove.append(prg_name.replace('.', '/') + '.py')
                    self.delete_row(row)

    def accept(self):
        """send updates to parent and leave
        """
        ok = self.master.accept_pathsettings([(x, y.input.text()) for x, y in self.paths],
                                             self.settingsdata,
                                             self.code_to_remove + self.data_to_remove)
        if ok:
            super().accept()


class ColumnSettingsDialog(qtw.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.initializing = True
        super().__init__(parent)
        self.setWindowTitle(self.master.title)

        self.sizer = qtw.QVBoxLayout()
        text = self.master.captions['T_COLSET'].format(
            self.master.book.page.settings[shared.SettType.PNL.value])
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addSpacing(41)
        hsizer.addWidget(qtw.QLabel(self.master.captions['C_TTL'], self),
                         alignment=core.Qt.AlignmentFlag.AlignHCenter | core.Qt.AlignmentFlag.AlignVCenter)
        hsizer.addSpacing(102)  # 82)
        hsizer.addWidget(qtw.QLabel(self.master.captions['C_WID'], self),
                         alignment=core.Qt.AlignmentFlag.AlignVCenter)
        hsizer.addSpacing(8)  # 84)
        hsizer.addWidget(qtw.QLabel(self.master.captions['C_IND'], self),
                         alignment=core.Qt.AlignmentFlag.AlignVCenter)
        hsizer.addWidget(qtw.QLabel(self.master.captions['C_SEQ'], self),
                         alignment=core.Qt.AlignmentFlag.AlignVCenter)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)

        pnl = qtw.QFrame(self)
        self.scrl = qtw.QScrollArea(self)
        self.scrl.setWidget(pnl)
        self.scrl.setAlignment(core.Qt.AlignmentFlag.AlignBottom)
        self.scrl.setWidgetResizable(True)
        self.bar = self.scrl.verticalScrollBar()
        self.gsizer = qtw.QVBoxLayout()
        self.rownum = 0  # indicates the number of rows in the gridlayout
        self.data, self.checks = [], []
        self.col_textids, self.col_names = self.master.col_textids, self.master.col_names
        for ix, item in enumerate(self.master.book.page.column_info):
            self.add_row(*item)
        box = qtw.QVBoxLayout()
        box.addLayout(self.gsizer)
        box.addStretch()
        pnl.setLayout(box)
        self.sizer.addWidget(self.scrl)

        buttonbox = qtw.QDialogButtonBox()
        btn = buttonbox.addButton(self.master.captions['C_ADDCOL'],
                                  qtw.QDialogButtonBox.ButtonRole.ActionRole)
        btn.clicked.connect(self.add_column)
        btn = buttonbox.addButton(self.master.captions['C_REMCOL'],
                                  qtw.QDialogButtonBox.ButtonRole.ActionRole)
        btn.clicked.connect(self.remove_columns)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        hsizer.addWidget(buttonbox)
        hsizer.addStretch()
        self.sizer.addLayout(hsizer)
        self.setLayout(self.sizer)
        self.initializing = False

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
        w_name.editTextChanged.connect(self.on_text_changed)
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
        # vbar = self.scrl.verticalScrollBar()
        # vbar.setMaximum(vbar.maximum() + 62)
        self.bar.setMaximum(self.bar.maximum() + 62)
        # vbar.setValue(vbar.maximum())
        self.bar.setValue(self.bar.maximum())

    def delete_row(self, rownum):
        """remove a column settings row
        """
        self.rownum -= 1
        check = self.checks[rownum]
        for widgets in self.data[rownum:]:
            w_colno = widgets[2]
            w_colno.setValue(w_colno.value() - 1)
        # w_name, w_width, w_colno, w_flag, _ = self.data[rownum]
        w_name, w_width, w_colno, w_flag = self.data[rownum][:4]
        for widget in check, w_name, w_width, w_colno, w_flag:
            self.gsizer.removeWidget(widget)
            widget.close()
        self.gsizer.removeItem(self.gsizer.itemAt(rownum))
        self.checks.pop(rownum)
        self.data.pop(rownum)

    def on_text_changed(self, text):
        "adjust column width based on length of column title"
        for w_name, w_width, *dummy in self.data:
            column_text = w_name.currentText()
            if column_text == text:
                w_width.setValue(10 * len(text))
                break

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
        data = [(x.currentText(), y.value(), b.isChecked(), a.value() - 1, c)
                for x, y, a, b, c in self.data]
        ok, cancel = self.master.accept_columnsettings(sorted(data, key=lambda x: x[3]))
        if ok:
            super().accept()


class NewColumnsDialog(qtw.QDialog):
    """dialoog voor aanmaken nieuwe kolom-ids
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.initializing = True
        super().__init__(parent)
        self.setWindowTitle(self.master.title)

        self.sizer = qtw.QVBoxLayout()
        text = '\n'.join(self.master.captions['T_TRANS'].split(' / '))
        hsizer = qtw.QHBoxLayout()
        hsizer.addWidget(qtw.QLabel(text, self))
        self.sizer.addLayout(hsizer)

        # maak een kop voor de id en een kop voor elke taal die ondersteund wordt
        gsizer = qtw.QGridLayout()
        row = col = 0
        gsizer.addWidget(qtw.QLabel('text id', self), row, col)
        for name in self.master.dialog_data['languages']:
            col += 1
            gsizer.addWidget(qtw.QLabel(name.split('.')[0].title(), self), row, col)

        # maak een regel voor elke nieuwe titel en neem de waarde over
        # tevens in de kolom die overeenkomt met de huidige taalinstelling
        # de betreffende text entry read-only maken
        self.widgets = []
        for item in self.master.dialog_data['new_titles']:
            row += 1
            entry_row = []
            for col in range(len(self.master.dialog_data['languages']) + 1):
                entry = qtw.QLineEdit(self)
                if col == 0:
                    text = self.master.dialog_data['textid']
                else:
                    text = item
                    if col == self.master.dialog_data['colno']:
                        entry.setEnabled(False)
                entry.setText(text)
                gsizer.addWidget(entry, row, col)
                entry_row.append(entry)
            self.widgets.append(entry_row)
        self.sizer.addLayout(gsizer)

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
        self.setLayout(self.sizer)
        self.initializing = False

    def accept(self):
        """save the changed settings and leave
        """
        entries = [[col.text() for col in row] for row in self.widgets]
        ok = self.master.accept_newcolumns(entries)
        if ok:
            super().accept()


class ExtraSettingsDialog(qtw.QDialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        # self.title = self.master.title
        self.captions = self.master.captions
        super().__init__(parent)
        ## self.resize(680, 400)
        self.setWindowTitle(self.master.title)

        self.sizer = qtw.QVBoxLayout()

        pnl = qtw.QFrame()
        vsizer = qtw.QVBoxLayout()

        hsizer = qtw.QHBoxLayout()
        text = qtw.QLabel(self.master.captions['S_PLGNAM'], self)
        self.t_program = qtw.QLineEdit(self.master.book.page.settings[shared.SettType.PLG.value],
                                       self)
        hsizer.addWidget(text)
        hsizer.addWidget(self.t_program)
        vsizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        text = qtw.QLabel(self.master.captions['S_PNLNAM'], self)
        self.t_title = qtw.QLineEdit(self.master.book.page.settings[shared.SettType.PNL.value],
                                     self)
        hsizer.addWidget(text)
        hsizer.addWidget(self.t_title)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        self.c_rebuild = qtw.QCheckBox(self.master.captions['T_MAKE'].format(
            self.master.captions['S_RBLD']), self)
        # if self.master.book.page.settings[shared.SettType.RBLD.value] == '1':
        #     self.c_rebuild.toggle()
        # met #1050 kan dit vereenvoudigd worden tot
        self.c_rebuild.setChecked(self.master.book.page.settings[shared.SettType.RBLD.value])
        hsizer.addWidget(self.c_rebuild)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        self.c_showdet = qtw.QCheckBox(self.master.captions['S_DETS'], self)
        # if self.master.book.page.settings[shared.SettType.DETS.value] == '1':
        #     self.c_showdet.toggle()
        # met #1050 kan dit vereenvoudigd worden tot
        self.c_showdet.setChecked(self.master.book.page.settings[shared.SettType.DETS.value])
        hsizer.addWidget(self.c_showdet)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        self.c_redef = qtw.QCheckBox(self.master.captions['T_MAKE'].format(
            self.master.captions['S_RSAV']), self)
        # if self.master.book.page.settings[shared.SettType.RDEF.value] == '1':
        #     self.c_redef.toggle()
        # met #1050 kan dit vereenvoudigd worden tot
        self.c_redef.setChecked(self.master.book.page.settings[shared.SettType.RDEF.value])
        hsizer.addWidget(self.c_redef)
        vsizer.addLayout(hsizer)
        pnl.setLayout(vsizer)
        pnl.setFrameStyle(qtw.QFrame.Shape.Box | qtw.QFrame.Shadow.Raised)
        self.sizer.addWidget(pnl)

        pnl = qtw.QFrame(self)
        vsizer = qtw.QVBoxLayout()
        text = self.master.captions['T_XTRASET'].format(
            self.master.book.page.settings[shared.SettType.PNL.value])
        hsizer = qtw.QHBoxLayout()
        label = qtw.QLabel(text, self)
        hsizer.addStretch()
        hsizer.addWidget(label)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addSpacing(41)
        hsizer.addWidget(qtw.QLabel(self.master.captions['C_NAM'], self),
                         alignment=core.Qt.AlignmentFlag.AlignHCenter)
        hsizer.addSpacing(52)
        hsizer.addWidget(qtw.QLabel(self.master.captions['C_VAL'], self),
                         alignment=core.Qt.AlignmentFlag.AlignHCenter)
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
        for name, value in self.master.book.page.settings.items():
            if name not in shared.settingnames and name != 'extra':
                try:
                    desc = self.master.book.page.settings['extra'][name]
                except KeyError:
                    desc = ''
                self.add_row(name, value, desc)
        pnl2.setLayout(self.gsizer)
        pnl.setFrameStyle(qtw.QFrame.Shape.Box)
        self.scrl.ensureVisible(0, 0)
        vsizer.addWidget(self.scrl)

        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        btn = qtw.QPushButton(self.master.captions['C_ADDSET'], self)
        btn.clicked.connect(self.add_setting)
        hsizer.addWidget(btn)
        btn = qtw.QPushButton(self.master.captions['C_REMSET'], self)
        btn.clicked.connect(self.remove_settings)
        hsizer.addWidget(btn)
        hsizer.addStretch()
        vsizer.addLayout(hsizer)
        pnl.setLayout(vsizer)
        pnl.setFrameStyle(qtw.QFrame.Shape.Box | qtw.QFrame.Shadow.Raised)
        self.sizer.addWidget(pnl)

        buttonbox = qtw.QDialogButtonBox()
        btn = buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Ok)
        btn = buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
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
        self.bar.setMaximum(self.bar.maximum() + 62)
        self.bar.setValue(self.bar.maximum())

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
        if any(test) and ask_question(self.parent, 'Q_REMSET'):
            for row in reversed(checked):
                self.delete_row(row)

    def accept(self):
        """update settings and leave
        """
        data = [(x.text(), y.text(), z.text()) for x, y, z in self.data]
        ok = self.master.accept_extrasettings(self.t_program.text(), self.t_title.text(),
                                              self.c_rebuild.isChecked(),
                                              self.c_showdet.isChecked(),
                                              self.c_redef.isChecked(), data)
        if not ok:
            self.c_showdet.setChecked(False)
            self.c_redef.setChecked(False)
        else:
            super().accept()


class EntryDialog(qtw.QDialog):
    """Dialog for Manual Entry
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.captions = self.master.captions

        super().__init__(parent)
        self.resize(680, 400)
        self.setWindowTitle(self.master.title + ": manual entry")

        self.sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        self.p0list = qtw.QTableWidget(self)

        # use self.parent.page.column_info to define grid
        names, widths = [], []
        for row in self.master.book.page.column_info:
            names.append(self.captions[row[0]])
            widths.append(row[1])
        self.p0list.setColumnCount(len(names))
        self.p0list.setHorizontalHeaderLabels(names)
        p0hdr = self.p0list.horizontalHeader()
        for indx, wid in enumerate(widths):
            p0hdr.resizeSection(indx, wid)

        # use self.master.page.data to populate grid
        self.data = self.master.book.page.data
        num_rows = 0
        for row in self.data.values():
            self.p0list.insertRow(num_rows)
            for i, element in enumerate(row):
                new_item = qtw.QTableWidgetItem()
                new_item.setText(element)
                self.p0list.setItem(num_rows, i, new_item)
            num_rows += 1
        self.numrows = num_rows

        hsizer.addWidget(self.p0list)
        self.sizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        hsizer.addStretch()
        buttonbox = qtw.QDialogButtonBox()
        btn = buttonbox.addButton(self.captions['C_ADDKEY'],
                                  qtw.QDialogButtonBox.ButtonRole.ActionRole)
        btn.clicked.connect(self.add_key)
        btn = buttonbox.addButton(self.captions['C_REMKEY'],
                                  qtw.QDialogButtonBox.ButtonRole.ActionRole)
        btn.clicked.connect(self.delete_key)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Save)
        buttonbox.addButton(qtw.QDialogButtonBox.StandardButton.Cancel)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
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
        new_values = collections.defaultdict(list)
        for rowid in range(self.p0list.rowCount()):
            for colid in range(self.p0list.columnCount()):
                value = self.p0list.item(rowid, colid).text()
                new_values[rowid + 1].append(value.replace('\\n', '\n'))
        self.master.book.page.data = new_values
        super().accept()


class CompleteDialog(qtw.QDialog):
    """Model dialog for entering / completing command descriptions
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        ## self.captions = self.parent.captions

        super().__init__(parent)
        self.resize(1100, 700)
        self.setWindowTitle(self.master.title + ": edit descriptions")

        self.read_data()

        self.sizer = qtw.QVBoxLayout()
        hsizer = qtw.QHBoxLayout()
        self.p0list = qtw.QTableWidget(len(self.cmds), 3, self)
        self.p0list.setHorizontalHeaderLabels([shared.get_text(self.parent, 'C_CMD'),
                                               shared.get_text(self.parent, 'C_DESC'),
                                               'value from earlier modification'])
        hdr = self.p0list.horizontalHeader()
        hdr.setStretchLastSection(True)
        self.build_table()
        self.p0list.setColumnWidth(0, 260)
        self.p0list.setColumnWidth(1, 520)

        hsizer.addWidget(self.p0list)
        self.sizer.addLayout(hsizer)

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
        self.setLayout(self.sizer)
        self.p0list.setCurrentCell(0, 1)  # self.p0list.setCurrentItem(itemAt(0,1))

    def read_data(self):  # *args):
        """lees eventuele extra commando's
        """
        self.cmds = self.master.book.page.descriptions
        self.desc = self.master.book.page.otherstuff.get('olddescs', {})
        # overgebleven afwijkende descriptions

    def build_table(self):
        "vul de tabel met in te voeren gegevens"
        # breakpoint()
        row = 0
        for key, desc in sorted(self.cmds.items()):
            new_item = qtw.QTableWidgetItem()
            new_item.setText(key)
            new_item.setFlags(new_item.flags() ^ core.Qt.ItemFlag.ItemIsEditable)
            self.p0list.setItem(row, 0, new_item)
            new_item = qtw.QTableWidgetItem()
            new_item.setText(desc)
            self.p0list.setItem(row, 1, new_item)
            new_item = qtw.QTableWidgetItem()
            olddesc = self.desc[key] if key in self.desc and self.desc[key] != desc else ''
            new_item.setText(olddesc)
            new_item.setFlags(new_item.flags() ^ core.Qt.ItemFlag.ItemIsEditable)
            self.p0list.setItem(row, 2, new_item)
            row += 1

    def accept(self):
        """confirm changes
        """
        new_values = {}
        for rowid in range(self.p0list.rowCount()):
            cmd = self.p0list.item(rowid, 0).text()
            desc = self.p0list.item(rowid, 1).text()
            new_values[cmd] = desc
        self.master.dialog_data = new_values
        qtw.QDialog.accept(self)


def show_dialog(win, cls):
    "show a dialog and return confirmation"
    ok = cls(win.gui, win).exec()
    return ok == qtw.QDialog.DialogCode.Accepted
