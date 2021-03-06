"""Dialog classes for hotkeys
"""
import os
import importlib
import importlib.util
import logging
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
import PyQt5.QtCore as core
import editor.hotkeys_constants as hkc


def get_text(win, message_id, text, args):
    """retourneer de tekst geïdentificeerd door <message_id>
    als <text> is opgegeven wordt die gebruikt
    <args> bevat een list van waarden die in de tekst kunnen worden ingevuld
    """
    if message_id:
        text = win.captions[message_id].replace(' / ', '\n')
    elif not text:
        text = win.captions['I_NOMSG']
        raise ValueError(text)
    if args:
        text = text.format(*args)
    return text


def show_message(win, message_id='', text='', args=None):
    """toon een boodschap in een dialoog
    """
    text = get_text(win, message_id, text, args)
    qtw.QMessageBox.information(win, win.title, text)
    return


def ask_question(win, message_id='', text='', args=None):
    """toon een vraag in een dialoog en retourneer het antwoord (Yes als True, No als False)
    na sluiten van de dialoog
    """
    text = get_text(win, message_id, text, args)
    ok = qtw.QMessageBox.question(win, win.title, text,
                                  qtw.QMessageBox.Yes | qtw.QMessageBox.No,
                                  qtw.QMessageBox.Yes)
    return ok == qtw.QMessageBox.Yes


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
        self.parent.data = []
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
        self.t_loc = FileBrowseButton(self,
                                      text=os.path.join('editor', 'plugins',
                                                        name + "_hotkeys.csv"),
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
        write the settings to this file along with some sample data - deferred to
        confirmation of the filesdialog
        """
        cloc = self.t_loc.input.text()
        ploc = self.t_program.text()
        if cloc == "":
            show_message(self.parent.parent, 'I_NEEDNAME')
            return
        cloc = os.path.abspath(cloc)
        if os.path.exists(cloc):
            show_message(self.parent.parent, 'I_GOTSETFIL', args=[cloc])
            return
        if importlib.util.find_spec(ploc):
            show_message(self.parent.parent, 'I_GOTPLGFIL', args=[ploc])
            return
        self.parent.loc = cloc
        self.parent.data = [ploc, self.t_title.text(),
                            int(self.c_rebuild.isChecked()),
                            int(self.c_details.isChecked()),
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
            self.parent.page.settings[hkc.SettType.PNL.value])
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
        self.title = self.parent.title
        self.captions = self.parent.captions
        super().__init__(parent)
        ## self.resize(680, 400)

        self.sizer = qtw.QVBoxLayout()

        pnl = qtw.QFrame()
        vsizer = qtw.QVBoxLayout()

        hsizer = qtw.QHBoxLayout()
        text = qtw.QLabel(self.parent.captions['S_PLGNAM'], self)
        self.t_program = qtw.QLineEdit(self.parent.page.settings[hkc.SettType.PLG.value],
                                       self)
        hsizer.addWidget(text)
        hsizer.addWidget(self.t_program)
        vsizer.addLayout(hsizer)

        hsizer = qtw.QHBoxLayout()
        text = qtw.QLabel(self.parent.captions['S_PNLNAM'], self)
        self.t_title = qtw.QLineEdit(self.parent.page.settings[hkc.SettType.PNL.value],
                                     self)
        hsizer.addWidget(text)
        hsizer.addWidget(self.t_title)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        self.c_rebuild = qtw.QCheckBox(self.parent.captions['T_MAKE'].format(
            self.parent.captions['S_RBLD']), self)
        if self.parent.page.settings[hkc.SettType.RBLD.value] == '1':
            self.c_rebuild.toggle()
        hsizer.addWidget(self.c_rebuild)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        self.c_showdet = qtw.QCheckBox(self.parent.captions['S_DETS'], self)
        try:
            if self.parent.page.settings[hkc.SettType.DETS.value] == '1':
                self.c_showdet.toggle()
        except KeyError:
            pass
        hsizer.addWidget(self.c_showdet)
        vsizer.addLayout(hsizer)
        hsizer = qtw.QHBoxLayout()
        self.c_redef = qtw.QCheckBox(self.parent.captions['T_MAKE'].format(
            self.parent.captions['S_RSAV']), self)
        if self.parent.page.settings[hkc.SettType.RDEF.value] == '1':
            self.c_redef.toggle()
        hsizer.addWidget(self.c_redef)
        vsizer.addLayout(hsizer)
        pnl.setLayout(vsizer)
        pnl.setFrameStyle(qtw.QFrame.Box | qtw.QFrame.Raised)
        self.sizer.addWidget(pnl)

        pnl = qtw.QFrame(self)
        vsizer = qtw.QVBoxLayout()
        text = self.parent.captions['T_XTRASET'].format(
            self.parent.page.settings[hkc.SettType.PNL.value])
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
        for name, value in self.parent.page.settings.items():
            if name not in hkc.csv_settingnames and name != 'extra':
                try:
                    desc = self.parent.page.settings['extra'][name]
                except KeyError:
                    desc = ''
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
        if self.c_redef.isChecked() and not self.c_showdet.isChecked():
            show_message(self, "I_NODET")
            return
        if self.c_showdet.isChecked():
            try:
                test = self.parent.page._keys.add_extra_attributes
            except AttributeError:
                self.c_showdet.setChecked(False)
                self.c_redef.setChecked(False)
                show_message(self, "I_IMPLXTRA")
                return
        self.parent.page.settings[hkc.SettType.PLG.value] = self.t_program.text()
        self.parent.page.settings[hkc.SettType.PNL.value] = self.t_title.text()
        value = '1' if self.c_rebuild.isChecked() else '0'
        self.parent.page.settings[hkc.SettType.RBLD.value] = value
        value = '1' if self.c_showdet.isChecked() else '0'
        self.parent.page.settings[hkc.SettType.DETS.value] = value
        value = '1' if self.c_redef.isChecked() else '0'
        self.parent.page.settings[hkc.SettType.RDEF.value] = value

        settingsdict, settdescdict = {}, {}
        for w_name, w_value, w_desc in self.data:
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
        self.title = self.parent.title
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
        self.plugindata = []
        self.checks = []
        self.paths = []
        self.progs = []
        self.settingsdata = {}
        # settingsdata is een mapping van pluginnaam op een tuple van programmanaam en
        # andere settings (alleen als er een nieuw csv file voor moet worden aangemaakt)
        for name, path in self.parent.ini["plugins"]:
            self.add_row(name, path)
            self.settingsdata[name] = (self.parent.pluginfiles[name],)
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
        vbar = self.scrl.verticalScrollBar()
        vbar.setMaximum(vbar.maximum() + 52)
        vbar.setValue(vbar.maximum())

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
        newtool, ok = qtw.QInputDialog.getText(self, self.parent.title,
                                               self.parent.captions['P_NEWPRG'])
        if ok:
            if newtool == "":
                show_message(self.parent, 'I_NEEDNAME')
                return
            self.last_added = newtool
            self.loc = prgloc = ""
            self.settingsdata[newtool] = (prgloc,)
            if ask_question(self.parent, 'P_INICSV'):
                ok = SetupDialog(self, newtool).exec_()
                if ok:
                    self.settingsdata[newtool] = self.data
                    prgloc = self.data[0]
            self.add_row(newtool, path=self.loc)

    def remove_programs(self):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        checked = [(x, y.text()) for x, y in enumerate(self.checks)
                   if y.isChecked()]
        if checked:
            dlg = DeleteDialog(self).exec_()
            if dlg == qtw.QDialog.Accepted:
                for row, name in reversed(checked):
                    csv_name, prg_name = '', ''
                    try:
                        csv_name = self.paths[row][1].input.text()
                        prg_name = self.settingsdata[name][0]
                    except KeyError:
                        logging.exception('')
                    logging.info('csv name is %s', csv_name)
                    logging.info('prg name is %s', prg_name)
                    if self.remove_data:
                        if csv_name:
                            self.data_to_remove.append(csv_name)
                    if self.remove_code:
                        if prg_name:
                            self.code_to_remove.append(
                                prg_name.replace('.', '/') + '.py')
                    self.delete_row(row)

    def accept(self):
        """send updates to parent and leave
        """
        if self.last_added not in [x[0] for x in self.paths]:
            self.last_added = ''
        self.parent.last_added = self.last_added
        for ix, entry in enumerate(self.paths):
            name, path = entry
            if name not in [x for x, y in self.parent.ini['plugins']]:
                csvname = path.input.text()
                if not csvname:
                    show_message(self, text='Please fill out all filenames')
                    return
                prgname = self.settingsdata[name][0]
                if not prgname:
                    # try to get the plugin name from the csv file
                    try:
                        data = hkc.readcsv(csvname)
                    except (FileNotFoundError, IsADirectoryError, ValueError):
                        show_message(self, text='{} does not seem to be a usable '
                                                'csv file'.format(csvname))
                        return
                    try:
                        prgname = data[0][hkc.SettType.PLG.value]
                    except KeyError:
                        show_message(self,
                                     text='{} does not contain a reference to a '
                                          'plugin (PluginName setting)'.format(csvname))
                        return
                if len(self.settingsdata[name]) == 1:  # existing plugin
                    try:
                        _ = importlib.import_module(prgname)
                    except ImportError:
                        show_message(self,
                                     text='{} does not contain a reference to a '
                                          'valid plugin'.format(csvname))
                        return

                self.parent.pluginfiles[name] = prgname
        for filename in self.code_to_remove + self.data_to_remove:
            os.remove(filename)
        self.newpathdata = {}
        for name, entry in self.settingsdata.items():
            if len(entry) > 1:
                self.newpathdata[name] = entry
        self.parent.ini["plugins"] = hkc.update_paths(self.paths, self.newpathdata,
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
