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
import editor.hotkeys_plugins

PLUGINS = editor.hotkeys_plugins.PLUGINS
MENUS = editor.hotkeys_plugins.MENUS

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
        self.find = gui.QComboBox(self)
        self.find.setMinimumContentsLength(20)
        self.find.setEditable(True)
        self.find.editTextChanged.connect(self.on_text_changed)
        self.b_next = gui.QPushButton(self.parent.captions["014"])
        self.b_next.clicked.connect(self.find_next)
        self.b_next.setEnabled(False)
        self.b_prev = gui.QPushButton(self.parent.captions["015"])
        self.b_prev.clicked.connect(self.find_prev)
        self.b_prev.setEnabled(False)
        self.pnl = gui.QStackedWidget(self)
        self.captions = self.parent.captions
        for txt, win in PLUGINS:
            if win is None:
                self.pnl.addWidget(EmptyPanel(self.pnl,
                    self.parent.captions["052"].format(txt)))
            else:
                self.pnl.addWidget(win(self.pnl))
        box = gui.QVBoxLayout()
        vbox = gui.QVBoxLayout()
        hbox = gui.QHBoxLayout()
        hbox.addSpacing(10)
        self.sel_text = gui.QLabel(self.parent.captions["050"], self)
        hbox.addWidget(self.sel_text)
        hbox.addWidget(self.sel)
        hbox.addStretch()
        self.find_text = gui.QLabel(self.parent.captions["051"], self)
        hbox.addWidget(self.find_text)
        hbox.addWidget(self.find)
        hbox.addWidget(self.b_next)
        hbox.addWidget(self.b_prev)
        ## hbox.addStretch()
        hbox.addSpacing(10)
        vbox.addLayout(hbox)
        box.addLayout(vbox)
        hbox = gui.QVBoxLayout()
        hbox.addWidget(self.pnl)
        box.addLayout(hbox)
        self.setLayout(box)

    def on_page_changed(self, indx):
        page = self.pnl.currentWidget() ## self.parent().page
        self.parent.sb.showMessage(self.parent.captions["053"].format(
            self.sel.currentText()))
        if page.modified:
            ok = page.exit()
            if not ok:
                # ook nog de vorige tekst in de combobox selecteren?
                return
        self.pnl.setCurrentIndex(indx)
        menus, funcs = MENUS.get(PLUGINS[indx], (None, None))
        if not menus:
            menus, funcs = DFLT_MENU, DFLT_MENU_FUNC
        self.parent.setup_menu(menus, funcs)
        self.parent.page = self.pnl.currentWidget()
        self.find.setEditText('')

    def on_text_changed(self, text):
        ## if self.find.count() == 0:
            ## self.find.addItem(text)
        ## elif self.text.startswith(self.find.itemText(0)):
            ## self.find.setItemText(0, text)
        ## self.parent.sb.showMessage(text)
        page = self.parent.page # self.pnl.currentWidget()
        col = page.p0list.columnCount() - 1
        self.items_found = page.p0list.findItems(text, core.Qt.MatchContains, col)
        if self.items_found:
            page.p0list.setCurrentItem(self.items_found[0])
            self.founditem = 0
            self.b_next.setEnabled(True)
        else:
            self.parent.sb.showMessage(self.parent.captions["054"].format(
                text))

    def find_next(self):
        self.b_prev.setEnabled(True)
        if self.founditem == len(self.items_found):
            self.parent.sb.showMessage(self.parent.captions["055"])
        else:
            self.founditem += 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])

    def find_prev(self):
        if self.founditem == 0:
            self.parent.sb.showMessage(self.parent.captions["056"])
        else:
            self.founditem -= 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])


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

        self.menu_bar = self.menuBar()
        self.ini = {'filename': CONF}
        with open(self.ini['filename']) as _in:
            for line in _in:
                if line.startswith('LANG'):
                    self.ini['lang'] = line.strip().split('=')[1]
        if 'lang' not in self.ini:
            self.ini['lang'] = 'english.lng'
        self.readcaptions(self.ini['lang']) # set up defaults
        self.sb.showMessage('Welcome to {}!'.format(self.captions["000"]))
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
