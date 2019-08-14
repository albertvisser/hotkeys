"""Hotkeys dialog code - wxPython version
"""
import importlib
import importlib.util
import wx
import wx.grid as wxg
import wx.lib.filebrowsebutton as wxfb
import editor.shared as shared


def show_message(win, message_id='', text=''):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    text = shared.get_text(win, message_id, text)
    wx.MessageBox(text, shared.get_title(win), parent=win)


def ask_question(win, message_id='', text='', args=None):
    """toon een vraag in een dialoog en retourneer het antwoord (Yes als True, No als False)
    na sluiten van de dialoog
    """
    text = shared.get_text(win, message_id, text, args)
    with wx.MessageDialog(win, text, shared.get_title(win),
                          wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION) as dlg:
        h = dlg.ShowModal()
    return h == wx.ID_YES


def ask_ync_question(win, message_id='', text='', args=None):
    """toon een vraag in een dialoog met drie mogelijkheden en retourneer het antwoord
    (Yes als (True, False), No als (False, False) en Cancel als (False, True)
    na sluiten van de dialoog
    """
    text = shared.get_text(win, message_id, text, args)
    with wx.MessageDialog(win, text, shared.get_title(win),
                          wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_QUESTION) as dlg:
        h = dlg.ShowModal()
    return h == wx.ID_YES, h == wx.ID_CANCEL


def get_textinput(win, text, prompt):
    """toon een dialoog waarin een regel tekst kan worden opgegeven en retourneer het antwoord
    (de opgegeven tekst en True bij OK) na sluiten van de dialoog
    """
    with wx.TextEntryDialog(win, text, prompt, value=text) as dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            text = dlg.GetValue()
    return text, ok == wx.ID_OK


def get_choice(win, title, caption, choices, current):
    """toon een dialoog waarin een waarde gekozen kan worden uit een lijst en retourneer het
    antwoord (de geselecteerde waarde en True bij OK) na sluiten van de dialoog
    """
    text = ''
    with wx.SingleChoiceDialog(win, title, caption, choices) as dlg:
        dlg.SetSelection(current)
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            text = dlg.GetStringSelection()
    return text, ok == wx.ID_OK


class InitialToolDialog(wx.Dialog):
    """dialog to define which tool to show on startup
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        oldmode, oldpref = self.master.prefs
        choices = [x[0] for x in self.master.ini["plugins"]]
        # indx = choices.index(oldpref) if oldpref in choices else 0
        super().__init__(parent, title=self.master.title)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(wx.StaticText(self, label=self.master.captions["M_PREF"]), 0, wx.TOP | wx.LEFT, 5)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.check_fixed = wx.RadioButton(self, label=self.master.captions["T_FIXED"])
        self.check_fixed.SetValue(oldmode == shared.mode_f)
        hbox.Add(self.check_fixed, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 5)
        self.sel_fixed = wx.ComboBox(self, size=(140, -1), style=wx.CB_DROPDOWN, choices=choices)
        self.sel_fixed.SetValue(oldpref)
        hbox.Add(self.sel_fixed, 0, wx.ALIGN_RIGHT | wx.RIGHT, 5)
        vbox.Add(hbox, 0, wx.TOP, 2)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.check_remember = wx.RadioButton(self, label=self.master.captions["T_RMBR"])
        self.check_remember.SetValue(oldmode == shared.mode_r)
        hbox.Add(self.check_remember, 0, wx.LEFT, 5)
        vbox.Add(hbox, 0, wx.TOP | wx.BOTTOM, 2)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 2)
        vbox.SetSizeHints(self)
        self.SetSizer(vbox)
        # self.SetAutoLayout(vbox)

    def accept(self):
        """confirm dialog
        """
        if self.check_fixed.GetValue():
            mode = shared.mode_f
        elif self.check_remember.GetValue():
            mode = shared.mode_r
        else:
            mode = None
        pref = self.sel_fixed.GetStringSelection()
        self.master.prefs = mode, pref


class FileBrowseButton(wx.Frame): # note: wx has this built in
    """Combination widget showing a text field and a button
    making it possible to either manually enter a filename or select
    one using a FileDialog
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
        self.setFrameStyle(wx.Frame.Panel | qtw.QFrame.Raised)
        vbox = wx.BoxSizer(wx.VERTICAL)()
        box = wx.BoxSizer(wx.HORIZONTAL)()
        self.input = wx.LineEdit(text, self)
        self.input.setMinimumWidth(200)
        box.Add(self.input)
        caption = self.parent.captions['C_BRWS']
        self.button = wx.PushButton(caption, self, clicked=self.browse)
        box.Add(self.button)
        vbox.Add(box)
        self.SetSizer(vbox)

    def browse(self):
        """callback for button
        """
        startdir = str(self.input.text()) or os.getcwd()
        path = wx.FileDialog.getOpenFileName(self, self.parent.captions['C_SELFIL'], startdir)
        if path[0]:
            self.input.setText(path[0])


