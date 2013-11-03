# -*- coding: UTF-8 -*-
"""hotkeys.py

    main gui (choicebook)
    importeert de verschillende applicatiemodules
    hierin wordt het menu gedefinieerd en de functies die daarbij horen
    het idee is dat de menuopties wanneer nodig uitgegrijsd zijn en dat
        in de routines wordt uitgevraagd wat te doen bij welke applicatie
    voor wat betreft de instellingen:
        taalkeuze: op dit niveau
        paden: op applicatie niveau
"""
import os
import  wx
import hotkeys_shared as hks
import vikey_gui

def show_message(self, message_id, caption_id='000'):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    dlg = wx.MessageDialog(self, self.captions[message_id],
        self.captions[caption_id],
        wx.YES_NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_INFORMATION
        )
    h = dlg.ShowModal()
    dlg.Destroy()
    return h

def m_read(self):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    wx.MessageBox('Lezen gekozen', self.captions['000'])
    return
    if not self.modified:
        h = show_message(self, '041')
        if h == wx.ID_YES:
            self.readkeys()
            self.page.PopulateList()

def m_save(self):
    """(menu) callback voor het terugschrijven van de hotkeys

    vraagt eerst of het ok is om de hotkeys weg te schrijven
    vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
    """
    wx.MessageBox('Opslaan gekozen', self.captions['000']) #hks.NOT_IMPLEMENTED)
    return
    if not self.modified:
        h = show_message(self, '041')
        if h != wx.ID_YES:
            return
    self.savekeys()
    if self.ini.restart:
        h = show_message(self, '026')
        if h == wx.ID_YES:
            os.system(self.ini.restart)
    else:
        wx.MessageBox(self.captions['037'], self.captions['000'])
        ## h = show_message(self, '037')

def m_user(self):
    """(menu) callback voor een nog niet geïmplementeerde actie"""
    return self.captions[hks.NOT_IMPLEMENTED]

def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.Close()

def m_loc(self):
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    wx.MessageBox('paden gekozen', self.captions['000']) #hks.NOT_IMPLEMENTED)
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
    dlg = FilesDialog(self, -1, self.captions["000"], paths, captions,
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
            mdlg = wx.MessageDialog(self,fout,self.captions["000"])
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

def m_lang(self):
    """(menu) callback voor taalkeuze

    past de settings aan en leest het geselecteerde language file
    """
    y = [x for x in os.listdir(hks.HERE) if os.path.splitext(x)[1] == ".lng"]
    dlg = wx.SingleChoiceDialog(
        self,self.captions["027"],self.captions["000"],
        y,
        wx.CHOICEDLG_STYLE
        )
    for i, x in enumerate(y):
        print x, self.ini.lang
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
    dlg.Destroy()

def m_about(self):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    info = wx.AboutDialogInfo()
    info.Name = self.captions['000']
    info.Version = hks.VRS
    info.Copyright = hks.AUTH
    ## info.Description = hks.TTL, 350, wx.ClientDC(self)
    ## info.WebSite = ("http://en.wikipedia.org/wiki/Hello_world", "Hello World home page")
    ## info.Developers = [ "Joe Programmer",
                        ## "Jane Coder",
                        ## "Vippy the Mascot" ]
    ## info.License = wordwrap(licenseText, 500, wx.ClientDC(self))
    wx.AboutBox(info)

# dispatch table for  menu callbacks
MENU_FUNC = {
    hks.M_READ: m_read,
    hks.M_SAVE: m_save,
    hks.M_USER: m_user,
    hks.M_EXIT: m_exit,
    hks.M_LOC: m_loc,
    hks.M_LANG: m_lang,
    hks.M_ABOUT: m_about,
    }

#----------------------------------------------------------------------------

pagetexts = [ "VI", "Total Commander", "Double Commander", "To", "Select", "Pages"]

class MainWindow(wx.Frame):
    """Hoofdscherm van de applicatie"""
    def __init__(self,parent,id,args):
        wid = 860 if hks.LIN else 688
        hig = 594
        wx.Frame.__init__(self,parent,wx.ID_ANY, "tcmdrkeys",size = (wid, hig),
                            style=wx.DEFAULT_FRAME_STYLE
                                | wx.NO_FULL_REPAINT_ON_RESIZE
                                ## | wx.BORDER_SIMPLE
                                )
        self.sb = self.CreateStatusBar() # A Statusbar in the bottom of the window
        self.readcaptions('english.lng')
        self.menuBar = wx.MenuBar()
        for title, items in hks.VI_MENU:
            menu = wx.Menu()
            for sel in items:
                if sel == -1:
                    menu.AppendSeparator()
                else:
                    menu.Append(int(sel), self.captions[sel])
                    self.Bind(wx.EVT_MENU, self.OnMenu, id=int(sel))
            self.menuBar.Append(menu, self.captions[title])
        self.SetMenuBar(self.menuBar)

        self.pnl = wx.Panel(self, -1) #, style=wx.BORDER_SIMPLE)
        self.book = wx.Choicebook(self.pnl, -1) # , size= (600, 700))
        for txt in pagetexts:
            if txt == "VI":
                win = vikey_gui.VIPanel(self.book, -1)
                win.doelayout()
            else:
                win = wx.Panel(self.book, -1 ) #, style=wx.BORDER_SIMPLE)
                st = wx.StaticText(win, -1, txt, (10,10))
            self.book.AddPage(win, txt)
        self.book.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.book.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGING, self.OnPageChanging)

        sizer0 = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(self.book, 1, wx.EXPAND, 0)
        sizer0.Add(sizer1, 1, wx.EXPAND, 0)
        self.pnl.SetSizer(sizer0)
        self.pnl.SetAutoLayout(True)
        sizer0.Fit(self.pnl)
        sizer0.SetSizeHints(self.pnl)
        self.pnl.Layout()
        self.Show(True)

    def readcaptions(self, lang):
        self.captions = {}
        with open(os.path.join(hks.HERE, lang)) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value
        return self.captions

    def OnMenu(self, event):
        id = str(event.GetId())
        text = MENU_FUNC[id](self)
        if text:
            dlg = wx.MessageDialog(self,text,self.captions["000"], wx.OK)
            h = dlg.ShowModal()
            dlg.Destroy()

    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        ## sel = self.GetSelection()
        ## self.log.write('OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def OnPageChanging(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        ## sel = self.GetSelection()
        ## self.log.write('OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel))
        event.Skip()

    def afsl(self, evt=None):
        self.Close(True)

def main(args=None):
    app = wx.App(redirect=True, filename="hotkeys.log")
    print '----------'
    frame = MainWindow(None, -1, args)
    app.MainLoop()

if __name__ == "__main__":
    main()
