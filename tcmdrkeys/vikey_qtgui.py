# -*- coding: UTF-8 -*-

from __future__ import print_function
import sys, os
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import vikeys
## import datetime

INI = "vikey_config.py"
from hotkeys_shared import * # constants
C_MENU = VI_MENU

class VIPanel(gui.QWidget):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    voornamelijk nodig om de specifieke verwerkingen met betrekking tot de lijst
    bij elkaar en apart van de rest te houden
    definieert feitelijk een "custom widget"
    """
    def __init__(self, parent):
        self.parent = parent
        self.ini = vikeys.VIKSettings(INI) # 1 pad + language instelling
        self.readkeys()
        self.readcaptions()
        gui.QFrame.__init__(self, parent)

        titles, widths = [], []
        for key, width in ((C_KEY,120),
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

    def doelayout(self):
        sizer0 = gui.QVBoxLayout()
        sizer1 = gui.QHBoxLayout()
        sizer1.addWidget(self.p0list)
        sizer0.addLayout(sizer1)
        self.setLayout(sizer0)

    def readkeys(self):
        self.data = vikeys.readkeys(self.ini.pad)

    def savekeys(self):
        vikeys.savekeys(self.ini.pad, self.data)
        self.modified = False
        self.setWindowTitle(self.captions["000"])

    def readcaptions(self):
        self.captions = {}
        with open(os.path.join(HERE, self.ini.lang)) as f_in:
            for x in f_in:
                if x[0] == '#' or x.strip() == "":
                    continue
                key, value = x.strip().split(None,1)
                self.captions[key] = value
        self.captions['000'] = 'VI hotkeys'
        return self.captions

    def setcaptions(self):
        title = self.captions["000"]
        if self.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)
        self.populate_list()

    def on_keypress(self, evt): #TODO - dit mag met actions
        """callback bij gebruik van een toets(encombinatie)
        """
        keycode = evt.GetKeyCode()
        togo = keycode - 48
        if evt.GetModifiers() == gui.QMOD_ALT: # evt.AltDown()
            if keycode == gui.QWXK_LEFT or keycode == gui.QWXK_NUMPAD_LEFT: #  keycode == 314
                pass
            elif keycode == gui.QWXK_RIGHT or keycode == gui.QWXK_NUMPAD_RIGHT: #  keycode == 316
                pass
            ## elif togo >= 0 and togo <= self.parent.pages: # Alt-0 t/m Alt-6
                ## pass
            elif keycode == 83: # Alt-S
                pass
            elif keycode == 70: # Alt-F
                pass
            elif keycode == 71: # Alt-G
                pass
        elif evt.GetModifiers() == gui.QMOD_CONTROL: # evt.ControlDown()
            if keycode == 81: # Ctrl-Q
                pass
            elif keycode == 80: # Ctrl-P
                self.keyprint(evt)
            elif keycode == 79: # Ctrl-O
                pass
            elif keycode == 78: # Ctrl-N
                pass
            elif keycode == 70: # Ctrl-H
                pass
            elif keycode == 90: # Ctrl-Z
                pass
        elif keycode == gui.QWXK_RETURN or keycode == gui.QWXK_NUMPAD_ENTER:# 13 or 372: # Enter
            pass
        #~ else:
            #~ evt.Skip()
        evt.Skip()

    def on_text_event(self,evt): #TODO
        """callback op het wijzigen van de tekst

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        #~ print "self.init is", self.init
        if not self.init:
            #~ print "ok, enabling buttons"
            self.enableButtons()

    def on_combobox_event(self,evt): #TODO
        """callback op het gebruik van een combobox

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        self.enableButtons()

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
            new_item.setText(0, data[0])
            new_item.setData(0, core.Qt.UserRole, key) # data[0])
            new_item.setText(1, data[1])
            new_item.setText(2, data[2])
            self.p0list.addTopLevelItem(new_item)

    def on_item_selected(self, event): #TODO
        """callback op het selecteren van een item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "Itemselected",seli,self.data[seli]
        self.vuldetails(seli)
        event.Skip()

    def on_item_deselected(self, event): #TODO
        """callback op het niet meer geselecteerd zijn van een item

        er wordt gevraagd of de key definitie moet worden bijgewerkt"""
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "ItemDeselected",seli,self.data[seli]
        if self.defchanged:
            self.defchanged = False
            dlg = gui.QMessageDialog(self,
                self.parent.captions["020"],
                self.parent.captions["000"],
                gui.QYES_NO | gui.QNO_DEFAULT | gui.QICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()
            if h == gui.QID_YES:
                ## print "OK gekozen"
                self.aanpassen()

    def on_item_activated(self, event): #TODO
        """callback op het activeren van een item (onderdeel van het selecteren)
        """
        self.currentItem = event.m_itemIndex

    def keyprint(self,evt): #TODO
        pass


class MainWindow(gui.QMainWindow):
    """Hoofdscherm van de applicatie"""
    def __init__(self): # , args):

        wid = 800 if LIN else 688
        hig = 594
        gui.QMainWindow.__init__(self)
        ## self.setWindowTitle("VI keys")
        self.resize(wid, hig)
        ## self.sb = self.statusBar() # A Statusbar in the bottom of the window
        self.page = VIPanel(self)
        self.setCentralWidget(self.page)
        self.captions = self.page.captions
        self.setWindowTitle(self.captions["000"])
        #~ self.SetIcon(gui.QIcon("task.ico",gui.QBITMAP_TYPE_ICO))
        ## self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))

    # --- schermen opbouwen: layout -----------------------------------------------------------------------------------------
        self.page.doelayout()
        self.show()
        if len(self.page.data) == 0:
            gui.QMessageBox.information(self, self.captions['042'],
                self.captions["000"])

def main():
    app = gui.QApplication(sys.argv) # redirect=True,filename="vikey_gui.log")
    frame = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    ## h = Tcksettings()
    ## h.set('paden',['ergens',])
    ## print h.__dict__
    main()