class SetupDialog(wx.Dialog):
    """dialoog voor het opzetten van een csv bestand

    geeft de mogelijkheid om alvast wat instellingen vast te leggen en zorgt er
    tevens voor dat het correcte formaat gebruikt wordt
    """
    def __init__(self, parent, name):
        self.parent = parent
        self.parent.data = []
        super().__init__()
        self.SetTitle(self.parent.master.captions['T_INICSV'])

        grid = wx.FlexGridSizer(2, 2, 2)

        text = wx.StaticText(self, label=self.parent.master.captions['T_NAMOF'].format(
            self.parent.master.captions['S_PLGNAM'].lower(),
            self.parent.master.captions['T_ISMADE']))
        self.t_program = wx.TextCtrl(self, text='editor.plugins.{}_keys'.format(name.lower()))
        grid.Add(text, 1, 0, 1, 3)
        grid.Add(self.t_program, 1, 3)  # , 1, 1)
        text = wx.StaticText(self, label=self.parent.master.captions['S_PNLNAM'])
        self.t_title = wx.TextCtrl(self, text=name + ' hotkeys')
        grid.Add(text, 2, 0, 1, 3)
        grid.Add(self.t_title, 2, 3)  # , 1, 1)
        self.c_rebuild = wx.CheckBox(self, label=self.parent.master.captions['T_MAKE'].format(
            self.parent.master.captions['S_RBLD']))
        grid.Add(self.c_rebuild, 3, 0, 1, 4)
        self.c_details = wx.CheckBox(self, label=self.parent.master.captions['S_DETS'])
        grid.Add(self.c_details, 4, 0, 1, 4)
        self.c_redef = wx.CheckBox(self, label=self.parent.master.captions['T_MAKE'].format(
            self.parent.master.captions['S_RSAV']))
        grid.Add(self.c_redef, 5, 0, 1, 4)
        text = wx.StaticText(self, label=self.parent.master.captions['Q_SAVLOC'])
        grid.Add(text, 6, 0, 1, 2)
        path = os.path.join('editor', 'plugins', name + "_hotkeys.csv")
        # self.t_loc = FileBrowseButton(self, text=path, level_down=True)
        self.t_loc = wxfb.FilebrowseButton(self, initialValue=path)
        grid.Add(self.t_loc, 6, 2, 1, 3)

        vbox = wx.BoxSizer(wx.VERTICAL)()
        vbox.Add(grid, 0, wx.ALIGN_HORIZONTAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 2)
        vbox.SetSizeHints(self)
        self.SetSizer(vbox)

    def accept(self):
        """
        set self.parent.loc to the chosen filename
        write the settings to this file along with some sample data - deferred to
        confirmation of the filesdialog
        """
        cloc = self.t_loc.input.GetValue()
        ploc = self.t_program.GetValue()
        if cloc == "":
            show_message(self.parent.master, 'I_NEEDNAME')
            return
        cloc = os.path.abspath(cloc)
        if os.path.exists(cloc):
            show_message(self.parent.master, 'I_GOTSETFIL', args=[cloc])
            return
        if importlib.util.find_spec(ploc):
            show_message(self.parent.master, 'I_GOTPLGFIL', args=[ploc])
            return
        self.parent.loc = cloc
        self.parent.data = [ploc, self.t_title.GetValue(),
                            int(self.c_rebuild.GetValue()),
                            int(self.c_details.GetValue()),
                            int(self.c_redef.GetValue())]
        super().accept()


