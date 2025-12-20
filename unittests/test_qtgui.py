"""unittests for ./editor/gui_qt.py
"""
# import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from editor import gui_qt as testee


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


class TestSingleDataInterface:
    """unittests for gui_qt.SingleDataInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.SingleDataInterface object

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


class TestTabbedInterface:
    """unittests for gui_qt.TabbedInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.TabbedInterface object

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

    def test_get_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        assert testobj.get_panel() == "current widget"
        assert capsys.readouterr().out == "called StackedWidget.currentWidget\n"

    def test_get_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        assert testobj.get_selected_panel(1) == 'widget'
        assert capsys.readouterr().out == "called StackedWidget.widget with arg 1\n"

    def test_set_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        testobj.set_selected_panel(2)
        assert capsys.readouterr().out == "called StackedWidget.setCurrentIndex with arg 2\n"

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


class TestGui:
    """unittests for gui_qt.Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.Gui object

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
