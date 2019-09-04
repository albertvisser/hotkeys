"""VI plugin for Hotkeys - gui specific functions - wxPython version
"""
import wx


def add_extra_fields(win, box):
    """add fields specific to this plugin
    """
    win.pre_parms_label = wx.StaticText(box)
    win.pre_parms_text = wx.TextCtrl(box)
    win.screenfields.append(win.pre_parms_text)
    win.ix_pre_parms = 1
    win.post_parms_label = wx.StaticText(box)
    win.post_parms_text = wx.TextCtrl(box)
    win.screenfields.append(win.post_parms_text)
    win.ix_post_parms = 2
    win.feature_label = wx.StaticText(box)
    win.feature_select = wx.ComboBox(box, style=wx.CB_READONLY, choices=win.master.featurelist)
    win.screenfields.append(win.feature_select)
    win.ix_feature_select = 3


# def get_frameheight():
#     "return the height for the descriptions field"
#     return x
def layout_extra_fields_topline(win, box):
    "add the specific fields to the layout"
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(win.pre_parms_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
    sizer.Add(win.pre_parms_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 2)
    sizer.Add(win.post_parms_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
    sizer.Add(win.post_parms_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 2)
    sizer.Add(win.feature_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
    sizer.Add(win.feature_select, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 2)
    box.Add(sizer, 0, wx.LEFT, 2)


def captions_extra_fields(win):
    "for plugin-specific fields, change the captions according to the language setting"
    # win.fieldname.setText(win.captions['some_value'])
    win.pre_parms_label.SetLabel(win.master.captions['C_BPARMS'] + ':')
    win.post_parms_label.SetLabel(win.master.captions['C_APARMS'] + ':')
    win.feature_label.SetLabel(win.master.captions['C_FEAT'] + ':')
