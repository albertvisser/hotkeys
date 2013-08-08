# -*- coding: UTF-8 -*-
from __future__ import print_function
import os
import sys
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import hotkeys_shared as hks
from tckey_qtgui import TCPanel
from vikey_qtgui import VIPanel
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
def show_message(self, message_id, caption_id='000'):
    """toon de boodschap geïdentificeerd door <message_id> in een dialoog
    met als titel aangegeven door <caption_id> en retourneer het antwoord
    na sluiten van de dialoog
    """
    ok = gui.QMessageBox.information(self, self.captions[message_id],
        self.captions[caption_id])
    return ok

def m_read(self):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    gui.QMessageBox.information(self, 'Lezen gekozen', self.captions['000'])
    return
    if not self.modified:
        h = show_message(self, '041')
        if h: # = gui.QMessageBox.Ok
            self.readkeys()
            self.page.populate_list()

def m_save(self):
    """(menu) callback voor het terugschrijven van de hotkeys

    vraagt eerst of het ok is om de hotkeys weg te schrijven
    vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
    """
    gui.QMessageBox.information(self, 'Opslaan gekozen', self.captions['000']) #hks.NOT_IMPLEMENTED)
    return
    if not self.modified:
        h = show_message(self, '041')
        if h != gui.QMessageBox.Ok:
            return
    self.savekeys()
    if self.ini.restart:
        h = show_message(self, '026')
        if h == gui.QMessageBox.Ok:
            os.system(self.ini.restart)
    else:
        gui.QMessageBox.information(self, self.captions['037'], self.captions['000'])
        ## h = show_message(self, '037')

def m_user(self):
    """(menu) callback voor een nog niet geïmplementeerde actie"""
    return self.captions[hks.NOT_IMPLEMENTED]

def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.close()

def m_loc(self):    # TODO: FilesDialog (in TCkey_gui aanpassen maar die wordt hier niet geimporteerd)
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    gui.QMessageBox.information(self, 'paden gekozen', self.captions['000']) #hks.NOT_IMPLEMENTED)
    return
    if self.modified:
        h = show_message(self, '025')
        if h == gui.QMessageBox.Ok:
            self.savekeys()
        elif h == gui.QMessageBox.Cancel:
            return
    paths = [self.ini.pad,]
    captions = [self.captions[x] for x in ('028','044','039')]
    ## captions = ['Define file locations for:', 'TC','UC','CI','KT','HK']
    dlg = FilesDialog(self, -1, self.captions["000"], paths, captions,
        size=(400, 200),
        #style=gui.QCAPTION | gui.QSYSTEM_MENU | gui.QTHICK_FRAME,
        style=gui.QDEFAULT_DIALOG_STYLE, # & ~gui.QCLOSE_BOX,
        )
    ## dlg.CenterOnScreen()
    fout = "*"
    text = ''
    while fout:
        val = dlg.ShowModal()
        pad = dlg.bVI.GetValue()
        fout = ""
        if val == gui.QID_OK:
            text = "modified"
            if pad != "":
                naam = self.captions['044']
                if not os.path.isdir(pad):
                    fout = self.captions['034'] % naam
                elif not os.path.exists(os.path.join(pad,naam)):
                    fout = self.captions['035'] % naam
        if fout:
            mdlg = gui.QMessageDialog(self,fout,self.captions["000"])
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
    indx = y.index(self.ini.lang) if self.ini.lang in y else 0
    ## for i, x in enumerate(y):
        ## print x, self.ini.lang
        ## if x == self.ini.lang:
            ## indx =
            ## break
    lang, ok = gui.QInputDialog.getItem(self, self.captions["027"], self.captions["000"],
        y, current=indx, editable=False)
    if ok:
        self.ini.lang = lang
        self.ini.write()
        self.readcaptions()
        self.setcaptions()

def m_about(self):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    info = gui.QMessageBox.about(self, self.captions['000'],
        "{}\nversion {}\n{}\n{}".format(hks.TTL, hks.VRS, hks.AUTH, hks.XTRA))

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
class ChoiceBook(gui.QFrame): #Widget):
    """ Als Tabwidget, maar met selector in plaats van tabs
    """
    def __init__(self, parent):
        ## gui.QWidget.__init__(self, parent)
        gui.QFrame.__init__(self, parent)
        self.sel = gui.QComboBox(self)
        self.sel.addItems(pagetexts)
        self.sel.currentIndexChanged.connect(self.on_page_changed)
        self.pnl = gui.QStackedWidget(self)
        for txt in pagetexts:
            if txt == "VI":
                win = VIPanel(self.pnl)
                win.doelayout()
            elif txt == 'Total Commander':
                win = TCPanel(self.pnl)
            else:
                win = gui.QFrame(self.pnl)
                st = gui.QLabel('Sorry, no interface yet for ' + txt, win)
            self.pnl.addWidget(win)
        vbox = gui.QVBoxLayout()
        hbox = gui.QVBoxLayout()
        hbox.addWidget(self.sel)
        vbox.addLayout(hbox)
        hbox = gui.QVBoxLayout()
        hbox.addWidget(self.pnl)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.on_page_changed(0)

    def on_page_changed(self, indx):
        self.pnl.setCurrentIndex(indx)
        if self.pnl.currentIndex() == 1:
            menus = hks.TC_MENU
        else:
            menus = hks.VI_MENU
        self.parent().setup_menu(menus)

class MainWindow(gui.QMainWindow):
    """Hoofdscherm van de applicatie"""
    def __init__(self, args):
        wid = 860 if hks.LIN else 688
        hig = 594
        gui.QMainWindow.__init__(self)
        self.setWindowTitle("tcmdrkeys")
        self.resize(wid, hig)
        self.sb = self.statusBar()
        self.sb.showMessage('Welcome to HotKeys!')
        self.readcaptions('english.lng')
        self.menu_bar = self.menuBar()

        self.book = ChoiceBook(self) # , size= (600, 700))
        self.setCentralWidget(self.book)
        ## self.setup_menu()
        self.show()

    def readcaptions(self, lang):
        self.captions = {}
        with open(os.path.join(hks.HERE, lang)) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value

    def setup_menu(self, menus):
        self.menu_bar.clear()
        for title, items in menus:
            menu = self.menu_bar.addMenu(self.captions[title])
            for sel in items:
                if sel == -1:
                    menu.addSeparator()
                else:
                    act = gui.QAction(self.captions[sel], self)
                    act.triggered.connect(functools.partial(self.on_menu, sel))
                    menu.addAction(act)

    def on_menu(self, actionid):
        text = MENU_FUNC[actionid](self)
        if text:
            gui.QMessageBox.information(self, text, self.captions["000"])

    def afsl(self, evt=None): #TODO
        self.close()

def main(args=None):
    app = gui.QApplication(sys.argv)
    ## redirect=True, filename="hotkeys.log")
    ## print '----------'
    frame = MainWindow(args)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
