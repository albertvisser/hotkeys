"""unittests for ./editor/gui_wx.py
"""
import types
import pytest
from mockgui import mockwxwidgets as mockwx
from editor import wxgui as testee


class MockGui:
    """testdouble for gui.Gui object
    """


class MockTabbedInterface:
    """testdouble for gui_qt.TabbedInterface object
    """
    def on_combobox(self):
        "dummy callback"


class MockSDI:
    """testdouble for gui_qt.SingleDataInterface object
    """


class MockHotkeyPanel:
    """testdouble for main.HotkeyPanel object
    """
    def process_changed_selection(self, *args):
        "stub for method call"
        print('called HotkeyPanel.process_changed_selection with args', args)
    def apply_changes(self):
        "stub for method call"
        print('called HotkeyPanel.apply_changes')
    def apply_deletion(self):
        "stub for method call"
        print('called HotkeyPanel.apply_deletion')


class MockChoiceBook:
    """testdouble for main.TabbedWidget object
    """
    def __init__(self):
        self.gui = MockTabbedInterface()
        self.page = MockHotkeyPanel()
    def on_page_changed(selfi, *args):
        print("called ChoiceBook.om_page_changed with args", args)
    def on_text_changed(self, *args):
        print("called ChoiceBook.om_text_changed with args", args)
    def find_next(self):
        "stub for method call"
    def find_prev(self):
        "stub for method call"
    def filter(self):
        "stub for method call"


class MockEditor:
    """testdouble for main.Editor object
    """
    def __init__(self):
        self.book = MockChoiceBook()


