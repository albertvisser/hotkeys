# -*- coding: UTF-8 -*-

from __future__ import print_function
import sys, os
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
from tcmdrkeys import opkeys
## import datetime
INI = "opkey_config.py"
from .hotkeys_shared import * # constants

class OperaPanel(HotkeyPanel):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    definieert feitelijk een "custom widget"
    """
    def __init__(self, parent):

        self.parent = parent.parent()
        HotkeyPanel.__init__(self, parent)
        self.captions = self.parent.captions
        self.ini = opkeys.OpKSettings(INI) # 1 pad + language instelling
        self.readkeys()
        self.modified = False

        titles, widths = [], []
        for key, width in ((C_KEY,120),
                ('047', 120),
                ('048', 120),
                ('049', 120),
                ## (C_MOD,70),
                (C_SRT,120),
                ## (C_CMD,160),
                (C_OMS,292)):
            titles.append(self.captions[key])
            widths.append(width)

        self.p0list = gui.QTreeWidget(self)
        self.p0list.setSortingEnabled(True)
        self.p0list.setHeaderLabels(titles)
        self.p0list.setAlternatingRowColors(True)
        ## self.p0list.currentItemChanged.connect(self.on_item_selected) # 2 params
        self.p0hdr = self.p0list.header()
        self.p0hdr.setClickable(True)
        for indx, wid in enumerate(widths):
            self.p0hdr.resizeSection(indx, wid)
        self.p0hdr.setStretchLastSection(True)
        self.populate_list()
        ## self.p0list.itemSelected.connect(self.on_item_selected)
        ## self.p0list.itemDeselected.connect(self.on_item_deselected)
        ## self.p0list.itemActivated.connect(self.on_item_activated)
        ## self.p0list.keyReleased.connect((self.on_keypress)

        sizer0 = gui.QVBoxLayout()
        sizer1 = gui.QHBoxLayout()
        sizer1.addWidget(self.p0list)
        sizer0.addLayout(sizer1)
        self.setLayout(sizer0)

    def readkeys(self):
        self.data = opkeys.readkeys(self.ini.csv)

    def savekeys(self):
        opkeys.savekeys(self.ini.csv, self.data)
        self.modified = False
        self.setWindowTitle(self.captions["000"])

    def setcaptions(self):
        title = self.captions["000"]
        if self.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)
        self.populate_list()

    def populate_list(self):
        """vullen van de list control
        """
        self.p0list.clear()
        ## self.p0list.SetMinSize((440,high))
        items = self.data.items()
        if items is None or len(items) == 0:
            return

        for key, data in items:
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, data[3])
            new_item.setData(0, core.Qt.UserRole, key) # data[0])
            new_item.setText(1, data[0])
            new_item.setText(2, data[1])
            new_item.setText(3, data[2])
            soort = C_DFLT if data[4] == "S" else C_RDEF
            new_item.setText(4, self.captions[soort])
            new_item.setText(5, data[5])
            self.p0list.addTopLevelItem(new_item)

    ## def exit(self):
        ## return True # geen vraag opslaan ja/nee

class MainWindow(gui.QMainWindow):
    """Hoofdscherm van de applicatie"""
    def __init__(self): # , args):

        wid = 800 if LIN else 688
        hig = 594
        gui.QMainWindow.__init__(self)
        self.setWindowTitle("Opera keys")
        self.resize(wid, hig)
        self.sb = self.statusBar()
        self.sb.showMessage('Welcome to Opera Keys!')

        #~ self.SetIcon(gui.QIcon("task.ico",gui.QBITMAP_TYPE_ICO))
        ## self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))

        self.menu_bar = self.menuBar()
        self.readcaptions('english.lng')
        self.setup_menu(DFLT_MENU, DFLT_MENU_FUNC)

        pnl = gui.QWidget(self)
        self.page = OperaPanel(pnl)
        sizer_v = gui.QVBoxLayout()
        sizer_h = gui.QHBoxLayout()
        sizer_h.addWidget(self.page)
        sizer_v.addLayout(sizer_h)
        self.b_exit = gui.QPushButton(self.captions[C_EXIT], self)
        self.b_exit.clicked.connect(self.exit)
        sizer_h = gui.QHBoxLayout()
        sizer_h.addStretch()
        sizer_h.addWidget(self.b_exit)
        sizer_h.addStretch()
        sizer_v.addLayout(sizer_h)
        pnl.setLayout(sizer_v)

        self.setCentralWidget(pnl)
        self.setcaptions()
        self.show()
        if len(self.page.data) == 0:
            gui.QMessageBox.information(self, self.captions['042'],
                self.captions["000"])

    def setup_menu(self, menus, funcs):
        self.menu_bar.clear()
        self._menus = menus
        self._menuitems = []
        for title, items in menus:
            menu = self.menu_bar.addMenu(self.captions[title])
            for sel in items:
                if sel == -1:
                    menu.addSeparator()
                else:
                    act = gui.QAction(self.captions[sel], self)
                    act.triggered.connect(functools.partial(self.on_menu, sel))
                    menu.addAction(act)
            self._menuitems.append(menu)
        self._menu_func = funcs

    def on_menu(self, actionid):
        text = self._menu_func[actionid](self)
        if text:
            gui.QMessageBox.information(self, text, self.captions["000"])

    def readcaptions(self, lang):
        self.captions = {}
        with open(os.path.join(HERE, lang)) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value
        self.captions['000'] = 'Opera hotkeys'

    def exit(self,e=None):
        if not self.page.exit():
            return
        self.close()

    def setcaptions(self):
        ## self.captions = self.page.captions
        title = self.captions["000"]
        if self.page.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)
        for indx, menu in enumerate(self._menuitems):
            menu.setTitle(self.captions[self._menus[indx][0]])
            for indx2, action in enumerate(menu.actions()):
                hulp = self._menus[indx][1][indx2]
                if hulp != -1:
                    action.setText(self.captions[hulp])
        self.b_exit.setText(self.captions[C_EXIT])
        self.page.setcaptions()


def main():
    app = gui.QApplication(sys.argv) # redirect=True,filename="vikey_gui.log")
    frame = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    ## h = Tcksettings()
    ## h.set('paden',['ergens',])
    ## print h.__dict__
    main()
