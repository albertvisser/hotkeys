"""unittests for ./plugin_examples/mergetool_wx.py
"""
import types
from mockgui import mockwxwidgets as mockwx
from editor.plugins import mergetool_wx as testee


class TestMergeDialogGui:
    """unittests for mergetool_wx.MergeDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for mergetool_wx.MergeDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            "stub"
            print('called MergeDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.MergeDialogGui, '__init__', mock_init)
        testobj = testee.MergeDialogGui()
        assert capsys.readouterr().out == 'called MergeDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'Dialog', mockwx.MockDialog)
        monkeypatch.setattr(testee.wx, 'ImageList', mockwx.MockImageList)
        monkeypatch.setattr(testee.wx, 'ArtProvider', mockwx.MockArtProvider)
        testobj = testee.MergeDialogGui('master', 'parent')
        assert testobj.master == 'master'
        assert isinstance(testobj.imglist, testee.wx.ImageList)
        assert testobj.okimage == 'bitmap'
        assert testobj.todoimage == 'bitmap'
        assert testobj.accel_list == []
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args"
                " () {'title': 'TCCM', 'size': (1500, 900), 'style': 536877120}\n"
                "called ImageList.__init__ with args (16, 16)\n"
                "called ArtProvider.GetBitmap with args ()\n"
                "called ImageList.Add with args ('bitmap',)\n"
                "called ArtProvider.GetBitmap with args ()\n"
                "called ImageList.Add with args ('bitmap',)\n")

    def test_init_display(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.init_display
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.init_display(), testee.wx.BoxSizer)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"

    def test_add_row(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.add_row
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        screen = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.add_row(screen), testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8240, 5)\n")

    def test_add_col_to_row(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.add_col_to_row
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        row = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.add_col_to_row(row), testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (8,)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8192)\n")

    def test_create_list(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_list
        """
        monkeypatch.setattr(testee, 'MyListCtrl', mockwx.MockListCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.imglist = 'imagelist'
        result = testobj.create_list(['col', 'umns'], 'callback')
        assert isinstance(result, mockwx.MockListCtrl)
        assert capsys.readouterr().out == (
            f"called ListCtrl.__init__ with args ({testobj},) {{'style': 8224}}\n"
            "called ListCtrl.InsertColumn with args (0, 'col')\n"
            "called ListCtrl.InsertColumn with args (1, 'umns')\n"
            "called ListCtrl.SetImageList with args ('imagelist', 1)\n"
            f"called ListCtrl.Bind with args ({testee.wx.EVT_LIST_ITEM_SELECTED}, 'callback')\n")

    def test_create_findbutton(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_findbutton
        """
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.create_findbutton(['col', 'umns'])
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                f"called ComboBox.__init__ with args ({testobj},)"
                " {'size': (120, -1), 'choices': ['Find col', 'Find umns'], 'style': 48}\n"
                "called combobox.SetSelection with args (1,)\n")

    def test_create_text(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_text
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.create_text(), testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj},) {{'size': (120, -1)}}\n")

    def test_create_button(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_button
        """
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.create_button('text', 'callback')
        assert isinstance(result, testee.wx.Button)
        assert capsys.readouterr().out == (
                f"called Button.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback') {{}}\n")
        result = testobj.create_button('text', 'callback', size=10)
        assert isinstance(result, testee.wx.Button)
        assert capsys.readouterr().out == (
                f"called Button.__init__ with args ({testobj},)"
                " {'label': 'text', 'size': (10, -1)}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, 'callback') {{}}\n")

    def test_add_row_to_col(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.add_row_to_col
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        col = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_row_to_col(col)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddStretchSpacer\n"
                "called hori sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args MockBoxSizer (1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (0, 8384, 10)\n")
        testobj.add_row_to_col(col, 'x')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.Add with args ('x', 1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8432)\n")
        testobj.add_row_to_col(col, 'x', left_align=True)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.Add with args ('x', 1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8208, 10)\n")
        testobj.add_row_to_col(col, 'x', center=True)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.Add with args ('x', 1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8240, 5)\n")
        testobj.add_row_to_col(col, 'x', right_align=True)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.Add with args ('x', 1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8224, 10)\n")
        testobj.add_row_to_col(col, 'x', 'y', 'z', 'q')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args ('x', 0)\n"
                "called hori sizer.Add with args ('y', 0)\n"
                "called hori sizer.Add with args ('z', 0)\n"
                "called hori sizer.Add with args ('q', 0)\n"
                "called hori sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args MockBoxSizer (1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (0, 8256, 10)\n")
        testobj.add_row_to_col(col, 'x', 'y')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args ('x', 0, 240, 2)\n"
                "called hori sizer.Add with args ('y', 0, 240, 2)\n"
                "called hori sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args MockBoxSizer (1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (0, 8256, 10)\n")

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.finalize_display
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetAutoLayout', mockwx.MockDialog.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        screen = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.finalize_display(screen)
        assert capsys.readouterr().out == ("called dialog.SetAutoLayout with args (True,)\n"
                                           "called dialog.SetSizer with args ( sizer,)\n")

    def test_create_hotkey(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_hotkey
        """
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(testee.wx, 'AcceleratorEntry', mockwx.MockAcceleratorEntry)
        monkeypatch.setattr(testee.wx, 'AcceleratorTable', mockwx.MockAcceleratorTable)
        monkeypatch.setattr(testee.wx.Dialog, 'Bind', mockwx.MockDialog.Bind)
        monkeypatch.setattr(testee.wx.Dialog, 'SetAcceleratorTable',
                            mockwx.MockDialog.SetAcceleratorTable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.accel_list = []
        testobj.create_hotkey('text', 'callback', 'keyseq', 'desc')
        assert len(testobj.accel_list) == 1
        assert isinstance(testobj.accel_list[0], testee.wx.AcceleratorEntry)
        assert capsys.readouterr().out == (
                "called MenuItem.__init__ with args (None, -1, 'text') {}\n"
                f"called dialog.Bind with args ({testee.wx.EVT_MENU}, 'callback')\n"
                "called menuitem.GetId\n"
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('keyseq',)\n")
        testobj.accel_list = []
        testobj.create_hotkey('text', 'callback', 'wrong', 'desc')
        assert len(testobj.accel_list) == 0
        assert capsys.readouterr().out == (
                "called MenuItem.__init__ with args (None, -1, 'text') {}\n"
                f"called dialog.Bind with args ({testee.wx.EVT_MENU}, 'callback')\n"
                "called menuitem.GetId\n"
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('wrong',)\n")
        # testobj.accel_list = []
        testobj.create_hotkey('help', 'callback', 'keyseq', 'desc')
        assert len(testobj.accel_list) == 1
        assert isinstance(testobj.accel_list[0], testee.wx.AcceleratorEntry)
        assert capsys.readouterr().out == (
                "called MenuItem.__init__ with args (None, -1, 'help') {}\n"
                f"called dialog.Bind with args ({testee.wx.EVT_MENU}, 'callback')\n"
                "called menuitem.GetId\n"
                "called AcceleratorEntry.__init__ with args () {'cmd': 'NewID'}\n"
                "called AcceleratorEntry.FromString with args ('keyseq',)\n"
                "called AcceleratorTable.__init__ with 1 AcceleratorEntries\n"
                "called dialog.SetAcceleratorTable\n")

    def test_clear_list(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.clear_list
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_list(listbox)
        assert capsys.readouterr().out == "called ListCtrl.DeleteAllItems\n"

    def test_get_listbox_count(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_listbox_count
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_listbox_count(listbox) == 2
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n")

    def test_add_listitem(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.add_listitem
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_listitem(listbox, 'keytext', 'command') == "itemindex"
        assert capsys.readouterr().out == (
                "called ListCtrl.GetItemCount\n"
                "called ListCtrl.InsertItem with args (2, 'keytext')\n"
                "called ListCtrl.SetItem with args ('itemindex', 1, 'command')\n")

    def test_set_listitem_icon(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.set_listitem_icon
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.okimage = 'okimage'
        testobj.set_listitem_icon(listbox, 'ix')
        assert capsys.readouterr().out == ("called ListCtrl.GetItem with args ('ix',)\n"
                                           "called item.SetImage with arg 'okimage'\n"
                                           "called ListCtrl.SetItem with args (item ix,)\n")

    def test_get_selected_listbox_data(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_selected_listbox_data
        """
        def mock_get(*args):
            print('called ListCtrl.GetItemText with args', args)
            raise IndexError
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_listbox_data(listbox) == (-1, -1, -1)
        assert capsys.readouterr().out == ("called ListCtrl.GetFirstSelected\n"
                                           "called ListCtrl.GetItemText with args (-1, 0)\n"
                                           "called ListCtrl.GetItemText with args (-1, 1)\n")
        listbox.GetItemText = mock_get
        assert testobj.get_selected_listbox_data(listbox) == (-1, '', '')
        assert capsys.readouterr().out == ("called ListCtrl.GetFirstSelected\n"
                                           "called ListCtrl.GetItemText with args (-1, 0)\n"
                                           "called ListCtrl.GetItemText with args (-1, 1)\n")

    def test_find_in_listbox(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.find_in_listbox
        """
        def mock_get(*args):
            print('called ListCtrl.GetItemText with args', args)
            return ['one', 'Two'][args[0]]
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        listbox.GetItemText = mock_get
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_in_listbox(listbox, 'Two') == 1
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n"
                                           "called ListCtrl.GetItemText with args (0, 0)\n"
                                           "called ListCtrl.GetItemText with args (1, 0)\n")
        assert testobj.find_in_listbox(listbox, 'twO') == None
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n"
                                           "called ListCtrl.GetItemText with args (0, 0)\n"
                                           "called ListCtrl.GetItemText with args (1, 0)\n")
        assert testobj.find_in_listbox(listbox, 'twO', col=1, start=1, exact=False) == 1
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n"
                                           "called ListCtrl.GetItemText with args (1, 1)\n")

    def test_replace_listbox_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.replace_listbox_item
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace_listbox_item(listbox, 'itemindex', 'cmdtext')
        assert capsys.readouterr().out == (
                "called ListCtrl.GetItem with args ('itemindex',)\n"
                "called ListCtrl.SetItemText with args (item itemindex, 1, 'cmdtext')\n")

    def test_ensure_listitem_visible(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.ensure_listitem_visible
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ensure_listitem_visible(listbox, 'ix')
        assert capsys.readouterr().out == "called ListCtrl.EnsureVisible with args ('ix',)\n"

    def test_remove_listbox_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.remove_listbox_item
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_listbox_item(listbox, 'itemindex')
        assert capsys.readouterr().out == "called ListCtrl.DeleteItem with args ('itemindex',)\n"

    def test_reset_listitem_icon(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.reset_listitem_icon
        """
        listbox = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.todoimage = 'todoimage'
        testobj.reset_listitem_icon(listbox, 'ix')
        assert capsys.readouterr().out == ("called ListCtrl.GetItem with args ('ix',)\n"
                                           "called item.SetImage with arg 'todoimage'\n"
                                           "called ListCtrl.SetItem with args (item ix,)\n")

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.set_focus_to
        """
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Control.SetFocus\n"

    def _test_popuptext(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.popuptext
        """
        # nog niet gemaakt
        # testobj = self.setup_testobj(monkeypatch, capsys)
        # assert testobj.popuptext(item, colno) == "expected_result"
        # assert capsys.readouterr().out == ("")

    def test_get_entry_text(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_entry_text
        """
        win = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_entry_text(win) == "value from textctrl"
        assert capsys.readouterr().out == "called text.GetValue\n"

    def test_get_search_choice(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_search_choice
        """
        control = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_search_choice(control) == "selection"
        assert capsys.readouterr().out == "called combobox.GetSelection\n"

    def test_find_listitems(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.find_listitems
        """
        def mock_find(*args, **kwargs):
            print('called MergeDialogGui.find_in_listbox with args', args, kwargs)
            start = kwargs.get('start', 0)
            if start > 2:
                return None
            return start + 1
        win = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_in_listbox = mock_find
        assert testobj.find_listitems(win, 'search') == [1, 3]
        assert capsys.readouterr().out == (
                f"called MergeDialogGui.find_in_listbox with args ({win}, 'search', 1)"
                " {'exact': False}\n"
                f"called MergeDialogGui.find_in_listbox with args ({win}, 'search', 1)"
                " {'start': 2, 'exact': False}\n"
                f"called MergeDialogGui.find_in_listbox with args ({win}, 'search', 1)"
                " {'start': 4, 'exact': False}\n")
        assert testobj.find_listitems(win, 'search', in_col=0) == [1, 3]
        assert capsys.readouterr().out == (
                f"called MergeDialogGui.find_in_listbox with args ({win}, 'search', 0)"
                " {'exact': False}\n"
                f"called MergeDialogGui.find_in_listbox with args ({win}, 'search', 0)"
                " {'start': 2, 'exact': False}\n"
                f"called MergeDialogGui.find_in_listbox with args ({win}, 'search', 0)"
                " {'start': 4, 'exact': False}\n")

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_selected_item
        """
        def mock_ensure(*args):
            print('called MergeDialogGui.ensure_listitem_visible with args', args)
        win = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ensure_listitem_visible = mock_ensure
        assert testobj.get_selected_item(win) == -1
        assert capsys.readouterr().out == "called ListCtrl.GetFirstSelected\n"
        win.GetFirstSelected = win.GetFirstSelected_2
        assert testobj.get_selected_item(win) == 0
        assert capsys.readouterr().out == (
                "called ListCtrl.GetFirstSelected\n"
                f"called MergeDialogGui.ensure_listitem_visible with args ({win}, 0)\n")

    def test_get_first_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_first_item
        """
        win = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_first_item(win) == 0
        assert capsys.readouterr().out == ""

    def test_get_last_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_last_item
        """
        win = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_last_item(win) == 1
        assert capsys.readouterr().out == "called ListCtrl.GetItemCount\n"

    def test_get_item_text(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_item_text
        """
        win = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_text(win, 'itemindex', 'col') == "itemindex"
        assert capsys.readouterr().out == (
                "called ListCtrl.GetItemText with args ('itemindex', 'col')\n")

    def test_set_selected_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.set_selected_item
        """
        win = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_selected_item(win, 'itemindex')
        assert capsys.readouterr().out == "called ListCtrl.Select with args ('itemindex',)\n"

    def test_reject(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.reject
        """
        monkeypatch.setattr(testee.wx.Dialog, 'EndModal', mockwx.MockDialog.EndModal)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reject()
        assert capsys.readouterr().out == "called Dialog.EndModal with arg 5101\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.accept
        """
        monkeypatch.setattr(testee.wx.Dialog, 'EndModal', mockwx.MockDialog.EndModal)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.accept()
        assert capsys.readouterr().out == "called Dialog.EndModal with arg 5100\n"
