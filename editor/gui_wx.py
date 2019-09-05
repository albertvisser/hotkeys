"""HotKeys main program - gui specific code - wxPython version
"""
# import os
# import sys
# import functools
import io
import wx
import wx.adv
import wx.lib.mixins.listctrl as listmix
from wx.lib.embeddedimage import PyEmbeddedImage
import editor.shared as shared


def getbitmap(data):
    "return bitmap created from PNG data - the old way using textIO"
    return wx.BitmapFromImage(wx.ImageFromStream(io.StringIO(data)))


class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):
    """base class voor de listcontrol

    maakt het definiëren in de gui class wat eenvoudiger
    """
    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ListRowHighlighter.__init__(self)


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
        self.olditem = None

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
        imglist = wx.ImageList(16, 16)

        # ik dacht dat ik dit netjes gekopieerd had maar als ik op een kolomheader klik
        # krijg ik toch een segfault
        # ook nadat ik de volgorde van al dit gelijk maak aan die in de demo
        smalluparrow = PyEmbeddedImage(
            b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAADxJ"
            b"REFUOI1jZGRiZqAEMFGke2gY8P/f3/9kGwDTjM8QnAaga8JlCG3CAJdt2MQxDCAUaOjyjKMp"
            b"cRAYAABS2CPsss3BWQAAAABJRU5ErkJggg==")
        self.sm_up = imglist.Add(smalluparrow.GetBitmap())

        smalldnarrow = PyEmbeddedImage(
            b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEhJ"
            b"REFUOI1jZGRiZqAEMFGke9QABgYGBgYWdIH///7+J6SJkYmZEacLkCUJacZqAD5DsInTLhDR"
            b"bcPlKrwugGnCFy6Mo3mBAQChDgRlP4RC7wAAAABJRU5ErkJggg==")
        self.sm_dn = imglist.Add(smalldnarrow.GetBitmap())

        self.p0list = MyListCtrl(self, size=(1140, 594), style=wx.LC_REPORT | wx.BORDER_SUNKEN |
                                                               # wx.LC_VRULES |
                                                               wx.LC_HRULES | wx.LC_SINGLE_SEL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        if self.master.column_info:
            for col, inf in enumerate(self.master.column_info):
                title, width = inf[:2]
                self.p0list.AppendColumn(self.master.captions[title])
                if col <= len(self.master.column_info):
                    self.p0list.SetColumnWidth(col, width)

            self.master.populate_list()

            # Now that the list exists we can init the other base class,
            # see wx/lib/mixins/listctrl.py
            self.itemDataMap = self.master.data  # nodig voor ColumnSorterMixin
            listmix.ColumnSorterMixin.__init__(self, len(self.master.column_info))
            self.SortListItems(0, True)

            self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected, self.p0list)
            self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_item_deselected, self.p0list)
            self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated, self.p0list)
            # self.Bind(wx.EVT_LIST_COL_CLICK, self.on_column_click, self.p0list)
            # self.p0list.Bind(wx.EVT_LEFT_DCLICK, self.on_doubleclick)

        self.p0list.SetImageList(imglist, wx.IMAGE_LIST_SMALL)

        sizer.Add(self.p0list, 1, wx.EXPAND | wx.ALL, 5)

        if self.master.has_extrapanel:
            self.layout_extra_fields(sizer)

        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)

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
                ted.Bind(wx.EVT_TEXT, self.master.on_text)
                self.screenfields.append(ted)
                self.txt_key = ted
            else:
                cb = wx.ComboBox(box, size=(140, -1), style=wx.CB_READONLY,
                                 choices=self.master.keylist)  # niet sorteren
                cb.Bind(wx.EVT_COMBOBOX, self.master.on_combobox)
                self.screenfields.append(cb)
                self.cmb_key = cb

        if 'C_MODS' in self.master.fields:
            for ix, x in enumerate(('M_CTRL', 'M_ALT', 'M_SHFT', 'M_WIN')):
                cb = wx.CheckBox(box, label=self.master.captions[x].join(("+ ", "")))
                cb.SetValue(False)
                self.screenfields.append(cb)
                cb.Bind(wx.EVT_CHECKBOX, self.master.on_checkbox)
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
            cb.Bind(wx.EVT_COMBOBOX, self.master.on_combobox)
            self.screenfields.append(cb)
            self.cmb_context = cb

        if 'C_CMD' in self.master.fields:
            self.txt_cmd = wx.StaticText(box, label=self.master.captions['C_CTXT'] + " ")
            cb = wx.ComboBox(box, size=(150, -1), style=wx.CB_READONLY)
            if 'C_CNTXT' not in self.master.fields:  # load on choosing context
                cb.SetItems(self.master.commandslist)
            cb.Bind(wx.EVT_COMBOBOX, self.master.on_combobox)
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
            self.txt_oms = wx.TextCtrl(box, size=(480, 40), style=wx.TE_MULTILINE | wx.TE_READONLY)

        try:
            self.master.reader.add_extra_fields(self, box)  # user exit
        except AttributeError:
            pass

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
        bsizer.AddSpacer(5)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        if 'C_KEY' in self.master.fields:
            sizer2.Add(self.lbl_key, 0, wx.ALIGN_CENTER_VERTICAL)
            if self.master.keylist is None:
                sizer2.Add(self.txt_key, 0, wx.ALIGN_CENTER_VERTICAL)
            else:
                sizer2.Add(self.cmb_key, 0, wx.ALIGN_CENTER_VERTICAL)
        if 'C_MODS' in self.master.fields:
            sizer2.Add(self.cb_ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
            sizer2.Add(self.cb_alt, 0, wx.ALIGN_CENTER_VERTICAL)
            sizer2.Add(self.cb_shift, 0, wx.ALIGN_CENTER_VERTICAL)
            sizer2.Add(self.cb_win, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(sizer2, 0)

        sizer1.AddStretchSpacer(1)
        if 'C_CNTXT' in self.master.fields:
            sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer2.Add(self.lbl_context, 0, wx.ALIGN_CENTER_VERTICAL)
            sizer2.Add(self.cmb_context, 0, wx.ALIGN_CENTER_VERTICAL)
            sizer1.Add(sizer2, 0)

        if 'C_CMD' in self.master.fields:
            sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer2.Add(self.txt_cmd, 0, wx.ALIGN_CENTER_VERTICAL)
            sizer2.Add(self.cmb_commando, 0, wx.ALIGN_CENTER_VERTICAL)
            sizer1.Add(sizer2, 0)

        try:
            self.master.reader.layout_extra_fields_topline(self, sizer1)  # user exit
        except AttributeError:
            pass

        sizer1.Add(self.b_save, 0)
        sizer1.Add(self.b_del, 0)
        bsizer.Add(sizer1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        self.toplinesizer = sizer1

        try:
            test = self.master.reader.layout_extra_fields_nextline
        except AttributeError:
            pass
        else:
            sizer1 = wx.BoxSizer(wx.HORIZONTAL)
            self.master.reader.layout_extra_fields_nextline(self, sizer1)  # user exit
            bsizer.Add(sizer1, 0)

        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        if 'C_DESC' in self.master.fields:
            # sizer2 = wx.BoxSizer(wx.VERTICAL)
            sizer1.Add(self.txt_oms, 1, wx.EXPAND)
            # sizer1.Add(sizer2, 1, wx.EXPAND)

        try:
            self.master.reader.layout_extra_fields(self, sizer1)  # user exit
        except AttributeError:
            pass

        bsizer.Add(sizer1, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        self._box.SetSizer(bsizer)
        # bsizer.Fit(self._box)
        sizer.Add(self._box, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND | wx.ALL, 2)

    def captions_extra_fields(self):
        """to be called on changing the language
        """
        print('in captions_extra_fields')
        print(self.master.fields)
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

        try:
            self.master.reader.captions_extra_fields(self)  # user exit
        except AttributeError:
            pass
        self.toplinesizer.Layout()

    def on_item_deselected(self, event):
        """callback op het niet meer geselecteerd zijn van een item

        onthou het item om later te vragen of de key definitie moet worden bijgewerkt
        """
        # check 1: zitten we niet te vroeg in het proces?
        if self.master.initializing_screen:
            return
        item = event.GetItem()
        if not item:  # bv. bij p0list.clear()
            return
        # print('in on_item_deselected, item is', item)
        self.olditem = item

    def on_item_selected(self, event):
        """callback op het selecteren van een item

        velden op het hoofdscherm worden bijgewerkt vanuit de selectie"""
        # check: is het überhaupt nodig?
        if not self.master.has_extrapanel:  # dit is hier wel voldoende
            return
        # check: zitten we niet te vroeg in het proces?
        item = event.GetItem()
        if not item:  # bv. bij p0list.clear()
            return
        #  check 2: kunnen we wijzigen (hebben we een extra schermdeel is niet voldoende)
        ## if not self.master.has_extrapanel:
            ## return
        if not bool(self.parent.master.page.settings[shared.SettType.RDEF.value]):
            return
        # print('in on_item_selected - has_extrapanel:', self.master.has_extrapanel, 'olditem is',
        #       self.olditem)
        self.initializing_keydef = True
        any_change, changedata = self.master.check_for_changes()
        found, indx = self.master.check_for_selected_keydef(changedata)
        make_change = self.master.ask_what_to_do(any_change, found, item, self.olditem)
        if make_change:
            item = self.master.apply_changes(found, indx, changedata)
        # if self.master.initializing_screen:
        #     self.refresh_extrascreen(event.GetItem())  # newitem)
        #     self.master.initializing_screen = False
        #     return
        # seli = self.p0list.GetItemData(event.GetEventObject().GetFirstSelected())  # Index())
        ## print "Itemselected",seli,self.data[seli]
        # self.refresh_extrascreen(seli)
        self.master.refresh_extrascreen(item)  # newitem)
        self.initializing_keydef = False
        event.Skip()

    def on_item_activated(self, event):
        """callback op het activeren van een item (onderdeel van het selecteren)
        """
        # print('in on_item_activated', event)
        self.current_item = event.GetItem()  # GetEventIndex()

    def on_update(self, event):
        """callback for editing kb shortcut
        """
        # print('in on_update', event)
        self.master.apply_changes()
        self.p0list.SetFocus()

    def on_delete(self, event):
        """callback for deleting kb shortcut
        """
        # print('in on_delete', event)
        self.master.apply_deletion()()
        self.p0list.SetFocus()

    # hulproutine t.b.v. managen column properties

    def update_columns(self, oldcount, newcount):
        "delete and insert columns"
        hlp = oldcount
        while hlp > newcount:
            self.p0list.DeleteColumn(0)
            hlp -= 1
        hlp = newcount
        while hlp > oldcount:
            self.p0list.AppendColumn('')
            hlp -= 1

    def refresh_headers(self, headers):
        "apply changes in the column headers"
        print(headers)
        print(self.master.column_info)
        for indx, coldata in enumerate(self.master.column_info):
            hdr = self.p0list.GetColumn(indx)
            print(hdr, hdr.GetText(), headers[indx])
            #if headers[indx] != hdr.GetText():
            hdr.SetText(headers[indx])
            hdr.SetWidth(coldata[1])
            self.p0list.SetColumn(indx, hdr)
        self.p0list.resizeLastColumn(100)

    def enable_buttons(self, state=True):
        """anders wordt de gelijknamige methode van de Panel base class geactiveerd"""

    def GetListCtrl(self):
        """ten behoeve van de columnsorter mixin"""
        return self.p0list

    # def GetSortImages(self):
    #     """ten behoeve van de columnsorter mixin"""
    #     return (self.sm_dn, self.sm_up)

    def OnSortOrderChanged(self):
        """ten behoeve van de columnsorter mixin
        na het sorteren moeten de regels weer om en om gekleurd worden"""
        self.p0list.RefreshRows()

# -- helper methods (called from master class) --
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
        for ix, value in enumerate(itemlist):
            self.p0list.SetItem(indx, ix, value)
        self.p0list.SetItemData(indx, key)

    def set_listselection(self, pos):
        "highlight the selected item in the list"
        self.p0list.Select(pos)

    def getfirstitem(self):
        "return first item in list"
        return self.p0list.GetItem(0)

    # used by on_text
    def get_widget_text(self, event):
        "return the text entered in a textfield"
        return event.GetEventWidget().GetValue()

    def enable_save(self, state):
        "make save button accessible"
        self.b_save.Enable(state)

    # used by on_combobox
    def get_choice_value(self, event):
        "return the value chosen in a combobox (and the widget itself)"
        cb = event.GetEventWidget()
        return cb, cb.GetValue()

    def get_combobox_text(self, cb):
        "return the text entered/selected in a combobox"
        return cb.GetText()

    def init_combobox(self, cb, choices=None):
        "initialize combobox to a set of new values"
        print('in init_combobox')
        cb.Clear()
        if choices is not None:
            cb.AppendItems(choices)

    def set_textfield_value(self, txt, value):
        "set the text for a textfield"
        txt.SetValue(value)

    # used by on_checkbox
    def get_check_value(self, event):
        "return the state set in a checkbox (and the widget itself)"
        cb = event.GetEventWidget()
        return cb, cb.GetValue()

    def get_checkbox_state(self, cb):
        "return the state set in a checkbox (without the widget)"
        return cb.GetValue()

    # used by refresh_extrascreen
    def enable_delete(self, state):
        "make delete button accessible"
        self.b_del.Enable(state)

    def get_itemdata(self, item):
        "return the data associated with a listitem"
        return item.GetData()

    def set_checkbox_state(self, cb, state):
        "set the state for a checkbox"
        cb.SetValue(state)

    def set_combobox_string(self, cmb, value, valuelist):
        "set the selection for a combobox"
        # print('in set_combobox_string')
        try:
            ix = valuelist.index(value)
        except ValueError:
            # print('exit on exception', value, 'not in', valuelist)
            return
        cmb.SetSelection(ix)

    def get_combobox_selection(self, cmb):
        "get the selection for a combobox"
        return cmb.GetStringSelection()

    # used by apply_changes en apply_deletion
    def get_selected_keydef(self):
        "return the currently selected keydef"
        return self.p0list.GetFirstSelected()

    def get_keydef_position(self, item):
        "return the index of a given keydef entry"
        return item.GetId()  # indexOfTopLevelItem(item)


class TabbedInterface(wx.Panel):
    """ Als wx.NoteBook, maar met selector in plaats van tabs
    """
    def __init__(self, parent, master):
        super().__init__(parent)
        self.parent = parent
        self.master = master

    def setup_selector(self):
        "create the selector"
        # print('in setup_selector')
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
        # print('appending to selector:', txt)
        self.sel.Append(txt)

    def format_screen(self):
        "realize the screen"
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddSpacer(10)
        self.sel_text = wx.StaticText(self)  # , label='', size=(80, -1))
        hbox.Add(self.sel_text, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.sel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        hbox.AddStretchSpacer(1)
        self.find_text = wx.StaticText(self)  # , label='', size=(80, -1))
        hbox.Add(self.find_text, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.find_loc, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        hbox.Add(wx.StaticText(self, label=' : '), 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.find, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox.Add(self.b_filter, 0)
        hbox.Add(self.b_next, 0)
        hbox.Add(self.b_prev, 0)
        hbox.AddSpacer(10)
        self.headlinesizer = hbox
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
        self.sel_text.SetLabel(self.parent.editor.captions['C_SELPRG'])
        self.find_text.SetLabel(self.parent.editor.captions['C_FIND'])
        if self.filter_on:
            self.b_filter.SetLabel(self.parent.editor.captions['C_FLTOFF'])
        else:
            self.b_filter.SetLabel(self.parent.editor.captions['C_FILTER'])
        self.b_next.SetLabel(self.parent.editor.captions['C_NEXT'])
        self.b_prev.SetLabel(self.parent.editor.captions['C_PREV'])
        self.headlinesizer.Layout()
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
        "return the currently selected panel's index"
        return self.pnl.GetCurrentPage()

    def get_selected_tool(self):
        "return the currently selected panel's name"
        return self.sel.GetStringSelection()

    def set_selected_panel(self, indx):
        "set the index of the panel to be selected"
        self.pnl.SetSelection(indx)

    def update_search(self, items):
        "refresh the search-related widgets"
        self.find_loc.Clear()
        self.find_loc.AppendItems(items)
        self.find_loc.SetSelection(len(items) - 1)
        if self.master.page.filtertext:
            self.find.SetValue(self.master.page.filtertext)
            self.b_filter.SetText(self.parent.captions['C_FLTOFF'])
            self.enable_search_buttons(filter=True)
        else:
            self.find.SetValue('')
            self.find.Enable(True)
            self.init_search_buttons()

    def after_changing_text(self, event):
        """callback for change in search text
        """
        text = event.GetEventObject().GetValue()
        if text:
            self.master.on_text_changed(text)

    # used by on_text_changed
    def get_search_col(self):
        "return the currently selected search column"
        return self.find_loc.GetStringSelection()

    def find_items(self, page, text):
        "return the items that contain the text to search for"
        result = []
        for i in range(page.gui.p0list.GetItemCount()):
            item = page.gui.p0list.GetItem(i)
            if text in page.gui.p0list.GetItemText(i, self.master.zoekcol):
                result.append(i)  # tem) - geen items maar indexes in de lijst opnemen
        return result

    def init_search_buttons(self):
        "set the search-related buttons to their initial values (i.e. disabled)"
        self.enable_search_buttons(next=False, prev=False, filter=False)

    def set_selected_keydef_item(self, page, index):
        "select a search result in the list"
        item = self.master.items_found[index]
        page.gui.p0list.Select(item)
        page.gui.p0list.EnsureVisible(item)

    def enable_search_buttons(self, next=None, prev=None, filter=None):
        "set the appropriate search-related button(s) to the given value)s)"
        if next is not None:
            self.b_next.Enable(next)
        if prev is not None:
            self.b_prev.Enable(prev)
        if filter is not None:
            self.b_filter.Enable(filter)

    # used by filter
    def get_filter_state_text(self):
        "return the current text of the filter button"
        return str(self.b_filter.GetLabel())

    def get_search_text(self):
        "return the text to search for"
        return self.find.GetValue()

    def get_found_keydef_position(self):
        "return the position marker of the current search result"
        plist = self.master.page.gui.p0list
        item = plist.GetFirstSelected()
        return plist.GetItemText(item, 0), plist.GetItemText(item, 1)

    def enable_search_text(self, value):
        "block or unblock entering/selecting a search text"
        self.find.Enable(value)

    def set_found_keydef_position(self):
        "find the next search rel=sult acoording to position marker(?)"
        plist = self.master.page.gui.p0list
        for i in range(plist.GetItemCount()):
            if (plist.GetItemText(i, 0), plist.GetItemText(i, 1)) == self.master.reposition:
                plist.Select(i)
                break

    def set_filter_state_text(self, state):
        "set the text for the filter button"
        self.b_filter.SetLabel(state)

    # hulproutines t.b.v. managen bestandslocaties

    def get_selected_index(self):
        "get index of selected item"
        return self.sel.GetSelection()  # currentIndex()

    def clear_selector(self):
        "reset selector"
        self.sel.Clear()

    def remove_tool(self, indx, program, program_list):
        """remove a tool from the confguration"""
        win = self.pnl.GetPage(indx)
        self.pnl.RemovePage(indx)
        if program in program_list:
            return win.master  # keep the widget (will be re-added)
        win.Destroy()  # lose the widget
        return None

    def add_tool(self, program, win):
        "add a tool to the configuration"
        self.add_subscreen(win)
        self.add_to_selector(program)

    def get_new_selection(self, item):
        "find the index to set the new selection to"
        return self.sel.GetSelection()  # findText(item)

    def set_selected_tool(self, selection):
        "set the new selection index"
        self.sel.SetSelection(selection)

    # hulproutines t.b.v. managen tool specifieke settings

    def get_selected_panel(self):
        "return index and handle of the selected panel"
        indx = self.sel.GetSelection()
        win = self.pnl.GetPage(indx)
        return indx, win

    def replace_panel(self, indx, win, newwin):
        "replace a panel with a modified version"
        self.pnl.InsertPage(indx, newwin)
        self.pnl.SetSelection(newwin)  # or ChangeSelection to avoid sending events
        self.pnl.RemovePage(win)

    def set_panel_editable(self, test_redef):
        "(re)set editability of the current panel"
        win = self.pnl.GetCurrentPage()
        win.set_extrascreen_editable(test_redef)

    # hulproutine t.b.v. managen column properties

    def refresh_locs(self, headers):
        "apply changes in the selector for `search in column`"
        self.find_loc.Clear()
        self.find_loc.AppendItems(headers)

    # hulpfunctie t.b.v. afsluiten: bepalen te onthouden tool

    def get_selected_text(self):
        "get text of selected item"
        return self.sel.GetStringselection()


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
        self.SetMenuBar(self.menu_bar)

    def resize_empty_screen(self, wid, hig):
        """full size not needed for a single message
        """
        self.SetSize(wid, hig)

    def go(self):
        "build and show the interface"
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

    def close(self, event=None):
        """applicatie afsluiten"""
        self.Close(True)

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
                oldmenu = self.menu_bar.Replace(ix, menu, self.editor.captions[title])
                oldmenu.Destroy()
                shared.log(oldmenu, always=True)
            else:
                self.menu_bar.Append(menu, self.editor.captions[title])
            self.menuitems[title] = menu, ''
            ix += 1

    def setcaptions(self):
        "set title for menuitem or action"
        topmenus = [x[0] for x in self.menu_bar.GetMenus()]
        for menu, item in self.menuitems.items():
            item, shortcut = item
            try:
                oldtitle = item.GetTitle()  # als deze kan dan is het een menu
            except AttributeError:
                item.SetText('\t'.join((self.editor.captions[menu], shortcut)))
            else:
                # dit stelt de titel van het menu in
                item.SetTitle(self.editor.captions[menu])
                # maar ik zoek de titel van het bijbehorende menuitem (in het bovenliggende menu)
                pmenu = item.GetParent()
                if pmenu:
                    for mitem in pmenu.GetMenuItems():
                        if mitem.IsSubMenu():
                            pmenu.SetLabel(mitem.GetId(), self.editor.captions[menu])
                else:
                    self.menu_bar.Replace(topmenus.index(item), item, self.editor.captions[menu])

    # hulproutine t.b.v. managen tool specifieke settings

    def modify_menuitem(self, caption, setting):
        "enable/disable menu option identified by caption"
        self.menuitems[caption][0].Enable(setting)