class TestGui:
    """unittest for gui_wx.Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Gui.__init__ with args', args)
        monkeypatch.setattr(testee.Gui, '__init__', mock_init)
        testobj = testee.Gui()
        assert capsys.readouterr().out == 'called Gui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Gui.__init__
        """
        monkeypatch.setattr(testee.wx.Frame, '__init__', mockwx.MockFrame.__init__)
        monkeypatch.setattr(testee.wx.Frame, 'CreateStatusBar', mockwx.MockFrame.CreateStatusBar)
        monkeypatch.setattr(testee.wx, 'MenuBar', mockwx.MockMenuBar)
        monkeypatch.setattr(testee.wx.Frame, 'SetMenuBar', mockwx.MockFrame.SetMenuBar)
        master = MockEditor()
        testee.shared.LIN = False
        testobj = testee.Gui(master)
        assert testobj.editor == master
        assert isinstance(testobj.app, testee.wx.App)
        assert isinstance(testobj.sb, mockwx.MockStatusBar)
        assert isinstance(testobj.menu_bar, mockwx.MockMenuBar)
        assert testobj.menuitems == {}
        assert capsys.readouterr().out == (
                "called frame.__init__ with args (None,) {'size': (688, 594), 'style': 541072960}\n"
                "called Frame.CreateStatusBar\n"
                "called StatusBar.__init__\n"
                "called MenuBar.__init__ with args ()\n"
                "called Frame.SetMenuBar with args (A MenuBar,)\n")
        testee.shared.LIN = False
        testobj = testee.Gui(master)
        assert testobj.editor == master
        assert isinstance(testobj.app, testee.wx.App)
        assert isinstance(testobj.sb, mockwx.MockStatusBar)
        assert isinstance(testobj.menu_bar, mockwx.MockMenuBar)
        assert testobj.menuitems == {}
        assert capsys.readouterr().out == (
                "called frame.__init__ with args (None,) {'size': (688, 594), 'style': 541072960}\n"
                "called Frame.CreateStatusBar\n"
                "called StatusBar.__init__\n"
                "called MenuBar.__init__ with args ()\n"
                "called Frame.SetMenuBar with args (A MenuBar,)\n")

    def test_start_display(self, monkeypatch, capsys):
        """unittest for Gui.start_display
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.start_display()
        assert isinstance(result, testee.wx.BoxSizer)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"

    def test_add_choicebook_to_display(self, monkeypatch, capsys):
        """unittest for Gui.add_choicebook_to_display
        """
        vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_choicebook_to_display(vbox, 'book')
        assert capsys.readouterr().out == "called  sizer.Add with args ('book', 1, 8432, 5)\n"

    def test_add_exitbutton_to_display(self, monkeypatch, capsys):
        """unittest for Gui.add_exitbutton_to_display
        """
        def callback():
            "dummy function just for reference"
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_exitbutton_to_display(vbox, ('exit', callback))
        assert capsys.readouterr().out == (
                f"called Button.__init__ with args ({testobj},) {{'label': 'exit'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback}) {{}}\n"
                "called  sizer.Add with args MockButton (0, 256)\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for Gui.go
        """
        monkeypatch.setattr(testee.wx.Frame, 'SetMenuBar', mockwx.MockFrame.SetMenuBar)
        monkeypatch.setattr(testee.wx.Frame, 'SetSizer', mockwx.MockFrame.SetSizer)
        monkeypatch.setattr(testee.wx.Frame, 'SetAutoLayout', mockwx.MockFrame.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Frame, 'Show', mockwx.MockFrame.Show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.app = mockwx.MockApp()
        sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called app.__init__ with args ()\n"
                                           "called BoxSizer.__init__ with args ()\n")
        testobj.go(sizer)
        assert capsys.readouterr().out == ("called Frame.SetSizer with args ( sizer,)\n"
                                           "called Frame.SetAutoLayout with args (True,)\n"
                                           f"called  sizer.Fit with args ({testobj},)\n"
                                           "called frame.Show with args (True,)\n"
                                           "called app.MainLoop\n")

    def test_close(self, monkeypatch, capsys):
        """unittest for Gui.close
        """
        monkeypatch.setattr(testee.wx.Frame, 'Close', mockwx.MockFrame.Close)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.close()
        assert capsys.readouterr().out == ("called Frame.Close with arg True\n")

    def test_set_window_title(self, monkeypatch, capsys):
        """unittest for Gui.set_window_title
        """
        monkeypatch.setattr(testee.wx.Frame, 'SetTitle', mockwx.MockFrame.SetTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_window_title('title')
        assert capsys.readouterr().out == "called Frame.SetTitle with args ('title',)\n"

    def test_statusbar_message(self, monkeypatch, capsys):
        """unittest for Gui.statusbar_message
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sb = mockwx.MockStatusBar()
        assert capsys.readouterr().out == "called StatusBar.__init__\n"
        testobj.statusbar_message('message')
        assert capsys.readouterr().out == "called statusbar.SetStatusText with args ('message',)\n"

    def test_setup_menu(self, monkeypatch, capsys):
        """unittest for Gui.setup_menu
        """
        def callback():
            "empty function just for reference"
        def mock_get(self):
            print('called MenuBar.GetMenus')
            return []
        def mock_get_2(self):
            print('called MenuBar.GetMenus')
            return ['x']
        def mock_getdata():
            print('called Editor.get_menudata')
            return []
        def mock_getdata_2():
            print('called Editor.get_menudata')
            return [('xxx', []), ('yyy', [-1])]
        def mock_getdata_3():
            print('called Editor.get_menudata')
            return [('menu', [('menuitem', (callback, 'keycombo'))]),
                    ('menu', [('submenu', [(('menuitem', (callback, 'keycombo')),), ''])])]
        def mock_bind(self, *args, **kwargs):
            # print('called Frame.Bind with args', args[:2])
            print('called Frame.Bind with args', args, kwargs)
        def mock_replace(self, *args):
            print('called menubar.Replace with args', args)
            return oldmenu
        monkeypatch.setattr(testee.wx, 'Menu', mockwx.MockMenu)
        monkeypatch.setattr(testee.wx, 'MenuItem', mockwx.MockMenuItem)
        monkeypatch.setattr(mockwx.MockMenuBar, 'GetMenus', mock_get)
        monkeypatch.setattr(testee.wx.Frame, 'Bind', mock_bind)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menu_bar = mockwx.MockMenuBar()
        testobj.menuitems = {}
        assert capsys.readouterr().out == "called MenuBar.__init__ with args ()\n"
        testobj.editor = types.SimpleNamespace(get_menudata=mock_getdata,
                                               captions={'xxx': 'X', 'yyy': 'Y'})
        testobj.setup_menu()
        assert capsys.readouterr().out == ("called MenuBar.GetMenus\n"
                                           "called Editor.get_menudata\n")
        testobj.editor.get_menudata = mock_getdata_2
        testobj.setup_menu()
        assert capsys.readouterr().out == ("called MenuBar.GetMenus\n"
                                           "called Editor.get_menudata\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called menubar.Append with args (A Menu, 'X')\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called menu.AppendSeparator with args ()\n"
                                           "called menubar.Append with args (A Menu, 'Y')\n")
        testobj.editor.captions = {'menu': 'menutext', 'menuitem': 'menuitemtext',
                                   'submenu': 'submenutext'}
        testobj.editor.get_menudata = mock_getdata_3
        testobj.setup_menu()
        assert capsys.readouterr().out == (
                "called MenuBar.GetMenus\n"
                "called Editor.get_menudata\n"
                "called Menu.__init__ with args ()\n"
                "called MenuItem.__init__ with args (None, -1) {'text': 'menuitemtext\\tkeycombo'}\n"
                "called menu.Append with args MockMenuItem\n"
                "called menuitem.GetId\n"
                "called Frame.Bind with args"
                f" ({testee.wx.EVT_MENU}, {callback}) {{'id': 'NewID'}}\n"
                "called menubar.Append with args (A Menu, 'menutext')\n"
                "called Menu.__init__ with args ()\n"
                "called Menu.__init__ with args ()\n"
                "called MenuItem.__init__ with args (None, -1) {'text': 'menuitemtext\\tkeycombo'}\n"
                "called menu.Append with args MockMenuItem\n"
                "called menuitem.GetId\n"
                "called Frame.Bind with args"
                f" ({testee.wx.EVT_MENU}, {callback}) {{'id': 'NewID'}}\n"
                "called menu.AppendSubMenu with args (A Menu, 'submenutext')\n"
                "called menubar.Append with args (A Menu, 'menutext')\n")
        oldmenu = mockwx.MockMenu()
        assert capsys.readouterr().out == "called Menu.__init__ with args ()\n"
        monkeypatch.setattr(mockwx.MockMenuBar, 'GetMenus', mock_get_2)
        monkeypatch.setattr(mockwx.MockMenuBar, 'Replace', mock_replace)
        testobj.editor.get_menudata = mock_getdata_2
        testobj.editor.captions = {'xxx': 'X', 'yyy': 'Y'}
        testobj.setup_menu()
        assert capsys.readouterr().out == ("called MenuBar.GetMenus\n"
                                           "called Editor.get_menudata\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called menubar.Replace with args (0, A Menu, 'X')\n"
                                           "called menu.Destroy\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called menu.AppendSeparator with args ()\n"
                                           "called menubar.Replace with args (1, A Menu, 'Y')\n"
                                           "called menu.Destroy\n")

    def test_update_menutitles(self, monkeypatch, capsys):
        """unittest for Gui.setcaptions
        """
        def mock_get():
            print('called MenuBar.GetMenus')
            return [(testmenu,)]
        def mock_getitems(self):
            print('called menu.GetMenuItems')
            return [testmenuitem]
        def mock_getparent(self):
            print('called menu.GetParent')
            return parentmenu
        def mock_is(self):
            print('called menuitem.IsSubMenu')
            return True
        monkeypatch.setattr(mockwx.MockMenuBar, 'GetMenus', mock_get)
        testmenu = mockwx.MockMenu()
        parentmenu = mockwx.MockMenu()
        testmenuitem = mockwx.MockMenuItem()
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called Menu.__init__ with args ()\n"
                                           "called MenuItem.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menu_bar = mockwx.MockMenuBar
        testobj.menuitems = {}
        testobj.update_menutitles()
        assert capsys.readouterr().out == "called MenuBar.GetMenus\n"
        testobj.editor = types.SimpleNamespace(captions={'menu': 'xxxxx', 'menuitem': 'yyyyyy'})
        testobj.menuitems = {'menu': (testmenu, 'xx'),
                             'menuitem': (testmenuitem, 'yy')}
        testobj.update_menutitles()
        assert capsys.readouterr().out == ("called MenuBar.GetMenus\n"
                                           "called menu.GetTitle\n"
                                           "called menu.SetTitle with arg 'xxxxx'\n"
                                           "called menu.GetParent\n"
                                           "called menubar.Replace with args (A Menu, 'xxxxx')\n"
                                           "called menuitem.SetItemLabel with arg 'yyyyyy\tyy'\n")
        monkeypatch.setattr(mockwx.MockMenu, 'GetParent', mock_getparent)
        testobj.update_menutitles()
        assert capsys.readouterr().out == ("called MenuBar.GetMenus\n"
                                           "called menu.GetTitle\n"
                                           "called menu.SetTitle with arg 'xxxxx'\n"
                                           "called menu.GetParent\n"
                                           "called menu.GetMenuItems\n"
                                           "called menuitem.SetItemLabel with arg 'yyyyyy\tyy'\n")
        monkeypatch.setattr(mockwx.MockMenu, 'GetMenuItems', mock_getitems)
        testobj.update_menutitles()
        assert capsys.readouterr().out == ("called MenuBar.GetMenus\n"
                                           "called menu.GetTitle\n"
                                           "called menu.SetTitle with arg 'xxxxx'\n"
                                           "called menu.GetParent\n"
                                           "called menu.GetMenuItems\n"
                                           "called menuitem.IsSubMenu\n"
                                           "called menuitem.SetItemLabel with arg 'yyyyyy\tyy'\n")
        monkeypatch.setattr(mockwx.MockMenuItem, 'IsSubMenu', mock_is)
        testobj.update_menutitles()
        assert capsys.readouterr().out == ("called MenuBar.GetMenus\n"
                                           "called menu.GetTitle\n"
                                           "called menu.SetTitle with arg 'xxxxx'\n"
                                           "called menu.GetParent\n"
                                           "called menu.GetMenuItems\n"
                                           "called menuitem.IsSubMenu\n"
                                           "called menuitem.GetId\n"
                                           "called menu.SetLabel with args ('NewID', 'xxxxx')\n"
                                           "called menuitem.SetItemLabel with arg 'yyyyyy\tyy'\n")

    def test_modify_menuitem(self, monkeypatch, capsys):
        """unittest for Gui.modify_menuitem
        """
        m_item = mockwx.MockMenuItem()
        assert capsys.readouterr().out == "called MenuItem.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menuitems = {'caption': [m_item]}
        testobj.modify_menuitem('caption', 'setting')
        assert capsys.readouterr().out == "called menuitem.Enable with arg setting\n"


class TestTabbedInterface:
    """unittest for gui_wx.TabbedInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.TabbedInterface object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TabbedInterface.__init__ with args', args)
        monkeypatch.setattr(testee.TabbedInterface, '__init__', mock_init)
        testobj = testee.TabbedInterface()
        assert capsys.readouterr().out == 'called TabbedInterface.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TabbedInterface.__init__
        """
        monkeypatch.setattr(testee.wx.Panel, '__init__', mockwx.MockPanel.__init__)
        testobj = testee.TabbedInterface('parent', 'master')
        assert testobj.parent == 'parent'
        assert testobj.master == 'master'
        assert capsys.readouterr().out == "called Panel.__init__ with args ('parent',) {}\n"

    def test_setup_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.setup_selector
        """
        def callback():
            "empty function for reference"
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        monkeypatch.setattr(testee.wx, 'Simplebook', mockwx.MockNoteBook)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.setup_selector(callback)
        assert isinstance(result, testee.wx.ComboBox)
        assert isinstance(testobj.pnl, testee.wx.Simplebook)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args"
                f" ({testobj},) {{'size': (140, -1), 'style': 16}}\n"
                f"called ComboBox.Bind with args ({testee.wx.EVT_COMBOBOX}, {callback}) {{}}\n"
                f"called NoteBook.__init__ with args ({testobj},) {{}}\n")

    def test_add_subscreen(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_subscreen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args () {}\n"
        testobj.add_subscreen('win')
        assert capsys.readouterr().out == "called NoteBook.AddPage with args ('win', '')\n"

    def test_add_to_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_to_selector
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        selector = mockwx.MockComboBox()
        testobj.add_to_selector(selector, 'txt')
        assert capsys.readouterr().out == ("called ComboBox.__init__ with args () {}\n"
                                           "called combobox.Append with args ('txt',)\n")

    def test_start_display(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.start_display
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.start_display()
        assert isinstance(result, testee.wx.BoxSizer)
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args (8,)\n"

    def test_start_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.start_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.start_line(vbox)
        assert isinstance(result, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called  sizer.Add with args MockBoxSizer (0, 8192)\n")

    def test_add_margin_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_margin_to_line
        """
        hbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_margin_to_line(hbox)
        assert capsys.readouterr().out == "called  sizer.AddSpacer with args (10,)\n"

    def test_add_text_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_text_to_line
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        hbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_text_to_line(hbox, 'xxx')
        assert isinstance(result, testee.wx.StaticText)
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                "called  sizer.Add with args MockStaticText (0, 2048)\n")

    def test_add_selector_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_selector_to_line
        """
        widget = mockwx.MockControl()
        hbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called Control.__init__\n"
                                           "called BoxSizer.__init__ with args ()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_selector_to_line(hbox, widget)
        assert capsys.readouterr().out == "called  sizer.Add with args MockControl (0, 2064, 5)\n"

    def test_add_combobox_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_combobox_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        hbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args ()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_combobox_to_line(hbox)
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                f"called ComboBox.__init__ with args ({testobj},) {{'style': 16}}\n"
                "called  sizer.Add with args MockComboBox (0, 2048)\n")
        result = testobj.add_combobox_to_line(hbox, 10, True, callback)
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                f"called ComboBox.__init__ with args ({testobj},) {{'style': 32}}\n"
                f"called ComboBox.Bind with args ({testee.wx.EVT_TEXT}, {callback}) {{}}\n"
                "called  sizer.Add with args MockComboBox (0, 2048)\n")

    def test_add_separator_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_separator_to_line
        """
        hbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_separator_to_line(hbox)
        assert capsys.readouterr().out == "called  sizer.AddStretchSpacer\n"

    def test_add_button_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_button_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        hbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_button_to_line(hbox, 'xxx', callback, 'enabled')
        assert isinstance(result, testee.wx.Button)
        assert capsys.readouterr().out == (
                f"called Button.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback}) {{}}\n"
                "called Button.Enable with arg enabled\n"
                "called  sizer.Add with args MockButton (0,)\n")

    def test_add_list_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_list_to_line
        """
        hbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockFrame()
        hbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called frame.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        testobj.add_list_to_line(hbox)
        assert capsys.readouterr().out == "called  sizer.Add with args MockFrame (0,)\n"

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.finalize_display
        """
        monkeypatch.setattr(testee.wx.Panel, 'SetAutoLayout', mockwx.MockPanel.SetAutoLayout)
        monkeypatch.setattr(testee.wx.Panel, 'SetSizer', mockwx.MockPanel.SetSizer)
        monkeypatch.setattr(testee.wx.Panel, 'Show', mockwx.MockPanel.Show)
        vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.finalize_display(vbox)
        assert capsys.readouterr().out == ("called Panel.SetAutoLayout with args (True,)\n"
                                           "called Panel.SetSizer with args ( sizer,)\n"
                                           f"called  sizer.Fit with args ({testobj},)\n"
                                           "called Panel.Show\n")

    def test_setcaption(self, monkeypatch, capsys):
        """unittest for TabbedInterface.setcaption
        """
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setcaption(widget, 'xxx')
        assert capsys.readouterr().out == "called Control.SetLabel with args ('xxx',) {}\n"

    def test_on_pagechange(self, monkeypatch, capsys):
        """unittest for TabbedInterface.on_pagechange
        """
        def mock_onpagechange(*args):
            print('called ChoiceBook.on_page_changed with args', args)
        def mock_get(self):
            print('called event.GetEventObject')
            return lb
        monkeypatch.setattr(mockwx.MockEvent, 'GetEventObject', mock_get)
        event = mockwx.MockEvent()
        lb = mockwx.MockListBox()
        assert capsys.readouterr().out == ("called event.__init__ with args ()\n"
                                           "called ListBox.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(on_page_changed=mock_onpagechange)
        testobj.on_pagechange(event)
        assert capsys.readouterr().out == ("called event.GetEventObject\n"
                                           "called listbox.GetSelection\n"
                                           "called ChoiceBook.on_page_changed with args (1,)\n")

    def test_selected_get_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args () {}\n"
        assert testobj.get_selected_panel() == "page"
        assert capsys.readouterr().out == "called NoteBook.GetCurrentPage\n"

    def test_set_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args () {}\n"
        testobj.set_selected_panel('indx')
        assert capsys.readouterr().out == ("called NoteBook.SetSelection with args ('indx',)\n")

    def test_get_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args () {}\n"
        assert testobj.get_panel('indx') == "page"
        assert capsys.readouterr().out == ("called NoteBook.GetPage with args ('indx',)\n")

    def test_replace_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.replace_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args () {}\n"
        testobj.replace_panel('indx', 'win', 'newwin')
        assert capsys.readouterr().out == (
                "called NoteBook.InsertPage with args ('indx', 'newwin')\n"
                "called NoteBook.SetSelection with args ('newwin',)\n"
                "called NoteBook.RemovePage with args ('win',)\n")

    def test_enable_widget(self, monkeypatch, capsys):
        """unittest for TabbedInterface.enable_widget
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj.enable_widget(widget, 'state')
        assert capsys.readouterr().out == "called Control.Enable with arg state\n"

    def test_refresh_combobox(self, monkeypatch, capsys):
        """unittest for TabbedInterface.refresh_combobox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj.refresh_combobox(cmb)
        assert capsys.readouterr().out == "called combobox.clear\n"
        testobj.refresh_combobox(cmb, ['x', 'y'])
        assert capsys.readouterr().out == ("called combobox.clear\n"
                                           "called combobox.AppendItems with args (['x', 'y'],)\n"
                                           "called combobox.SetSelection with args (1,)\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        assert testobj.get_combobox_value(cmb) == "value from combobox"
        assert capsys.readouterr().out == "called combobox.GetValue\n"

    def test_set_combobox_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_combobox_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj.set_combobox_text(cmb, '')
        assert capsys.readouterr().out == "called combobox.SetValue with args ('',)\n"
        testobj.set_combobox_text(cmb, 'xxx')
        assert capsys.readouterr().out == ("called combobox.SetValue with args ('xxx',)\n"
                                           "called combobox.Enable with arg True\n")

    def test_get_combobox_index(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_combobox_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj.get_combobox_index(cmb)
        assert capsys.readouterr().out == "called combobox.GetSelection\n"

    def test_on_textchange(self, monkeypatch, capsys):
        """unittest for TabbedInterface.on_textchange
        """
        def mock_ontextchange(*args):
            print('called ChoiceBook.on_text_changed with args', args)
        def mock_get(self):
            print('called event.GetEventObject')
            return txt
        def mock_getv(self):
            print('called text.GetValue')
            return ''
        monkeypatch.setattr(mockwx.MockEvent, 'GetEventObject', mock_get)
        event = mockwx.MockEvent()
        txt = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == ("called event.__init__ with args ()\n"
                                           "called TextCtrl.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(on_text_changed=mock_ontextchange)
        testobj.on_textchange(event)
        assert capsys.readouterr().out == (
                "called event.GetEventObject\n"
                "called text.GetValue\n"
                "called ChoiceBook.on_text_changed with args ('value from textctrl',)\n")
        monkeypatch.setattr(mockwx.MockTextCtrl, 'GetValue', mock_getv)
        testobj.on_textchange(event)
        assert capsys.readouterr().out == (
                "called event.GetEventObject\n"
                "called text.GetValue\n")

    def test_get_search_col(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_search_col
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        assert testobj.get_search_col(cmb) == "current text"
        assert capsys.readouterr().out == "called combobox.GetStringSelection\n"

    def test_get_combobox_index_for_item(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_combobox_index_for_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        assert testobj.get_combobox_index_for_item(cb, 'item') == 'selection'
        assert capsys.readouterr().out == "called combobox.GetSelection\n"

    def test_set_combobox_index(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_combobox_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj.set_combobox_index(cmb, 'selection')
        assert capsys.readouterr().out == "called combobox.SetSelection with args ('selection',)\n"

    def test_get_button_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockwx.MockButton(label='xxx')
        assert capsys.readouterr().out == "called Button.__init__ with args () {'label': 'xxx'}\n"
        assert testobj.get_button_text(button) == "xxx"
        assert capsys.readouterr().out == "called Button.GetLabel\n"

    def test_set_button_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockwx.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args () {}\n"
        testobj.set_button_text(button, "state")
        assert capsys.readouterr().out == "called Button.SetLabel with arg 'state'\n"

    def test_find_items(self, monkeypatch, capsys):
        """unittest for TabbedInterface.find_items
        """
        def mock_get(self, *args):
            nonlocal counter
            print('called ListCtrl.GetItemText with args', args)
            counter += 1
            if counter == 1:
                return ''
            return 'text'
        def mock_count():
            print('called ListCtrl.GetItemCount')
            return 0
        monkeypatch.setattr(mockwx.MockListCtrl, 'GetItemText', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        counter = 0
        assert testobj.find_items(p0list, 'xxx', 'text') == [2]
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n"
                                           "called ListCtrl.GetItemText with args (0, 'xxx')\n"
                                           "called ListCtrl.GetItemText with args (1, 'xxx')\n")
        p0list.GetItemCount = mock_count
        counter = 0
        assert testobj.find_items(p0list, 'xxx', 'text') == []
        assert capsys.readouterr().out == "called ListCtrl.GetItemCount\n"

    def test_set_selected_keydef_item(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_keydef_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj.set_selected_keydef_item(p0list, ['xxx', 'yyy', 'zzz'], 2)
        assert capsys.readouterr().out == ("called ListCtrl.Select with args ('zzz',)\n"
                                           "called ListCtrl.EnsureVisible with args ('zzz',)\n")

    def test_get_found_keydef_position(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_found_keydef_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.master.page = MockHotkeyPanel()
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        assert testobj.get_found_keydef_position(p0list) == (-1, -1)
        assert capsys.readouterr().out == ("called ListCtrl.GetFirstSelected\n"
                                           "called ListCtrl.GetItemText with args (-1, 0)\n"
                                           "called ListCtrl.GetItemText with args (-1, 1)\n")

    def test_set_found_keydef_position(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_found_keydef_position
        """
        def mock_get(self, *args):
            nonlocal counter
            print('called ListCtrl.GetItemText with args', args)
            counter += 1
            return counter
        def mock_count():
            print('called ListCtrl.GetItemCount')
            return 0
        monkeypatch.setattr(mockwx.MockListCtrl, 'GetItemText', mock_get)
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        counter = 0
        testobj.set_found_keydef_position(p0list, (3, 4))
        assert capsys.readouterr().out == ("called ListCtrl.GetItemCount\n"
                                           "called ListCtrl.GetItemText with args (0, 0)\n"
                                           "called ListCtrl.GetItemText with args (0, 1)\n"
                                           "called ListCtrl.GetItemText with args (1, 0)\n"
                                           "called ListCtrl.GetItemText with args (1, 1)\n"
                                           "called ListCtrl.Select with args (1,)\n")
        p0list.GetItemCount = mock_count
        counter = 0
        testobj.set_found_keydef_position(p0list, (3, 4))
        assert capsys.readouterr().out == "called ListCtrl.GetItemCount\n"

    def test_remove_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.remove_tool
        """
        def mock_get(*args):
            print('called NoteBook.GetPage with args', args)
            return win
        win = mockwx.MockPanel()
        assert capsys.readouterr().out == "called Panel.__init__ with args () {}\n"
        win.master = 'master'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        testobj.pnl.GetPage = mock_get
        assert capsys.readouterr().out == "called NoteBook.__init__ with args () {}\n"
        assert testobj.remove_tool(1, 'program', []) is None
        assert capsys.readouterr().out == ("called NoteBook.GetPage with args (1,)\n"
                                           "called NoteBook.RemovePage with args (1,)\n"
                                           "called Panel.Destroy with args ()\n")
        assert testobj.remove_tool(1, 'program', ['program', 'list']) == "master"
        assert capsys.readouterr().out == ("called NoteBook.GetPage with args (1,)\n"
                                           "called NoteBook.RemovePage with args (1,)\n")


class TestSingleDataInterface:
    """unittest for gui_wx.SingleDataInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.SingleDataInterface object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SingleDataInterface.__init__ with args', args)
        monkeypatch.setattr(testee.SingleDataInterface, '__init__', mock_init)
        testobj = testee.SingleDataInterface()
        testobj.parent = MockTabbedInterface()
        testobj.master = MockHotkeyPanel()
        # testobj.p0list = mockwx.MockTreeWidget()
        # assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args ()\n'
        #                                    "called Tree.__init__\n")
        assert capsys.readouterr().out == 'called SingleDataInterface.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.__init__
        """
        monkeypatch.setattr(testee.wx, 'Panel', mockwx.MockPanel)
        parent = types.SimpleNamespace(pnl='panel')
        testobj = testee.SingleDataInterface(parent, 'master')
        assert testobj.parent == parent
        assert testobj.master == 'master'
        assert testobj._savestates == (False, False)
        assert isinstance(testobj._sizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == ("called Panel.__init__ with args ('panel',) {}\n")

    def test_setup_empty_screen(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.setup_empty_screen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj.setup_empty_screen('nodata', 'title')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'nodata'}}\n"
                "called hori sizer.Add with args MockStaticText ()\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_setup_list(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.setup_list
        """
        def callback():
            "empty function for reference"
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'ImageList', mockwx.MockImageList)
        monkeypatch.setattr(testee, 'PyEmbeddedImage', mockwx.MockEmbeddedImage)
        # monkeypatch.setattr(testee.wx, 'ListCtrl', mockwx.MockListCtrl)
        # monkeypatch.setattr(testee.wx.lib.mixins.listctrl, 'ListCtrlAutoWidthMixin',
        #                     mockwx.MockListCtrlAutoWidthMixin)
        # monkeypatch.setattr(testee.wx.lib.mixins.listctrl, 'ListRowHighlighter',
        #                     mockwx.MockListRowHighlighter)
        monkeypatch.setattr(testee, 'MyListCtrl', mockwx.MockListCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.setup_list(['xxx', 'yyy'], [1, 2], callback)
        assert isinstance(result, testee.MyListCtrl)
        assert testobj.sm_up == 'bitmap from image'
        assert testobj.sm_dn == 'bitmap from image'
        # testobj.imglist check ik niet, wordt verder niet gebruikti maar wel handig in output:
        assert capsys.readouterr().out == (
                "called ImageList.__init__ with args (16, 16)\n"
                "called PyEmbeddedImage.__init__\n"
                "called PyEmbeddedImage.GetBitmap\n"
                "called ImageList.Add with args ('bitmap from image',)\n"
                "called PyEmbeddedImage.__init__\n"
                "called PyEmbeddedImage.GetBitmap\n"
                "called ImageList.Add with args ('bitmap from image',)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                "called ListCtrl.__init__ with args"
                f" ({testobj},) {{'size': (1140, 594), 'style': 134225952}}\n"
                "called ListCtrl.AppendColumn with args ('xxx',)\n"
                "called ListCtrl.SetColumnWidth with args (0, 1)\n"
                "called ListCtrl.AppendColumn with args ('yyy',)\n"
                "called ListCtrl.SetColumnWidth with args (1, 2)\n"
                f"called ListCtrl.Bind with args ({testee.wx.EVT_LIST_ITEM_SELECTED}, {callback})\n"
                "called ListCtrl.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_DESELECTED}, {testobj.on_item_deselected})\n"
                "called ListCtrl.Bind with args"
                f" ({testee.wx.EVT_LIST_ITEM_ACTIVATED}, {testobj.on_item_activated})\n"
                f"called ListCtrl.SetImageList with args ({testobj.imglist}, 1)\n"
                "called hori sizer.Add with args MockListCtrl (1, 8432, 5)\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_start_extrapanel(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.start_extrapanel
        """
        monkeypatch.setattr(testee.wx, 'Panel', mockwx.MockPanel)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.start_extrapanel(90)
        assert isinstance(result, testee.wx.BoxSizer)
        assert isinstance(testobj._frm, testee.wx.Panel)
        assert capsys.readouterr().out == (
                f"called Panel.__init__ with args ({testobj},) {{'size': (-1, 120)}}\n"
                "called  sizer.Add with args MockPanel (0, 8240)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called vert sizer.AddSpacer with args (5,)\n"
                "called Panel.SetSizer with args (vert sizer,)\n")

    def test_start_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.start_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.start_line(vsizer)
        assert isinstance(result, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called  sizer.Add with args MockBoxSizer (0, 8432, 5)\n")

    def test_add_label_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_label_to_line
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._frm = mockwx.MockPanel()
        hsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called Panel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        result = testobj.add_label_to_line(hsizer, 'xxx')
        assert isinstance(result, testee.wx.StaticText)
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj._frm},) {{'label': 'xxx '}}\n"
                "called  sizer.Add with args MockStaticText (0, 2048)\n")
        result = testobj.add_label_to_line(hsizer, 'xxx', add=False)
        assert isinstance(result, testee.wx.StaticText)
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj._frm},) {{'label': 'xxx '}}\n")

    def test_add_textfield_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_textfield_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._frm = mockwx.MockFrame()
        hsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called frame.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        result = testobj.add_textfield_to_line(hsizer)
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj._frm},) {{'size': (-1, -1)}}\n"
                "called  sizer.Add with args MockTextCtrl (0, 2048)\n")
        result = testobj.add_textfield_to_line(hsizer, 8, callback, add=False)
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj._frm},) {{'size': (8, -1)}}\n"
                f"called TextCtrl.Bind with args ({testee.wx.EVT_TEXT}, {callback})\n")

    def test_add_combobox_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_combobox_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.on_combobox = callback
        testobj._frm = mockwx.MockFrame()
        hsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called frame.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        result = testobj.add_combobox_to_line(hsizer, 'xxx')
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args"
                f" ({testobj._frm},) {{'size': (-1, -1), 'style': 16, 'choices': 'xxx'}}\n"
                f"called ComboBox.Bind with args ({testee.wx.EVT_COMBOBOX}, {callback}) {{}}\n"
                "called  sizer.Add with args MockComboBox (0, 2048)\n")
        result = testobj.add_combobox_to_line(hsizer, 'xxx', 10, False)
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args"
                f" ({testobj._frm},) {{'size': (10, -1), 'style': 16, 'choices': 'xxx'}}\n"
                f"called ComboBox.Bind with args ({testee.wx.EVT_COMBOBOX}, {callback}) {{}}\n")

    def test_add_checkbox_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_checkbox_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.on_checkbox = callback
        testobj._frm = mockwx.MockFrame()
        hbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called frame.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        result = testobj.add_checkbox_to_line(hbox, 'xxx')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj._frm},) {{'label': 'xxx'}}\n"
                "called checkbox.SetValue with args (False,)\n"
                f"called CheckBox.Bind with args ({testee.wx.EVT_CHECKBOX}, {callback}) {{}}\n"
                "called  sizer.Add with args MockCheckBox (0, 2048)\n")

    def test_add_separator_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_separator_to_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        hsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_separator_to_line(hsizer)
        assert capsys.readouterr().out == "called  sizer.AddStretchSpacer\n"

    def test_add_button_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_button_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._frm = mockwx.MockFrame()
        hsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called frame.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        result = testobj.add_button_to_line(hsizer, 'xxx', callback)
        assert isinstance(result, testee.wx.Button)
        assert capsys.readouterr().out == (
                f"called Button.__init__ with args ({testobj._frm},) {{'label': 'xxx'}}\n"
                "called Button.Enable with arg False\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback}) {{}}\n"
                "called  sizer.Add with args MockButton (0,)\n")

    def test_add_descfield_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_descfield_to_line
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._frm = mockwx.MockFrame()
        hsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called frame.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        result = testobj.add_descfield_to_line(hsizer)
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj._frm},) {{'style': 48}}\n"
                "called  sizer.Add with args MockTextCtrl (1, 8432, 5)\n")

    def test_set_extrapanel_editable(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_extrapanel_editable
        """
        field1 = mockwx.MockControl()
        field2 = mockwx.MockControl()
        btn1 = mockwx.MockButton()
        btn2 = mockwx.MockButton()
        assert capsys.readouterr().out == ("called Control.__init__\n"
                                           "called Control.__init__\n"
                                           "called Button.__init__ with args () {}\n"
                                           "called Button.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._savestates = ['x', 'y']
        testobj.set_extrapanel_editable([field1, field2], [btn1, btn2], True)
        assert testobj._savestates == ['x', 'y']
        assert capsys.readouterr().out == ("called Control.Enable with arg True\n"
                                           "called Control.Enable with arg True\n"
                                           "called Button.Enable with arg x\n"
                                           "called Button.Enable with arg y\n")
        testobj.set_extrapanel_editable([field1, field2], [btn1, btn2], False)
        assert capsys.readouterr().out == ("called Control.Enable with arg False\n"
                                           "called Control.Enable with arg False\n"
                                           "called Button.IsEnabled\ncalled Button.IsEnabled\n"
                                           "called Button.Enable with arg False\n"
                                           "called Button.Enable with arg False\n")

    def test_finalize_screen(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.finalize_screen
        """
        def mock_sort(self, *args):
            print('called ColumnSorterMixin.SortListItems with args', args)
        monkeypatch.setattr(testee.listmix, 'ColumnSorterMixin', mockwx.MockColumnSorterMixin)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.SortListItems = mock_sort
        monkeypatch.setattr(testobj, 'SetAutoLayout', mockwx.MockFrame.SetAutoLayout)
        monkeypatch.setattr(testobj, 'SetSizer', mockwx.MockFrame.SetSizer)
        testobj._sizer = mockwx.MockBoxSizer()
        testobj.master.p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args ()\n"
                                           "called ListCtrl.__init__ with args () {}\n")
        testobj.master.data = {'1': 'x', '2': 'y'}
        testobj.master.column_info = ['a', 'b']
        testobj.p0list = ''
        testobj.finalize_screen(testobj.p0list)
        assert capsys.readouterr().out == (
                "called Frame.SetAutoLayout with args ()\n"
                "called Frame.SetSizer with args ()\n"
                f"called  sizer.Fit with args ({testobj},)\n")
        testobj.p0list = 'p0list'
        testobj.finalize_screen(testobj.p0list)
        assert capsys.readouterr().out == (
                "called ColumnSorterMixin.__init__ with args (2,) {}\n"
                "called ColumnSorterMixin.SortListItems with args (True,)\n"
                "called ListCtrl.RefreshRows\n"
                "called ListCtrl.Select with args (0,)\n"
                "called Frame.SetAutoLayout with args ()\n"
                "called Frame.SetSizer with args ()\n"
                f"called  sizer.Fit with args ({testobj},)\n")

    def _test_resize_if_necessary(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.resize_if_necessary
        """
        # niet ge"implementeerd. wellicht ook niet nodig
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.resize_if_necessary() == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_on_item_deselected(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_item_deselected
        """
        def mock_get(self):
            print('called event.GetItem')
            return None
        def mock_get_2(self):
            print('called event.GetItem')
            return 'treeitem'
        monkeypatch.setattr(mockwx.MockEvent, 'GetItem', mock_get)
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.initializing_screen = True
        testobj.on_item_deselected(event)
        assert capsys.readouterr().out == ("")
        testobj.master.initializing_screen = False
        testobj.on_item_deselected(event)
        assert not hasattr(testobj, 'olditem')
        assert capsys.readouterr().out == ("called event.GetItem\n")
        monkeypatch.setattr(mockwx.MockEvent, 'GetItem', mock_get_2)
        testobj.on_item_deselected(event)
        assert testobj.olditem == 'treeitem'
        assert capsys.readouterr().out == ("called event.GetItem\n")

    def test_on_item_selected(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_item_selected
        """
        def mock_get(self):
            print('called event.GetItem')
            return None
        def mock_get_2(self):
            print('called event.GetItem')
            return 'treeitem'
        def mock_process(*args):
            print('called HotkeyPanel.process_changed_selection with args', args)
        monkeypatch.setattr(mockwx.MockEvent, 'GetItem', mock_get)
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.olditem = 'olditem'
        testobj.master.process_changed_selecion = mock_process
        testobj.master.has_extrapanel = False
        testobj.on_item_selected(event)
        assert capsys.readouterr().out == ("called event.GetItem\n")
        testobj.master.has_extrapanel = True
        testobj.on_item_selected(event)
        assert capsys.readouterr().out == ("called event.GetItem\n")
        monkeypatch.setattr(mockwx.MockEvent, 'GetItem', mock_get_2)
        testobj.on_item_selected(event)
        assert capsys.readouterr().out == (
                "called event.GetItem\n"
                "called HotkeyPanel.process_changed_selection with args ('treeitem', 'olditem')\n"
                "called event.Skip\n")

    def test_on_item_activated(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_item_activated
        """
        def mock_get(self):
            print('called event.GetItem')
            return 'treeitem'
        monkeypatch.setattr(mockwx.MockEvent, 'GetItem', mock_get)
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == "called event.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_item_activated(event)
        assert testobj.current_item == 'treeitem'
        assert capsys.readouterr().out == ("called event.GetItem\n")

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_focus_to
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockwx.MockControl()
        assert capsys.readouterr().out == "called Control.__init__\n"
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == ("called Control.SetFocus\n")

    def test_update_columns(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.update_columns
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockListCtrl
        testobj.update_columns(p0list, 1, 1)
        assert capsys.readouterr().out == ("")
        testobj.update_columns(p0list, 1, 3)
        assert capsys.readouterr().out == ("called ListCtrl.AppendColumn with args ()\n"
                                           "called ListCtrl.AppendColumn with args ()\n")
        testobj.update_columns(p0list, 3, 1)
        assert capsys.readouterr().out == ("called ListCtrl.DeleteColumn with args ()\n"
                                           "called ListCtrl.DeleteColumn with args ()\n")

    def test_refresh_headers(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.refresh_headers
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockListCtrl
        testobj.refresh_headers(p0list, [])
        assert capsys.readouterr().out == ("called ListCtrl.resizeLastColumn with args (100,)\n")
        testobj.refresh_headers(p0list, [('x', 1), ('y', 2)])
        assert capsys.readouterr().out == ("called ListCtrl.GetColumn with args ()\n"
                                           "called item.SetText with arg 'x'\n"
                                           "called item.SetWidth with arg 1\n"
                                           "called ListCtrl.SetColumn with args (x,)\n"
                                           "called ListCtrl.GetColumn with args ()\n"
                                           "called item.SetText with arg 'y'\n"
                                           "called item.SetWidth with arg 2\n"
                                           "called ListCtrl.SetColumn with args (y,)\n"
                                           "called ListCtrl.resizeLastColumn with args (100,)\n")

    def test_GetListCtrl(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.GetListCtrl
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        assert testobj.GetListCtrl() == testobj.master.p0list
        assert capsys.readouterr().out == ""

    def test_GetSortImages(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.GetSortImages
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sm_dn = 'down arrow'
        testobj.sm_up = 'up arrow'
        assert testobj.GetSortImages() == ('down arrow', 'up arrow')
        assert capsys.readouterr().out == ""

    def test_OnSortOrderChanged(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.OnSortOrderChanged
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj.OnSortOrderChanged()
        assert capsys.readouterr().out == ("called ListCtrl.RefreshRows\n")

    def test_set_title(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_title
        """
        # geen idee of deze gebruikt wordt
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.parent = types.SimpleNamespace(
                parent=types.SimpleNamespace(gui=mockwx.MockFrame()))
        assert capsys.readouterr().out == "called frame.__init__ with args () {}\n"
        testobj.set_title('title')
        assert capsys.readouterr().out == ("called Frame.SetTitle with args ('title',)\n")

    def test_clear_list(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.clear_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj.clear_list(p0list)
        assert capsys.readouterr().out == "called ListCtrl.DeleteAllItems\n"

    def test_build_listitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.build_listitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        assert testobj.build_listitem('5') == "itemindex"
        assert capsys.readouterr().out == (
                "called ListCtrl.Append with args ('5',)\n"
                "called ListCtrl.SetItemData with args ('itemindex', 5)\n")

    def test_set_listitemtext(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_listitemtext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj.set_listitemtext(1, 2, 'value')
        assert capsys.readouterr().out == "called ListCtrl.SetItem with args (1, 2, 'value')\n"

    def _test_add_listitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_listitem
        """
        # niet geïmplementeerd, dus niet afgemaakt
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_listitem(['item', 'list']) == "expected_result"
        assert capsys.readouterr().out == ("")

    def test_set_listselection(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_listselection
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_listselection(p0list, 'pos')
        assert capsys.readouterr().out == ("called ListCtrl.Select with args ('pos',)\n")

    def test_getfirstitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.getfirstitem
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert str(testobj.getfirstitem(p0list)) == 'item 0'
        assert capsys.readouterr().out == ("called ListCtrl.GetItem with args (0,)\n")

    def test_get_listitem_at_position(self, monkeypatch, capsys):
        """unittest for SingledataInterface.get_listitem_at_position
        """
        p0list = mockwx.MockListCtrl()
        item = mockwx.MockListItem()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_listitem_at_position(p0list, item) == 'id'
        assert capsys.readouterr().out == "called item.GetId\n"

    def test_get_itemdata(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_itemdata
        """
        def mock_get(self):
            print("called item.GetData")
            return 5
        monkeypatch.setattr(mockwx.MockListItem, 'GetData', mock_get)
        item = mockwx.MockListItem()
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_itemdata(item) == "5"
        assert capsys.readouterr().out == ("called item.GetData\n")

    def test_get_listbox_selection(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_selected_keydef
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.get_listbox_selection(p0list)
        assert isinstance(result[0], mockwx.MockListItem)
        assert str(result[0]) == 'item -1'
        assert result[1] == -1
        assert capsys.readouterr().out == ("called ListCtrl.GetFirstSelected\n"
                                           "called ListCtrl.GetItem with args (-1,)\n")

    def test_get_listitem_position(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_listitem_position
        """
        p0list = mockwx.MockListCtrl()
        assert capsys.readouterr().out == "called ListCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        with pytest.raises(NotImplementedError):
            testobj.get_listitem_position(p0list, 'item')
        # assert capsys.readouterr().out == ("")

    def test_get_widget_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_widget_text
        """
        def mock_get(self):
            print('called event.GetEventWidget')
            return txt
        monkeypatch.setattr(mockwx.MockEvent, 'GetEventWidget', mock_get)
        event = mockwx.MockEvent()
        txt = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == ('called event.__init__ with args ()\n'
                                           "called TextCtrl.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_widget_text(event) == "value from textctrl"
        assert capsys.readouterr().out == ("called event.GetEventWidget\n"
                                           "called text.GetValue\n")

    def test_set_textfield_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_textfield_value
        """
        txt = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_textfield_value(txt, 'value')
        assert capsys.readouterr().out == "called text.SetValue with args ('value',)\n"

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.enable_button
        """
        button = mockwx.MockButton()
        assert capsys.readouterr().out == "called Button.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_button(button, 'state')
        assert capsys.readouterr().out == ("called Button.Enable with arg state\n")

    def test_get_choice_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_choice_value
        """
        def mock_get(self):
            print('called event.GetEventWidget')
            return cb
        monkeypatch.setattr(mockwx.MockEvent, 'GetEventWidget', mock_get)
        event = mockwx.MockEvent()
        cb = mockwx.MockComboBox()
        assert capsys.readouterr().out == ("called event.__init__ with args ()\n"
                                           "called ComboBox.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_choice_value(event) == (cb, 'value from combobox')
        assert capsys.readouterr().out == ("called event.GetEventWidget\n"
                                           "called combobox.GetValue\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_combobox_value
        """
        cb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_combobox_value(cb) == "value from combobox"
        assert capsys.readouterr().out == ("called combobox.GetValue\n")

    def test_init_combobox(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.init_combobox
        """
        cb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.init_combobox(cb)
        assert capsys.readouterr().out == ("called combobox.clear\n")
        testobj.init_combobox(cb, choices=['x', 'y'])
        assert capsys.readouterr().out == ("called combobox.clear\n"
                                           "called combobox.AppendItems with args (['x', 'y'],)\n")

    def test_set_combobox_string(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_combobox_string
        """
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_combobox_string(cmb, 'value', ['value', 'list'])
        assert capsys.readouterr().out == ("called combobox.SetSelection with args (0,)\n")
        testobj.set_combobox_string(cmb, 'value', [])
        assert capsys.readouterr().out == ""

    def test_set_label_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_label_text
        """
        lbl = mockwx.MockStaticText()
        assert capsys.readouterr().out == "called StaticText.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_label_text(lbl, "value")
        assert capsys.readouterr().out == ("called StaticText.SetLabel with args ('value',) {}\n")

    def test_get_check_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_check_value
        """
        def mock_get(self):
            print('called event.GetEventWidget')
            return cb
        monkeypatch.setattr(mockwx.MockEvent, 'GetEventWidget', mock_get)
        event = mockwx.MockEvent()
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == ("called event.__init__ with args ()\n"
                                           "called CheckBox.__init__ with args () {}\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_check_value(event) == (cb, 'value from checkbox')
        assert capsys.readouterr().out == ("called event.GetEventWidget\n"
                                           "called checkbox.GetValue\n")

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_checkbox_state
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_state(cb) == "value from checkbox"
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")

    def test_set_checkbox_state(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_checkbox_state
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_checkbox_state(cb, 'state')
        assert capsys.readouterr().out == ("called checkbox.SetValue with args ('state',)\n")


class TestMyListCtrl:
    """unittest for gui_wx.MyListCtrl
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_wx.MyListCtrl object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called MyListCtrl.__init__ with args', args)
        monkeypatch.setattr(testee.MyListCtrl, '__init__', mock_init)
        testobj = testee.MyListCtrl()
        assert capsys.readouterr().out == 'called MyListCtrl.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for MyListCtrl.__init__
        """
        monkeypatch.setattr(testee.wx, 'ListCtrl', mockwx.MockListCtrl)
        monkeypatch.setattr(testee.wx.lib.mixins.listctrl, 'ListCtrlAutoWidthMixin',
                            mockwx.MockListCtrlAutoWidthMixin)
        monkeypatch.setattr(testee.wx.lib.mixins.listctrl, 'ListRowHighlighter',
                            mockwx.MockListRowHighlighter)
        testobj = testee.MyListCtrl('parent')
        assert capsys.readouterr().out == (
                "called ListCtrl.__init__ with args"
                " ('parent', -1, wx.Point(-1, -1), wx.Size(-1, -1), 0) {}\n"
                "called ListCtrlAutoWidthMixin.__init__ with args () {}\n"
                "called ListRowHighlighter.__init__ with args () {}\n")


def mock_get_text(*args):
    "stub"
    print('called shared.get_text with args', args)
    return 'text'


def mock_get_title(*args):
    "stub"
    print('called shared.get_title with args', args)
    return 'title'


def test_show_message(monkeypatch, capsys):
    """unittest for wxgui.show_message
    """
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
    testee.show_message('win')
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', '', '', None)\n"
            "called shared.get_title with args ('win',)\n"
            "called wx.MessageBox with args ('text', 'title') {'parent': 'win'}\n")
    testee.show_message('win', message_id='xxx', text='yyy', args={'aa': 'bbbb'})
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            "called wx.MessageBox with args ('text', 'title') {'parent': 'win'}\n")


def test_show_cancel_message(monkeypatch, capsys):
    """unittest for wxgui.show_cancel_message
    """
    def mock_messagebox_2(*args, **kwargs):
        print(f'called wx.MessageBox with args', args, kwargs)
        return testee.wx.OK
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.wx, 'MessageBox', mockwx.mock_messagebox)
    assert not testee.show_cancel_message('win')
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', '', '', None)\n"
            "called shared.get_title with args ('win',)\n"
            "called wx.MessageBox with args ('text', 'title') {'parent': 'win', 'style': 20}\n")
    monkeypatch.setattr(testee.wx, 'MessageBox', mock_messagebox_2)
    assert testee.show_cancel_message('win')
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', '', '', None)\n"
            "called shared.get_title with args ('win',)\n"
            "called wx.MessageBox with args ('text', 'title') {'parent': 'win', 'style': 20}\n")
    assert testee.show_cancel_message('win', message_id='xxx', text='yyy', args={'aa': 'bbbb'})
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            "called wx.MessageBox with args ('text', 'title') {'parent': 'win', 'style': 20}\n")


def test_ask_question(monkeypatch, capsys):
    """unittest for wxgui.ask_question
    """
    def mock_show(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_YES
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    assert not testee.ask_question('win')
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', '', '', None)\n"
            "called shared.get_title with args ('win',)\n"
            "called MessageDialog.__init__ with args ('win', 'text', 'title', 1162) {}\n"
            "called MessageDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show)
    assert testee.ask_question('win', message_id='xxx', text='yyy', args={'aa': 'bbbb'})
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            "called MessageDialog.__init__ with args ('win', 'text', 'title', 1162) {}\n"
            "called MessageDialog.ShowModal\n")


def test_ask_ync_question(monkeypatch, capsys):
    """unittest for wxgui.ask_ync_question
    """
    def mock_show(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_YES
    def mock_show_2(self):
        print('called MessageDialog.ShowModal')
        return testee.wx.ID_CANCEL
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.wx, 'MessageDialog', mockwx.MockMessageDialog)
    assert testee.ask_ync_question('win') == (False, False)
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', '', '', None)\n"
            "called shared.get_title with args ('win',)\n"
            "called MessageDialog.__init__ with args ('win', 'text', 'title', 1178) {}\n"
            "called MessageDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show)
    assert testee.ask_ync_question('win', message_id='xxx', text='yyy', args={}) == (True, False)
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {})\n"
            "called shared.get_title with args ('win',)\n"
            "called MessageDialog.__init__ with args ('win', 'text', 'title', 1178) {}\n"
            "called MessageDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockMessageDialog, 'ShowModal', mock_show_2)
    assert testee.ask_ync_question('win', message_id='xxx', text='yyy',
                                   args={'aa': 'bbbb'}) == (False, True)
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            "called MessageDialog.__init__ with args ('win', 'text', 'title', 1178) {}\n"
            "called MessageDialog.ShowModal\n")


def test_get_textinput(monkeypatch, capsys):
    """unittest for wxgui.get_textinput
    """
    def mock_show(self):
        print('called TextDialog.ShowModal')
        return testee.wx.ID_OK
    def mock_get(*args, **kwargs):
        print('called TextDialog.GetValue')
        return 'xxx'
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.wx, 'TextEntryDialog', mockwx.MockTextDialog)
    assert testee.get_textinput('win', 'text') == ('text', False)
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'T_MAIN')\n"
            "called TextDialog.__init__ with args ('', 'text') {'value': 'text'}\n"
            "called TextDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockTextDialog, 'ShowModal', mock_show)
    assert testee.get_textinput('win', 'text') == ('', True)
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'T_MAIN')\n"
            "called TextDialog.__init__ with args ('', 'text') {'value': 'text'}\n"
            "called TextDialog.ShowModal\n"
            "called TextDialog.GetValue\n")
    monkeypatch.setattr(mockwx.MockTextDialog, 'GetValue', mock_get)
    assert testee.get_textinput('win', 'text', 'prompt') == ('xxx', True)
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'T_MAIN')\n"
            "called TextDialog.__init__ with args ('prompt', 'text') {'value': 'text'}\n"
            "called TextDialog.ShowModal\n"
            "called TextDialog.GetValue\n")


