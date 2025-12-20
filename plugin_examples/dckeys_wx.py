"""Hotkeys plugin voor Double Commander - wx specifieke code
"""
import wx


def layout_extra_fields(win, layout):
    """add the extra fields to the layout
    """
    sizer = wx.FlexGridSizer(2, 2, 2)
    # line = 0
    sizer.Add(win.lbl_parms, 0, wx.ALIGN_CENTER_VERTICAL)
    sizer.Add(win.txt_parms, 1, wx.EXPAND)
    # line += 1
    sizer.Add(win.lbl_controls, 0, wx.ALIGN_CENTER_VERTICAL)
    sizer.Add(win.cmb_controls, 1, wx.EXPAND)
    layout.Add(sizer, 0, wx.LEFT, 5)
