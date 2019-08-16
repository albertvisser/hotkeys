"""HotKeys main program - gui specific code - wxPython version
"""
# import os
# import sys
# import functools
from types import SimpleNamespace
import wx
import wx.adv
import wx.lib.mixins.listctrl as listmix
import editor.shared as shared
import editor.dialogs_wx as hkd


class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    """base class voor de listcontrol

    maakt het definiëren in de gui class wat eenvoudiger
    """
    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)


class DummyPage(wx.Panel):
    "simulate some HotKeyPanel functionality"
    def __init__(self, parent, message):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label=message))
        self.SetSizer(sizer)
        sizer.Fit(self)

    def exit(self):
        """simulate processing triggered by exit button
        """
        return True


class SingleDataInterface(wx.Panel, listmix.ColumnSorterMixin):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    voornamelijk nodig om de specifieke verwerkingen met betrekking tot de lijst
    bij elkaar en apart van de rest te houden
    definieert feitelijk een "custom widget"
    """
    def __init__(self, parent, master):
        super().__init__(parent.pnl)
        self.parent = parent
        self.master = master
        self.defchanged = False

    def setup_empty_screen(self, nodata, title):
        """build a subscreen with only a message
        """
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, label=nodata))
        self.SetSizer(sizer)
        self.title = title

    def setup_list(self):
        """add the list widget to the interface
        """
        self.p0list = MyListCtrl(self, size=(1140, 594), style=wx.LC_REPORT | wx.BORDER_SUNKEN |
                                                               # wx.LC_VRULES |
                                                               wx.LC_HRULES | wx.LC_SINGLE_SEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        if self.master.column_info:
            listmix.ColumnSorterMixin.__init__(self, 3)  # 5)
            for col, inf in enumerate(self.master.column_info):
                title, width = inf[:2]
                self.p0list.AppendColumn(self.master.captions[title])
                if col <= len(self.master.column_info):
                    self.p0list.SetColumnWidth(col, width)

            self.master.populate_list()

            # Now that the list exists we can init the other base class,
            # see wx/lib/mixins/listctrl.py
            self.itemDataMap = self.master.data  # nodig voor ColumnSorterMixin
            # self.SortListItems(0, True)

            self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected, self.p0list)
            self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_item_deselected, self.p0list)
            self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated, self.p0list)
            self.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_click, self.p0list)
            self.p0list.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)

        sizer.Add(self.p0list, 1, wx.EXPAND)

        if self.master.has_extrapanel:
            self.layout_extra_fields(sizer)

        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)
        # sizer.SetSizeHints(self)
        ## self.Layout()

    def set_title(self, title):
        """set screen title
        """
        self.master.parent.parent.gui.SetTitle(title)

    def clear_list(self):
        "reset listcontrol"
        self.p0list.DeleteAllItems()  # of ClearAll() - doet ook de kolommen
        # self.p0list.DeleteAllColumns()  - maar moeten de kolommen wel weg?

    def build_listitem(self, key):
        "create a new item for the list"
        # item = wx.ListItem()
        # item.SetData(key)
        itemlist = [key]  # item]
        return itemlist  # "new_item" is in dit geval een list

    def set_listitemtext(self, itemlist, indx, value):
        "set the text for a list item"
        # print('item', itemlist, 'index', indx, 'value', value)
        # "new_item" is in dit geval een list die verderop wordt toegevoegd aan de control
        # self.p0list.SetItem(item, indx, value)
        # if indx == 0:
        #     item = itemlist.pop()
        # else:
        #     item = wx.ListItem()
        # item.SetColumn(indx)
        # item.SetText(value)
        itemlist.append(value)
        return itemlist

    def add_listitem(self, itemlist):
        "add an item to the list"
        # "new_item" is in dit geval een list die verderop wordt toegevoegd aan de control
        key = itemlist.pop(0)
        indx = self.p0list.Append(itemlist)
        self.p0list.SetItemData(indx, key)

    def set_listselection(self, pos):
        "highlight the selected item in the list"
        self.p0list.Select(pos)

    def add_extra_fields(self):
        """fields showing details for selected keydef, to make editing possible
        """
        self.screenfields = []
        self._box = box = wx.Panel(self)
        # frameheight = 90
        # try:
        #     frameheight = self.master.reader.get_frameheight()  # user exit
        # except AttributeError:
        #     pass
        # box.setMaximumHeight(frameheight)

        if 'C_KEY' in self.master.fields:
            self.lbl_key = wx.StaticText(box, label=self.master.captions['C_KTXT'] + " ")
            if self.master.keylist is None:
                ted = wx.TextCtrl(box, size=(90, -1))
                ted.Bind(wx.EVT_TEXT, self.on_text)
                self.screenfields.append(ted)
                self.txt_key = ted
            else:
                cb = wx.ComboBox(box, size=(90, -1), style=wx.CB_DROPDOWN,
                                 choices=self.master.keylist)  # niet sorteren
                cb.Bind(wx.EVT_COMBOBOX, self.on_combobox)
                self.screenfields.append(cb)
                self.cmb_key = cb

        if 'C_MODS' in self.master.fields:
            for ix, x in enumerate(('M_CTRL', 'M_ALT', 'M_SHFT', 'M_WIN')):
                cb = wx.CheckBox(box, self.master.captions[x].join(("+ ", "")))
                cb.SetValue(False)
                self.screenfields.append(cb)
                cb.Bind(wx.EVT_CHECKBOX, self.on_checkbox)
                if ix == 0:
                    self.cb_ctrl = cb
                elif ix == 1:
                    self.cb_alt = cb
                elif ix == 2:
                    self.cb_shift = cb
                elif ix == 3:
                    self.cb_win = cb

        if 'C_CNTXT' in self.master.fields:
            self.lbl_context = wx.StaticText(box, label=self.master.captions['C_CNTXT'])
            cb = wx.ComboBox(box, size=(110, -1), style=wx.CB_READONLY,
                             choices=self.master.contextslist)
            cb.Bind(wx.EVT_COMBOBOX, self.on_combobox)
            self.screenfields.append(cb)
            self.cmb_context = cb

        if 'C_CMD' in self.master.fields:
            self.txt_cmd = wx.StaticText(box, label=self.master.captions['C_CTXT'] + " ")
            cb = wx.ComboBox(self, size=(150, -1), style=wx.CB_READONLY)
            if 'C_CNTXT' not in self.master.fields:  # load on choosing context
                cb.SetItems(self.master.commandslist)
            cb.Bind(wx.EVT_COMBOBOX, self.on_combobox)
            self.screenfields.append(cb)
            self.cmb_commando = cb

        self.b_save = wx.Button(box, label=self.master.captions['C_SAVE'])
        self.b_save.Enable(False)
        self.b_save.Bind(wx.EVT_BUTTON, self.on_update)
        self.b_del = wx.Button(box, label=self.master.captions['C_DEL'])
        self.b_del.Enable(False)
        self.b_del.Bind(wx.EVT_BUTTON, self.on_delete)
        self._savestates = (False, False)

        if 'C_DESC' in self.master.fields:
            self.txt_oms = wx.TextCtrl(box, style=wx.TE_MULTILINE | wx.TE_READONLY)

        # FIXME: even wachten tot plugin ook is aangepast
        # try:
        #     self.master.reader.add_extra_fields(self, box)  # user exit
        # except AttributeError:
        #     pass

        self.set_extrascreen_editable(bool(int(self.master.settings['RedefineKeys'])))

    def set_extrascreen_editable(self, switch):
        """open up fields in extra screen when applicable
        """
        for widget in self.screenfields:
            widget.Enable(switch)
        ## if 'C_CMD' in self.fields:
        if switch:
            state_s, state_d = self._savestates
        else:
            self._savestates = (self.b_save.IsEnabled(), self.b_del.IsEnabled())
            state_s, state_d = False, False
        self.b_save.Enable(state_s)
        self.b_del.Enable(state_d)

    def layout_extra_fields(self, sizer):
        """add the extra fields to the layout
        """
        bsizer = wx.BoxSizer(wx.VERTICAL)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        if 'C_KEY' in self.master.fields:
            sizer3 = wx.BoxSizer(wx.HORIZONTAL)
            sizer3.Add(self.lbl_key, 0)
            if self.master.keylist is None:
                sizer3.Add(self.txt_key, 0)
            else:
                sizer3.Add(self.cmb_key, 0)
            sizer2.Add(sizer3, 0)

        if 'C_MODS' in self.master.fields:
            sizer3 = wx.BoxSizer(wx.HORIZONTAL)
            sizer3.Add(self.cb_ctrl, 0)
            sizer3.Add(self.cb_alt, 0)
            sizer3.Add(self.cb_shift, 0)
            sizer3.Add(self.cb_win, 0)
            sizer2.Add(sizer3, 0)

        sizer1.Add(sizer2, 0)
        if 'C_CNTXT' in self.master.fields:
            sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer2.Add(self.lbl_context, 0)
            sizer2.Add(self.cmb_context, 0)
            sizer1.Add(sizer2, 0)

        if 'C_CMD' in self.master.fields:
            sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer2.Add(self.txt_cmd, 0)
            sizer2.Add(self.cmb_commando, 0)
            sizer1.Add(sizer2, 0)

        # FIXME: even wachten tot plugin ook is aangepast
        # try:
        #     self.master.reader.layout_extra_fields_topline(self, sizer1)  # user exit
        # except AttributeError:
        #     pass

        sizer1.Add(self.b_save, 0)
        sizer1.Add(self.b_del, 0)
        bsizer.Add(sizer1, 0)

        # FIXME: even wachten tot plugin ook is aangepast
        # try:
        #     test = self.master.reader.layout_extra_fields_nextline
        # except AttributeError:
        #     pass
        # else:
        #     sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        #     self.master.reader.layout_extra_fields_nextline(self, sizer1)  # user exit
        #     bsizer.Add(sizer1, 0)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        if 'C_DESC' in self.master.fields:
            sizer2 = wx.BoxSizer(wx.VERTICAL)
            sizer2.Add(self.txt_oms, 1, wx.EXPAND)
            sizer1.Add(sizer2, 1, wx.EXPAND)

        # FIXME: even wachten tot plugin ook is aangepast
        # try:
        #     self.master.reader.layout_extra_fields(self, sizer1)  # user exit
        # except AttributeError:
        #     pass

        bsizer.Add(sizer1, 0)

        self._box.SetSizer(bsizer)
        sizer.Add(self._box)

    def captions_extra_fields(self):
        """to be called on changing the language
        """
        if 'C_KEY' in self.master.fields:
            self.lbl_key.SetLabel(self.master.captions['C_KTXT'])
        if 'C_MODS' in self.master.fields:
            self.cb_win.SetLabel(self.master.captions['M_WIN'].join(("+", "  ")))
            self.cb_ctrl.SetLabel(self.master.captions['M_CTRL'].join(("+", "  ")))
            self.cb_alt.SetLabel(self.master.captions['M_ALT'].join(("+", "  ")))
            self.cb_shift.SetLabel(self.master.captions['M_SHFT'].join(("+", "  ")))
        if 'C_CNTXT' in self.master.fields:
            self.lbl_context.SetLabel(self.master.captions['C_CNTXT'] + ':')
        if 'C_CMD' in self.master.fields:
            self.txt_cmd.SetLabel(self.master.captions['C_CTXT'])
        self.b_save.SetLabel(self.master.captions['C_SAVE'])
        self.b_del.SetLabel(self.master.captions['C_DEL'])
        # FIXME: even wachten tot plugin ook is aangepast
        # try:
        #     self.master.reader.captions_extra_fields(self)  # user exit
        # except AttributeError:
        #     pass

    def GetListCtrl(self):
        """ten behoeve van de columnsorter mixin"""
        return self.p0list

    def GetSortImages(self):
        """ten behoeve van de columnsorter mixin"""
        return (self.sm_dn, self.sm_up)

    def AfterSort(self):
        """ na het sorteren moeten de regels weer om en om gekleurd worden"""
        kleur = False
        for key in range(len(self.data.items)):
            if kleur:
            #     self.p0list.SetItemBackgroundColour(key, wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU))
            # else:
                self.p0list.SetItemBackgroundColour(key, wx.SystemSettings.GetColour(wx.SYS_COLOUR_INFOBK))
            kleur = not kleur

    def on_column_click(self, event):  # FIXME: do we need this for wx version?
        """callback op het klikken op een kolomtitel
        """
        print("on_column_click: %d\n" % event.GetColumn())
        ## self.parent.sorter = self.GetColumnSorter()
        event.Skip()

    def on_doubleclick(self, event):
        """callback op dubbelklikken op een kolomtitel
        """
        print("on_doubleclick item %s\n" % self.p0list.GetItemText(self.current_item))
        event.Skip()

    def on_text(self, event):  # , ted, text):
        """on changing a text entry
        """
        ted = event.GetEventWidget()
        text = ted.GetValue()
        print('in on_text with', ted, text)
        if self.master.initializing_screen:
            return
        # text = str(text)    # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan
        #                     # de callback soms fout? Of is het Py3 vs Py2?
        # hlp = ted.text()
        # if text != hlp:
        #     text = hlp
        self.defchanged = False
        if 'C_KEY' in self.master.fields:
            if text == self._origdata[self.master.ix_key]:
                self.defchanged = True
                self.b_save.Enable(True)
            elif text == self._origdata[self.master.ix_key]:
                self.defchanged = False
                self.b_save.Enable(False)

    def on_combobox(self, event):  # , cb, text):
        """callback op het gebruik van een combobox

        zorgt ervoor dat de buttons ge(de)activeerd worden
        """
        cb = event.GetEventWidget()
        text = cb.GetValue()
        print('in on_combobox with', cb, text)
        if self.master.initializing_screen:
            return
        # text = str(text)    # ineens krijg ik hier altijd "<class 'str'>" voor terug? Is de bind aan
        #                     # de callback soms fout? Of is het Py3 vs Py2?
        # hlp = cb.currentText()
        # if text != hlp:
        #     text = hlp
        self.defchanged = False
        try:
            test_key = bool(self.cmb_key)  # moet/kan dit met GetValue?
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
            keyitemindex = self.master.ix_key
            if text != self._origdata[keyitemindex]:
                self._newdata[keyitemindex] = text
                if not self.initializing_keydef:
                    self.defchanged = True
                    if 'C_CMD' in self.fields:
                        self.b_save.Enable(True)
            elif str(self.cmb_commando.GetText()) == self._origdata[keyitemindex]:  # UNDEF
                self.defchanged = False
                if 'C_CMD' in self.fields:
                    self.b_save.Enable(False)
        elif test_cnx and cb == self.cmb_context:
            if text != self._origdata[self.ix_cntxt]:
                context = self._origdata[self.ix_cntxt] = self.cmb_context.GetText()
                self.cmb_commando.clear()
                # if self.master.contextactionsdict:
                #     actionslist = self.master.contextactionsdict[context]
                # else:
                #     actionslist = self.master.commandslist
                actionslist = self.master.contextactionsdict[context] or self.master.commandslist
                self.cmb_commando.addItems(actionslist)
                if not self.initializing_keydef:
                    self.defchanged = True
                    if 'C_CMD' in self.fields:
                        self.b_save.Enable(True)
            elif str(self.cmb_commando.GetText()) == self._origdata[self.ix_cntxt]:
                self.defchanged = False
                if 'C_CMD' in self.fields:
                    self.b_save.Enable(False)
        elif test_cmd and cb == self.cmb_commando:
            cmditemindex = self.ix_cmd
            if text != self._origdata[cmditemindex]:
                self._newdata[cmditemindex] = text
                try:
                    self.txt_oms.SetText(self.master.descriptions[text])
                except KeyError:
                    self.txt_oms.SetText(self.captions['M_NODESC'])
                if not self.initializing_keydef:
                    self.defchanged = True
                    if 'C_CMD' in self.fields:
                        self.b_save.Enable(True)
            elif str(self.cmb_key.currentText()) == self._origdata[cmditemindex]:
                if 'C_CMD' in self.fields:
                    self.b_save.Enable(False)
        else:
            try:
                self.master.reader.on_combobox(self, cb, text)  # user exit
            except AttributeError:
                pass

    def on_checkbox(self, event):  # cb, state):
        """callback op het gebruik van een checkbox

        voorlopig alleen voor de modifiers
        """
        cb = event.GetEventWidget()
        state = cb.GetValue()
        print('in on_checkbox', cb, state)
        if self.master.initializing_screen:
            return
        ## state = bool(state)
        for win, indx in zip((self.cb_shift, self.cb_ctrl, self.cb_alt, self.cb_win),
                             self.master.ix_mods):
            if cb == win and state != self._origdata[indx]:
                self._newdata[indx] = state
                if not self.initializing_keydef:
                    self.defchanged = True
                    if 'C_CMD' in self.fields:
                        self.b_save.Enable(True)
                break
        else:
            states = [self.cb_shift.isChecked(), self.cb_ctrl.isChecked(),
                      self.cb_alt.isChecked(), self.cb_win.isChecked()]
            if states == [self._origdata[x] for x in self.master.ix_mods]:
                self.defchanged = False
                if 'C_CMD' in self.fields:
                    self.b_save.Enable(False)

    def on_item_selected(self, event):
        """callback op het selecteren van een item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        item = event.GetItem()
        print('in on_item_selected', event, item)
        # check: is het überhaupt nodig?
        if not self.master.has_extrapanel:  # dit is hier wel voldoende
            return
        # check: zitten we niet te vroeg in het proces?
        if not item:  # bv. bij p0list.clear()
            return
        # if self.master.initializing_screen:
        #     self.refresh_extrascreen(event.GetItem())  # newitem)
        #     self.master.initializing_screen = False
        #     return
        # seli = self.p0list.GetItemData(event.GetEventObject().GetFirstSelected())  # Index())
        ## print "Itemselected",seli,self.data[seli]
        # self.refresh_extrascreen(seli)
        self.refresh_extrascreen(item)  # newitem)
        # self.on_item_selected_2(seli)
        event.Skip()

    def on_item_deselected(self, event):
        """callback op het niet meer geselecteerd zijn van een item

        er wordt gevraagd of de key definitie moet worden bijgewerkti
        """
        olditem = event.GetItem()
        print('in on_item_deselected', event, olditem)
        return  # voorlopig verder negeren
        # TODO: kijken wat hiervan aan GUI onafhankelijke code kan worden uitgefilterd
        # check 1: zitten we niet te vroeg in het proces?
        if self.master.initializing_screen:
            return
        if not olditem:  # bv. bij p0list.clear()
            return
        #  check 2: kunnen we wijzigen (hebben we een extra schermdeel is niet voldoende)
        ## if not self.master.has_extrapanel:
            ## return
        if not bool(self.parent.master.page.settings[shared.SettType.RDEF.value]):
            return

        # indx = event.GetIndex()  # EventObject()
        # seli = self.p0list.GetItemData(indx)  # test.GetFirstSelected())  # Index())

        # bepalen wat er aan de hand is
        other_item = other_cntxt = other_cmd = False
        if 'C_KEYS' in self.master.fields:
            origkey = self._origdata[self.master.ix_key]
            key = self._newdata[self.master.ix_key]
            other_item = key != origkey
        if 'C_MODS' in self.master.fields:
            origmods = ''.join([y for x, y in zip(self.master.ix_mods, ('WCAS'))
                                if self._origdata[x]])
            mods = ''.join([y for x, y in zip(self.master.ix_mods, ('WCAS'))
                            if self._newdata[x]])
            other_item = other_item or mods != origmods
        if 'C_CMD' in self.master.fields:
            origcmd = self._origdata[self.ix_cmd]
            cmnd = self._newdata[self.ix_cmd]
            other_cmd = cmnd != origcmd
        if 'C_CNTXT' in self.master.fields:
            origcntxt = self._origdata[self.ix_cntxt]
            context = self._newdata[self.ix_cntxt]
            other_cntxt = context != origcntxt
        # deze afvraging wordt lastig want in deseleced weet ik nog niet wat new_item wordt
        cursor_moved = True if newitem != olditem and olditem is not None else False
        any_change = other_item or other_cmd or other_cntxt

        # kijken of de selectie al bestaat
        found = False
        for number, item in self.master. data.items():
            keymatch = modmatch = cntxtmatch = True
            if 'C_KEYS' in self.master.fields and item[0] != key:
                keymatch = False
            if 'C_MODS' in self.master.fields and item[1] != mods:
                modmatch = False
            if 'C_CNTXT' in self.master.fields and item[2] != context:
                cntxtmatch = False
            if keymatch and modmatch and cntxtmatch:
                found = True
                indx = number
                break

        # vragen wat er moet gebeuren
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
            item = self.p0list.currentItem()                # TODO nog omschrijven
            pos = self.p0list.indexOfTopLevelItem(item)     # deze ook
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
            self.master.modified = True
            self._origdata = self.init_origdata
            if 'C_KEY' in self.master.fields:
                self._origdata[self.master.ix_key] = key
            if 'C_MODS' in self.master.fields:
                for mod, indx in zip(('WCAS'), self.master.ix_mods):
                    self._origdata[indx] = mod in mods
            if 'C_CMD' in self.master.fields:
                self._origdata[self.ix_cmd] = cmnd
            if 'C_CNTXT' in self.master.fields:
                self._origdata[self.ix_cntxt] = context
            try:
                self.reader.on_extra_selected(self, item)  # user exit
            except AttributeError:
                pass
            # newitem = self.p0list.topLevelItem(pos)
            self.populate_list(pos)    # refresh

    def on_item_activated(self, event):
        """callback op het activeren van een item (onderdeel van het selecteren)
        """
        print('in on_item_activated', event)
        self.current_item = event.GetItem()  # GetEventIndex()

    def on_update(self, event):
        """callback for editing kb shortcut
        """
        print('in on_update', event)
        self.do_modification()
        self.p0list.SetFocus()

    def on_delete(self, event):
        """callback for deleting kb shortcut
        """
        print('in on_delete', event)
        self.do_modification(delete=True)
        self.p0list.SetFocus()

    def refresh_extrascreen(self, selitem):
        """show new values after changing kb shortcut
        """
        print('in refresh_extrascreen', selitem)
        if not selitem:  # bv. bij p0list.clear()
            return
        seli = selitem.GetData()
        keydefdata = self.master.data[seli]
        if 'C_CMD' in self.master.fields:
            self.b_save.Enable(False)
            self.b_del.Enable(False)
        self._origdata = self.master.init_origdata[:]
        for indx, item in enumerate(keydefdata):
            if self.master.column_info[indx][0] == 'C_KEY':
                key = item
                if self.master.keylist is None:
                    self.txt_key.SetText(key)
                else:
                    # ix = self.master.keylist.index(key)
                    self.cmb_key.SetString(key)
                self._origdata[self.master.ix_key] = key
            elif self.master.column_info[indx][0] == 'C_MODS':
                mods = item
                self.cb_shift.SetValue(False)
                self.cb_ctrl.SetValue(False)
                self.cb_alt.SetValue(False)
                self.cb_win.SetValue(False)
                for x, y, z in zip('SCAW',
                                   self.master.ix_mods,
                                   (self.cb_shift, self.cb_ctrl, self.cb_alt, self.cb_win)):
                    if x in mods:
                        self._origdata[y] = True
                        z.SetValue(True)
            elif self.master.column_info[indx][0] == 'C_TYPE':
                soort = item
                if soort == 'U':
                    self.b_del.Enable(True)
            elif self.master.column_info[indx][0] == 'C_CNTXT' and self.master.contextslist:
                context = item
                # ix = self.master.contextslist.index(context)
                # self.cmb_context.setCurrentIndex(ix)
                self.cmb_context.SetString(context)
                self._origdata[self.ix_cntxt] = context
            elif self.master.column_info[indx][0] == 'C_CMD' and self.master.commandslist:
                command = item
                if 'C_CNTXT' in self.fields:
                    self.cmb_commando.Clear()
                    context = self.cmb_context.GetStringSelection()  # currentText()
                    # if self.contextactionsdict:
                    #     actionslist = self.master.contextactionsdict[context]
                    # else:
                    #     actionslist = self.master.commandslist
                    actionslist = self.master.contextactionsdict[context] or self.master.commandslist
                    self.cmb_commando.SetItems(actionslist)
                    # try:
                    #     ix = actionslist.index(command)
                    # except ValueError:
                    #     ix = -1
                # else:
                    # ix = self.master.commandslist.index(command)
                # if ix >= 0:
                #     self.cmb_commando.setCurrentIndex(ix)
                self.cmb_commando.SetString(command)
                self._origdata[self.ix_cmd] = command
            elif self.master.column_info[indx][0] == 'C_DESC':
                oms = item
                self.txt_oms.SetValue(oms)
            else:
                try:
                    self.master.reader.vul_extra_details(self, indx, item)  # user exit
                except AttributeError:
                    pass
        self._newdata = self._origdata[:]

    def do_modification(self, delete=False):
        """currently this only works for tcmdrkys - or does it?
        """
        # TODO uitzetten overbodig maken
        print("in do_modification - Aanpassen uitgezet, werkt nog niet voor alles")
        return
        # zou dit niet hetzelfde moeten zijn als het laatste stuk in on_item_deselected
        #   (onder de conditie "make_change")?
        item = self.p0list.currentItem()                # TODO nog omschrijven
        pos = self.p0list.indexOfTopLevelItem(item)     # deze ook
        if delete:
            indx = item.data(0, core.Qt.UserRole)       # deze ook
            if self.captions["{:03}".format(indx)] == 'C_TYPE':
                if self.data[indx][1] == "S":  # can't delete standard key
                    hkd.show_message(self.parent, 'I_STDDEF')
                    return
            elif self.captions["{:03}".format(indx)] == 'C_KEY':
                if self.data[indx][0] in self.defkeys:  # restore standard if any
                    cmnd = self.master.defkeys[self.data[indx][0]]
                    if cmnd in self.master.omsdict:
                        oms = self.master.omsdict[cmnd]
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
            self.master.populate_list(pos)    # refresh
        else:
            self.on_item_selected(item, item)  # , from_update=True)

    # hulproutine t.b.v. managen column properties

    def refresh_headers(self, headers):
        "apply changes in the column headers"
        self.p0list.setHeaderLabels(headers)
        hdr = self.p0list.header()
        hdr.setSectionsClickable(True)
        for indx, col in enumerate(self.master.column_info):
            hdr.resizeSection(indx, col[1])
        hdr.setStretchLastSection(True)

    def enable_buttons(self, state=True):
        """anders wordt de gelijknamige methode van de Panel base class geactiveerd"""


