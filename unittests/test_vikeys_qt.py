from editor.plugins import vikeys_qt as testee
from mockgui import mockqtwidgets as mockqtw


def test_layout_extra_fields_topline_qt(monkeypatch, capsys):
    """unittest for vikeys_qt.layout_extra-fields_topline
    """
    monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
    win = mockqtw.MockWidget()
    win.pre_parms_label = mockqtw.MockLabel()
    win.pre_parms_text = mockqtw.MockLineEdit()
    win.post_parms_label = mockqtw.MockLabel()
    win.post_parms_text = mockqtw.MockLineEdit()
    win.feature_label = mockqtw.MockLabel()
    win.feature_select = mockqtw.MockComboBox()
    box = mockqtw.MockVBoxLayout()
    assert capsys.readouterr().out == ("called Widget.__init__\n"
                                       "called Label.__init__\ncalled LineEdit.__init__\n"
                                       "called Label.__init__\ncalled LineEdit.__init__\n"
                                       "called Label.__init__\ncalled ComboBox.__init__\n"
                                       "called VBox.__init__\n")
    testee.layout_extra_fields_topline(win, box)
    assert capsys.readouterr().out == (
            "called HBox.__init__\n"
            "called HBox.addWidget with arg MockLabel\n"
            "called HBox.addWidget with arg MockLineEdit\n"
            "called HBox.addWidget with arg MockLabel\n"
            "called HBox.addWidget with arg MockLineEdit\n"
            "called HBox.addWidget with arg MockLabel\n"
            "called HBox.addWidget with arg MockComboBox\n"
            "called VBox.addLayout with arg MockHBoxLayout\n")
