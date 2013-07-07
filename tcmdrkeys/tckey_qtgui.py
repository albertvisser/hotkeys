# -*- coding: UTF-8 -*-

from __future__ import print_function
import sys, os
import functools
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
import wx
import wx.lib.filebrowsebutton as filebrowse
import wx.gizmos   as  gizmos
import images
import tcmdrkys
import string
## import datetime

HERE = os.path.abspath(os.path.dirname(__file__))
TTL = "A hotkey editor"
VRS = "1.1.x"
AUTH = "(C) 2008 Albert Visser"
INI = "tckey_config.py"
WIN = True if sys.platform == "win32" else False
LIN = True if sys.platform == 'linux2' else False

# voorziening voor starten op usb-stick onder Windows (drive letters in config aanpassen)
if WIN and __file__ != "tckey_gui.py":
    drive = os.path.splitdrive(os.getcwd())[0] + "\\"
    with open(INI) as f_in:
        lines = f_in.readlines()
    for line in lines:
        if line.startswith('TC_PAD='):
            olddrive = line[7:10]
            break
    if olddrive.upper() != drive.upper():
        bak = INI + ".bak"
        if os.path.exists(bak):
            os.remove(bak)
        os.rename(INI,bak)
        with open(INI,"w") as f_out:
            for line in lines:
                if olddrive.lower() in line:
                    f_out.write(line.replace(olddrive.lower(),drive.upper()))
                elif olddrive.upper() in line:
                    f_out.write(line.replace(olddrive.upper(),drive.upper()))
                else:
                    f_out.write(line)

#--- dit zit ook in hotkeys_shared.py
# constanten voor  captions en dergelijke 9correspondeert met nummers in language files)
C_KEY, C_MOD, C_SRT, C_CMD, C_OMS = '001', '043', '002', '003', '004'
C_DFLT, C_RDEF = '005', '006'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
C_SAVE, C_DEL, C_EXIT, C_KTXT, C_CTXT ='010', '011', '012', '018', '019'
M_APP, M_READ, M_SAVE, M_USER, M_EXIT = '200', '201', '202', '203', '209'
M_SETT, M_LOC, M_LANG, M_HELP, M_ABOUT = '210', '211', '212', '290', '299'
C_MENU = (
    (M_APP,(M_READ, M_SAVE, M_USER, -1 , M_EXIT)),
    (M_SETT,(M_LOC,M_LANG)),
    (M_HELP,(M_ABOUT,))
    )
NOT_IMPLEMENTED = '404'
#----

#--- deze functies zitten ook in hotkeys_qt.py
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
    if not self.modified:
        h = show_message(self, '041')
        if h == gui.QMessageBox.Ok:
            self.readkeys()
            self.page.populate_list()

def m_save(self):
    """(menu) callback voor het terugschrijven van de hotkeys

    vraagt eerst of het ok is om de hotkeys weg te schrijven
    vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
    """
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
        ## gui.QMessageBox.information(self, self.captions['037'], self.captions['000'])
        h = show_message(self, '037')

def m_user(self):
    """(menu) callback voor een nog niet geïmplementeerde actie"""
    return self.captions[NOT_IMPLEMENTED]

def m_exit(self):
    """(menu) callback om het programma direct af te sluiten"""
    self.close()

def m_loc(self): # TODO?
    """(menu) callback voor aanpassen van de bestandslocaties

    vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
    toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
    (met name of de opgegeven paden kloppen)
    """
    if self.page.modified:
        h = show_message(self, '025')
        if h == gui.QMessageBox.Ok:
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
    ## captions = ['Define file locations for:', 'TC','UC','CI','KT','HK']
    ok = FilesDialog(self, self.captions["000"], paths, captions).exec_()
    if ok == gui.QDialog.Accepted:
        paden, restarter = self.paden[:-1], self.paden[-1]
        self.page.ini.set("paden", paden)

