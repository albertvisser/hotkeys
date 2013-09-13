# -*- coding: UTF-8 -*-
"""Hotkeys plugin voor Total Commander
"""
from __future__ import print_function
import sys
import os
import string
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core

from .hotkeys_shared import * # constants
from tcmdrkeys import tcmdrkys as keys

# alleen de TC-specifieke menufuncties, de rest wordt uit hotkeys_shared geïmporteerd
def m_read(self):
    """(menu) callback voor het lezen van de hotkeys

    vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
    zet de gelezen keys daarna ook in de gui
    """
    doit = True
    if not self.page.modified:
        doit = False
        h = show_message(self, '041')
        if h == gui.QMessageBox.Yes:
            doit = True
    if doit:
        self.page.readkeys()
        self.page.populate_list()

def m_save(self):
    """(menu) callback voor het terugschrijven van de hotkeys

    vraagt eerst of het ok is om de hotkeys weg te schrijven
    vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
    """
    if not self.page.modified:
        h = show_message(self, '041')
        if h != gui.QMessageBox.Yes:
            return
    self.page.savekeys()
    if self.page.ini.restart:
        h = show_message(self, '026')
        if h == gui.QMessageBox.Yes:
            os.system(self.page.ini.restart)
    else:
        gui.QMessageBox.information(self, self.captions['000'], self.captions['037'])

def m_loc(self):
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    if self.page.modified:
        h = show_message(self, '025')
        if h == gui.QMessageBox.Yes:
            self.page.savekeys()
        elif h == gui.QMessageBox.Cancel:
            return
    paths = self.page.ini.paden
    if self.page.ini.restart:
        paths.append(self.page.ini.restart)
    else:
        paths.append('')
    captions = [self.captions[x] for x in (
        '028','029','030','031','032','033','039','038','040'
        )]
    ok = FilesDialog(self, self.captions["000"], paths, captions).exec_()
    if ok == gui.QDialog.Accepted:
        paden, restarter = self.paden[:-1], self.paden[-1]
        self.page.ini.set("paden", paden)

TC_MENU = (
    (M_APP,(M_READ, M_SAVE, M_USER, -1 , M_EXIT)),
    (M_SETT,(M_LOC,M_LANG)),
    (M_HELP,(M_ABOUT,))
    )

# dispatch table for  menu callbacks
TC_MENU_FUNC = {
    M_READ: m_read,
    M_SAVE: m_save,
    M_USER: m_user,
    M_EXIT: m_exit,
    M_LOC: m_loc,
    M_LANG: m_lang,
    M_ABOUT: m_about,
}


