"""unittests for ./editor/qtgui.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from editor import qtgui as testee


class MockGui:
    """testdouble for gui.Gui object
    """


class MockTabbedInterface:
    """testdouble for qtgui.TabbedInterface object
    """
    def on_combobox(self):
        "dummy callback"


class MockSDI:
    """testdouble for qtgui.SingleDataInterface object
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
    """unittests for qtgui.Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.Gui object

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
        testobj.editor = MockEditor()
        testobj.app = mockqtw.MockApplication()
        testobj.sb = mockqtw.MockStatusBar()
        testobj.menu_bar = mockqtw.MockMenuBar()
        assert capsys.readouterr().out == ("called Gui.__init__ with args ()\n"
                                           "called Application.__init__\n"
                                           "called StatusBar.__init__ with args ()\n"
                                           "called MenuBar.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Gui.__init__
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mockqtw.MockMainWindow.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mockqtw.MockMainWindow.statusBar)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'menuBar', mockqtw.MockMainWindow.menuBar)
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mockqtw.MockApplication.__init__)
        monkeypatch.setattr(testee.shared, 'LIN', False)
        master = MockEditor()
        testobj = testee.Gui(master)
        assert testobj.editor == master
        assert isinstance(testobj.app, mockqtw.MockApplication)
        assert isinstance(testobj.sb, mockqtw.MockStatusBar)
        assert isinstance(testobj.menu_bar, mockqtw.MockMenuBar)
        assert testobj.menuitems == {}
        assert capsys.readouterr().out == ("called Application.__init__\n"
                                           "called MainWindow.__init__\n"
                                           "called Application.__init__\n"
                                           "called MainWindow.resize with args (688, 832)\n"
                                           "called MainWindow.statusBar\n"
                                           "called StatusBar.__init__ with args ()\n"
                                           "called MainWindow.menuBar\n"
                                           "called MenuBar.__init__\n")
        monkeypatch.setattr(testee.shared, 'LIN', True)
        testobj = testee.Gui(master)
        assert testobj.editor == master
        assert isinstance(testobj.app, mockqtw.MockApplication)
        assert isinstance(testobj.sb, mockqtw.MockStatusBar)
        assert isinstance(testobj.menu_bar, mockqtw.MockMenuBar)
        assert testobj.menuitems == {}
        assert capsys.readouterr().out == ("called Application.__init__\n"
                                           "called MainWindow.__init__\n"
                                           "called Application.__init__\n"
                                           "called MainWindow.resize with args (1140, 832)\n"
                                           "called MainWindow.statusBar\n"
                                           "called StatusBar.__init__ with args ()\n"
                                           "called MainWindow.menuBar\n"
                                           "called MenuBar.__init__\n")

    def test_start_display(self, monkeypatch, capsys):
        """unittest for Gui.start_display
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.start_display()
        assert isinstance(result, testee.qtw.QVBoxLayout)
        assert isinstance(testobj._frm, testee.qtw.QFrame)
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called VBox.__init__\n")

    def test_add_choicebook_to_display(self, monkeypatch, capsys):
        """unittest for Gui.add_choicebook_to_display
        """
        vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_choicebook_to_display(vbox, 'book')
        assert capsys.readouterr().out == "called VBox.addWidget with arg str\n"

    def test_add_exitbutton_to_display(self, monkeypatch, capsys):
        """unittest for Gui.add_exitbutton_to_display
        """
        def callback():
            "dummy function just for reference"
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_exitbutton_to_display(vbox, ('exit', callback))
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('exit', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called PushButton.setDefault with arg `True`\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_go(self, monkeypatch, capsys):
        """unittest for Gui.go
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                            mockqtw.MockMainWindow.setCentralWidget)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mockqtw.MockMainWindow.show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._frm = mockqtw.MockFrame()
        vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called Frame.__init__\ncalled VBox.__init__\n"
        with pytest.raises(SystemExit):
            testobj.go(vbox)
        assert capsys.readouterr().out == (
                "called Frame.setLayout with arg MockVBoxLayout\n"
                "called MainWidget.setCentralWidget with arg `MockFrame`\n"
                "called MainWindow.show\n"
                "called Application.exec\n")

    def test_set_window_title(self, monkeypatch, capsys):
        """unittest for Gui.set_window_title
        """
        monkeypatch.setattr(testee.Gui, 'setWindowTitle', mockqtw.MockMainWindow.setWindowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_window_title('title')
        assert capsys.readouterr().out == ("called MainWindow.setWindowTitle with arg `title`\n")

    def test_statusbar_message(self, monkeypatch, capsys):
        """unittest for Gui.statusbar_message
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.statusbar_message('message')
        assert capsys.readouterr().out == ("called StatusBar.showMessage with arg `message`\n")

    def test_setup_menu(self, monkeypatch, capsys):
        """unittest for Gui.setup_menu
        """
        def mock_create(*args):
            print(f'called Gui.create_menuaction with args {args}')
            result = mockqtw.MockAction()
            return result
        def mock_get():
            print('called Editor.get_menudata')
            return []
        def mock_get_2():
            print('called Editor.get_menudata')
            return [('menu', [('xxx', (mock_callback, 'XXX')), -1,
                              ('submenu', ([('yyy', (mock_callback, 'YYY'))], ''))
                              ])]
        def mock_callback():
            "stub for function object"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menu_bar = mockqtw.MockMenuBar()
        assert capsys.readouterr().out == "called MenuBar.__init__\n"
        testobj.editor.get_menudata = mock_get
        testobj.editor.captions = {}
        testobj.menuitems = {'M_TOOL': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.create_menuaction = mock_create
        testobj.setup_menu(minimal=True)
        assert capsys.readouterr().out == ("called MenuBar.clear\n"
                                           "called Editor.get_menudata\n"
                                           "called Action.setEnabled with arg `False`\n")
        testobj.editor.captions = {'menu': 'Menutitle', 'xxx': 'Menuitem X', 'submenu': 'Subtitle',
                                   'yyy': 'Menuitem Y'}
        testobj.menuitems = {}
        testobj.editor.get_menudata = mock_get_2
        testobj.setup_menu()
        assert list(testobj.menuitems) == ['menu', 'xxx', 'submenu', 'yyy']
        assert isinstance(testobj.menuitems['menu'], mockqtw.MockMenu)
        assert isinstance(testobj.menuitems['submenu'], mockqtw.MockMenu)
        assert isinstance(testobj.menuitems['xxx'], mockqtw.MockAction)
        assert isinstance(testobj.menuitems['yyy'], mockqtw.MockAction)
        assert capsys.readouterr().out == (
                "called MenuBar.clear\n"
                "called Editor.get_menudata\n"
                "called MenuBar.addMenu with arg  Menutitle\n"
                "called Menu.__init__ with args ('Menutitle',)\n"
                f"called Gui.create_menuaction with args ('xxx', {mock_callback}, 'XXX')\n"
                "called Action.__init__ with args ()\n"
                "called Menu.addAction\n"
                "called Menu.addSeparator\n"
                "called Action.__init__ with args ('-----', None)\n"
                "called Menu.addMenu with args ('Subtitle',)\n"
                "called Menu.__init__ with args ()\n"
                f"called Gui.create_menuaction with args ('yyy', {mock_callback}, 'YYY')\n"
                "called Action.__init__ with args ()\n"
                "called Menu.addAction\n")

    def test_create_menuaction(self, monkeypatch, capsys):
        """unittest for Gui.create_menuaction
        """
        def mock_callback():
            "stub for function object"
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.captions = {'xxx': 'yyyyyy'}
        result = testobj.create_menuaction('xxx', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n")

        testobj.editor.captions = {'M_READ': 'yyyyyy'}
        testobj.editor.book.page.data = {}
        result = testobj.create_menuaction('M_READ', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.data = {'keydef': ['x']}
        result = testobj.create_menuaction('M_READ', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n")

        testobj.editor.captions = {'M_RBLD': 'yyyyyy'}
        testobj.editor.book.page.settings = {}
        result = testobj.create_menuaction('M_RBLD', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.settings = {testee.shared.SettType.RBLD.value: False}
        result = testobj.create_menuaction('M_RBLD', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.settings = {testee.shared.SettType.RBLD.value: True}
        result = testobj.create_menuaction('M_RBLD', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `True`\n")

        testobj.editor.captions = {'M_SAVE': 'yyyyyy'}
        testobj.editor.book.page.settings = {}
        result = testobj.create_menuaction('M_SAVE', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.settings = {testee.shared.SettType.RDEF.value: False}
        result = testobj.create_menuaction('M_SAVE', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.settings = {testee.shared.SettType.RDEF.value: True}
        result = testobj.create_menuaction('M_SAVE', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `True`\n")

    def test_update_menutitles(self, monkeypatch, capsys):
        """unittest for Gui.setcaptions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.captions = {'menu': 'xxxxx', 'menuaction': 'yyyyyy'}
        testobj.menuitems = {'menu': mockqtw.MockMenu(), 'menuaction': mockqtw.MockAction()}
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n")
        testobj.update_menutitles()
        assert capsys.readouterr().out == ("called Menu.setTitle with arg 'xxxxx'\n"
                                           "called Action.setText with arg `yyyyyy`\n")
        testobj.menuitems = {'xxx': 'yyy'}
        with pytest.raises(AttributeError) as exc:
            testobj.update_menutitles()
        assert str(exc.value) == "'str' object has no attribute 'setText'"

    def test_modify_menuitem(self, monkeypatch, capsys):
        """unittest for Gui.modify_menuitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menuitems = {'caption': mockqtw.MockAction()}
        assert capsys.readouterr().out == 'called Action.__init__ with args ()\n'
        testobj.modify_menuitem('caption', 'setting')
        assert capsys.readouterr().out == "called Action.setEnabled with arg `setting`\n"


class TestTabbedInterface:
    """unittests for qtgui.TabbedInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.TabbedInterface object

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
        testobj.parent = MockGui()
        testobj.master = MockChoiceBook()
        assert capsys.readouterr().out == 'called TabbedInterface.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TabbedInterface.__init__
        """
        monkeypatch.setattr(testee.qtw.QFrame, '__init__', mockqtw.MockFrame.__init__)
        testobj = testee.TabbedInterface('parent', 'master')
        assert testobj.parent == 'parent'
        assert testobj.master == 'master'
        assert capsys.readouterr().out == ("called Frame.__init__\n")

    def test_setup_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.setup_selector
        """
        def callback():
            "dummy function, just for reference"
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QStackedWidget', mockqtw.MockStackedWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        sel = testobj.setup_selector(callback)
        assert isinstance(sel, testee.qtw.QComboBox)
        assert isinstance(testobj._pnl, testee.qtw.QStackedWidget)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                f"called Signal.connect with args ({callback},)\n"
                "called StackedWidget.__init__\n")

    def test_add_subscreen(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_subscreen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        win = MockHotkeyPanel()
        win.gui = MockSDI()
        testobj.add_subscreen(win.gui)
        assert capsys.readouterr().out == f"called StackedWidget.addWidget with arg {win.gui}\n"

    def test_add_to_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_to_selector
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        sel = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.add_to_selector(sel, 'text')
        assert capsys.readouterr().out == "called ComboBox.addItem with arg `text`\n"

    def test_start_display(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.start_display
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.start_display()
        assert isinstance(result, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == "called VBox.__init__\n"

    def test_start_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.start_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.start_line(vbox)
        assert isinstance(result, testee.qtw.QHBoxLayout)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_margin_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_margin_to_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj.add_margin_to_line(hbox)
        assert capsys.readouterr().out == "called HBox.addSpacing\n"

    def test_add_text_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_text_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.add_text_to_line(hbox, 'xxx')
        assert isinstance(result, testee.qtw.QLabel)
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx', {testobj})\n"
                "called HBox.addWidget with arg MockLabel\n")

    def test_add_selector_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_selector_to_line
        """
        widget = mockqtw.MockWidget()
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called Widget.__init__\ncalled HBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_selector_to_line(hbox, widget)
        assert capsys.readouterr().out == "called HBox.addWidget with arg MockWidget\n"

    def test_add_combobox_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_combobox_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.add_combobox_to_line(hbox)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.setEditable with arg `False`\n"
                "called HBox.addWidget with arg MockComboBox\n")
        result = testobj.add_combobox_to_line(hbox, 10, True, callback)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                f"called ComboBox.__init__\n"
                "called ComboBox.setMinimumContentsLength with arg 10\n"
                "called ComboBox.setEditable with arg `True`\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockComboBox\n")

    def test_add_separator_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_separator_to_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj.add_separator_to_line(hbox)
        assert capsys.readouterr().out == "called HBox.addStretch\n"

    def test_add_button_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_button_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        result = testobj.add_button_to_line(hbox, 'xxx', callback, 'enabled')
        assert isinstance(result, testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                f"called PushButton.__init__ with args ('xxx', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback},)\n"
                "called PushButton.setEnabled with arg `enabled`\n"
                "called HBox.addWidget with arg MockPushButton\n")

    def test_add_list_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_list_to_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockFrame()
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called Frame.__init__\ncalled HBox.__init__\n"
        testobj.add_list_to_line(hbox)
        assert capsys.readouterr().out == "called HBox.addWidget with arg MockFrame\n"

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.finalize_display
        """
        monkeypatch.setattr(testee.qtw.QFrame, 'setLayout', mockqtw.MockFrame.setLayout)
        vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.finalize_display(vbox)
        assert capsys.readouterr().out == "called Frame.setLayout with arg MockVBoxLayout\n"

    def test_setcaption(self, monkeypatch, capsys):
        """unittest for TabbedInterface.setcaptions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj.setcaption(widget, 'xxx')
        assert capsys.readouterr().out == "called Label.setText with arg `xxx`\n"

    def test_on_pagechange(self, monkeypatch, capsys):
        """unittest for TabbedInterface.on_pagechange
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_pagechange(5)
        assert capsys.readouterr().out == "called ChoiceBook.om_page_changed with args (5,)\n"

    def test_get_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        assert testobj.get_selected_panel() == "current widget"
        assert capsys.readouterr().out == "called StackedWidget.currentWidget\n"

    def test_set_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        testobj.set_selected_panel(2)
        assert capsys.readouterr().out == "called StackedWidget.setCurrentIndex with arg 2\n"

    def test_get_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        assert testobj.get_panel(1) == 'widget'
        assert capsys.readouterr().out == "called StackedWidget.widget with arg 1\n"

    def test_replace_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.replace_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        testobj.replace_panel('indx', 'win', 'newwin')
        assert capsys.readouterr().out == (
                "called StackedWidget.insertWidget with args ('indx', 'newwin')\n"
                "called StackedWidget.setCurrentIndex with arg indx\n"
                "called StackedWidget.removeWidget with arg win\n")

    # def test_set_panel_editable(self, monkeypatch, capsys):
    #     """unittest for TabbedInterface.set_panel_editable
    #     """
    #     def mock_set(arg):
    #         print(f"called Frame.set_extrascreen_editable with arg {arg}")
    #     win = mockqtw.MockFrame()
    #     win.set_extrascreen_editable = mock_set
    #     assert capsys.readouterr().out == "called Frame.__init__\n"
    #     def mock_widget():
    #         print("called StackedWidget.currentWidget")
    #         return win
    #     testobj = self.setup_testobj(monkeypatch, capsys)
    #     testobj._pnl = mockqtw.MockStackedWidget()
    #     testobj._pnl.currentWidget = mock_widget
    #     assert capsys.readouterr().out == "called StackedWidget.__init__\n"
    #     testobj.set_panel_editable(True)
    #     assert capsys.readouterr().out == ("called StackedWidget.currentWidget\n"
    #                                        "called Frame.set_extrascreen_editable with arg True\n")
    #     testobj.set_panel_editable(False)
    #     assert capsys.readouterr().out == ("called StackedWidget.currentWidget\n"
    #                                        "called Frame.set_extrascreen_editable with arg False\n")

    def test_enable_widget(self, monkeypatch, capsys):
        """unittest for TabbedInterface.enable_widget
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj.enable_widget(widget, 'state')
        assert capsys.readouterr().out == "called Widget.setEnabled with arg state\n"

    def _test_update_search(self, monkeypatch, capsys):
        """unittest for TabbedInterface.update_search
        """
        def mock_init():
            print('called TabbedInterface.init_search_buttons')
        def mock_enable(**kwargs):
            print('called TabbedInterface.enable_search_buttons with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_loc = mockqtw.MockComboBox()
        testobj.find = mockqtw.MockComboBox()
        testobj.b_filter = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.master.page.filtertext = ''
        testobj.parent.captions = {'C_FLTOFF': 'xxx'}
        testobj.init_search_buttons = mock_init
        testobj.enable_search_buttons = mock_enable
        testobj.update_search(['items'])
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.addItems with arg ['items']\n"
                                           "called ComboBox.setCurrentText with arg `items`\n"
                                           "called ComboBox.setEditText with arg ``\n"
                                           "called ComboBox.setEnabled with arg True\n"
                                           "called TabbedInterface.init_search_buttons\n")
        testobj.master.page.filtertext = 'qqq'
        testobj.update_search(['items', 'last'])
        assert capsys.readouterr().out == (
                "called ComboBox.clear\n"
                "called ComboBox.addItems with arg ['items', 'last']\n"
                "called ComboBox.setCurrentText with arg `last`\n"
                "called ComboBox.setEditText with arg `qqq`\n"
                "called PushButton.setText with arg `xxx`\n"
                "called TabbedInterface.enable_search_buttons with args {'filter': True}\n")

    def test_refresh_combobox(self, monkeypatch, capsys):
        """unittest for TabbedInterface.refresh_combobox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.refresh_combobox(cmb)
        assert capsys.readouterr().out == "called ComboBox.clear\n"
        testobj.refresh_combobox(cmb, ['x', 'y'])
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.addItems with arg ['x', 'y']\n"
                                           "called ComboBox.setCurrentText with arg `y`\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_value(cmb) == "current text"
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_set_combobox_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_combobox_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.set_combobox_text(cmb, '')
        assert capsys.readouterr().out == "called ComboBox.setEditText with arg ``\n"
        testobj.set_combobox_text(cmb, 'xxx')
        assert capsys.readouterr().out == ("called ComboBox.setEditText with arg `xxx`\n"
                                           "called ComboBox.setEnabled with arg True\n")

    def test_get_combobox_index(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_combobox_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.get_combobox_index(cmb)
        assert capsys.readouterr().out == "called ComboBox.currentIndex\n"

    def test_get_search_col(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_search_col
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_search_col(cmb) == "current text"
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_get_combobox_index_for_item(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_combobox_index_for_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_index_for_item(cb, 'item') == 1
        assert capsys.readouterr().out == "called ComboBox.findText with args ('item',)\n"

    def test_set_combobox_index(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_combobox_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.set_combobox_index(cmb, 'selection')
        assert capsys.readouterr().out == "called ComboBox.setCurrentIndex with arg `selection`\n"

    def test_on_textchange(self, monkeypatch, capsys):
        """unittest for TabbedInterface.on_textchange
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_textchange('xxx')
        assert capsys.readouterr().out == "called ChoiceBook.om_text_changed with args ('xxx',)\n"

    def test_get_button_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockqtw.MockPushButton('xxx')
        assert capsys.readouterr().out == "called PushButton.__init__ with args ('xxx',) {}\n"
        assert testobj.get_button_text(button) == "xxx"
        assert capsys.readouterr().out == "called PushButton.text\n"

    def test_set_button_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_button_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.set_button_text(button, "state")
        assert capsys.readouterr().out == "called PushButton.setText with arg `state`\n"

    def test_find_items(self, monkeypatch, capsys):
        """unittest for TabbedInterface.find_items
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.master.zoekcol = 'xxx'
        p0list = mockqtw.MockTreeWidget()
        assert testobj.find_items(p0list, 'xxx', 'text') == []
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called Tree.findItems with args ('text',"
                                           f" {testee.core.Qt.MatchFlag.MatchContains!r}, 'xxx')\n")

    def test_set_selected_keydef_item(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_keydef_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.set_selected_keydef_item(p0list, ['xxx', 'yyy', 'zzz'], 2)
        assert capsys.readouterr().out == ("called Tree.setCurrentItem with arg `zzz`\n"
                                           "called Tree.scrollToItem with arg `zzz`\n")

    def test_get_found_keydef_position(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_found_keydef_position
        """
        item = mockqtw.MockTreeItem('xxx', 'yyy')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx', 'yyy')\n"
        def mock_current():
            print('called Tree.currentItem')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.master.page = MockHotkeyPanel()
        p0list = mockqtw.MockTreeWidget()
        p0list.currentItem = mock_current
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_found_keydef_position(p0list) == ('xxx', 'yyy')
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           "called TreeItem.text with arg 0\n"
                                           "called TreeItem.text with arg 1\n")

    def test_set_found_keydef_position(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_found_keydef_position
        """
        item = mockqtw.MockTreeItem('xxx', 'yyy')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx', 'yyy')\n"
        def mock_count():
            print('called Tree.topLevelItemCount')
            return 2
        item2 = mockqtw.MockTreeItem('aaa', 'bbb')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('aaa', 'bbb')\n"
        def mock_item(num):
            print(f'called Tree.topLevelItem with arg {num}')
            if num == 1:
                return item
            return item2
        def mock_current():
            print('called Tree.currentItem')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.set_found_keydef_position(p0list, ('x', 'y'))
        assert capsys.readouterr().out == "called Tree.topLevelItemCount\n"
        p0list.topLevelItemCount = mock_count
        p0list.topLevelItem = mock_item
        p0list.currentItem = mock_current
        testobj.set_found_keydef_position(p0list, ('xxx', 'yyy'))
        assert capsys.readouterr().out == ("called Tree.topLevelItemCount\n"
                                           "called Tree.topLevelItem with arg 0\n"
                                           "called TreeItem.text with arg 0\n"
                                           "called TreeItem.text with arg 1\n"
                                           "called Tree.topLevelItem with arg 1\n"
                                           "called TreeItem.text with arg 0\n"
                                           "called TreeItem.text with arg 1\n"
                                           f"called Tree.setCurrentItem with arg `{item}`\n")

    def test_remove_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.remove_tool
        """
        win = mockqtw.MockFrame()
        win.master = 'master'
        assert capsys.readouterr().out == "called Frame.__init__\n"
        def mock_widget(num):
            print(f"called StackedWidget.widget with arg {num}")
            return win
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockStackedWidget()
        testobj._pnl.widget = mock_widget
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        assert testobj.remove_tool(1, 'program', []) is None
        assert capsys.readouterr().out == ("called StackedWidget.widget with arg 1\n"
                                           f"called StackedWidget.removeWidget with arg {win}\n"
                                           "called Frame.close\n")
        assert testobj.remove_tool(1, 'program', ['program', 'list']) == "master"
        assert capsys.readouterr().out == ("called StackedWidget.widget with arg 1\n"
                                           f"called StackedWidget.removeWidget with arg {win}\n")


class TestSingleDataInterface:
    """unittests for qtgui.SingleDataInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SingleDataInterface object

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
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args ()\n'
                                           "called Tree.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.__init__
        """
        monkeypatch.setattr(testee.qtw.QFrame, '__init__', mockqtw.MockFrame.__init__)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.SingleDataInterface('parent', 'master')
        assert testobj.parent == 'parent'
        assert testobj.master == 'master'
        assert testobj._savestates == (False, False)
        assert isinstance(testobj._sizer, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called VBox.__init__\n")

    def test_setup_empty_screen(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.setup_empty_screen
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.SingleDataInterface, 'setLayout', mockqtw.MockFrame.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.setup_empty_screen('nodata', 'title')
        assert testobj.title == 'title'
        assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called VBox.addLayout with arg MockHBoxLayout\n"
            "called HBox.addStretch\n"
            f"called Label.__init__ with args ('nodata', {testobj})\n"
            "called HBox.addWidget with arg MockLabel\n"
            "called HBox.addStretch\n")

    def test_setup_list(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.setup_list
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.setup_list([], [], callback)
        assert isinstance(result, testee.qtw.QTreeWidget)
        assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called Tree.__init__\n"
            "called HBox.addWidget with arg MockTreeWidget\n"
            "called VBox.addLayout with arg MockHBoxLayout\n"
            "called Tree.setHeaderLabels with arg `[]`\n"
            "called Tree.setAlternatingRowColors with arg True\n"
            f"called Signal.connect with args ({callback},)\n"
            "called Tree.header\n"
            "called Header.__init__\n"
            "called Header.setSectionsClickable with value True\n"
            "called Header.setStretchLastSection with arg True\n"
            "called Tree.setSortingEnabled with arg True\n")
        result = testobj.setup_list(['x', 'y'], [1, 2], callback)
        assert isinstance(result, testee.qtw.QTreeWidget)
        assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called Tree.__init__\n"
            "called HBox.addWidget with arg MockTreeWidget\n"
            "called VBox.addLayout with arg MockHBoxLayout\n"
            "called Tree.setHeaderLabels with arg `['x', 'y']`\n"
            "called Tree.setAlternatingRowColors with arg True\n"
            f"called Signal.connect with args ({callback},)\n"
            "called Tree.header\n"
            "called Header.__init__\n"
            "called Header.setSectionsClickable with value True\n"
            "called Header.resizeSection with args (0, 1)\n"
            "called Header.resizeSection with args (1, 2)\n"
            "called Header.setStretchLastSection with arg True\n"
            "called Tree.setSortingEnabled with arg True\n")

    def test_start_extrapanel(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.start_extrapanel
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.start_extrapanel(90)
        assert isinstance(result, testee.qtw.QVBoxLayout)
        assert isinstance(testobj._frm, testee.qtw.QFrame)
        assert capsys.readouterr().out == (
                "called Frame.__init__\n"
                "called Frame.setFixedHeight with arg `90`\n"
                "called VBox.addWidget with arg MockFrame\n"
                "called VBox.__init__\n"
                "called Frame.setLayout with arg MockVBoxLayout\n")

    def test_start_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.start_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.start_line(vbox)
        assert isinstance(result, testee.qtw.QHBoxLayout)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_label_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_label_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._frm = mockqtw.MockFrame()
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called Frame.__init__\ncalled HBox.__init__\n"
        result = testobj.add_label_to_line(hbox, 'xxx')
        assert isinstance(result, testee.qtw.QLabel)
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx', {testobj._frm})\n"
                "called HBox.addWidget with arg MockLabel\n")

    def test_add_textfield_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_textfield_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._frm = mockqtw.MockFrame()
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called Frame.__init__\ncalled HBox.__init__\n"
        result = testobj.add_textfield_to_line(hbox)
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                "called LineEdit.__init__\n"
                "called HBox.addWidget with arg MockLineEdit\n")
        result = testobj.add_textfield_to_line(hbox, 8, callback)
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                f"called LineEdit.__init__\n"
                "called LineEdit.setMaximumWidth with arg `8`\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockLineEdit\n")

    def test_add_combobox_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_combobox_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentTextChanged', {str: mockqtw.MockSignal()})
        assert capsys.readouterr().out == "called Signal.__init__\n"
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.on_combobox = callback
        testobj._frm = mockqtw.MockFrame()
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called Frame.__init__\ncalled HBox.__init__\n"
        result = testobj.add_combobox_to_line(hbox, 'xxx')
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                f"called ComboBox.__init__\n"
                "called ComboBox.addItems with arg xxx\n"
                "called Signal.connect with args"
                f" (functools.partial({callback}, {result}, <class 'str'>),)\n"
                "called HBox.addWidget with arg MockComboBox\n")
        result = testobj.add_combobox_to_line(hbox, 'xxx', 10)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                f"called ComboBox.__init__\n"
                "called ComboBox.setMaximumWidth with arg `10`\n"
                "called ComboBox.addItems with arg xxx\n"
                "called Signal.connect with args"
                f" (functools.partial({callback}, {result}, <class 'str'>),)\n"
                "called HBox.addWidget with arg MockComboBox\n")

    def test_add_checkbox_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_checkbox_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.on_checkbox = callback
        testobj._frm = mockqtw.MockFrame()
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called Frame.__init__\ncalled HBox.__init__\n"
        result = testobj.add_checkbox_to_line(hbox, 'xxx')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('xxx', {testobj._frm})\n"
                "called Signal.connect with args"
                f" (functools.partial({callback}, {result}),)\n"
                "called HBox.addWidget with arg MockCheckBox\n")

    def test_add_separator_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_separator_to_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        testobj.add_separator_to_line(hbox)
        assert capsys.readouterr().out == "called HBox.addStretch\n"

    def test_add_button_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_button_to_line
        """
        def callback():
            "dummy function"
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._frm = mockqtw.MockFrame()
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called Frame.__init__\ncalled HBox.__init__\n"
        result = testobj.add_button_to_line(hbox, 'xxx', callback)
        assert isinstance(result, testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                f"called PushButton.__init__ with args ('xxx', {testobj._frm}) {{}}\n"
                "called PushButton.setEnabled with arg `False`\n"
                f"called Signal.connect with args ({callback},)\n"
                "called HBox.addWidget with arg MockPushButton\n")

    def test_add_descfield_to_line(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_descfield_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._frm = mockqtw.MockFrame()
        hbox = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called Frame.__init__\ncalled HBox.__init__\n"
        result = testobj.add_descfield_to_line(hbox)
        assert isinstance(result, testee.qtw.QTextEdit)
        assert capsys.readouterr().out == (
                f"called Editor.__init__ with args ({testobj._frm},)\n"
                "called Editor.setReadOnly with arg `True`\n"
                "called HBox.addWidget with arg MockEditorWidget\n")

    def test_set_extrapanel_editable(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_extrapanel_editable
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        screenfields = [mockqtw.MockLineEdit(), mockqtw.MockCheckBox()]
        button1 = mockqtw.MockPushButton()
        button2 = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj._savestates = (False, False)
        testobj.set_extrapanel_editable(screenfields, [button1, button2], True)
        assert capsys.readouterr().out == ("called LineEdit.setEnabled with arg True\n"
                                           "called CheckBox.setEnabled with arg True\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n")
        button1.setEnabled(True)
        button2.setEnabled(True)
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        testobj._savestates = ()
        testobj.set_extrapanel_editable(screenfields, [button1, button2], False)
        assert testobj._savestates == (True, True)
        assert capsys.readouterr().out == ("called LineEdit.setEnabled with arg False\n"
                                           "called CheckBox.setEnabled with arg False\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n")

    def test_finalize_screen(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.finalize_screen
        """
        monkeypatch.setattr(testee.qtw.QFrame, 'setLayout', mockqtw.MockFrame.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._sizer = 'sizer'
        testobj.finalize_screen()
        assert capsys.readouterr().out == "called Frame.setLayout with arg str\n"

    def _test_resize_if_necessary(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.resize_if_necessary
        """
        # not implemented
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.resize_if_necessary()
        assert capsys.readouterr().out == ""

    def test_on_item_selected(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_item_selected
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.has_extrapanel = True
        testobj.on_item_selected('', 'olditem')
        assert capsys.readouterr().out == ""
        testobj.master.has_extrapanel = False
        testobj.on_item_selected('newitem', 'olditem')
        assert capsys.readouterr().out == ""
        testobj.master.has_extrapanel = True
        testobj.on_item_selected('newitem', 'olditem')
        assert capsys.readouterr().out == (
                "called HotkeyPanel.process_changed_selection with args ('newitem', 'olditem')\n")

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_update
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Widget.setFocus\n"

    def test_update_columns(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.update_columns
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.update_columns(p0list, 'oldcount', 'newcount')
        assert capsys.readouterr().out == "called Tree.setColumnCount with arg `newcount`\n"

    def test_refresh_headers(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.refresh_headers
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.refresh_headers(p0list, (('xxx', 10), ('yyy', 20)))
        assert capsys.readouterr().out == ("called Tree.setColumnCount with arg `2`\n"
                                           "called Tree.setHeaderLabels with arg `['xxx', 'yyy']`\n"
                                           "called Tree.header\ncalled Header.__init__\n"
                                           "called Header.setSectionsClickable with value True\n"
                                           "called Header.resizeSection with args (0, 10)\n"
                                           "called Header.resizeSection with args (1, 20)\n"
                                           "called Header.setStretchLastSection with arg True\n")

    def test_set_title(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.parent = MockChoiceBook()
        testobj.master.parent.parent = MockEditor()
        testobj.master.parent.parent.gui = mockqtw.MockMainWindow()
        assert capsys.readouterr().out == ("called MainWindow.__init__\n"
                                           "called Application.__init__\n")
        testobj.set_title('title')
        assert capsys.readouterr().out == "called MainWindow.setWindowTitle with arg `title`\n"

    def test_clear_list(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.clear_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.clear_list(p0list)
        assert capsys.readouterr().out == "called Tree.clear\n"

    def test_build_listitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.build_listitem
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.build_listitem('key')
        assert isinstance(result, testee.qtw.QTreeWidgetItem)
        assert result.data(0, testee.core.Qt.ItemDataRole.UserRole) == 'key'
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setData with args"
                f" (0, {testee.core.Qt.ItemDataRole.UserRole!r}, 'key')\n"
                f"called TreeItem.data with args (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n")

    def test_set_listitemtext(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_listitemtext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_listitemtext(item, 1, 'value')
        assert capsys.readouterr().out == ("called TreeItem.setText with args (1, 'value')\n"
                                           "called TreeItem.setTooltip with args (1, 'value')\n")

    def test_add_listitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_listitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.add_listitem(p0list, 'new_item')
        assert capsys.readouterr().out == "called Tree.addTopLevelItem\n"

    def test_set_listselection(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_listselection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        treeitem = mockqtw.MockTreeItem()
        p0list.addTopLevelItem(treeitem)
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called Tree.addTopLevelItem\n")
        testobj.set_listselection(p0list, 0)
        assert capsys.readouterr().out == (
                "called Tree.topLevelItem with arg `0`\n"
                "called Tree.setCurrentItem with arg `Tree.topLevelItem`\n")

    def test_getfirstitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.getfirstitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        treeitem = mockqtw.MockTreeItem()
        p0list.addTopLevelItem(treeitem)
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called Tree.addTopLevelItem\n")
        assert testobj.getfirstitem(p0list) == 'Tree.topLevelItem'
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `0`\n")

    def test_get_listitem_at_position(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_keydef_at_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        result = testobj.get_listitem_at_position(p0list, 1)
        assert result == 'Tree.topLevelItem'
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `1`\n")

    def test_get_itemdata(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_itemdata
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        item.setData(0, testee.core.Qt.ItemDataRole.UserRole, 'data')
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setData with args"
                f" (0, {testee.core.Qt.ItemDataRole.UserRole!r}, 'data')\n")
        assert testobj.get_itemdata(item) == "data"
        assert capsys.readouterr().out == (
                f"called TreeItem.data with args (0, {testee.core.Qt.ItemDataRole.UserRole!r})\n")

    def test_get_listbox_selection(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_selected_keydef
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        result = testobj.get_listbox_selection(p0list)
        assert result == ('called Tree.currentItem', 'index')
        assert capsys.readouterr().out == (
                "called Tree.indexOfTopLevelItem with arg `called Tree.currentItem`\n")

    def test_get_listitem_position(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_keydef_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_listitem_position(p0list, 'item') == 'index'
        assert capsys.readouterr().out == ("called Tree.indexOfTopLevelItem with arg `item`\n")

    def test_get_widget_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_widget_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        ted = mockqtw.MockLineEdit()
        ted.setText('xxx')
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.setText with arg `xxx`\n")
        assert testobj.get_widget_text(ted, 'text') == "xxx"
        assert capsys.readouterr().out == ("called LineEdit.text\n")
        assert testobj.get_widget_text(ted, 'xxx') == "xxx"
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_set_textfield_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_textfield_value

        wordt gebruikt voor zowel QLineEdit, QComboBox en QTextEdit
        dit is ducktyping, elk apart testen niet nodig
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        txt = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_textfield_value(txt, 'value')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `value`\n")

    def test_enable_button(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.enable_button
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        button = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.enable_button(button, True)
        assert button.isEnabled()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n")
        testobj.enable_button(button, False)
        assert not button.isEnabled()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `False`\n")

    def test_get_choice_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_choice_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_choice_value(cb, 'dummy', 'text') == (cb, 'text')

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.get_combobox_value(cb)
        assert capsys.readouterr().out == ("called ComboBox.currentText\n")

    def test_init_combobox(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.init_combobox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.init_combobox(cb)
        assert capsys.readouterr().out == ("called ComboBox.clear\n")
        testobj.init_combobox(cb, choices=[])
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.addItems with arg []\n")
        testobj.init_combobox(cb, choices=['xxx', 'yyy'])
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.addItems with arg ['xxx', 'yyy']\n")

    def test_set_combobox_string(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_combobox_string
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.set_combobox_string(cb, 'value', [])
        assert capsys.readouterr().out == ""
        testobj.set_combobox_string(cb, 'value', ['value', 'list'])
        assert capsys.readouterr().out == "called ComboBox.setCurrentIndex with arg `0`\n"

    def test_set_label_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_label_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        lbl = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj.set_label_text(lbl, 'value')
        assert capsys.readouterr().out == "called Label.setText with arg `value`\n"

    def test_get_check_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_check_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert testobj.get_check_value(cb, True) == (cb, True)
        assert capsys.readouterr().out == ""
        assert testobj.get_check_value(cb, False) == (cb, False)
        assert capsys.readouterr().out == ""

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_checkbox_state
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert not testobj.get_checkbox_state(cb)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")
        cb.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        assert testobj.get_checkbox_state(cb)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")

    def test_set_checkbox_state(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_checkbox_state
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj.set_checkbox_state(cb, False)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg False\n"
        testobj.set_checkbox_state(cb, True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"


def mock_get_text(*args):
    "stub"
    print('called shared.get_text with args', args)
    return 'text'


def mock_get_title(*args):
    "stub"
    print('called shared.get_title with args', args)
    return 'title'


def mock_info(*args):
    "stub"
    print('called MessageBox.information with args', args)
    return testee.qtw.QMessageBox.StandardButton.Cancel


def mock_info_2(*args):
    "stub"
    print('called MessageBox.information with args', args)
    return testee.qtw.QMessageBox.StandardButton.Ok


def mock_question(*args):
    "stub"
    print('called MessageBox.question with args', args)
    return testee.qtw.QMessageBox.StandardButton.No


def mock_question_2(*args):
    "stub"
    print('called MessageBox.question with args', args)
    return testee.qtw.QMessageBox.StandardButton.Yes


def mock_question_3(*args):
    "stub"
    print('called MessageBox.question with args', args)
    return testee.qtw.QMessageBox.StandardButton.Cancel


def test_show_message(monkeypatch, capsys):
    """unittest for qtgui.show_message
    """
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info)
    testee.show_message('win', message_id='xxx', text='yyy')
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', None)\n"
            "called shared.get_title with args ('win',)\n"
            "called MessageBox.information with args ('win', 'title', 'text')\n")
    testee.show_message('win', message_id='xxx', text='yyy', args={'aa': 'bbbb'})
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            "called MessageBox.information with args ('win', 'title', 'text')\n")


def test_show_cancel_message(monkeypatch, capsys):
    """unittest for qtgui.show_cancel_message
    """
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info)
    assert not testee.show_cancel_message('win', message_id='xxx', text='yyy')
    buttons = testee.qtw.QMessageBox.StandardButton.Ok | testee.qtw.QMessageBox.StandardButton.Cancel
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', None)\n"
            "called shared.get_title with args ('win',)\n"
            f"called MessageBox.information with args ('win', 'title', 'text', {buttons!r})\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info_2)
    assert testee.show_cancel_message('win', message_id='xxx', text='yyy', args={'aa': 'bbbb'})
    buttons = testee.qtw.QMessageBox.StandardButton.Ok | testee.qtw.QMessageBox.StandardButton.Cancel
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            f"called MessageBox.information with args ('win', 'title', 'text', {buttons!r})\n")


def test_ask_question(monkeypatch, capsys):
    """unittest for qtgui.ask_question
    """
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question)
    assert not testee.ask_question('win', message_id='xxx', text='yyy')
    buttons = testee.qtw.QMessageBox.StandardButton.Yes | testee.qtw.QMessageBox.StandardButton.No
    yesbutton = testee.qtw.QMessageBox.StandardButton.Yes
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', None)\n"
            "called shared.get_title with args ('win',)\n"
            f"called MessageBox.question with args ('win', 'title', 'text', {buttons!r},"
            f" {yesbutton!r})\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question_2)
    assert testee.ask_question('win', message_id='xxx', text='yyy', args={'aa': 'bbbb'})
    buttons = testee.qtw.QMessageBox.StandardButton.Yes | testee.qtw.QMessageBox.StandardButton.No
    yesbutton = testee.qtw.QMessageBox.StandardButton.Yes
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            f"called MessageBox.question with args ('win', 'title', 'text', {buttons!r},"
            f" {yesbutton!r})\n")


def test_ask_ync_question(monkeypatch, capsys):
    """unittest for qtgui.ask_ync_question
    """
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question)
    assert testee.ask_ync_question('win', message_id='xxx', text='yyy') == (False, False)
    # buttons = testee.qtw.QMessageBox.StandardButton.Yes | testee.qtw.QMessageBox.StandardButton.No | testee.qtw.QMessageBox.StandardButton.Cancel
    # # hier komt `buttons` ineens niet meer overeen met de buttons in de testee methode
    # daarom stdout vergelijking maar laten zitten
    # assert capsys.readouterr().out == (
    #         "called shared.get_text with args ('win', 'xxx', 'yyy', None)\n"
    #         "called shared.get_title with args ('win',)\n"
    #         f"called MessageBox.question with args ('win', 'title', 'text', {buttons}")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question_2)
    assert testee.ask_ync_question('win', message_id='xxx', text='yyy', args={}) == (True, False)
    # buttons = testee.qtw.QMessageBox.StandardButton.Yes | testee.qtw.QMessageBox.StandardButton.No | testee.qtw.QMessageBox.StandardButton.Cancel
    # assert capsys.readouterr().out == (
    #         "called shared.get_text with args ('win', 'xxx', 'yyy', {})\n"
    #         "called shared.get_title with args ('win',)\n"
    #         f"called MessageBox.question with args ('win', 'title', 'text', {buttons}")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question_3)
    assert testee.ask_ync_question('win', message_id='xxx', text='yyy',
                                   args={'aa': 'bbbb'}) == (False, True)


def test_get_textinput(monkeypatch, capsys):
    """unittest for qtgui.get_textinput
    """
    def mock_get(*args, **kwargs):
        print('called Inputdialog.getText with args', args, kwargs)
        return '', testee.qtw.QDialog.DialogCode.Rejected
    def mock_get_2(*args, **kwargs):
        print('called Inputdialog.getText with args', args, kwargs)
        return 'xxx', testee.qtw.QDialog.DialogCode.Accepted
    monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get)
    assert testee.get_textinput('win', 'text', 'prompt') == ('', False)
    assert capsys.readouterr().out == ("called Inputdialog.getText with args"
                                       " ('win', 'Application Title', 'prompt') {'text': 'text'}\n")
    monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get_2)
    assert testee.get_textinput('win', 'text', 'prompt') == ('xxx', True)
    assert capsys.readouterr().out == ("called Inputdialog.getText with args"
                                       " ('win', 'Application Title', 'prompt') {'text': 'text'}\n")


def test_get_choice(monkeypatch, capsys):
    """unittest for qtgui.get_choice
    """
    def mock_get(*args, **kwargs):
        print('called Inputdialog.getItem with args', args, kwargs)
        return ''
    def mock_get_2(*args, **kwargs):
        print('called Inputdialog.getItem with args', args, kwargs)
        return 'xxx'
    monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get)
    assert testee.get_choice('win', 'title', 'caption', ['choices'], 'current') == ""
    assert capsys.readouterr().out == (
            "called Inputdialog.getItem with args"
            " ('win', 'title', 'caption', ['choices'], 'current') {'editable': False}\n")
    monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get_2)
    assert testee.get_choice('win', 'title', 'caption', ['choices'], 'current') == "xxx"
    assert capsys.readouterr().out == (
            "called Inputdialog.getItem with args"
            " ('win', 'title', 'caption', ['choices'], 'current') {'editable': False}\n")


def test_get_file_to_open(monkeypatch, capsys):
    """unittest for qtgui.get_file_to_open
    """
    def mock_get(*args):
        print('called shared.get_open_title with args', args)
    def mock_get_file(*args, **kwargs):
        print('called FileDialog.getOpenFileName with args', args, kwargs)
        return '', False
    def mock_get_file_2(*args, **kwargs):
        print('called FileDialog.getOpenFileName with args', args, kwargs)
        return 'xxx', True
    monkeypatch.setattr(testee.shared, 'get_open_title', mock_get)
    monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get_file)
    assert testee.get_file_to_open('win') == ""
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', '')\n"
            "called FileDialog.getOpenFileName with args"
            " ('win', None) {'directory': '', 'filter': ''}\n")
    monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get_file_2)
    assert testee.get_file_to_open('win', 'oms', 'extension', 'start') == "xxx"
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', 'oms')\n"
            "called FileDialog.getOpenFileName with args"
            " ('win', None) {'directory': 'start', 'filter': 'extension'}\n")


def test_get_file_to_save(monkeypatch, capsys):
    """unittest for qtgui.get_file_to_save
    """
    def mock_get(*args):
        print('called shared.get_open_title with args', args)
    def mock_get_file(*args, **kwargs):
        print('called FileDialog.getSaveFileName with args', args, kwargs)
        return '', False
    def mock_get_file_2(*args, **kwargs):
        print('called FileDialog.getSaveFileName with args', args, kwargs)
        return 'xxx', True
    monkeypatch.setattr(testee.shared, 'get_open_title', mock_get)
    monkeypatch.setattr(testee.qtw.QFileDialog, 'getSaveFileName', mock_get_file)
    assert testee.get_file_to_save('win') == ""
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', '')\n"
            "called FileDialog.getSaveFileName with args"
            " ('win', None) {'filter': ''}\n")
    monkeypatch.setattr(testee.qtw.QFileDialog, 'getSaveFileName', mock_get_file_2)
    assert testee.get_file_to_save('win', 'oms', 'extension', 'start') == "xxx"
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', 'oms')\n"
            "called FileDialog.getSaveFileName with args"
            " ('win', None) {'filter': 'extension'}\n")


def test_show_dialog(monkeypatch, capsys):
    """unittest for qtgui.show_dialog
    """
    def mock_exec(self):
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Rejected
    def mock_exec_2(self):
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Accepted
    dlg = mockqtw.MockDialog()
    assert capsys.readouterr().out == "called Dialog.__init__ with args None () {}\n"
    monkeypatch.setattr(mockqtw.MockDialog, 'exec', mock_exec)
    assert not testee.show_dialog(dlg)
    assert capsys.readouterr().out == "called Dialog.exec\n"
    monkeypatch.setattr(mockqtw.MockDialog, 'exec', mock_exec_2)
    assert testee.show_dialog(dlg)
    assert capsys.readouterr().out == "called Dialog.exec\n"


class TestInitialToolDialogiGui:
    """unittest for qtgui.InitialToolDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.InitialToolDialogGui object

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
        assert capsys.readouterr().out == "called InitialToolDialogGui.__init__ with args ()\n"
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.__init__
        """
        # monkeypatch.setattr(testee.qtw, 'QDialog', mockqtw.MockDialog)
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        # monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        # monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.InitialToolDialogGui('parent', 'master', 'title')
        assert isinstance(testobj.vbox, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ("called Dialog.__init__ with args master () {}\n"
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called VBox.__init__\n"
                                           "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_text(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.add_text
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_text('text')
        assert capsys.readouterr().out == (f"called Label.__init__ with args ('text', {testobj})\n"
                                           "called VBox.addWidget with arg MockLabel\n")

    def test_add_radiobutton_line(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.add_radiobutton_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_radiobutton_line('xxx', True)
        assert isinstance(result[0], testee.qtw.QRadioButton)
        assert result[1] == ''
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called RadioButton.__init__ with args ('xxx', {testobj}) {{}}\n"
                "called RadioButton.setChecked with arg `True`\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        result = testobj.add_radiobutton_line('xxx', True, ['a', 'b'], 1)
        assert isinstance(result[0], testee.qtw.QRadioButton)
        assert isinstance(result[1], testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called RadioButton.__init__ with args ('xxx', {testobj}) {{}}\n"
                "called RadioButton.setChecked with arg `True`\n"
                "called HBox.addWidget with arg MockRadioButton\n"
                "called ComboBox.__init__\ncalled ComboBox.addItems with arg ['a', 'b']\n"
                "called ComboBox.setCurrentIndex with arg `1`\n"
                "called ComboBox.setEditable with arg `True`\n"
                "called HBox.addWidget with arg MockComboBox\ncalled HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.add_okcancel_buttons
        """
        def callback1():
            "dummy method for reference"
        def callback2():
            "dummy method for reference"
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.accept = callback1
        testobj.reject = callback2
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == ("called ButtonBox.__init__ with args ()\n"
                                           "called ButtonBox.addButton with args (1,)\n"
                                           "called ButtonBox.addButton with args (2,)\n"
                                           f"called Signal.connect with args ({testobj.accept},)\n"
                                           f"called Signal.connect with args ({testobj.reject},)\n"
                                           "called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_radiobutton_value(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.get_radiobutton_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        rb = mockqtw.MockRadioButton()
        assert capsys.readouterr().out == "called RadioButton.__init__ with args () {}\n"
        assert not testobj.get_radiobutton_value(rb)
        assert capsys.readouterr().out == ("called RadioButton.isChecked\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.get_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_value(cmb) == 'current text'
        assert capsys.readouterr().out == ("called ComboBox.currentText\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for InitialToolDialogGui.accept
        """
        def mock_confirm():
            print('called InitialToolDialog.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called InitialToolDialog.confirm\n"
                                           "called Dialog.accept\n")


class TestFilesDialogGui:
    """unittest for qtgui.FilesDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.FilesDialogGui object

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
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        # monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        # monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        # monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        # monkeypatch.setattr(testee.FilesDialog, 'add_row', mock_add)
        testobj = testee.FilesDialogGui('master', 'parent', 'title')
        assert testobj.code_to_remove == []
        assert testobj.data_to_remove == []
        # assert isinstance(testobj.scrl, testee.qtw.QScrollArea)
        # assert testobj.bar == 'vertical scrollbar'
        # assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        # assert isinstance(testobj.gsizer, testee.qtw.QGridLayout)
        # assert testobj.rownum == 0
        # assert testobj.plugindata == []
        # assert testobj.checks == []
        # assert testobj.paths == []
        # assert testobj.progs == []
        # assert testobj.settingsdata == {'name': ('data', )}
        # hier zit weer zo'n OR die blijkbaar een integer verandert in een object (Alignment)
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ("called Dialog.__init__ with args parent () {}\n"
                                           "called Dialog.resize with args (680, 400)\n"
                                           "called Dialog.setWindowTitle with args ('title',)\n"
                                           "called VBox.__init__\n"
                                           "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_explanation(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_explanation
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_explanation('text')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Label.__init__ with args ('text', {testobj})\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_captions(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_captions
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_captions([])
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_captions([('xx', 10), ('yy', 20)])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addSpacing\n"
                f"called Label.__init__ with args ('xx', {testobj})\n"
                "called HBox.addWidget with args"
                " MockLabel {'alignment': <AlignmentFlag.AlignCenter: 132>}\n"
                "called HBox.addSpacing\n"
                f"called Label.__init__ with args ('yy', {testobj})\n"
                "called HBox.addWidget with args"
                " MockLabel {'alignment': <AlignmentFlag.AlignCenter: 132>}\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_locationbrowserarea(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_locationbrowserarea
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.add_locationbrowserarea(), testee.qtw.QScrollArea)
        assert testobj.bar == 'vertical scrollbar'
        assert isinstance(testobj.gsizer, testee.qtw.QGridLayout)
        assert testobj.rownum == 0
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           f"called ScrollArea.__init__ with args ({testobj},)\n"
                                           "called ScrollArea.setWidget with arg `MockFrame`\n"
                                           "called ScrollArea.setWidgetResizable with arg `True`\n"
                                           "called ScrollArea.verticalScrollBar\n"
                                           "called Grid.__init__\n"
                                           "called VBox.__init__\n"
                                           "called VBox.addLayout with arg MockGridLayout\n"
                                           "called VBox.addStretch\n"
                                           "called Frame.setLayout with arg MockVBoxLayout\n"
                                           "called VBox.addWidget with arg MockScrollArea\n")

    def _test_finish_browserarea(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.finish_browserarea
        """
        # not implemented for qt, so no unittest

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_buttons
        """
        def mock_add(self, *args):
            print('called ButtonBox.addButton with args', args)
            return mockqtw.MockPushButton()
        def callback1():
            "dummy function for reference"
        def callback2():
            "dummy function for reference"
        def callback3():
            "dummy function for reference"
        monkeypatch.setattr(mockqtw.MockButtonBox, 'addButton', mock_add)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons([])
        assert capsys.readouterr().out == ("called ButtonBox.__init__ with args ()\n"
                                           "called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_buttons([('ok', callback1), ('cancel', callback2), ('text', callback3)])
        assert capsys.readouterr().out == ("called ButtonBox.__init__ with args ()\n"
                                           "called ButtonBox.addButton with args (1,)\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback1},)\n"
                                           "called ButtonBox.addButton with args (2,)\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback2},)\n"
                                           "called ButtonBox.addButton with args ('text', 9)\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback3},)\n"
                                           "called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def _test_finish_display(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.finish_display
        """
        # not implemented for qt, so no unittest

    def test_add_row(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.add_row
        """
        class MockFileBrowseButton:
            "stub for FileBrowseButton object"
            def __init__(self, *args, **kwargs):
                print('called gui.FileBrowseButton with args', args, kwargs)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee, 'FileBrowseButton', MockFileBrowseButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        # testobj.scrl = mockqtw.MockScrollArea()
        testobj.bar = mockqtw.MockScrollBar()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called ScrollBar.__init__\n")
        testobj.rownum = 0
        result = testobj.add_row('name')
        assert len(result) == 2
        assert isinstance(result[0], testee.qtw.QCheckBox)
        assert isinstance(result[1], testee.FileBrowseButton)
        assert testobj.rownum == 1
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('name', {testobj})\n"
                "called Grid.addWidget with arg MockCheckBox at (1, 0)\n"
                f"called gui.FileBrowseButton with args ({testobj},)"
                " {'text': '', 'buttoncaption': '', 'dialogtitle': '', 'tooltiptext': ''}\n"
                "called Grid.addWidget with arg MockFileBrowseButton at (1, 1)\n"
                "called Scrollbar.maximum\n"
                "called Scrollbar.setMaximum with value `151`\n"
                "called Scrollbar.maximum\n"
                "called Scrollbar.setValue with value `99`\n")
        testobj.rownum = 0
        result = testobj.add_row('name', 'path', buttoncaption='btn', dialogtitle='dlg',
                                 tooltiptext='tip')
        assert len(result) == 2
        assert isinstance(result[0], testee.qtw.QCheckBox)
        assert isinstance(result[1], testee.FileBrowseButton)
        assert testobj.rownum == 1
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('name', {testobj})\n"
                "called Grid.addWidget with arg MockCheckBox at (1, 0)\n"
                f"called gui.FileBrowseButton with args ({testobj},) {{'text': 'path',"
                " 'buttoncaption': 'btn', 'dialogtitle': 'dlg', 'tooltiptext': 'tip'}\n"
                "called Grid.addWidget with arg MockFileBrowseButton at (1, 1)\n"
                "called Scrollbar.maximum\n"
                "called Scrollbar.setMaximum with value `151`\n"
                "called Scrollbar.maximum\n"
                "called Scrollbar.setValue with value `99`\n")

    def test_delete_row(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.delete_row
        """
        class MockFileBrowseButton:
            "stub for FileBrowseButton object"
            def __init__(self, *args, **kwargs):
                print('called gui.FileBrowseButton with args', args, kwargs)
            def close(self):
                print('called gui.FileBrowseButton.close')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        check = mockqtw.MockCheckBox()
        browse = MockFileBrowseButton()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called gui.FileBrowseButton with args () {}\n")
        testobj.delete_row(2, check, browse)
        assert capsys.readouterr().out == (
                "called Grid.removeWidget with arg MockCheckBox\n"
                "called CheckBox.close\n"
                "called Grid.removeWidget with arg MockFileBrowseButton\n"
                "called gui.FileBrowseButton.close\n")

    def test_get_browser_value(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.get_browser_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        browser = types.SimpleNamespace(input=mockqtw.MockLineEdit())
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        assert testobj.get_browser_value(browser) == ''
        assert capsys.readouterr().out == "called LineEdit.text\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for FilesDialogGui.accept
        """
        def mock_confirm():
            print('called InitialToolDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Rejected
        def mock_confirm_2():
            print('called InitialToolDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Accepted
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == "called InitialToolDialog.confirm\n"
        testobj.master.confirm = mock_confirm_2
        testobj.accept()
        assert capsys.readouterr().out == ("called InitialToolDialog.confirm\n"
                                           "called Dialog.accept\n")


class TestFileBrowseButton:
    """unittest for qtgui.FileBrowseButton
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.FileBrowseButton object

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

    def test_init(self, monkeypatch, capsys):
        """unittest for FileBrowseButton.__init__
        """
        # def mock_init(self, parent):
        #     print(f"called Frame.__init__ with arg {parent}")
        monkeypatch.setattr(testee.qtw.QFrame, '__init__', mockqtw.MockFrame.__init__)
        monkeypatch.setattr(testee.qtw.QFrame, 'setWindowTitle', mockqtw.MockFrame.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QFrame, 'setFrameStyle', mockqtw.MockFrame.setFrameStyle)
        monkeypatch.setattr(testee.qtw.QFrame, 'setLayout', mockqtw.MockFrame.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        cp = {'C_BRWS': 'xxx'}
        parent = types.SimpleNamespace(master=types.SimpleNamespace(title='master1', captions=cp),
                                       parent=types.SimpleNamespace(
                                           master=types.SimpleNamespace(title='master2',
                                                                        captions=cp)))
        testobj = testee.FileBrowseButton(parent)
        assert testobj.dialogtitle == ''
        assert isinstance(testobj.input, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called Frame.setFrameStyle with arg `34`\n"
                                           "called VBox.__init__\n"
                                           "called HBox.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called LineEdit.setMinimumWidth with arg `200`\n"
                                           "called HBox.addWidget with arg MockLineEdit\n"
                                           "called PushButton.__init__ with args"
                                           f" ('', {testobj}) {{'clicked': {testobj.browse}}}\n"
                                           "called HBox.addWidget with arg MockPushButton\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n"
                                           "called Frame.setLayout with arg MockVBoxLayout\n")
        testobj = testee.FileBrowseButton(parent, text="xxx\\yyy", buttoncaption="xxx",
                                          dialogtitle="yyy", tooltiptext="zzz")
        assert testobj.dialogtitle == 'yyy'
        assert isinstance(testobj.input, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called Frame.setFrameStyle with arg `34`\n"
                                           "called VBox.__init__\n"
                                           "called HBox.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called LineEdit.setMinimumWidth with arg `200`\n"
                                           "called HBox.addWidget with arg MockLineEdit\n"
                                           "called PushButton.__init__ with args"
                                           f" ('xxx', {testobj}) {{'clicked': {testobj.browse}}}\n"
                                           "called HBox.addWidget with arg MockPushButton\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n"
                                           "called Frame.setLayout with arg MockVBoxLayout\n")

    def test_browse(self, monkeypatch, capsys):
        """unittest for FileBrowseButton.browse
        """
        def mock_get(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileName with args', parent, args, kwargs)
            return 'zzz', True
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName',
                            mockqtw.MockFileDialog.getOpenFileName)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.input = mockqtw.MockLineEdit()
        testobj.dialogtitle = 'yyy'
        assert capsys.readouterr().out == ("called LineEdit.__init__\n")
        testobj.browse()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                f" ('yyy', '{testee.shared.HERE}/plugins') {{}}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get)
        testobj.input = mockqtw.MockLineEdit('qqq')
        assert capsys.readouterr().out == ("called LineEdit.__init__\n")
        testobj.browse()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                f"called FileDialog.getOpenFileName with args {testobj} ('yyy', 'qqq') {{}}\n"
                "called LineEdit.setText with arg `zzz`\n")


class TestSetupDialogGui:
    """unittest for qtgui.SetupDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.SetupDialogGui object

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
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.SetupDialogGui('master', 'parent', 'title')
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args parent () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n"
                "called Grid.__init__\n"
                "called VBox.addLayout with arg MockGridLayout\n")

    def test_add_textinput_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_textinput_line
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.lineno = 0
        assert isinstance(testobj.add_textinput_line('text', 'suggest'), testee.qtw.QLineEdit)
        assert testobj.lineno == 1
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0, 1, 3)\n"
                "called LineEdit.__init__\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_checkbox_line
        """
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.lineno = 0
        assert isinstance(testobj.add_checkbox_line('text'), testee.qtw.QCheckBox)
        assert testobj.lineno == 1
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockCheckBox at (1, 0, 1, 4)\n")

    def test_add_filebrowse_line(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_filebrowse_line
        """
        class MockFileBrowseButton:
            "stub for FileBrowseButton object"
            def __init__(self, *args, **kwargs):
                print('called FileBrowseButton with args', args, kwargs)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee, 'FileBrowseButton', MockFileBrowseButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.grid = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.lineno = 0
        result = testobj.add_filebrowse_line('text', 'suggest')
        assert isinstance(result, testee.FileBrowseButton)
        assert testobj.lineno == 1
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0, 1, 2)\n"
                f"called FileBrowseButton with args ({testobj},)"
                " {'text': 'suggest', 'buttoncaption': '', 'dialogtitle': '', 'tooltiptext': ''}\n"
                "called Grid.addWidget with arg MockFileBrowseButton at (1, 2, 1, 3)\n")
        testobj.lineno = 0
        result = testobj.add_filebrowse_line('text', 'suggest', buttoncaption='xxx',
                                             dialogtitle='yyy', tooltiptext='zzz')
        assert isinstance(result, testee.FileBrowseButton)
        assert testobj.lineno == 1
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('text', {testobj})\n"
                "called Grid.addWidget with arg MockLabel at (1, 0, 1, 2)\n"
                f"called FileBrowseButton with args ({testobj},) {{'text': 'suggest',"
                " 'buttoncaption': 'xxx', 'dialogtitle': 'yyy', 'tooltiptext': 'zzz'}\n"
                "called Grid.addWidget with arg MockFileBrowseButton at (1, 2, 1, 3)\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.vbox = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called ButtonBox.__init__ with args ()\n"
                                           "called ButtonBox.addButton with args (1,)\n"
                                           "called ButtonBox.addButton with args (2,)\n"
                                           f"called Signal.connect with args ({testobj.accept},)\n"
                                           f"called Signal.connect with args ({testobj.reject},)\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_textinput_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        ted = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        assert testobj.get_textinput_value(ted) == ''
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert not testobj.get_checkbox_value(cb)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")

    def test_get_filebrowse_value(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.get_filebrowse_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        fbb = types.SimpleNamespace(input=mockqtw.MockLineEdit())
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        assert testobj.get_filebrowse_value(fbb) == ''
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for SetupDialogGui.accept
        """
        def mock_confirm():
            print('called SetupDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Rejected
        def mock_confirm_2():
            print('called SetupDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Accepted
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == "called SetupDialog.confirm\n"
        testobj.master.confirm = mock_confirm_2
        testobj.accept()
        assert capsys.readouterr().out == ("called SetupDialog.confirm\n"
                                           "called Dialog.accept\n")


class TestDeleteDialogGui:
    """unittest for qtgui.DeleteDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.DeleteDialogGui object

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
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.DeleteDialogGui('master', 'parent', 'title')
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args parent () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_text_line(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.add_text_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_text_line('text')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Label.__init__ with args ('text', {testobj})\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.add_checkbox_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_checkbox_line('text')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called CheckBox.__init__ with args ('text', {testobj})\n"
                                           "called HBox.addWidget with arg MockCheckBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == (
                "called ButtonBox.__init__ with args ()\n"
                "called ButtonBox.addButton with args (1,)\n"
                "called ButtonBox.addButton with args (2,)\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called VBox.addWidget with arg MockButtonBox\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert not testobj.get_checkbox_value(cb)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for DeleteDialogGui.accept
        """
        def mock_confirm():
            print('called InitialToolDialog.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called InitialToolDialog.confirm\n"
                                           "called Dialog.accept\n")


class TestColumnSettingsDialogGui:
    """unittest for qtgui.ColumnSettingsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.ColumnSettingsDialogGui object

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
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.ColumnSettingsDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args parent () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")
        # monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        # def mock_add(*args):
        #     print('called ColumsSettingsDialogGui.add_row with args', args)
        # monkeypatch.setattr(mockqtw.MockButtonBox, 'addButton', mock_addbutton)
        # monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        # monkeypatch.setattr(testee.ColumnSettingsDialog, 'add_row', mock_add)
        # parent = mockqtw.MockFrame()
        # master = types.SimpleNamespace(book=types.SimpleNamespace(page=types.SimpleNamespace()))
        # master.title = 'title'
        # master.captions = {'T_COLSET': 'COLSET {}', 'C_TTL': 'TTL', 'C_WID': 'WID', 'C_IND': 'IND',
        #                    'C_SEQ': 'SEQ', 'C_ADDCOL': 'ADDCOL', 'C_REMCOL': 'REMCOL'}
        # master.col_textids = []
        # master.col_names = []
        # master.book.page.settings = {testee.shared.SettType.PNL.value: 'XXX'}
        # master.book.page.column_info = [('xxx', 5, 0, 0), ('yyy', 10, 1, 1)]
        # assert testobj.rownum == 0
        # assert testobj.data == []
        # assert testobj.checks == []
        # assert testobj.col_textids == master.col_textids
        # assert testobj.col_names == master.col_names

    def test_add_explanation(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_explanation
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_explanation('text')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Label.__init__ with args ('text', {testobj})\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_captions(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_captions
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_captions([])
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_captions([('xx', 10), ('yy', 20)])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addSpacing\n"
                f"called Label.__init__ with args ('xx', {testobj})\n"
                "called HBox.addWidget with args"
                " MockLabel {'alignment': <AlignmentFlag.AlignCenter: 132>}\n"
                "called HBox.addSpacing\n"
                f"called Label.__init__ with args ('yy', {testobj})\n"
                "called HBox.addWidget with args"
                " MockLabel {'alignment': <AlignmentFlag.AlignCenter: 132>}\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_columndefs_area(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_columndefs_area
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_columndefs_area()
        assert isinstance(result, testee.qtw.QScrollArea)
        assert testobj.bar == 'vertical scrollbar'
        assert isinstance(testobj.gsizer, testee.qtw.QGridLayout)
        assert testobj.rownum == 0
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           f"called ScrollArea.__init__ with args ({testobj},)\n"
                                           "called ScrollArea.setWidget with arg `MockFrame`\n"
                                           "called ScrollArea.setAlignment with arg 64\n"
                                           "called ScrollArea.setWidgetResizable with arg `True`\n"
                                           "called ScrollArea.verticalScrollBar\n"
                                           "called Grid.__init__\n"
                                           "called VBox.__init__\n"
                                           "called VBox.addLayout with arg MockGridLayout\n"
                                           "called VBox.addStretch\n"
                                           "called Frame.setLayout with arg MockVBoxLayout\n"
                                           "called VBox.addWidget with arg MockScrollArea\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_buttons
        """
        def mock_add(self, *args):
            print('called ButtonBox.addButton with args', args)
            return mockqtw.MockPushButton()
        def callback1():
            "dummy function for reference"
        def callback2():
            "dummy function for reference"
        def callback3():
            "dummy function for reference"
        monkeypatch.setattr(mockqtw.MockButtonBox, 'addButton', mock_add)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons([])
        assert capsys.readouterr().out == ("called ButtonBox.__init__ with args ()\n"
                                           "called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_buttons([('ok', callback1), ('cancel', callback2), ('text', callback3)])
        assert capsys.readouterr().out == ("called ButtonBox.__init__ with args ()\n"
                                           "called ButtonBox.addButton with args (1,)\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback1},)\n"
                                           "called ButtonBox.addButton with args (2,)\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback2},)\n"
                                           "called ButtonBox.addButton with args ('text', 9)\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback3},)\n"
                                           "called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def _test_finalize_columndefs_area(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.finalize_columndefs_area
        """
        # not implemented, so no unittest

    def test_add_checkbox_to_line(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_checkbox_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_checkbox_to_line('row', 'col', 'text', '', False, True)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called CheckBox.__init__ with args ({testobj},)\n"
                "called HBox.addWidget with arg MockCheckBox\n"
                "called HBox.addSpacing\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 'col')\n")
        result = testobj.add_checkbox_to_line('row', 'col', 'text', 'width', True, False)
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addSpacing\n"
                f"called CheckBox.__init__ with args ({testobj},)\n"
                "called CheckBox.setFixedWidth with arg 'width'\n"
                "called HBox.addWidget with arg MockCheckBox\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 'col')\n")

    def test_add_combobox_to_line(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_combobox_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_combobox_to_line('row', 'col', [], 0)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.addItems with arg []\n"
                "called ComboBox.setEditable with arg `True`\n"
                f"called Signal.connect with args ({testobj.on_text_changed},)\n"
                "called Grid.addWidget with arg MockComboBox at ('row', 'col')\n")
        result = testobj.add_combobox_to_line('row', 'col', ['x', 'y'], 1)
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                "called ComboBox.addItems with arg ['x', 'y']\n"
                "called ComboBox.setEditable with arg `True`\n"
                f"called Signal.connect with args ({testobj.on_text_changed},)\n"
                "called ComboBox.setCurrentIndex with arg `0`\n"
                "called Grid.addWidget with arg MockComboBox at ('row', 'col')\n")

    def test_add_spinbox_to_line(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.add_spinbox_to_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        result = testobj.add_spinbox_to_line('row', 'col', '', ('', ''), 'width', ('', ''))
        assert isinstance(result, testee.qtw.QSpinBox)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called SpinBox.__init__\n"
                "called SpinBox.setMaximum with arg ''\n"
                "called SpinBox.setFixedWidth with arg 'width'\n"
                "called HBox.addWidget with arg MockSpinBox\n"
                "called HBox.addStretch\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 'col')\n")
        result = testobj.add_spinbox_to_line('row', 'col', 'x', ('min', 'max'), 'width', ('f', 'a'))
        assert isinstance(result, testee.qtw.QSpinBox)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addSpacing\n"
                "called SpinBox.__init__\n"
                "called SpinBox.setMinimum with arg 'min'\n"
                "called SpinBox.setMaximum with arg 'max'\n"
                "called SpinBox.setValue with arg 'x'\n"
                "called SpinBox.setFixedWidth with arg 'width'\n"
                "called HBox.addWidget with arg MockSpinBox\n"
                "called HBox.addSpacing\n"
                "called Grid.addLayout with arg MockHBoxLayout at ('row', 'col')\n")

    def test_finalize_line(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.finalize_line
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.bar = mockqtw.MockScrollBar()
        assert capsys.readouterr().out == "called ScrollBar.__init__\n"
        testobj.finalize_line()
        assert capsys.readouterr().out == ("called Scrollbar.maximum\n"
                                           "called Scrollbar.setMaximum with value `161`\n"
                                           "called Scrollbar.maximum\n"
                                           "called Scrollbar.setValue with value `99`\n")

    def test_adapt_column_index(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.adapt_column_index
        """
        def mock_value():
            print('called SpinBox.value')
            return 2
        def mock_value_2():
            print('called SpinBox.value')
            return 1
        def mock_set(arg):
            print(f'called SpinBox.setValue with arg {arg}')
        current_widget = types.SimpleNamespace(value=mock_value, setValue=mock_set)
        removed_widget = types.SimpleNamespace(value=mock_value)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.adapt_column_index(removed_widget, current_widget)
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called SpinBox.value\n")
        removed_widget.value = mock_value_2
        testobj.adapt_column_index(removed_widget, current_widget)
        assert capsys.readouterr().out == ("called SpinBox.value\n"
                                           "called SpinBox.value\n"
                                           "called SpinBox.value\n"
                                           "called SpinBox.setValue with arg 1\n")

    def test_delete_row(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.delete_row
        """
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockVBoxLayout()
        testobj.rownum = 2
        check = mockqtw.MockCheckBox()
        spinner = mockqtw.MockSpinBox(1)
        w0 = mockqtw.MockWidget()
        w1 = mockqtw.MockWidget()
        w3 = mockqtw.MockWidget()
        widgets = [w0, w1, spinner, w3, '']
        assert capsys.readouterr().out == ("called VBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called SpinBox.__init__\n"
                                           "called Widget.__init__\n"
                                           "called Widget.__init__\n"
                                           "called Widget.__init__\n")
        testobj.delete_row(0, check, widgets)
        assert testobj.rownum == 1
        assert capsys.readouterr().out == (
                "called VBox.removeWidget with arg MockCheckBox\n"
                "called CheckBox.close\n"
                "called VBox.removeWidget with arg MockWidget\n"
                "called Widget.close\n"
                "called VBox.removeWidget with arg MockWidget\n"
                "called Widget.close\n"
                "called VBox.removeWidget with arg MockSpinBox\n"
                "called SpinBox.close\n"
                "called VBox.removeWidget with arg MockWidget\n"
                "called Widget.close\n"
                "called VBox.itemAt with arg 0\n"
                "called VBox.removeItem\n")

    def test_on_text_changed(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.on_text_changed
        """
        class MockComboBox:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called ComboBox.__init__')
                self._text = args[0]
            def currentText(self):
                print('called ComboBox.currentText')
                return self._text
        name1 = MockComboBox('name1')
        width1 = mockqtw.MockSpinBox(10)
        name2 = MockComboBox('name2')
        width2 = mockqtw.MockSpinBox(1)
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called SpinBox.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called SpinBox.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(data=[])
        testobj.on_text_changed('name2')
        assert capsys.readouterr().out == ""
        testobj.master.data = [(name1, width1, 'x', 'y'), (name2, width2, 'a', 'b')]
        testobj.on_text_changed('name2')
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called ComboBox.currentText\n"
                                           "called SpinBox.setValue with arg '50'\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert not testobj.get_checkbox_value(cb)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")

    def test_get_combobox_value(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.get_combobox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cmb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_value(cmb) == 'current text'
        assert capsys.readouterr().out == ("called ComboBox.currentText\n")

    def test_get_spinbox_value(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.get_spinbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        sb = mockqtw.MockSpinBox(2)
        assert capsys.readouterr().out == "called SpinBox.__init__\n"
        assert testobj.get_spinbox_value(sb) == 2
        assert capsys.readouterr().out == ("called SpinBox.value\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialogGui.accept
        """
        def mock_confirm():
            print('called InitialToolDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Rejected
        def mock_confirm_2():
            print('called InitialToolDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Accepted
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == "called InitialToolDialog.confirm\n"
        testobj.master.confirm = mock_confirm_2
        testobj.accept()
        assert capsys.readouterr().out == ("called InitialToolDialog.confirm\n"
                                           "called Dialog.accept\n")


class TestNewColumnsDialogGui:
    """unittest for qtgui.NewColumnsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.NewColumnsDialogGui object

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
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        testobj = testee.NewColumnsDialogGui('master', 'parent', 'title')
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.gsizer, testee.qtw.QGridLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args parent () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\ncalled Grid.__init__\n"
                "called VBox.addLayout with arg MockGridLayout\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_explanation(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.add_explanation
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_explanation('text')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Label.__init__ with args ('text', {testobj})\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_titles(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.add_titles
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        testobj.add_titles(['xxx', 'yyy'])
        assert capsys.readouterr().out == (f"called Label.__init__ with args ('xxx', {testobj})\n"
                                           "called Grid.addWidget with arg MockLabel at (0, 0)\n"
                                           f"called Label.__init__ with args ('yyy', {testobj})\n"
                                           "called Grid.addWidget with arg MockLabel at (0, 1)\n")

    def test_add_text_entry(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.add_text_entry
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == "called Grid.__init__\n"
        assert isinstance(testobj.add_text_entry('xxx', 1, 2, True), testee.qtw.QLineEdit)
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.setEnabled with arg True\n"
                                           "called Grid.addWidget with arg MockLineEdit at (1, 2)\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == (
                "called ButtonBox.__init__ with args ()\n"
                "called ButtonBox.addButton with args (1,)\n"
                "called ButtonBox.addButton with args (2,)\n"
                f"called Signal.connect with args ({testobj.accept},)\n"
                f"called Signal.connect with args ({testobj.reject},)\n"
                "called HBox.__init__\n"
                "called HBox.addStretch\n"
                "called HBox.addWidget with arg MockButtonBox\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_get_textentry_value(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.get_textentry_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        ted = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        assert testobj.get_textentry_value(ted) == ''
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for NewColumnsDialogGui.accept
        """
        def mock_confirm():
            print('called InitialToolDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Rejected
        def mock_confirm_2():
            print('called InitialToolDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Accepted
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == "called InitialToolDialog.confirm\n"
        testobj.master.confirm = mock_confirm_2
        testobj.accept()
        assert capsys.readouterr().out == ("called InitialToolDialog.confirm\n"
                                           "called Dialog.accept\n")


class TestExtraSettingsDialogGui:
    """unittest for qtgui.ExtraSettingsDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.ExtraSettingsDialogGui object

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
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QFrame, 'setFrameStyle', mockqtw.MockFrame.setFrameStyle)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.ExtraSettingsDialogGui('master', 'parent', 'title')
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args parent () {}\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_block(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_block
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.start_block()
        assert isinstance(result, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called VBox.__init__\n"
                                           "called Frame.setLayout with arg MockVBoxLayout\n"
                                           "called Frame.setFrameStyle with arg `38`\n"
                                           "called VBox.addWidget with arg MockFrame\n")

    def test_add_textinput_line(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_textinput_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        vsizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_textinput_line(vsizer, 'text', 'suggest')
        assert isinstance(result, testee.qtw.QLineEdit)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Label.__init__ with args ('text', {testobj})\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called LineEdit.__init__\n"
                                           "called HBox.addWidget with arg MockLineEdit\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_checkbox_line(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_checkbox_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        vsizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_checkbox_line(vsizer, 'xxx', 'yyy')
        assert isinstance(result, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called CheckBox.__init__ with args ('xxx', {testobj})\n"
                                           "called CheckBox.setChecked with arg yyy\n"
                                           "called HBox.addWidget with arg MockCheckBox\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_text_line(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_text_line
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        vsizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_text_line(vsizer, 'text')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           f"called Label.__init__ with args ('text', {testobj})\n"
                                           "called HBox.addWidget with arg MockLabel\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_titles(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_titles
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        vsizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_titles(vsizer, [(10, 'xx'), ('20', 'yy')])
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                "called HBox.addSpacing\n"
                f"called Label.__init__ with args ('xx', {testobj})\n"
                "called HBox.addWidget with args"
                " MockLabel {'alignment': <AlignmentFlag.AlignHCenter: 4>}\n"
                "called HBox.addSpacing\n"
                f"called Label.__init__ with args ('yy', {testobj})\n"
                "called HBox.addWidget with args"
                " MockLabel {'alignment': <AlignmentFlag.AlignHCenter: 4>}\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_inputarea(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_inputarea
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
        vsizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.add_inputarea(vsizer), testee.qtw.QScrollArea)
        assert testobj.bar == 'vertical scrollbar'
        assert isinstance(testobj.gsizer, testee.qtw.QGridLayout)
        assert testobj.rownum == 0
        assert capsys.readouterr().out == (
                "called Frame.__init__\n"
                f"called ScrollArea.__init__ with args ({testobj},)\n"
                "called ScrollArea.setWidget with arg `MockFrame`\n"
                "called ScrollArea.setWidgetResizable with arg `True`\n"
                "called ScrollArea.verticalScrollBar\n"
                "called Grid.__init__\n"
                "called Frame.setLayout with arg MockGridLayout\n"
                "called Frame.setFrameStyle with arg `32`\n"
                "called ScrollArea.ensureVisible with args (0, 0)\n"
                "called VBox.addWidget with arg MockScrollArea\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_buttons
        """
        def callback1():
            "dummy function for reference"
        def callback2():
            "dummy function for reference"
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        vsizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_buttons(vsizer, [('xx', callback1), ('yy', callback2)])
        assert capsys.readouterr().out == (
                f"called HBox.__init__\n"
                "called HBox.addStretch\n"
                f"called PushButton.__init__ with args ('xx', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback1},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                f"called PushButton.__init__ with args ('yy', {testobj}) {{}}\n"
                f"called Signal.connect with args ({callback2},)\n"
                "called HBox.addWidget with arg MockPushButton\n"
                "called HBox.addStretch\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called ButtonBox.__init__ with args ()\n"
                                           "called ButtonBox.addButton with args (1,)\n"
                                           "called ButtonBox.addButton with args (2,)\n"
                                           f"called Signal.connect with args ({testobj.accept},)\n"
                                           f"called Signal.connect with args ({testobj.reject},)\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.add_row
        """
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.rownum = 0
        testobj.gsizer = mockqtw.MockGridLayout()
        testobj.bar = mockqtw.MockScrollBar()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called ScrollBar.__init__\n")
        testobj.add_row('', 'value', 'desc')
        assert testobj.rownum == 2
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj},)\n"
                "called Grid.addWidget with arg MockCheckBox at (1, 0)\n"
                "called LineEdit.__init__\n"
                "called LineEdit.setFixedWidth with arg `88`\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 1)\n"
                "called LineEdit.__init__\n"
                "called Grid.addWidget with arg MockLineEdit at (1, 2)\n"
                "called LineEdit.__init__\n"
                "called Grid.addWidget with arg MockLineEdit at (2, 2)\n"
                "called Scrollbar.maximum\ncalled Scrollbar.setMaximum with value `161`\n"
                "called Scrollbar.maximum\ncalled Scrollbar.setValue with value `99`\n")
        testobj.add_row('name', 'value', 'desc')
        assert testobj.rownum == 4
        assert capsys.readouterr().out == (
                f"called CheckBox.__init__ with args ({testobj},)\n"
                "called Grid.addWidget with arg MockCheckBox at (3, 0)\n"
                "called LineEdit.__init__\n"
                "called LineEdit.setFixedWidth with arg `88`\n"
                "called LineEdit.setReadOnly with arg `True`\n"
                "called Grid.addWidget with arg MockLineEdit at (3, 1)\n"
                "called LineEdit.__init__\n"
                "called Grid.addWidget with arg MockLineEdit at (3, 2)\n"
                "called LineEdit.__init__\n"
                "called Grid.addWidget with arg MockLineEdit at (4, 2)\n"
                "called Scrollbar.maximum\ncalled Scrollbar.setMaximum with value `161`\n"
                "called Scrollbar.maximum\ncalled Scrollbar.setValue with value `99`\n")

    def test_delete_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.delete_row
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        check = mockqtw.MockCheckBox()
        name = mockqtw.MockLineEdit()
        value = mockqtw.MockLineEdit()
        desc = mockqtw.MockLineEdit()
        testobj.gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == ("called CheckBox.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called Grid.__init__\n")
        testobj.delete_row(1, [check, name, value, desc])
        assert capsys.readouterr().out == ("called Grid.removeWidget with arg MockCheckBox\n"
                                           "called CheckBox.close\n"
                                           "called Grid.removeWidget with arg MockLineEdit\n"
                                           "called LineEdit.close\n"
                                           "called Grid.removeWidget with arg MockLineEdit\n"
                                           "called LineEdit.close\n"
                                           "called Grid.removeWidget with arg MockLineEdit\n"
                                           "called LineEdit.close\n")

    def test_get_checkbox_value(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.get_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert not testobj.get_checkbox_value(cb)
        assert capsys.readouterr().out == "called CheckBox.isChecked\n"

    def test_get_textinput_value(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.get_textinput_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        txt = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        assert testobj.get_textinput_value(txt) == ''
        assert capsys.readouterr().out == "called LineEdit.text\n"

    def test_set_checkbox_value(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.set_checkbox_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj.set_checkbox_value(cb, 'xxx')
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg xxx\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialogGui.accept
        """
        def mock_confirm():
            print('called InitialToolDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Rejected
        def mock_confirm_2():
            print('called InitialToolDialog.confirm')
            return testee.qtw.QDialog.DialogCode.Accepted
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == "called InitialToolDialog.confirm\n"
        testobj.master.confirm = mock_confirm_2
        testobj.accept()
        assert capsys.readouterr().out == ("called InitialToolDialog.confirm\n"
                                           "called Dialog.accept\n")


class TestEntryDialogGui:
    """unittest for qtgui.EntryDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.EntryDialogGui object

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
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        # monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        # monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        # monkeypatch.setattr(mockqtw.MockButtonBox, 'addButton', mock_addbutton)
        testobj = testee.EntryDialogGui('master', 'parent', 'title')
        assert testobj.master == 'master'
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args parent () {}\n"
                "called Dialog.resize with args (680, 400)\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_table_to_display(self, monkeypatch, capsys):
        """unittest for TextEntryDialogGui.add_table_to_display
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        result = testobj.add_table_to_display([])
        assert isinstance(result, testee.qtw.QTableWidget)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Table.__init__ with args ({testobj},)\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setColumnCount with arg '0'\n"
                "called Table.setHorizontalHeaderLabels with arg '[]'\n"
                "called Table.horizontalHeader\n"
                "called HBox.addWidget with arg MockTable\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")
        result = testobj.add_table_to_display([('xx', 10), ('yy', 20)])
        assert isinstance(result, testee.qtw.QTableWidget)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Table.__init__ with args ({testobj},)\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setColumnCount with arg '2'\n"
                "called Table.setHorizontalHeaderLabels with arg '['xx', 'yy']'\n"
                "called Table.horizontalHeader\n"
                "called Header.resizeSection with args (0, 10)\n"
                "called Header.resizeSection with args (1, 20)\n"
                "called HBox.addWidget with arg MockTable\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_buttons(self, monkeypatch, capsys):
        """unittest for TextEntryDialogGui.add_buttons
        """
        def mock_add(self, *args):
            print('called ButtonBox.addButton with args', args)
            return mockqtw.MockPushButton()
        def callback1():
            "dummy function for reference"
        def callback2():
            "dummy function for reference"
        def callback3():
            "dummy function for reference"
        monkeypatch.setattr(mockqtw.MockButtonBox, 'addButton', mock_add)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_buttons([])
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called ButtonBox.__init__ with args ()\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_buttons([('ok', callback1), ('cancel', callback2), ('text', callback3)])
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called ButtonBox.__init__ with args ()\n"
                                           "called ButtonBox.addButton with args (4,)\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback1},)\n"
                                           "called ButtonBox.addButton with args (2,)\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback2},)\n"
                                           "called ButtonBox.addButton with args ('text', 9)\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           f"called Signal.connect with args ({callback3},)\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_row(self, monkeypatch, capsys):
        """unittest for TextEntryDialogGui.add_row
        """
        monkeypatch.setattr(testee.qtw, 'QTableWidgetItem', mockqtw.MockTableItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.add_row(p0list, 1, ['x', 'y'])
        assert capsys.readouterr().out == (
                "called Table.rowCount\n"
                "called Table.insertRow with arg '1'\n"
                "called TableItem.__init__ with arg ''\n"
                "called TableItem.setText with arg 'x'\n"
                "called Table.setItem with args (0, 0, MockTableItem)\n"
                "called TableItem.__init__ with arg ''\n"
                "called TableItem.setText with arg 'y'\n"
                "called Table.setItem with args (0, 1, MockTableItem)\n"
                "called Table.scrollToBottom\n")

    def test_delete_key(self, monkeypatch, capsys):
        """unittest for EntryDialogGui.delete_key
        """
        def mock_selected():
            print('called Table.selectedRanges')
            return [mockqtw.MockTableSelectionRange(0, 1, 1, 1)]
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = testee.qtw.QTableWidget()
        p0list.setRowCount(2)
        p0list.selectedRanges = mock_selected
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n"
                                           "called Table.setRowCount with arg '2'\n")
        testobj.delete_key(p0list)
        assert capsys.readouterr().out == ("called Table.selectedRanges\n"
                                           "called TableRange.__init__ with args (0, 1, 1, 1)\n"
                                           "called TableRange.rowCount\n"
                                           "called TableRange.topRow\n"
                                           "called TableRange.topRow\n"
                                           "called Table.removeRow with arg '1'\n"
                                           "called Table.removeRow with arg '0'\n")

    def test_get_table_columns(self, monkeypatch, capsys):
        """unittest for TextEntryDialogGui.get_table_columns
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        assert testobj.get_table_columns(p0list) == 0
        assert capsys.readouterr().out == ("called Table.columnCount\n")

    def test_get_tableitem_value(self, monkeypatch, capsys):
        """unittest for TextEntryDialogGui.get_tableitem_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTable()
        table_item = mockqtw.MockTableItem('text')
        p0list.setItem(1, 2, table_item)
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n"
                                           "called TableItem.__init__ with arg 'text'\n"
                                           "called Table.setItem with args (1, 2, MockTableItem)\n")
        assert testobj.get_tableitem_value(p0list, 1, 2) == 'text'
        assert capsys.readouterr().out == ("called Table.item with args (1, 2)\n"
                                           "called TableItem.text\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for EntryDialogGui.accept
        """
        def mock_confirm():
            print('called EntryDialog.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called EntryDialog.confirm\n"
                                           "called Dialog.accept\n")


class TestCompleteDialogGui:
    """unittest for qtgui.CompleteDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for qtgui.CompleteDialogGui object

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
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = testee.CompleteDialogGui('master', 'parent', 'title')
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args parent () {}\n"
                "called Dialog.resize with args (1100, 700)\n"
                "called Dialog.setWindowTitle with args ('title',)\n"
                "called VBox.__init__\n"
                "called Dialog.setLayout with arg MockVBoxLayout\n")

    def test_add_table_to_display(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.add_table_to_display
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cmds = [1, 2, 3]
        testobj.sizer = mockqtw.MockVBoxLayout()
        testobj.p0list = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called VBox.__init__\n"
                                           "called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        result = testobj.add_table_to_display([])
        assert isinstance(result, testee.qtw.QTableWidget)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           f"called Table.__init__ with args (3, 3, {testobj})\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n"
                                           "called Table.setHorizontalHeaderLabels with arg '[]'\n"
                                           "called Table.horizontalHeader\n"
                                           "called Header.setStretchLastSection with arg True\n"
                                           "called HBox.addWidget with arg MockTable\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        result = testobj.add_table_to_display([('xx', 10.), ('yy', 20,)])
        assert isinstance(result, testee.qtw.QTableWidget)
        assert capsys.readouterr().out == (
                "called HBox.__init__\n"
                f"called Table.__init__ with args (3, 3, {testobj})\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setHorizontalHeaderLabels with arg '['xx', 'yy']'\n"
                "called Table.horizontalHeader\n"
                "called Table.setColumnWidth with args (0, 10.0)\n"
                "called Table.setColumnWidth with args (0, 20)\n"
                "called Header.setStretchLastSection with arg True\n"
                "called HBox.addWidget with arg MockTable\n"
                "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_row(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.add_row
        """
        def mock_flags(self):
            print('called TableItem.flags')
            return testee.core.Qt.ItemFlag.ItemIsEditable
        monkeypatch.setattr(testee.qtw, 'QTableWidgetItem', mockqtw.MockTableItem)
        monkeypatch.setattr(mockqtw.MockTableItem, 'flags', mock_flags)
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.add_row(p0list, 1, 'key', 'desc', 'olddesc')
        assert capsys.readouterr().out == (
                "called TableItem.__init__ with arg ''\n"
                "called TableItem.setText with arg 'key'\n"
                "called Table.setItem with args (1, 0, MockTableItem)\n"
                "called TableItem.__init__ with arg ''\n"
                "called TableItem.setText with arg 'desc'\n"
                "called TableItem.flags\n"
                "called TableItem.setFlags with arg ItemFlag.NoItemFlags\n"
                "called Table.setItem with args (1, 1, MockTableItem)\n"
                "called TableItem.__init__ with arg ''\n"
                "called TableItem.setText with arg 'olddesc'\n"
                "called TableItem.flags\n"
                "called TableItem.setFlags with arg ItemFlag.NoItemFlags\n"
                "called Table.setItem with args (1, 2, MockTableItem)\n")

    def test_add_okcancel_buttons(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.add_okcancel_buttons
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_okcancel_buttons()
        assert capsys.readouterr().out == ("called ButtonBox.__init__ with args ()\n"
                                           "called ButtonBox.addButton with args (4,)\n"
                                           "called ButtonBox.addButton with args (2,)\n"
                                           f"called Signal.connect with args ({testobj.accept},)\n"
                                           f"called Signal.connect with args ({testobj.reject},)\n"
                                           "called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg MockButtonBox\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_set_focus_to_list(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.set_focus_to_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        p0list = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.set_focus_to_list(p0list)
        assert capsys.readouterr().out == "called Table.setCurrentCell with args (0, 1)\n"

    def test_accept(self, monkeypatch, capsys):
        """unittest for CompleteDialogGui.accept
        """
        def mock_confirm():
            print('called InitialToolDialog.confirm')
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(confirm=mock_confirm)
        testobj.accept()
        assert capsys.readouterr().out == ("called InitialToolDialog.confirm\n"
                                           "called Dialog.accept\n")