class DeleteDialog(wx.Dialog):
    """dialog for deleting a tool from the collection
    """
    def __init__(self, parent):
        self.parent = parent
        self.last_added = ''  # TODO uitzoeken: kan dit wel altijd
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)()
        hsizer = wx.BoxSizer(wx.HORIZONTAL)()
        label = wx.StaticText(self.parent.master.captions['Q_REMPRG'], self)
        hsizer.Add(label)
        hsizer.addStretch()
        self.sizer.Add(hsizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)()
        check = wx.CheckBox(self.parent.master.captions['Q_REMCSV'], self)
        hsizer.Add(check)
        self.remove_keydefs = check
        hsizer.addStretch()
        self.sizer.Add(hsizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)()
        check = wx.CheckBox(self.parent.master.captions['Q_REMPLG'], self)
        hsizer.Add(check)
        self.remove_plugin = check
        hsizer.addStretch()
        self.sizer.Add(hsizer)

        buttonbox = wx.DialogButtonBox()
        buttonbox.addButton(wx.DialogButtonBox.Ok)
        buttonbox.addButton(wx.DialogButtonBox.Cancel)
        buttonbox.accepted.Bind(self.accept)
        buttonbox.rejected.Bind(self.reject)
        self.sizer.Add(buttonbox)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 2)
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def accept(self):
        """send settings to parent and leave
        """
        self.parent.remove_data = self.remove_keydefs.GetValue()
        self.parent.remove_code = self.remove_plugin.GetValue()
        wx.Dialog.accept(self)


class FilesDialog(wx.Dialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.title = self.master.title
        self.last_added = ''
        self.code_to_remove = []
        self.data_to_remove = []
        super().__init__(parent, size=(680, 400))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        text = '\n'.join((self.master.captions['T_TOOLS'].split(' / ')))
        label = wx.StaticText(self, label=text)
        self.sizer.Add(label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(36)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_PRGNAM']), 0,
                   wx.ALIGN_CENTER_HORIZONTAL)
        hsizer.AddSpacer(84)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_CSVLOC']), 0,
                   wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.Add(hsizer)

        self.scrl = wx.ScrolledWindow(self)
        self.gsizer = wx.FlexGridSizer(cols=2, vgap=2, hgap=2)
        self.gsizer.AddGrowableCol(1)
        rownum = 0
        self.rownum = rownum
        self.plugindata = []
        self.checks = []
        self.paths = []
        self.progs = []
        self.settingsdata = {}
        # settingsdata is een mapping van pluginnaam op een tuple van programmanaam en
        # andere settings (alleen als er een nieuw csv file voor moet worden aangemaakt)
        for name, path in self.master.ini["plugins"]:
            self.add_row(name, path)
            self.settingsdata[name] = (self.master.pluginfiles[name],)
        self.scrl.SetSizer(self.gsizer)
        self.sizer.Add(self.scrl, 1, wx.EXPAND | wx.ALL, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, label=self.master.captions['C_ADDPRG'])
        btn.Bind(wx.EVT_BUTTON, self.add_program)
        hbox.Add(btn)
        btn = wx.Button(self, label=self.master.captions['C_REMPRG'])
        btn.Bind(wx.EVT_BUTTON, self.remove_programs)
        hbox.Add(btn)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 2)
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def add_row(self, name, path=''):
        """create a row for defining a file location
        """
        self.rownum += 1
        colnum = 0
        check = wx.CheckBox(self, label=name)
        self.gsizer.Add(check, 0, wx.ALIGN_CENTER_VERTICAL)
        self.checks.append(check)
        colnum += 1
        # browse = FileBrowseButton(self, text=path)
        # startdir = os.path.dirname(path) if path else '.'
        # browse = wxfb.FilebrowseButton(self, startDirectory=startdir, initialValue=path, fileMask=
        browse = wxfb.FileBrowseButton(self, size=(300, -1), labelText='', initialValue=path)
        self.gsizer.Add(browse, 0, wx.EXPAND)
        self.paths.append((name, browse))
        # vbar = self.scrl.verticalScrollBar()
        # vbar.setMaximum(vbar.maximum() + 52)
        # vbar.setValue(vbar.maximum())

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

    def add_program(self, event):
        """nieuwe rij aanmaken in self.gsizer"""
        newtool, ok = get_textinput(self, self.master.title, self.master.captions['P_NEWPRG'])
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

    def remove_programs(self, event):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        checked = [(x, y.text()) for x, y in enumerate(self.checks) if y.GetValue()]
        if checked:
            dlg = DeleteDialog(self).exec_()
            if dlg == wx.Dialog.Accepted:
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
        # TODO onderbrengen in een gui onafhankeljke validatieroutine
        if self.last_added not in [x[0] for x in self.paths]:
            self.last_added = ''
        self.master.last_added = self.last_added
        for ix, entry in enumerate(self.paths):
            name, path = entry
            if name not in [x for x, y in self.master.ini['plugins']]:
                csvname = path.input.text()
                if not csvname:
                    show_message(self, text='Please fill out all filenames')
                    return
                prgname = self.settingsdata[name][0]
                if not prgname:
                    # try to get the plugin name from the csv file
                    try:
                        data = shared.readcsv(csvname)
                    except (FileNotFoundError, IsADirectoryError, ValueError):
                        show_message(self, text='{} does not seem to be a usable '
                                                'csv file'.format(csvname))
                        return
                    try:
                        prgname = data[0][shared.SettType.PLG.value]
                    except KeyError:
                        show_message(self, text='{} does not contain a reference to a '
                                                'plugin (PluginName setting)'.format(csvname))
                        return
                if len(self.settingsdata[name]) == 1:  # existing plugin
                    try:
                        _ = importlib.import_module(prgname)
                    except ImportError:
                        show_message(self, text='{} does not contain a reference to a '
                                                'valid plugin'.format(csvname))
                        return

                self.master.pluginfiles[name] = prgname
        for filename in self.code_to_remove + self.data_to_remove:
            os.remove(filename)
        self.newpathdata = {}
        for name, entry in self.settingsdata.items():
            if len(entry) > 1:
                self.newpathdata[name] = entry
        self.master.ini["plugins"] = shared.update_paths(self.paths, self.newpathdata,
                                                         self.master.ini["lang"])
        super().accept()


