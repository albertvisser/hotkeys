"""VI plugin for Hotkeys - gui specific functions - Qt version
"""
import PyQt6.QtWidgets as qtw


def layout_extra_fields_topline(win, box):
    "add the specific fields to the layout"
    sizer = qtw.QHBoxLayout()
    sizer.addWidget(win.pre_parms_label)
    sizer.addWidget(win.pre_parms_text)
    sizer.addWidget(win.post_parms_label)
    sizer.addWidget(win.post_parms_text)
    sizer.addWidget(win.feature_label)
    sizer.addWidget(win.feature_select)
    box.addLayout(sizer)
