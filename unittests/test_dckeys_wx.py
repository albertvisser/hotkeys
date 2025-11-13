import types
from editor.plugins import dckeys_wx as testee
from mockgui import mockwxwidgets as mockwx


def test_layout_extra_fields(monkeypatch, capsys):
    """testmethode voor dckey_wx.layout_extra_fields
    """
    monkeypatch.setattr(testee.wx, 'FlexGridSizer', mockwx.MockFlexGridSizer)
    layout = mockwx.MockBoxSizer('')
    win = types.SimpleNamespace(lbl_parms='parms', txt_parms='parmstxt', lbl_controls='controls',
                                cmb_controls='combobox')
    testee.layout_extra_fields(win, layout)
    assert capsys.readouterr().out == (
            "called BoxSizer.__init__ with args ('',)\n"
            "called FlexGridSizer.__init__ with args (2, 2, 2) {}\n"
            f"called FlexGridSizer.Add with args <item> (0, {testee.wx.ALIGN_CENTER_VERTICAL})\n"
            f"called FlexGridSizer.Add with args <item> (1, {testee.wx.EXPAND})\n"
            f"called FlexGridSizer.Add with args <item> (0, {testee.wx.ALIGN_CENTER_VERTICAL})\n"
            f"called FlexGridSizer.Add with args <item> (1, {testee.wx.EXPAND})\n"
            f"called  sizer.Add with args <item> (0, {testee.wx.LEFT}, 5)\n")
