"""VI plugin for Hotkeys - gui specific functions - wxPython version
"""
import wx


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
