"""unittests for ./plugin_examples/mergetool/mergetool_qt.py
"""
import types
from editor.plugins.mergetool import qtgui as testee
from mockgui import mockqtwidgets as mockqtw


class TestMergeDialogGui:
    """unittests for mergetool.qtgui.MergeDialogGui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for mergetool.qtgui.MergeDialogGui object

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
        monkeypatch.setattr(testee.gui, 'QIcon', mockqtw.MockIcon)
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        testobj = testee.MergeDialogGui('master', 'parent')
        assert isinstance(testobj, testee.qtw.QDialog)
        assert capsys.readouterr().out == (
                "called Dialog.__init__ with args parent () {}\n"
                "called Dialog.setWindowTitle with args ('TCCM',)\n"
                "called Icon.__init__ with arg"
                " `/usr/share/icons/Adwaita/16x16/emblems/emblem-ok-symbolic.symbolic.png`\n"
                "called Icon.__init__ with arg"
                " `/usr/share/icons/Adwaita/16x16/emblems/emblem-new.png`\n"
                "called Dialog.resize with args (1500, 900)\n")

    def test_init_display(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.init_display
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.init_display(), testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == "called VBox.__init__\n"

    def test_add_row(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.add_row
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        screen = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        assert isinstance(testobj.add_row(screen), testee.qtw.QHBoxLayout)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_add_col_to_row(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.add_col_to_row
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        row = mockqtw.MockHBoxLayout()
        assert capsys.readouterr().out == "called HBox.__init__\n"
        assert isinstance(testobj.add_col_to_row(row), testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == ("called VBox.__init__\n"
                                           "called HBox.addLayout with arg MockVBoxLayout\n")

    def test_create_list(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_list
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.create_list(['column', 'labels'], 'callback')
        assert isinstance(result, testee.qtw.QTreeWidget)
        assert capsys.readouterr().out == (
                "called Tree.__init__\n"
                "called Tree.setColumnCount with arg `2`\n"
                "called Tree.setHeaderLabels with arg `['column', 'labels']`\n"
                "called Tree.setMouseTracking with arg `True`\n"
                "called Signal.connect with args ('callback',)\n"
                f"called Signal.connect with args ({testobj.popuptext},)\n")

    def test_create_findbutton(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_findbutton
        """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.create_findbutton([])
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.setEditable with arg `False`\n"
                                           "called ComboBox.setCurrentIndex with arg `1`\n")
        result = testobj.create_findbutton(['column', 'labels'])
        assert isinstance(result, testee.qtw.QComboBox)
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.setEditable with arg `False`\n"
                                           "called ComboBox.addItem with arg `Find column`\n"
                                           "called ComboBox.addItem with arg `Find labels`\n"
                                           "called ComboBox.setCurrentIndex with arg `1`\n")

    def test_create_text(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_text
        """
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert isinstance(testobj.create_text(), testee.qtw.QLineEdit)
        assert capsys.readouterr().out == f"called LineEdit.__init__ with args ({testobj},)\n"

    def test_create_button(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_button
        """
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.create_button('text', 'callback')
        assert isinstance(result, testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                f"called PushButton.__init__ with args ('text', {testobj}) {{}}\n"
                "called Signal.connect with args ('callback',)\n")
        result = testobj.create_button('text', 'callback', size=10)
        assert isinstance(result, testee.qtw.QPushButton)
        assert capsys.readouterr().out == (
                f"called PushButton.__init__ with args ('text', {testobj}) {{}}\n"
                "called PushButton.setMaximumWidth with arg `10`\n"
                "called Signal.connect with args ('callback',)\n")

    def test_add_row_to_col(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.add_row_to_col
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        col = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.add_row_to_col(col)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, 'x', 'y')
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg x\n"
                                           "called HBox.addWidget with arg y\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, 'x', 'y', right_align=True)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg x\n"
                                           "called HBox.addWidget with arg y\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, right_align=True)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, 'x', 'y', right_align=False)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg x\n"
                                           "called HBox.addWidget with arg y\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, 'x', 'y', left_align=True)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg x\n"
                                           "called HBox.addWidget with arg y\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, left_align=True)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, 'x', 'y', left_align=False)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg x\n"
                                           "called HBox.addWidget with arg y\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, 'x', 'y', center=True)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addStretch\n"
                                           "called HBox.addWidget with arg x\n"
                                           "called HBox.addWidget with arg y\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, center=True)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")
        testobj.add_row_to_col(col, 'x', 'y', center=False)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg x\n"
                                           "called HBox.addWidget with arg y\n"
                                           "called VBox.addLayout with arg MockHBoxLayout\n")

    def test_finalize_display(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.finalize_display
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        screen = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == "called VBox.__init__\n"
        testobj.finalize_display(screen)
        assert capsys.readouterr().out == "called Dialog.setLayout with arg MockVBoxLayout\n"

    def test_create_hotkey(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.create_hotkey
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'addAction', mockqtw.MockDialog.addAction)
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.create_hotkey('text', 'callback', 'keyseq', 'desc')
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('text', {testobj})\n"
                "called Signal.connect with args ('callback',)\n"
                "called Action.setShortcut with arg `keyseq`\n"
                "called Dialog.addAction\n")

    def test_clear_list(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.clear_list
        """
        listbox = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_list(listbox)
        assert capsys.readouterr().out == "called Tree.clear\n"

    def test_get_listbox_count(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_listbox_count(
        """
        listbox = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_listbox_count(listbox) == 0
        assert capsys.readouterr().out == "called Tree.topLevelItemCount\n"

    def test_add_listitem(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.add_listitem
        """
        listbox = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.add_listitem(listbox, 'keytext', 'command')
        assert isinstance(result, testee.qtw.QTreeWidgetItem)
        assert capsys.readouterr().out == ("called TreeItem.__init__ with args ()\n"
                                           "called TreeItem.setText with args (0, 'keytext')\n"
                                           "called TreeItem.setText with args (1, 'command')\n"
                                           "called Tree.addTopLevelItem\n")

    def test_set_listitem_icon(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.set_listitem_icon
        """
        listbox = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.okicon = 'okicon'
        testobj.set_listitem_icon(listbox, item)
        assert capsys.readouterr().out == "called TreeItem.setIcon with args (0, 'okicon')\n"

    def test_get_selected_listbox_data(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_selected_listbox_data
        """
        class MockTreeItem:
            def text(self, col):
                print(f'called TreeItem.text with arg {col}')
                return f'text{col}'
        class MockTree:
            "teststub"
            def currentItem(self):
                print('called Tree.currentItem')
                return treeitem
        def mock_text(col):
            print(f'called TreeItem.text with arg {col}')
            raise AttributeError
        # monkeypatch.setattr()
        listbox = MockTree()
        treeitem = MockTreeItem()
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_listbox_data(listbox) == (treeitem, 'text0', 'text1')
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           "called TreeItem.text with arg 0\n"
                                           "called TreeItem.text with arg 1\n")
        treeitem.text = mock_text
        assert testobj.get_selected_listbox_data(listbox) == (treeitem, '', '')
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           "called TreeItem.text with arg 0\n"
                                           "called TreeItem.text with arg 1\n")

    def test_find_in_listbox(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.find_in_listbox
        """
        class MockTreeItem:
            def __init__(self, ix):
                self._ix = ix
            def text(self, col):
                print(f'called TreeItem.text with arg {col}')
                return f'text{self._ix}{col}'
        class MockTree:
            "teststub"
            def topLevelItemCount(self):
                print('called Tree.topLevelItemCount')
                return count
            def topLevelItem(self, ix):
                print(f'called Tree.topLevelItem with arg {ix}')
                return treeitems[ix]
        listbox = MockTree()
        treeitems = [MockTreeItem(0), MockTreeItem(1), MockTreeItem(2)]
        testobj = self.setup_testobj(monkeypatch, capsys)
        count = 0
        assert testobj.find_in_listbox(listbox, 'text') is None
        assert capsys.readouterr().out == "called Tree.topLevelItemCount\n"
        count = 3
        assert testobj.find_in_listbox(listbox, 'text10') == treeitems[1]
        assert capsys.readouterr().out == ("called Tree.topLevelItemCount\n"
                                           "called Tree.topLevelItem with arg 0\n"
                                           "called TreeItem.text with arg 0\n"
                                           "called Tree.topLevelItem with arg 1\n"
                                           "called TreeItem.text with arg 0\n")

    def test_replace_listbox_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.replace_listbox_item
        """
        listbox = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.replace_listbox_item(listbox, item, 'cmdtext')
        assert capsys.readouterr().out == "called TreeItem.setText with args (1, 'cmdtext')\n"

    def test_ensure_listitem_visible(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.ensure_listitem_visible
        """
        def mock_index(arg):
            print(f'called Tree.indexFromItem with arg `{item}`')
            return 2
        listbox = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        listbox.indexFromItem = mock_index
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ensure_listitem_visible(listbox, item)
        assert capsys.readouterr().out == (
                f"called Tree.indexFromItem with arg `{item}`\n"
                "called Tree.scrollToItem with arg `2`\n")

    def test_remove_listbox_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.remove_listbox_item
        """
        listbox = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_listbox_item(listbox, item)
        assert capsys.readouterr().out == (
                f"called Tree.indexOfTopLevelItem with arg `{item}`\n"
                "called Tree.takeTopLevelItem with arg `index`\n")

    def test_reset_listitem_icon(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.reset_listitem_icon
        """
        def mock_item(arg):
            print(f'called Tree.topLevelItem with arg `{arg}`')
            return item
        listbox = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        listbox.topLevelItem = mock_item
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.todoicon = 'todoicon'
        testobj.reset_listitem_icon(listbox, 'ix')
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `ix`\n"
                                           "called TreeItem.setIcon with args (0, 'todoicon')\n")

    def test_set_focus_to(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.set_focus_to
        """
        widget = mockqtw.MockWidget()
        assert capsys.readouterr().out == "called Widget.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_focus_to(widget)
        assert capsys.readouterr().out == "called Widget.setFocus\n"

    def test_popuptext(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.popuptext
        """
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.popuptext(item, 'colno')
        assert capsys.readouterr().out == ""
        testobj.popuptext(item, 1)
        assert capsys.readouterr().out == ("called TreeItem.text with arg 1\n"
                                           "called TreeItem.setTooltip with args (1, None)\n")

    def test_get_entry_text(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_entry_text
        """
        def mock_text():
            return 'text'
        win = types.SimpleNamespace(text=mock_text)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_entry_text(win) == "text"
        assert capsys.readouterr().out == ("")

    def test_get_search_choice(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_search_choice
        """
        def mock_current():
            print('called Tree.currentIndex')
            return 'current'
        control = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        control.currentIndex = mock_current
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_search_choice(control) == "current"
        assert capsys.readouterr().out == "called Tree.currentIndex\n"

    def test_find_listitems(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.find_listitems
        """
        win = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.find_listitems(win, 'search') == []
        assert capsys.readouterr().out == ("called Tree.findItems with args"
                                           " ('search', <MatchFlag.MatchContains: 1>, 1)\n")
        assert testobj.find_listitems(win, 'search', in_col=0) == []
        assert capsys.readouterr().out == ("called Tree.findItems with args"
                                           " ('search', <MatchFlag.MatchContains: 1>, 0)\n")

    def test_get_selected_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_selected_item
        """
        def mock_current():
            print('called Tree.currentItem')
            return 'current'
        win = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        win.currentItem = mock_current
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_selected_item(win) == "current"
        assert capsys.readouterr().out == ("called Tree.currentItem\n")

    def test_get_first_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_first_item
        """
        win = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        win = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_first_item(win) == "Tree.topLevelItem"
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `0`\n")

    def test_get_last_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_last_item
        """
        win = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        win = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_last_item(win) == "Tree.topLevelItem"
        assert capsys.readouterr().out == ("called Tree.topLevelItemCount\n"
                                           "called Tree.topLevelItem with arg `-1`\n")

    def test_get_item_text(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.get_item_text
        """
        win = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem('x', 'y')
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ('x', 'y')\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.get_item_text(win, item, 1) == "y"
        assert capsys.readouterr().out == ("called TreeItem.text with arg 1\n")

    def test_set_selected_item(self, monkeypatch, capsys):
        """unittest for MergeDialogGui.set_selected_item
        """
        win = mockqtw.MockTreeWidget()
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_selected_item(win, item)
        assert capsys.readouterr().out == (f"called Tree.setCurrentItem with arg `{item}`\n")
