# -*- coding: UTF-8 -*-
"""basic plugin for tool using a gtkaccel_map
"""
import sys
import collections
import functools
import string
import PyQt4.QtGui as gui
import PyQt4.QtCore as core
from .read_gtkaccel import read_keydefs_and_stuff

C_SAVE, C_DEL, C_KTXT, C_CTXT = '010', '011', '018', '019'
C_PARMS, C_CTRL, C_CNTXT = '090', '091', '047'
M_CTRL, M_ALT, M_SHFT, M_WIN = '007', '008', '009', '013'
settname = ''
C_KEY, C_TYPE, C_CMD, C_DESC, C_MODS = '001', '002', '003', '004', '043'
C_CODE, C_PLAT, C_FEAT, C_MNU = '046', '048', '049', '092'

def _translate_keyname(inp):
    convert = {'Escape': 'Esc', 'Delete': 'Del', 'Return': 'Enter',
        'Page_up': 'PgUp', 'Page_down': 'PgDn'}
    if inp in convert:
        out = convert[inp]
    else:
        out = inp
    return out

def buildcsv(settname, parent, showinfo=True):
    """lees de keyboard definities uit het/de settings file(s) van het tool zelf
    en geef ze terug voor schrijven naar het csv bestand
    """
    shortcuts = collections.OrderedDict()

    try:
        initial = parent.page.settings[settname][0]
    except KeyError:
        initial = ''
    if showinfo:
        kbfile = gui.QFileDialog.getOpenFileName(parent, parent.captions['059'],
            directory=initial)
    else:
        kbfile = initial
    if not kbfile:
        return

    stuffdict = read_keydefs_and_stuff(kbfile)
    keydefs = stuffdict.pop('keydefs')
    actions = stuffdict['actions']
    omsdict = stuffdict['descriptions']

    lastkey, used = 0, {}
    for key, mods, command in keydefs:
        lastkey += 1
        context, action = actions[command]
        description = omsdict[command]
        shortcuts[str(lastkey)] = (_translate_keyname(key), mods, context, action,
            description)

    return shortcuts, stuffdict

# callbacks for gui elements
def on_combobox(self, cb, text):
    """callback op het gebruik van een combobox

    zorgt ervoor dat de buttons ge(de)activeerd worden
    """
    if self.initializing:
        return
    text = str(text) # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan de
                     # callback soms fout?
    hlp = cb.currentText()
    if text != hlp:
        text = hlp
    ## print(self._origdata)
    self.defchanged = False
    keyitemindex = 0
    cmditemindex = 6
    if cb == self.cmb_key:
        if text != self._origdata[keyitemindex]:
            self._newdata[keyitemindex] = text
            self.defchanged = True
            self.b_save.setEnabled(True)
        elif str(self.cmb_commando.currentText()) == self._origdata[cmditemindex]:
            self.b_save.setEnabled(False)
    elif cb == self.cmb_commando:
        if text != self._origdata[cmditemindex]:
            self._newdata[cmditemindex] = text
            self.defchanged = True
            try:
                self.txt_oms.setText(self.descriptionsdict[text])
            except KeyError:
                self.txt_oms.setText('(Geen omschrijving beschikbaar)')
            self.b_save.setEnabled(True)
        elif str(self.cmb_key.currentText()) == self._origdata[keyitemindex]:
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
    return
    self.aanpassen()
    self.parent.p0list.setFocus()

def on_delete(self):
    return
    self.aanpassen(delete=True)
    self.parent.p0list.setFocus()