class MyPanel(HotkeyPanel):

    def __init__(self, parent):
        """setup specific for this plugin, column definitions, generic setup
        """
        self._origdata = ["", False, False, False, False, ""]
        self._newdata = self._origdata[:]
        self.mag_weg = True
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []

        self._keys = keys
        coldata = (
            (C_KEY, 100, 0, False),
            (C_MOD, 90, 1, False),
            (C_SRT, 80, 2, True),
            (C_CMD, 160, 3, False),
            (C_OMS, 452, 4, False)
            )
        HotkeyPanel.__init__(self, parent, coldata, ini="tckey_config.py",
            title='TC Hotkeys') #, menus=, funcs=)

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        self._box = box = gui.QFrame(self)
        box.setFrameShape(gui.QFrame.StyledPanel)
        box.setMaximumHeight(90)
        self.txt_key = gui.QLabel(self.captions[C_KTXT] + " ", box)
        self.keylist = [x for x in string.ascii_uppercase] + \
            [x for x in string.digits] + ["F" + str(i) for i in range(1,13)] + \
            [self.captions[str(x)] for x in range(100,121)] + \
            ['PAUSE', 'OEM_.', 'OEM_,', 'OEM_+', 'OEM_-', 'OEM_</>', 'OEM_US`~',
            'OEM_US[{', 'OEM_US]}', 'OEM_US\\|', 'OEM_US;:', "OEM_US'" + '"',
            'OEM_US/?', 'OEM_FR!']
        not_found = []
        for key, value in self.data.items():
            if value[0] not in self.keylist:
                print(value)
                not_found.append(key)
        for key in not_found:
            del self.data[key]
        cb = gui.QComboBox(box)
        cb.addItems(self.keylist)
        cb.currentIndexChanged[str].connect(functools.partial(self.on_combobox, cb))
        self.cmb_key = cb

        for x in (M_CTRL, M_ALT, M_SHFT, M_WIN):
            cb = gui.QCheckBox(self.captions[x].join(("+","  ")), box) #, (65, 60), (150, 20), gui.QNO_BORDER)
            cb.setChecked(False)
            cb.stateChanged.connect(functools.partial(self.on_checkbox, cb))
            if x == M_CTRL:
                self.cb_ctrl = cb
            elif x == M_ALT:
                self.cb_alt = cb
            elif x == M_SHFT:
                self.cb_shift = cb
            elif x == M_WIN:
                self.cb_win = cb

        self.txt_cmd = gui.QLabel(self.captions[C_CTXT] + " ", box)
        self.commandlist = [x for x in self.omsdict.keys()]
        self.commandlist.sort()
        cb = gui.QComboBox(self)
        cb.addItems(self.commandlist)
        cb.currentIndexChanged[str].connect(functools.partial(self.on_combobox, cb))
        self.cmb_commando = cb

        self.b_save = gui.QPushButton(self.captions[C_SAVE], box) ##, (120, 45))
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(self.on_update)
        self.b_del = gui.QPushButton(self.captions[C_DEL], box) #, size= (50,-1)) ##, (120, 45))
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(self.on_delete)

        self.txt_oms = gui.QTextEdit(box)
        self.txt_oms.setMaximumHeight(40)
        self.txt_oms.setReadOnly(True)

    def layout_extra_fields(self):
        """add the extra fileds to the layout
        """
        bsizer = gui.QVBoxLayout()
        sizer1 = gui.QHBoxLayout()
        sizer2 = gui.QHBoxLayout()
        sizer3 = gui.QHBoxLayout()
        sizer3.addWidget(self.txt_key)
        sizer3.addWidget(self.cmb_key)
        sizer2.addLayout(sizer3)
        sizer3 = gui.QHBoxLayout()
        sizer3.addWidget(self.cb_win)
        sizer3.addWidget(self.cb_ctrl)
        sizer3.addWidget(self.cb_alt)
        sizer3.addWidget(self.cb_shift)
        sizer2.addLayout(sizer3)
        sizer1.addLayout(sizer2)
        sizer2 = gui.QHBoxLayout()
        sizer2.addWidget(self.txt_cmd)
        sizer2.addWidget(self.cmb_commando)
        sizer1.addLayout(sizer2)
        sizer1.addWidget(self.b_save)
        sizer1.addWidget(self.b_del)

        bsizer.addLayout(sizer1)
        sizer1 = gui.QHBoxLayout()
        sizer1.addWidget(self.txt_oms)
        bsizer.addLayout(sizer1)
        self._box.setLayout(bsizer)
        self._sizer.addWidget(self._box)

    def captions_extra_fields(self):
        """to be called on changing the language
        """
        self.cb_win.setText(self.captions[M_WIN].join(("+", "  ")))
        self.cb_ctrl.setText(self.captions[M_CTRL].join(("+", "  ")))
        self.cb_alt.setText(self.captions[M_ALT].join(("+", "  ")))
        self.cb_shift.setText(self.captions[M_SHFT].join(("+", "  ")))
        self.b_save.setText(self.captions[C_SAVE])
        self.b_del.setText(self.captions[C_DEL])
        self.txt_key.setText(self.captions[C_KTXT])
        self.txt_cmd.setText(self.captions[C_CTXT])

    def on_item_selected(self, newitem, olditem): # olditem, newitem):
        """callback on selection of an item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        if not newitem: # bv. bij p0list.clear()
            return
        if self._initializing:
            self.vuldetails(newitem)
            return
        print('itemselected called', newitem.text(0))
        if olditem is not None:
            print('old item was', olditem.text(0))
        origkey = self._origdata[0]
        origmods = ''.join([y for x, y in zip((4, 2, 3, 1),
            ('WCAS')) if self._origdata[x]])
        origcmd = self._origdata[5]
        key = self._newdata[0]
        mods = ''.join([y for x, y in zip((4, 2, 3, 1),
            ('WCAS')) if self._newdata[x]])
        cmd = self._newdata[5]
        cursor_moved = True if newitem != olditem and olditem is not None else False
        other_item = key != origkey or mods != origmods
        other_cmd = cmd != origcmd
        any_change = other_item or other_cmd
        gevonden = False
        for number, item in self.data.items():
            if key == item[0] == key and item[1] == mods:
                gevonden = True
                indx = number
                break
        print(cursor_moved, other_item, other_cmd, gevonden)
        doit = False
        if any_change:
            if cursor_moved:
                h = gui.QMessageBox.question(self,
                    self.captions["000"], self.captions["020"],
                    gui.QMessageBox.Yes | gui.QMessageBox.No)
                doit = True if h == gui.QMessageBox.Yes else False
            elif other_item:
                if gevonden:
                    ok = gui.QMessageBox.question(self,
                        self.captions["000"], self.captions["045"],
                        gui.QMessageBox.Yes | gui.QMessageBox.No)
                    doit = True if ok == gui.QMessageBox.Yes else False
                else:
                    doit = True
            else:
                doit = True
        if doit:
            item = self.p0list.currentItem()
            pos = self.p0list.indexOfTopLevelItem(item)
            if gevonden:
                self.data[indx] = (key, mods, 'U', cmd, self.omsdict[cmd])
            else:
                newdata = [x for x in self.data.values()]
                newvalue = (key, mods, 'U', cmd, self.omsdict[cmd])
                newdata.append(newvalue)
                newdata.sort()
                for x, y in enumerate(newdata):
                    if y == newvalue:
                        indx = x
                    self.data[x] = y
            self.modified = True
            self._origdata = [key, False, False, False, False, cmd]
            for mod, indx in zip(('WCAS'),(4, 2, 3, 1)):
                self._origdata[indx] = mod in mods
            self.populate_list(pos)    # refresh
            newitem = self.p0list.topLevelItem(pos)
        self.vuldetails(newitem)

    def readkeys(self):
        self.cmdict, self.omsdict, self.defkeys, self.data = keys.readkeys(self.ini.paden)

    def savekeys(self):
        HotkeyPanel.savekeys(pad=self.ini.tcpad)

    def vuldetails(self, selitem):  # let op: aangepast (gebruik zip)
        if not selitem: # bv. bij p0list.clear()
            return
        seli = selitem.data(0, core.Qt.UserRole)
        if sys.version < '3':
            seli = seli.toPyObject()
        key, mods, soort, cmd, oms = self.data[seli]
        self.b_save.setEnabled(False)
        self.b_del.setEnabled(False)
        if soort == 'U':
            self.b_del.setEnabled(True)
        self._origdata = [key, False, False, False, False, cmd]
        ix = self.keylist.index(key)
        self.cmb_key.setCurrentIndex(ix)
        self.cb_shift.setChecked(False)
        self.cb_ctrl.setChecked(False)
        self.cb_alt.setChecked(False)
        self.cb_win.setChecked(False)
        self.cmb_key.setEditText(key)
        for x, y, z in zip('SCAW',(1, 2, 3, 4), (self.cb_shift, self.cb_ctrl,
                self.cb_alt, self.cb_win)):
            if x in mods:
                self._origdata[y] = True
                z.setChecked(True)
        self._newdata = self._origdata[:]
        ix = self.commandlist.index(cmd)
        self.cmb_commando.setCurrentIndex(ix)
        self.txt_oms.setText(oms)

    def aanpassen(self, delete=False): # TODO
        print('aanpassen called')
        item = self.p0list.currentItem()
        pos = self.p0list.indexOfTopLevelItem(item)
        if delete:
            indx = item.data(0, core.Qt.UserRole)
            if sys.version < '3':
                indx = int(indx.toPyObject())
            if self.data[indx][1] == "S": # can't delete standard key
                gui.QMessageBox.information(self, self.captions["000"],
                    self.captions['024'])
                return
            else:
                if self.data[indx][0] in self.defkeys: # restore standard if any
                    cmd = self.defkeys[self.data[indx][0]]
                    if cmd in self.omsdict:
                        oms = self.omsdict[cmd]
                    else:
                        oms = cmd
                        cmd = ""
                    self.data[indx] = (key, 'S', cmd, oms)
                else:
                    del self.data[indx]
                    ## pos -= 1
            self.b_save.setEnabled(False)
            self.b_del.setEnabled(False)
            self.modified = True
            self.parent.setWindowTitle(' '.join((self.captions["000"],
                self.captions['017'])))
            print('item deleted, pos is', pos)
            self.populate_list(pos)    # refresh
        else:
            self.on_item_selected(item, item) # , from_update=True)


    def on_combobox(self, cb, text):
        """callback op het gebruik van een combobox

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        text = str(text)
        ## print('on combobox:', text)
        ## print(self._origdata)
        self.defchanged = False
        if cb == self.cmb_key:
            if text != self._origdata[0]:
                self._newdata[0] = text
                self.defchanged = True
                self.b_save.setEnabled(True)
            elif str(self.cmb_commando.currentText()) == self._origdata[5]:
                self.b_save.setEnabled(False)
        elif cb == self.cmb_commando:
            if text != self._origdata[5]:
                self._newdata[5] = text
                self.defchanged = True
                try:
                    self.txt_oms.setText(self.omsdict[text])
                except KeyError:
                    self.txt_oms.setText('(Geen omschrijving beschikbaar)')
                self.b_save.setEnabled(True)
            elif str(self.cmb_key.currentText()) == self._origdata[0]:
                self.b_save.setEnabled(False)
        ## print(self._origdata)
        ## print(self._newdata)

    def on_checkbox(self, cb, state):
        state = bool(state)
        for win, indx in zip((self.cb_shift, self.cb_ctrl, self.cb_alt, self.cb_win),
                range(1,5)):
            if cb == win and state != self._origdata[indx]:
                self._newdata[indx] = state
                self.defchanged = True
                self.b_save.setEnabled(True)
        else:
            states = [bool(self.cb_shift.isChecked()), bool(self.cb_ctrl.isChecked()),
                bool(self.cb_alt.isChecked()), bool(self.cb_win.isChecked())]
            if states == self._origdata[1:5]:
                self.defchanged = False
                self.b_save.setEnabled(False)
        ## print('on checkbox:', indx, state)
        ## print(self._origdata)
        ## print(self._newdata)

    def on_update(self):
        self.aanpassen()
        self.p0list.setFocus()

    def on_delete(self):
        self.aanpassen(delete=True)
        self.p0list.setFocus()


def main():
    app = gui.QApplication(sys.argv)
    frame = MainWindow(menus=TC_MENU, funcs=TC_MENU_FUNC)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
