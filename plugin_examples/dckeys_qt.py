"""Hotkeys plugin voor Double Commander - qt specifieke code
"""
import PyQt6.QtWidgets as qtw


def layout_extra_fields(win, layout):
    """add the extra fields to the layout
    """
    sizer = qtw.QGridLayout()
    line = 0
    sizer.addWidget(win.lbl_parms, line, 0)
    sizer.addWidget(win.txt_parms, line, 1)
    line += 1
    sizer.addWidget(win.lbl_controls, line, 0)
    sizer.addWidget(win.cmb_controls, line, 1)
    layout.addLayout(sizer)
