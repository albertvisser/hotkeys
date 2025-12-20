import types
from editor.plugins import vikeys_wx as testee
from mockgui import mockwxwidgets as mockwx


def test_layout_extra_fields_topline(monkeypatch, capsys):
    """unittest for vikeys_wx.layout_extra_fields_topline
    """
    monkeypatch.setattr(testee.wx, 'BoxSizer', mockwx.MockBoxSizer)
    layout = mockwx.MockBoxSizer('')
    win = types.SimpleNamespace(pre_parms_label='pre_label', pre_parms_text='pre_text',
                                post_parms_label='post_label', post_parms_text='post_text',
                                feature_label='feat_label', feature_select='feat_select')
    testee.layout_extra_fields_topline(win, layout)
    assert capsys.readouterr().out == (
            "called BoxSizer.__init__ with args ('',)\n"
            "called BoxSizer.__init__ with args (4,)\n"
            "called hori sizer.Add with args ('pre_label',"
            f" 0, {testee.wx.ALIGN_CENTER_VERTICAL | testee.wx.LEFT | testee.wx.RIGHT}, 2)\n"
            "called hori sizer.Add with args ('pre_text',"
            f" 0, {testee.wx.ALIGN_CENTER_VERTICAL | testee.wx.RIGHT}, 2)\n"
            "called hori sizer.Add with args ('post_label',"
            f" 0, {testee.wx.ALIGN_CENTER_VERTICAL | testee.wx.LEFT | testee.wx.RIGHT}, 2)\n"
            "called hori sizer.Add with args ('post_text',"
            f" 0, {testee.wx.ALIGN_CENTER_VERTICAL | testee.wx.RIGHT}, 2)\n"
            "called hori sizer.Add with args ('feat_label',"
            f" 0, {testee.wx.ALIGN_CENTER_VERTICAL | testee.wx.LEFT | testee.wx.RIGHT}, 2)\n"
            "called hori sizer.Add with args ('feat_select',"
            f" 0, {testee.wx.ALIGN_CENTER_VERTICAL | testee.wx.RIGHT}, 2)\n"
            f"called  sizer.Add with args MockBoxSizer (0, {testee.wx.LEFT}, 2)\n")
