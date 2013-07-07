# -*- coding: UTF-8 -*-
import sys,os
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import wx
import functools
from tccm_mixin import TCCMMixin
from tcmdrkys import keyboardtext, defaultcommands, usercommands, userkeys
import csv

# verbinden van een toets aan een "dummy" mogelijk maken zodat de key in het bestand zit
# ook al is er geen commando voor

class MainFrame(gui.QMainWindow, TCCMMixin):
    def __init__(self, parent=None):
        """Opbouwen van het scherm"""
        self.files = {
            'key': ['KEYBOARD.TXT','',self.load_key],
            'cmd': ['TOTALCMD.INC','',self.load_cmd],
            'usr': ['usercmd.ini','',self.load_usr],
            'ini': ['wincmd.ini','',self.load_ini]
            }
        self.basedir = os.getcwd()
        gui.QMainWindow.__init__(self,parent)
        self.setWindowTitle("TCCM")
        self.resize(650,486)
        ## home = os.path.split(__file__)[0]
        ## self.apoicon = gui.QIcon(os.path.join(home,"apropos.ico"),gui.QBITMAP_TYPE_ICO)
        ## self.SetIcon(self.apoicon)

        self.setup_menu()

        pnl = gui.QFrame(self)
        cb = gui.QComboBox(pnl)
        cb.setMinimumWidth(80)
        ## cb.itemSelected.connect(self.EvtText)
        ## cb.editTextChanged.connect(self.EvtText)
        te = gui.QTextEdit(pnl)
        te.resize=(200,80)
        te.setReadOnly(True)
        self.cmb_key = cb
        self.txt_key = te
        cb = gui.QComboBox(pnl)
        cb.setMinimumWidth(120)
        ## cb.itemSelected.connect(self.EvtText)
        ## cb.editTextChanged.connect(self.EvtText)
        te = gui.QTextEdit(pnl)
        te.resize=(200,80)
        te.setReadOnly(True)
        self.cmb_cmd = cb
        self.txt_cmd = te

        self.btn_link = gui.QPushButton("&Add/Edit Link", pnl)
        ## self.btn_link.clicked.connect(self.make_link)

        self.lst_links = gui.QTreeWidget(pnl)
        self.lst_links.resize(460,300)
        widths = (70, 60, 100, 200)
        self.lst_links.setHeaderLabels(("Key", "Number", "Command", "Description"))
        hdr = self.lst_links.header()
        hdr.setClickable(True)
        for indx, wid in enumerate(widths):
            hdr.resizeSection(indx, wid)
        hdr.setStretchLastSection(True)
        ## self.lst_links.Bind(gui.QEVT_LIST_ITEM_SELECTED,self.enable_edit)
        ## self.btn_edit = gui.QButton(pnl,-1,"&Modify Link")
        ## self.btn_edit.Bind(gui.QEVT_BUTTON,self.edit_link)
        self.btn_delete = gui.QPushButton("&Discard Link", pnl)
        ## self.btn_delete.clicked.connect(self.delete_link)

        self.btn_save = gui.QPushButton("&Save Links", pnl)
        ## self.btn_save.clicked.connect(self.save_links)
        self.btn_quit = gui.QPushButton("&Afsluiten", pnl)
        self.btn_quit.clicked.connect(self.quit)

        self.btn_link.setEnabled(False)
        ## self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)
        self.btn_save.setEnabled(False)

        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.cmb_key)
        vbox2.addStretch()
        hbox.addLayout(vbox2)
        hbox.addWidget(self.txt_key)
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.cmb_cmd)
        vbox2.addStretch()
        hbox.addLayout(vbox2)
        hbox.addWidget(self.txt_cmd)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.btn_link)
        vbox2.addStretch()
        hbox.addLayout(vbox2)
        hbox.addWidget(self.lst_links)
        vbox2 = gui.QVBoxLayout()
        ## vbox2.Add(self.btn_edit)
        vbox2.addWidget(self.btn_delete)
        vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox.addLayout(hbox)
        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.btn_save)
        hbox.addWidget(self.btn_quit)
        hbox.addStretch()
        vbox.addLayout(hbox)
        pnl.setLayout(vbox)
        self.setCentralWidget(pnl)
        ## self.Bind(gui.QEVT_CLOSE,self.afsl)
        self.show()

    def setup_menu(self):
        menu_bar = self.menuBar()
        filemenu = menu_bar.addMenu("&File")

        submenu = filemenu.addMenu("Open &datafiles")
        self.menu_open = []
        for item in [x[0] for x in self.files.values()]:
            action = gui.QAction("Open &" + item, self)
            action.setCheckable(True)
            self.menu_open.append(action)
            action.triggered.connect(functools.partial(self.load_file,
                self.menu_open.index(action)))
            submenu.addAction(action)
        submenu.addSeparator()
        submenu.addAction(gui.QAction("&All-in-one", self, triggered=self.load_all))

        filemenu.addAction(gui.QAction("&Open definitions file", self,
            triggered=self.load_links))
        filemenu.addAction(gui.QAction("&Save definitions file ", self,
            triggered=self.save_links))
        filemenu.addAction(gui.QAction("&Clear definitions and reload datafiles", self,
            triggered=self.reset))
        filemenu.addAction(gui.QAction("&Exit", self, triggered=self.quit))

    def load_file(self,evt=None,ask=True): # TODO
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
            for naam in self.files.keys():
                self.files[naam][1] = pad
                self.files[naam][2](pad)
            self.setup()

    def ask_file(self,naam,ask=True): # TODO
        """vraag de locatie van het bestand en haal het op
        als alle bestanden bekend zijn de tabellen initialiseren"""
        fn = self.files[naam][0]
        pad = ""
        while True:
            dlg = gui.QDirDialog(self, "Selecteer de directory met {0} erin".format(fn),
                defaultPath=self.basedir,
                style=gui.QDD_DEFAULT_STYLE
                )
            if dlg.ShowModal() == gui.QID_OK:
                pad = dlg.GetPath()
                self.basedir = pad
            dlg.Destroy()
            if not pad or os.path.exists(os.path.join(pad,fn)):
                break
            dlg = gui.QMessageDialog(self,'Dit file staat niet in deze directory',
                'Helaas',gui.QOKCancel)
            h = dlg.ShowModal()
            dlg.Destroy()
            if h == gui.QCANCEL:
                break
        return pad

    def load_key(self,pad): # TODO
        self.keydict = dict(keyboardtext(pad))
        print self.keydict
        self.cmb_key.Clear()
        self.cmb_key.AppendItems(sorted(self.keydict.keys()))
        self.cmb_key.SetSelection(0)
        try:
            self.txt_key.SetValue(self.keydict[self.cmb_key.GetValue()])
        except KeyError as msg:
            print msg

    def load_cmd(self,pad): # TODO
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

    def setup(self): # TODO
        if not all([y[1] for y in self.files.values()]):
            return
        self.lst_links.DeleteAllItems()
        self.btn_link.Enable()
        self.data = []

    def load_links(self,evt): # TODO
        pad = ''
        dlg = gui.QFileDialog(self, message="Select definition file",
            defaultDir=self.basedir,
            defaultFile="TC_hotkeys.csv",
            wildcard="csv files (*.csv)|*.csv",
            style=gui.QOPEN
            )
        if dlg.ShowModal() == gui.QID_OK:
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

    def EvtText(self, evt): # TODO
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

    def get_entry(self): # TODO
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

    def make_link(self,evt): # TODO
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

    def enable_edit(self,evt): # TODO
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

    def delete_link(self,evt): # TODO
        dlg = gui.QMessageDialog(self,-1,"Really delete?","Delete entry",
            style=gui.QYES_NO)
        if dlg.ShowModal == gui.QYES:
            self.lst_links.DeleteItem(self.ix)
            self.ix = -1
            ## self.btn_edit.Disable()
            self.btn_delete.Disable()
        dlg.Destroy()

    def save_links(self,evt): # TODO
        dlg = gui.QFileDialog(self, message="Save definition file",
            defaultDir=self.basedir,
            defaultFile="TC_hotkeys.csv",
            wildcard="csv files (*.csv)|*.csv",
            style=gui.QSAVE
            )
        if dlg.ShowModal() == gui.QID_OK:
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
        self.close()

def main():
    app = gui.QApplication(sys.argv) # redirect=True,filename="tccm.log")
    frm = MainFrame()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