def m_lang(self):
    """(menu) callback voor taalkeuze

    past de settings aan en leest het geselecteerde language file
    """
    choices = [x for x in os.listdir(HERE) if os.path.splitext(x)[1] == ".lng"]
    indx = choices.index(self.page.ini.lang) if self.page.ini.lang in choices else 0
    lang, ok = gui.QInputDialog.getItem(self, self.captions["027"],
        self.captions["000"], choices, current=indx, editable=False)
    if ok:
        self.page.ini.set('lang', str(lang))
        self.page.readcaptions()
        self.page.setcaptions()

def m_about(self):
    """(menu) callback voor het tonen van de "about" dialoog
    """
    info = gui.QMessageBox.about(self,  self.captions['000'],
        "\n\n".join((VRS, AUTH)))

# dispatch table for  menu callbacks
MENU_FUNC = {
    M_READ: m_read,
    M_SAVE: m_save,
    M_USER: m_user,
    M_EXIT: m_exit,
    M_LOC: m_loc,
    M_LANG: m_lang,
    M_ABOUT: m_about,
}
#----

class TCPanel(gui.QWidget):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    definieert feitelijk een "custom widget"
    """
    def __init__(self, parent, args=None, can_exit=False): # , top):

        self.can_exit = can_exit
        self.captions = {}
        self.data = []
        self.ini = tcmdrkys.TckSettings(INI)
        if self.ini.paden[0] == '':
            self.ini.lang = 'english.lng'
            ## win = gui.QWidget()
            ## gui.QMessageBox.information(win, 'TC_Hotkeys',
                ## 'Geen settings file ({}) in deze directory'.format(INI))
            ## win.close()
            ## return
        self.readcaptions()
        ## print "start",datetime.datetime.today()
        ## self.parent = parent
        self.modified = False
        self.orig = ["", False, False, False, False, ""]
        self.mag_weg = True
        if args:
            self.fpad = args[0]
            ext = os.path.splitext(self.fpad)[1]
            if ext == "" and not os.path.isdir(self.fpad):
                self.fpad += ".xml"
            elif ext != ".xml":
                self.fpad = ""
        else:
            self.fpad  = ""
        self.dirname,self.filename = os.path.split(self.fpad)
        #~ print self.dirname,self.filename
        self.newfile = self.newitem = False
        self.oldsort = -1
        self.idlist = self.actlist = self.alist = []
        self.readkeys()

        gui.QWidget.__init__(self, parent)
        self.parent = parent
        ## self.top = top

        titles, widths = [], []
        for key, width in ((C_KEY, 70),
                (C_MOD, 90),
                (C_SRT, 80),
                (C_CMD, 160),
                (C_OMS, 452)):
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
        ## self.Bind(gui.QEVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.p0list)
        ## self.Bind(gui.QEVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.p0list)
        ## self.Bind(gui.QEVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.p0list)
        ## self.Bind(gui.QEVT_LIST_COL_CLICK, self.OnColClick, self.p0list)
        ## self.p0list.Bind(gui.QEVT_LEFT_DCLICK, self.OnDoubleClick)
        ## self.p0list.Bind(gui.QEVT_KEY_DOWN, self.OnKeyPress)

        box = gui.QFrame(self)
        box.setFrameShape(gui.QFrame.StyledPanel)
        ## box.setLineWidth(1)
        box.setMaximumHeight(90)
        self.txt_key = gui.QLabel(self.captions[C_KTXT] + " ", box)
        self.keylist = [x for x in string.ascii_uppercase] + \
            [x for x in string.digits] + ["F" + str(i) for i in range(1,13)] + \
            [self.captions[str(x)] for x in xrange(100,118)]
        cb = gui.QComboBox(box)
        cb.addItems(self.keylist)
        ## self.Bind(gui.QEVT_COMBOBOX, self.EvtComboBox, cb)
        ## self.Bind(gui.QEVT_TEXT, self.EvtText, cb)
        ## self.Bind(gui.QEVT_TEXT_ENTER, self.EvtTextEnter, cb)
        self.cmb_key = cb

        for x in (M_CTRL, M_ALT, M_SHFT, M_WIN):
            cb = gui.QCheckBox(self.captions[x].join(("+","  ")), box) #, (65, 60), (150, 20), gui.QNO_BORDER)
            cb.setChecked(False)
            ## self.Bind(gui.QEVT_CHECKBOX, self.EvtCheckBox, cb)
            if x == M_CTRL:
                self.cb_ctrl = cb
            elif x == M_ALT:
                self.cb_alt = cb
            elif x == M_SHFT:
                self.cb_shift = cb
            elif x == M_WIN:
                self.cb_win = cb

        self.txt_cmd = gui.QLabel(self.captions[C_CTXT] + " ", box)
        commandlist = [x for x in self.omsdict.keys()]
        commandlist.sort()
        cb = gui.QComboBox(self)
        cb.addItems(commandlist)
        ## self.Bind(gui.QEVT_COMBOBOX, self.EvtComboBox, cb)
        ## self.Bind(gui.QEVT_TEXT, self.EvtText, cb)
        ## self.Bind(gui.QEVT_TEXT_ENTER, self.EvtTextEnter, cb)
        self.cmb_commando = cb

        self.b_save = gui.QPushButton(self.captions[C_SAVE], box) ##, (120, 45))
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(self.on_click)
        self.b_del = gui.QPushButton(self.captions[C_DEL], box) #, size= (50,-1)) ##, (120, 45))
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(self.on_click)

        self.txt_oms = gui.QTextEdit(box)
        ## self.txt_oms.resize=(125, 36)
        self.txt_oms.setMaximumHeight(40)
        self.txt_oms.setReadOnly(True)

        if can_exit:
            self.b_exit = gui.QPushButton(self.captions[C_EXIT], self)
            self.b_exit.clicked.connect(self.parent.exit)
            ## self.Bind(gui.QEVT_KEY_DOWN, self.OnKeyPress)

    # --- schermen opbouwen: layout -----------------------------------------------------------------------------------------
        sizer0 = gui.QVBoxLayout()
        sizer1 = gui.QHBoxLayout()
        sizer1.addWidget(self.p0list)
        sizer0.addLayout(sizer1)

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
        box.setLayout(bsizer)
        sizer0.addWidget(box)

        if can_exit:
            sizer2 = gui.QHBoxLayout()
            sizer2.addStretch()
            sizer2.addWidget(self.b_exit)
            sizer2.addStretch()
            sizer0.addLayout(sizer2)
        self.setLayout(sizer0)

    def readkeys(self):
        self.cmdict, self.omsdict, self.defkeys, self.data = tcmdrkys.readkeys(
            self.ini.paden)

    def savekeys(self):
        tcmdrkys.savekeys(self.ini.tcpad, self.data)
        self.modified = False
        self.setWindowTitle(self.captions["000"])

    def readcaptions(self):
        for x in file(os.path.join(HERE, self.ini.lang)):
            if x[0] == '#' or x.strip() == "":
                continue
            key,value = x.strip().split(None,1)
            self.captions[key] = value

    def setcaptions(self): # TODO
        if self.can_exit:
            self.parent.setcaptions()
        self.cb_win.setText(self.captions[M_WIN].join(("+", "  ")))
        self.cb_ctrl.setText(self.captions[M_CTRL].join(("+", "  ")))
        self.cb_alt.setText(self.captions[M_ALT].join(("+", "  ")))
        self.cb_shift.setText(self.captions[M_SHFT].join(("+", "  ")))
        self.b_save.setText(self.captions[C_SAVE])
        self.b_del.setText(self.captions[C_DEL])
        self.b_exit.setText(self.captions[C_EXIT])
        self.txt_key.setText(self.captions[C_KTXT])
        self.txt_cmd.setText(self.captions[C_CTXT])
        self.populate_list()

    def vuldetails(self,seli): # TODO
        key, mods, soort, cmd, oms = self.data[seli]
        ## print "details vullen met",key,soort,cmd,oms
        self.bSave.Enable(False)
        if soort == 'U':
            self.bDel.Enable(True)
        self.orig =  [key, False, False, False, False, cmd]
        self.cbShift.SetValue(False)
        self.cbCtrl.SetValue(False)
        self.cbAlt.SetValue(False)
        self.cbWin.SetValue(False)
        self.cmbKey.SetValue(key)
        if 'S' in mods:
        ## for mod in mods:
            ## if mod == "S":
                self.orig[1] = True
                self.cbShift.SetValue(True)
        if 'C' in mods:
            ## elif mod == "C":
                self.orig[2] = True
                self.cbCtrl.SetValue(True)
        if 'A' in mods:
            ## elif mod == "A":
                self.orig[3] = True
                self.cbAlt.SetValue(True)
        if 'W' in mods:
            ## elif mod == "W":
                self.orig[4] = True
                self.cbWin.SetValue(True)
        self.cmbCommando.SetValue(cmd)
        self.txtOms.SetValue(oms)

    def aanpassen(self, delete=False): # TODO
        oktocontinue = True
        origkey = self.orig[0]
        key = self.cmbKey.GetValue()
        if key not in self.keylist:
            if key.upper() in self.keylist:
                key = key.upper()
                self.cmbKey.SetValue(key)
            else:
                oktocontinue = False
        origmods = ''
        if self.orig[4]:
            origmods += 'W'
        if self.orig[2]:
            origmods += 'C'
        if self.orig[3]:
            origmods += 'A'
        if self.orig[1]:
            origmods += 'S'
        mods = ""
        if self.cbWin.GetValue():
            mods += "W"
        if self.cbCtrl.GetValue():
            mods += "C"
        if self.cbAlt.GetValue():
            mods += "A"
        if self.cbShift.GetValue():
            mods += "S"
        ## if mods != "":
            ## key = " + ".join((key,mods))
        origcmd = self.orig[5]
        cmd = self.cmbCommando.GetValue()
        if cmd not in self.omsdict.keys():
            oktocontinue = False
        if not oktocontinue:
            h = self.captions['021'] if delete else self.captions['022']
            dlg = gui.QMessageDialog(self, h, self.captions["000"],
                gui.QOK | gui.QICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()
            return
        gevonden = False
        print(origkey, ';', origmods, ';', key, ';', mods)
        for number, value in self.data.iteritems():
            ## print number, value
            if value[0] == key and value[1] == mods:
                gevonden = True
                indx = number
                break
        if gevonden:
            if key != origkey or mods != origmods:
                dlg = gui.QMessageDialog(self, self.captions["045"],
                    self.captions["000"],
                    gui.QYES_NO | gui.QNO_DEFAULT |  gui.QICON_INFORMATION
                    )
                h = dlg.ShowModal()
                dlg.Destroy()
                if h == gui.QID_NO:
                    oktocontinue = False
        if not delete:
            if gevonden:
                if oktocontinue:
                    self.data[indx] = (key, mods, 'U', cmd, self.omsdict[cmd])
            else:
                newdata = self.data.values()
                newvalue = (key, mods, 'U', cmd, self.omsdict[cmd])
                newdata.append(newvalue)
                newdata.sort()
                for x, y in enumerate(newdata):
                    if y == newvalue:
                        indx = x
                    self.data[x] = y
        else:
            if not gevonden:
                dlg = gui.QMessageDialog(self, self.captions['023'],
                    self.captions["000"],
                    gui.QOK | gui.QICON_INFORMATION
                    )
                h = dlg.ShowModal()
                dlg.Destroy()
                oktocontinue = False
            elif self.data[indx][1] == "S":
                dlg = gui.QMessageDialog(self, self.captions['024'],
                    self.captions["000"],
                    gui.QOK | gui.QICON_INFORMATION
                    )
                h = dlg.ShowModal()
                dlg.Destroy()
                oktocontinue = False
            else:
                # kijk of er een standaard definitie bij de toets hoort, zo ja deze terugzetten
                if self.data[indx][0] in self.defkeys:
                    cmd = self.defkeys[self.data[indx][0]]
                    if cmd in self.omsdict:
                        oms = self.omsdict[cmd]
                    else:
                        oms = cmd
                        cmd = ""
                    self.data[indx] = (key, 'S', cmd, oms)
                else:
                    del self.data[indx]
                    indx -= 1
        if oktocontinue:
            self.page.PopulateList()
            self.modified = True
            self.SetTitle(self.captions["000"] + ' ' + self.captions['017'])
            self.bSave.Enable(False)
            self.bDel.Enable(False)
            self.page.p0list.Select(indx)

    def onKeyPress(self, evt): # TODO - dit mag met actions
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

    def on_text_event(self,evt): # TODO
        """callback op het wijzigen van de tekst

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        #~ print "self.init is", self.init
        if not self.init:
            #~ print "ok, enabling buttons"
            self.enableButtons()
    ## def EvtText(self,evt): # TODO
        self.defchanged = False
        cb = evt.GetEventObject()
        ## print "EvtText on",cb
        h = evt.GetString()
        if cb == self.cmbKey:
            ## print "h:",h
            j = self.cmbCommando.GetValue()
            ## print "j:",j
            if h.strip() == "" or j.strip() == "":
                self.bSave.Enable(False)
                self.bDel.Enable(False)
            elif h != self.orig[0]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)
        elif cb == self.cmbCommando:
            j = self.cmbKey.GetValue()
            ## print "h:",h
            ## print "j:",j
            if h.strip() == "" or j.strip() == "":
                self.bSave.Enable(False)
                self.bDel.Enable(False)
            elif h != self.orig[5]:
                self.defchanged = True
                try:
                    self.txtOms.SetValue(self.omsdict[h])
                except KeyError:
                    print("Key bestaat niet in omsdict:",h)
                    return
                self.bSave.Enable(True)
                self.bDel.Enable(True)

    ## def EvtTextEnter(self,evt): # TODO
        ## cb = evt.GetEventObject()
        ## print "EvtTextEnter on",cb

    def on_combobox_event(self,evt): # TODO
        """callback op het gebruik van een combobox

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        self.enable_buttons()

    def populate_list(self): # TODO
        """vullen van de list control
        """
        self.p0list.clear()
        items = self.data.items()
        if items is None or len(items) == 0:
            return

        for key, data in items:
            new_item = gui.QTreeWidgetItem()
            new_item.setText(0, data[0])
            new_item.setData(0, core.Qt.UserRole, key) # data[0])
            new_item.setText(1, data[1])
            soort = C_DFLT if data[2] == "S" else C_RDEF
            new_item.setText(2, self.captions[soort])
            new_item.setText(3, data[3])
            new_item.setText(4, data[4])
            self.p0list.addTopLevelItem(new_item)

    def after_sort(self): # TODO
        """ na het sorteren moeten de regels weer om en om gekleurd worden"""
        kleur = False
        for key in range(len(self.data.items)):
            if kleur:
                #~ self.p0list.SetItemBackgroundColour(key,gui.QSystemSettings.GetColour(gui.QSYS_COLOUR_MENU))
            #~ else:
                self.p0list.SetItemBackgroundColour(key,gui.QSystemSettings.GetColour(gui.QSYS_COLOUR_INFOBK))
            kleur = not kleur

    def on_item_selected(self, event): # TODO
        """callback op het selecteren van een item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "Itemselected",seli,self.top.data[seli]
        self.top.vuldetails(seli)
        event.Skip()

    def on_item_deselected(self, event): # TODO
        """callback op het niet meer geselecteerd zijn van een item

        er wordt gevraagd of de key definitie moet worden bijgewerkt"""
        seli = self.p0list.GetItemData(event.m_itemIndex)
        ## print "ItemDeselected",seli,self.top.data[seli]
        if self.top.defchanged:
            self.top.defchanged = False
            dlg = gui.QMessageDialog(self,
                self.top.captions["020"],
                self.top.captions["000"],
                gui.QYES_NO | gui.QNO_DEFAULT | gui.QICON_INFORMATION
                )
            h = dlg.ShowModal()
            dlg.Destroy()
            if h == gui.QID_YES:
                ## print "OK gekozen"
                self.top.aanpassen()

    def on_item_activated(self, event): # TODO
        """callback op het activeren van een item (onderdeel van het selecteren)
        """
        self.currentItem = event.m_itemIndex

    def on_column_click(self, event): # TODO
        """callback op het klikken op een kolomtitel
        """
        ## print "OnColClick: %d\n" % event.GetColumn()
        ## self.parent.sorter = self.GetColumnSorter()
        event.Skip()

    def on_doubleclick(self, event): # TODO
        """callback op dubbelklikken op een kolomtitel
        """
        pass
        # self.log.WriteText("OnDoubleClick item %s\n" % self.p0list.GetItemText(self.currentItem))
        event.Skip()


    def keyprint(self,evt): # TODO
        pass

    def on_checkbox_event(self,evt): # TODO
        cb = evt.GetEventObject()
        if cb == self.cbShift:
            if cb.GetValue() != self.orig[1]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)
        elif cb == self.cbCtrl:
            if cb.GetValue() != self.orig[2]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)
        elif cb == self.cbAlt:
            if cb.GetValue() != self.orig[3]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)
        elif cb == self.cbWin:
            if cb.GetValue() != self.orig[4]:
                self.defchanged = True
                self.bSave.Enable(True)
                self.bDel.Enable(True)

    def on_click(self,evt): # TODO
        b = evt.GetEventObject()
        key = self.cmbKey.GetValue()
        cmd = self.cmbCommando.GetValue()
        if b == self.bSave:
            ## print "keydef opslaan gekozen",key,cmd
            self.aanpassen()
        elif b == self.bDel:
            ## print "keydef verwijderen gekozen",key,cmd
            self.aanpassen(delete=True)

    def OnSetFocus(self,evt): # TODO
        pass

    def OnKillFocus(self,evt): # TODO
        pass


