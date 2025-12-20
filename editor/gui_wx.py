"""HotKeys main program - gui specific code - wxPython version
"""
import wx
import wx.adv
import wx.lib.mixins.listctrl as listmix
from wx.lib.embeddedimage import PyEmbeddedImage
from editor import shared


class MyListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.ListRowHighlighter):
    """base class voor de listcontrol

    maakt het definiëren in de gui class wat eenvoudiger
    """
    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.ListRowHighlighter.__init__(self)


class SingleDataInterface(wx.Panel, listmix.ColumnSorterMixin):
    """base class voor het gedeelte van het hoofdscherm met de listcontrol erin

    voornamelijk nodig om de specifieke verwerkingen met betrekking tot de lijst
    bij elkaar en apart van de rest te houden
    definieert feitelijk een "custom widget"
    """
    def __init__(self, parent, master):
        wx.Panel.__init__(self, parent.pnl)   # niet via super() i.v.m. mixin apart __init__en
        self.parent = parent
        self.master = master
        self.olditem = None
        self._savestates = (False, False)
        self._sizer = wx.BoxSizer(wx.VERTICAL)

    def setup_empty_screen(self, nodata, title):
        """build a subscreen with only a message
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(wx.StaticText(self, label=nodata))
        self._sizer.Add(sizer)

    def setup_list(self, colheaders, colwidths, callback):
        """add the list widget to the interface
        """
        self.imglist = wx.ImageList(16, 16)

        # ik dacht dat ik dit netjes gekopieerd had maar als ik op een kolomheader klik
        # krijg ik toch een traceback. Hij geeft een KeyError in de mixin code: 121 bij DC bijv.
        # ook nadat ik de volgorde van al dit gelijk maak aan die in de demo
        smalluparrow = PyEmbeddedImage(
            b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAADxJ"
            b"REFUOI1jZGRiZqAEMFGke2gY8P/f3/9kGwDTjM8QnAaga8JlCG3CAJdt2MQxDCAUaOjyjKMp"
            b"cRAYAABS2CPsss3BWQAAAABJRU5ErkJggg==")
        # self.sm_up = self.imglist.Add(smalluparrow.GetBitmap())
        self.sm_up = self.imglist.Add(smalluparrow.GetBitmap())

        smalldnarrow = PyEmbeddedImage(
            b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAEhJ"
            b"REFUOI1jZGRiZqAEMFGke9QABgYGBgYWdIH///7+J6SJkYmZEacLkCUJacZqAD5DsInTLhDR"
            b"bcPlKrwugGnCFy6Mo3mBAQChDgRlP4RC7wAAAABJRU5ErkJggg==")
        self.sm_dn = self.imglist.Add(smalldnarrow.GetBitmap())

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        p0list = MyListCtrl(self, size=(1140, 594), style=wx.LC_REPORT | wx.BORDER_SUNKEN
                            # | wx.LC_HRULES
                            | wx.LC_SINGLE_SEL)
        for col, title in enumerate(colheaders):
            p0list.AppendColumn(title)
            p0list.SetColumnWidth(col, colwidths[col])

        # self.Bind(wx.EVT_LIST_ITEM_SELECTED, callback, p0list)
        p0list.Bind(wx.EVT_LIST_ITEM_SELECTED, callback)
        # self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_item_deselected, p0list)
        p0list.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_item_deselected)
        # self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated, p0list)
        p0list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_item_activated)

        p0list.SetImageList(self.imglist, wx.IMAGE_LIST_SMALL)

        sizer.Add(p0list, 1, wx.EXPAND | wx.ALL, 5)
        self._sizer.Add(sizer)
        return p0list

    def start_extrapanel(self, frameheight):
        "start a new area for screen widgets"
        self._frm = wx.Panel(self, size=(-1, frameheight + 30))
        self._sizer.Add(self._frm, 0, wx.EXPAND | wx.LEFT | wx.RIGHT)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.AddSpacer(5)
        self._frm.SetSizer(vsizer)
        return vsizer

    def start_line(self, vsizer):
        "start a new line of widgets in the given screen"
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer.Add(hsizer, 0, wx.EXPAND | wx.ALL, 5)
        return hsizer

    def add_label_to_line(self, hsizer, text, add=True):
        "add the given text to the given screen line"
        fld = wx.StaticText(self._frm, label=text + " ")
        if add:
            hsizer.Add(fld, 0, wx.ALIGN_CENTER_VERTICAL)
        return fld

    def add_textfield_to_line(self, hsizer, width=None, callback=None, add=True):
        "add a field to enter text on the given screen line"
        if not width:
            width = -1
        fld = wx.TextCtrl(self._frm, size=(width, -1))
        if callback:
            fld.Bind(wx.EVT_TEXT, callback)
        if add:
            hsizer.Add(fld, 0, wx.ALIGN_CENTER_VERTICAL)
        return fld

    def add_combobox_to_line(self, hsizer, items, width=None, add=True):
        "add a combobox with the given caption and a standard callback"
        if not width:
            width = -1
        cmb = wx.ComboBox(self._frm, size=(width, -1), style=wx.CB_READONLY, choices=items)
        cmb.Bind(wx.EVT_COMBOBOX, self.master.on_combobox)
        if add:
            hsizer.Add(cmb, 0, wx.ALIGN_CENTER_VERTICAL)
        return cmb

    def add_checkbox_to_line(self, hsizer, text):
        "add a checkbox with the given caption and a standard callback"
        cb = wx.CheckBox(self._frm, label=text)
        cb.SetValue(False)
        cb.Bind(wx.EVT_CHECKBOX, self.master.on_checkbox)
        hsizer.Add(cb, 0, wx.ALIGN_CENTER_VERTICAL)
        return cb

    def add_separator_to_line(self, hsizer):
        "separate the keydef from the definition"
        hsizer.AddStretchSpacer()

    def add_button_to_line(self, hsizer, text, callback):
        "add a button with the given text and callback"
        btn = wx.Button(self._frm, label=text)
        btn.Enable(False)
        btn.Bind(wx.EVT_BUTTON, callback)
        hsizer.Add(btn, 0)
        return btn

    def add_descfield_to_line(self, hsizer):
        "add a text field for the description"
        fld = wx.TextCtrl(self._frm, style=wx.TE_MULTILINE | wx.TE_READONLY)
        hsizer.Add(fld, 1, wx.EXPAND | wx.ALL, 5)
        return fld

    def set_extrapanel_editable(self, screenfields, buttons, switch):
        """open up fields in extra screen when applicable
        """
        for widget in screenfields:
            widget.Enable(switch)
        if switch:
            state_s, state_d = self._savestates
        else:
            self._savestates = (buttons[0].IsEnabled(), buttons[1].IsEnabled())
            state_s, state_d = False, False
        buttons[0].Enable(state_s)
        buttons[1].Enable(state_d)

    def finalize_screen(self):
        "last actions to add the screen to the display"
        self.itemDataMap = {int(x): y for x, y in self.master.data.items()}
        listmix.ColumnSorterMixin.__init__(self, len(self.master.column_info))
        self.SortListItems(0, True)
        self.master.p0list.RefreshRows()
        self.master.p0list.Select(0)

        self.SetAutoLayout(True)
        self.SetSizer(self._sizer)
        self._sizer.Fit(self)

    def resize_if_necessary(self):
        """to be called on changing the language
        """
        # self.toplinesizer.Layout()
        # misschien is dit bij wx variant nodig terwijl het bij de qt variant vanzelf gebeurt?
        # of zitten nu alle mogelijke topline velden in de main code en is dit niet meer nodig?

    def on_item_deselected(self, event):
        """callback op het niet meer geselecteerd zijn van een item

        onthou het item om later te vragen of de key definitie moet worden bijgewerkt
        """
        if self.master.initializing_screen:
            return
        item = event.GetItem()
        if not item:  # bv. bij p0list.clear()
            return
        self.olditem = item

    def on_item_selected(self, event):
        """callback op het selecteren van een item
        """
        item = event.GetItem()
        if self.master.has_extrapanel and item:
            self.master.process_changed_selection(item, self.olditem)
            event.Skip()

    def on_item_activated(self, event):
        """callback op het activeren van een item (onderdeel van het selecteren)
        """
        # print('in on_item_activated', event)
        self.current_item = event.GetItem()  # GetEventIndex()
        # uitgezocht dat dit nergens (meer) wordt gebruikt

    def set_focus_to(self, widget):
        "set the field to start inputting data"
        widget.SetFocus()

    def update_columns(self, p0list, oldcount, newcount):
        "delete and insert columns"
        hlp = oldcount
        while hlp > newcount:
            p0list.DeleteColumn(0)
            hlp -= 1
        hlp = newcount
        while hlp > oldcount:
            p0list.AppendColumn('')
            hlp -= 1

    def refresh_headers(self, p0list, column_info):
        "apply changes in the column headers"
        for indx, coldata in enumerate(column_info):
            hdr = p0list.GetColumn(indx)
            hdr.SetText(coldata[0])
            hdr.SetWidth(coldata[1])
            p0list.SetColumn(indx, hdr)
        p0list.resizeLastColumn(100)   # misschien te weinig

    def GetListCtrl(self):
        """ten behoeve van de columnsorter mixin"""
        return self.master.p0list

    def GetSortImages(self):
        """ten behoeve van de columnsorter mixin"""
        return (self.sm_dn, self.sm_up)

    def OnSortOrderChanged(self):
        """ten behoeve van de columnsorter mixin
        na het sorteren moeten de regels weer om en om gekleurd worden"""
        self.master.p0list.RefreshRows()

    def set_title(self, title):
        """set screen title
        """
        self.master.parent.parent.gui.SetTitle(title)

    def clear_list(self, p0list):
        "reset listcontrol"
        p0list.DeleteAllItems()

    def build_listitem(self, key):
        "create a new item for the list"
        # # item = wx.ListItem()
        # # item.SetData(key)
        # itemlist = [key]  # item]
        # return itemlist  # "new_item" is in dit geval een list
        indx = self.master.p0list.Append(key)
        self.master.p0list.SetItemData(indx, int(key))
        return indx

    # def set_listitemtext(self, itemlist, indx, value):
    def set_listitemtext(self, itemindex, columnindex, value):
        "set the text for a list item"
        # # print('item', itemlist, 'index', indx, 'value', value)
        # # "new_item" is in dit geval een list die verderop wordt toegevoegd aan de control
        # # self.p0list.SetItem(item, indx, value)
        # # if indx == 0:
        # #     item = itemlist.pop()
        # # else:
        # #     item = wx.ListItem()
        # # item.SetColumn(indx)
        # # item.SetText(value)
        # itemlist.append(value)
        # return itemlist
        self.master.p0list.SetItem(itemindex, columnindex, value)

    # def add_listitem(self, p0list, itemlist):
    def add_listitem(self, p0list, itemindex):
        "add an item to the list"
        # build_item heeft dit hier eigenlijk al gedaan
        # key = itemlist.pop(0)
        # indx = p0list.Append(itemlist)
        # for ix, value in enumerate(itemlist):
        #     p0list.SetItem(indx, ix, value)
        # p0list.SetItemData(indx, int(key))

    def set_listselection(self, p0list, pos):
        "highlight the selected item in the list"
        p0list.Select(pos)

    def getfirstitem(self, p0list):
        "return first item in list"
        return p0list.GetItem(0)

    def get_listitem_at_position(self, p0list, item):
        "return the index of a given keydef entry"
        return item.GetId()  # indexOfTopLevelItem(item)

    def get_itemdata(self, item):
        "return the data associated with a listitem"
        return str(item.GetData())

    def get_listbox_selection(self, p0list):
        "return the currently selected keydef and its position in the list"
        pos = p0list.GetFirstSelected()
        return p0list.GetItem(pos), pos

    def get_listitem_position(self, p0list, item):
        "return the index of a given keydef entry"
        raise NotImplementedError

    def get_widget_text(self, event):
        "return the text entered in a textfield"
        return event.GetEventWidget().GetValue()

    def set_textfield_value(self, txt, value):
        "set the text for a textfield"
        txt.SetValue(value)

    def enable_button(self, button, state):
        "make button accessible"
        button.Enable(state)

    def get_choice_value(self, event):
        """return the value chosen in a combobox (and the widget itself)

        this method is used from within the onchange callback
        """
        cb = event.GetEventWidget()
        return cb, cb.GetValue()

    def get_combobox_value(self, cb):
        "return the text entered/selected in a combobox"
        return cb.GetValue()
        # return cmb.GetStringSelection()
        # return cb.GetText() - staat niet in de documentatie van dit ComboBox of TextEntry

    def init_combobox(self, cb, choices=None):
        "initialize combobox to a set of new values"
        cb.Clear()
        if choices is not None:
            cb.AppendItems(choices)

    def set_combobox_string(self, cmb, value, valuelist):
        "set the selection for a combobox"
        # print('in set_combobox_string')
        try:
            ix = valuelist.index(value)
        except ValueError:
            # print('exit on exception', value, 'not in', valuelist)
            return
        cmb.SetSelection(ix)

    def set_label_text(self, lbl, value):
        "set the text for a label / static text"
        lbl.SetLabel(value)

    # used by on_checkbox
    def get_check_value(self, event):
        """return the state set in a checkbox (and the widget itself)

        this method is used from within the onchange callback
        """
        cb = event.GetEventWidget()
        return cb, cb.GetValue()

    def get_checkbox_state(self, cb):
        "return the state set in a checkbox (without the widget)"
        return cb.GetValue()

    def set_checkbox_state(self, cb, state):
        "set the state for a checkbox"
        cb.SetValue(state)


class TabbedInterface(wx.Panel):
    """ Als wx.NoteBook, maar met selector in plaats van tabs
    """
    def __init__(self, parent, master):
        super().__init__(parent)
        self.parent = parent
        self.master = master

    def setup_selector(self, callback):
        "create the selector"
        # print('in setup_selector')
        sel = wx.ComboBox(self, size=(140, -1), style=wx.CB_READONLY)
        sel.Bind(wx.EVT_COMBOBOX, callback)  # self.after_changing_page)
        # als ik echt met een choicebook werkte, kon ik deze *twee*  gebruiken:
        # self.book.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.OnPageChanged)
        # self.book.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.pnl = wx.Simplebook(self)
        # self.pnl = wx.Choicebook(self)
        return sel

    def add_subscreen(self, win):
        "add a screen to the tabbed widget"
        self.pnl.AddPage(win, '')

    def add_to_selector(self, selector, txt):
        "add an option to the selector"
        selector.Append(txt)

    def start_display(self):
        "build the screen container"
        vbox = wx.BoxSizer(wx.VERTICAL)
        return vbox

    def start_line(self, vbox):
        "add a line to the screen container"
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox.Add(hbox, 0, wx.EXPAND)
        return hbox

    def add_margin_to_line(self, hbox):
        "add the fixed margin"
        hbox.AddSpacer(10)

    def add_text_to_line(self, hbox, text=""):
        "add a fixed text"
        text = wx.StaticText(self, label=text)  # , size=(80, -1))
        hbox.Add(text, 0, wx.ALIGN_CENTER_VERTICAL)
        return text

    def add_selector_to_line(self, hbox, widget):
        "add the book selector to the line"
        hbox.Add(widget, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

    def add_combobox_to_line(self, hbox, minwidth=0, editable=False, callback=None):
        "add a combobox selector"
        # size = (-1, -1) if minwidth == 0 else (minwidth, -1)
        style = wx.CB_READONLY if not editable else wx.CB_DROPDOWN
        # if minwidth:
        #     cmb = wx.ComboBox(self, size=(minwidth, -1), style=style)
        # else:
        #     cmb = wx.ComboBox(self, style=style)
        cmb = wx.ComboBox(self, style=style)
        if callback:
            cmb.Bind(wx.EVT_TEXT, callback)
        hbox.Add(cmb, 0, wx.ALIGN_CENTER_VERTICAL)
        # hbox.Add(self.find_loc, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        return cmb

    def add_separator_to_line(self, hbox):
        "separate the selector from the search-related widgets"
        hbox.AddStretchSpacer()

    def add_button_to_line(self, hbox, text, callback, enabled):
        "add a button with the given text and callback "
        btn = wx.Button(self, label=text)
        btn.Bind(wx.EVT_BUTTON, callback)
        btn.Enable(enabled)
        hbox.Add(btn, 0)
        return btn

    def add_list_to_line(self, hbox):
        "add the list with keydefs to the display"
        hbox.Add(self.pnl, 0)

    def finalize_display(self, vbox):
        "realize the layout"
        self.SetAutoLayout(True)
        self.SetSizer(vbox)
        vbox.Fit(self)
        # vbox.SetSizeHints(self)
        self.Show()

    def setcaption(self, widget, caption):
        "set the given widget's caption (this is intended for label fields)"
        widget.SetLabel(caption)

    def on_pagechange(self, event):  # after_changing_page(self, event):
        """callback for change in tool page selector
        """
        self.master.on_page_changed(event.GetEventObject().GetSelection())

    # used by on_page_changed
    def get_panel(self):
        "return the currently selected panel's index"
        return self.pnl.GetCurrentPage()

    # def get_selected_tool(self):
    #     "return the currently selected panel's name"
    #     return self.sel.GetStringSelection()

    def set_selected_panel(self, indx):
        "set the index of the panel to be selected"
        self.pnl.SetSelection(indx)

    def get_selected_panel(self, indx):
        "return index and handle of the selected panel"
        # indx = self.sel.GetSelection()
        win = self.pnl.GetPage(indx)
        return win

    def replace_panel(self, indx, win, newwin):
        "replace a panel with a modified version"
        self.pnl.InsertPage(indx, newwin)
        self.pnl.SetSelection(newwin)  # or ChangeSelection to avoid sending events
        self.pnl.RemovePage(win)

    # def set_panel_editable(self, test_redef):
    #     "(re)set editability of the current panel"
    #     win = self.pnl.GetCurrentPage()
    #     win.set_extrapanel_editable(test_redef)

    def enable_widget(self, widget, state):
        "make the specified widget usable (or not)"
        widget.Enable(state)

    # def update_search(self, items):
    #     "refresh the search-related widgets"
    def refresh_combobox(self, cmb, items=None):
        "refill the values for the given checkbox and select the last one"
        cmb.Clear()
        if items:
            cmb.AppendItems(items)
            cmb.SetSelection(len(items) - 1)

    def get_combobox_value(self, cmb):
        "return the given combobox's value"
        # return cmb.GetStringSelection()
        return cmb.GetValue()

    def set_combobox_text(self, cmb, text):
        "set the text for the given combobox"
        cmb.SetValue(text)
        if text:
            cmb.Enable(True)

    def get_combobox_index(self, cmb):
        "get index of selected item"
        return cmb.GetSelection()

    def on_textchange(self, event):     # after_changing_text(self, event):
        """callback for change in search text
        """
        text = event.GetEventObject().GetValue()
        if text:
            self.master.on_text_changed(text)

    # used by on_text_changed
    def get_search_col(self, cb):
        "return the currently selected search column"
        return cb.GetStringSelection()

    # def get_new_selection(self, item):
    def get_combobox_index_for_item(self, cb, item):
        "find the index to set the new selection to"
        return cb.GetSelection()  # findText(item)

    # def set_selected_tool(self, selection):
    def set_combobox_index(self, selector, selection):
        "set the new selection index"
        selector.SetSelection(selection)

    # used by filter
    def get_button_text(self, button):
        "return the current text of the filter button"
        return button.GetLabel()

    def set_button_text(self, button, state):
        "set the text for the filter button"
        button.SetLabel(state)

    def find_items(self, p0list, zoekcol, text):
        "return the items that contain the text to search for"
        result = []
        for i in range(p0list.GetItemCount()):
            # item = page.gui.p0list.GetItem(i)
            if text in p0list.GetItemText(i, zoekcol):
                result.append(i + 1)  # tem) - geen items maar indexes in de lijst opnemen
        return result

    def set_selected_keydef_item(self, p0list, items, index):
        "select a search result in the list"
        item = items[index]
        p0list.Select(item)
        p0list.EnsureVisible(item)

    # def get_search_text(self):
    #     "return the text to search for"
    #     return self.find.GetValue()

    def get_found_keydef_position(self, p0list):
        "return the position marker of the current search result"
        item = p0list.GetFirstSelected()
        return p0list.GetItemText(item, 0), p0list.GetItemText(item, 1)

    def set_found_keydef_position(self, p0list, pos):
        "find the next search rel=sult acoording to position marker(?)"
        for i in range(p0list.GetItemCount()):
            if (p0list.GetItemText(i, 0), p0list.GetItemText(i, 1)) == pos:
                p0list.Select(i)
                break

    # hulproutines t.b.v. managen bestandslocaties

    # def clear_selector(self):
    #     "reset selector"
    #     self.sel.Clear()

    def remove_tool(self, indx, program, program_list):
        """remove a tool from the confguration"""
        win = self.pnl.GetPage(indx)
        self.pnl.RemovePage(indx)
        if program in program_list:
            return win.master   # keep the widget (will be re-added)
        win.Destroy()           # lose the widget
        return None             # explicit return to accentuate difference

    # hulproutines t.b.v. managen tool specifieke settings

    # hulproutine t.b.v. managen column properties

    # def refresh_locs(self, headers):
    #     "apply changes in the selector for `search in column`"
    #     self.find_loc.Clear()
    #     self.find_loc.AppendItems(headers)

    # hulpfunctie t.b.v. afsluiten: bepalen te onthouden tool

    # def get_selected_text(self):
    #     "get text of selected item"
    #     return self.sel.GetStringselection()


class Gui(wx.Frame):
    """Hoofdscherm van de applicatie"""
    def __init__(self, parent=None):
        self.editor = parent
        self.app = wx.App()
        wid = 1140 if shared.LIN else 688
        hig = 594
        super().__init__(None, size=(wid, hig), style=wx.DEFAULT_FRAME_STYLE
                         # | wx.BORDER_SIMPLE
                         | wx.NO_FULL_REPAINT_ON_RESIZE)
        self.sb = self.CreateStatusBar()
        self.menu_bar = wx.MenuBar()
        self.menuitems = {}
        self.SetMenuBar(self.menu_bar)

    def start_display(self):
        "setup the screen container"
        sizer = wx.BoxSizer(wx.VERTICAL)
        return sizer

    def add_choicebook_to_display(self, vbox, bookgui):
        "main portion of the interface"
        vbox.Add(bookgui, 1, wx.EXPAND | wx.ALL, 5)

    def add_exitbutton_to_display(self, vbox, buttondef):
        "a single button at the bottom"
        text, callback = buttondef
        btn = wx.Button(self, label=text)
        btn.Bind(wx.EVT_BUTTON, callback)
        vbox.Add(btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        return btn

    def go(self, sizer):
        "finish and show the interface"
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
                    subsel, value = sel
                    callback, shortcut = value
                    if callable(callback):
                        menutext = '\t'.join((self.editor.captions[subsel], shortcut))
                        item = wx.MenuItem(None, -1, text=menutext)
                        self.menuitems[subsel] = item, shortcut
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
                        menu.AppendSubMenu(submenu, self.editor.captions[subsel])
                        self.menuitems[subsel] = submenu, ''
            if has_items:
                oldmenu = self.menu_bar.Replace(ix, menu, self.editor.captions[title])
                oldmenu.Destroy()
            else:
                self.menu_bar.Append(menu, self.editor.captions[title])
            self.menuitems[title] = menu, ''
            ix += 1

    # def setcaptions(self):
    def update_menutitles(self):
        "set title for menuitem or action"
        topmenus = [x[0] for x in self.menu_bar.GetMenus()]
        for menu, item in self.menuitems.items():
            subitem, shortcut = item
            try:
                oldtitle = subitem.GetTitle()  # als deze kan dan is het een menu
            except AttributeError:
                subitem.SetItemLabel('\t'.join((self.editor.captions[menu], shortcut)))
            else:
                # dit stelt de titel van het menu in
                subitem.SetTitle(self.editor.captions[menu])
                # maar ik zoek de titel van het bijbehorende menuitem (in het bovenliggende menu)
                pmenu = subitem.GetParent()
                if pmenu:
                    for m_item in pmenu.GetMenuItems():
                        if m_item.IsSubMenu():
                            pmenu.SetLabel(m_item.GetId(), self.editor.captions[menu])
                else:
                    self.menu_bar.Replace(topmenus.index(subitem), subitem,
                                          self.editor.captions[menu])

    # hulproutine t.b.v. managen tool specifieke settings

    def modify_menuitem(self, caption, setting):
        "enable/disable menu option identified by caption"
        self.menuitems[caption][0].Enable(setting)
