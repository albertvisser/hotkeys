"""unittests for ./editor/plugins/dckeys_qt.py
"""
import types
from editor.plugins import dckeys_qt as testee
from mockgui import mockqtwidgets as mockqtw

def test_layout_extra_fields(monkeypatch, capsys):
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
            "called Grid.addWidget with arg MockLabel at (0, 0)\n"
            "called Grid.addWidget with arg MockLineEdit at (0, 1)\n"
            "called Grid.addWidget with arg MockLabel at (1, 0)\n"
            "called HBox.__init__\n"
            "called HBox.addWidget with arg MockComboBox\n"
            "called HBox.addStretch\n"
            "called Grid.addLayout with arg MockHBoxLayout at (1, 1)\n"
            "called VBox.addLayout with arg MockGridLayout\n")
