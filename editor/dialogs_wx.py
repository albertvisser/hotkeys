"""Hotkeys dialog code - wxPython version
"""
import os
import collections
import wx
import wx.grid as wxg
import wx.lib.filebrowsebutton as wxfb
import wx.lib.scrolledpanel as wxsp
import editor.shared as shared


def show_message(win, message_id='', text='', args=None):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    text = shared.get_text(win, message_id, text, args)
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


def get_textinput(win, text, prompt=''):
    """toon een dialoog waarin een regel tekst kan worden opgegeven en retourneer het antwoord
    (de opgegeven tekst en True bij OK) na sluiten van de dialoog
    """
    title = shared.get_text(win, 'T_MAIN')
    with wx.TextEntryDialog(win, prompt, title, value=text) as dlg:
        ok = dlg.ShowModal()
        if ok == wx.ID_OK:
            text = dlg.GetValue()
    return text, ok == wx.ID_OK


def get_choice(win, title, caption, choices, current):
    """toon een dialoog waarin een waarde gekozen kan worden uit een lijst en retourneer het
    antwoord (de geselecteerde waarde en True bij OK) na sluiten van de dialoog
    """
    text = ''
    with wx.SingleChoiceDialog(win, title, caption, choices, wx.CHOICEDLG_STYLE) as dlg:
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
        self.parent.master.accept_startupsettings(self.check_fixed.GetValue(),
                                                  self.check_remember.GetValue(),
                                                  self.sel_fixed.GetStringSelection())
        return True