class TabbedInterface(wx.Panel):
    """ Als wx.NoteBook, maar met selector in plaats van tabs
    """
    def __init__(self, parent, master):
        super().__init__(parent)
        self.parent = parent
        self.master = master

    def setup_selector(self):
        "create the selector"
        self.sel = wx.ComboBox(self, size=(140, -1), style=wx.CB_READONLY)
        self.sel.Bind(wx.EVT_COMBOBOX, self.after_changing_page)
        # als ik echt met een choicebook werkte, kon ik deze *twee*  gebruiken:
        # self.book.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.OnPageChanged)
        # self.book.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.pnl = wx.Simplebook(self)
        # self.pnl = wx.Choicebook(self)

    def setup_search(self):
        "add the search widgets to the interface"
        self.find_loc = wx.ComboBox(self, size=(140, -1), style=wx.CB_READONLY)
        self.find = wx.ComboBox(self, size=(140, -1), style=wx.CB_DROPDOWN)
        self.find.Bind(wx.EVT_TEXT, self.after_changing_text)
        self.b_next = wx.Button(self, label='next')
        self.b_next.Bind(wx.EVT_BUTTON, self.master.find_next)
        self.b_next.Enable(False)
        self.b_prev = wx.Button(self, label='prev')
        self.b_prev.Bind(wx.EVT_BUTTON, self.master.find_prev)
        self.b_prev.Enable(False)
        self.b_filter = wx.Button(self, label=self.parent.editor.captions['C_FILTER'])
        self.b_filter.Bind(wx.EVT_BUTTON, self.master.filter)
        self.b_filter.Enable(False)
        self.filter_on = False

    def add_subscreen(self, win):
        "add a screen to the tabbed widget"
        self.pnl.AddPage(win.gui, '')

    def add_to_selector(self, txt):
        "add an option to the selector"
        self.sel.Append(txt)

    def format_screen(self):
        "realize the screen"
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddSpacer(10)
        self.sel_text = wx.StaticText(self, label='', size=(80, -1))
        hbox.Add(self.sel_text, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.sel, 0)
        hbox.Add(wx.StaticText(self, label=''), 1, wx.EXPAND)
        self.find_text = wx.StaticText(self, label='', size=(80, -1))
        hbox.Add(self.find_text, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.find_loc, 0)
        hbox.Add(wx.StaticText(self, label=' : '), 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.find, 0)
        hbox.Add(self.b_filter, 0)
        hbox.Add(self.b_next, 0)
        hbox.Add(self.b_prev, 0)
        hbox.AddSpacer(10)
        vbox.Add(hbox, 0, wx.EXPAND)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.pnl, 0)
        vbox.Add(hbox, 0)
        self.SetAutoLayout(True)
        self.SetSizer(vbox)
        vbox.Fit(self)
        # vbox.SetSizeHints(self)
        self.setcaptions()
        self.Show()

    def setcaptions(self):
        """update captions according to selected language
        """
        self.b_next.SetLabel(self.parent.editor.captions['C_NEXT'])
        self.b_prev.SetLabel(self.parent.editor.captions['C_PREV'])
        self.sel_text.SetLabel(self.parent.editor.captions['C_SELPRG'])
        self.find_text.SetLabel(self.parent.editor.captions['C_FIND'])
        if self.filter_on:
            self.b_filter.SetLabel(self.parent.editor.captions['C_FLTOFF'])
        else:
            self.b_filter.SetLabel(self.parent.editor.captions['C_FILTER'])
        try:
            self.parent.b_exit.SetLabel(self.parent.editor.captions['C_EXIT'])
        except AttributeError:  # exit button bestaat nog niet tijdens initialisatie
            pass

    def after_changing_page(self, event):
        """callback for change in tool page selector
        """
        self.master.on_page_changed(event.GetEventObject().GetSelection())  # GetValue())  # for now

    # used by on_page_changed
    def get_panel(self):
        return self.pnl.GetCurrentPage()

    def get_selected_tool(self):
        return self.sel.GetStringSelection()

    def set_selected_panel(self, indx):
        self.pnl.SetSelection(indx)

    def update_search(self, items):
        self.find_loc.Clear()
        self.find_loc.AppendItems(items)
        self.find_loc.SetSelection(len(items) - 1)
        if self.master.page.filtertext:
            self.find.SetValue(self.master.page.filtertext)
            self.b_filter.SetText(self.parent.captions['C_FLTOFF'])
            self.b_filter.Enable(True)
        else:
            self.find.SetValue('')
            self.find.Enable(True)
            self.b_next.Enable(False)
            self.b_prev.Enable(False)
            self.b_filter.Enable(False)

    def after_changing_text(self, event):
        """callback for change in search text
        """
        text = event.GetEventObject().GetValue()
        if text:
            self.master.on_text_changed(text)

    # used by on_text_changed
    def get_search_col(self):
        return self.find_loc.GetStringSelection()

    def find_items(self, page, text):
        # hier moet ik nog iets moois op vinden:
        # page.gui.p0list.findItems(text, core.Qt.MatchContains, self.zoekcol)
        return []

    def init_search_buttons(self):
        self.enable_search_buttons(next=False, prev=False, filter=False)

    def set_selected_keydef_item(self, page, index):
        page.p0list.SetSelectedItem(self.items_found[index])

    def enable_search_buttons(self, next=None, prev=None, filter=None):
        if next is not None:
            self.b_next.Enable(next)
        if prev is not None:
            self.b_filter.Enable(prev)
        if filter is not None:
            self.b_filter.Enable(filter)

    # used by filter
    def get_filter_wanted(self):
        return str(self.b_filter.GetValue())

    def get_search_text(self):
        return str(self.find.GetStringSelection())

    def get_found_keydef_position(self):
        # dit is nog de qt variant
        item = self.master.page.gui.p0list.GetSelection()  # dit moet anders - p0list is een
        return item.text(0), item.text(1)  # dit moet anders      - wx.ListCtrl subclass

    def enable_search_text(self, value):
        self.find.Enable(value)

    def set_found_keydef_position(self):
        # dit is nog de qt variant
        for ix in range(self.master.page.gui.p0list.topLevelItemCount()):  # dit moet anders
            item = self.master.page.gui.p0list.topLevelItem(ix)  # dit moet anders
            if (item.text(0), item.text(1)) == self.reposition:  # dit moet anders
                self.master.page.gui.p0list.setCurrentItem(item)  # dit moet anders
                break

    def set_filter_wanted(self, state):
        self.b_filter.SetValue(state)

    def set_selected(self, selection):
        "set the new selection index"
        self.sel.SetSelection(selection)


