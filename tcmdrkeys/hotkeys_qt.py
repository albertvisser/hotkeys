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
from __future__ import print_function
import os
import sys
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
from .hotkeys_shared import * # constants
from .tc_plugin import TC_MENU, TC_MENU_FUNC
from .tc_plugin import MyPanel as TCPanel
from .vi_plugin import MyPanel as VIPanel
from .scite_plugin import MyPanel as SciTEPanel
from .opera_plugin import MyPanel as OperaPanel
from .generic_plugin import MyPanel as EmptyPanel
PLUGINS = [
    ("VI", VIPanel),
    ("Total Commander", TCPanel),
    ("SciTE", SciTEPanel),
    ("Double Commander", None),
    ("Opera", OperaPanel)
    ]

class ChoiceBook(gui.QFrame): #Widget):
    """ Als QTabwidget, maar met selector in plaats van tabs
    """
    def __init__(self, parent):
        ## gui.QWidget.__init__(self, parent)
        self.parent = parent.parent()
        gui.QFrame.__init__(self, parent)
        self.sel = gui.QComboBox(self)
        self.sel.addItems([txt[0] for txt in PLUGINS]) #pagetexts)
        self.sel.currentIndexChanged.connect(self.on_page_changed)
        self.pnl = gui.QStackedWidget(self)
        self.captions = self.parent.captions
        for txt, win in PLUGINS:
            if win is None:
                self.pnl.addWidget(EmptyPanel(self.pnl, 'Nog geen plugin voor ' + txt))
            else:
                self.pnl.addWidget(win(self.pnl))
        vbox = gui.QVBoxLayout()
        hbox = gui.QVBoxLayout()
        hbox.addWidget(self.sel)
        vbox.addLayout(hbox)
        hbox = gui.QVBoxLayout()
        hbox.addWidget(self.pnl)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def on_page_changed(self, indx):
        page = self.pnl.currentWidget() ## self.parent().page
        self.parent.sb.showMessage('View/edit {} keyboard shortcuts'.format(
            self.sel.currentText()))
        if page.modified:
            ok = page.exit()
            if not ok:
                # ook nog de vorige tekst in de combobox selecteren?
                return
        self.pnl.setCurrentIndex(indx)
        if indx == 1:
            menus, funcs = TC_MENU, TC_MENU_FUNC
        else:
            menus, funcs = DFLT_MENU, DFLT_MENU_FUNC
        self.parent.setup_menu(menus, funcs)
        self.parent.page = self.pnl.currentWidget()


class MainFrame(MainWindow):
    """Hoofdscherm van de applicatie"""
    def __init__(self, args):

        wid = 860 if LIN else 688
        hig = 594
        gui.QMainWindow.__init__(self)
        self.title = 'Hotkeys'
        self.setWindowTitle("tcmdrkeys")
        self.resize(wid, hig)
        self.sb = self.statusBar()
        self.sb.showMessage('Welcome to HotKeys!')

        self.menu_bar = self.menuBar()
        self.readcaptions('english.lng') # set up defaults
        pnl = gui.QWidget(self)
        self.book = ChoiceBook(pnl) # , size= (600, 700))
        sizer_v = gui.QVBoxLayout()
        sizer_h = gui.QHBoxLayout()
        sizer_h.addWidget(self.book)
        sizer_v.addLayout(sizer_h)
        self.b_exit = gui.QPushButton(self.captions[C_EXIT], pnl)
        self.b_exit.clicked.connect(self.exit)
        sizer_h = gui.QHBoxLayout()
        sizer_h.addStretch()
        sizer_h.addWidget(self.b_exit)
        sizer_h.addStretch()
        sizer_v.addLayout(sizer_h)
        pnl.setLayout(sizer_v)

        self.setCentralWidget(pnl)
        self.page = self.book.pnl.currentWidget()
        self.book.on_page_changed(0)
        self.setcaptions()
        self.show()


def main(args=None):
    app = gui.QApplication(sys.argv)
    ## redirect=True, filename="hotkeys.log")
    ## print '----------'
    frame = MainFrame(args)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main(sys.argv[1:])
