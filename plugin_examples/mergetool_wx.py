"""Hotkeys plugin for Total Commander - wxPython specific code
"""
import contextlib
import wx
# import editor.plugins.mergetool_shared as shared
from ..wxgui import MyListCtrl     # wx.ListCtrl with mixins


# class MergeDialog(shared.MergeMixin, wx.Dialog):
class MergeDialogGui(wx.Dialog):
    """Dialoog om een gedocumenteerde toetscombinatie te koppelen aan een commando

    In het ene ini bestand staat namelijk toets + omschrijving en in het andere
    command + omschrijving en de omschrijvingen hoeven uiteraard niet 100% gelijk
    te zijn, dus moeten ze handmatig gekoppeld worden.
    """
    def __init__(self, master, parent):
        """Opbouwen van het scherm

        parent is een SingleDataInterface, master is MergeTool
        """
        self.master = master
        wx.Dialog.__init__(self, parent, title="TCCM", size=(1500, 900),
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        # image voor het vinkje opzetten dat m.b.v. SetItemColumnImage ingesteld kan worden
        self.imglist = wx.ImageList(16, 16)
        # self.todoimage = self.imglist.Add(wx.NullBitmap)
        self.okimage = self.imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK))
        self.todoimage = self.imglist.Add(wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK))
        self.accel_list = []

    def init_display(self):
        "build the screen container"
        return wx.BoxSizer(wx.VERTICAL)

    def add_row(self, screen):
        "create a horizontal subcontainer to add stuff into"
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        screen.Add(sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
        return sizer

    def add_col_to_row(self, row):
        "create a vertical subcontainer to add stuff into"
        sizer = wx.BoxSizer(wx.VERTICAL)
        row.Add(sizer, 1, wx.EXPAND)
        return sizer

    def create_list(self, columns, callback):
        "create a listbox"
        listbox = MyListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        for ix, text in enumerate(columns):
            listbox.InsertColumn(ix, text)
        listbox.SetImageList(self.imglist, wx.IMAGE_LIST_SMALL)
        listbox.Bind(wx.EVT_LIST_ITEM_SELECTED, callback)
        # self.listkeys.SetToolTip(self.popuptext)  -- nog iets op vinden
        # self.listcmds.SetToolTip(self.popuptext)  -- nog iets op vinden
        return listbox

    def create_findbutton(self, columns):
        "create a 'Find' combobox"
        control = wx.ComboBox(self, size=(120, -1), choices=['Find ' + x for x in columns],
                              style=wx.CB_DROPDOWN | wx.CB_READONLY)
        control.SetSelection(1)
        return control

    def create_text(self):
        "create a text field"
        return wx.TextCtrl(self, size=(120, -1))

    def create_button(self, text, callback, size=0):
        "create a button"
        if size:
            button = wx.Button(self, label=text, size=(size, -1))
        else:
            button = wx.Button(self, label=text)
        button.Bind(wx.EVT_BUTTON, callback)
        return button

    def add_row_to_col(self, col, *args, **kwargs):
        "create a horizontal subcontainer to add widgets to"
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        if len(args) == 1:
            sizer.Add(args[0], 1, wx.EXPAND)
            if 'left_align' in kwargs:
                col.Add(sizer, 1, wx.EXPAND | wx.LEFT, 10)
            elif 'center' in kwargs:
                col.Add(sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
            elif 'right_align' in kwargs:
                col.Add(sizer, 1, wx.EXPAND | wx.RIGHT, 10)
            else:
                col.Add(sizer, 1, wx.EXPAND | wx.ALL)
        elif len(args) == 4:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.AddStretchSpacer()
            hbox.Add(args[0], 0)  # , wx.ALIGN_CENTER_VERTICAL)
            hbox.Add(args[1], 0)  # , wx.ALIGN_CENTER_VERTICAL)
            hbox.Add(args[2], 0)
            hbox.Add(args[3], 0)
            hbox.AddStretchSpacer()
            sizer.Add(hbox, 1, wx.EXPAND)
            col.Add(sizer, 0, wx.EXPAND | wx.TOP, 10)  # wx.ALL)
        else:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.AddStretchSpacer()
            for item in args:
                hbox.Add(item, 0, wx.ALL, 2)
            hbox.AddStretchSpacer()
            sizer.Add(hbox, 1, wx.EXPAND)
            if len(args) == 2:
                col.Add(sizer, 0, wx.EXPAND | wx.TOP, 10)  # wx.ALL)
            else:
                col.Add(sizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)  # wx.ALL)
        # for arg in ('right_align', 'center'):
        #     if kwargs.get(arg, False):
        #         sizer.AddStretchSpacer()
        # for item in args:
        #     sizer.Add(item, 0)
        # for arg in ('left_align', 'center'):
        #     if kwargs.get(arg, False):
        #         sizer.AddStretchSpacer()
        # col.Add(sizer, 1, wx.EXPAND | wx.ALL)

    # def create_row(self, *args, **kwargs):
    #     "create a row (horizontal line) of widgets"
    #     sizer = wx.BoxSizer(wx.HORIZONTAL)
    #     for arg in ('right_align', 'center'):
    #         if kwargs.get(arg, False):
    #             sizer.AddStretchSpacer()
    #     for item in args:
    #         sizer.Add(item, 0)
    #     for arg in ('left_align', 'center'):
    #         if kwargs.get(arg, False):
    #             sizer.AddStretchSpacer()
    #     return sizer

    # def create_column(self, *args, **kwargs):
    #     "create a column (vertical line) of widgets"
    #     sizer = wx.BoxSizer(wx.VERTICAL)
    #     for arg in ('bottom_align', 'center'):
    #         if kwargs.get(arg, False):
    #             sizer.AddStretchSpacer()
    #     stretch = 1
    #     for item in args:
    #         sizer.Add(item, stretch, wx.EXPAND)
    #         stretch = 0 if stretch == 1 else stretch
    #     for arg in ('top_align', 'center'):
    #         if kwargs.get(arg, False):
    #             sizer.AddStretchSpacer()
    #     return sizer

    # def add_to_screen(self, parent, sizer, **kwargs):
    #     "add a row or column to the screen estate"
    #     if kwargs.get('left', ''):
    #         hbox.Add(vbox2, 1, wx.EXPAND | wx.LEFT, 10)
    #     elif kwargs.get('middle', ''):
    #         hbox.Add(vbox2, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 5)
    #     elif kwargs.get('right', ''):
    #         hbox.Add(vbox2, 1, wx.EXPAND | wx.RIGHT, 10)
    #     else:  # if kwargs,get('center', ''):
    #         vbox.Add(hbox, 0, wx.ALIGN_CENTER_HORIZONTAL)

    def finalize_display(self, vbox):
        "add the layout to the window"
        self.SetAutoLayout(True)
        self.SetSizer(vbox)
        # vbox.SetSizeHints(self)  # dit dus juist niet; sizer bepaalt grootte van venster

    def create_hotkey(self, text, callback, keyseq, desc):
        "create shortcuts for actions"
        menuitem = wx.MenuItem(None, -1, text)
        self.Bind(wx.EVT_MENU, callback, menuitem)
        accel = wx.AcceleratorEntry(cmd=menuitem.GetId())
        ok = accel.FromString(keyseq)
        if ok:
            self.accel_list.append(accel)
        if text == 'help':
            accel_table = wx.AcceleratorTable(self.accel_list)
            self.SetAcceleratorTable(accel_table)

    def clear_list(self, listbox):
        "initialize the list"
        listbox.DeleteAllItems()

    def get_listbox_count(self, listbox):
        "return the number of entries in the list"
        return listbox.GetItemCount()

    def add_listitem(self, listbox, keytext, command):
        "add an item to the list of mappings"
        index = listbox.InsertItem(listbox.GetItemCount(), keytext)
        listbox.SetItem(index, 1, command)
        return index

    def set_listitem_icon(self, listbox, ix):
        "set the check image for a keycombo list item"
        item = listbox.GetItem(ix)
        item.SetImage(self.okimage)
        listbox.SetItem(item)

    # def get_selected_key_data(self):
    #     "get the texts for the selected keycombo"
    #     keychoice = self.listkeys.GetFirstSelected()
    #     keytext = self.listkeys.GetItemText(keychoice, 0)
    #     keyoms = self.listkeys.GetItemText(keychoice, 1)
    #     return keychoice, keytext, keyoms

    # def get_selected_cmd_data(self):
    #     "get the texts for the selected command"
    #     cmdchoice = self.listcmds.GetFirstSelected()
    #     cmdtext = self.listcmds.GetItemText(cmdchoice, 0)
    #     return cmdchoice, cmdtext

    # def get_selected_matchitem(self):
    #     "get the selected mapping item"
    #     ix = self.listmatches.GetFirstSelected()
    #     if ix == -1:
    #         return None
    #     return ix

    def get_selected_listbox_data(self, listbox):
        "get the selected item and the texts for it"
        choice = listbox.GetFirstSelected()
        text0 = text1 = ''
        with contextlib.suppress(IndexError):
            text0 = listbox.GetItemText(choice, 0)
        with contextlib.suppress(IndexError):
            text1 = listbox.GetItemText(choice, 1)
        return choice, text0, text1

    # def find_in_listmatches(self, keytext):
    #     "find a keycombo in the mappings list"
    #     return self.find_in_list(self.listmatches, 0, keytext)

    # def find_in_listkeys(self, keytext):
    #     "find a keycombo in the shortcuts list"
    #     return self.find_in_list(self.listkeys, 0, keytext)

    def find_in_listbox(self, listbox, text, col=0, start=0, exact=True):
        "find text in a column in a list from a given item"
        for ix in range(start, listbox.GetItemCount()):
            itemtext = listbox.GetItemText(ix, col)
            if (exact and itemtext == text) or (not exact and text.upper() in itemtext.upper()):
                break
        else:
            ix = None
        return ix

    def replace_listbox_item(self, listbox, itemindex, cmdtext):
        "replace the command in a mapping item"
        item = listbox.GetItem(itemindex)
        listbox.SetItemText(item, 1, cmdtext)

    def ensure_listitem_visible(self, listbox, ix):
        "make sure the selected mapping can be viewed in the list"
        listbox.EnsureVisible(ix)

    def remove_listbox_item(self, listbox, itemindex):
        "delete a mapping from the list"
        # find = listbox.GetItemText(item.GetId(), 0)
        # listbox.DeleteItem(find)
        listbox.DeleteItem(itemindex)  # item.GetId())

    def reset_listitem_icon(self, listbox, ix):
        "find the corresponding keycombo item and unset the check image"
        item = listbox.GetItem(ix)
        item.SetImage(self.todoimage)
        listbox.SetItem(item)

    # def focuskeylist(self, event=None):
    #     "shift focus for selecting a keycombo item"
    #     self.listkeys.SetFocus()

    # def focuscmdlist(self, event=None):
    #     "shift focus for selecting a command item"
    #     self.listcmds.SetFocus()

    # def focusmatchlist(self, event=None):
    #     "shift focus for selecting a mapping item"
    #     self.listmatches.SetFocus()

    # def focusfindkey(self, event=None):
    #     "shift focus to enter a keycombo search phrase"
    #     self.findkeytext.SetFocus()

    # def focusfindcmd(self, event=None):
    #     "shift focus to enter a command search phrase"
    #     self.findcmdtext.SetFocus()

    def set_focus_to(self, widget, event=None):
        "shift focus to a specific screen element"
        widget.SetFocus()

    def popuptext(self, item, colno):
        "show complete text of description if moused over"
        # moet nog wxPython variant voor maken
        # if colno == 1:
        #     item.setToolTip(colno, item.text(colno))

    def get_entry_text(self, win):
        "get a text entry field's text"
        return win.GetValue()

    def get_search_choice(self, control):
        "return the selected item's index for the given list"
        return control.GetSelection()

    def find_listitems(self, win, search, in_col=1):
        "find all items in a list that contain a search text"
        results = []
        itemindex = self.find_in_listbox(win, search, in_col, exact=False)
        while itemindex is not None:  # != -1:
            # print(itemindex)
            results.append(itemindex)
            itemindex = self.find_in_listbox(win, search, in_col, start=itemindex + 1, exact=False)
        # for itemindex in results:
        #     item = win.GetItem(itemindex)
        #     print(item, itemindex, item.GetText(), win.GetItemText(itemindex), 0)
        return results

    def get_selected_item(self, win):
        "get the selected item in a list"
        sel = win.GetFirstSelected()
        if sel != -1:
            self.ensure_listitem_visible(win, sel)
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
        "set the selected item for one of the lists"
        win.Select(itemindex)

    # def count_matches(self):
    #     "get the current number of mappings in the list"
    #     return self.listmatches.GetItemCount()

    # def get_matchitem_data(self, itemindex):
    #     "get the texts for a mapping item"
    #     return (self.get_item_text(self.listmatches, itemindex, 0),
    #             self.get_item_text(self.listmatches, itemindex, 1))

    def reject(self):
        "discard the dialog"
        self.EndModal(wx.ID_CANCEL)

    def accept(self):
        "close the dialog after confirmation"
        self.EndModal(wx.ID_OK)
