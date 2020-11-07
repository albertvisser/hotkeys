"""Hotkeys plugin for Total Commander - wxPython specific code
"""
import wx
import editor.plugins.mergetool_shared as shared
from ..gui_wx import MyListCtrl     # wx.ListCtrl with mixins


class MergeDialog(shared.MergeMixin, wx.Dialog):
    """Dialoog om een gedocumenteerde toetscombinatie te koppelen aan een commando

    In het ene ini bestand staat namelijk toets + omschrijving en in het andere
    command + omschrijving en de omschrijvingen hoeven uiteraard niet 100% gelijk
    te zijn, dus moeten ze handmatig gekoppeld worden.
    """
    def __init__(self, parent, master):
        """Opbouwen van het scherm

        parent is een SingleDataInterface, master is een HotKeyPanel
        """
        shared.MergeMixin.__init__(self, master)
        wx.Dialog.__init__(self, parent, title="TCCM", size=(1000, 600),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        # image voor het vinkje opzetten dat m.b.v. SetItemColumnImage ingesteld kan worden
        self.imglist = wx.ImageList(16, 16)
        # self.todoimage = self.imglist.Add(wx.NullBitmap)
        self.okimage = self.imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK))
        self.todoimage = self.imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK)) # ART_MINUS

        self.listkeys = MyListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listkeys.InsertColumn(0, 'Key')
        self.listkeys.InsertColumn(1, 'Description')
        self.listkeys.SetImageList(self.imglist, wx.IMAGE_LIST_SMALL)
        # self.listkeys.SetToolTip(self.popuptext)  -- nog iets op vinden
        self.listkeys.Bind(wx.EVT_LIST_ITEM_SELECTED, self.select_match_fromkeys)

        self.findkeybutton = self.create_findbutton(columns=('key', 'text'))
        self.findkeybutton.SetSelection(1)
        self.findkeytext = wx.TextCtrl(self, size=(120, -1))
        self.nextkey = wx.Button(self, label='&Next', size=(50, -1))
        self.nextkey.Bind(wx.EVT_BUTTON, self.findnextkey)
        self.prevkey = wx.Button(self, label='&Prev', size=(50, -1))
        self.prevkey.Bind(wx.EVT_BUTTON, self.findprevkey)

        self.listcmds = MyListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listcmds.InsertColumn(0, 'Command')
        self.listcmds.InsertColumn(1, 'Description')
        # self.listcmds.SetToolTip(self.popuptext)  -- nog iets op vinden
        self.listcmds.Bind(wx.EVT_LIST_ITEM_SELECTED, self.select_match_from_cmds)

        self.findcmdbutton = self.create_findbutton(columns=('cmd', 'text'))
        self.findcmdbutton.SetSelection(1)
        self.findcmdtext = wx.TextCtrl(self, size=(120, -1))
        self.nextcmd = wx.Button(self, label='Ne&xt', size=(50, -1))
        self.nextcmd.Bind(wx.EVT_BUTTON, self.findnextcmd)
        self.prevcmd = wx.Button(self, label='Pre&v', size=(50, -1))
        self.prevcmd.Bind(wx.EVT_BUTTON, self.findprevcmd)

        self.listmatches = MyListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listmatches.InsertColumn(0, 'Key')
        self.listmatches.InsertColumn(1, 'Command')
        self.listmatches.Bind(wx.EVT_LIST_ITEM_SELECTED, self.select_listitems_from_matches)

        self.btn_match = wx.Button(self, label="&+ Add/Replace match")
        self.btn_match.Bind(wx.EVT_BUTTON, self.make_match)
        self.btn_delete = wx.Button(self, label="&- Discard match")
        self.btn_delete.Bind(wx.EVT_BUTTON, self.delete_match)

        self.btn_load = wx.Button(self, label="&Load matches")
        self.btn_load.Bind(wx.EVT_BUTTON, self.load_matches)
        self.btn_clear = wx.Button(self, label="&Clear All")
        self.btn_clear.Bind(wx.EVT_BUTTON, self.reset_all)
        self.btn_save = wx.Button(self, label="&Save matches")
        self.btn_save.Bind(wx.EVT_BUTTON, self.save_matches)
        self.btn_quit = wx.Button(self, label="&Afsluiten")
        self.btn_quit.Bind(wx.EVT_BUTTON, self.close)
        self.btn_build = wx.Button(self, label="&Build CSV")
        self.btn_build.Bind(wx.EVT_BUTTON, self.confirm)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.listkeys, 1, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.AddStretchSpacer()
        hbox2.Add(self.findkeybutton, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.findkeytext, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.nextkey, 0)
        hbox2.Add(self.prevkey, 0)
        hbox2.AddStretchSpacer()
        vbox2.Add(hbox2, 0, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND | wx.LEFT, 10)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.listcmds, 1, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.AddStretchSpacer()
        hbox2.Add(self.findcmdbutton, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.findcmdtext, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.nextcmd, 0)
        hbox2.Add(self.prevcmd, 0)
        hbox2.AddStretchSpacer()
        vbox2.Add(hbox2, 0, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.listmatches, 1, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.AddStretchSpacer()
        hbox2.Add(self.btn_match)
        hbox2.Add(self.btn_delete)
        hbox2.AddStretchSpacer()
        vbox2.Add(hbox2, 0, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND | wx.RIGHT, 10)
        vbox.Add(hbox, 1, wx.EXPAND)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        hbox.Add(self.btn_load, 0, wx.ALL, 2)
        hbox.Add(self.btn_clear, 0, wx.ALL, 2)
        hbox.Add(self.btn_save, 0, wx.ALL, 2)
        hbox.Add(self.btn_quit, 0, wx.ALL, 2)
        hbox.Add(self.btn_build)
        hbox.AddStretchSpacer()
        vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.SetAutoLayout(True)
        self.SetSizer(vbox)
        # vbox.SetSizeHints(self)  # dit dus juist niet; sizer bepaalt grootte van venster

        accel_list = []
        for text, callback, keyseq, desc in self.getshortcuts():
            menuitem = wx.MenuItem(None, -1, text)
            self.Bind(wx.EVT_MENU, callback, menuitem)
            accel = wx.AcceleratorEntry(cmd=menuitem.GetId())
            ok = accel.FromString(keyseq)
            if ok:
                accel_list.append(accel)
        accel_table = wx.AcceleratorTable(accel_list)
        self.SetAcceleratorTable(accel_table)
        self.load_files()

    def create_findbutton(self, columns):
        """stel in waarop gezocht moet worden
        """
        control = wx.ComboBox(self, size=(120, -1), choices = ['Find ' + x for x in columns],
                              style=wx.CB_DROPDOWN | wx.CB_READONLY)
        return control

    def clear_listkeys(self):
        "initialize the list of keycombos"
        self.listkeys.DeleteAllItems()

    def add_listkeys_item(self, key, value):
        "add an item to the list of keycombos"
        index = self.listkeys.InsertItem(self.listkeys.GetItemCount(), key)
        self.listkeys.SetItem(index, 1, value['oms'])

    def clear_listcmds(self):
        "initialize the list of mappable commands"
        self.listcmds.DeleteAllItems()

    def add_listcmds_item(self, key, value):
        "add an item to the list of mappable commands"
        index = self.listcmds.InsertItem(self.listkeys.GetItemCount(), key)
        self.listcmds.SetItem(index, 1, value['oms'])

    def clear_listmatches(self):
        "(re)initialize the list of mappings"
        self.listmatches.DeleteAllItems()
        for ix in range(self.listkeys.GetItemCount()):
            self.reset_listitem_icon(ix)

    def add_listmatches_item(self, keytext, command):
        "add an item to the list of mappings"
        index = self.listmatches.InsertItem(self.listmatches.GetItemCount(), keytext)
        self.listmatches.SetItem(index, 1, command)
        return index  # self.listmatches.GetItem(index)

    def set_listitem_icon(self, ix):
        "set the check image for a keycombo list item"
        # item = self.listkeys.GetItem(keychoice)
        item = self.listkeys.GetItem(ix)
        item.SetImage(self.okimage)
        self.listkeys.SetItem(item)

    def get_selected_key_data(self):
        "get the texts for the selected keycombo"
        keychoice = self.listkeys.GetFirstSelected()
        keytext = self.listkeys.GetItemText(keychoice, 0)
        keyoms = self.listkeys.GetItemText(keychoice, 1)
        return keychoice, keytext, keyoms

    def get_selected_cmd_data(self):
        "get the texts for the selected command"
        cmdchoice = self.listcmds.GetFirstSelected()
        cmdtext = self.listcmds.GetItemText(cmdchoice, 0)
        return cmdchoice, cmdtext

    def get_selected_matchitem(self):
        "get the selected mapping item"
        ix = self.listmatches.GetFirstSelected()
        if ix == -1:
            return None
        return ix

    def find_in_list(self, lst, col, text, start=0, exact=True):
        "find text in a column in a list from a given item"
        for ix in range(start, lst.GetItemCount()):
            itemtext = lst.GetItemText(ix, col)
            if (exact and itemtext == text) or (not exact and text.upper() in itemtext.upper()):
                # item = self.listkeys.GetItem(ix)
                break
        else:
           ix = None  # -1  # item = None
        return ix

    def find_in_listmatches(self, keytext):
        "find a keycombo in the mappings list"
        return self.find_in_list(self.listmatches, 0, keytext)

    def find_in_listkeys(self, keytext):
        "find a keycombo in the shortcuts list"
        return self.find_in_list(self.listkeys, 0, keytext)

    def replace_matchlist_item(self, itemindex, cmdtext):
        "replace the command in a mapping item"
        item = self.listmatches.GetItem(itemindex)
        self.listmatches.SetItemText(item, 1, cmdtext)

    def ensure_item_visible(self, ix, win=None):  # item):
        "make sure the selected mapping can be viewed in the list"
        if win == None:
            win = self.listmatches
        print(win.EnsureVisible(ix))  # item.GetId())

    def remove_matchitem(self, itemindex):
        "delete a mapping from the list"
        # find = self.listmatches.GetItemText(item.GetId(), 0)
        # self.listmatches.DeleteItem(find)
        self.listmatches.DeleteItem(itemindex)  # item.GetId())

    def reset_listitem_icon(self, ix):
        "find the corresponding keycombo item and unset the check image"
        item = self.listkeys.GetItem(ix)
        item.SetImage(self.todoimage)
        self.listkeys.SetItem(item)

    def focuskeylist(self, event=None):
        "shift focus for selecting a keycombo item"
        self.listkeys.SetFocus()

    def focuscmdlist(self, event=None):
        "shift focus for selecting a command item"
        self.listcmds.SetFocus()

    def focusmatchlist(self, event=None):
        "shift focus for selecting a mapping item"
        self.listmatches.SetFocus()

    def focusfindkey(self, event=None):
        "shift focus to enter a keycombo search phrase"
        self.findkeytext.SetFocus()

    def focusfindcmd(self, event=None):
        "shift focus to enter a command search phrase"
        self.findcmdtext.SetFocus()

    def popuptext(self, item, colno):
        "show complete text of description if moused over"
        if colno == 1:
            item.setToolTip(colno, item.text(colno))

    def get_entry_text(self, win):
        "get a text entry field's text"
        return win.GetValue()

    def get_search_choice(self, control):
        "return the selected item's index for the given list"
        return control.GetSelection()

    def find_listitems(self, win, search, in_col=1):
        "find all items in a list that contain a search text"
        results = []
        itemindex = self.find_in_list(win, in_col, search, exact=False)
        while itemindex is not None:  # != -1:
            print(itemindex)
            results.append(itemindex)
            itemindex = self.find_in_list(win, 1, search, start=itemindex + 1, exact=False)
        for itemindex in results:
            item = win.GetItem(itemindex)
            print(item, itemindex, item.GetText(), win.GetItemText(itemindex), 0)
        return results

    def get_selected_item(self, win):
        "get the selected item in a list"
        sel = win.GetFirstSelected()
        if sel != -1:
            self.ensure_item_visible(sel, win)
        return sel
        # test = win.GetFirstSelected()
        # all_items, count = [test], win.GetSelectedItemCount()
        # while count - len(all_items) > 0:
        #     all_items.append(win.GetNextSelected())
        # print(count, 'items selected:', all_items)
        # found = None if test == -1 else win.GetItem(test)
        # print('get selected', found, test, end=' ')
        # if found:
        #     print(found.GetText(), win)
        # else:
        #     print('(not found)', win)
        # # if test == -1:
        # #     test = None
        # # else:
        # #     test = win.GetItem(test)
        # return found

    def get_first_item(self, win):
        "get the first item of a list"
        return 0  # win.GetItem(0)

    def get_last_item(self, win):
        "get the last item of a list"
        return win.GetItemCount() - 1  # win.GetItem(win.GetItemCount() - 1)

    def get_item_text(self, win, itemindex, col):
        "get the text for a column of an item in one of the lists"
        # print(item, col, item.GetId(), win.GetItemText(item.GetId()))
        return win.GetItemText(itemindex, col)

    def set_selected_item(self, win, itemindex):
        "set the selected item for on of the lists"
        ix = win.GetFirstSelected()
        if ix != -1:
            print('in set_selected: selection is now', win.GetItem(ix), ix, win.GetItemText(ix, 0))
        item = win.GetItem(itemindex)
        print('in set_selected: set item', item, itemindex, item.GetText())
        win.Select(itemindex)
        ix = win.GetFirstSelected()
        print('in set_selected: item is ', win.GetItem(ix), ix, win.GetItemText(ix, 0))
        print('let`s try some more:', win.GetItem(ix, 0), win.GetItem(ix, 1),
              win.GetItem(ix).GetText())

    def count_matches(self):
        "get the current number of mappings in the list"
        return self.listmatches.GetItemCount()

    def get_matchitem_data(self, itemindex):
        "get the texts for a mapping item"
        return (self.get_item_text(self.listmatches, itemindex, 0),
                self.get_item_text(self.listmatches, itemindex, 1))

    def reject(self):
        "discard the dialog"
        self.EndModal(wx.ID_CANCEL)

    def finish(self):
        "finalize confirmation"
        self.EndModal(wx.ID_OK)

    def accept(self):
        "close the dialog after confirmation"
        return True