def test_get_choice(monkeypatch, capsys):
    """unittest for wxgui.get_choice
    """
    def mock_show(self):
        print('called ChoiceDialog.ShowModal')
        return testee.wx.ID_OK
    monkeypatch.setattr(testee.wx, 'SingleChoiceDialog', mockwx.MockChoiceDialog)
    assert testee.get_choice('win', 'title', 'text', ['x', 'y'], 'sel') == ('', False)
    assert capsys.readouterr().out == (
            "called ChoiceDialog.__init__ with args ('title', 'text', ['x', 'y'])\n"
            "called ChoiceDialog.SetSelection with arg 'sel'\n"
            "called ChoiceDialog.ShowModal\n")
    monkeypatch.setattr(mockwx.MockChoiceDialog, 'ShowModal', mock_show)
    assert testee.get_choice('win', 'title', 'text', ['x', 'y'], 'sel') == ('selected value', True)
    assert capsys.readouterr().out == (
            "called ChoiceDialog.__init__ with args ('title', 'text', ['x', 'y'])\n"
            "called ChoiceDialog.SetSelection with arg 'sel'\n"
            "called ChoiceDialog.ShowModal\n"
            "called ChoiceDialog.GetStringSelection\n")


def test_get_file_to_open(monkeypatch, capsys):
    """unittest for wxgui.get_file_to_open
    """
    def mock_get(*args):
        print('called shared.get_open_title with args', args)
        return args[1]
    monkeypatch.setattr(testee.shared, 'get_open_title', mock_get)
    monkeypatch.setattr(testee.wx, 'LoadFileSelector', mockwx.mock_loadfileselector)
    assert testee.get_file_to_open('win') == "xxxx"
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', '')\n"
            "called wx.LoadFileSelector with args"
            " ('C_SELFIL', '') {'default_name': '', 'parent': 'win'}\n")
    assert testee.get_file_to_open('win', 'oms', 'extension', 'start') == "xxxx"
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', 'oms')\n"
            "called wx.LoadFileSelector with args"
            " ('C_SELFIL', 'extension') {'default_name': 'start', 'parent': 'win'}\n")


