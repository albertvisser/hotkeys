"""Hotkeys plugin for Total Commander - wxPython specific code
"""
import wx
import editor.plugins.tcmdrkys_shared as shared
from ..gui_wx import MyListCtrl     # wx.ListCtrl with mixins


class TcMergeDialog(shared.TcMergeMixin, wx.Dialog):
    """Dialoog om een gedocumenteerde toetscombinatie te koppelen aan een commando

    In het ene ini bestand staat namelijk toets + omschrijving en in het andere
    command + omschrijving en de omschrijvingen hoeven uiteraard niet 100% gelijk
    te zijn, dus moeten ze handmatig gekoppeld worden. Vandaar de ietwat misleidende
    naam "links"
    """
    def __init__(self, parent, master):
        """Opbouwen van het scherm

        parent is een SingleDataInterface, master is een HotKeyPanel
        """
        shared.TcMergeMixin.__init__(self, master)
        wx.Dialog.__init__(self, parent, title="TCCM", size=(1000, 600),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        # image voor het vinkje opzetten dat m.b.v. SetItemColumnImage ingesteld kan worden
        self.imglist = wx.ImageList(16, 16)
        # self.todoimage = self.imglist.Add(wx.NullBitmap)
        self.okimage = self.imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK))

        self.listkeys = MyListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listkeys.InsertColumn(0, 'Key')
        self.listkeys.InsertColumn(1, 'Description')
        self.listkeys.SetImageList(self.imglist, wx.IMAGE_LIST_SMALL)
        # self.listkeys.SetToolTip(self.popuptext)  -- nog iets op vinden

        self.findkeytext = wx.TextCtrl(self, size=(120, -1))
        self.nextkey = wx.Button(self, label='&Next', size=(50, -1))
        self.nextkey.Bind(wx.EVT_BUTTON, self.findnextkey)
        self.prevkey = wx.Button(self, label='&Prev', size=(50, -1))
        self.prevkey.Bind(wx.EVT_BUTTON, self.findprevkey)

        self.listcmds = MyListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listcmds.InsertColumn(0, 'Command')
        self.listcmds.InsertColumn(1, 'Description')
        # self.listcmds.SetToolTip(self.popuptext)  -- nog iets op vinden

        self.findcmdtext = wx.TextCtrl(self, size=(120, -1))
        self.nextcmd = wx.Button(self, label='Ne&xt', size=(50, -1))
        self.nextcmd.Bind(wx.EVT_BUTTON, self.findnextcmd)
        self.prevcmd = wx.Button(self, label='Pre&v', size=(50, -1))
        self.prevcmd.Bind(wx.EVT_BUTTON, self.findprevcmd)

        self.listlinks = MyListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listlinks.InsertColumn(0, 'Key')
        self.listlinks.InsertColumn(1, 'Command')

        self.btn_link = wx.Button(self, label="&+ Add/Replace Link")
        self.btn_link.Bind(wx.EVT_BUTTON, self.make_link)
        self.btn_delete = wx.Button(self, label="&- Discard Link")
        self.btn_delete.Bind(wx.EVT_BUTTON, self.delete_link)

        self.btn_load = wx.Button(self, label="&Load Links")
        self.btn_load.Bind(wx.EVT_BUTTON, self.load_links)
        self.btn_clear = wx.Button(self, label="&Clear All")
        self.btn_clear.Bind(wx.EVT_BUTTON, self.reset_all)
        self.btn_save = wx.Button(self, label="&Save Links")
        self.btn_save.Bind(wx.EVT_BUTTON, self.save_links)
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
        hbox2.Add(wx.StaticText(self, label='Find text:'), 0, wx.ALIGN_CENTER_VERTICAL)
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
        hbox2.Add(wx.StaticText(self, label='Find text:'), 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.findcmdtext, 0, wx.ALIGN_CENTER_VERTICAL)
        hbox2.Add(self.nextcmd, 0)
        hbox2.Add(self.prevcmd, 0)
        hbox2.AddStretchSpacer()
        vbox2.Add(hbox2, 0, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)

        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox2.Add(self.listlinks, 1, wx.EXPAND)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.AddStretchSpacer()
        hbox2.Add(self.btn_link)
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

    def clear_listlinks(self):
        "(re)initialize the list of mappings"
        self.listlinks.DeleteAllItems()
        for ix in range(self.listkeys.GetItemCount()):
            item = self.listkeys.GetItem(ix)
            self.reset_listitem_icon(item)

    def add_listlinks_item(self, keytext, command):
        "add an item to the list of mappings"
        index = self.listlinks.InsertItem(self.listlinks.GetItemCount(), keytext)
        self.listlinks.SetItem(index, 1, command)

    def set_listitem_icon(self, item):
        "set the check image for a keycombo list item"
        # item = self.listkeys.GetItem(keychoice)
        item.SetImage(self.okimage)
        self.listkeys.SetItem(item)

    def get_selected_key_data(self):
        "get the texts for the selected keycombo"
        keychoice = self.listkeys.GetFirstSelected()
        keytext = self.listkeys.GetItemText(keychoice, 0)
        key = self.listkeys.GetItemData(keychoice, 0)
        return keychoice, key, keytext

    def get_selected_cmd_data(self):
        "get the texts for the selected command"
        cmdchoice = self.listcmds.GetFirstSelected()
        cmdtext = self.listcmds.GetItemtext(cmdchoice, 0)
        return cmdchoice, cmdtext

    def get_selected_linkitem(self, ix):
        "get the selected mapping item"
        return self.listlinks.GetItem(ix)

    def find_in_list(self, lst, col, text, start=0, exact=True):
        "find text in a column in a list from a given item"
        for ix in range(start, lst.GetItemCount()):
            itemtext = lst.GetItemText(ix, col)
            if (exact and itemtext == text) or (not exact and text.upper() in itemtext.upper()):
                break
        else:
           ix = -1
        return ix

    def find_in_listlinks(self, keytext):
        "find a keycombo in the mappings list"
        return self.find_in_list(self.listlinks, 0, keytext)

    def find_in_listkeys(self, keytext):
        "find a keycombo in the shortcuts list"
        return self.find_in_list(self.listkeys, 0, keytext)

    def replace_linklist_item(self, item, cmdtext):
        "replace the command in a mapping item"
        self.listlinks.SetItemText(item, 1, cmdtext)

    def ensure_item_visible(self, item):
        "make sure the selected mapping can be viewed in the list"
        self.listlinks.scrollTo(self.listlinks.indexFromItem(item))

    def remove_linkitem(self, item):
        "delete a mapping from the list"
        find = self.listlinks.GetText(item, 0)
        self.listlinks.DeleteItem(find)

    def reset_listitem_icon(self, item):
        "find the corresponding keycombo item and unset the check image"
        item.SetImage(-1)  # self.todoimage)
        self.listkeys.SetItem(item)

    def focuskeylist(self, event=None):
        "shift focus for selecting a keycombo item"
        self.listkeys.SetFocus()

    def focuscmdlist(self, event=None):
        "shift focus for selecting a command item"
        self.listcmds.SetFocus()

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

    def find_listitems(self, win, search):
        "find all items in a list that contain a search text"
        results = []
        item = self.find_in_list(self.listkeys, 1, search, exact=False)
        while item != -1:
            results.append(item)
            item = self.find_in_list(self.listkeys, 1, search, start=item + 1, exact=False)
        return results

    def get_selected_item(self, win):
        "get the selected item in a list"
        test = win.GetFirstSelected()
        if test == -1:
            test = None
        return test

    def get_first_item(self, win):
        "get the first item of a list"
        return 0

    def get_last_item(self, win):
        "get the last item of a list"
        return win.GetItemCount() - 1

    def get_item_text(self, win, item, col):
        "get the text for a column of an item in one of the lists"
        return win.GetItemText(item, col)

    def set_selected_item(self, win, item):
        "set the selected item for on of the lists"
        win.Select(item)

    def count_links(self):
        "get the current number of mappings in the list"
        return self.listlinks.GetItemCount()

    def get_linkitem_data(self, ix):
        "get the texts for a mapping item"
        item = self.listlinks.GetItem(ix)
        return self.gui.get_item_text(item, 0), self.gui.get_item_text(item, 1)

    def reject(self):
        "discard the dialog"
        self.EndModal(wx.ID_CANCEL)

    def accept(self):
        "confirm the change amd end the dialog"
        self.EndModal(wx.ID_OK)
