import sys,os
import wx
from tccm_mixin import TCCMMixin
from tcmdrkys import keyboardtext, defaultcommands, usercommands, userkeys
import csv

# verbinden van een toets aan een "dummy" mogelijk maken zoadt de key in het bestand zit ook a;l is er geen
# commando voor

class MainFrame(wx.Frame,TCCMMixin):
    def __init__(self,parent,id):
        """Opbouwen van het scherm"""
        self.files = {
            'key': ['KEYBOARD.TXT','',self.load_key],
            'cmd': ['TOTALCMD.INC','',self.load_cmd],
            'usr': ['USERCMD.INI','',self.load_usr],
            'ini': ['WINCMD.INI','',self.load_ini]
            }
        self.basedir = os.getcwd()
        wx.Frame.__init__(self,parent,id,"TCCM",size=(650,486))
        ## home = os.path.split(__file__)[0]
        ## self.apoicon = wx.Icon(os.path.join(home,"apropos.ico"),wx.BITMAP_TYPE_ICO)
        ## self.SetIcon(self.apoicon)
        pnl = wx.Panel(self,-1)

        menuBar = wx.MenuBar()
        filemenu = wx.Menu()

        submenu = wx.Menu()
        self.menu_open = []
        for item in [x[0] for x in self.files.values()]:
            menu_id = wx.NewId()
            ## print item,menu_id
            mnu = wx.MenuItem(submenu, menu_id, text="Open &" + item,
                kind=wx.ITEM_CHECK
                )
            submenu.AppendItem(mnu)
            self.menu_open.append(menu_id)
            self.Bind(wx.EVT_MENU, self.load_file, id=menu_id)
        submenu.AppendSeparator()
        menu_id = wx.NewId()
        submenu.Append(menu_id, "&All-in-one")
        self.Bind(wx.EVT_MENU, self.load_all, id=menu_id)

        filemenu.AppendMenu(-1, "Open &datafiles",submenu)

        menu_id = wx.NewId()
        filemenu.Append(menu_id, "&Open definitions file")
        self.Bind(wx.EVT_MENU, self.load_links, id=menu_id)

        menu_id = wx.NewId()
        filemenu.Append(menu_id, "&Save definitions file ")
        self.Bind(wx.EVT_MENU, self.save_links, id=menu_id)

        menu_id = wx.NewId()
        filemenu.Append(menu_id, "&Clear definitions and reload datafiles")
        self.Bind(wx.EVT_MENU, self.reset, id=menu_id)

        menu_id = wx.NewId()
        filemenu.Append(menu_id, "&Exit")
        self.Bind(wx.EVT_MENU, self.quit, id=menu_id)
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)

        cb = wx.ComboBox(pnl,-1,size=(80,-1),style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtText, cb)
        self.Bind(wx.EVT_TEXT, self.EvtText, cb)
        self.cmb_key = cb
        self.txt_key = wx.TextCtrl(pnl,-1,size=(200,80),
            style=wx.TE_READONLY | wx.TE_MULTILINE)
        cb = wx.ComboBox(pnl,-1,size=(120,-1),style=wx.CB_DROPDOWN)
        self.Bind(wx.EVT_COMBOBOX, self.EvtText, cb)
        self.Bind(wx.EVT_TEXT, self.EvtText, cb)
        self.cmb_cmd = cb
        self.txt_cmd = wx.TextCtrl(pnl,-1,size=(200,80),
            style=wx.TE_READONLY | wx.TE_MULTILINE)

        self.btn_link = wx.Button(pnl,-1,"&Add/Edit Link")
        self.btn_link.Bind(wx.EVT_BUTTON,self.make_link)
        self.lst_links = wx.ListCtrl(pnl,-1,size=(460,300),
            style = wx.LC_REPORT )
        self.lst_links.InsertColumn(0,"Key",width=70)
        self.lst_links.InsertColumn(1,"Number",width=55)
        self.lst_links.InsertColumn(2,"Command",width=160)
        self.lst_links.InsertColumn(3,"Description",width=200)
        self.lst_links.Bind(wx.EVT_LIST_ITEM_SELECTED,self.enable_edit)
        ## self.btn_edit = wx.Button(pnl,-1,"&Modify Link")
        ## self.btn_edit.Bind(wx.EVT_BUTTON,self.edit_link)
        self.btn_delete = wx.Button(pnl,-1,"&Discard Link")
        self.btn_delete.Bind(wx.EVT_BUTTON,self.delete_link)

        self.btn_save = wx.Button(pnl,-1,"&Save Links")
        self.btn_save.Bind(wx.EVT_BUTTON,self.save_links)
        self.btn_quit = wx.Button(pnl,-1,"&Afsluiten")
        self.btn_quit.Bind(wx.EVT_BUTTON,self.quit)

        self.btn_link.Disable()
        ## self.btn_edit.Disable()
        self.btn_delete.Disable()
        self.btn_save.Disable()

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.cmb_key,0,wx.ALL, 5)
        hbox.Add(self.txt_key,0,wx.ALL, 5)
        hbox.Add(self.cmb_cmd,0,wx.ALL, 5)
        hbox.Add(self.txt_cmd,0,wx.ALL, 5)
        vbox.Add(hbox,0,wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.btn_link,0,wx.ALL, 1)
        hbox.Add(self.lst_links,0, wx.ALL | wx.EXPAND, 5)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        ## vbox2.Add(self.btn_edit)
        vbox2.Add(self.btn_delete)
        hbox.Add(vbox2,0,wx.EXPAND)
        vbox.Add(hbox,0,wx.ALIGN_CENTER_HORIZONTAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.btn_save)
        hbox.Add(self.btn_quit)
        vbox.Add(hbox,0,wx.ALIGN_CENTER_HORIZONTAL)
        pnl.SetSizer(vbox)
        pnl.SetAutoLayout(True)
        vbox.Fit(pnl)
        vbox.SetSizeHints(pnl)
        pnl.Layout()
        ## self.Bind(wx.EVT_CLOSE,self.afsl)
        self.Show()

    def load_file(self,evt=None,ask=True):
        ## print evt.EventObject
        ## print evt.Id
        if evt is not None:
            naam = self.files.keys()[self.menu_open.index(evt.Id)]
        ## print naam
        if ask:
            pad = self.ask_file(naam)
            if not pad:
                return
            self.files[naam][1] = pad
            self.files[naam][2](pad)
        self.setup()

    def load_all(self,evt):
        naam = 'ini'
        pad = self.ask_file(naam)
        if pad:
            for key in self.files.keys():
                self.files[key][1] = pad
                self.files[key][2](pad)
            self.setup()

    def ask_file(self,naam,ask=True):
        """vraag de locatie van het bestand en haal het op
        als alle bestanden bekend zijn de tabellen initialiseren"""
        fn = self.files[naam][0]
        pad = ""
        while True:
            dlg = wx.DirDialog(self, "Selecteer de directory met {0} erin".format(fn),
                defaultPath=self.basedir,
                style=wx.DD_DEFAULT_STYLE
                )
            if dlg.ShowModal() == wx.ID_OK:
                pad = dlg.GetPath()
                self.basedir = pad
            dlg.Destroy()
            if not pad or os.path.exists(os.path.join(pad,fn)):
                break
            dlg = wx.MessageDialog(self,'Dit file staat niet in deze directory',
                'Helaas',wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        return pad

    def load_key(self,pad):
        self.keydict = dict(keyboardtext(pad))
        self.cmb_key.Clear()
        self.cmb_key.AppendItems(sorted(self.keydict.keys()))
        self.cmb_key.SetSelection(0)
        self.txt_key.SetValue(self.keydict[self.cmb_key.GetValue()])

    def load_cmd(self,pad):
        self.cmddict, self.omsdict = defaultcommands(pad)
        self.cmds = dict([reversed(x) for x in self.cmddict.items()])
        self.cmb_cmd.Clear()
        self.cmb_cmd.AppendItems(sorted(self.omsdict.keys()))
        self.cmb_cmd.Insert('',0)
        self.cmb_cmd.SetSelection(0)
        self.txt_cmd.SetValue('no command available') #self.omsdict[self.cmb_cmd.GetValue()])

    def load_usr(self,pad):
        self.usrdict, self.uomsdict = usercommands(pad)

    def load_ini(self,pad):
        self.usrkeys = dict(userkeys(pad))

    def setup(self):
        if not all([y[1] for y in self.files.values()]):
            return
        self.lst_links.DeleteAllItems()
        self.btn_link.Enable()
        self.data = []

    def load_links(self,evt):
        dlg = wx.FileDialog(self, message="Select definition file",
            defaultDir=self.basedir,
            defaultFile="TC_hotkeys.csv",
            wildcard="csv files (*.csv)|*.csv",
            style=wx.OPEN
            )
        if dlg.ShowModal() == wx.ID_OK:
            pad = dlg.GetPath()
        dlg.Destroy()
        if pad:
            self.lst_links.DeleteAllItems()
            self.btn_link.Enable()
            rdr = csv.reader(open(pad,'rb'))
            for row in rdr:
                ix = self.lst_links.InsertStringItem(sys.maxint,row[0])
                self.lst_links.SetStringItem(ix,1,row[1])
                self.lst_links.SetStringItem(ix,2,row[2])
                self.lst_links.SetStringItem(ix,3,row[3])
            self.btn_save.Enable()

    def EvtText(self, evt):
        self.ix = -1
        ## self.btn_edit.Disable()
        self.btn_delete.Disable()
        cb = evt.GetEventObject()
        if cb == self.cmb_key:
            try:
                self.txt_key.SetValue(self.keydict[evt.GetString()])
            except KeyError:
                pass
        elif cb == self.cmb_cmd:
            try:
                self.txt_cmd.SetValue(self.omsdict[evt.GetString()])
            except KeyError:
                self.txt_cmd.SetValue('no command available')
        evt.Skip()

    def get_entry(self):
        gekozen_key = self.cmb_key.GetValue()
        gekozen_cmd = self.cmb_cmd.GetValue()
        try:
            gekozen_oms = self.omsdict[gekozen_cmd]
        except KeyError:
            gekozen_cmd = ''
            gekozen_oms = self.keydict[gekozen_key]
            gekozen_code = ''
        else:
            gekozen_code = self.cmds[gekozen_cmd]
        return gekozen_key, gekozen_code, gekozen_cmd, gekozen_oms

    def make_link(self,evt):
        gekozen_key, gekozen_code, gekozen_cmd, gekozen_oms = self.get_entry()
        # let op: als link al bestaat: vervangen, niet toevoegen
        found = False
        for ix in range(self.lst_links.ItemCount):
            if self.lst_links.GetItemText(ix) == gekozen_key:
                found = True
                break
        if not found:
            ix = self.lst_links.InsertStringItem(sys.maxint,gekozen_key)
        ## self.lst_links.SetStringItem(ix,0,gekozen_key)
        self.lst_links.SetStringItem(ix,1,gekozen_code)
        self.lst_links.SetStringItem(ix,2,gekozen_cmd)
        self.lst_links.SetStringItem(ix,3,gekozen_oms)
        self.lst_links.EnsureVisible(ix)
        self.btn_save.Enable()

    def enable_edit(self,evt):
        ix = evt.m_itemIndex
        gekozen_key = self.lst_links.GetItemText(ix)
        gekozen_cmd = self.lst_links.GetItem(ix, 2).m_text
        self.cmb_key.SetValue(gekozen_key)
        self.txt_key.SetValue(self.keydict[gekozen_key])
        self.cmb_cmd.SetValue(gekozen_cmd)
        try:
            self.txt_cmd.SetValue(self.omsdict[gekozen_cmd])
        except KeyError:
            self.txt_cmd.SetValue('no command available')
        ## self.btn_edit.Enable()
        self.btn_delete.Enable()
        self.ix = ix

    ## def edit_link(self,evt):
        ## gekozen_key, gekozen_code, gekozen_cmd, gekozen_oms = self.get_entry()
        ## self.lst_links.SetStringItem(ix,0,gekozen_key)
        ## self.lst_links.SetStringItem(ix,1,gekozen_code)
        ## self.lst_links.SetStringItem(ix,2,gekozen_cmd)
        ## self.lst_links.SetStringItem(ix,3,gekozen_oms)
        ## self.ix = -1
        ## self.btn_edit.Disable()
        ## self.btn_delete.Disable()

    def delete_link(self,evt):
        dlg = wx.MessageDialog(self,-1,"Really delete?","Delete entry",
            style=wx.YES_NO)
        if dlg.ShowModal == wx.YES:
            self.lst_links.DeleteItem(self.ix)
            self.ix = -1
            ## self.btn_edit.Disable()
            self.btn_delete.Disable()
        dlg.Destroy()

    def save_links(self,evt):
        dlg = wx.FileDialog(self, message="Save definition file",
            defaultDir=self.basedir,
            defaultFile="TC_hotkeys.csv",
            wildcard="csv files (*.csv)|*.csv",
            style=wx.SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            pad = dlg.GetPath()
        dlg.Destroy()
        if pad:
            wrtr = csv.writer(open(pad,"wb"))
            for ix in range(self.lst_links.ItemCount):
                wrtr.writerow((
                    self.lst_links.GetItemText(ix),
                    self.lst_links.GetItem(ix,1).GetText(),
                    self.lst_links.GetItem(ix,2).GetText(),
                    self.lst_links.GetItem(ix,3).GetText()
                ))

    def reset(self,evt):
        self.setup()

    def quit(self,evt):
        self.Destroy()

class Main():
    def __init__(self):
        app = wx.App(redirect=False) # redirect=True,filename="tccm.log")
        frm = MainFrame(None, -1)
        app.MainLoop()

if __name__ == "__main__":
    Main()