class FileBrowseButton(wx.Frame):  # note: wx has this built in
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
        super().__init__(parent, style=wx.BORDER_RAISED)
        vbox = wx.BoxSizer(wx.VERTICAL)()
        box = wx.BoxSizer(wx.HORIZONTAL)()
        self.input = wx.TextCtrl(self, size=(200, -1), value=text)
        box.Add(self.input)
        caption = self.parent.captions['C_BRWS']
        self.button = wx.Button(self, label=caption)
        self.button.Bind(wx.EVT_BUTTON, self.browse)
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
        super().__init__(parent, title=self.parent.master.captions['T_INICSV'])

        box = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(2, 2, 2)
        text = wx.StaticText(self, label=self.parent.master.captions['T_NAMOF'].format(
            self.parent.master.captions['S_PLGNAM'].lower(),
            self.parent.master.captions['T_ISMADE']))
        self.t_program = wx.TextCtrl(self, value='editor.plugins.{}_keys'.format(name.lower()),
                                     size=(160, -1))
        grid.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.LEFT, 5)
        grid.Add(self.t_program, 0, wx.TOP | wx.RIGHT, 5)
        text = wx.StaticText(self, label=self.parent.master.captions['S_PNLNAM'])
        self.t_title = wx.TextCtrl(self, value=name + ' hotkeys', size=(160, -1))
        grid.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        grid.Add(self.t_title, 0, wx.RIGHT, 5)
        box.Add(grid, 0, wx.ALL, 5)

        self.c_rebuild = wx.CheckBox(self, label=self.parent.master.captions['T_MAKE'].format(
            self.parent.master.captions['S_RBLD']))
        box.Add(self.c_rebuild, 0, wx.LEFT, 15)
        self.c_details = wx.CheckBox(self, label=self.parent.master.captions['S_DETS'])
        box.Add(self.c_details, 0, wx.LEFT, 15)
        self.c_redef = wx.CheckBox(self, label=self.parent.master.captions['T_MAKE'].format(
            self.parent.master.captions['S_RSAV']))
        box.Add(self.c_redef, 0, wx.LEFT, 15)

        line = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.StaticText(self, label=self.parent.master.captions['Q_SAVLOC'])
        line.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 5)
        path = os.path.join('editor', 'plugins', name + "_hotkeys.csv")
        # self.t_loc = FileBrowseButton(self, text=path, level_down=True)
        self.t_loc = wxfb.FileBrowseButton(self, size=(300, -1), style=wx.BORDER_SUNKEN,
                                           labelText='', initialValue=path)
        line.AddStretchSpacer()
        line.Add(self.t_loc, 0, wx.EXPAND | wx.RIGHT, 5)
        box.Add(line, 0, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        box.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
        box.SetSizeHints(self)
        self.SetSizer(box)

    def accept(self):
        """
        set self.parent.loc to the chosen filename
        write the settings to this file along with some sample data - deferred to
        confirmation of the filesdialog
        """
        return self.parent.master.accept_csvsettings(self.t_loc.GetValue(),
                                                     self.t_program.GetValue(),
                                                     self.t_title.GetValue(),
                                                     self.c_rebuild.GetValue(),
                                                     self.c_details.GetValue(),
                                                     self.c_redef.GetValue())


class DeleteDialog(wx.Dialog):
    """dialog for deleting a tool from the collection
    """
    def __init__(self, parent):
        self.parent = parent
        self.last_added = ''  # TODO uitzoeken: kan dit wel altijd
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, label=self.parent.master.captions['Q_REMPRG'])
        hsizer.Add(label, 0, wx.LEFT | wx.RIGHT, 5)
        # hsizer.addStretch()
        self.sizer.Add(hsizer,1, wx.TOP, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        check = wx.CheckBox(self, label=self.parent.master.captions['Q_REMCSV'])
        hsizer.Add(check, 0, wx.LEFT, 10)
        self.remove_keydefs = check
        # hsizer.addStretch()
        self.sizer.Add(hsizer, 1, wx.TOP, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        check = wx.CheckBox(self, label=self.parent.master.captions['Q_REMPLG'])
        hsizer.Add(check, 0, wx.LEFT, 10)
        self.remove_plugin = check
        # hsizer.addStretch()
        self.sizer.Add(hsizer, 1, wx.TOP, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 2)
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def accept(self):
        """send settings to parent and leave
        """
        self.parent.remove_data = self.remove_keydefs.GetValue()
        self.parent.remove_code = self.remove_plugin.GetValue()


class FilesDialog(wx.Dialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        # self.title = self.master.title
        self.last_added = ''
        self.code_to_remove = []
        self.data_to_remove = []
        super().__init__(parent, size=(680, 400), title=self.master.title)

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

        self.scrl = wxsp.ScrolledPanel(self, style=wx.BORDER_SUNKEN)
        self.gsizer = wx.FlexGridSizer(cols=2, vgap=2, hgap=2)
        self.gsizer.AddGrowableCol(1)
        rownum = 0
        self.rownum = rownum
        self.plugindata = []
        self.checks = []
        self.paths = []
        self.progs = []
        self.sizeritems = []
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
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 5)
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def add_row(self, name, path=''):
        """create a row for defining a file location
        """
        self.rownum += 1
        colnum = 0
        check = wx.CheckBox(self.scrl, label=name)
        item0 = self.gsizer.Add(check, 0, wx.ALIGN_CENTER_VERTICAL)
        self.checks.append(check)
        colnum += 1
        # browse = wxfb.FilebrowseButton(self, startDirectory=startdir, initialValue=path, fileMask=
        browse = wxfb.FileBrowseButton(self.scrl, size=(300, -1), style=wx.BORDER_SUNKEN,
                                       labelText='', initialValue=path)
        item1 = self.gsizer.Add(browse, 0, wx.EXPAND)
        self.sizeritems.append((item0, item1))
        self.paths.append((name, browse))
        self.gsizer.Layout()
        self.scrl.Fit()
        self.scrl.SetScrollbar(wx.VERTICAL, 0, 1, self.rownum * 52)
        self.scrl.ScrollChildIntoView(browse)
        # print('ready adding row')
        # vbar = self.scrl.verticalScrollBar()
        # vbar.setMaximum(vbar.maximum() + 52)
        # vbar.setValue(vbar.maximum())

    def delete_row(self, rownum):
        """remove a tool location definition row
        """
        check = self.checks[rownum]
        print(check, self.gsizer.GetItem(check))
        name, win = self.paths[rownum]
        print(name, win, self.gsizer.GetItem(win))
        print(self.sizeritems)
        print(self.gsizer.GetChildren())
        start = rownum - 1
        self.gsizer.Remove(start)  # rownum * 2 - 1)
        check.Destroy()
        self.gsizer.Remove(start + 1)  # rownum * 2)
        win.Destroy()
        self.gsizer.Layout()
        self.scrl.Fit()
        self.scrl.SetScrollbar(wx.VERTICAL, 0, 1, self.rownum * 52)
        # self.scrl.ScrollChildIntoView(browse)
        self.checks.pop(rownum)
        self.paths.pop(rownum)
        self.settingsdata.pop(name)

    def add_program(self, event):
        """nieuwe rij aanmaken in self.gsizer"""
        newtool, ok = get_textinput(self, '', self.master.captions['P_NEWPRG'])
        if ok:
            if newtool == "":
                show_message(self.parent, 'I_NEEDNAME')
                return
            self.last_added = newtool
            self.loc = prgloc = ""
            self.settingsdata[newtool] = (prgloc,)
            if ask_question(self.parent, 'P_INICSV'):
                with SetupDialog(self, newtool) as dlg:
                    send = True
                    while send:
                        send = False
                        test = dlg.ShowModal()
                        if test == wx.ID_OK:
                            if not dlg.accept():
                                send = True
                            else:
                                self.settingsdata[newtool] = self.parent.data
                                prgloc = self.parent.data[0]
            self.add_row(newtool, path=self.parent.loc)
            self.Fit()

    def remove_programs(self, event):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        checked = [(x, y.GetLabel()) for x, y in enumerate(self.checks) if y.GetValue()]
        if checked:
            with DeleteDialog(self) as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    dlg.accept()
                    for row, name in reversed(checked):
                        csv_name, prg_name = '', ''
                        try:
                            csv_name = self.paths[row][1].GetValue()  # input.text()
                            prg_name = self.settingsdata[name][0]
                        except KeyError:
                            shared.log_exc('')
                        shared.log('csv name is %s', csv_name)
                        shared.log('prg name is %s', prg_name)
                        if self.remove_data:
                            if csv_name:
                                self.data_to_remove.append(csv_name)
                        if self.remove_code:
                            if prg_name:
                                self.code_to_remove.append(
                                    prg_name.replace('.', '/') + '.py')
                        self.delete_row(row)
            self.Fit()

    def accept(self):
        """send updates to parent and leave
        """
        return self.master.accept_pathsettings([(x, y.GetValue()) for x, y in self.paths],
                                               self.settingsdata,
                                               self.code_to_remove + self.data_to_remove)


class ColumnSettingsDialog(wx.Dialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.initializing = True
        super().__init__(parent, title=self.master.title)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        text = self.master.captions['T_COLSET'].format(
            self.master.book.page.settings[shared.SettType.PNL.value])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label=text))
        self.sizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(36)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_TTL']),
                   0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(137)  # 82)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_WID']),
                   0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(100)  # 84)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_IND']),
                   0, wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(44)
        hsizer.Add(wx.StaticText(self, label=self.master.captions['C_SEQ']),
                   0, wx.ALIGN_CENTER_VERTICAL)
        self.sizer.Add(hsizer)

        self.scrl = wxsp.ScrolledPanel(self, style=wx.BORDER_RAISED)
        # self.scrl.setWidget(pnl)
        # self.scrl.setAlignment(core.Qt.AlignBottom)
        # self.scrl.setWidgetResizable(True)
        # self.bar = self.scrl.verticalScrollBar()
        self.gsizer = wx.BoxSizer(wx.VERTICAL)
        self.rownum = 0  # indicates the number of rows in the gridlayout
        self.data, self.checks = [], []
        self.col_textids, self.col_names, self.last_textid = \
            self.master.col_textids, self.master.col_names, self.master.last_textid
        for ix, item in enumerate(self.master.book.page.column_info):
            item.append(ix)
            self.add_row(*item)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.gsizer)
        self.scrl.SetSizer(box)
        self.sizer.Add(self.scrl, 1, wx.EXPAND | wx.ALL, 5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, label=self.master.captions['C_ADDCOL'])
        btn.Bind(wx.EVT_BUTTON, self.add_column)
        hbox.Add(btn)
        btn = wx.Button(self, label=self.master.captions['C_REMCOL'])
        btn.Bind(wx.EVT_BUTTON, self.remove_columns)
        hbox.Add(btn)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_BOTTOM | wx.TOP | wx.BOTTOM,
                       2)
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)
        self.initializing = False

    # def ShowModal(self):
    #     """reimplementation to prevent dialog from showing in some cases
    #     """
    #     if self.last_textid == '099':
    #         show_message(self.parent, text="Can't perform this function: "
    #                                        "no language text identifiers below 100 left")
    #         return None
    #     return super().ShowModal()

    def add_row(self, name='', width='', is_flag=False, colno=''):
        """create a row for defining column settings
        """
        self.rownum += 1
        rownum = self.rownum
        colnum = 0
        check = wx.CheckBox(self.scrl, size=(20, -1))
        ghsizer = wx.BoxSizer(wx.HORIZONTAL)
        ghsizer.Add(check, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 2)
        self.checks.append(check)

        colnum += 1
        w_name = wx.ComboBox(self.scrl, size=(140, -1), style=wx.CB_READONLY,  # wx.CB_DROPDOWN,
                             choices=self.col_names)
        if name:
            w_name.SetSelection(self.col_names.index(self.master.captions[name]))
        # else:
        #     w_name.SetSelection('')
        ghsizer.Add(w_name, 0, wx.LEFT, 2)

        colnum += 1
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(20)
        w_width = wx.SpinCtrl(self.scrl, size=(130, -1), style=wx.SP_ARROW_KEYS)
        w_width.SetMax(999)
        if width:
            w_width.SetValue(width)
        hsizer.Add(w_width)
        hsizer.AddSpacer(20)
        ghsizer.Add(hsizer, 0)

        colnum += 1
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(40)
        w_flag = wx.CheckBox(self.scrl, size=(32, -1))
        w_flag.SetValue(is_flag)
        hsizer.Add(w_flag)
        hsizer.AddSpacer(24)
        ghsizer.Add(hsizer, 0, wx.ALIGN_CENTER_VERTICAL)

        colnum += 1
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(68)
        val = self.rownum if colno == '' else colno + 1
        w_colno = wx.SpinCtrl(self.scrl, size=(126, -1))
        w_colno.SetRange(1, 99)
        w_colno.SetValue(val)
        hsizer.Add(w_colno)
        ghsizer.Add(hsizer, 0)

        self.gsizer.Add(ghsizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        old_colno = "new" if colno == '' else colno
        self.data.append((w_name, w_width, w_colno, w_flag, old_colno))
        self.gsizer.Layout()
        self.scrl.Fit()

        self.scrl.SetScrollbar(wx.VERTICAL, 0, 1, self.rownum * 62)
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
            w_colno.SetValue(w_colno.GetValue() - 1)
        w_name, w_width, w_colno, w_flag, _ = self.data[rownum]
        self.gsizer.Remove(rownum)
        for widget in check, w_name, w_width, w_colno, w_flag:
            widget.Destroy()
        self.gsizer.Layout()
        self.scrl.Fit()
        self.checks.pop(rownum)
        self.data.pop(rownum)

    def add_column(self, event):
        """nieuwe rij aanmaken in self.gsizer"""
        self.add_row()
        self.Fit()

    def remove_columns(self, event):
        """alle aangevinkte items verwijderen uit self.gsizer"""
        test = [x.GetValue() for x in self.checks]
        checked = [x for x, y in enumerate(test) if y]
        if not any(test):
            return
        if ask_question(self.parent, 'Q_REMCOL'):
            for row in reversed(checked):
                self.delete_row(row)
        self.Fit()

    def accept(self):
        """save the changed settings and leave
        """
        data = [(x.GetValue(), y.GetValue(), a.GetValue(), b.GetValue(), c)
                for x, y, a, b, c in self.data]
        return self.master.accept_columnsettings(data)


class ExtraSettingsDialog(wx.Dialog):
    """dialoog voor invullen tool specifieke instellingen
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        # self.title = self.master.title
        self.captions = self.master.captions
        super().__init__(parent, size=(680, 400), title=self.master.title)

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        pnl = wx.Panel(self, style=wx.BORDER_RAISED)
        vsizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(pnl, label=self.master.captions['S_PLGNAM']), 0,
                   wx.ALIGN_CENTER_VERTICAL)
        self.t_program = wx.TextCtrl(pnl, size=(260, -1))
        self.t_program.SetValue(self.master.book.page.settings[shared.SettType.PLG.value])
        hsizer.Add(self.t_program, 0, wx.EXPAND | wx.TOP | wx.LEFT, 5)
        vsizer.Add(hsizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(pnl, label=self.master.captions['S_PNLNAM']), 0,
                   wx.ALIGN_CENTER_VERTICAL)
        self.t_title = wx.TextCtrl(pnl, size=(260, -1))
        self.t_title.SetValue(self.master.book.page.settings[shared.SettType.PNL.value])
        hsizer.Add(self.t_title, 0, wx.EXPAND | wx.LEFT, 5)
        vsizer.Add(hsizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.c_rebuild = wx.CheckBox(pnl, label=self.master.captions['T_MAKE'].format(
            self.master.captions['S_RBLD']))
        if self.master.book.page.settings[shared.SettType.RBLD.value] == '1':
            self.c_rebuild.SetValue(True)
        hsizer.Add(self.c_rebuild, 0)
        vsizer.Add(hsizer, 0, wx.LEFT | wx.RIGHT, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.c_showdet = wx.CheckBox(pnl, label=self.master.captions['S_DETS'])
        try:
            if self.master.book.page.settings[shared.SettType.DETS.value] == '1':
                self.c_showdet.SetValue(True)
        except KeyError:
            pass
        hsizer.Add(self.c_showdet)
        vsizer.Add(hsizer, 0, wx.LEFT | wx.RIGHT, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.c_redef = wx.CheckBox(pnl, label=self.master.captions['T_MAKE'].format(
            self.master.captions['S_RSAV']))
        if self.master.book.page.settings[shared.SettType.RDEF.value] == '1':
            self.c_redef.SetValue(True)
        hsizer.Add(self.c_redef)
        vsizer.Add(hsizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        pnl.SetSizer(vsizer)
        self.sizer.Add(pnl, 0, wx.EXPAND | wx.ALL, 10)

        pnl = wx.Panel(self, style=wx.BORDER_RAISED)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        text = self.master.captions['T_XTRASET'].format(
            self.master.book.page.settings[shared.SettType.PNL.value])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(pnl, label=text), 0)
        vsizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddSpacer(41)
        hsizer.Add(wx.StaticText(pnl, label=self.master.captions['C_NAM']), 0)
        hsizer.AddSpacer(52)
        hsizer.Add(wx.StaticText(pnl, label=self.master.captions['C_VAL']), 0)
        vsizer.Add(hsizer, 0)

        self.scrl = wxsp.ScrolledPanel(pnl, style=wx.BORDER_SIMPLE)

        self.gsizer = wx.FlexGridSizer(3, 2, 2)
        self.gsizer.AddGrowableCol(2, 1)
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
        size = self.rownum or 1
        self.scrl.SetMinSize((-1, size * 80))
        self.scrl.SetSizer(self.gsizer)
        self.gsizer.Fit(self.scrl)
        vsizer.Add(self.scrl, 1, wx.EXPAND | wx.ALL, 5)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(pnl, label=self.master.captions['C_ADDSET'])
        btn.Bind(wx.EVT_BUTTON, self.add_setting)
        hsizer.Add(btn)
        btn = wx.Button(pnl, label=self.master.captions['C_REMSET'])
        btn.Bind(wx.EVT_BUTTON, self.remove_settings)
        hsizer.Add(btn)
        vsizer.Add(hsizer, 0, wx.ALIGN_CENTER_HORIZONTAL)
        pnl.SetSizer(vsizer)
        self.sizer.Add(pnl, 1, wx.EXPAND | wx.ALL, 10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(self, id=wx.ID_OK))
        hbox.Add(wx.Button(self, id=wx.ID_CANCEL))
        self.sizer.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 2)
        self.sizer.SetSizeHints(self)
        self.SetSizer(self.sizer)

    def add_row(self, name='', value='', desc=''):
        """add a row for defining a setting (name, value)
        """
        self.rownum += 1
        colnum = 0
        check = wx.CheckBox(self.scrl)
        self.gsizer.Add(check, 0, wx.LEFT, 2)
        self.checks.append(check)
        colnum += 1
        w_name = wx.TextCtrl(self.scrl, value=name, size=(120, -1))
        if name:
            w_name.SetEditable(False)
        self.gsizer.Add(w_name)
        colnum += 1
        vsizer = wx.BoxSizer(wx.VERTICAL)
        w_value = wx.TextCtrl(self.scrl, value=value)  # , size=(320, -1))
        self.gsizer.Add(w_value, 1, wx.EXPAND | wx.RIGHT, 5)
        self.rownum += 1
        self.gsizer.AddStretchSpacer()
        self.gsizer.AddStretchSpacer()
        w_desc = wx.TextCtrl(self.scrl, value=desc)  # , size=(320, -1))
        self.gsizer.Add(w_desc, 1, wx.EXPAND | wx.RIGHT, 5)
        self.data.append((w_name, w_value, w_desc))
        self.gsizer.Layout()
        self.scrl.SetScrollbar(wx.VERTICAL, 0, 1, self.rownum * 62)
        # vbar = self.scrl.verticalScrollBar()
        # vbar.setMaximum(vbar.maximum() + 62)
        # vbar.setValue(vbar.maximum())
        test = self.scrl.GetScrollLines(wx.VERTICAL)
        test2 = self.scrl.GetScrollPos(wx.VERTICAL)
        test3 = self.scrl.GetScrollRange(wx.VERTICAL)
        # print(test, test2, test3)
        # print('before scrolling')
        self.scrl.Scroll(-1, test)
        # print('after  scrolling')

    def delete_row(self, rownum):
        """delete a setting definition row
        """
        check = self.checks[rownum]
        w_name, w_value, w_desc = self.data[rownum]
        start = rownum - 1
        for ix, widget in enumerate((check, w_name, w_value, w_desc)):
            self.gsizer.Remove(start + ix)
            widget.Destroy()
        self.gsizer.Layout()
        self.scrl.Fit()
        self.checks.pop(rownum)
        self.data.pop(rownum)

    def add_setting(self, event):
        """nieuwe rij aanmaken in self.gsizer"""
        self.add_row()
        # print('ready building new row')

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
        data = [(x.GetValue(), y.GetValue(), z.GetValue()) for x, y, z in self.data]
        ok = self.master.accept_extrasettings(self.t_program.GetValue(),
                                              self.t_title.GetValue(),
                                              self.c_rebuild.GetValue(),
                                              self.c_showdet.GetValue(),
                                              self.c_redef.GetValue(), data)
        if not ok:
            "eigenlijk moet de dialoog in dit geval opnieuw gestart worden"
            self.c_showdet.SetValue(False)
            self.c_redef.SetValue(False)
        return ok


class EntryDialog(wx.Dialog):
    """Dialog for Manual Entry
    """
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master
        self.captions = self.master.captions

        super().__init__(parent, size=(680, 400), title=self.master.title)

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
        new_values = collections.defaultdict(list)
        for rowid in range(self.p0list.GetNumberRows()):
            for colid in range(self.p0list.GetNumberCols()):
                new_values[rowid + 1].append(self.p0list.GetCellValue(rowid, colid))
        self.master.book.page.data = new_values
        return True


def show_dialog(win, cls):
    "show a dialog and return confirmation"
    with cls(win.gui, win) as dlg:
        send = True
        while send:
            ok = dlg.ShowModal()
            send = False
            if ok == wx.ID_OK and not dlg.accept():
                send = True
    return ok == wx.ID_OK
