"""Hotkeys plugin example

this module contains the gui-toolkit specific part (in this case, for wxPython)
"""
# import wx

# uncomment these to define routines to be used by methods of a HotKeyPanel instance
# ** corresponds to the ShowDetails setting **
# win is a reference to the HotKeyPanel instance
# box is a reference to the frame containing the screen fields

# def add_extra_fields(win, box):
#     """add fields specific to this plugin
#     """
#     win.fieldlabel = wx.StaticText(box)
#     win.fieldentry = wx.TextCtrl(box)   # or ComboBox etc
#     win.screenfields.append(win.fieldentry)
#     win_ix_field = 1  # number accordingly


# def get_frameheight():
#     "return the height for the descriptions field if different from the default"
#     return x


# def layout_extra_fields_topline(win, box):
#     """add the specific fields to the layout
#     """
#     use this if you want to use the screen line the `keys` field is on
#     sizer = wx.BoxSizer(wx.HORIZONTAL)
#     sizer.Add(win.fieldlabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
#     sizer.Add(win.fieldname, wx.RIGHT, 2)
#     box.Add(sizer, 0, wx.LEFT, 2)


# def layout_extra_fields_nextline(win, box):
#     """add the specific fields to the layout
#     """
#     use this if you want to make a new line above the description field
#     sizer = wx.BoxSizer(wx.HORIZONTAL)
#     sizer.Add(win.fieldlabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
#     sizer.Add(win.fieldname, wx.RIGHT, 2)
#     box.Add(sizer, 0, wx.LEFT, 2)


# def layout_extra_fields(win, box):
#     """add the specific fields to the layout
#     """
#     use this if you want to put them next to the description field
#     adjust the desc field's height accordingly using `get_frameheight`
#     sizer = wx.BoxSizer(wx.VERTICAL)
#     sizer.Add(win.fieldlabel, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 2)
#     sizer.Add(win.fieldname, wx.RIGHT, 2)
#     box.Add(sizer, 0, wx.LEFT, 2)


# def captions_extra_fields(win):
#     "for plugin-specific fields, change the captions according to the language setting"
#     win.fieldlabel.setText(win.captions['some_value'] + ':')

