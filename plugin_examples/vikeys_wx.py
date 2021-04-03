"""VI plugin for Hotkeys - gui specific functions - wxPython version
"""
import wx


def add_extra_fields(win, box):
    """add fields specific to this plugin
    """
    win.pre_parms_label = wx.StaticText(box)
    win.pre_parms_text = wx.TextCtrl(box)
    win.screenfields.append(win.pre_parms_text)
    win.post_parms_label = wx.StaticText(box)
    win.post_parms_text = wx.TextCtrl(box)
    win.screenfields.append(win.post_parms_text)
    win.feature_label = wx.StaticText(box)
    win.feature_select = wx.ComboBox(box, style=wx.CB_READONLY, choices=win.master.featurelist)
    win.screenfields.append(win.feature_select)


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