def test_get_file_to_save(monkeypatch, capsys):
    """unittest for wxgui.get_file_to_save
    """
    def mock_get(*args):
        print('called shared.get_open_title with args', args)
        return args[1]
    monkeypatch.setattr(testee.shared, 'get_open_title', mock_get)
    monkeypatch.setattr(testee.wx, 'SaveFileSelector', mockwx.mock_savefileselector)
    assert testee.get_file_to_save('win') == "xxxx"
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', '')\n"
            "called wx.SaveFileSelector with args"
            " ('C_SELFIL', '') {'default_name': '', 'parent': 'win'}\n")
    assert testee.get_file_to_save('win', 'oms', 'extension', 'start') == "xxxx"
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', 'oms')\n"
            "called wx.SaveFileSelector with args"
            " ('C_SELFIL', 'extension') {'default_name': 'start', 'parent': 'win'}\n")


def test_show_dialog(monkeypatch, capsys):
    """unittest for wxgui.show_DialogGui
    """
    def mock_show():
        print('called Dialog.ShowModal')
        return testee.wx.ID_CANCEL
    def mock_accept():
        nonlocal counter
        print('called Dialog.accept')
        counter += 1
        if counter == 1:
            return False
        return True
    dlg = mockwx.MockDialog('parent')
    assert capsys.readouterr().out == "called Dialog.__init__ with args () {}\n"
    dlg.accept = mock_accept
    counter = 0
    assert testee.show_dialog(dlg)
    assert capsys.readouterr().out == ("called Dialog.ShowModal\n"
                                       "called Dialog.accept\n"
                                       "called Dialog.ShowModal\n"
                                       "called Dialog.accept\n")
    dlg.ShowModal = mock_show
    assert not testee.show_dialog(dlg)
    assert capsys.readouterr().out == "called Dialog.ShowModal\n"


