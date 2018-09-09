"""hotkeys.py - PyQt5 version

    main gui (choicebook)
    importeert de verschillende applicatiemodules
    hierin wordt het menu gedefinieerd en de functies die daarbij horen
    het idee is dat de menuopties wanneer nodig uitgegrijsd zijn en dat
        in de routines wordt uitgevraagd wat te doen bij welke applicatie
    voor wat betreft de instellingen:
        taalkeuze: op dit niveau
        paden: op applicatie niveau (in betreffende csv file)
"""
from __future__ import print_function
import os
import sys
## import shutil
import string
import functools
import importlib
import logging
import PyQt5.QtWidgets as qtw
## import PyQt5.QtGui as gui
import PyQt5.QtCore as core

import editor.hotkeys_constants as hkc
import editor.hotkeys_dialogs_qt5 as hkd


class HotkeyPanel(qtw.QFrame):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    definieert feitelijk een "custom widget"
    coldata is een list of tuple van 4-tuples die achtereenvolgens aangeven
    de kolomtitel, de breedte, de index op self.data en of het een soort aangeeft
    verwacht dat de subclass van te voren een attribuut gedefinieerd heeft:
    _keys: de module om de settings te lezen
    """
    def __init__(self, parent, pad):
        self.pad = pad
        # switch om het gedrag van bepaalde routines tijdens initialisatie te beïnvloeden
        self._initializing_screen = True
        self.modified = False

        super().__init__(parent)
        self.parent = parent  # .parent()
        self.captions = self.parent.parent.captions
        self.filtertext = ''
        self.has_extrapanel = False

        logging.info(self.pad)
        nodata = ''
        if self.pad:
            try:
                self.settings, self.column_info, self.data = hkc.readcsv(self.pad)
            except ValueError as e:
                logging.exception('')
                nodata = self.captions['I_NOSET'].format(e, self.pad)
            except FileNotFoundError:
                logging.exception('')
                nodata = self.captions['I_NOSETFIL'].format(self.pad)
        else:
            nodata = self.captions['I_NOSETFIL'].format(self.pad)
        if nodata:
            self.settings, self.column_info, self.data = {}, [], {}
        self.otherstuff = {}  # ruimte voor zaken als een lijst met mogelijke commando's

        if not self.settings or not self.column_info:
            tmp = ":\n\n" + nodata if nodata else ""
            nodata = self.captions['I_NODATA'] + tmp
        else:
            try:
                modulename = self.settings[hkc.SettType.PLG.value]
            except KeyError:
                logging.exception('')
                nodata = True
            else:
                try:
                    self._keys = importlib.import_module(modulename)
                except ImportError:
                    logging.exception('')
                    nodata = True
            if nodata:
                nodata = self.captions['I_NODATA'].replace('data', 'plugin code')

        if not nodata:
            self.p0list = qtw.QTreeWidget(self)
            self.parent.page = self
            try:
                test = self._keys.buildcsv
            except AttributeError:
                pass
            else:
                try:
                    self.otherstuff = self._keys.buildcsv(parent, showinfo=False)[1]
                except FileNotFoundError:
                    nodata = "Can't build settings for {}".format(modulename)
                # except AttributeError:
                #    print('Got AttributeError for {}'.format(modulename))
                #    raise

        if nodata:
            _sizer = qtw.QVBoxLayout()
            hsizer = qtw.QHBoxLayout()
            hsizer.addStretch()
            hsizer.addWidget(qtw.QLabel(nodata, self))
            hsizer.addStretch()
            _sizer.addLayout(hsizer)
            self.setLayout(_sizer)
            self.title = self.parent.parent.title
            return

        try:
            self.has_extrapanel = bool(int(self.settings[hkc.SettType.DETS.value]))
        except KeyError:
            pass

        self.title = self.settings["PanelName"]

        # self.has_extrapanel controleert extra initialisaties en het opbouwen van het extra
        # schermdeel - het vullen van veldwaarden hierin gebeurt als gevolg van het vullen
        # van de eerste rij in de listbox, daarom moet deze het laatst
        # self.otherstuff = self._keys.getotherstuff()
        if self.has_extrapanel:
            logging.info('extrapanel: %s', self.has_extrapanel)
            self.fields = [x[0] for x in self.column_info]
            self.add_extra_attributes()
            self.add_extra_fields()

        self._sizer = qtw.QVBoxLayout()
        if self.column_info:
            self.p0list.setSortingEnabled(True)
            self.p0list.setHeaderLabels([self.captions[col[0]] for col in
                                         self.column_info])
            self.p0list.setAlternatingRowColors(True)
            self.p0list.currentItemChanged.connect(self.on_item_selected)
            hdr = self.p0list.header()
            hdr.setSectionsClickable(True)
            for indx, col in enumerate(self.column_info):
                if indx <= len(self.column_info):
                    hdr.resizeSection(indx, col[1])
            hdr.setStretchLastSection(True)
            self.populate_list()
            sizer1 = qtw.QHBoxLayout()
            sizer1.addWidget(self.p0list)
            self._sizer.addLayout(sizer1)

        # indien van toepassing: toevoegen van de rest van de GUI aan de layout
        if self.has_extrapanel:
            self.layout_extra_fields(self._sizer)

        self.setLayout(self._sizer)
        self._initializing_screen = False
        logging.info(self.otherstuff)

    def readkeys(self):
        "(re)read the data for the keydef list"
        self.data = hkc.readcsv(self.pad)[2]

    def savekeys(self):
        """save modified keydef back

        allows saving back to csv without (?) saving to the tool settings
        """
        self.parent.data = self.data
        try:
            self._keys.savekeys(self)
        except AttributeError:
            pass
        hkc.writecsv(self.pad, self.settings, self.column_info, self.data,
                     self.parent.parent.ini['lang'])
        self.set_title(modified=False)

    def set_title(self, modified=None):
        """set title and adapt to modified flag
        if modified flag is not supplied, use its current state
        """
        # is this of any use? does this window has its own title?
        if modified is not None:
            self.modified = False
        title = self.title
        if self.modified:
            title += ' ' + self.captions["T_MOD"]
        self.setWindowTitle(title)

    def setcaptions(self):
        """update captions according to selected language
        """
        self.set_title()
        if self.has_extrapanel:
            self.captions_extra_fields()
        if self.data:
            self.populate_list()

    def populate_list(self, pos=0):
        """vullen van de list control
        """
        self.p0list.clear()
        items = self.data.items()
        # if not items:  # if items is None or len(items) == 0:
        #     return

        for key, data in items:
            try:
                int(key)
            except ValueError:
                continue
            new_item = qtw.QTreeWidgetItem()
            new_item.setData(0, core.Qt.UserRole, key)
            for indx, col in enumerate(self.column_info):
                is_soort = col[2]
                value = data[indx]
                if is_soort:
                    value = 'C_DFLT' if value == 'S' else 'C_RDEF'
                    value = self.captions[value]
                new_item.setText(indx, value)
            self.p0list.addTopLevelItem(new_item)
            self.p0list.setCurrentItem(self.p0list.topLevelItem(pos))

    def exit(self):
        """processing triggered by exit button
        """
        if self.modified:
            ok = qtw.QMessageBox.question(self, self.parent.title,
                                          self.parent.captions['Q_SAVXIT'],
                                          qtw.QMessageBox.Yes | qtw.QMessageBox.No |
                                          qtw.QMessageBox.Cancel)
            if ok == qtw.QMessageBox.Yes:
                self.savekeys()
            elif ok == qtw.QMessageBox.Cancel:
                return False
        return True

    def add_extra_attributes(self):
        """pertaining to details for selected keydef, to make editing possible
        """
        self.init_origdata = []
        ix_item = 0
        if 'C_KEY' in self.fields:
            self.init_origdata.append('')
            self.ix_key = ix_item
            ix_item += 1
            self.keylist = [x for x in string.ascii_uppercase] + \
                [x for x in string.digits] + ["F" + str(i) for i in range(1, 13)] + \
                hkc.named_keys + \
                ['.', ',', '+', '=', '-', '`', '[', ']', '\\', ';', "'", '/']
        if 'C_MODS' in self.fields:
            self.init_origdata += [False, False, False, False]
            self.ix_mods = []
            for _ in range(4):
                self.ix_mods.append(ix_item)
                ix_item += 1
        if 'C_CNTXT' in self.fields:
            self.init_origdata.append('')
            self.ix_cntxt = ix_item
            ix_item += 1
        if 'C_CMD' in self.fields:
            self.init_origdata.append('')
            self.ix_cmd = ix_item
            ix_item += 1
        self.contextslist = []
        self.contextsactionsdict = {}
        self.commandslist = []
        try:
            self._keys.add_extra_attributes(self)  # user exit
        except AttributeError:
            pass
        if self.keylist:
            self.keylist.sort()

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        # print(self.keylist)
        self.screenfields = []
        self._box = box = qtw.QFrame(self)
        frameheight = 90
        try:
            frameheight = self._keys.get_frameheight()  # user exit
        except AttributeError:
            pass
        box.setMaximumHeight(frameheight)

        if 'C_KEY' in self.fields:
            self.lbl_key = qtw.QLabel(self.captions['C_KTXT'] + " ", box)
            if self.keylist is None:
                ted = qtw.QLineEdit(box)
                ted.setMaximumWidth(90)
                ted.textChanged[str].connect(functools.partial(self.on_text, ted, str))
                self.screenfields.append(ted)
                self.txt_key = ted
            else:
                cb = qtw.QComboBox(box)
                cb.setMaximumWidth(90)
                cb.addItems(self.keylist)  # niet sorteren
                cb.currentIndexChanged[str].connect(functools.partial(self.on_combobox,
                                                                      cb, str))
                self.screenfields.append(cb)
                self.cmb_key = cb

        if 'C_MODS' in self.fields:
            for ix, x in enumerate(('M_CTRL', 'M_ALT', 'M_SHFT', 'M_WIN')):
                cb = qtw.QCheckBox(self.captions[x].join(("+ ", "")), box)
                cb.setChecked(False)
                self.screenfields.append(cb)
                cb.stateChanged.connect(functools.partial(self.on_checkbox, cb))
                if ix == 0:
                    self.cb_ctrl = cb
                elif ix == 1:
                    self.cb_alt = cb
                elif ix == 2:
                    self.cb_shift = cb
                elif ix == 3:
                    self.cb_win = cb

        if 'C_CNTXT' in self.fields:
            self.lbl_context = qtw.QLabel(self.captions['C_CNTXT'], box)
            cb = qtw.QComboBox(box)
            cb.addItems(self.contextslist)
            cb.setMaximumWidth(110)
            cb.currentIndexChanged[str].connect(functools.partial(self.on_combobox,
                                                                  cb, str))
            self.screenfields.append(cb)
            self.cmb_context = cb

        if 'C_CMD' in self.fields:
            self.txt_cmd = qtw.QLabel(self.captions['C_CTXT'] + " ", box)
            cb = qtw.QComboBox(self)
            cb.setMaximumWidth(150)
            if 'C_CNTXT' not in self.fields:  # load on choosing context
                cb.addItems(self.commandslist)
            cb.currentIndexChanged[str].connect(functools.partial(self.on_combobox,
                                                                  cb, str))
            self.screenfields.append(cb)
            self.cmb_commando = cb

        self.b_save = qtw.QPushButton(self.captions['C_SAVE'], box)
        self.b_save.setEnabled(False)
        self.b_save.clicked.connect(self.on_update)
        self.b_del = qtw.QPushButton(self.captions['C_DEL'], box)
        self.b_del.setEnabled(False)
        self.b_del.clicked.connect(self.on_delete)
        self._savestates = (False, False)

        if 'C_DESC' in self.fields:
            self.txt_oms = qtw.QTextEdit(box)
            self.txt_oms.setReadOnly(True)

        try:
            self._keys.add_extra_fields(self, box)  # user exit
        except AttributeError:
            pass

        self.set_extrascreen_editable(bool(int(self.settings['RedefineKeys'])))

    def set_extrascreen_editable(self, switch):
        """open up fields in extra screen when applicable
        """
        for widget in self.screenfields:
            widget.setEnabled(switch)
        ## if 'C_CMD' in self.fields:
        if switch:
            state_s, state_d = self._savestates
        else:
            self._savestates = (self.b_save.isEnabled(), self.b_del.isEnabled())
            state_s, state_d = False, False
        self.b_save.setEnabled(state_s)
        self.b_del.setEnabled(state_d)

    def layout_extra_fields(self, sizer):
        """add the extra fields to the layout
        """
        bsizer = qtw.QVBoxLayout()

        sizer1 = qtw.QHBoxLayout()
        sizer2 = qtw.QHBoxLayout()
        if 'C_KEY' in self.fields:
            sizer3 = qtw.QHBoxLayout()
            sizer3.addWidget(self.lbl_key)
            if self.keylist is None:
                sizer3.addWidget(self.txt_key)
            else:
                sizer3.addWidget(self.cmb_key)
            sizer3.addStretch()
            sizer2.addLayout(sizer3)

        if 'C_MODS' in self.fields:
            sizer3 = qtw.QHBoxLayout()
            sizer3.addWidget(self.cb_ctrl)
            sizer3.addWidget(self.cb_alt)
            sizer3.addWidget(self.cb_shift)
            sizer3.addWidget(self.cb_win)
            sizer3.addStretch()
            sizer2.addLayout(sizer3)

        sizer1.addLayout(sizer2)
        sizer1.addStretch()
        if 'C_CNTXT' in self.fields:
            sizer2 = qtw.QHBoxLayout()
            sizer2.addWidget(self.lbl_context)
            sizer2.addWidget(self.cmb_context)
            sizer1.addLayout(sizer2)

        if 'C_CMD' in self.fields:
            sizer2 = qtw.QHBoxLayout()
            sizer2.addWidget(self.txt_cmd)
            sizer2.addWidget(self.cmb_commando)
            sizer1.addLayout(sizer2)

        try:
            self._keys.layout_extra_fields_topline(self, sizer1)  # user exit
        except AttributeError:
            pass

        sizer1.addWidget(self.b_save)
        sizer1.addWidget(self.b_del)
        bsizer.addLayout(sizer1)

        try:
            test = self._keys.layout_extra_fields_nextline
        except AttributeError:
            pass
        else:
            sizer1 = qtw.QHBoxLayout()
            self._keys.layout_extra_fields_nextline(self, sizer1)  # user exit
            bsizer.addLayout(sizer1)

        sizer1 = qtw.QHBoxLayout()
        if 'C_DESC' in self.fields:
            sizer2 = qtw.QVBoxLayout()
            sizer2.addWidget(self.txt_oms)
            sizer1.addLayout(sizer2, 2)

        try:
            self._keys.layout_extra_fields(self, sizer1)  # user exit
        except AttributeError:
            pass

        bsizer.addLayout(sizer1)

        self._box.setLayout(bsizer)
        sizer.addWidget(self._box)

    def captions_extra_fields(self):
        """to be called on changing the language
        """
        if 'C_KEY' in self.fields:
            self.lbl_key.setText(self.captions['C_KTXT'])
        if 'C_MODS' in self.fields:
            self.cb_win.setText(self.captions['M_WIN'].join(("+", "  ")))
            self.cb_ctrl.setText(self.captions['M_CTRL'].join(("+", "  ")))
            self.cb_alt.setText(self.captions['M_ALT'].join(("+", "  ")))
            self.cb_shift.setText(self.captions['M_SHFT'].join(("+", "  ")))
        if 'C_CNTXT' in self.fields:
            self.lbl_context.setText(self.captions['C_CNTXT'] + ':')
        if 'C_CMD' in self.fields:
            self.txt_cmd.setText(self.captions['C_CTXT'])
        self.b_save.setText(self.captions['C_SAVE'])
        self.b_del.setText(self.captions['C_DEL'])
        try:
            self._keys.captions_extra_fields(self)  # user exit
        except AttributeError:
            pass

    def on_text(self, ted, text):
        """on changing a text entry
        """
        if self._initializing_screen:
            return
        text = str(text)    # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan
                            # de callback soms fout? Of is het Py3 vs Py2?
        hlp = ted.text()
        if text != hlp:
            text = hlp
        if 'C_KEY' in self.fields:
            if text == self._origdata[self.ix_key]:
                self.defchanged = True
                self.b_save.setEnabled(True)
            elif ted.text() == self._origdata[self.ix_key]:
                self.defchanged = False
                self.b_save.setEnabled(False)

    def on_combobox(self, cb, text):
        """callback op het gebruik van een combobox

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        if self._initializing_screen:
            return
        text = str(text)    # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan
                            # de callback soms fout? Of is het Py3 vs Py2?
        hlp = cb.currentText()
        if text != hlp:
            text = hlp
        self.defchanged = False
        try:
            test_key = bool(self.cmb_key)
        except AttributeError:
            test_key = False
        try:
            test_cmd = bool(self.cmb_commando)
        except AttributeError:
            test_cmd = False
        try:
            test_cnx = bool(self.cmb_context)
        except AttributeError:
            test_cnx = False
        if test_key and cb == self.cmb_key:
            keyitemindex = self.ix_key
            if text != self._origdata[keyitemindex]:
                self._newdata[keyitemindex] = text
                if not self.initializing_keydef:
                    self.defchanged = True
                    if 'C_CMD' in self.fields:
                        self.b_save.setEnabled(True)
            elif str(self.cmb_commando.currentText()) == self._origdata[keyitemindex]:  # UNDEF
                self.defchanged = False
                if 'C_CMD' in self.fields:
                    self.b_save.setEnabled(False)
        elif test_cnx and cb == self.cmb_context:
            if text != self._origdata[self.ix_cntxt]:
                context = self._origdata[self.ix_cntxt] = self.cmb_context.currentText()
                self.cmb_commando.clear()
                if self.contextactionsdict:
                    actionslist = self.contextactionsdict[context]
                else:
                    actionslist = self.commandslist
                self.cmb_commando.addItems(actionslist)
                if not self.initializing_keydef:
                    self.defchanged = True
                    if 'C_CMD' in self.fields:
                        self.b_save.setEnabled(True)
            elif str(self.cmb_commando.currentText()) == self._origdata[self.ix_cntxt]:
                self.defchanged = False
                if 'C_CMD' in self.fields:
                    self.b_save.setEnabled(False)
        elif test_cmd and cb == self.cmb_commando:
            cmditemindex = self.ix_cmd
            if text != self._origdata[cmditemindex]:
                self._newdata[cmditemindex] = text
                try:
                    self.txt_oms.setText(self.descriptions[text])
                except KeyError:
                    self.txt_oms.setText(self.captions['M_NODESC'])
                if not self.initializing_keydef:
                    self.defchanged = True
                    if 'C_CMD' in self.fields:
                        self.b_save.setEnabled(True)
            elif str(self.cmb_key.currentText()) == self._origdata[cmditemindex]:
                if 'C_CMD' in self.fields:
                    self.b_save.setEnabled(False)
        else:
            try:
                self._keys.on_combobox(self, cb, text)  # user exit
            except AttributeError:
                pass

    def on_checkbox(self, cb, state):
        """callback op het gebruik van een checkbox

        voorlopig alleen voor de modifiers
        """
        if self._initializing_screen:
            return
        ## state = bool(state)
        for win, indx in zip(
                (self.cb_shift, self.cb_ctrl, self.cb_alt, self.cb_win),
                self.ix_mods):
            if cb == win and state != self._origdata[indx]:
                self._newdata[indx] = state
                if not self.initializing_keydef:
                    self.defchanged = True
                    if 'C_CMD' in self.fields:
                        self.b_save.setEnabled(True)
                break
        else:
            states = [self.cb_shift.isChecked(), self.cb_ctrl.isChecked(),
                      self.cb_alt.isChecked(), self.cb_win.isChecked()]
            if states == [self._origdata[x] for x in self.ix_mods]:
                self.defchanged = False
                if 'C_CMD' in self.fields:
                    self.b_save.setEnabled(False)

    def on_item_selected(self, newitem, olditem):
        """callback on selection of an item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie

        bevat een soort detectie of de definitie gewijzigd is die rekening probeert
        te houden met of een nieuwe keydef wordt aangemaakt die een kopie is van de
        oude voor een andere keycombo - alleen die triggert ook bij opbouwen van
        het scherm
        """
        if not self.has_extrapanel:
            return
        # if not int(self.parent.page.settings[hkc.SettType.RDEF.value]):
        #     return
        if not newitem:  # bv. bij p0list.clear()
            return
        self.initializing_keydef = True
        if self._initializing_screen:
            self.refresh_extrascreen(newitem)
            self.initializing_keydef = False
            return
        other_item = other_cntxt = other_cmd = False
        if 'C_KEYS' in self.fields:
            origkey = self._origdata[self.ix_key]
            key = self._newdata[self.ix_key]
            other_item = key != origkey
        if 'C_MODS' in self.fields:
            origmods = ''.join([y for x, y in zip(self.ix_mods, ('WCAS'))
                                if self._origdata[x]])
            mods = ''.join([y for x, y in zip(self.ix_mods, ('WCAS'))
                            if self._newdata[x]])
            other_item = other_item or mods != origmods
        if 'C_CMD' in self.fields:
            origcmd = self._origdata[self.ix_cmd]
            cmnd = self._newdata[self.ix_cmd]
            other_cmd = cmnd != origcmd
        if 'C_CNTXT' in self.fields:
            origcntxt = self._origdata[self.ix_cntxt]
            context = self._newdata[self.ix_cntxt]
            other_cntxt = context != origcntxt
        cursor_moved = True if newitem != olditem and olditem is not None else False
        any_change = other_item or other_cmd or other_cntxt
        found = False
        for number, item in self.data.items():
            keymatch = modmatch = cntxtmatch = True
            if 'C_KEYS' in self.fields and item[0] != key:
                keymatch = False
            if 'C_MODS' in self.fields and item[1] != mods:
                modmatch = False
            if 'C_CNTXT' in self.fields and item[2] != context:
                cntxtmatch = False
            if keymatch and modmatch and cntxtmatch:
                found = True
                indx = number
                break
        make_change = False
        if any_change:
            if cursor_moved:
                make_change = hkd.ask_question(self, "Q_SAVCHG")
            elif other_item:
                if found:
                    make_change = hkd.ask_question(self, "Q_DPLKEY")
                else:
                    make_change = True
            else:
                make_change = True
        # TODO note this only works for one specific plugin (tcmdrkys) I think
        # which is no problem as long as I don't modify keydefs
        if make_change:
            item = self.p0list.currentItem()
            pos = self.p0list.indexOfTopLevelItem(item)
            if found:
                self.data[indx] = (key, mods, 'U', cmnd, self.omsdict[cmnd])
            else:
                newdata = [x for x in self.data.values()]
                # TODO: fix error when modifying TC keydef
                # UnboundLocalError: local variable 'key' referenced before assignment
                newvalue = (key, mods, 'U', cmnd, self.omsdict[cmnd])
                newdata.append(newvalue)
                newdata.sort()
                for x, y in enumerate(newdata):
                    if y == newvalue:
                        indx = x
                    self.data[x] = y
            self.modified = True
            self._origdata = self.init_origdata
            if 'C_KEY' in self.fields:
                self._origdata[self.ix_key] = key
            if 'C_MODS' in self.fields:
                for mod, indx in zip(('WCAS'), self.ix_mods):
                    self._origdata[indx] = mod in mods
            if 'C_CMD' in self.fields:
                self._origdata[self.ix_cmd] = cmnd
            if 'C_CNTXT' in self.fields:
                self._origdata[self.ix_cntxt] = context
            try:
                self._keys.on_extra_selected(self, item)  # user exit
            except AttributeError:
                pass
            newitem = self.p0list.topLevelItem(pos)
            self.populate_list(pos)    # refresh
        self.refresh_extrascreen(newitem)
        self.initializing_keydef = False

    def on_update(self):
        """callback for editing kb shortcut
        """
        self.do_modification()
        self.p0list.setFocus()

    def on_delete(self):
        """callback for deleting kb shortcut
        """
        self.do_modification(delete=True)
        self.p0list.setFocus()

    def refresh_extrascreen(self, selitem):
        """show new values after changing kb shortcut
        """
        if not selitem:  # bv. bij p0list.clear()
            return
        seli = selitem.data(0, core.Qt.UserRole)
        if sys.version < '3':
            seli = seli.toPyObject()
        keydefdata = self.data[seli]
        if 'C_CMD' in self.fields:
            self.b_save.setEnabled(False)
            self.b_del.setEnabled(False)
        self._origdata = self.init_origdata[:]
        for indx, item in enumerate(keydefdata):
            if self.column_info[indx][0] == 'C_KEY':
                key = item
                if self.keylist is None:
                    self.txt_key.setText(key)
                else:
                    ix = self.keylist.index(key)
                    self.cmb_key.setCurrentIndex(ix)
                self._origdata[self.ix_key] = key
            elif self.column_info[indx][0] == 'C_MODS':
                mods = item
                self.cb_shift.setChecked(False)
                self.cb_ctrl.setChecked(False)
                self.cb_alt.setChecked(False)
                self.cb_win.setChecked(False)
                for x, y, z in zip('SCAW', self.ix_mods, (self.cb_shift, self.cb_ctrl,
                                                          self.cb_alt, self.cb_win)):
                    if x in mods:
                        self._origdata[y] = True
                        z.setChecked(True)
            elif self.column_info[indx][0] == 'C_TYPE':
                soort = item
                if soort == 'U':
                    self.b_del.setEnabled(True)
            elif self.column_info[indx][0] == 'C_CNTXT' and self.contextslist:
                context = item
                ix = self.contextslist.index(context)
                self.cmb_context.setCurrentIndex(ix)
                self._origdata[self.ix_cntxt] = context
            elif self.column_info[indx][0] == 'C_CMD' and self.commandslist:
                command = item
                if 'C_CNTXT' in self.fields:
                    self.cmb_commando.clear()
                    context = self.cmb_context.currentText()
                    if self.contextactionsdict:
                        actionslist = self.contextactionsdict[context]
                    else:
                        actionslist = self.commandslist
                    self.cmb_commando.addItems(actionslist)
                    try:
                        ix = actionslist.index(command)
                    except ValueError:
                        ix = -1
                else:
                    ix = self.commandslist.index(command)
                if ix >= 0:
                    self.cmb_commando.setCurrentIndex(ix)
                self._origdata[self.ix_cmd] = command
            elif self.column_info[indx][0] == 'C_DESC':
                oms = item
                self.txt_oms.setText(oms)
            else:
                try:
                    self._keys.vul_extra_details(self, indx, item)  # user exit
                except AttributeError:
                    pass
        self._newdata = self._origdata[:]

    def do_modification(self, delete=False):
        """currently this only works for tcmdrkys - or does it?
        """
        # TODO uitzetten overbodig maken
        print("Aanpassen uitgezet, werkt nog niet voor alles")
        return
        item = self.p0list.currentItem()
        pos = self.p0list.indexOfTopLevelItem(item)
        if delete:
            indx = item.data(0, core.Qt.UserRole)
            if sys.version < '3':
                indx = int(indx.toPyObject())
            if self.captions["{:03}".format(indx)] == 'C_TYPE':
                if self.data[indx][1] == "S":  # can't delete standard key
                    hkd.show_message(self.parent, 'I_STDDEF')
                    return
            elif self.captions["{:03}".format(indx)] == 'C_KEY':
                if self.data[indx][0] in self.defkeys:  # restore standard if any
                    cmnd = self.defkeys[self.data[indx][0]]
                    if cmnd in self.omsdict:
                        oms = self.omsdict[cmnd]
                    else:
                        oms, cmnd = cmnd, ""
                    key = self.data[indx][0]                 # is this correct?
                    self.data[indx] = (key, 'S', cmnd, oms)  # key UNDEF
                else:
                    del self.data[indx]
                    ## pos -= 1
            self.b_save.setEnabled(False)
            self.b_del.setEnabled(False)
            self.set_title(modified=True)
            self.populate_list(pos)    # refresh
        else:
            self.on_item_selected(item, item)  # , from_update=True)


