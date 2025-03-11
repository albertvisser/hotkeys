"""unittests for ./editor/plugins/gtkaccel_keys_qt.py
"""
import types
from editor.plugins import gtkaccel_keys_qt as qttestee
from mockgui import mockqtwidgets as mockqtw


class TestAccelCompleteDialog:
    """unittests for gtkaccel_keys_qt.AccelCompleteDialog object
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gtkaccel_keys_qt.AccelCompleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        # monkeypatch.setattr(qttestee.qtw, 'QDialog', mockqtw.MockDialog)
        monkeypatch.setattr(qttestee.qtw.QWidget, '__init__', mockqtw.MockWidget.__init__)
        monkeypatch.setattr(qttestee.CompleteDialog, '__init__', mockqtw.MockDialog.__init__)
        parent = qttestee.qtw.QWidget()
        master = types.SimpleNamespace()
        testobj = qttestee.AccelCompleteDialog(parent, master)
        testobj.parent = parent
        testobj.master = master
        assert capsys.readouterr().out == (
                "called Widget.__init__\n"
                f"called Dialog.__init__ with args {parent} ({master},) {{}}\n")
        return testobj

    def test_read_data(self, monkeypatch, capsys):
        """unittest for AccelCompleteDialog.read_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(dialog_data={'descdict': {'desc': 'dict'},
                                                            'actions': {'act': 'ions'}})
        testobj.read_data()
        assert testobj.desc == {'desc': 'dict'}
        assert testobj.cmds == {'act': 'ions'}

    def test_build_table(self, monkeypatch, capsys):
        """unittest for AccelCompleteDialog.build_table
        """
        def mock_settext(self, arg):
            "stub"
            print(f"called TableItem.setText with arg '{arg}'")
            if isinstance(arg, tuple):
                raise TypeError

        monkeypatch.setattr(qttestee.qtw, 'QTableWidgetItem', mockqtw.MockTableItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.cmds = {}
        testobj.p0list = mockqtw.MockTable()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n")
        testobj.build_table()
        assert testobj.cmds == {}
        assert capsys.readouterr().out == ""
        testobj.cmds = {'xxx': 'yyy', 'aaa': 'bbb'}
        testobj.desc = {'bbb': 'aaadesc'}
        testobj.build_table()
        assert testobj.cmds == {'bbb': 'aaa', 'yyy': 'xxx'}
        assert capsys.readouterr().out == ("called TableItem.__init__ with arg ''\n"
                                           "called TableItem.setText with arg 'bbb'\n"
                                           "called Table.setItem with args (0, 0, item of type"
                                           " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                                           "called TableItem.__init__ with arg ''\n"
                                           "called TableItem.setText with arg ''\n"
                                           "called Table.setItem with args (0, 1, item of type"
                                           " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                                           "called TableItem.__init__ with arg ''\n"
                                           "called TableItem.setText with arg 'yyy'\n"
                                           "called Table.setItem with args (1, 0, item of type"
                                           " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                                           "called TableItem.__init__ with arg ''\n"
                                           "called TableItem.setText with arg ''\n"
                                           "called Table.setItem with args (1, 1, item of type"
                                           " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n")
        monkeypatch.setattr(mockqtw.MockTableItem, 'setText', mock_settext)
        testobj.cmds = {'xxx': ('yyy', 'zzz'), 'qqq': ('rrr', 'sss')}
        testobj.desc = {('yyy', 'zzz'): 'xxxdesc'}
        testobj.build_table()
        assert testobj.cmds == {('rrr/sss'): 'qqq', ('yyy/zzz'): 'xxx'}
        assert capsys.readouterr().out == ("called TableItem.__init__ with arg ''\n"
                                           "called TableItem.setText with arg '('rrr', 'sss')'\n"
                                           "called TableItem.setText with arg 'rrr/sss'\n"
                                           "called Table.setItem with args (0, 0, item of type"
                                           " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                                           "called TableItem.__init__ with arg ''\n"
                                           "called TableItem.setText with arg ''\n"
                                           "called Table.setItem with args (0, 1, item of type"
                                           " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                                           "called TableItem.__init__ with arg ''\n"
                                           "called TableItem.setText with arg '('yyy', 'zzz')'\n"
                                           "called TableItem.setText with arg 'yyy/zzz'\n"
                                           "called Table.setItem with args (1, 0, item of type"
                                           " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                                           "called TableItem.__init__ with arg ''\n"
                                           "called TableItem.setText with arg ''\n"
                                           "called Table.setItem with args (1, 1, item of type"
                                           " <class 'mockgui.mockqtwidgets.MockTableItem'>)\n")
