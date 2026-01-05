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
                f"called NoteBook.__init__ with args ({testobj},)\n")

    def test_add_subscreen(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_subscreen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
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

    def test_get_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        assert testobj.get_panel() == "page"
        assert capsys.readouterr().out == "called NoteBook.GetCurrentPage\n"

    def test_set_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.set_selected_panel('indx')
        assert capsys.readouterr().out == ("called NoteBook.SetSelection with args ('indx',)\n")

    def test_get_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        assert testobj.get_selected_panel('indx') == "page"
        assert capsys.readouterr().out == ("called NoteBook.GetPage with args ('indx',)\n")

    def test_replace_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.replace_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockwx.MockNoteBook()
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
        testobj.replace_panel('indx', 'win', 'newwin')
        assert capsys.readouterr().out == (
                "called NoteBook.InsertPage with args ('indx', 'newwin')\n"
                "called NoteBook.SetSelection with args ('newwin',)\n"
                "called NoteBook.RemovePage with args ('win',)\n")

    # def test_set_panel_editable(self, monkeypatch, capsys):
    #     """unittest for TabbedInterface.set_panel_editable
    #     """
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj.pnl = mockwx.MockNoteBook()
    #     assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
    #     testobj.set_panel_editable(test_redef)
    #     assert capsys.readouterr().out == ("")

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
        assert capsys.readouterr().out == "called NoteBook.__init__ with args ()\n"
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
        testobj.finalize_screen()
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
        assert capsys.readouterr().out == "called ListCtrl.DeleteAllItems with args ()\n"

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


def _test_show_message(monkeypatch, capsys):
    """unittest for dialogs_wx.show_message
    """
    assert testee.show_message(win, message_id='', text='', args=None) == "expected_result"


def _test_show_cancel_message(monkeypatch, capsys):
    """unittest for dialogs_wx.show_cancel_message
    """
    assert testee.show_cancel_message(win, message_id='', text='', args=None) == "expected_result"


def _test_ask_question(monkeypatch, capsys):
    """unittest for dialogs_wx.ask_question
    """
    assert testee.ask_question(win, message_id='', text='', args=None) == "expected_result"


def _test_ask_ync_question(monkeypatch, capsys):
    """unittest for dialogs_wx.ask_ync_question
    """
    assert testee.ask_ync_question(win, message_id='', text='', args=None) == "expected_result"


def _test_get_textinput(monkeypatch, capsys):
    """unittest for dialogs_wx.get_textinput
    """
    assert testee.get_textinput(win, text, prompt='') == "expected_result"


def _test_get_choice(monkeypatch, capsys):
    """unittest for dialogs_wx.get_choice
    """
    assert testee.get_choice(win, title, caption, choices, current) == "expected_result"


def _test_get_file_to_open(monkeypatch, capsys):
    """unittest for dialogs_wx.get_file_to_open
    """
    assert testee.get_file_to_open(win, oms='', extension='', start='') == "expected_result"


def _test_get_file_to_save(monkeypatch, capsys):
    """unittest for dialogs_wx.get_file_to_save
    """
    assert testee.get_file_to_save(win, oms='', extension='', start='') == "expected_result"


def _test_show_dialog(monkeypatch, capsys):
    """unittest for dialogs_wx.show_dialog
    """
    assert testee.show_dialog(win, cls) == "expected_result"


class TestInitialToolDialog:
    """unittest for dialogs_wx.InitialToolDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.InitialToolDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called InitialToolDialog.__init__ with args', args)
        monkeypatch.setattr(testee.InitialToolDialog, '__init__', mock_init)
        testobj = testee.InitialToolDialog()
        assert capsys.readouterr().out == 'called InitialToolDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for InitialToolDialog.__init__
        """
        testobj = testee.InitialToolDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for InitialToolDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestFileBrowseButton:
    """unittest for dialogs_wx.FileBrowseButton
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.FileBrowseButton object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FileBrowseButton.__init__ with args', args)
        monkeypatch.setattr(testee.FileBrowseButton, '__init__', mock_init)
        testobj = testee.FileBrowseButton()
        assert capsys.readouterr().out == 'called FileBrowseButton.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for FileBrowseButton.__init__
        """
        testobj = testee.FileBrowseButton(parent, text="", level_down=False)
        assert capsys.readouterr().out == ("")

    def _test_browse(self, monkeypatch, capsys):
        """unittest for FileBrowseButton.browse
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.browse() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestSetupDialog:
    """unittest for dialogs_wx.SetupDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.SetupDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SetupDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SetupDialog, '__init__', mock_init)
        testobj = testee.SetupDialog()
        assert capsys.readouterr().out == 'called SetupDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for SetupDialog.__init__
        """
        testobj = testee.SetupDialog(parent, name)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for SetupDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestDeleteDialog:
    """unittest for dialogs_wx.DeleteDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.DeleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called DeleteDialog.__init__ with args', args)
        monkeypatch.setattr(testee.DeleteDialog, '__init__', mock_init)
        testobj = testee.DeleteDialog()
        assert capsys.readouterr().out == 'called DeleteDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for DeleteDialog.__init__
        """
        testobj = testee.DeleteDialog(parent)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for DeleteDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestFilesDialog:
    """unittest for dialogs_wx.FilesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.FilesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FilesDialog.__init__ with args', args)
        monkeypatch.setattr(testee.FilesDialog, '__init__', mock_init)
        testobj = testee.FilesDialog()
        assert capsys.readouterr().out == 'called FilesDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for FilesDialog.__init__
        """
        testobj = testee.FilesDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_add_row(self, monkeypatch, capsys):
        """unittest for FilesDialog.add_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_row(name, path='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_row(self, monkeypatch, capsys):
        """unittest for FilesDialog.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_row(rownum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_program(self, monkeypatch, capsys):
        """unittest for FilesDialog.add_program
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_program(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_programs(self, monkeypatch, capsys):
        """unittest for FilesDialog.remove_programs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_programs(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for FilesDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestColumnSettingsDialog:
    """unittest for dialogs_wx.ColumnSettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.ColumnSettingsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ColumnSettingsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ColumnSettingsDialog, '__init__', mock_init)
        testobj = testee.ColumnSettingsDialog()
        assert capsys.readouterr().out == 'called ColumnSettingsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.__init__
        """
        testobj = testee.ColumnSettingsDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_add_row(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.add_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_row(name='', width='', is_flag=False, colno='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_on_text_changed(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.on_text_changed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.on_text_changed(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_row(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_row(rownum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_column(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.add_column
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_column(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_columns(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.remove_columns
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_columns(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestNewColumnsDialog:
    """unittest for dialogs_wx.NewColumnsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.NewColumnsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called NewColumnsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.NewColumnsDialog, '__init__', mock_init)
        testobj = testee.NewColumnsDialog()
        assert capsys.readouterr().out == 'called NewColumnsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for NewColumnsDialog.__init__
        """
        testobj = testee.NewColumnsDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for NewColumnsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestExtraSettingsDialog:
    """unittest for dialogs_wx.ExtraSettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.ExtraSettingsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ExtraSettingsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ExtraSettingsDialog, '__init__', mock_init)
        testobj = testee.ExtraSettingsDialog()
        assert capsys.readouterr().out == 'called ExtraSettingsDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.__init__
        """
        testobj = testee.ExtraSettingsDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_add_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.add_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_row(name='', value='', desc='') == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_row(rownum) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_add_setting(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.add_setting
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_setting(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_remove_settings(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.remove_settings
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.remove_settings(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestEntryDialog:
    """unittest for dialogs_wx.EntryDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.EntryDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EntryDialog.__init__ with args', args)
        monkeypatch.setattr(testee.EntryDialog, '__init__', mock_init)
        testobj = testee.EntryDialog()
        assert capsys.readouterr().out == 'called EntryDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for EntryDialog.__init__
        """
        testobj = testee.EntryDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_add_key(self, monkeypatch, capsys):
        """unittest for EntryDialog.add_key
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.add_key(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_delete_key(self, monkeypatch, capsys):
        """unittest for EntryDialog.delete_key
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.delete_key(event) == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for EntryDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")


class TestCompleteDialog:
    """unittest for dialogs_wx.CompleteDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_wx.CompleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CompleteDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CompleteDialog, '__init__', mock_init)
        testobj = testee.CompleteDialog()
        assert capsys.readouterr().out == 'called CompleteDialog.__init__ with args ()\n'
        return testobj

    def _test_init(self, monkeypatch, capsys):
        """unittest for CompleteDialog.__init__
        """
        testobj = testee.CompleteDialog(parent, master)
        assert capsys.readouterr().out == ("")

    def _test_accept(self, monkeypatch, capsys):
        """unittest for CompleteDialog.accept
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.accept() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_read_data(self, monkeypatch, capsys):
        """unittest for CompleteDialog.read_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.read_data() == "expected_result"
        assert capsys.readouterr().out == ("")

    def _test_build_table(self, monkeypatch, capsys):
        """unittest for CompleteDialog.build_table
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_table() == "expected_result"
        assert capsys.readouterr().out == ("")