class FileBrowseButton(gui.QWidget):
    def __init__(self, parent, getdirectory=False):
        self.startdir = self.caption = ''
        self.getdir = getdirectory
        gui.QWidget.__init__(self, parent)
        vbox = gui.QVBoxLayout()
        box = gui.QHBoxLayout()
        self.label = gui.QLabel('Enter a {}:'.format('directory' if self.getdir
            else 'file'), self)
        box.addWidget(self.label)
        box.addStretch()
        self.input = gui.QLineEdit(self)
        self.input.setMinimumWidth(200)
        ## inp.setText(strt)
        box.addWidget(self.input)
        self.button = gui.QPushButton('Select', self, clicked=self.browse)
        box.addWidget(self.button)
        vbox.addLayout(box)
        self.setLayout(vbox)

    def browse(self):
        caption = self.caption or 'Browse {}'.format('directories' if self.getdir
            else 'files')
        startdir = str(self.input.text()) or os.getcwd()
        if self.getdir:
            path = gui.QFileDialog.getExistingDirectory(self, caption, startdir)
        else:
            path = gui.QFileDialog.getOpenFileName(self, caption, startdir)
        if path:
            self.input.setText(path)

class FilesDialog(gui.QDialog):
    """dialoog met meerdere FileBrowseButtons

    voor het instellen van de bestandslocaties
    """
    def __init__(self, parent, title, locations, captions): # TODO
        self.parent = parent
        self.locations = locations
        self.captions = captions
        ## print locations
        gui.QDialog.__init__(self, parent)
        self.resize=(350, 200)

        sizer = gui.QVBoxLayout()

        text = captions.pop(0)
        label = gui.QLabel(text, self)
        sizer.addWidget(label)

        buttons = []
        ## callbacks = (self.bTCCallback,self.bUCCallback,
            ## self.bCICallback,self.bKTCallback,self.bHKCallback)
        rstrcap2 = captions.pop()
        rstrcap = captions.pop()
        dircap = captions.pop()

        rstrloc = locations.pop()
        for i, x in enumerate(captions):
            if i < len(locations):
                dir = locations[i]
                strt = dir
            else:
                dir = locations[0]
                strt = ""
            ## dir = os.path.split(dir)[0]
            ## print i,dir

            fbb = FileBrowseButton(self, getdirectory=True)
            fbb.label.setText(x)
            fbb.caption = dircap % x
            fbb.input.setText(strt)
            sizer.addWidget(fbb)
            buttons.append(fbb)
        self.bTC,self.bUC,self.bCI,self.bKT,self.bHK = buttons

        if rstrloc:
            dir, naam = os.path.split(rstrloc)
        else:
            dir, naam = locations[0],''
        self.bRST = FileBrowseButton(self)
        self.bRST.label.setText(rstrcap)
        self.bRST.input.setText(naam)
        self.bRST.caption = rstrcap2
        sizer.addWidget(self.bRST)

        ## line = gui.QStaticLine(self, -1, size=(20,-1), style=gui.QLI_HORIZONTAL)
        ## sizer.Add(line, 0, gui.QGROW|gui.QALIGN_CENTER_VERTICAL|gui.QRIGHT|gui.QTOP, 5)

        button_box = gui.QDialogButtonBox(gui.QDialogButtonBox.Ok |
            gui.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        ## button_box.rejected.connect(button_box.reject)
        sizer.addWidget(button_box)
        self.setLayout(sizer)
        ## btnsizer = gui.QStdDialogButtonSizer()
        ## btn = gui.QButton(self, gui.QID_OK)
        ## btn.SetDefault()
        ## btnsizer.AddButton(btn)
        ## btn = gui.QButton(self, gui.QID_CANCEL)
        ## btnsizer.AddButton(btn)
        ## btnsizer.Realize()
        ## sizer.Add(btnsizer, 0, gui.QALIGN_CENTER|gui.QALL, 2)
        ## self.SetSizer(sizer)
        ## sizer.Fit(self)

    def accept(self):
        paden = [
            str(self.bTC.input.text()),
            str(self.bUC.input.text()),
            str(self.bCI.input.text()),
            str(self.bKT.input.text()),
            str(self.bHK.input.text()),
            str(self.bRST.input.text())
            ]
        fout = ''
        for i, pad in enumerate(paden):
            if pad != "":
                if i == 5:
                    if not os.path.exists(pad):
                        fout = self.parent.captions['036'] % naam
                else:
                    naam = self.captions[i]
                    if naam == 'Hotkeys.hky':
                        naam = 'tc default hotkeys.ohky'
                    if not os.path.exists(os.path.join(pad,naam)):
                        fout = self.parent.captions['035'] % naam
        if fout:
            gui.MessageBox.information(self, self.parent.captions["000"], fout)
            return
        self.parent.paden = paden
        return gui.QDialog.Accepted

    ## def bTCCallback(self, evt):
        ## print "It's the FileBrowseButton for wincmd.ini"
        ## # het zou mooi wezen als deze waarde bij wijzigen default gemaakt wordt voor de andere
        ## # maar ik denk niet dat dat kan zonder ze weg te gooien en opnieuw te maken

    ## def bUCCallback(self, evt):
        ## print "It's the FileBrowseButton for usercmd.ini", evt.GetString()

    ## def bCICallback(self, evt):
        ## print "It's the FileBrowseButton for totalcmd.inc", evt.GetString()

    ## def bKTCallback(self, evt):
        ## print "It's the FileBrowseButton for keyboard.txt", evt.GetString()

    ## def bHKCallback(self, evt):
        ## print "It's the FileBrowseButton for hotkeys.hky", evt.GetString()

class MainWindow(gui.QMainWindow):
    """Hoofdscherm van de applicatie"""
    def __init__(self, args):

        wid = 860 if LIN else 688
        gui.QMainWindow.__init__(self)
        self.setWindowTitle("tcmdrkeys")
        self.resize(wid, 594)
        self.sb = self.statusBar()

    # --- schermen opbouwen: controls plaatsen -----------------------------------------------------------------------------------------
        #~ self.SetIcon(gui.QIcon("task.ico",gui.QBITMAP_TYPE_ICO))
        ## self.SetIcon(images.gettaskIcon())
        #~ self.SetMinSize((476, 560))

        self.page = TCPanel(self, args, can_exit=True)
        self.setCentralWidget(self.page)
        self.captions = self.page.captions
        self.setWindowTitle(self.captions["000"])

        self.menu_bar = self.menuBar()
        self.menuitems = []
        for title, items in C_MENU:
            menu = self.menu_bar.addMenu(self.captions[title])
            self.menuitems.append(menu)
            for sel in items:
                if sel == -1:
                    menu.addSeparator()
                else:
                    act = gui.QAction(self.captions[sel], self)
                    act.triggered.connect(functools.partial(self.on_menu, sel))
                    menu.addAction(act)

        ## print "na layouten scherm",datetime.datetime.today()
        self.show()
        if len(self.page.data) == 0:
            dlg = gui.QMessageBox.information(self, self.captions["000"],
                self.captions['042'])

    def on_menu(self, id_):
        text = MENU_FUNC[id_](self)
        if text:
            dlg = gui.QMessageBox.information(self, self.captions["000"], text)

    def setcaptions(self):
        ## self.captions = self.page.captions
        title = self.captions["000"]
        if self.page.modified:
            title += ' ' + self.captions["017"]
        self.setWindowTitle(title)
        for indx, menu in enumerate(self.menuitems):
            menu.setTitle(self.captions[C_MENU[indx][0]])
            ## hulp = [x for x in C_MENU[indx][1] if x != -1]
            ## print(hulp)
            for indx2, action in enumerate(menu.actions()):
                ## action.setText(self.captions[hulp[indx2]])
                hulp = C_MENU[indx][1][indx2]
                if hulp != -1:
                    action.setText(self.captions[hulp])

    def exit(self,e=None): # TODO
        if self.page.modified:
            ok = gui.QMessageDialog.information(self, self.captions["000"],
                self.captions['025'],
                gui.QYES_NO | gui.QCANCEL | gui.QNO_DEFAULT | gui.QICON_INFORMATION
                )
            if h == gui.QID_YES:
                self.page.savekeys()
            elif h == gui.QID_CANCEL:
                return
        self.close()

    def afdrukken(self): # TODO
        self.css = ""
        if self.css != "":
            self.css = "".join(("<style>",self.css,"</style>"))
        self.text.insert(0,"".join(("<html><head><title>titel</title>",self.css,"</head><body>")))
        self.text.append("</body></html>")
        self.printer.Print("".join(self.text),self.hdr)
        return
        # de moelijke manier
        data = gui.QPrintDialogData()
        data.EnableSelection(False)
        data.EnablePrintToFile(True)
        data.EnablePageNumbers(False)
        data.SetAllPages(True)
        dlg = gui.QPrintDialog(self, data)
        if dlg.ShowModal() == gui.QID_OK:
            pdd = dlg.GetPrintDialogData()
            prt = wxPrinter(pdd)
            pda = Prtdata(self.textcanvas)
            if not prt.Print(self,prtdata,False):
                MessageBox("Unable to print the document.")
            prt.Destroy()
        dlg.Destroy()

def main(args=None):
    app = gui.QApplication(sys.argv)
    #redirect=True, filename="tckey.log")
    frame = MainWindow(args)
    sys.exit(app.exec_())

if __name__ == '__main__':
    ## h = Tcksettings()
    ## h.set('paden',['ergens',])
    ## print h.__dict__
    main(sys.argv[1:])