class TestInitialToolDialogGui:
    """unittest for wxgui.InitialToolDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.InitialToolDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called InitialToolDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.InitialToolDialogGui, '__init__', mock_init)
        testobj = testee.InitialToolDialogGui()
        assert capsys.readouterr().out == 'called InitialToolDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = testee.InitialToolDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.vbox, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title'}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.SetSizer with args (vert sizer,)\n")

    def test_add_text(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.add_text
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_text('text')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called  sizer.Add with args MockStaticText (0, 80, 5)\n")

    def test_add_radiobutton_line(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.add_radiobutton_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'RadioButton', mockwx.MockRadioButton)
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.add_radiobutton_line('text', True)
        assert isinstance(result[0], testee.wx.RadioButton)
        assert result[1] == ''
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called RadioButton.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called radiobutton.SetValue with args (True,)\n"
                "called hori sizer.Add with args MockRadioButton (0, 2064, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 192, 2)\n")
        result = testobj.add_radiobutton_line('text', False, [])
        assert isinstance(result[0], testee.wx.RadioButton)
        assert isinstance(result[1], testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called RadioButton.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called radiobutton.SetValue with args (False,)\n"
                "called hori sizer.Add with args MockRadioButton (0, 2064, 5)\n"
                "called ComboBox.__init__ with args"
                f" ({testobj},) {{'size': (140, -1), 'style': 32, 'choices': []}}\n"
                "called combobox.SetSelection with args (0,)\n"
                "called hori sizer.Add with args MockComboBox (0, 32, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 192, 2)\n")
        result = testobj.add_radiobutton_line('text', True, ['x', 'y'], 1)
        assert isinstance(result[0], testee.wx.RadioButton)
        assert isinstance(result[1], testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called RadioButton.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called radiobutton.SetValue with args (True,)\n"
                "called hori sizer.Add with args MockRadioButton (0, 2064, 5)\n"
                "called ComboBox.__init__ with args"
                f" ({testobj},) {{'size': (140, -1), 'style': 32, 'choices': ['x', 'y']}}\n"
                "called combobox.SetSelection with args (1,)\n"
                "called hori sizer.Add with args MockComboBox (0, 32, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 192, 2)\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 384, 2)\n")

    def test_get_radiobutton_value(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.get_radiobutton_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        rb = mockwx.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        assert testobj.get_radiobutton_value(rb) == 'value from radiobutton'
        assert capsys.readouterr().out == "called radiobutton.GetValue\n"

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.get_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockwx.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__ with args () {}\n"
        assert testobj.get_combobox_value(cmb) == 'current text'
        assert capsys.readouterr().out == "called combobox.GetStringSelection\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.accept
        """
        def mock_confirm():
            print('called InitialToolDialog.confirm')
            return 'ok'
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept() == "ok"
        assert capsys.readouterr().out == "called InitialToolDialog.confirm\n"