class ColumnSettingsDialog(wx.Dialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.initializing = True
        super().__init__(parent)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        text = self.master.captions['T_COLSET'].format(
            self.master.book.page.settings[shared.SettType.PNL.value])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label=text))
        self.sizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(41)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_TTL']),
                   0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(102)  # 82)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_WID']),
                   0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(8)  # 84)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_IND']),
                   0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_SEQ']),
                   0, wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(hsizer)

        self.scrl = wx.ScrolledWindow(self)
        # self.scrl.setWidget(pnl)
        # self.scrl.setAlignment(core.Qt.AlignBottom)
        # self.scrl.setWidgetResizable(True)
        # self.bar = self.scrl.verticalScrollBar()
        self.gsizer = wx.BoxSizer(wx.VERTICAL)
        self.rownum = 0  # indicates the number of rows in the gridlayout
        self.data, self.checks = [], []
        self.col_textids, self.col_names, self.last_textid = \
            shared.read_columntitledata(self.master)
        for ix, item in enumerate(self.master.book.page.column_info):
            item.append(ix)
            self.add_row(*item)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.gsizer)
        self.scrl.SetSizer(box)
        self.sizer.Add(self.scrl)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, label=self.master.captions['C_ADDCOL'])
        btn.Bind(wx.EVT_BUTTON, self.add_column)
        hbox.Add(btn)
        btn = wx.Button(self, label=self.master.captions['C_REMCOL'])
        btn.Bind(wx.EVT_BUTTON, self.remove_columns)
        hbox.Add(btn)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 2)
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)
        self.initializing = False

    def ShowModal(self):
        """reimplementation to prevent dialog from showing in some cases
        """
        if self.last_textid == '099':
            # TODO: rethink this
            show_message(self.parent, text="Can't perform this function: "
                                           "no language text identifiers below 100 left")
            return
        return super().ShowModal()

    def add_row(self, name='', width='', is_flag=False, colno=''):
        """create a row for defining column settings
        """
        self.rownum += 1
        rownum = self.rownum
        colnum = 0
        check = wx.CheckBox(self)
        ghsizer = wx.BoxSizer(wx.HORIZONTAL)
        ghsizer.Add(check, rownum)
        self.checks.append(check)
        colnum += 1
        w_name = wx.ComboBox(self, size=(140, -1), style=wx.CB_DROPDOWN, choices=self.col_names)
        if name:
            w_name.SetSelection(self.col_names.index(self.master.captions[name]))
        # else:
        #     w_name.SetSelection('')
        ghsizer.Add(w_name, rownum)
        colnum += 1
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(20)
        w_width = wx.SpinCtrl(self, size=(48, -1))
        w_width.SetMax(999)
        if width:
            w_width.SetValue(width)
        hsizer.Add(w_width)
        hsizer.AddSpacer(20)
        ghsizer.Add(hsizer, rownum)
        colnum += 1
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(40)
        w_flag = wx.CheckBox(self, size=(32, -1))
        w_flag.SetValue(is_flag)
        hsizer.Add(w_flag)
        hsizer.AddSpacer(24)
        ghsizer.Add(hsizer, rownum)
        colnum += 1
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(68)
        val = self.rownum if colno == '' else colno + 1
        w_colno = wx.SpinCtrl(self, size=(36, -1))
        w_colno.SetRange(1, 99)
        w_colno.SetValue(val)
        hsizer.Add(w_colno)
        ghsizer.Add(hsizer, rownum)
        self.gsizer.Add(ghsizer)
        old_colno = "new" if colno == '' else colno
        self.data.append((w_name, w_width, w_colno, w_flag, old_colno))
        # vbar = self.scrl.verticalScrollBar()
        # vbar.setMaximum(vbar.maximum() + 62)
        # vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        """remove a column settings row
        """
        self.rownum -= 1
        check = self.checks[rownum]
        for widgets in self.data[rownum:]:
            w_colno = widgets[2]
            w_colno.setValue(w_colno.value() - 1)                       # omschrijven
        w_name, w_width, w_colno, w_flag, _ = self.data[rownum]
        for widget in check, w_name, w_width, w_colno, w_flag:
            self.gsizer.removeWidget(widget)                            # omschrijven
            widget.close()                                              # omschrijven
        self.gsizer.removeItem(self.gsizer.itemAt(rownum))              # omschrijven
        self.checks.pop(rownum)
        self.data.pop(rownum)

    def add_column(self, event):
        """nieuwe rij aanmaken in self.gsizer"""
        self.add_row()

    def remove_columns(self, event):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        test = [x.GetValue() for x in self.checks]
        checked = [x for x, y in enumerate(test) if y]
        if not any(test):
            return
        if ask_question(self.parent, 'Q_REMCOL'):
            for row in reversed(checked):
                self.delete_row(row)

    def accept(self):
        """save the changed settings and leave
        """
        # TODO: het meeste hiervan kan in een gui-onafhankelijke validatieroutine
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
            column_info.append([name, int(w_width.text()), w_flag.GetValue(),
                                old_colno])
        if new_titles:
            shared.add_columntitledata(new_titles)
        self.master.book.page.column_info = column_info
        for id_, name in new_titles:
            self.master.captions[id_] = name
            self.master.book.page.captions[id_] = name


class ExtraSettingsDialog(wx.Dialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.title = self.master.title
        self.captions = self.master.captions
        super().__init__(parent, size=(680, 400))

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        pnl = wx.Panel(self, style=wx.BORDER_RAISED)
        vsizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['S_PLGNAM']), 0,
                   wx.ALIGN_CENTER_VERTICAL)
        self.t_program = wx.TextCtrl(self)
        self.t_program.SetValue(self.master.book.page.settings[shared.SettType.PLG.value])
        hsizer.Add(self.t_program, 0)
        vsizer.Add(hsizer, 0)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['S_PNLNAM']), 0,
                   wx.ALIGN_CENTER_VERTICAL)
        self.t_title = wx.TextCtrl(self)
        self.t_title.SetValue(self.master.book.page.settings[shared.SettType.PNL.value])
        hsizer.Add(self.t_title, 0)
        vsizer.Add(hsizer, 0)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.c_rebuild = wx.CheckBox(self, label=self.master.captions['T_MAKE'].format(
            self.master.captions['S_RBLD']))
        if self.master.book.page.settings[shared.SettType.RBLD.value] == '1':
            self.c_rebuild.SetValue(True)
        hsizer.Add(self.c_rebuild, 0)
        vsizer.Add(hsizer, 0)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.c_showdet = wx.CheckBox(self, label=self.master.captions['S_DETS'])
        try:
            if self.master.book.page.settings[shared.SettType.DETS.value] == '1':
                self.c_showdet.SetValue(True)
        except KeyError:
            pass
        hsizer.Add(self.c_showdet)
        vsizer.Add(hsizer)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.c_redef = wx.CheckBox(self, label=self.master.captions['T_MAKE'].format(
            self.master.captions['S_RSAV']))
        if self.master.book.page.settings[shared.SettType.RDEF.value] == '1':
            self.c_redef.SetValue(True)
        hsizer.Add(self.c_redef)
        vsizer.Add(hsizer)

        pnl.SetSizer(vsizer)
        self.sizer.Add(pnl)

        pnl = wx.Panel(self, style=wx.BORDER_RAISED)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        text = self.master.captions['T_XTRASET'].format(
            self.master.book.page.settings[shared.SettType.PNL.value])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label=text), 0)
        vsizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(41)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_NAM']), 0)
        hsizer.AddSpacer(52)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_VAL']), 0)
        vsizer.Add(hsizer, 0)

        self.scrl = wx.ScrolledWindow(self, style=wx.BORDER_SIMPLE)

        self.gsizer = wx.FlexGridSizer(2, 2, 2)
        rownum = 0
        self.rownum = rownum
        self.data, self.checks = [], []
        for name, value in self.master.book.page.settings.items():
            if name not in shared.csv_settingnames and name != 'extra':
                try:
                    desc = self.master.book.page.settings['extra'][name]
                except KeyError:
                    desc = ''
                self.add_row(name, value, desc)
        self.scrl.SetSizer(self.gsizer)
        vsizer.Add(self.scrl, 0)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, label=self.master.captions['C_ADDSET'])
        btn.Bind(wx.EVT_BUTTON, self.add_setting)
        hsizer.Add(btn)
        btn = wx.Button(self, label=self.master.captions['C_REMSET'])
        btn.Bind(wx.EVT_BUTTON, self.remove_settings)
        hsizer.Add(btn)
        vsizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        pnl.SetSizer(vsizer)
        self.sizer.Add(pnl)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 2)
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def add_row(self, name='', value='', desc=''):
        """add a row for defining a setting (name, value)
        """
        return # even lui
        self.rownum += 1
        colnum = 0
        check = wx.CheckBox(self)
        self.gsizer.Add(check, self.rownum, colnum)
        self.checks.append(check)
        colnum += 1
        w_name = wx.LineEdit(name, self)
        w_name.setFixedWidth(88)
        if name:
            w_name.setReadOnly(True)
        ## w_name.setMaxLength(50)
        self.gsizer.Add(w_name, self.rownum, colnum)
        colnum += 1
        w_value = wx.LineEdit(value, self)
        self.gsizer.Add(w_value, self.rownum, colnum)
        self.rownum += 1
        w_desc = wx.LineEdit(desc, self)
        self.gsizer.Add(w_desc, self.rownum, colnum)
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

    def add_setting(self, event):
        """nieuwe rij aanmaken in self.gsizer"""
        self.add_row()

    def remove_settings(self, event):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        test = [x.GetValue() for x in self.checks]
        checked = [x for x, y in enumerate(test) if y]
        if any(test):
            if ask_question(self.parent, 'Q_REMSET'):
                for row in reversed(checked):
                    self.delete_row(row)

    def accept(self):
        """update settings and leave
        """
        # TODO: het meeste hiervan kan in een gui onafhankelijke validatieroutine
        if self.c_redef.GetValue() and not self.c_showdet.isChecked():
            show_message(self, "I_NODET")
            return
        if self.c_showdet.GetValue():
            try:
                test = self.master.book.page.reader.add_extra_attributes
            except AttributeError:
                self.c_showdet.setChecked(False)
                self.c_redef.setChecked(False)
                show_message(self, "I_IMPLXTRA")
                return
        self.master.book.page.settings[shared.SettType.PLG.value] = self.t_program.text()
        self.master.book.page.settings[shared.SettType.PNL.value] = self.t_title.text()
        value = '1' if self.c_rebuild.GetValue() else '0'
        self.master.book.page.settings[shared.SettType.RBLD.value] = value
        value = '1' if self.c_showdet.GetValue() else '0'
        self.master.book.page.settings[shared.SettType.DETS.value] = value
        value = '1' if self.c_redef.GetValue() else '0'
        self.master.book.page.settings[shared.SettType.RDEF.value] = value

        settingsdict, settdescdict = {}, {}
        for w_name, w_value, w_desc in self.data:
            settingsdict[w_name.text()] = w_value.text()
            settdescdict[w_name.text()] = w_desc.text()
        todelete = []
        for setting in self.master.book.page.settings:
            if setting not in shared.csv_settingnames:
                todelete.append(setting)
        for setting in todelete:
            del self.master.book.page.settings[setting]
        self.master.book.page.settings.update(settingsdict)
        self.master.book.page.settings['extra'] = settdescdict

        super().accept()


class EntryDialog(wx.Dialog):
    """Dialog for Manual Entry
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.captions = self.master.captions

        super().__init__(parent, size=(680, 400))

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.p0list = wxg.Grid(self)
        self.p0list.CreateGrid(len(self.master.book.page.data),
                               len(self.master.book.page.column_info))
        self.p0list.SetRowLabelSize(20)

        # use self.master.book.page.column_info to define grid
        for ix, row in enumerate(self.master.book.page.column_info):
            self.p0list.SetColLabelValue(ix, self.captions[row[0]])
            self.p0list.SetColSize(ix, row[1])

        # use self.master.page.data to populate grid
        self.data = self.master.book.page.data
        num_rows = 0
        for rowkey, row in self.data.items():
            for i, element in enumerate(row):
                self.p0list.SetCellValue(num_rows, i, element)
            num_rows += 1
        self.numrows = num_rows

        hsizer.Add(self.p0list, 1, wx.EXPAND)
        self.sizer.Add(hsizer, 1, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, label=self.captions['C_ADDKEY'])
        btn.Bind(wx.EVT_BUTTON, self.add_key)
        hbox.Add(btn)
        btn = wx.Button(self, label=self.captions['C_REMKEY'])
        btn.Bind(wx.EVT_BUTTON, self.delete_key)
        hbox.Add(btn)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM | wx.BOTTOM, 2)
        # self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def add_key(self, event):
        "add a line to the grid"
        self.p0list.AppendRows()
        for i in range(self.p0list.GetNumberCols()):
            self.p0list.SetCellValue(self.numrows, i, '')
        self.numrows += 1
        self.p0list.ShowRow(self.numrows - 1)  # dit werkt nog niet zoals ik wil (scroll to bottom)

    def delete_key(self, event):
        "remove selected line(s) from the grid"
        selected_rows = []
        for row in self.p0list.GetSelectedRows():  # moet misschien reversed?
            self.p0list.DeleteRows(row)

    def accept(self):
        """send updates to parent and leave
        """
        # TODO onderbrengen in een gui onafhankelijke validatieroutine?
        new_values = {}
        for rowid in range(self.p0list.GetNumberRows()):
            value = []
            for colid in range(self.p0list.GetNumberCols()):
                # try:
                    value.append(self.p0list.GetCellValue(rowid, colid))
                # except AttributeError:
                #     value.append('')
            if value != [''] * self.p0list.GetNumberCols():
                new_values[len(new_values)] = value
        self.master.book.page.data = new_values


def manage_filesettings(win):
    "relay"
    with FilesDialog(win.gui, win) as dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            dlg.accept()
    return ok == wx.ID_OK


def manage_extrasettings(win):
    "relay"
    with ExtraSettingsDialog(win.gui, win) as dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            dlg.accept()
    return ok == wx.ID_OK


def manage_columnsettings(win):
    "relay"
    with ColumnSettingsDialog(win.gui, win) as dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            dlg.accept()
    return ok == wx.ID_OK


def manual_entry(win):
    "relay"
    with EntryDialog(win.gui, win) as dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            dlg.accept()
    return ok == wx.ID_OK


def manage_startupsettings(win):
    "relay"
    with InitialToolDialog(win.gui, win) as dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            dlg.accept()
    return ok == wx.ID_OK
