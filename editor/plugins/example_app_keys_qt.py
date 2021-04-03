"""Hotkeys plugin example

this module contains the gui-toolkit specific part (in this case, for PyQT5)
"""
# import PyQt5.QtWidgets as qtw
# import PyQt5.QtGui as gui
# import PyQt5.QtCore as core

# uncomment these to define routines to be used by methods of a HotKeyPanel instance
# ** corresponds to the ShowDetails setting **
# win is a reference to the HotKeyPanel instance
# box is a reference to the frame containing the screen fields

# def get_frameheight():
#     "return the height for the descriptions field if different from the default"
#     return x


# def layout_extra_fields_topline(win, box):
#     """add the specific fields to the layout
#     """
#     use this if you want to use the screen line the `keys` field is on
#     sizer = qtw.QHBoxLayout()
#     sizer.addWidget(win.fieldlabel)
#     sizer.addWidget(win.fieldentry)
#     box.addLayout(sizer)


# def layout_extra_fields_nextline(win, box):
#     """add the specific fields to the layout
#     """
#     use this if you want to make a new line above the description field
#     sizer = qtw.QHBoxLayout()
#     sizer.addWidget(win.fieldlabel)
#     sizer.addWidget(win.fieldentry)
#     box.addLayout(sizer)


# def layout_extra_fields(win, box):
#     """add the specific fields to the layout
#     """
#     use this if you want to put them next to the description field
#     adjust the desc field's height accordingly using `get_frameheight`
#     sizer = qtw.QVBoxLayout()
#     sizer.addWidget(win.fieldlabel)
#     sizer.addWidget(win.fieldentry)
#     box.addLayout(sizer)