class TestFilesDialogGui:
    """unittest for wxgui.FilesDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.FilesDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FilesDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.FilesDialogGui, '__init__', mock_init)
        testobj = testee.FilesDialogGui()
        assert capsys.readouterr().out == 'called FilesDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = testee.FilesDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'size': (680, 400), 'title': 'title'}\n"
                "called BoxSizer.__init__ with args (8,)\n")

    def test_add_explanation(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_explanation
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_explanation('text')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called  sizer.Add with args MockStaticText (0, 496, 5)\n")

    def test_add_captions(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_captions
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_captions([('cap', 10), ('tions', 20)])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddSpacer with args (10,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'cap'}}\n"
                "called hori sizer.Add with args MockStaticText (0, 16, 10)\n"
                "called hori sizer.AddSpacer with args (20,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'tions'}}\n"
                "called hori sizer.Add with args MockStaticText (0, 16, 20)\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_locationbrowserarea(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_locationbrowserarea
        """
        monkeypatch.setattr(testee.wxsp, 'ScrolledPanel', mockwx.MockScrolledPanel)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.add_locationbrowserarea(), testee.wxsp.ScrolledPanel)
        assert capsys.readouterr().out == (
                f"called ScrolledPanel.__init__ with args ({testobj},) {{'style': 134217728}}\n"
                "called BoxSizer.__init__ with args (8,)\n")

    def test_finish_browserarea(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.finish_browserarea
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        testobj.scrl = mockwx.MockScrolledPanel()
        testobj.gsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args ()\n"
                                           "called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        testobj.finish_browserarea()
        assert capsys.readouterr().out == (
                "called ScrolledPanel.Fit with args ()\n"
                "called ScrolledPanel.SetSizer with args ( sizer,)\n"
                f"called  sizer.SetSizeHints with args ({testobj.scrl},)\n"
                "called ScrolledPanel.SetupScrolling\n"
                "called  sizer.Add with args MockScrolledPanel (1, 8432, 5)\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_buttons
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_buttons([('ok', ''), ('cancel', ''), ('xxx', callback)])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback}) {{}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 448, 5)\n")

    def test_finish_display(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.finish_display
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.finish_display()
        assert capsys.readouterr().out == (
                f"called  sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.SetSizer with args ( sizer,)\n")

    def test_add_row(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_row
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        monkeypatch.setattr(testee.wxfb, 'FileBrowseButton', mockwx.MockFileBrowse)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        testobj.scrl = mockwx.MockScrolledPanel()
        testobj.gsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args ()\n"
                                           "called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        testobj.rownum = 0
        result = testobj.add_row('name')
        assert isinstance(result[0], testee.wx.CheckBox)
        assert isinstance(result[1], testee.wxfb.FileBrowseButton)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called CheckBox.__init__ with args"
                f" ({testobj.scrl},) {{'label': 'name', 'size': (150, -1)}}\n"
                "called hori sizer.Add with args MockCheckBox (0, 2048, 16, 5)\n"
                "called FileBrowseButton.__init__ with args"
                f" ({testobj.scrl},) {{'size': (400, -1), 'style': 134217728,"
                " 'labelText': '', 'buttonText': '',"
                f" 'initialValue': '{testee.shared.HERE}/plugins',"
                " 'toolTip': '', 'dialogTitle': ''}\n"
                "called hori sizer.Add with args MockFileBrowse (0, 8240, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0,)\n"
                "called  sizer.Layout with args ()\n"
                "called ScrolledPanel.Fit with args ()\n"
                "called  sizer.Layout with args ()\n"
                f"called ScrolledPanel.ScrollChildIntoView with arg {result[1]}\n")
        testobj.rownum = 0
        result = testobj.add_row('name', 'xxx', 'btcp', 'dlgttl', 'tttext')
        assert isinstance(result[0], testee.wx.CheckBox)
        assert isinstance(result[1], testee.wxfb.FileBrowseButton)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called CheckBox.__init__ with args"
                f" ({testobj.scrl},) {{'label': 'name', 'size': (150, -1)}}\n"
                "called hori sizer.Add with args MockCheckBox (0, 2048, 16, 5)\n"
                "called FileBrowseButton.__init__ with args"
                f" ({testobj.scrl},) {{'size': (400, -1), 'style': 134217728,"
                " 'labelText': '', 'buttonText': 'btcp', 'initialValue': 'xxx',"
                " 'toolTip': 'tttext', 'dialogTitle': 'dlgttl'}\n"
                "called hori sizer.Add with args MockFileBrowse (0, 8240, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0,)\n"
                "called  sizer.Layout with args ()\n"
                "called ScrolledPanel.Fit with args ()\n"
                "called  sizer.Layout with args ()\n"
                f"called ScrolledPanel.ScrollChildIntoView with arg {result[1]}\n")

    def test_delete_row(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        testobj.scrl = mockwx.MockScrolledPanel()
        testobj.gsizer = mockwx.MockBoxSizer()
        check = mockwx.MockCheckBox()
        browse = mockwx.MockFileBrowse()
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args ()\n"
                                           "called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n"
                                           "called CheckBox.__init__ with args () {}\n"
                                           "called FileBrowseButton.__init__ with args () {}\n")
        testobj.delete_row('rownum', check, browse)
        assert capsys.readouterr().out == ("called BoxSizer.Remove with args ('rownum',)\n"
                                           "called CheckBox.Destroy with args ()\n"
                                           "called FileBrowseButton.Destroy with args ()\n"
                                           "called  sizer.Layout with args ()\n"
                                           "called ScrolledPanel.Fit with args ()\n"
                                           "called  sizer.Layout with args ()\n")

    def test_get_browser_value(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.get_browser_value
        """
        browse = mockwx.MockFileBrowse()
        assert capsys.readouterr().out == "called FileBrowseButton.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_browser_value(browse) == 'value from filebrowse'
        assert capsys.readouterr().out == ("called FileBrowseButton.GetValue\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.accept
        """
        def mock_confirm():
            print('called FilesDialog.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept()
        assert capsys.readouterr().out == ("called FilesDialog.confirm\n")


# niet gebruikt - verwijderen?
# class TestFileBrowseButton:
#     """unittest for wxgui.FileBrowseButton
#     """
#     def setup_testobj(self, monkeypatch, capsys):
#         """stub for wxgui.FileBrowseButton object
#
#         create the object skipping the normal initialization
#         intercept messages during creation
#         return the object so that other methods can be monkeypatched in the caller
#         """
#         def mock_init(self, *args):
#             """stub
#             """
#             print('called FileBrowseButton.__init__ with args', args)
#         monkeypatch.setattr(testee.FileBrowseButton, '__init__', mock_init)
#         testobj = testee.FileBrowseButton()
#         assert capsys.readouterr().out == 'called FileBrowseButton.__init__ with args ()\n'
#         return testobj
#
#     def _test_init(self, monkeypatch, capsys):
#         """unittest for FileBrowseButton.__init__
#         """
#         testobj = testee.FileBrowseButton(parent, text="", level_down=False)
#         assert capsys.readouterr().out == ("")
#
#     def _test_browse(self, monkeypatch, capsys):
#         """unittest for FileBrowseButton.browse
#         """
#         testobj = self.setup_testobj(monkeypatch, capsys)
#         assert testobj.browse() == "expected_result"
#         assert capsys.readouterr().out == ("")


class TestSetupDialogGui:
    """unittest for wxgui.SetupDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.SetupDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SetupDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.SetupDialogGui, '__init__', mock_init)
        testobj = testee.SetupDialogGui()
        assert capsys.readouterr().out == 'called SetupDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = testee.SetupDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.box, testee.wx.BoxSizer)
        assert isinstance(testobj.grid, testee.wx.FlexGridSizer)
        assert testobj.lineno == -1
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title'}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called vert sizer.Add with args FlexGridSizer (0, 240, 5)\n"
                "called dialog.SetSizer with args (vert sizer,)\n")

    def test_add_textinput_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_textinput_line
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.lineno = 1
        result = testobj.add_textinput_line('text', 'suggest')
        assert isinstance(result, testee.wx.TextCtrl)
        assert testobj.lineno == 2
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj},) {{'value': 'suggest', 'size': (160, -1)}}\n"
                "called GridSizer.Add with args MockStaticText (0, 2128, 5)\n"
                "called GridSizer.Add with args MockTextCtrl (0, 96, 5)\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_checkbox_line
        """
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.box = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.lineno = 1
        result = testobj.add_checkbox_line('text')
        assert isinstance(result, testee.wx.CheckBox)
        assert testobj.lineno == 2
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj}, 'text') {{}}\n"
                "called GridSizer.Add with args MockCheckBox (0, 16, 15)\n")

    def test_add_filebrowse_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_filebrowse_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wxfb, 'FileBrowseButton', mockwx.MockFileBrowse)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.box = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.add_filebrowse_line('text', 'suggest')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockStaticText (0, 2096, 5)\n"
                "called FileBrowseButton.__init__ with args"
                f" ({testobj},) {{'size': (300, -1), 'style': 134217728, 'labelText': '',"
                " 'buttonText': '', 'initialValue': 'suggest', 'toolTip': '', 'dialogTitle': ''}\n"
                "called hori sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args MockFileBrowse (0, 8224, 5)\n"
                "called GridSizer.Add with args MockBoxSizer (0, 8192)\n")
        testobj.add_filebrowse_line('text', 'suggest', 'btncp', 'dlgttl', 'tttext')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockStaticText (0, 2096, 5)\n"
                "called FileBrowseButton.__init__ with args"
                f" ({testobj},) {{'size': (300, -1), 'style': 134217728, 'labelText': '',"
                " 'buttonText': 'btncp', 'initialValue': 'suggest', 'toolTip': 'tttext',"
                " 'dialogTitle': 'dlgttl'}\n"
                "called hori sizer.AddStretchSpacer\n"
                "called hori sizer.Add with args MockFileBrowse (0, 8224, 5)\n"
                "called GridSizer.Add with args MockBoxSizer (0, 8192)\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.box = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 448, 5)\n"
                f"called  sizer.SetSizeHints with args ({testobj},)\n")

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_textinput_value
        """
        ted = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textinput_value(ted) == 'value from textctrl'
        assert capsys.readouterr().out == ("called text.GetValue\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_checkbox_value
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(cb) == 'value from checkbox'
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")

    def test_get_filebrowse_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_filebrowse_value
        """
        fbb = types.SimpleNamespace(input=mockwx.MockTextCtrl())
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_filebrowse_value(fbb) == 'value from textctrl'
        assert capsys.readouterr().out == ("called text.GetValue\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.accept
        """
        def mock_confirm():
            print('called SetupDialog.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept()
        assert capsys.readouterr().out == ("called SetupDialog.confirm\n")


class TestDeleteDialogGui:
    """unittest for wxgui.DeleteDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.DeleteDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called DeleteDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.DeleteDialogGui, '__init__', mock_init)
        testobj = testee.DeleteDialogGui()
        assert capsys.readouterr().out == 'called DeleteDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = testee.DeleteDialogGui('master', 'parent', 'title')
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.SetSizer with args (vert sizer,)\n")

    def test_add_text_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_text_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_text_line('text')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockStaticText (0, 48, 5)\n"
                "called  sizer.Add with args MockBoxSizer (1, 64, 5)\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_checkbox_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.add_checkbox_line('text')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called CheckBox.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockCheckBox (0, 16, 10)\n"
                "called  sizer.Add with args MockBoxSizer (1, 64, 5)\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 448, 2)\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_checkbox_value
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(cb) == 'value from checkbox'
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.accept
        """
        def mock_confirm():
            print('called DeleteDialog.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept()
        assert capsys.readouterr().out == ("called DeleteDialog.confirm\n")


class TestColumnSettingsDialogGui:
    """unittest for wxgui.ColumnSettingsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.ColumnSettingsDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ColumnSettingsDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.ColumnSettingsDialogGui, '__init__', mock_init)
        testobj = testee.ColumnSettingsDialogGui()
        assert capsys.readouterr().out == 'called ColumnSettingsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = testee.ColumnSettingsDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title'}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.SetSizer with args (vert sizer,)\n")

    def test_add_explanation(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_explanation
        """
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_explanation('text')
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called  sizer.Add with args MockStaticText (0, 496, 5)\n")

    def test_add_captions(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_captions
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_captions([('cap', 10), ('tions', 20)])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddSpacer with args (10,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'cap'}}\n"
                "called hori sizer.Add with args MockStaticText (0, 16, 10)\n"
                "called hori sizer.AddSpacer with args (20,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'tions'}}\n"
                "called hori sizer.Add with args MockStaticText (0, 16, 20)\n"
                "called  sizer.Add with args MockBoxSizer ()\n")

    def test_add_columndefs_area(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_columndefs_area
        """
        monkeypatch.setattr(testee.wxsp, 'ScrolledPanel', mockwx.MockScrolledPanel)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.add_columndefs_area(), testee.wxsp.ScrolledPanel)
        assert capsys.readouterr().out == (
                f"called ScrolledPanel.__init__ with args ({testobj},) {{'style': 67108864}}\n"
                "called BoxSizer.__init__ with args (8,)\n")

    def test_finalize_columndefs_area(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.finalize_columndefs_area
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        scrl = mockwx.MockScrolledPanel()
        testobj.gsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args ()\n"
                                           "called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        testobj.finalize_columndefs_area(scrl)
        assert capsys.readouterr().out == (
                "called ScrolledPanel.Fit with args ()\n"
                "called ScrolledPanel.SetSizer with args ( sizer,)\n"
                f"called  sizer.SetSizeHints with args ({scrl},)\n"
                "called ScrolledPanel.SetupScrolling\n"
                "called  sizer.Add with args MockScrolledPanel (1, 8432, 5)\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_buttons
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_buttons([('ok', ''), ('cancel', ''), ('xxx', callback)])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback}) {{}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 448, 2)\n")

    def test_add_checkbox_to_line(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_checkbox_to_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.scrl = mockwx.MockScrolledPanel()
        assert capsys.readouterr().out == "called ScrolledPanel.__init__ with args () {}\n"
        result = testobj.add_checkbox_to_line(0, 0, 'text', 10, True, False)
        assert isinstance(result, testee.wx.CheckBox)
        assert isinstance(testobj.rowsizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddSpacer with args (True,)\n"
                f"called CheckBox.__init__ with args ({testobj.scrl}, 'text') {{'size': (10, -1)}}\n"
                "called hori sizer.Add with args MockCheckBox ()\n"
                "called hori sizer.Add with args MockBoxSizer (0,)\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.scrl = mockwx.MockScrolledPanel()
        testobj.rowsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        result = testobj.add_checkbox_to_line(0, 1, 'text', 10, False, True)
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called CheckBox.__init__ with args ({testobj.scrl}, 'text') {{'size': (10, -1)}}\n"
                "called hori sizer.Add with args MockCheckBox ()\n"
                "called hori sizer.AddSpacer with args (True,)\n"
                "called  sizer.Add with args MockBoxSizer (0,)\n")

    def test_add_combobox_to_line(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_combobox_to_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'ComboBox', mockwx.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.scrl = mockwx.MockScrolledPanel()
        testobj.rowsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        result = testobj.add_combobox_to_line(0, 0, [], 0)
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args"
                f" ({testobj.scrl},) {{'size': (140, -1), 'style': 32, 'choices': []}}\n"
                "called ComboBox.Bind with args"
                f" ({testee.wx.EVT_TEXT}, {testobj.on_text_changed}) {{}}\n"
                "called  sizer.Add with args MockComboBox (0, 16, 2)\n")
        result = testobj.add_combobox_to_line(0, 1, ['x', 'y'], 1)
        assert isinstance(result, testee.wx.ComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__ with args"
                f" ({testobj.scrl},) {{'size': (140, -1), 'style': 32, 'choices': ['x', 'y']}}\n"
                "called combobox.SetSelection with args (1,)\n"
                "called ComboBox.Bind with args"
                f" ({testee.wx.EVT_TEXT}, {testobj.on_text_changed}) {{}}\n"
                "called  sizer.Add with args MockComboBox (0, 16, 2)\n")

    def test_add_spinbox_to_line(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_spinbox_to_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'SpinCtrl', mockwx.MockSpinCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.scrl = mockwx.MockScrolledPanel()
        testobj.rowsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        result = testobj.add_spinbox_to_line(0, 0, 0, (0, 1), 10, (True, False))
        assert isinstance(result, testee.wx.SpinCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddSpacer with args (True,)\n"
                "called SpinCtrl.__init__ with args"
                f" ({testobj.scrl},) {{'size': (90, -1), 'style': 16384}}\n"
                "called SpinCtrl.SetRange with args (0, 1)\n"
                "called hori sizer.Add with args MockSpinCtrl ()\n"
                "called  sizer.Add with args MockBoxSizer (0,)\n")
        result = testobj.add_spinbox_to_line(0, 1, 5, (1, 10), 10, (False, True))
        assert isinstance(result, testee.wx.SpinCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called SpinCtrl.__init__ with args"
                f" ({testobj.scrl},) {{'size': (90, -1), 'style': 16384}}\n"
                "called SpinCtrl.SetRange with args (1, 10)\n"
                "called SpinCtrl.SetValue with args (5,)\n"
                "called hori sizer.Add with args MockSpinCtrl ()\n"
                "called hori sizer.AddSpacer with args (True,)\n"
                "called  sizer.Add with args MockBoxSizer (0,)\n")

    def test_finalize_line(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.finalize_line
        """
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        scrl = mockwx.MockScrolledPanel()
        testobj.gsizer = mockwx.MockBoxSizer()
        testobj.rowsizer = mockwx.MockBoxSizer()
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n"
                                           "called BoxSizer.__init__ with args ()\n"
                                           "called BoxSizer.__init__ with args ()\n")
        testobj.finalize_line(scrl, 'checkbox')
        assert capsys.readouterr().out == (
                "called  sizer.Add with args MockBoxSizer (0, 8240, 5)\n"
                "called  sizer.Layout with args ()\n"
                "called ScrolledPanel.Fit with args ()\n"
                "called  sizer.Layout with args ()\n")

    def test_adapt_column_index(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.adapt_column_index
        """
        current_widget = mockwx.MockSpinCtrl()
        current_widget.SetValue(1)
        removed_widget = mockwx.MockSpinCtrl()
        removed_widget.SetValue(1)
        assert capsys.readouterr().out == ("called SpinCtrl.__init__ with args () {}\n"
                                           "called SpinCtrl.SetValue with args (1,)\n"
                                           "called SpinCtrl.__init__ with args () {}\n"
                                           "called SpinCtrl.SetValue with args (1,)\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.adapt_column_index(removed_widget, current_widget)
        assert capsys.readouterr().out == ("called SpinCtrl.GetValue\n"
                                           "called SpinCtrl.GetValue\n")
        current_widget.SetValue(2)
        assert capsys.readouterr().out == "called SpinCtrl.SetValue with args (2,)\n"
        testobj.adapt_column_index(removed_widget, current_widget)
        assert capsys.readouterr().out == ("called SpinCtrl.GetValue\n"
                                           "called SpinCtrl.GetValue\n"
                                           "called SpinCtrl.GetValue\n"
                                           "called SpinCtrl.SetValue with args (1,)\n")

    def test_delete_row(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.scrl = mockwx.MockScrolledPanel()
        testobj.gsizer = mockwx.MockBoxSizer()
        testobj.sizer = mockwx.MockBoxSizer()
        w0 = mockwx.MockControl()
        w1 = mockwx.MockControl()
        assert capsys.readouterr().out == ("called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n"
                                           "called BoxSizer.__init__ with args ()\n"
                                           "called Control.__init__\n"
                                           "called Control.__init__\n")
        testobj.delete_row(1, [w0, w1])
        assert capsys.readouterr().out == ("called BoxSizer.Remove with args (1,)\n"
                                           "called Control.Destroy with args ()\n"
                                           "called Control.Destroy with args ()\n"
                                           "called  sizer.Layout with args ()\n"
                                           "called ScrolledPanel.Fit with args ()\n"
                                           "called  sizer.Layout with args ()\n")

    def test_on_text_changed(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.on_text_changed
        """
        class MockComboBox:
            "stub"
            def __init__(self, *args, **kwargs):
                self._text = args[0]
            def GetValue(self):
                print('called ComboBox.GetValue')
                return self._text
            def GetItems(self):
                print('called ComboBox.GetItems')
                return []
            def SetSelection(self, *args):
                print(f'called combobox.SetSelection with args', args)
        def mock_get(self):
            print('called Event.GetEventObject')
            return name2
        def mock_get_2(self):
            print('called ComboBox.GetItems')
            return ['xxx', 'name21', 'yyy']
        name1 = MockComboBox('name1')
        width1 = mockwx.MockSpinCtrl(10)
        name2 = MockComboBox('name2')
        width2 = mockwx.MockSpinCtrl(1)
        monkeypatch.setattr(mockwx.MockEvent, 'GetEventObject', mock_get)
        event = mockwx.MockEvent()
        assert capsys.readouterr().out == ("called SpinCtrl.__init__ with args (10,) {}\n"
                                           "called SpinCtrl.__init__ with args (1,) {}\n"
                                           "called event.__init__ with args ()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(data=[])
        testobj.on_text_changed(event)
        assert capsys.readouterr().out == ("called Event.GetEventObject\n"
                                           "called ComboBox.GetValue\n"
                                           "called ComboBox.GetItems\n")
        monkeypatch.setattr(MockComboBox, 'GetItems', mock_get_2)
        testobj.master.data = [(name1, width1, 'x', 'y'), (name2, width2, 'a', 'b')]
        testobj.on_text_changed(event)
        assert capsys.readouterr().out == ("called Event.GetEventObject\n"
                                           "called ComboBox.GetValue\n"
                                           "called ComboBox.GetItems\n"
                                           "called combobox.SetSelection with args (1,)\n"
                                           "called SpinCtrl.SetValue with args (60,)\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_checkbox_value
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(cb) == 'value from checkbox'
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.accept
        """
        def mock_confirm():
            print('called FilesDialog.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept()
        assert capsys.readouterr().out == ("called FilesDialog.confirm\n")


class TestNewColumnsDialogGui:
    """unittest for wxgui.NewColumnsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.NewColumnsDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called NewColumnsDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.NewColumnsDialogGui, '__init__', mock_init)
        testobj = testee.NewColumnsDialogGui()
        assert capsys.readouterr().out == 'called NewColumnsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'GridSizer', mockwx.MockGridSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        master = types.SimpleNamespace(dialog_data={'languages': ['en', 'nl']})
        testobj = testee.NewColumnsDialogGui(master, 'parent', 'title')
        assert testobj.master == master
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert isinstance(testobj.gsizer, testee.wx.GridSizer)
        assert not testobj.initializing
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'title': 'title'}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called GridSizer.__init__ with args (3, 2, 2) {}\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.SetSizer with args (vert sizer,)\n")

    def test_add_explanation(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.add_explanation
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_explanation('text')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockStaticText ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 240, 5)\n")

    def test_add_titles(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.add_captions
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        testobj.add_titles(['cap', 'tions'])
        assert capsys.readouterr().out == (
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'cap'}}\n"
                "called GridSizer.Add with args MockStaticText (0, 2064, 10)\n"
                f"called StaticText.__init__ with args ({testobj},) {{'label': 'tions'}}\n"
                "called GridSizer.Add with args MockStaticText (0, 2064, 10)\n")

    def test_add_text_entry(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.add_text_entry
        """
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockwx.MockGridSizer()
        assert capsys.readouterr().out == "called GridSizer.__init__ with args () {}\n"
        result = testobj.add_text_entry('text', '', '', 'enabled')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                f"called TextCtrl.__init__ with args ({testobj},) {{'value': 'text'}}\n"
                f"called text.Enable with arg enabled\n"
                "called GridSizer.Add with args MockTextCtrl (0, 8432)\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 448, 5)\n")

    def test_get_textentry_value(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.get_textentry_value
        """
        ted = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textentry_value(ted) == 'value from textctrl'
        assert capsys.readouterr().out == ("called text.GetValue\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.accept
        """
        def mock_confirm():
            print('called NewColumnsDialog.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept()
        assert capsys.readouterr().out == ("called NewColumnsDialog.confirm\n")


class TestExtraSettingsDialogGui:
    """unittest for wxgui.ExtraSettingsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.ExtraSettingsDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ExtraSettingsDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.ExtraSettingsDialogGui, '__init__', mock_init)
        testobj = testee.ExtraSettingsDialogGui()
        assert capsys.readouterr().out == 'called ExtraSettingsDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = testee.ExtraSettingsDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args () {'size': (680, 400), 'title': 'title'}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                f"called vert sizer.SetSizeHints with args ({testobj},)\n"
                "called dialog.SetSizer with args (vert sizer,)\n")

    def test_start_block(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.start_block
        """
        monkeypatch.setattr(testee.wx, 'Panel', mockwx.MockPanel)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        assert isinstance(testobj.start_block(), testee.wx.BoxSizer)
        assert isinstance(testobj.pnl, testee.wx.Panel)
        assert capsys.readouterr().out == (
                f"called Panel.__init__ with args ({testobj},) {{'style': 67108864}}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called Panel.SetSizer with args (vert sizer,)\n"
                "called  sizer.Add with args MockPanel (0, 8432, 10)\n")

    def test_add_textinput_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_textinput_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.pnl = mockwx.MockPanel()
        assert capsys.readouterr().out == "called Panel.__init__ with args () {}\n"
        result = testobj.add_textinput_line(sizer, 'text', 'suggest')
        assert isinstance(result, testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj.pnl},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockStaticText (0, 2048)\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj.pnl},) {{'value': 'suggest', 'size': (260, -1)}}\n"
                "called hori sizer.Add with args MockTextCtrl (0, 8272, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 8240, 5)\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_checkbox_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.pnl = mockwx.MockPanel()
        assert capsys.readouterr().out == "called Panel.__init__ with args () {}\n"
        result = testobj.add_checkbox_line(vsizer, 'text', 'value')
        assert isinstance(result, testee.wx.CheckBox)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called CheckBox.__init__ with args ({testobj.pnl},) {{'label': 'text'}}\n"
                "called checkbox.SetValue with args ('value',)\n"
                "called hori sizer.Add with args MockCheckBox (0,)\n"
                "called  sizer.Add with args MockBoxSizer (0, 48, 5)\n")

    def test_add_text_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_text_line
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.pnl = mockwx.MockPanel()
        assert capsys.readouterr().out == "called Panel.__init__ with args () {}\n"
        testobj.add_text_line(vsizer, 'text')
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called StaticText.__init__ with args ({testobj.pnl},) {{'label': 'text'}}\n"
                "called hori sizer.Add with args MockStaticText (0,)\n"
                "called  sizer.Add with args MockBoxSizer (0, 304, 5)\n")

    def test_add_titles(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_titles
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'StaticText', mockwx.MockStaticText)
        testobj = self.setup_testobj(monkeypatch, capsys)
        vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.pnl = mockwx.MockPanel()
        assert capsys.readouterr().out == "called Panel.__init__ with args () {}\n"
        testobj.add_titles(vsizer, [(10, 'cap'), (20, 'tions')])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called hori sizer.AddSpacer with args (10,)\n"
                f"called StaticText.__init__ with args ({testobj.pnl},) {{'label': 'cap'}}\n"
                "called hori sizer.Add with args MockStaticText (0,)\n"
                "called hori sizer.AddSpacer with args (20,)\n"
                f"called StaticText.__init__ with args ({testobj.pnl},) {{'label': 'tions'}}\n"
                "called hori sizer.Add with args MockStaticText (0,)\n"
                "called  sizer.Add with args MockBoxSizer (0,)\n")

    def test_add_inputarea(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_inputarea
        """
        monkeypatch.setattr(testee.wxsp, 'ScrolledPanel', mockwx.MockScrolledPanel)
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        testobj = self.setup_testobj(monkeypatch, capsys)
        vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.pnl = mockwx.MockPanel()
        assert capsys.readouterr().out == "called Panel.__init__ with args () {}\n"
        assert isinstance(testobj.add_inputarea(vsizer), testee.wxsp.ScrolledPanel)
        assert isinstance(testobj.scrl, testee.wxsp.ScrolledPanel)
        assert isinstance(testobj.gsizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                f"called ScrolledPanel.__init__ with args ({testobj.pnl},) {{'style': 33554432}}\n"
                "called BoxSizer.__init__ with args (8,)\n")

    def test_finalize_inputarea(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.finalize_inputarea
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        vsizer = mockwx.MockBoxSizer()
        scroller = mockwx.MockScrolledPanel()
        testobj.gsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args ()\n"
                                           "called ScrolledPanel.__init__ with args () {}\n"
                                           "called BoxSizer.__init__ with args ()\n")
        testobj.finalize_inputarea(vsizer, scroller)
        assert capsys.readouterr().out == (
                # "called ScrolledPanel.Fit with args ()\n"
                "called ScrolledPanel.SetSizer with args ( sizer,)\n"
                f"called  sizer.Fit with args ({scroller},)\n"
                f"called  sizer.SetSizeHints with args ({scroller},)\n"
                "called ScrolledPanel.SetupScrolling\n"
                "called  sizer.Add with args MockScrolledPanel (1, 8432, 5)\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_buttons
        """
        def callback1():
            "dummy function"
        def callback2():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        vsizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.pnl = mockwx.MockPanel()
        assert capsys.readouterr().out == "called Panel.__init__ with args () {}\n"
        testobj.add_buttons(vsizer, [('xxx', callback1), ('yyy', callback2)])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj.pnl},) {{'label': 'xxx'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback1}) {{}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj.pnl},) {{'label': 'yyy'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback2}) {{}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 256)\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 384, 2)\n")

    def test_add_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_row
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'CheckBox', mockwx.MockCheckBox)
        monkeypatch.setattr(testee.wx, 'TextCtrl', mockwx.MockTextCtrl)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        gsizer = mockwx.MockBoxSizer()
        testobj.scrl = mockwx.MockScrolledPanel()
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args ()\n"
                                           "called BoxSizer.__init__ with args ()\n"
                                           "called ScrolledPanel.__init__ with args () {}\n")
        result = testobj.add_row(gsizer, '', '', '')
        assert isinstance(result[0], testee.wx.CheckBox)
        assert isinstance(result[1], testee.wx.TextCtrl)
        assert isinstance(result[2], testee.wx.TextCtrl)
        assert isinstance(result[3], testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                f"called CheckBox.__init__ with args ({testobj.scrl},) {{}}\n"
                "called hori sizer.Add with args MockCheckBox (0, 2064, 5)\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj.scrl},) {{'value': '', 'size': (120, -1)}}\n"
                "called hori sizer.Add with args MockTextCtrl (0, 48, 2)\n"
                "called hori sizer.Add with args MockBoxSizer (0,)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj.scrl},) {{'value': '', 'size': (320, -1)}}\n"
                "called vert sizer.Add with args MockTextCtrl (1,)\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj.scrl},) {{'value': '', 'size': (320, -1)}}\n"
                "called vert sizer.Add with args MockTextCtrl (1,)\n"
                "called hori sizer.Add with args MockBoxSizer (0, 8224, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 8192)\n"
                "called  sizer.Layout with args ()\n"
                "called ScrolledPanel.Fit with args ()\n"
                f"called ScrolledPanel.ScrollChildIntoView with arg {result[3]}\n"
                "called  sizer.Layout with args ()\n")
        result = testobj.add_row(gsizer, name='xxx', value='yyy', desc='zzz')
        assert isinstance(result[0], testee.wx.CheckBox)
        assert isinstance(result[1], testee.wx.TextCtrl)
        assert isinstance(result[2], testee.wx.TextCtrl)
        assert isinstance(result[3], testee.wx.TextCtrl)
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                "called BoxSizer.__init__ with args (4,)\n"
                f"called CheckBox.__init__ with args ({testobj.scrl},) {{}}\n"
                "called hori sizer.Add with args MockCheckBox (0, 2064, 5)\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj.scrl},) {{'value': 'xxx', 'size': (120, -1)}}\n"
                "called text.SetEditable with arg False\n"
                "called hori sizer.Add with args MockTextCtrl (0, 48, 2)\n"
                "called hori sizer.Add with args MockBoxSizer (0,)\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj.scrl},) {{'value': 'yyy', 'size': (320, -1)}}\n"
                "called vert sizer.Add with args MockTextCtrl (1,)\n"
                "called TextCtrl.__init__ with args"
                f" ({testobj.scrl},) {{'value': 'zzz', 'size': (320, -1)}}\n"
                "called vert sizer.Add with args MockTextCtrl (1,)\n"
                "called hori sizer.Add with args MockBoxSizer (0, 8224, 5)\n"
                "called  sizer.Add with args MockBoxSizer (0, 8192)\n"
                "called  sizer.Layout with args ()\n"
                "called ScrolledPanel.Fit with args ()\n"
                f"called ScrolledPanel.ScrollChildIntoView with arg {result[3]}\n"
                "called  sizer.Layout with args ()\n")

    def test_delete_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        gsizer = mockwx.MockBoxSizer()
        testobj.scrl = mockwx.MockScrolledPanel()
        widget1 = mockwx.MockControl()
        widget2 = mockwx.MockControl()
        widget3 = mockwx.MockControl()
        widget4 = mockwx.MockControl()
        assert capsys.readouterr().out == ("called BoxSizer.__init__ with args ()\n"
                                           "called BoxSizer.__init__ with args ()\n"
                                           "called ScrolledPanel.__init__ with args () {}\n"
                                           "called Control.__init__\n"
                                           "called Control.__init__\n"
                                           "called Control.__init__\n"
                                           "called Control.__init__\n")
        testobj.delete_row(gsizer, 1, [widget1, widget2, widget3, widget4])
        assert capsys.readouterr().out == ("called BoxSizer.Remove with args (4,)\n"
                                           "called BoxSizer.Remove with args (5,)\n"
                                           "called BoxSizer.Remove with args (6,)\n"
                                           "called BoxSizer.Remove with args (7,)\n"
                                           "called Control.Destroy with args ()\n"
                                           "called Control.Destroy with args ()\n"
                                           "called Control.Destroy with args ()\n"
                                           "called Control.Destroy with args ()\n"
                                           "called  sizer.Layout with args ()\n"
                                           "called ScrolledPanel.Fit with args ()\n"
                                           "called  sizer.Layout with args ()\n")

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_textinput_value
        """
        ted = mockwx.MockTextCtrl()
        assert capsys.readouterr().out == "called TextCtrl.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_textinput_value(ted) == 'value from textctrl'
        assert capsys.readouterr().out == ("called text.GetValue\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_checkbox_value
        """
        cb = mockwx.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__ with args () {}\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_checkbox_value(cb) == 'value from checkbox'
        assert capsys.readouterr().out == ("called checkbox.GetValue\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.accept
        """
        def mock_confirm():
            print('called FilesDialog.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept()
        assert capsys.readouterr().out == ("called FilesDialog.confirm\n")


class TestEntryDialogGui:
    """unittest for wxgui.EntryDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.EntryDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EntryDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.EntryDialogGui, '__init__', mock_init)
        testobj = testee.EntryDialogGui()
        assert capsys.readouterr().out == 'called EntryDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for EntryDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = testee.EntryDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args"
                " () {'size': (1000, 800), 'title': 'title', 'style': 536877120}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n")

    def test_add_table_to_display(self, monkeypatch, capsys):
        """unittest for EntryDialogGui.add_table_to_display
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wxg, 'Grid', mockwx.MockGrid)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.add_table_to_display([('xxx', 10), ('yyy', 20)])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Grid.__init__ with args ({testobj},)\n"
                "called Grid.CreateGrid with args (0, 2)\n"
                "called Grid.SetRowLabelSize with args (20,)\n"
                "called Grid.SetColLabelValue with args (0, 'xxx')\n"
                "called Grid.SetColSize with args (0, 10)\n"
                "called Grid.SetColLabelValue with args (1, 'yyy')\n"
                "called Grid.SetColSize with args (1, 20)\n"
                "called hori sizer.Add with args MockGrid (1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8192)\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_buttons
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_buttons([('ok', ''), ('cancel', ''), ('xxx', callback)])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'label': 'xxx'}}\n"
                f"called Button.Bind with args ({testee.wx.EVT_BUTTON}, {callback}) {{}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 384, 2)\n")

    def test_add_row(self, monkeypatch, capsys):
        """unittest for EntryDialogGui.add_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args ()\n"
        testobj.add_row(p0list, 1, ['xxx', 'yyy'])
        assert capsys.readouterr().out == ("called Grid.AppendRows with args ()\n"
                                           "called Grid.SetCellValue with args (1, 0, 'xxx')\n"
                                           "called Grid.SetCellValue with args (1, 1, 'yyy')\n"
                                           "called Grid.ShowRow with args (1,)\n")

    def test_delete_key(self, monkeypatch, capsys):
        """unittest for EntryDialogGui.delete_key
        """
        def mock_get(self, *args):
            print('called Grid.GetSelectedRows')
            return ['row1', 'row2']
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args ()\n"
        testobj.delete_key(p0list, 'event')
        assert capsys.readouterr().out == ("called Grid.GetSelectedRows\n")
        monkeypatch.setattr(mockwx.MockGrid, 'GetSelectedRows', mock_get)
        testobj.delete_key(p0list, 'event')
        assert capsys.readouterr().out == ("called Grid.GetSelectedRows\n"
                                           "called Grid.DeleteRows with args ('row1',)\n"
                                           "called Grid.DeleteRows with args ('row2',)\n")

    def test_get_tableitem_value(self, monkeypatch, capsys):
        """unittest for EntryDialogGui.get_tableitemr_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args ()\n"
        assert testobj.get_tableitem_value(p0list, 'row', 'col') == "value at ('row', 'col')"
        assert capsys.readouterr().out == ("called Grid.GetCellValue with args ('row', 'col')\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for EntryDialogGui.accept
        """
        def mock_confirm():
            print('called FilesDialog.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept()
        assert capsys.readouterr().out == ("called FilesDialog.confirm\n")


class TestCompleteDialogGui:
    """unittest for wxgui.CompleteDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for wxgui.CompleteDialogGui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CompleteDialogGui.__init__ with args', args)
        monkeypatch.setattr(testee.CompleteDialogGui, '__init__', mock_init)
        testobj = testee.CompleteDialogGui()
        assert capsys.readouterr().out == 'called CompleteDialogGui.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.__init__
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx.Dialog, '__init__', mockwx.MockDialog.__init__)
        monkeypatch.setattr(testee.wx.Dialog, 'SetSizer', mockwx.MockDialog.SetSizer)
        testobj = testee.CompleteDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.wx.BoxSizer)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args"
                " () {'title': 'title', 'size': (1016, 800), 'style': 536877120}\n"
                "called BoxSizer.__init__ with args (8,)\n"
                "called dialog.SetSizer with args (vert sizer,)\n")

    def test_add_table_to_display(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.add_table_to_display
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wxg, 'Grid', mockwx.MockGrid)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        result = testobj.add_table_to_display([('xxx', 10), ('yyy', 20)])
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Grid.__init__ with args ({testobj},)\n"
                "called Grid.CreateGrid with args (0, 2)\n"
                "called Grid.SetRowLabelSize with args (20,)\n"
                "called Grid.SetColLabelValue with args (0, 'xxx')\n"
                "called Grid.SetColSize with args (0, 10)\n"
                "called Grid.SetColLabelValue with args (1, 'yyy')\n"
                "called Grid.SetColSize with args (1, 990)\n"
                "called hori sizer.Add with args MockGrid (1, 8192)\n"
                "called  sizer.Add with args MockBoxSizer (1, 8192)\n")

    def test_add_row(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.add_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args ()\n"
        testobj.add_row(p0list, 1, 'xxx', 'yyy', 'zzz')
        assert capsys.readouterr().out == ("called Grid.AppendRows with args ()\n"
                                           "called Grid.SetCellValue with args (1, 0, 'xxx')\n"
                                           "called Grid.SetCellValue with args (1, 1, 'yyy')\n"
                                           "called Grid.SetCellValue with args (1, 2, 'zzz')\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
        monkeypatch.setattr(testee.wx, 'Button', mockwx.MockButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockwx.MockBoxSizer()
        assert capsys.readouterr().out == "called BoxSizer.__init__ with args ()\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == (
                "called BoxSizer.__init__ with args (4,)\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5100}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                f"called Button.__init__ with args ({testobj},) {{'id': 5101}}\n"
                "called hori sizer.Add with args MockButton ()\n"
                "called  sizer.Add with args MockBoxSizer (0, 384, 2)\n")

    def test_set_focus_to_list(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.set_focus_to_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockwx.MockGrid()
        assert capsys.readouterr().out == "called Grid.__init__ with args ()\n"
        testobj.set_focus_to_list(p0list)
        assert capsys.readouterr().out == ("called Grid.GoToCell with args (0, 1)\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.accept
        """
        def mock_confirm():
            print('called CompleteDialog.confirm')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        assert testobj.accept()
        assert capsys.readouterr().out == ("called CompleteDialog.confirm\n")