class MyPanel(gui.QFrame):

    def __init__(self, parent):
        gui.QFrame.__init__(self)
        self.parent = parent
        self.initializing = False
        ## self.csvfile = self.parent.pad
        ## self.settings = self.parent.settings

    def add_extra_attributes(self):
         # key, mods, cmnd, params, controls
        self._origdata = ["", False, False, False, False, "", '']
        self._newdata = self._origdata[:]

        self.keylist = [x for x in string.ascii_uppercase] + \
            [x for x in string.digits] + ["F" + str(i) for i in range(1,13)] + \
            ['Num' + x for x in string.digits] + ['>', '<'] + \
            [self.parent.captions[str(x)] for x in range(100,121)] + \
            ['.', ',', '+', '-', '`', '[', ']', '\\', ';', "'", '/']
        ## self.commandsdict = self.parent.otherstuff['keydefs']
        ## self.commandlist = sorted(self.commandsdict.keys())

        self.contextslist = self.parent.otherstuff['contexts']
        self.contextactionsdict = self.parent.otherstuff['actionscontext']
        self.actionslist = self.parent.otherstuff['actions']
        self.descriptionsdict = self.parent.otherstuff['descriptions']

        try:
            self.otherslist = self.parent.otherstuff['others']
        except KeyError:
            pass
        else:
            self.othersdict = self.parent.otherstuff['othercontext']
            self.otherskeys = self.parent.otherstuff['otherkeys']

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        self._box = box = gui.QFrame(self)
        ## box.setFrameShape(gui.QFrame.StyledPanel)
        box.setMaximumHeight(90)
        self.txt_key = gui.QLabel(self.parent.captions[C_KTXT] + " ", box)
        cb = gui.QComboBox(box)
        cb.setMaximumWidth(90)
        cb.addItems(self.keylist)
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_key = cb

        for x in (M_CTRL, M_ALT, M_SHFT, M_WIN):
            cb = gui.QCheckBox(self.parent.captions[x].join(("+ ","")), box)
            cb.setChecked(False)
            cb.stateChanged.connect(functools.partial(on_checkbox, self, cb))
            if x == M_CTRL:
                self.cb_ctrl = cb
            elif x == M_ALT:
                self.cb_alt = cb
            elif x == M_SHFT:
                self.cb_shift = cb
            elif x == M_WIN:
                self.cb_win = cb

        self.lbl_contexts = gui.QLabel(self.parent.captions[C_CNTXT], box)
        cb = gui.QComboBox(box)
        cb.addItems(self.contextslist)
        cb.setMaximumWidth(110)
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_contexts = cb

        self.txt_cmd = gui.QLabel(self.parent.captions[C_CTXT] + " ", box)
        ## self.commandlist.sort()
        cb = gui.QComboBox(self)
        cb.setMaximumWidth(150)
        ## cb.addItems(self.actionslist) # only load on choosing a context
        cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            self, cb, str))
        self.cmb_commando = cb

        self.b_save = gui.QPushButton(self.parent.captions[C_SAVE], box) ##, (120, 45))
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(functools.partial(on_update, self))
        self.b_del = gui.QPushButton(self.parent.captions[C_DEL], box) #, size= (50,-1)) ##, (120, 45))
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(functools.partial(on_delete, self))

        ## self.lbl_parms = gui.QLabel(self.parent.captions[C_PARMS], box)
        ## self.txt_parms = gui.QLineEdit(box)
        ## self.txt_parms.setMaximumWidth(280)
        ## self.lbl_controls = gui.QLabel(self.parent.captions[C_CTRL], box)
        ## cb = gui.QComboBox(box)
        ## cb.addItems(self.controlslist)
        ## cb.currentIndexChanged[str].connect(functools.partial(on_combobox,
            ## self, cb, str))
        ## self.cmb_controls = cb

        self.txt_oms = gui.QTextEdit(box)
        ## self.txt_oms.setMaximumHeight(40)
        if not self.parent.settings['RedefineKeys'][0] == '1':
            for widget in self.children():
                widget.setEnabled(False)
        self.txt_oms.setReadOnly(True)

    def layout_extra_fields(self, sizer):
        """add the extra fields to the layout
        """
        bsizer = gui.QVBoxLayout()

        sizer1 = gui.QHBoxLayout()
        sizer2 = gui.QHBoxLayout()
        sizer3 = gui.QHBoxLayout()
        sizer3.addWidget(self.txt_key)
        sizer3.addWidget(self.cmb_key)
        sizer2.addLayout(sizer3)
        sizer3 = gui.QHBoxLayout()
        sizer3.addWidget(self.cb_ctrl)
        sizer3.addWidget(self.cb_alt)
        sizer3.addWidget(self.cb_shift)
        sizer3.addWidget(self.cb_win)
        sizer2.addLayout(sizer3)
        sizer1.addLayout(sizer2)
        sizer1.addStretch()
        sizer2 = gui.QHBoxLayout()
        sizer2.addWidget(self.lbl_contexts)
        sizer2.addWidget(self.cmb_contexts)
        sizer1.addLayout(sizer2)
        sizer2 = gui.QHBoxLayout()
        sizer2.addWidget(self.txt_cmd)
        sizer2.addWidget(self.cmb_commando)
        sizer1.addLayout(sizer2)
        sizer1.addWidget(self.b_save)
        sizer1.addWidget(self.b_del)
        bsizer.addLayout(sizer1)

        sizer1 = gui.QHBoxLayout()
        sizer2 = gui.QVBoxLayout()
        sizer2.addWidget(self.txt_oms)
        ## bsizer.addLayout(sizer1)
        sizer1.addLayout(sizer2, 2)

        ## sizer1 = gui.QHBoxLayout()
        ## sizer2 = gui.QGridLayout()
        ## line = 0
        ## sizer2.addWidget(self.lbl_contexts, line, 0)
        ## sizer3 = gui.QHBoxLayout()
        ## sizer3.addWidget(self.cmb_contexts)
        ## sizer3.addStretch()
        ## sizer2.addLayout(sizer3, line, 1)
        ## line += 1
        ## sizer2.addWidget(self.lbl_parms, line, 0)
        ## sizer2.addWidget(self.txt_parms, line, 1)
        ## line += 1
        ## sizer2.addWidget(self.lbl_controls, line, 0)
        ## sizer3 = gui.QHBoxLayout()
        ## sizer3.addWidget(self.cmb_controls)
        ## sizer3.addStretch()
        ## sizer2.addLayout(sizer3, line, 1)
        ## sizer1.addLayout(sizer2, 1)

        bsizer.addLayout(sizer1)

        self._box.setLayout(bsizer)
        sizer.addWidget(self._box)

    def captions_extra_fields(self):
        """to be called on changing the language
        """
        self.cb_win.setText(self.parent.captions[M_WIN].join(("+", "  ")))
        self.cb_ctrl.setText(self.parent.captions[M_CTRL].join(("+", "  ")))
        self.cb_alt.setText(self.parent.captions[M_ALT].join(("+", "  ")))
        self.cb_shift.setText(self.parent.captions[M_SHFT].join(("+", "  ")))
        self.b_save.setText(self.parent.captions[C_SAVE])
        self.b_del.setText(self.parent.captions[C_DEL])
        self.txt_key.setText(self.parent.captions[C_KTXT])
        self.txt_cmd.setText(self.parent.captions[C_CTXT])
        ## self.lbl_parms.setText(self.parent.captions[C_PARMS])
        ## self.lbl_controls.setText(self.parent.captions[C_CTRL])
        self.lbl_contexts.setText(self.parent.captions[C_CNTXT])

    def on_item_selected(self, newitem, olditem): # olditem, newitem):
        """callback on selection of an item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        if not newitem: # bv. bij p0list.clear()
            return
        if self.initializing:
            self.vuldetails(newitem)
            return
        ## print('itemselected called', newitem.text(0))
        ## if olditem is not None:
            ## print('old item was', olditem.text(0))
        ## print('In itemselected:', self._origdata, self._newdata)
        pass
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
        for number, item in self.parent.data.items():
            if key == item[0] == key and item[1] == mods:
                gevonden = True
                indx = number
                break
        ## print(cursor_moved, other_item, other_cmd, gevonden)
        make_change = False
        if any_change:
            if cursor_moved:
                h = gui.QMessageBox.question(self,
                    self.parent.captions["000"], self.parent.captions["020"],
                    gui.QMessageBox.Yes | gui.QMessageBox.No)
                make_change = True if h == gui.QMessageBox.Yes else False
            elif other_item:
                if gevonden:
                    ok = gui.QMessageBox.question(self,
                        self.parent.captions["000"], self.parent.captions["045"],
                        gui.QMessageBox.Yes | gui.QMessageBox.No)
                    make_change = True if ok == gui.QMessageBox.Yes else False
                else:
                    make_change = True
            else:
                make_change = True
        if make_change:
            item = self.parent.p0list.currentItem()
            pos = self.parent.p0list.indexOfTopLevelItem(item)
            if gevonden:
                self.parent.data[indx] = (key, mods, 'U', cmd, self.omsdict[cmd])
            else:
                newdata = [x for x in self.parent.data.values()]
                newvalue = (key, mods, 'U', cmd, self.omsdict[cmd])
                newdata.append(newvalue)
                newdata.sort()
                for x, y in enumerate(newdata):
                    if y == newvalue:
                        indx = x
                    self.parent.data[x] = y
            self.parent.modified = True
            self._origdata = [key, False, False, False, False, cmd]
            for mod, indx in zip(('WCAS'),(4, 2, 3, 1)):
                self._origdata[indx] = mod in mods
            self.parent.populate_list(pos)    # refresh
            newitem = self.parent.p0list.topLevelItem(pos)
        self.vuldetails(newitem)

    def vuldetails(self, selitem):  # let op: aangepast (gebruik zip)
        if not selitem: # bv. bij p0list.clear()
            return
        seli = selitem.data(0, core.Qt.UserRole)
        if sys.version < '3':
            seli = seli.toPyObject()
        ## key, mods, context, command, oms = self.parent.data[seli]
        keydefdata = self.parent.data[seli]
        # todo: derive the order of these elements from the csv file
        self.b_save.setEnabled(False)
        self.b_del.setEnabled(False)
        self._origdata = ['', False, False, False, False, '', '']
        for indx, item in enumerate(keydefdata):
            if self.parent.column_info[indx][0] == C_KEY:
                key = item
                ix = self.keylist.index(key)
                self.cmb_key.setCurrentIndex(ix)
                ## self.cmb_key.setEditText(key)
                self._origdata[0] = key
            elif self.parent.column_info[indx][0] == C_MODS:
                mods = item
                self.cb_shift.setChecked(False)
                self.cb_ctrl.setChecked(False)
                self.cb_alt.setChecked(False)
                self.cb_win.setChecked(False)
                for x, y, z in zip('SCAW',(1, 2, 3, 4), (self.cb_shift,
                        self.cb_ctrl, self.cb_alt, self.cb_win)):
                    if x in mods:
                        self._origdata[y] = True
                        z.setChecked(True)
            elif self.parent.column_info[indx][0] == C_TYPE:
                soort = item
                if soort == 'U':
                    self.b_del.setEnabled(True)
            elif self.parent.column_info[indx][0] == C_CNTXT:
                context = item
                ix = self.contextslist.index(context)
                self.cmb_contexts.setCurrentIndex(ix)
                self._origdata[5] = context
            elif self.parent.column_info[indx][0] == C_CMD:
                command = item
                self.initializing = True
                self.cmb_commando.clear()
                actionslist = self.contextactionsdict[context]
                self.cmb_commando.addItems(actionslist)
                ix = actionslist.index(command)
                self.cmb_commando.setCurrentIndex(ix)
                self.initializing = False
                self._origdata[6] = command
            elif self.parent.column_info[indx][0] == C_DESC:
                oms = item
                self.txt_oms.setText(oms)
        self._newdata = self._origdata[:]

    def aanpassen(self, delete=False): # TODO
        print('aanpassen called')
        return
        item = self.parent.p0list.currentItem()
        pos = self.parent.p0list.indexOfTopLevelItem(item)
        if delete:
            indx = item.data(0, core.Qt.UserRole)
            if sys.version < '3':
                indx = int(indx.toPyObject())
            if self.parent.captions["{:03}".format(indx)] == C_TYPE:
                if self.parent.data[indx][1] == "S": # can't delete standard key
                    gui.QMessageBox.information(self, self.parent.captions["000"],
                        self.parent.captions['024'])
                    return
            elif self.parent.captions["{:03}".format(indx)] == C_KEY:
                if self.parent.data[indx][0] in self.defkeys: # restore standard if any
                    cmd = self.defkeys[self.parent.data[indx][0]]
                    if cmd in self.omsdict:
                        oms = self.omsdict[cmd]
                    else:
                        oms = cmd
                        cmd = ""
                    self.parent.data[indx] = (key, 'S', cmd, oms)
                else:
                    del self.parent.data[indx]
                    ## pos -= 1
            self.b_save.setEnabled(False)
            self.b_del.setEnabled(False)
            self.parent.modified = True
            self.parent.setWindowTitle(' '.join((self.parent.captions["000"],
                self.parent.captions['017'])))
            print('item deleted, pos is', pos)
            self.parent.populate_list(pos)    # refresh
        else:
            self.on_item_selected(item, item) # , from_update=True)

#