class Gui(wx.Frame):
    """Hoofdscherm van de applicatie"""
    def __init__(self, parent=None):
        self.editor = parent
        self.app = wx.App()
        wid = 1140 if shared.LIN else 688
        hig = 594
        super().__init__(None, size=(wid, hig), style=wx.DEFAULT_FRAME_STYLE |
                                                      # wx.BORDER_SIMPLE |
                                                      wx.NO_FULL_REPAINT_ON_RESIZE)
        self.sb = self.CreateStatusBar()
        self.menu_bar = wx.MenuBar()
        self.menuitems = {}

    def show_empty_screen(self):
        """what to do when there's no data to show
        """
        message = self.editor.captions["EMPTY_CONFIG_TEXT"]
        self.editor.book = SimpleNamespace()
        self.editor.book.gui = DummyPage(self, message)
        self.editor.book.page = SimpleNamespace()
        self.editor.book.page.gui = self.editor.book.gui
        self.SetSize(640, 80)

    def go(self):
        "build and show the interface"
        self.SetMenuBar(self.menu_bar)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.editor.book.gui, 1, wx.EXPAND | wx.ALL, 5)
        self.b_exit = wx.Button(self, label=self.editor.captions['C_EXIT'])
        self.b_exit.Bind(wx.EVT_BUTTON, self.editor.exit)
        sizer.Add(self.b_exit, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        # sizer.SetSizeHints(self)
        self.Show(True)
        self.app.MainLoop()

    def set_window_title(self, title):
        "show a title in the titlebar"
        self.SetTitle(title)

    def statusbar_message(self, message):
        "show a message in the statusbar"
        self.sb.SetStatusText(message)

    def setup_tabs(self):
        """build the tabbed widget into the interface

        for compatibility - has already happened elsewhere in the application
        """

    def setup_menu(self):
        """build menus and actions
        """
        print('in setup_menu')
        has_items = bool(self.menu_bar.GetMenus())
        ix = 0
        for title, items in self.editor.get_menudata():
            menu = wx.Menu()
            for sel in items:
                if sel == -1:
                    menu.AppendSeparator()
                else:
                    sel, value = sel
                    callback, shortcut = value
                    if callable(callback):
                        menutext = '\t'.join((self.editor.captions[sel], shortcut))
                        item = wx.MenuItem(None, -1, text=menutext)
                        self.menuitems[sel] = item, shortcut
                        menu.Append(item)
                        self.Bind(wx.EVT_MENU, callback, id=item.GetId())
                    else:
                        submenu = wx.Menu()
                        for selitem, values in callback:
                            callback_, shortcut = values
                            menutext = '\t'.join((self.editor.captions[selitem], shortcut))
                            item = wx.MenuItem(None, -1, text=menutext)
                            self.menuitems[selitem] = item, shortcut
                            submenu.Append(item)
                            self.Bind(wx.EVT_MENU, callback_, id=item.GetId())
                        menu.AppendSubMenu(submenu, self.editor.captions[sel])
                        self.menuitems[sel] = submenu, ''
            if has_items:
                oldmenu, menu = menu, self.menu_bar.Replace(ix, menu, self.editor.captions[title])
                oldmenu.Destroy()
            else:
                self.menu_bar.Append(menu, self.editor.captions[title])
            self.menuitems[title] = menu, ''
            ix += 1

    def setcaptions(self):
        "set title for menuitem or action"
        for menu, item in self.menuitems.items():
            item, shortcut = item
            shared.log(item, always=True)
            try:
                shared.log('trying to change menu title to' +  self.editor.captions[menu],
                           always=True)
                item.SetTitle(self.editor.captions[menu])
            except AttributeError:
                shared.log('changing menu item title', always=True)
                item.SetText('\t'.join((self.editor.captions[menu], shortcut)))
           #  else:
           #      self.menu_bar.SetMenuLabel(['M_APP', 'M_SETT'].index(menu), self.editor.captions[menu])

    def close(self, event=None):
        """applicatie afsluiten"""
        self.Close(True)
