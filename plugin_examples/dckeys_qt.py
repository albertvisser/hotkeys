"""Hotkeys plugin voor Double Commander - qt specifieke code
"""
import PyQt6.QtWidgets as qtw


def layout_extra_fields(win, layout):
    """add the extra fields to the layout
    """
    sizer2 = qtw.QGridLayout()
    line = 0
    sizer2.addWidget(win.lbl_parms, line, 0)
    sizer2.addWidget(win.txt_parms, line, 1)
    line += 1
    sizer2.addWidget(win.lbl_controls, line, 0)
    sizer3 = qtw.QHBoxLayout()
    sizer3.addWidget(win.cmb_controls)
    sizer3.addStretch()
    sizer2.addLayout(sizer3, line, 1)
    layout.addLayout(sizer2, 1)