class ChoiceBook(qtw.QFrame):
    """ Als QTabwidget, maar met selector in plaats van tabs
    """
    def __init__(self, parent, plugins):
        self.plugins = plugins
        self.parent = parent
        super().__init__(parent)
        self.sel = qtw.QComboBox(self)
        self.sel.currentIndexChanged.connect(self.on_page_changed)
        self.find_loc = qtw.QComboBox(self)
        self.find_loc.setMinimumContentsLength(5)
        self.find_loc.setEditable(False)
        self.find = qtw.QComboBox(self)
        self.find.setMinimumContentsLength(20)
        self.find.setEditable(True)
        self.find.editTextChanged.connect(self.on_text_changed)
        self.b_next = qtw.QPushButton("", self)
        self.b_next.clicked.connect(self.find_next)
        self.b_next.setEnabled(False)
        self.b_prev = qtw.QPushButton('', self)
        self.b_prev.clicked.connect(self.find_prev)
        self.b_prev.setEnabled(False)
        self.b_filter = qtw.QPushButton(self.parent.captions['C_FILTER'], self)
        self.b_filter.clicked.connect(self.filter)
        self.b_filter.setEnabled(False)
        self.filter_on = False
        self.pnl = qtw.QStackedWidget(self)
        for txt, loc in self.plugins:
            if loc and not os.path.exists(loc):
                loc = os.path.join(hkc.BASE, loc)
            win = HotkeyPanel(self, loc)
            self.pnl.addWidget(win)
            try:
                fl = win.settings[hkc.SettType.PLG.value]
            except KeyError:
                fl = ''  # error is handled elsewhere
            self.parent.pluginfiles[txt] = fl
            self.sel.addItem(txt)
        self.b_exit = qtw.QPushButton(self.parent.captions['C_EXIT'], self)
        self.b_exit.clicked.connect(self.parent.exit)

        box = qtw.QVBoxLayout()
        vbox = qtw.QVBoxLayout()
        hbox = qtw.QHBoxLayout()
        hbox.addSpacing(10)
        self.sel_text = qtw.QLabel("", self)
        hbox.addWidget(self.sel_text)
        hbox.addWidget(self.sel)
        hbox.addStretch()
        self.find_text = qtw.QLabel("", self)
        hbox.addWidget(self.find_text)
        hbox.addWidget(self.find_loc)
        hbox.addWidget(qtw.QLabel(":", self))
        hbox.addWidget(self.find)
        hbox.addWidget(self.b_filter)
        hbox.addWidget(self.b_next)
        hbox.addWidget(self.b_prev)
        hbox.addSpacing(10)
        vbox.addLayout(hbox)
        box.addLayout(vbox)
        hbox = qtw.QVBoxLayout()
        hbox.addWidget(self.pnl)
        box.addLayout(hbox)

        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.b_exit)
        hbox.addStretch()
        box.addLayout(hbox)

        self.setLayout(box)
        self.setcaptions()

    def setcaptions(self):
        """update captions according to selected language
        """
        self.b_next.setText(self.parent.captions['C_NEXT'])
        self.b_prev.setText(self.parent.captions['C_PREV'])
        self.sel_text.setText(self.parent.captions['C_SELPRG'])
        self.find_text.setText(self.parent.captions['C_FIND'])
        if self.filter_on:
            self.b_filter.setText(self.parent.captions['C_FLTOFF'])
        else:
            self.b_filter.setText(self.parent.captions['C_FILTER'])
        self.b_exit.setText(self.parent.captions['C_EXIT'])

    def on_page_changed(self, indx):
        """callback for change in tool page
        """
        page = self.pnl.currentWidget()
        if page is None:
            return
        self.parent.sb.showMessage(self.parent.captions["M_DESC"].format(
            self.sel.currentText()))
        if page.modified:
            ok = page.exit()
            if not ok:
                return
        self.pnl.setCurrentIndex(indx)
        self.parent.page = self.pnl.currentWidget()  # change to new selection
        self.parent.setup_menu()
        if not all((self.parent.page.settings, self.parent.page.column_info,
                    self.parent.page.data)):
            return
        self.parent.page.setcaptions()
        items = [self.parent.captions[x[0]] for x in self.parent.page.column_info]
        self.find_loc.clear()
        self.find_loc.addItems(items)
        self.find_loc.setCurrentText(items[-1])
        if self.parent.page.filtertext:
            self.find.setEditText(self.parent.page.filtertext)
            self.b_filter.setText(self.parent.captions['C_FLTOFF'])
            self.b_filter.setEnabled(True)
        else:
            self.find.setEditText('')
            self.find.setEnabled(True)
            self.b_next.setEnabled(False)
            self.b_prev.setEnabled(False)
            self.b_filter.setEnabled(False)

    def on_text_changed(self, text):
        """callback for change in search text
        """
        page = self.parent.page  # self.pnl.currentWidget()
        for ix, item in enumerate(page.column_info):
            if self.page.captions[item[0]] == self.find_loc.currentText():
                self.zoekcol = ix
                break
        self.items_found = page.p0list.findItems(text, core.Qt.MatchContains, self.zoekcol)
        self.b_next.setEnabled(False)
        self.b_prev.setEnabled(False)
        self.b_filter.setEnabled(False)
        if self.items_found:
            page.p0list.setCurrentItem(self.items_found[0])
            self.founditem = 0
            if len(self.items_found) < len(self.parent.page.data.items()):
                self.b_next.setEnabled(True)
                self.b_filter.setEnabled(True)
            self.parent.sb.showMessage(self.parent.captions["I_#FOUND"].format(
                len(self.items_found)))
        else:
            self.parent.sb.showMessage(self.parent.captions["I_NOTFND"].format(text))

    def find_next(self):
        """to next search result
        """
        self.b_prev.setEnabled(True)
        if self.founditem < len(self.items_found) - 1:
            self.founditem += 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])
        else:
            self.parent.sb.showMessage(self.parent.captions["I_NONXT"])
            self.b_next.setEnabled(False)

    def find_prev(self):
        """to previous search result
        """
        self.b_next.setEnabled(True)
        if self.founditem == 0:
            self.parent.sb.showMessage(self.parent.captions["I_NOPRV"])
            self.b_prev.setEnabled(False)
        else:
            self.founditem -= 1
            self.parent.page.p0list.setCurrentItem(self.items_found[self.founditem])

    def filter(self):
        """filter shown items according to search text
        """
        if not self.items_found:
            return
        state = str(self.b_filter.text())
        text = str(self.find.currentText())
        item = self.parent.page.p0list.currentItem()
        self.reposition = item.text(0), item.text(1)
        if state == self.parent.captions['C_FILTER']:
            state = self.parent.captions['C_FLTOFF']
            self.filter_on = True
            self.parent.page.filtertext = text
            self.parent.page.olddata = self.parent.page.data
            self.parent.page.data = {ix: item for ix, item in enumerate(
                self.parent.page.data.values()) if text.upper() in item[self.zoekcol].upper()}
            self.b_next.setEnabled(False)
            self.b_prev.setEnabled(False)
            self.find.setEnabled(False)
        else:       # self.filter_on == True
            state = self.parent.captions['C_FILTER']
            self.filter_on = False
            self.parent.page.filtertext = ''
            self.parent.page.data = self.parent.page.olddata
            self.b_next.setEnabled(True)
            self.b_prev.setEnabled(True)
            self.find.setEnabled(True)
        self.parent.page.populate_list()
        for ix in range(self.parent.page.p0list.topLevelItemCount()):
            item = self.parent.page.p0list.topLevelItem(ix)
            if (item.text(0), item.text(1)) == self.reposition:
                self.parent.page.p0list.setCurrentItem(item)
                break
        self.b_filter.setText(state)
        if self.parent.page.data == self.parent.page.olddata:
            self.on_text_changed(text)  # reselect items_found after setting filter to off


