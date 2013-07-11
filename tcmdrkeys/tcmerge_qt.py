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
        cb.setMinimumWidth(160)
        cb.currentIndexChanged[str].connect(functools.partial(self.on_choice, cb))
        te = gui.QTextEdit(pnl)
        te.setMaximumHeight(80)
        te.setReadOnly(True)
        self.cmb_key = cb
        self.txt_key = te
        cb = gui.QComboBox(pnl)
        cb.setMinimumWidth(160)
        cb.currentIndexChanged[str].connect(functools.partial(self.on_choice, cb))
        te = gui.QTextEdit(pnl)
        te.setMaximumHeight(80)
        te.setReadOnly(True)
        self.cmb_cmd = cb
        self.txt_cmd = te

        self.btn_link = gui.QPushButton("&+ Add/Replace Link", pnl)
        self.btn_link.clicked.connect(self.make_link)
        ## self.btn_edit = gui.QButton(pnl,-1,"&Modify Link")
        ## self.btn_edit.Bind(gui.QEVT_BUTTON,self.edit_link)
        self.btn_delete = gui.QPushButton("&- Discard Link", pnl)
        self.btn_delete.clicked.connect(self.delete_link)

        self.lst_links = gui.QTreeWidget(pnl)
        self.lst_links.resize(460,300)
        widths = (70, 60, 100, 200)
        self.lst_links.setHeaderLabels(("Key", "Number", "Command", "Description"))
        hdr = self.lst_links.header()
        hdr.setClickable(True)
        for indx, wid in enumerate(widths):
            hdr.resizeSection(indx, wid)
        hdr.setStretchLastSection(True)
        self.lst_links.currentItemChanged.connect(self.enable_edit)

        self.btn_save = gui.QPushButton("&Save Links", pnl)
        self.btn_save.clicked.connect(self.save_links)
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
        ## vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.txt_key)
        ## vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.cmb_cmd)
        ## vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.txt_cmd)
        ## vbox2.addStretch()
        hbox.addLayout(vbox2)
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.btn_link)
        hbox.addWidget(self.btn_delete)
        hbox.addStretch()
        vbox.addLayout(hbox)

        hbox = gui.QHBoxLayout()
        vbox2 = gui.QVBoxLayout()
        vbox2.addWidget(self.lst_links)
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
        filemenu.addAction(gui.QAction("&Clear definitions and reload datafiles",
            self, triggered=self.reset))
        filemenu.addAction(gui.QAction("&Exit", self, triggered=self.quit))

    def load_file(self, fileid=None, ask=True):
        if fileid is not None:
            naam = self.files.keys()[fileid]
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

    def ask_file(self, naam, ask=True):
        """vraag de locatie van het bestand en haal het op
        als alle bestanden bekend zijn de tabellen initialiseren"""
        fn = self.files[naam][0]
        pad = ""
        while True:
            pad = str(gui.QFileDialog.getExistingDirectory(self, "Selecteer"
                " de directory met {0} erin".format(fn), self.basedir))
            if pad:
                self.basedir = pad
            if not pad or os.path.exists(os.path.join(pad,fn)):
                break
            h = gui.QMessageBox.information(self, 'Helaas',
                'Dit file staat niet in deze directory',
                gui.QMessageBox.Ok | gui.QMessageBox.Cancel)
            if h == gui.QCANCEL:
                break
        return pad

    def load_key(self,pad):
        self.keydict = dict(keyboardtext(pad))
        self.cmb_key.clear()
        self.cmb_key.addItems(sorted(self.keydict.keys()))
        self.cmb_key.setCurrentIndex(0)
        ## try
        this = self.keydict[str(self.cmb_key.itemText(self.cmb_key.currentIndex()))]
        ## except KeyError as msg:
            ## print msg
        self.txt_key.setText(this)

    def load_cmd(self,pad):
        self.cmddict, self.omsdict = defaultcommands(pad)
        self.cmds = dict([reversed(x) for x in self.cmddict.items()])
        self.cmb_cmd.clear()
        self.cmb_cmd.addItems(sorted(self.omsdict.keys()))
        self.cmb_cmd.insertItems(0, '')
        self.cmb_cmd.setCurrentIndex(0)
        self.txt_cmd.setText('no command available') #self.omsdict[self.cmb_cmd.GetValue()])

    def load_usr(self,pad):
        self.usrdict, self.uomsdict = usercommands(pad)

    def load_ini(self,pad):
        self.usrkeys = dict(userkeys(pad))

    def setup(self):
        if not all([y[1] for y in self.files.values()]):
            return
        self.lst_links.clear()
        self.btn_link.setEnabled(True)
        self.data = []

    def load_links(self,evt):
        fname = gui.QFileDialog.getOpenFileName(self, "Select definition file",
            self.basedir, "csv files (*.csv)")
            ## defaultFile="TC_hotkeys.csv",
        if fname:
            self.lst_links.clear()
            self.btn_link.setEnabled(True)
            rdr = csv.reader(open(fname,'rb'))
            for row in rdr:
                new = gui.QTreeWidgetItem(row)
                self.lst_links.addTopLevelItem(new)
                ## ix = self.lst_links.InsertStringItem(sys.maxint,row[0])
                ## self.lst_links.SetStringItem(ix,1,row[1])
                ## self.lst_links.SetStringItem(ix,2,row[2])
                ## self.lst_links.SetStringItem(ix,3,row[3])
            self.btn_save.setEnabled(True)

    def on_choice(self, cb, text):
        text = str(text)
        ## self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)
        if cb == self.cmb_key:
            try:
                self.txt_key.setText(self.keydict[text])
            except KeyError:
                pass
        elif cb == self.cmb_cmd:
            try:
                self.txt_cmd.setText(self.omsdict[text])
            except KeyError:
                self.txt_cmd.setText('no command available')

    def get_entry(self):
        gekozen_key = str(self.cmb_key.currentText())
        gekozen_cmd = str(self.cmb_cmd.currentText())
        print(gekozen_key, gekozen_cmd)
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
        for ix in range(self.lst_links.topLevelItemCount()):
            item = self.lst_links.topLevelItem(ix)
            if str(item.text(0)) == gekozen_key:
                found = True
                break
        if not found:
            item = gui.QTreeWidgetItem()
            item.setText(0, gekozen_key)
            self.lst_links.addTopLevelItem(item)
        item.setText(1,gekozen_code)
        item.setText(2,gekozen_cmd)
        item.setText(3,gekozen_oms)
        ## self.lst_links.EnsureVisible(ix)
        self.btn_save.setEnabled(True)

    def enable_edit(self, item, previtem):
        gekozen_key = str(item.text(0))
        gekozen_cmd = str(item.text(2))
        self.cmb_key.setCurrentIndex(sorted(self.keydict.keys()).index(gekozen_key)) # setEditText(gekozen_key)
        # let op: het volgende gaat niet werken als menu optie 1 nog niet is uitgevoerd
        self.txt_key.setText(self.keydict[gekozen_key])
        self.cmb_cmd.setCurrentIndex(sorted(self.omsdict.keys()).index(gekozen_cmd)) # setEditText(gekozen_cmd)
        try:
            self.txt_cmd.setText(self.omsdict[gekozen_cmd])
        except KeyError:
            self.txt_cmd.setText('no command available')
        ## self.btn_edit.Enable()
        self.btn_delete.setEnabled(True)

    ## def edit_link(self,evt):
        ## gekozen_key, gekozen_code, gekozen_cmd, gekozen_oms = self.get_entry()
        ## self.lst_links.SetStringItem(ix,0,gekozen_key)
        ## self.lst_links.SetStringItem(ix,1,gekozen_code)
        ## self.lst_links.SetStringItem(ix,2,gekozen_cmd)
        ## self.lst_links.SetStringItem(ix,3,gekozen_oms)
        ## self.ix = -1
        ## self.btn_edit.Disable()
        ## self.btn_delete.Disable()

    def delete_link(self, evt):
        ok = gui.QMessageBox.question(self, "Delete entry", "Really delete?",
            gui.QMessageBox.Yes | gui.QMessageBox.No,
            defaultButton = gui.QMessageBox.Yes)
        if ok == gui.QMessageBox.Yes:
            item = self.lst_links.currentItem()
            ix = self.lst_links.indexOfTopLevelItem(item)
            self.lst_links.takeTopLevelItem(ix)
            ## self.btn_edit.Disable()
            self.btn_delete.setEnabled(False)

    def save_links(self,evt):
        fname = gui.QFileDialog.getSaveFileName(self, "Save definition file",
            os.path.join(self.basedir, "TC_hotkeys.csv"), "csv files (*.csv)")
        if fname:
            wrtr = csv.writer(open(fname,"wb"))
            for ix in range(self.lst_links.topLevelItemCount()):
                item = self.lst_links.topLevelItem(ix)
                wrtr.writerow([str(item.text(x)) for x in range(4)])

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

