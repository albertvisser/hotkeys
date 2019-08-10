"""Hotkeys dialog code - wxPython version
"""
import wx


def show_message(self, message_id='', text='', caption_id='T_MAIN'):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    if message_id:
        text = self.editor.captions[message_id]
    with wx.MessageDialog(self, text, self.editor.captions[caption_id],
                          wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_INFORMATION) as dlg:
        h = dlg.ShowModal()
    ## dlg.Destroy()
    return h == wx.ID_YES, h == wx.ID_CANCEL


def ask_question(win, message_id='', text='', args=None):
    """toon een vraag in een dialoog en retourneer het antwoord (Yes als True, No als False)
    na sluiten van de dialoog
    """


def ask_ync_question(win, message_id='', text='', args=None):
    """toon een vraag in een dialoog met drie mogelijkheden en retourneer het antwoord
    (Yes als (True, False), No als (False, False) en Cancel als (False, True)
    na sluiten van de dialoog
    """


class MainWindow(wx.Frame):
    """Hoofdscherm van de applicatie"""
    def __init__(self,parent, id, args):
        # args can contain an alternate tool configuration but we ignore that for now
        self.sb = self.CreateStatusBar()
        self.readcaptions('english.lng')
        ## print('in mainwindow', self.captions)
        # TODO: aanpassen aan nieuwe architectuur
        self.menuBar = wx.MenuBar()
        self.SetMenuBar(self.menuBar)

        btn = wx.Button(self, label=self.captions['C_EXIT'])
        btn.Bind(wx.EVT_BUTTON, self.exit)
        sizer0.Add(btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(sizer0)
        self.SetAutoLayout(True)
        sizer0.Fit(self)
        sizer0.SetSizeHints(self)
        # self.pnl.Layout()
        self.Show(True)

    def m_loc(self, event):
        """(menu) callback voor aanpassen van de bestandslocaties

        vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
        toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
        (met name of de opgegeven paden kloppen)
        """
        wx.MessageBox('paden gekozen', self.captions['T_MAIN']) #shared.NOT_IMPLEMENTED)
        return
        if self.modified:
            h = show_message(self, '025')
            if h == wx.ID_YES:
                self.savekeys()
            elif h == wx.ID_CANCEL:
                return
        paths = [self.ini.pad,]
        captions = [self.captions[x] for x in ('028','044','039')]
        ## captions = ['Define file locations for:', 'TC','UC','CI','KT','HK']
        dlg = FilesDialog(self, -1, self.captions['T_MAIN'], paths, captions,
            size=(400, 200),
            #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
            style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
            )
        ## dlg.CenterOnScreen()
        fout = "*"
        text = ''
        while fout:
            val = dlg.ShowModal()
            pad = dlg.bVI.GetValue()
            fout = ""
            if val == wx.ID_OK:
                text = "modified"
                if pad != "":
                    naam = self.captions['044']
                    if not os.path.isdir(pad):
                        fout = self.captions['034'] % naam
                    elif not os.path.exists(os.path.join(pad,naam)):
                        fout = self.captions['035'] % naam
            if fout:
                mdlg = wx.MessageDialog(self,fout,self.captions['T_MAIN'])
                mdlg.ShowModal()
                mdlg.Destroy()
        dlg.Destroy()
        if text:
            ## for i,pad in enumerate(paden):
                ## if pad != "":
                    ## self.ini.paden[i] = pad
            self.ini.pad = pad
            self.ini.write()
            text = ''

    def m_lang(self, event):
        """(menu) callback voor taalkeuze

        past de settings aan en leest het geselecteerde language file
        """
        choices = [x for x in os.listdir(os.path.join(shared.HERE, 'languages'))
                   if os.path.splitext(x)[1] == ".lng"]
        with wx.SingleChoiceDialog(self, self.captions['P_SELLNG'], self.captions['T_MAIN'], choices,
                                   wx.CHOICEDLG_STYLE) as dlg:
            for i, x in enumerate(choices):
                print(x, self.ini.lang)
                if x == self.ini.lang:
                    dlg.SetSelection(i)
                    break
            h = dlg.ShowModal()
            if h == wx.ID_OK:
                lang = dlg.GetStringSelection()
                self.ini.lang = lang
                self.ini.write()
                self.readcaptions()
                self.setcaptions()
        ## dlg.Destroy()

    def m_about(self, event):
        """(menu) callback voor het tonen van de "about" dialoog
        """
        info = wx.adv.AboutDialogInfo()
        info.Name = self.captions['T_MAIN']
        info.Version = shared.VRS
        info.Copyright = shared.AUTH
        ## info.Description = shared.TTL, 350, wx.ClientDC(self)
        ## info.WebSite = ("http://en.wikipedia.org/wiki/Hello_world", "Hello World home page")
        ## info.Developers = [ "Joe Programmer",
                            ## "Jane Coder",
                            ## "Vippy the Mascot" ]
        ## info.License = wordwrap(licenseText, 500, wx.ClientDC(self))
        wx.adv.AboutBox(info, self)

    def m_exit(self, event):
        """(menu) callback om het programma direct af te sluiten"""
        self.exit()
