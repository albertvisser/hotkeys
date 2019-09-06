"""VI plugin for Hotkeys - gui specific functions - Qt5 version
"""
import PyQt5.QtWidgets as qtw


def add_extra_fields(win, box):
    """add fields specific to this plugin
    """
    win.pre_parms_label = qtw.QLabel(box)
    win.pre_parms_text = qtw.QLineEdit(box)
    win.screenfields.append(win.pre_parms_text)
    win.ix_pre_parms = 1
    win.post_parms_label = qtw.QLabel(box)
    win.post_parms_text = qtw.QLineEdit(box)
    win.screenfields.append(win.post_parms_text)
    win.ix_post_parms = 2
    win.feature_label = qtw.QLabel(box)
    win.feature_select = qtw.QComboBox(box)
    win.feature_select.addItems(win.master.featurelist)
    win.screenfields.append(win.feature_select)
    win.ix_feature_select = 3


# def get_frameheight():
#     "return the height for the descriptions field"
#     return x
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