class MainFrame(qtw.QMainWindow):
    """Hoofdscherm van de applicatie
    """
    def __init__(self, args):
        wid = 1140 if hkc.LIN else 688
        hig = 594
        super().__init__()
        self.resize(wid, hig)
        self.sb = self.statusBar()

        self.menu_bar = self.menuBar()
        ini = args.conf or hkc.CONF
        self.ini = hkc.read_settings(ini)
        self.readcaptions(self.ini['lang'])  # set up defaults
        if self.ini['plugins'] == []:
            self.show_empty_screen()
            return

        self.pluginfiles = {}
        self.title = self.captions["T_MAIN"]
        self.setWindowTitle(self.title)
        self.sb.showMessage(self.captions["T_HELLO"].format(self.captions["T_MAIN"]))
        self.book = ChoiceBook(self, self.ini['plugins'])
        self.setCentralWidget(self.book)
        self.page = self.book.pnl.currentWidget()
        start = 0
        if 'title' in self.ini and self.ini['title']:
            self.title = self.ini['title']
        if 'initial' in self.ini and self.ini['initial'] != '':
            start = [x for x, y in self.ini['plugins']].index(self.ini['initial'])
        self.book.sel.setCurrentIndex(start)
        self.setcaptions()

    def show_empty_screen(self):
        """what to do when there's no data to show
        """
        frm = qtw.QFrame(self)
        vbox = qtw.QVBoxLayout()
        text = qtw.QLabel(self.captions["EMPTY_CONFIG_TEXT"], self)
        vbox.addWidget(text)
        hbox = qtw.QHBoxLayout()
        hbox.addStretch()
        btn = qtw.QPushButton('Ok', self)
        btn.clicked.connect(self.close)
        btn.setDefault(True)
        hbox.addWidget(btn)
        hbox.addStretch()
        vbox.addLayout(hbox)
        frm.setLayout(vbox)
        self.setCentralWidget(frm)
        self.resize(640, 80)
        self.show()

    def setup_menu(self):
        """build menus and actions
        """
        self.menu_bar.clear()
        self._menuitems = {}  # []
        for title, items in (('M_APP', (
                                 ('M_SETT', ((
                                     ('M_TITLE', (self.m_title, '')),
                                     ('M_LOC', (self.m_loc, 'Ctrl+F')),
                                     ('M_LANG', (self.m_lang, 'Ctrl+L')),
                                     ('M_PREF', (self.m_pref, ''))), '')),
                                 ('M_EXIT', (self.m_exit, 'Ctrl+Q')), )),
                             ('M_TOOL', (
                                 ('M_SETT', ((
                                     ('M_COL', (self.m_col, '')),
                                     ('M_MISC', (self.m_tool, '')),
                                     ('M_ENTR', (self.m_entry, '')), ), '')),
                                 ('M_READ', (self.m_read, 'Ctrl+R')),
                                 ('M_RBLD', (self.m_rebuild, 'Ctrl+B')),
                                 ('M_SAVE', (self.m_save, 'Ctrl+S')), )),
                             ('M_HELP', (
                                 ('M_ABOUT', (self.m_about, 'Ctrl+H')), ))):
            menu = self.menu_bar.addMenu(self.captions[title])
            self._menuitems[title] = menu
            for sel in items:
                if sel == -1:
                    menu.addSeparator()
                    continue
                else:
                    sel, values = sel
                    callback, shortcut = values
                    if callable(callback):
                        act = self.create_menuaction(sel, callback, shortcut)
                        menu.addAction(act)
                        self._menuitems[sel] = act
                    else:
                        submenu = menu.addMenu(self.captions[sel])
                        self._menuitems[sel] = submenu
                        for sel, values in callback:
                            callback, shortcut = values
                            act = self.create_menuaction(sel, callback, shortcut)
                            submenu.addAction(act)
                            self._menuitems[sel] = act

    def create_menuaction(self, sel, callback, shortcut):
        """return created action w. some special cases
        """
        act = qtw.QAction(self.captions[sel], self)
        ## act.triggered.connect(functools.partial(callback, self))
        act.triggered.connect(callback)
        act.setShortcut(shortcut)
        if sel == 'M_READ':
            if not self.page.data:
                act.setEnabled(False)
        if sel == 'M_RBLD':
            try:
                act.setEnabled(bool(int(self.page.settings[hkc.SettType.RBLD.value])))
            except KeyError:
                act.setEnabled(False)
        elif sel == 'M_SAVE':
            try:
                act.setEnabled(bool(int(self.page.settings[hkc.SettType.RDEF.value])))
            except KeyError:
                act.setEnabled(False)
        return act

    # menu callbacks
    def m_read(self):
        """(menu) callback voor het lezen van de hotkeys

        vraagt eerst of het ok is om de hotkeys (opnieuw) te lezen
        zet de gelezen keys daarna ook in de gui
        """
        if not self.page.settings:
            hkd.show_message(self, 'I_ADDSET')
            return
        if not self.page.modified:
            if not hkd.ask_question(self, 'Q_NOCHG'):
                return
        self.page.readkeys()
        self.page.populate_list()

    def m_save(self):
        """(menu) callback voor het terugschrijven van de hotkeys

        vraagt eerst of het ok is om de hotkeys weg te schrijven
        vraagt daarna eventueel of de betreffende applicatie geherstart moet worden
        """
        if not self.page.modified:
            if not hkd.ask_question(self, 'Q_NOCHG'):
                return
        try:
            self.page.savekeys()
        except AttributeError:
            hkd.show_message(self, 'I_DEFSAV')
            return
        hkd.show_message(self, 'I_RSTRT')

    def m_title(self):
        """menu callback voor het aanpassen van de schermtitel
        """
        oldtitle = self.title
        newtitle, ok = qtw.QInputDialog.getText(self, oldtitle, self.captions["T_TITLE"],
                                                text=oldtitle)
        if ok == qtw.QDialog.Accepted:
            if newtitle != oldtitle:
                self.title = self.ini['title'] = newtitle
                hkc.change_setting('title', oldtitle, newtitle, self.ini['filename'])
                if not newtitle:
                    hkd.show_message(self, 'I_STITLE')
                    self.title = self.captions["T_MAIN"]
                self.set_title()

    def m_loc(self):
        """(menu) callback voor aanpassen van de bestandslocaties

        vraagt bij wijzigingen eerst of ze moeten worden opgeslagen
        toont dialoog met bestandslocaties en controleert de gemaakte wijzigingen
        (met name of de opgegeven paden kloppen)
        """
        # self.ini["plugins"] bevat de lijst met tools en csv locaties
        current_programs = [x for x, y in self.ini["plugins"]]
        current_paths = [y for x, y in self.ini["plugins"]]
        ok = hkd.FilesDialog(self).exec_()
        if ok == qtw.QDialog.Accepted:
            selection = self.book.sel.currentIndex()
            hkc.modify_settings(self.ini)

            # update the screen(s)
            # clear the selector and the stackedwidget while pairing up programs and windows
            # that need to be kept or replaced
            hlpdict = {}
            self.book.sel.clear()
            current_items = reversed([(x, y) for x, y in enumerate(current_programs)])
            new_programs = [x for x, y in self.ini["plugins"]]
            new_paths = [y for x, y in self.ini["plugins"]]
            for indx, program in current_items:  # we need to do this in reverse
                win = self.book.pnl.widget(indx)
                self.book.pnl.removeWidget(win)
                if program in new_programs:
                    hlpdict[program] = win  # keep the widget
                else:
                    win.close()  # lose the widget
            # add new ones, modify existing or leave them alone
            for indx, program in enumerate(new_programs):
                if program in current_programs:
                    # compare the new and the existing path
                    old_loc = current_paths[current_programs.index(program)]
                    new_loc = new_paths[new_programs.index(program)]
                    if new_loc == old_loc:  # unchanged
                        win = hlpdict[program]
                    else:  # take data from different location
                        win = HotkeyPanel(self.book, new_loc)
                else:  # new entry
                    loc = new_paths[indx]
                    if not os.path.exists(loc):
                        loc = os.path.join(hkc.BASE, loc)
                    win = HotkeyPanel(self.book, loc)
                self.book.sel.addItem(program)
                self.book.pnl.addWidget(win)
            if self.last_added:
                selection = self.book.sel.findText(self.last_added)
            if selection > len(self.ini['plugins']) - 1:
                selection -= 1
            self.book.sel.setCurrentIndex(selection)

    def m_rebuild(self):
        """rebuild csv data from (updated) settings
        """
        if not self.page.settings:
            hkd.show_message(self, 'I_ADDSET')
            return
        try:
            test = self.page._keys.buildcsv
        except AttributeError:
            hkd.show_message(self, 'I_DEFRBLD')
            return
        newdata = test(self)
        if newdata[0]:
            self.page.data = newdata[0]
            self.page.otherstuff = newdata[1]
            hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                         self.page.data, self.ini['lang'])
            self.page.populate_list()
            mld = 'keyboard definitions rebuilt'
        else:
            mld = 'No definition data'
            try:
                test = newdata[1]
            except IndexError:
                mld = 'No extra definition'
            mld = self.captions['I_#FOUND'].format(mld)
        hkd.show_message(self, text=mld)

    def m_tool(self):
        """define tool-specific settings
        """
        if not self.page.settings:
            self.page.settings = {x: '' for x in hkc.csv_settingnames}
        old_redef = bool(int(self.page.settings[hkc.SettType.RDEF.value]))
        dlg = hkd.ExtraSettingsDialog(self).exec_()
        if dlg == qtw.QDialog.Accepted:
            hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                         self.page.data, self.ini['lang'])
            test_redef = bool(int(self.page.settings[hkc.SettType.RDEF.value]))
            test_dets = bool(int(self.page.settings[hkc.SettType.DETS.value]))
            test_rbld = bool(int(self.page.settings[hkc.SettType.RBLD.value]))
            self._menuitems['M_SAVE'].setEnabled(test_redef)
            self._menuitems['M_RBLD'].setEnabled(test_rbld)
            indx = self.book.sel.currentIndex()
            win = self.book.pnl.widget(indx)
            if test_dets != self.page.has_extrapanel:
                self.page.has_extrapanel = test_dets
                newwin = HotkeyPanel(self.book, self.book.plugins[indx][1])
                self.book.pnl.insertWidget(indx, newwin)
                self.book.pnl.setCurrentIndex(indx)
                self.book.pnl.removeWidget(win)
            elif test_redef != old_redef and test_dets:
                win = self.book.pnl.currentWidget()
                win.set_extrascreen_editable(test_redef)

    def m_col(self):
        """define tool-specific settings: column properties
        """
        if not self.page.settings:
            hkd.show_message(self, 'I_ADDSET')
            return
        dlg = hkd.ColumnSettingsDialog(self).exec_()
        if dlg == qtw.QDialog.Accepted:
            new_pagedata = {}
            for key, value in self.page.data.items():
                newvalue = []
                for colinf in self.page.column_info:
                    test = colinf[-1]
                    if test == 'new':
                        newvalue.append('')
                    else:
                        newvalue.append(value[test])
                new_pagedata[key] = newvalue
            self.page.data = new_pagedata
            self.page.column_info = [x[:-1] for x in self.page.column_info]

            hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                         self.page.data, self.ini['lang'])
            if not self.page.data:
                return
            headers = [self.captions[col[0]] for col in self.page.column_info]
            self.page.p0list.setHeaderLabels(headers)
            self.book.find_loc.clear()
            self.book.find_loc.addItems(headers)
            hdr = self.page.p0list.header()
            hdr.setSectionsClickable(True)
            for indx, col in enumerate(self.page.column_info):
                hdr.resizeSection(indx, col[1])
            hdr.setStretchLastSection(True)
            self.page.populate_list()

    def m_entry(self):
        """manual entry of keyboard shortcuts
        """
        if not all((self.page.settings, self.page.column_info)):
            hkd.show_message(self, 'I_ADDCOL')
            return
        dlg = hkd.EntryDialog(self).exec_()
        if dlg == qtw.QDialog.Accepted:
            if self.page.data:
                hkc.writecsv(self.page.pad, self.page.settings, self.page.column_info,
                             self.page.data, self.ini['lang'])
                self.page.populate_list()

    def m_lang(self):
        """(menu) callback voor taalkeuze

        past de settings aan en leest het geselecteerde language file
        """
        # bepaal welke language files er beschikbaar zijn
        choices = [x.name for x in hkc.HERELANG.iterdir() if x.suffix == ".lng"]
        # bepaal welke er momenteel geactiveerd is
        oldlang = self.ini['lang']
        indx = choices.index(oldlang) if oldlang in choices else 0
        lang, ok = qtw.QInputDialog.getItem(self, self.title, self.captions["P_SELLNG"],
                                            choices, current=indx, editable=False)
        if ok:
            hkc.change_setting('lang', oldlang, lang, self.ini['filename'])
            self.ini['lang'] = lang
            self.readcaptions(lang)
            self.setcaptions()

    def m_about(self):
        """(menu) callback voor het tonen van de "about" dialoog
        """
        hkd.show_message(self, text='\n'.join(self.captions['T_ABOUT'].format(
            self.captions['T_SHORT'], hkc.VRS, hkc.AUTH,
            self.captions['T_LONG']).split(' / ')))

    def m_pref(self):
        """mogelijkheid bieden om een tool op te geven dat default getoond wordt
        """
        oldpref = self.ini.get("initial", None)
        oldmode = self.ini.get("startup", None)
        self.prefs = oldmode, oldpref
        ok = hkd.InitialToolDialog(self).exec_()
        if ok == qtw.QDialog.Accepted:
            mode, pref = self.prefs
            if mode:
                self.ini['startup'] = mode
                hkc.change_setting('startup', oldmode, mode, self.ini['filename'])
            if mode == 'Fixed':
                self.ini['initial'] = pref
                hkc.change_setting('initial', oldpref, pref, self.ini['filename'])

    def m_exit(self):
        """(menu) callback om het programma direct af te sluiten
        """
        self.exit()

    # other methods
    def exit(self):  # , e=None):
        """quit the application
        """
        if not self.page.exit():
            return
        self.close()

    def close(self):
        """extra actions to perform on closing
        """
        mode = self.ini.get("startup", '')
        pref = self.ini.get("initial", '')
        # when setting is 'fixed', don't remember a startup tool that is removed from the config
        # TODO: should actually be handled in the files definition dialog
        if mode == hkc.mode_f and pref not in [x[0] for x in self.ini['plugins']]:
            oldmode, mode = mode, hkc.mode_r
            print(oldmode, mode)
            self.ini['startup'] = mode
            hkc.change_setting('startup', oldmode, mode, self.ini['filename'])
        # when setting is 'remember', set the remembered tool to the current one
        if mode == hkc.mode_r:
            oldpref, pref = pref, self.book.sel.currentText()
            hkc.change_setting('initial', oldpref, pref, self.ini['filename'])
        super().close()

    def readcaptions(self, lang):
        """get captions from language file or settings
        """
        self.captions = hkc.readlang(lang)

    def set_title(self):
        """adjust title and modified flag
        """
        title = self.title
        if self.page.modified:
            title += ' ' + self.captions["T_MOD"]
        self.setWindowTitle(title)

    def setcaptions(self):
        """propagate captions to other parts of the application
        """
        self.set_title()
        for menu, item in self._menuitems.items():
            try:
                item.setTitle(self.captions[menu])
            except AttributeError:
                item.setText(self.captions[menu])
        self.book.setcaptions()
        self.page.setcaptions()


def main(args=None):
    """launch the application
    """
    app = qtw.QApplication(sys.argv)
    win = MainFrame(args)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv[1:])
