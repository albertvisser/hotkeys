"""unittests for ./editor/plugins/dckeys_qt.py
"""
import types
from editor.plugins import dckeys_qt as testee
from mockgui import mockqtwidgets as mockqtw

def test_layout_extra_fieldst(monkeypatch, capsys):
    """testmethode voor dckey_qt.layout_extra_fields
    """
    monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    win = types.SimpleNamespace()
    win.lbl_parms = mockqtw.MockLabel()
    win.txt_parms = mockqtw.MockLineEdit()
    win.lbl_controls = mockqtw.MockLabel()
    win.cmb_controls = mockqtw.MockComboBox()
    layout = mockqtw.MockVBoxLayout()
    assert capsys.readouterr().out == ("called Label.__init__\ncalled LineEdit.__init__\n"
                                       "called Label.__init__\ncalled ComboBox.__init__\n"
                                       "called VBox.__init__\n")
    testee.layout_extra_fields(win, layout)
    assert capsys.readouterr().out == (
            "called Grid.__init__\n"
            "called Grid.addWidget with arg of type"
            " <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)\n"
            "called Grid.addWidget with arg of type"
            " <class 'mockgui.mockqtwidgets.MockLineEdit'> at (0, 1)\n"
            "called Grid.addWidget with arg of type"
            " <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0)\n"
            "called HBox.__init__\n"
            "called HBox.addWidget with arg of type"
            " <class 'mockgui.mockqtwidgets.MockComboBox'>\n"
            "called HBox.addStretch\n"
            "called Grid.addLayout with arg of type"
            " <class 'mockgui.mockqtwidgets.MockHBoxLayout'> at (1, 1)\n"
            "called VBox.addLayout with arg of type"
            " <class 'mockgui.mockqtwidgets.MockGridLayout'>\n")


def build_testobj(monkeypatch, capsys):
    """create stub for dckey_qt.DCCompleteDialog
    """
    # class MockCompleteDialog:
    #     """stub for dialogs_qt.CompleteDialog object
    #     """
    #     def mock_init(self):
    #         print("called CompleteDialog.__init__")
    def mock_init(self, *args):
        print("called DcCompleteDialog.__init__ with args", args)
        self.parent, self.master = args
    # monkeypatch.setattr(testee, 'CompleteDialog', MockCompleteDialog)
    monkeypatch.setattr(testee.DcCompleteDialog, '__init__', mock_init)
    parent = types.SimpleNamespace()
    master = types.SimpleNamespace()
    testobj = testee.DcCompleteDialog(parent, master)
    assert capsys.readouterr().out == (
            f"called DcCompleteDialog.__init__ with args ({parent}, {master})\n")
    return testobj


def test_read_data(monkeypatch, capsys):
    """testmethode voor dckey_qt.DCCompleteDialog.read_data
    """
    testobj = build_testobj(monkeypatch, capsys)
    testobj.master.dialog_data = {'descdict': {}, 'cmddict': {}}
    testobj.read_data()
    assert testobj.cmds == {}
    assert testobj.desc == {}
    testobj.master.dialog_data = {'descdict': {'a': 'x', 'b': '', 'c': 'y'},
                                  'cmddict': {'a': 'q', 'd': '', 'e': 'z'}}
    testobj.read_data()
    assert testobj.cmds == {'a': 'x', 'b': '', 'c': 'y', 'd': ''}
    assert testobj.desc == {'a': 'q', 'd': '', 'e': 'z', 'b': ''}


def test_build_table(monkeypatch, capsys):
    """testmethode voor dckey_qt.DCCompleteDialog.build_table
    """
    monkeypatch.setattr(testee.qtw, 'QTableWidgetItem', mockqtw.MockTableItem)
    testobj = build_testobj(monkeypatch, capsys)
    testobj.cmds = {'x': 'yyy', 'a': 'bbb'}
    testobj.p0list = mockqtw.MockTable()
    assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                       "called Header.__init__\n""called Header.__init__\n")
    testobj.build_table()
    assert capsys.readouterr().out == ("called TableItem.__init__ with arg ''\n"
                                       "called TableItem.setText with arg 'a'\n"
                                       "called Table.setItem with args (0, 0, item of type"
                                       " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                                       "called TableItem.__init__ with arg ''\n"
                                       "called TableItem.setText with arg 'bbb'\n"
                                       "called Table.setItem with args (0, 1, item of type"
                                       " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                                       "called TableItem.__init__ with arg ''\n"
                                       "called TableItem.setText with arg 'x'\n"
                                       "called Table.setItem with args (1, 0, item of type"
                                       " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                                       "called TableItem.__init__ with arg ''\n"
                                       "called TableItem.setText with arg 'yyy'\n"
                                       "called Table.setItem with args (1, 1, item of type"
                                       " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n")
