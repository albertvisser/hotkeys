"""unittests for ./editor/dialogs_qt.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from editor import dialogs_qt as testee

initialtool = """\
called Dialog.__init__ with args None () {{}}
called Dialog.setWindowTitle with args ('a title',)
called VBox.__init__
called Label.__init__ with args ('', {testobj})
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.__init__
called RadioButton.__init__ with args ('', {testobj}) {{}}
called RadioButton.setChecked with arg `False`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called ComboBox.__init__
called ComboBox.addItems with arg ['p', 'p']
called ComboBox.setEditable with arg `True`
called ComboBox.setCurrentIndex with arg `0`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called RadioButton.__init__ with args ('', {testobj}) {{}}
called RadioButton.setChecked with arg `False`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockRadioButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called ButtonBox.__init__ with args ()
called ButtonBox.addButton with args (1,)
called ButtonBox.addButton with args (2,)
called Signal.connect with args ({testobj.accept},)
called Signal.connect with args ({testobj.reject},)
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
filebrowse = """\
called Frame.__init__
called Frame.setWindowTitle wth arg '{title}'
called Frame.setFrameStyle with arg `34`
called VBox.__init__
called HBox.__init__
called LineEdit.__init__
called LineEdit.setMinimumWidth with arg `200`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called PushButton.__init__ with args ('xxx', {testobj}) {{'clicked': {testobj.browse}}}
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
"""
setup = """\
called Frame.__init__
called Dialog.__init__ with args None () {{}}
called Dialog.setWindowTitle with args ('T_INIKDEF',)
called Grid.__init__
called Label.__init__ with args ('T_NAMOF s_plgnam T_ISMADE', {testobj})
called LineEdit.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (1, 0, 1, 3)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 3)
called Label.__init__ with args ('S_PNLNAM', {testobj})
called LineEdit.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (2, 0, 1, 3)
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (2, 3)
called CheckBox.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at (3, 0, 1, 4)
called CheckBox.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at (4, 0, 1, 4)
called CheckBox.__init__
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'> at (5, 0, 1, 4)
called Label.__init__ with args ('Q_SAVLOC', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (6, 0, 1, 2)
called gui.FileBrowseButton with args ({testobj},) {{'text': 'editor/plugins/Name_hotkeys.json', 'level_down': True}}
called Grid.addWidget with arg of type <class 'test_dialogs_qt.TestSetupDialog.test_init.<locals>.MockFileBrowseButton'> at (6, 2, 1, 3)
called ButtonBox.__init__ with args ()
called ButtonBox.addButton with args (1,)
called ButtonBox.addButton with args (2,)
called Signal.connect with args ({testobj.accept},)
called Signal.connect with args ({testobj.reject},)
called VBox.__init__
called VBox.addStretch
called HBox.__init__
called HBox.addStretch
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called VBox.addStretch
called Dialog.setLayout
"""
delete = """\
called Frame.__init__
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('title',)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('xxx', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called CheckBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called CheckBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called ButtonBox.__init__ with args ()
called ButtonBox.addButton with args (1,)
called ButtonBox.addButton with args (2,)
called Signal.connect with args ({testobj.accept},)
called Signal.connect with args ({testobj.reject},)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>
called Dialog.setLayout
"""
files = """\
called Frame.__init__
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.resize with args (680, 400)
called Dialog.setWindowTitle with args ('title',)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('xxx', {testobj})
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('yyy', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>, kwargs {{'alignment': <PyQt5.QtCore.Qt.Alignment object at 0x7a29459e62e0>}}
called HBox.addSpacing
called Label.__init__ with args ('zzz', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>, kwargs {{'alignment': 128}}
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.__init__
called ScrollArea.__init__ with args ({testobj},)
called ScrollArea.setWidget with arg of type `<class 'mockgui.mockqtwidgets.MockFrame'>`
called ScrollArea.setWidgetResizable with arg `True`
called ScrollArea.verticalScrollBar
called Grid.__init__
called FilesDialog.add_row with args ({testobj}, 'name', 'path')
called VBox.__init__
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called VBox.addStretch
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockScrollArea'>
called ButtonBox.__init__ with args ()
called ButtonBox.addButton with args ('aaa', 9)
called PushButton.__init__ with args () {{}}
called Signal.connect with args ({testobj.add_program},)
called ButtonBox.addButton with args ('bbb', 9)
called PushButton.__init__ with args () {{}}
called Signal.connect with args ({testobj.remove_programs},)
called ButtonBox.addButton with args (1,)
called PushButton.__init__ with args () {{}}
called ButtonBox.addButton with args (2,)
called PushButton.__init__ with args () {{}}
called Signal.connect with args ({testobj.accept},)
called Signal.connect with args ({testobj.reject},)
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
columns = """\
called Frame.__init__
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('title',)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('COLSET XXX', {testobj})
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('TTL', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>, kwargs {{'alignment': <PyQt5.QtCore.Qt.Alignment object at 0x74690d32c050>}}
called HBox.addSpacing
called Label.__init__ with args ('WID', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>, kwargs {{'alignment': 128}}
called HBox.addSpacing
called Label.__init__ with args ('IND', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>, kwargs {{'alignment': 128}}
called Label.__init__ with args ('SEQ', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>, kwargs {{'alignment': 128}}
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.__init__
called ScrollArea.__init__ with args ({testobj},)
called ScrollArea.setWidget with arg of type `<class 'mockgui.mockqtwidgets.MockFrame'>`
called ScrollArea.setAlignment with arg 64
called ScrollArea.setWidgetResizable with arg `True`
called ScrollArea.verticalScrollBar
called VBox.__init__
called ColumsSettingsDialog.add_row with args ({testobj}, 'xxx', 5, 0, 0)
called ColumsSettingsDialog.add_row with args ({testobj}, 'yyy', 10, 1, 1)
called VBox.__init__
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called VBox.addStretch
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockScrollArea'>
called ButtonBox.__init__ with args ()
called ButtonBox.addButton with args ('ADDCOL', 9)
called PushButton.__init__ with args () {{}}
called Signal.connect with args ({testobj.add_column},)
called ButtonBox.addButton with args ('REMCOL', 9)
called PushButton.__init__ with args () {{}}
called Signal.connect with args ({testobj.remove_columns},)
called ButtonBox.addButton with args (1,)
called PushButton.__init__ with args () {{}}
called ButtonBox.addButton with args (2,)
called PushButton.__init__ with args () {{}}
called Signal.connect with args ({testobj.accept},)
called Signal.connect with args ({testobj.reject},)
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
addcol_1 = """\
called CheckBox.__init__
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called ComboBox.__init__
called ComboBox.addItems with arg ['xxx', 'yyy']
called ComboBox.setEditable with arg `True`
"""
addcol_2a = """\
called ComboBox.clearEditText
"""
addcol_2b = """\
called ComboBox.setCurrentIndex with arg `0`
"""
addcol_3 = """\
called Signal.connect with args ({testobj.on_text_changed},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called HBox.__init__
called HBox.addSpacing
called SpinBox.__init__
called SpinBox.setMaximum with arg '999'
"""
addcol_3b = """\
called SpinBox.setValue with arg '5'
"""
addcol_4 = """\
called SpinBox.setFixedWidth with arg '48'
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockSpinBox'>
called HBox.addSpacing
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addSpacing
called CheckBox.__init__
called CheckBox.setChecked with arg {flag}
called CheckBox.setFixedWidth with arg '32'
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called HBox.addSpacing
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addSpacing
called SpinBox.__init__
called SpinBox.setMinimum with arg '1'
called SpinBox.setMaximum with arg '99'
called SpinBox.setValue with arg '2'
called SpinBox.setFixedWidth with arg '36'
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockSpinBox'>
called HBox.addStretch
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Scrollbar.maximum
called Scrollbar.setMaximum with value `161`
called Scrollbar.maximum
called Scrollbar.setValue with value `99`
"""
newcols_start = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('title',)
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('xxx\\nyyy', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Grid.__init__
called Label.__init__ with args ('text id', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 0)
called Label.__init__ with args ('En', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 1)
called Label.__init__ with args ('Nl', {testobj})
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'> at (0, 2)
"""
newcols_middle = """\
called LineEdit.__init__
called LineEdit.setText with arg `Q0`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 0)
called LineEdit.__init__
called LineEdit.setEnabled with arg False
called LineEdit.setText with arg `qq`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 1)
called LineEdit.__init__
called LineEdit.setText with arg `qq`
called Grid.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 2)
"""
newcols_end = """\
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called ButtonBox.__init__ with args ()
called ButtonBox.addButton with args (1,)
called ButtonBox.addButton with args (2,)
called Signal.connect with args ({testobj.accept},)
called Signal.connect with args ({testobj.reject},)
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
extra_start = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.setWindowTitle with args ('title',)
called VBox.__init__
called Frame.__init__
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('xxx', {testobj})
called LineEdit.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called Label.__init__ with args ('yyy', {testobj})
called LineEdit.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLineEdit'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called CheckBox.__init__{action}
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called CheckBox.__init__{action}
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called CheckBox.__init__{action}
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockCheckBox'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called Frame.setFrameStyle with arg `38`
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockFrame'>
called Frame.__init__
called VBox.__init__
called HBox.__init__
called Label.__init__ with args ('ddd', {testobj})
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('eee', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>, kwargs {{'alignment': {testee.core.Qt.AlignmentFlag.AlignHCenter!r}}}
called HBox.addSpacing
called Label.__init__ with args ('fff', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>, kwargs {{'alignment': {testee.core.Qt.AlignmentFlag.AlignHCenter!r}}}
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.__init__
called ScrollArea.__init__ with args ({testobj},)
called ScrollArea.setWidget with arg of type `<class 'mockgui.mockqtwidgets.MockFrame'>`
called ScrollArea.setWidgetResizable with arg `True`
called ScrollArea.verticalScrollBar
called Grid.__init__
"""
extra_middle = """\
called ExtraSettingsDialog.add_row with args ('PluginName', 'xxx', '')
called ExtraSettingsDialog.add_row with args ('PanelName', 'yyy', '')
called ExtraSettingsDialog.add_row with args ('RebuildData', '1', '')
called ExtraSettingsDialog.add_row with args ('RedefineKeys', '1', '')
called ExtraSettingsDialog.add_row with args ('ShowDetails', '1', '')
called ExtraSettingsDialog.add_row with args ('XYZ', 'xyz', 'xxyyzz')
called ExtraSettingsDialog.add_row with args ('ABC', 'abc', '')
"""
extra_end = """\
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockGridLayout'>
called Frame.setFrameStyle with arg `32`
called ScrollArea.ensureVisible with args (0, 0)
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockScrollArea'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('add', {testobj}) {{}}
called Signal.connect with args ({testobj.add_setting},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called PushButton.__init__ with args ('rem', {testobj}) {{}}
called Signal.connect with args ({testobj.remove_settings},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called Frame.setFrameStyle with arg `38`
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockFrame'>
called ButtonBox.__init__ with args ()
called ButtonBox.addButton with args (1,)
called ButtonBox.addButton with args (2,)
called Signal.connect with args ({testobj.accept},)
called Signal.connect with args ({testobj.reject},)
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
entry_start = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.resize with args (680, 400)
called Dialog.setWindowTitle with args ('title',)
called VBox.__init__
called HBox.__init__
called Table.__init__ with args ({testobj},)
called Header.__init__
called Header.__init__
called Table.setColumnCount with arg '2'
called Table.setHorizontalHeaderLabels with arg '['xxxx', 'yyyy']'
called Table.horizontalHeader
called Header.resizeSection for col 0 width 1
called Header.resizeSection for col 1 width 2
"""
entry_middle = """\
called Table.insertRow with arg '0'
called TableItem.__init__ with arg xy
called TableItem.settext with arg xx
called Table.setItem with args (0, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)
called TableItem.__init__ with arg xy
called TableItem.settext with arg yy
called Table.setItem with args (0, 1, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)
called Table.insertRow with arg '1'
called TableItem.__init__ with arg xy
called TableItem.settext with arg aa
called Table.setItem with args (1, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)
called TableItem.__init__ with arg xy
called TableItem.settext with arg bb
called Table.setItem with args (1, 1, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)
"""
entry_end = """\
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockTable'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addStretch
called ButtonBox.__init__ with args ()
called ButtonBox.addButton with args ('add', 9)
called PushButton.__init__ with args () {{}}
called Signal.connect with args ({testobj.add_key},)
called ButtonBox.addButton with args ('remove', 9)
called PushButton.__init__ with args () {{}}
called Signal.connect with args ({testobj.delete_key},)
called ButtonBox.addButton with args (1,)
called PushButton.__init__ with args () {{}}
called ButtonBox.addButton with args (2,)
called PushButton.__init__ with args () {{}}
called Signal.connect with args ({testobj.accept},)
called Signal.connect with args ({testobj.reject},)
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""
complete = """\
called Dialog.__init__ with args {testobj.parent} () {{}}
called Dialog.resize with args (680, 400)
called CompleteDialog.read_data
called Table.__init__ with args (3, 2, {testobj})
called Header.__init__
called Header.__init__
called shared.get_text with args ({testobj.parent}, 'C_CMD')
called shared.get_text with args ({testobj.parent}, 'C_DESC')
called Table.setHorizontalHeaderLabels with arg '[None, None]'
called Table.horizontalHeader
called Header.setStretchLastSection with arg True
called CompleteDialog.build_table
called Table.setColumnWidth with args (0, 260)
called VBox.__init__
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockTable'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called ButtonBox.__init__ with args ()
called ButtonBox.addButton with args (1,)
called ButtonBox.addButton with args (2,)
called Signal.connect with args ({testobj.accept},)
called Signal.connect with args ({testobj.reject},)
called HBox.__init__
called HBox.addStretch
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockButtonBox'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Dialog.setLayout
"""


@pytest.fixture
def expected_output():
    """Output expectations for dialogs_qt.py (__init__ methods)
    """
    return {'initialtool': initialtool, 'filebrowse': filebrowse, 'setup': setup,
            'delete': delete, 'files': files, 'columns': columns,
            'addcol1': addcol_1 + addcol_2a + addcol_3 + addcol_4,
            'addcol2': addcol_1 + addcol_2b + addcol_3 + addcol_3b + addcol_4,
            'newcols': newcols_start + newcols_end,
            'newcols2': newcols_start + newcols_middle + newcols_end,
            'extra': extra_start + extra_end, 'extra2': extra_start + extra_middle + extra_end,
            'entry': entry_start + entry_end, 'entry2': entry_start + entry_middle + entry_end,
            'complete': complete}


def mock_get_text(*args):
    "stub"
    print('called shared.get_text with args', args)
    return 'text'


def mock_get_title(*args):
    "stub"
    print('called shared.get_title with args', args)
    return 'title'


def mock_info(*args):
    "stub"
    print('called MessageBox.information with args', args)
    return testee.qtw.QMessageBox.StandardButton.Cancel


def mock_info_2(*args):
    "stub"
    print('called MessageBox.information with args', args)
    return testee.qtw.QMessageBox.StandardButton.Ok


def mock_question(*args):
    "stub"
    print('called MessageBox.question with args', args)
    return testee.qtw.QMessageBox.StandardButton.No


def mock_question_2(*args):
    "stub"
    print('called MessageBox.question with args', args)
    return testee.qtw.QMessageBox.StandardButton.Yes


def mock_question_3(*args):
    "stub"
    print('called MessageBox.question with args', args)
    return testee.qtw.QMessageBox.StandardButton.Cancel


def test_show_message(monkeypatch, capsys):
    """unittest for dialogs_qt.show_message
    """
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info)
    testee.show_message('win', message_id='xxx', text='yyy')
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', None)\n"
            "called shared.get_title with args ('win',)\n"
            "called MessageBox.information with args ('win', 'title', 'text')\n")
    testee.show_message('win', message_id='xxx', text='yyy', args={'aa': 'bbbb'})
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            "called MessageBox.information with args ('win', 'title', 'text')\n")


def test_show_cancel_message(monkeypatch, capsys):
    """unittest for dialogs_qt.show_cancel_message
    """
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info)
    assert not testee.show_cancel_message('win', message_id='xxx', text='yyy')
    buttons = testee.qtw.QMessageBox.StandardButton.Ok | testee.qtw.QMessageBox.StandardButton.Cancel
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', None)\n"
            "called shared.get_title with args ('win',)\n"
            f"called MessageBox.information with args ('win', 'title', 'text', {buttons!r})\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'information', mock_info_2)
    assert testee.show_cancel_message('win', message_id='xxx', text='yyy', args={'aa': 'bbbb'})
    buttons = testee.qtw.QMessageBox.StandardButton.Ok | testee.qtw.QMessageBox.StandardButton.Cancel
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            f"called MessageBox.information with args ('win', 'title', 'text', {buttons!r})\n")


def test_ask_question(monkeypatch, capsys):
    """unittest for dialogs_qt.ask_question
    """
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question)
    assert not testee.ask_question('win', message_id='xxx', text='yyy')
    buttons = testee.qtw.QMessageBox.StandardButton.Yes | testee.qtw.QMessageBox.StandardButton.No
    yesbutton = testee.qtw.QMessageBox.StandardButton.Yes
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', None)\n"
            "called shared.get_title with args ('win',)\n"
            f"called MessageBox.question with args ('win', 'title', 'text', {buttons!r},"
            f" {yesbutton!r})\n")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question_2)
    assert testee.ask_question('win', message_id='xxx', text='yyy', args={'aa': 'bbbb'})
    buttons = testee.qtw.QMessageBox.StandardButton.Yes | testee.qtw.QMessageBox.StandardButton.No
    yesbutton = testee.qtw.QMessageBox.StandardButton.Yes
    assert capsys.readouterr().out == (
            "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
            "called shared.get_title with args ('win',)\n"
            f"called MessageBox.question with args ('win', 'title', 'text', {buttons!r},"
            f" {yesbutton!r})\n")


def test_ask_ync_question(monkeypatch, capsys):
    """unittest for dialogs_qt.ask_ync_question
    """
    monkeypatch.setattr(testee.shared, 'get_text', mock_get_text)
    monkeypatch.setattr(testee.shared, 'get_title', mock_get_title)
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question)
    assert testee.ask_ync_question('win', message_id='xxx', text='yyy') == (False, False)
    # buttons = testee.qtw.QMessageBox.StandardButton.Yes | testee.qtw.QMessageBox.StandardButton.No | testee.qtw.QMessageBox.StandardButton.Cancel
    # # hier komt `buttons` ineens niet meer overeen met de buttons in de testee methode
    # daarom stdout vergelijking maar laten zitten
    # assert capsys.readouterr().out == (
    #         "called shared.get_text with args ('win', 'xxx', 'yyy', None)\n"
    #         "called shared.get_title with args ('win',)\n"
    #         f"called MessageBox.question with args ('win', 'title', 'text', {buttons}")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question_2)
    assert testee.ask_ync_question('win', message_id='xxx', text='yyy', args={}) == (True, False)
    # buttons = testee.qtw.QMessageBox.StandardButton.Yes | testee.qtw.QMessageBox.StandardButton.No | testee.qtw.QMessageBox.StandardButton.Cancel
    # assert capsys.readouterr().out == (
    #         "called shared.get_text with args ('win', 'xxx', 'yyy', {})\n"
    #         "called shared.get_title with args ('win',)\n"
    #         f"called MessageBox.question with args ('win', 'title', 'text', {buttons}")
    monkeypatch.setattr(testee.qtw.QMessageBox, 'question', mock_question_3)
    assert testee.ask_ync_question('win', message_id='xxx', text='yyy',
                                   args={'aa': 'bbbb'}) == (False, True)
    # buttons = testee.qtw.QMessageBox.StandardButton.Yes | testee.qtw.QMessageBox.StandardButton.No | testee.qtw.QMessageBox.StandardButton.Cancel
    # assert capsys.readouterr().out == (
    #         "called shared.get_text with args ('win', 'xxx', 'yyy', {'aa': 'bbbb'})\n"
    #         "called shared.get_title with args ('win',)\n"
    #         f"called MessageBox.question with args ('win', 'title', 'text', {buttons}")


def test_get_textinput(monkeypatch, capsys):
    """unittest for dialogs_qt.get_textinput
    """
    def mock_get(*args, **kwargs):
        print('called Inputdialog.getText with args', args, kwargs)
        return '', testee.qtw.QDialog.DialogCode.Rejected
    def mock_get_2(*args, **kwargs):
        print('called Inputdialog.getText with args', args, kwargs)
        return 'xxx', testee.qtw.QDialog.DialogCode.Accepted
    monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get)
    assert testee.get_textinput('win', 'text', 'prompt') == ('', False)
    assert capsys.readouterr().out == ("called Inputdialog.getText with args"
                                       " ('win', 'Application Title', 'prompt') {'text': 'text'}\n")
    monkeypatch.setattr(testee.qtw.QInputDialog, 'getText', mock_get_2)
    assert testee.get_textinput('win', 'text', 'prompt') == ('xxx', True)
    assert capsys.readouterr().out == ("called Inputdialog.getText with args"
                                       " ('win', 'Application Title', 'prompt') {'text': 'text'}\n")


def test_get_choice(monkeypatch, capsys):
    """unittest for dialogs_qt.get_choice
    """
    def mock_get(*args, **kwargs):
        print('called Inputdialog.getItem with args', args, kwargs)
        return ''
    def mock_get_2(*args, **kwargs):
        print('called Inputdialog.getItem with args', args, kwargs)
        return 'xxx'
    monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get)
    assert testee.get_choice('win', 'title', 'caption', ['choices'], 'current') == ""
    assert capsys.readouterr().out == (
            "called Inputdialog.getItem with args"
            " ('win', 'title', 'caption', ['choices'], 'current') {'editable': False}\n")
    monkeypatch.setattr(testee.qtw.QInputDialog, 'getItem', mock_get_2)
    assert testee.get_choice('win', 'title', 'caption', ['choices'], 'current') == "xxx"
    assert capsys.readouterr().out == (
            "called Inputdialog.getItem with args"
            " ('win', 'title', 'caption', ['choices'], 'current') {'editable': False}\n")


def test_get_file_to_open(monkeypatch, capsys):
    """unittest for dialogs_qt.get_file_to_open
    """
    def mock_get(*args):
        print('called shared.get_open_title with args', args)
    def mock_get_file(*args, **kwargs):
        print('called FileDialog.getOpenFileName with args', args, kwargs)
        return '', False
    def mock_get_file_2(*args, **kwargs):
        print('called FileDialog.getOpenFileName with args', args, kwargs)
        return 'xxx', True
    monkeypatch.setattr(testee.shared, 'get_open_title', mock_get)
    monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get_file)
    assert testee.get_file_to_open('win') == ""
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', '')\n"
            "called FileDialog.getOpenFileName with args"
            " ('win', None) {'directory': '', 'filter': ''}\n")
    monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get_file_2)
    assert testee.get_file_to_open('win', 'oms', 'extension', 'start') == "xxx"
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', 'oms')\n"
            "called FileDialog.getOpenFileName with args"
            " ('win', None) {'directory': 'start', 'filter': 'extension'}\n")


def test_get_file_to_save(monkeypatch, capsys):
    """unittest for dialogs_qt.get_file_to_save
    """
    def mock_get(*args):
        print('called shared.get_open_title with args', args)
    def mock_get_file(*args, **kwargs):
        print('called FileDialog.getSaveFileName with args', args, kwargs)
        return '', False
    def mock_get_file_2(*args, **kwargs):
        print('called FileDialog.getSaveFileName with args', args, kwargs)
        return 'xxx', True
    monkeypatch.setattr(testee.shared, 'get_open_title', mock_get)
    monkeypatch.setattr(testee.qtw.QFileDialog, 'getSaveFileName', mock_get_file)
    assert testee.get_file_to_save('win') == ""
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', '')\n"
            "called FileDialog.getSaveFileName with args"
            " ('win', None) {'filter': ''}\n")
    monkeypatch.setattr(testee.qtw.QFileDialog, 'getSaveFileName', mock_get_file_2)
    assert testee.get_file_to_save('win', 'oms', 'extension', 'start') == "xxx"
    assert capsys.readouterr().out == (
            "called shared.get_open_title with args ('win', 'C_SELFIL', 'oms')\n"
            "called FileDialog.getSaveFileName with args"
            " ('win', None) {'filter': 'extension'}\n")


class TestInitialToolDialog:
    """unittest for dialogs_qt.InitialToolDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.InitialToolDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called InitialToolDialog.__init__ with args', args)
        monkeypatch.setattr(testee.InitialToolDialog, '__init__', mock_init)
        testobj = testee.InitialToolDialog()
        testobj.parent = mockqtw.MockFrame()
        testobj.parent.master = types.SimpleNamespace()
        assert capsys.readouterr().out == ("called InitialToolDialog.__init__ with args ()\n"
                                           "called Frame.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for InitialToolDialog.__init__
        """
        parent = types.SimpleNamespace()
        master = types.SimpleNamespace(prefs=('oldmode', 'oldpref'),
                                       ini={'plugins': ['plg1', 'plg2']},
                                       title='a title',
                                       captions={'M_PREF': '', "T_FIXED": '', 'T_RMBR': ''})
        # monkeypatch.setattr(testee.qtw, 'QDialog', mockqtw.MockDialog)
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QRadioButton', mockqtw.MockRadioButton)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = testee.InitialToolDialog(parent, master)
        assert capsys.readouterr().out == expected_output['initialtool'].format(testobj=testobj)

    def test_accept(self, monkeypatch, capsys):
        """unittest for InitialToolDialog.accept
        """
        def mock_accept(*args):
            print('called Editor.accept_startupsettings with args', args)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.accept_startupsettings = mock_accept
        testobj.check_fixed = mockqtw.MockRadioButton()
        testobj.check_remember = mockqtw.MockRadioButton()
        testobj.sel_fixed = mockqtw.MockComboBox()
        assert capsys.readouterr().out == ("called RadioButton.__init__ with args () {}\n"
                                           "called RadioButton.__init__ with args () {}\n"
                                           "called ComboBox.__init__\n")
        testobj.accept()
        assert capsys.readouterr().out == (
                "called RadioButton.isChecked\n"
                "called RadioButton.isChecked\n"
                "called ComboBox.currentText\n"
                "called Editor.accept_startupsettings with args (False, False, 'current text')\n"
                "called Dialog.accept\n")


class TestFileBrowseButton:
    """unittest for dialogs_qt.FileBrowseButton
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.FileBrowseButton object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FileBrowseButton.__init__ with args', args)
        monkeypatch.setattr(testee.FileBrowseButton, '__init__', mock_init)
        testobj = testee.FileBrowseButton()
        assert capsys.readouterr().out == 'called FileBrowseButton.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for FileBrowseButton.__init__
        """
        # def mock_init(self, parent):
        #     print(f"called Frame.__init__ with arg {parent}")
        monkeypatch.setattr(testee.qtw.QFrame, '__init__', mockqtw.MockFrame.__init__)
        monkeypatch.setattr(testee.qtw.QFrame, 'setWindowTitle', mockqtw.MockFrame.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QFrame, 'setFrameStyle', mockqtw.MockFrame.setFrameStyle)
        monkeypatch.setattr(testee.qtw.QFrame, 'setLayout', mockqtw.MockFrame.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        cp = {'C_BRWS': 'xxx'}
        parent = types.SimpleNamespace(master=types.SimpleNamespace(title='master1', captions=cp),
                                       parent=types.SimpleNamespace(
                                           master=types.SimpleNamespace(title='master2',
                                                                        captions=cp)))
        testobj = testee.FileBrowseButton(parent)
        assert capsys.readouterr().out == expected_output["filebrowse"].format(testobj=testobj,
                                                                               title="master1")
        testobj = testee.FileBrowseButton(parent, text="xxx\\yyy", level_down=True)
        assert capsys.readouterr().out == expected_output["filebrowse"].format(testobj=testobj,
                                                                               title="master2")

    def test_browse(self, monkeypatch, capsys):
        """unittest for FileBrowseButton.browse
        """
        def mock_get(parent, *args, **kwargs):
            print('called FileDialog.getOpenFileName with args', parent, args, kwargs)
            return 'zzz', True
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName',
                            mockqtw.MockFileDialog.getOpenFileName)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent = types.SimpleNamespace(captions={'C_SELFIL': 'xxx'})
        testobj.input = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n")
        testobj.browse()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                f"called FileDialog.getOpenFileName with args {testobj}"
                f" ('xxx', '{testee.shared.HERE}/plugins') {{}}\n")
        monkeypatch.setattr(testee.qtw.QFileDialog, 'getOpenFileName', mock_get)
        testobj.input = mockqtw.MockLineEdit('qqq')
        assert capsys.readouterr().out == ("called LineEdit.__init__\n")
        testobj.browse()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                f"called FileDialog.getOpenFileName with args {testobj} ('xxx', 'qqq') {{}}\n"
                "called LineEdit.setText with arg `zzz`\n")


class TestSetupDialog:
    """unittest for dialogs_qt.SetupDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.SetupDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SetupDialog.__init__ with args', args)
        monkeypatch.setattr(testee.SetupDialog, '__init__', mock_init)
        testobj = testee.SetupDialog()
        testobj.parent = mockqtw.MockFrame()
        testobj.parent.master = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called SetupDialog.__init__ with args ()\n'
                                           "called Frame.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for SetupDialog.__init__
        """
        class MockFileBrowseButton:
            "stub for FileBrowseButton object"
            def __init__(self, *args, **kwargs):
                print('called gui.FileBrowseButton with args', args, kwargs)
        parent = mockqtw.MockFrame()
        parent.master = types.SimpleNamespace(captions={'T_INIKDEF': 'T_INIKDEF',
                                                        'T_NAMOF': 'T_NAMOF {} {}',
                                                        'S_PLGNAM': 'S_PLGNAM',
                                                        'T_ISMADE': 'T_ISMADE',
                                                        'S_PNLNAM': 'S_PNLNAM',
                                                        'T_MAKE': 'T_MAKE {}',
                                                        'S_RBLD': 'S_RBLD',
                                                        'S_DETS': 'S_DETS',
                                                        'S_RSAV': 'S_RSAV',
                                                        'Q_SAVLOC': 'Q_SAVLOC'})
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee, 'FileBrowseButton', MockFileBrowseButton)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = testee.SetupDialog(parent, 'Name')
        assert capsys.readouterr().out == expected_output['setup'].format(testobj=testobj)

    def test_accept(self, monkeypatch, capsys):
        """unittest for SetupDialog.accept
        """
        def mock_accept(*args):
            print('called Editor.accept_pluginsettings with args', args)
            return False
        def mock_accept_2(*args):
            print('called Editor.accept_pluginsettings with args', args)
            return True
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.master.accept_pluginsettings = mock_accept
        testobj.t_loc = types.SimpleNamespace(input=mockqtw.MockLineEdit('loc'))
        testobj.t_program = mockqtw.MockLineEdit('prog')
        testobj.t_title = mockqtw.MockLineEdit('name')
        testobj.c_rebuild = mockqtw.MockCheckBox()
        testobj.c_details = mockqtw.MockCheckBox()
        testobj.c_redef = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n")
        testobj.accept()
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Editor.accept_pluginsettings with args"
                                           " ('loc', 'prog', 'name', False, False, False)\n")
        testobj.parent.master.accept_pluginsettings = mock_accept_2
        testobj.accept()
        assert capsys.readouterr().out == ("called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called LineEdit.text\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Editor.accept_pluginsettings with args"
                                           " ('loc', 'prog', 'name', False, False, False)\n"
                                           "called Dialog.accept\n")


class TestDeleteDialog:
    """unittest for dialogs_qt.DeleteDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.DeleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called DeleteDialog.__init__ with args', args)
        monkeypatch.setattr(testee.DeleteDialog, '__init__', mock_init)
        testobj = testee.DeleteDialog()
        testobj.parent = mockqtw.MockFrame()
        testobj.parent.master = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called DeleteDialog.__init__ with args ()\n'
                                           "called Frame.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for DeleteDialog.__init__
        """
        parent = mockqtw.MockFrame()
        parent.master = types.SimpleNamespace(title='title',
                                              captions={'Q_REMPRG': 'xxx', 'Q_REMKDEF': 'yyy',
                                                        'Q_REMPLG': 'zzz'})
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = testee.DeleteDialog(parent)
        assert testobj.parent.master.last_added == ''
        assert isinstance(testobj.remove_keydefs, testee.qtw.QCheckBox)
        assert isinstance(testobj.remove_plugin, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['delete'].format(testobj=testobj)

    def test_accept(self, monkeypatch, capsys):
        """unittest for DeleteDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_keydefs = mockqtw.MockCheckBox()
        testobj.remove_keydefs.setChecked(True)
        testobj.remove_plugin = mockqtw.MockCheckBox()
        testobj.remove_plugin.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n")
        testobj.accept()
        assert testobj.parent.remove_data
        assert testobj.parent.remove_code
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n"
                                           "called Dialog.accept\n")


class TestFilesDialog:
    """unittest for dialogs_qt.FilesDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.FilesDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FilesDialog.__init__ with args', args)
        monkeypatch.setattr(testee.FilesDialog, '__init__', mock_init)
        testobj = testee.FilesDialog()
        testobj.parent = mockqtw.MockFrame()
        testobj.parent.master = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called FilesDialog.__init__ with args ()\n'
                                           "called Frame.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for FilesDialog.__init__
        """
        def mock_add(*args):
            print('called FilesDialog.add_row with args', args)
        def mock_addbutton(self, *args):
            print('called ButtonBox.addButton with args', args)
            return mockqtw.MockPushButton()
        parent = mockqtw.MockFrame()
        master = types.SimpleNamespace(title='title',
                                       captions={'T_TOOLS': 'xxx',
                                                 'C_PRGNAM': 'yyy',
                                                 'C_KDEFLOC': 'zzz',
                                                 'C_ADDPRG': 'aaa',
                                                 'C_REMPRG': 'bbb'},
                                       ini={'plugins': [('name', 'path')]},
                                       pluginfiles={'name': 'data'})
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(mockqtw.MockButtonBox, 'addButton', mock_addbutton)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.FilesDialog, 'add_row', mock_add)
        testobj = testee.FilesDialog(parent, master)
        assert testobj.code_to_remove == []
        assert testobj.data_to_remove == []
        assert isinstance(testobj.scrl, testee.qtw.QScrollArea)
        assert testobj.bar == 'vertical scrollbar'
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.gsizer, testee.qtw.QGridLayout)
        assert testobj.rownum == 0
        assert testobj.plugindata == []
        assert testobj.checks == []
        assert testobj.paths == []
        assert testobj.progs == []
        assert testobj.settingsdata == {'name': ('data', )}
        # hier zit weer zo'n OR die blijkbaar een integer verandert in een object (Alignment)
        # assert capsys.readouterr().out == expected_output['files'].format(testobj=testobj)

    def test_add_row(self, monkeypatch, capsys):
        """unittest for FilesDialog.add_row
        """
        class MockFileBrowseButton:
            "stub for FileBrowseButton object"
            def __init__(self, *args, **kwargs):
                print('called gui.FileBrowseButton with args', args, kwargs)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee, 'FileBrowseButton', MockFileBrowseButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        # testobj.scrl = mockqtw.MockScrollArea()
        testobj.bar = mockqtw.MockScrollBar()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called ScrollBar.__init__\n")
        testobj.checks = []
        testobj.paths = []
        testobj.rownum = 0
        testobj.add_row('name')
        assert testobj.rownum == 1
        assert len(testobj.checks) == 1
        assert isinstance(testobj.checks[0], testee.qtw.QCheckBox)
        assert len(testobj.paths) == 1
        assert testobj.paths[0][0] == 'name'
        assert isinstance(testobj.paths[0][1], testee.FileBrowseButton)
        assert capsys.readouterr().out == (
                "called CheckBox.__init__\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockCheckBox'> at (1, 0)\n"
                f"called gui.FileBrowseButton with args ({testobj},) {{'text': ''}}\n"
                "called Grid.addWidget with arg of type"
                " <class 'test_dialogs_qt.TestFilesDialog.test_add_row"
                ".<locals>.MockFileBrowseButton'> at (1, 1)\n"
                "called Scrollbar.maximum\n"
                "called Scrollbar.setMaximum with value `151`\n"
                "called Scrollbar.maximum\n"
                "called Scrollbar.setValue with value `99`\n")
        testobj.checks = []
        testobj.paths = []
        testobj.rownum = 0
        testobj.add_row('name', 'path')
        assert testobj.rownum == 1
        assert testobj.rownum == 1
        assert len(testobj.checks) == 1
        assert isinstance(testobj.checks[0], testee.qtw.QCheckBox)
        assert len(testobj.paths) == 1
        assert testobj.paths[0][0] == 'name'
        assert isinstance(testobj.paths[0][1], testee.FileBrowseButton)
        assert capsys.readouterr().out == (
                "called CheckBox.__init__\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockCheckBox'> at (1, 0)\n"
                f"called gui.FileBrowseButton with args ({testobj},) {{'text': 'path'}}\n"
                "called Grid.addWidget with arg of type"
                " <class 'test_dialogs_qt.TestFilesDialog.test_add_row"
                ".<locals>.MockFileBrowseButton'> at (1, 1)\n"
                "called Scrollbar.maximum\n"
                "called Scrollbar.setMaximum with value `151`\n"
                "called Scrollbar.maximum\n"
                "called Scrollbar.setValue with value `99`\n")

    def test_delete_row(self, monkeypatch, capsys):
        """unittest for FilesDialog.delete_row
        """
        class MockFileBrowseButton:
            "stub for FileBrowseButton object"
            def __init__(self, *args, **kwargs):
                print('called gui.FileBrowseButton with args', args, kwargs)
            def close(self):
                print('called gui.FileBrowseButton.close')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockGridLayout()
        testobj.checks = [mockqtw.MockCheckBox()]
        testobj.paths = [('name', MockFileBrowseButton())]
        testobj.settingsdata = {'name': 'data'}
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called gui.FileBrowseButton with args () {}\n")
        testobj.delete_row(0)
        assert not testobj.checks
        assert not testobj.paths
        assert not testobj.settingsdata
        assert capsys.readouterr().out == (
                "called Grid.removeWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                "called CheckBox.close\n"
                "called Grid.removeWidget with arg of type"
                " <class 'test_dialogs_qt.TestFilesDialog.test_delete_row"
                ".<locals>.MockFileBrowseButton'>\n"
                "called gui.FileBrowseButton.close\n")

    def test_add_program(self, monkeypatch, capsys):
        """unittest for FilesDialog.add_program
        """
        def mock_get(*args):
            print('called get_textinput with args', args)
            return '', False
        def mock_get_2(*args):
            print('called get_textinput with args', args)
            return '', True
        def mock_get_3(*args):
            print('called get_textinput with args', args)
            return 'qqq', True
        def mock_show(*args):
            print('called show_message with args', args)
        def mock_ask(*args):
            print('called ask_question with args', args)
            return False
        def mock_ask_2(*args):
            print('called ask_question with args', args)
            return True
        class MockSetup:
            "stub for SetupDialog object"
            def __init__(self, *args):
                print('called SetupDialog with args', args)
            def exec(self):
                print('called SetupDialog.exec')
                return False
        class MockSetup2:
            "stub for SetupDialog object"
            def __init__(self, *args):
                print('called SetupDialog with args', args)
            def exec(self):
                print('called SetupDialog.exec')
                return True
        def mock_add(*args, **kwargs):
            print('called FilesDialog with args', args, kwargs)
        monkeypatch.setattr(testee, 'get_textinput', mock_get)
        monkeypatch.setattr(testee, 'show_message', mock_show)
        monkeypatch.setattr(testee, 'ask_question', mock_ask)
        monkeypatch.setattr(testee, 'SetupDialog', MockSetup)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.settingsdata = {}
        testobj.parent = mockqtw.MockFrame()
        assert capsys.readouterr().out == ("called Frame.__init__\n")
        testobj.master = types.SimpleNamespace(captions={'P_NEWPRG': 'xxx'})
        testobj.add_row = mock_add
        testobj.parent.data = ['data_loc', 'prgloc', 'yyy']
        testobj.add_program()
        assert capsys.readouterr().out == (
                f"called get_textinput with args ({testobj}, '', 'xxx')\n")
        monkeypatch.setattr(testee, 'get_textinput', mock_get_2)
        testobj.add_program()
        assert capsys.readouterr().out == (
                f"called get_textinput with args ({testobj}, '', 'xxx')\n"
                f"called show_message with args ({testobj.parent}, 'I_NEEDNAME')\n")
        monkeypatch.setattr(testee, 'get_textinput', mock_get_3)
        testobj.add_program()
        assert capsys.readouterr().out == (
                f"called get_textinput with args ({testobj}, '', 'xxx')\n"
                f"called ask_question with args ({testobj.parent}, 'P_INIKDEF')\n"
                "called FilesDialog with args ('qqq',) {'path': ''}\n")
        monkeypatch.setattr(testee, 'ask_question', mock_ask_2)
        testobj.add_program()
        assert capsys.readouterr().out == (
                f"called get_textinput with args ({testobj}, '', 'xxx')\n"
                f"called ask_question with args ({testobj.parent}, 'P_INIKDEF')\n"
                f"called SetupDialog with args ({testobj}, 'qqq')\n"
                "called SetupDialog.exec\n"
                "called FilesDialog with args ('qqq',) {'path': ''}\n")
        monkeypatch.setattr(testee, 'SetupDialog', MockSetup2)
        testobj.add_program()
        assert capsys.readouterr().out == (
                f"called get_textinput with args ({testobj}, '', 'xxx')\n"
                f"called ask_question with args ({testobj.parent}, 'P_INIKDEF')\n"
                f"called SetupDialog with args ({testobj}, 'qqq')\n"
                "called SetupDialog.exec\n"
                "called FilesDialog with args ('qqq',) {'path': 'data_loc'}\n")

    def test_remove_programs(self, monkeypatch, capsys):
        """unittest for FilesDialog.remove_programs
        """
        class MockDelete:
            "stub for DeleteDialog object"
            def __init__(self, parent):
                print('called DeleteDialog.__init__')
            def exec(self):
                print('called DeleteDialog.exec')
                return testee.qtw.QDialog.DialogCode.Rejected
        class MockDelete2:
            "stub for DeleteDialog object"
            def __init__(self, parent):
                print('called DeleteDialog.__init__')
            def exec(self):
                print('called DeleteDialog.exec')
                return testee.qtw.QDialog.DialogCode.Accepted
        class MockFileBrowseButton:
            "stub for FileBrowseButton object"
            def __init__(self, *args, **kwargs):
                print('called gui.FileBrowseButton with args', args, kwargs)
                self.input = mockqtw.MockLineEdit(args[0])
            def close(self):
                print('called gui.FileBrowseButton.close')
        def mock_delete(row):
            print(f"called FilesDialog.delete_row with arg {row}")
        check_a = mockqtw.MockCheckBox('xxx')
        file_a = MockFileBrowseButton('aaa')
        check_b = mockqtw.MockCheckBox('yyy')
        file_b = MockFileBrowseButton('bbb')
        check_c = mockqtw.MockCheckBox('zzz')
        file_c = MockFileBrowseButton('ccc')
        check_c.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called gui.FileBrowseButton with args ('aaa',) {}\n"
                                           "called LineEdit.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called gui.FileBrowseButton with args ('bbb',) {}\n"
                                           "called LineEdit.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called gui.FileBrowseButton with args ('ccc',) {}\n"
                                           "called LineEdit.__init__\n"
                                           "called CheckBox.setChecked with arg True\n")
        monkeypatch.setattr(testee, 'DeleteDialog', MockDelete)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.delete_row = mock_delete
        testobj.checks = [check_a, check_b]
        testobj.paths = [('xxx', file_a), ('yyy', file_b)]
        testobj.settingsdata = {}
        testobj.data_to_remove = []
        testobj.code_to_remove = []
        testobj.remove_programs()
        assert not testobj.data_to_remove
        assert not testobj.code_to_remove
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called CheckBox.isChecked\n")
        monkeypatch.setattr(testee, 'DeleteDialog', MockDelete2)
        testobj.checks = [check_c]
        testobj.paths = [('zzz', file_c)]
        testobj.settingsdata = {'ccc': 'path.name'}
        testobj.data_to_remove = []
        testobj.code_to_remove = []
        with pytest.raises(KeyError) as exc:
            testobj.remove_programs()
        assert str(exc.value) == "'zzz'"
        assert not testobj.data_to_remove
        assert not testobj.code_to_remove
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called DeleteDialog.__init__\n"
                                           "called DeleteDialog.exec\n"
                                           "called LineEdit.text\n")
        testobj.checks = [check_c]
        testobj.paths = [('zzz', file_c)]
        testobj.settingsdata = {'zzz': ('path.name',)}
        testobj.data_to_remove = []
        testobj.code_to_remove = []
        testobj.remove_data, testobj.remove_code = True, False
        testobj.remove_programs()
        assert testobj.data_to_remove == ['ccc']
        assert not testobj.code_to_remove
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called DeleteDialog.__init__\n"
                                           "called DeleteDialog.exec\n"
                                           "called LineEdit.text\n"
                                           "called FilesDialog.delete_row with arg 0\n")
        testobj.checks = [check_c]
        testobj.paths = [('zzz', file_c)]
        testobj.settingsdata = {'zzz': ('path.name',)}
        testobj.data_to_remove = []
        testobj.code_to_remove = []
        testobj.remove_data, testobj.remove_code = False, True
        testobj.remove_programs()
        assert not testobj.data_to_remove
        assert testobj.code_to_remove == ['path/name.py']
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n"
                                           "called DeleteDialog.__init__\n"
                                           "called DeleteDialog.exec\n"
                                           "called LineEdit.text\n"
                                           "called FilesDialog.delete_row with arg 0\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for FilesDialog.accept
        """
        def mock_accept(*args):
            print('called Editor.accept_pathsettings with args', args)
            return False
        def mock_accept_2(*args):
            print('called Editor.accept_pathsettings with args', args)
            return True
        class MockFileBrowseButton:
            "stub for FileBrowseButton object"
            def __init__(self, *args, **kwargs):
                print('called gui.FileBrowseButton with args', args, kwargs)
                self.input = mockqtw.MockLineEdit(args[0])
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.paths = [('aaa', MockFileBrowseButton('bbb'))]
        assert capsys.readouterr().out == ("called gui.FileBrowseButton with args ('bbb',) {}\n"
                                           "called LineEdit.__init__\n")
        testobj.settingsdata = []
        testobj.code_to_remove = []
        testobj.data_to_remove = []
        testobj.master = types.SimpleNamespace()
        testobj.master.accept_pathsettings = mock_accept
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Editor.accept_pathsettings with args ([('aaa', 'bbb')], [], [])\n")
        testobj.master.accept_pathsettings = mock_accept_2
        testobj.code_to_remove = ['xxx']
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Editor.accept_pathsettings with args ([('aaa', 'bbb')], [], ['xxx'])\n"
                "called Dialog.accept\n")
        testobj.data_to_remove = ['yyy']
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called Editor.accept_pathsettings with args ([('aaa', 'bbb')], [], ['xxx', 'yyy'])\n"
                "called Dialog.accept\n")


class TestColumnSettingsDialog:
    """unittest for dialogs_qt.ColumnSettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ColumnSettingsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ColumnSettingsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ColumnSettingsDialog, '__init__', mock_init)
        testobj = testee.ColumnSettingsDialog()
        testobj.parent = mockqtw.MockFrame()
        testobj.parent.master = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called ColumnSettingsDialog.__init__ with args ()\n'
                                           "called Frame.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ColumnSettingsDialog.__init__
        """
        def mock_add(*args):
            print('called ColumsSettingsDialog.add_row with args', args)
        def mock_addbutton(self, *args):
            print('called ButtonBox.addButton with args', args)
            return mockqtw.MockPushButton()
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
        monkeypatch.setattr(mockqtw.MockButtonBox, 'addButton', mock_addbutton)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.ColumnSettingsDialog, 'add_row', mock_add)
        parent = mockqtw.MockFrame()
        master = types.SimpleNamespace(book=types.SimpleNamespace(page=types.SimpleNamespace()))
        master.title = 'title'
        master.captions = {'T_COLSET': 'COLSET {}', 'C_TTL': 'TTL', 'C_WID': 'WID', 'C_IND': 'IND',
                           'C_SEQ': 'SEQ', 'C_ADDCOL': 'ADDCOL', 'C_REMCOL': 'REMCOL'}
        master.col_textids = []
        master.col_names = []
        master.book.page.settings = {testee.shared.SettType.PNL.value: 'XXX'}
        master.book.page.column_info = [('xxx', 5, 0, 0), ('yyy', 10, 1, 1)]
        testobj = testee.ColumnSettingsDialog(parent, master)
        assert testobj.parent == parent
        assert testobj.master == master
        assert isinstance(testobj.scrl, testee.qtw.QScrollArea)
        testobj.bar = 'vertical scrollbar'
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.gsizer, testee.qtw.QVBoxLayout)
        assert testobj.rownum == 0
        assert testobj.data == []
        assert testobj.checks == []
        assert testobj.col_textids == master.col_textids
        assert testobj.col_names == master.col_names
        # hier zit weer zo'n OR die blijkbaar een integer verandert in een object (Alignment)
        # assert capsys.readouterr().out == expected_output['columns'].format(testobj=testobj)

    def test_add_row(self, monkeypatch, capsys, expected_output):
        """unittest for ColumnSettingsDialog.add_row
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockVBoxLayout()
        testobj.bar = mockqtw.MockScrollBar()
        assert capsys.readouterr().out == ("called VBox.__init__\ncalled ScrollBar.__init__\n")
        testobj.rownum = 1
        testobj.data = []
        testobj.checks = []
        testobj.col_textids = ['xxx', 'yyy']
        testobj.col_names = ['xxx', 'yyy']
        testobj.add_row()
        assert testobj.rownum == 2
        assert len(testobj.checks) == 1
        assert isinstance(testobj.checks[0], testee.qtw.QCheckBox)
        assert len(testobj.data) == 1
        assert isinstance(testobj.data[0][0], testee.qtw.QComboBox)
        assert isinstance(testobj.data[0][1], testee.qtw.QSpinBox)
        assert isinstance(testobj.data[0][2], testee.qtw.QSpinBox)
        assert isinstance(testobj.data[0][3], testee.qtw.QCheckBox)
        assert testobj.data[0][4] == 'new'
        assert capsys.readouterr().out == expected_output['addcol1'].format(testobj=testobj,
                                                                            flag=False)
        testobj.add_row(name='xxx', width='5', is_flag=True, colno=1)
        assert testobj.rownum == 3
        assert len(testobj.checks) == 2
        assert isinstance(testobj.checks[1], testee.qtw.QCheckBox)
        assert len(testobj.data) == 2
        assert isinstance(testobj.data[0][0], testee.qtw.QComboBox)
        assert isinstance(testobj.data[0][1], testee.qtw.QSpinBox)
        assert isinstance(testobj.data[0][2], testee.qtw.QSpinBox)
        assert isinstance(testobj.data[0][3], testee.qtw.QCheckBox)
        assert testobj.data[0][4] == 'new'
        assert capsys.readouterr().out == expected_output['addcol2'].format(testobj=testobj,
                                                                            flag=True)

    def test_delete_row(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.delete_row
        """
        monkeypatch.setattr(testee.qtw, 'QSpinBox', mockqtw.MockSpinBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gsizer = mockqtw.MockVBoxLayout()
        testobj.rownum = 2
        check1 = mockqtw.MockCheckBox()
        check2 = mockqtw.MockCheckBox()
        testobj.checks = [check1, check2]
        spinner1 = mockqtw.MockSpinBox(1)
        spinner2 = mockqtw.MockSpinBox(2)
        w0 = mockqtw.MockWidget()
        w1 = mockqtw.MockWidget()
        w3 = mockqtw.MockWidget()
        testobj.data = [(w0, w1, spinner1, w3, ''), ('', '', spinner2, '', '')]
        assert capsys.readouterr().out == ("called VBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called SpinBox.__init__\ncalled SpinBox.__init__\n"
                                           "called Widget.__init__\ncalled Widget.__init__\n"
                                           "called Widget.__init__\n")
        testobj.delete_row(0)
        assert testobj.rownum == 1
        assert testobj.checks == [check2]
        assert testobj.data == [('', '', spinner2, '', '')]
        assert capsys.readouterr().out == (
                "called SpinBox.value\ncalled SpinBox.setValue with arg '0'\n"
                "called SpinBox.value\ncalled SpinBox.setValue with arg '1'\n"
                "called VBox.removeWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                "called CheckBox.close\n"
                "called VBox.removeWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockWidget'>\n"
                "called Widget.close\n"
                "called VBox.removeWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockWidget'>\n"
                "called Widget.close\n"
                "called VBox.removeWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockSpinBox'>\n"
                "called SpinBox.close\n"
                "called VBox.removeWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockWidget'>\n"
                "called Widget.close\ncalled VBox.itemAt with arg 0\ncalled VBox.removeItem\n")

    def test_on_text_changed(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.on_text_changed
        """
        class MockComboBox:
            "stub"
            def __init__(self, *args, **kwargs):
                print('called ComboBox.__init__')
                self._text = args[0]
            def currentText(self):
                print('called ComboBox.currentText')
                return self._text
        name1 = MockComboBox('name1')
        width1 = mockqtw.MockSpinBox(10)
        name2 = MockComboBox('name2')
        width2 = mockqtw.MockSpinBox(1)
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called SpinBox.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called SpinBox.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.data = [(name1, width1, 'x', 'y'), (name2, width2, 'a', 'b')]
        testobj.on_text_changed('name2')
        assert capsys.readouterr().out == ("called ComboBox.currentText\n"
                                           "called ComboBox.currentText\n"
                                           "called SpinBox.setValue with arg '50'\n")

    def test_add_column(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.add_column
        """
        def mock_add():
            print("called ColumnSettingsDialog.add_row")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_row = mock_add
        testobj.add_column()
        assert capsys.readouterr().out == ("called ColumnSettingsDialog.add_row\n")

    def test_remove_columns(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.remove_columns
        """
        def mock_ask(*args):
            print('called ask_question with args', args)
            return False
        def mock_ask_2(*args):
            print('called ask_question with args', args)
            return True
        def mock_delete(arg):
            print(f'called ColumnSettingsDialog.delete_row with arg {arg}')
        monkeypatch.setattr(testee, 'ask_question', mock_ask)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.delete_row = mock_delete
        check1 = mockqtw.MockCheckBox()
        check2 = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called CheckBox.__init__\ncalled CheckBox.__init__\n")
        testobj.checks = [check1, check2]
        testobj.remove_columns()
        assert capsys.readouterr().out == ("called CheckBox.isChecked\ncalled CheckBox.isChecked\n")
        check2.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.setChecked with arg True\n")
        monkeypatch.setattr(testee, 'ask_question', mock_ask_2)
        testobj.remove_columns()
        assert capsys.readouterr().out == (
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called ask_question with args ({testobj.parent}, 'Q_REMCOL')\n"
                "called ColumnSettingsDialog.delete_row with arg 1\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for ColumnSettingsDialog.accept
        """
        def mock_accept(arg):
            print(f'called Editor.accept_columnsettings with arg {arg}')
            return False, False
        def mock_accept_2(arg):
            print(f'called Editor.accept_columnsettings with arg {arg}')
            return True, False
        def mock_accept_3(arg):
            print(f'called Editor.accept_columnsettings with arg {arg}')
            return False, True
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace()
        testobj.master.accept_columnsettings = mock_accept
        w1 = mockqtw.MockComboBox()
        w2 = mockqtw.MockSpinBox()
        w3 = mockqtw.MockLineEdit()
        w4 = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == ("called ComboBox.__init__\ncalled SpinBox.__init__\n"
                                           "called LineEdit.__init__\ncalled CheckBox.__init__\n")
        testobj.data = [(w1, w2, w3, w4, 'xxx')]
        testobj.accept()
        assert capsys.readouterr().out == (
            "called ComboBox.currentText\n"
            "called SpinBox.value\n"
            "called LineEdit.text\n"
            "called CheckBox.isChecked\n"
            "called Editor.accept_columnsettings with arg [('current text', 0, '', False, 'xxx')]\n")
        testobj.master.accept_columnsettings = mock_accept_2
        testobj.accept()
        assert capsys.readouterr().out == (
            "called ComboBox.currentText\n"
            "called SpinBox.value\n"
            "called LineEdit.text\n"
            "called CheckBox.isChecked\n"
            "called Editor.accept_columnsettings with arg [('current text', 0, '', False, 'xxx')]\n"
            "called Dialog.accept\n")
        testobj.master.accept_columnsettings = mock_accept_3
        testobj.accept()
        assert capsys.readouterr().out == (
            "called ComboBox.currentText\n"
            "called SpinBox.value\n"
            "called LineEdit.text\n"
            "called CheckBox.isChecked\n"
            "called Editor.accept_columnsettings with arg [('current text', 0, '', False, 'xxx')]\n")


class TestNewColumnsDialog:
    """unittest for dialogs_qt.NewColumnsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.NewColumnsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called NewColumnsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.NewColumnsDialog, '__init__', mock_init)
        testobj = testee.NewColumnsDialog()
        testobj.parent = mockqtw.MockFrame()
        testobj.parent.master = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called NewColumnsDialog.__init__ with args ()\n'
                                           "called Frame.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for NewColumnsDialog.__init__
        """
        parent = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        master = types.SimpleNamespace(title='title',
                                       captions={'T_TRANS': 'xxx / yyy'},
                                       dialog_data={'languages': ['en.lng', 'nl.lng'],
                                                    'new_titles': []})
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        testobj = testee.NewColumnsDialog(parent, master)
        assert testobj.widgets == []
        assert capsys.readouterr().out == expected_output['newcols'].format(testobj=testobj)

        master = types.SimpleNamespace(title='title',
                                       captions={'T_TRANS': 'xxx / yyy'},
                                       dialog_data={'languages': ['en.lng', 'nl.lng'],
                                                    'new_titles': ['qq'], 'textid': 'Q0', 'colno': 1})
        testobj = testee.NewColumnsDialog(parent, master)
        assert len(testobj.widgets) == 1
        assert len(testobj.widgets[0]) == 3
        for item in testobj.widgets[0]:
            assert isinstance(item, mockqtw.MockLineEdit)
        assert capsys.readouterr().out == expected_output['newcols2'].format(testobj=testobj)

    def test_accept(self, monkeypatch, capsys):
        """unittest for NewColumnsDialog.accept
        """
        def mock_accept(arg):
            print(f'called Editor.accept_newcolumns with arg {arg}')
            return False
        def mock_accept_2(arg):
            print(f'called Editor.accept_newcolumns with arg {arg}')
            return True
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace()
        testobj.master.accept_newcolumns = mock_accept
        testobj.widgets = []
        testobj.accept()
        assert capsys.readouterr().out == ("called Editor.accept_newcolumns with arg []\n")

        testobj.master.accept_newcolumns = mock_accept_2
        w1 = mockqtw.MockLineEdit('xxx')
        w2 = mockqtw.MockLineEdit('yyy')
        assert capsys.readouterr().out == "called LineEdit.__init__\ncalled LineEdit.__init__\n"
        testobj.widgets = [(w1, w2), (w2, w1)]
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called LineEdit.text\n"
                "called Editor.accept_newcolumns with arg [['xxx', 'yyy'], ['yyy', 'xxx']]\n"
                "called Dialog.accept\n")


class TestExtraSettingsDialog:
    """unittest for dialogs_qt.ExtraSettingsDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.ExtraSettingsDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ExtraSettingsDialog.__init__ with args', args)
        monkeypatch.setattr(testee.ExtraSettingsDialog, '__init__', mock_init)
        testobj = testee.ExtraSettingsDialog()
        testobj.parent = mockqtw.MockFrame()
        testobj.parent.master = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called ExtraSettingsDialog.__init__ with args ()\n'
                                           "called Frame.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for ExtraSettingsDialog.__init__
        """
        def mock_add(self):
            "stub"
        def mock_remove(self):
            "stub"
        def mock_add_row(self, *args):
            print('called ExtraSettingsDialog.add_row with args', args)
        parent = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        master = types.SimpleNamespace(title='title',
                                       captions={'S_PLGNAM': 'xxx', 'S_PNLNAM': 'yyy',
                                                 'T_MAKE': 'zzz {}', 'S_RBLD': 'aaa',
                                                 'S_RSAV': 'bbb', 'S_DETS': 'ccc',
                                                 'T_XTRASET': 'ddd', 'C_NAM': 'eee', 'C_VAL': 'fff',
                                                 'C_ADDSET': 'add', 'C_REMSET': 'rem'},
                                       extra={'name': 'qqq'})
        master.book = types.SimpleNamespace(page=types.SimpleNamespace())
        master.book.page.settings = {testee.shared.SettType.PLG.value: 'xxx',
                                     testee.shared.SettType.PNL.value: 'yyy',
                                     testee.shared.SettType.RBLD.value: '0',
                                     testee.shared.SettType.RDEF.value: '0',
                                     testee.shared.SettType.DETS.value: '0'}
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QFrame, 'setFrameStyle', mockqtw.MockFrame.setFrameStyle)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QGridLayout', mockqtw.MockGridLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(testee.qtw, 'QScrollArea', mockqtw.MockScrollArea)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.ExtraSettingsDialog, 'add_setting', mock_add)
        monkeypatch.setattr(testee.ExtraSettingsDialog, 'remove_settings', mock_remove)
        monkeypatch.setattr(testee.ExtraSettingsDialog, 'add_row', mock_add_row)
        testobj = testee.ExtraSettingsDialog(parent, master)
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.t_title, testee.qtw.QLineEdit)
        assert isinstance(testobj.c_rebuild, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_showdet, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_redef, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['extra'].format(
                testobj=testobj, testee=testee, action="")
        master.book.page.settings[testee.shared.SettType.RBLD.value] = '1'
        master.book.page.settings[testee.shared.SettType.RDEF.value] = '1'
        master.book.page.settings[testee.shared.SettType.DETS.value] = '1'
        master.book.page.settings['XYZ'] = 'xyz'
        master.book.page.settings['ABC'] = 'abc'
        monkeypatch.setattr(testee.shared, 'settingnames', [])
        master.book.page.settings['extra'] = {'XYZ': 'xxyyzz'}
        testobj = testee.ExtraSettingsDialog(parent, master)
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.t_title, testee.qtw.QLineEdit)
        assert isinstance(testobj.c_rebuild, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_showdet, testee.qtw.QCheckBox)
        assert isinstance(testobj.c_redef, testee.qtw.QCheckBox)
        assert capsys.readouterr().out == expected_output['extra2'].format(
                testobj=testobj, testee=testee, action="\ncalled CheckBox.toggle")

    def test_add_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.add_row
        """
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.rownum = 0
        testobj.gsizer = mockqtw.MockGridLayout()
        testobj.checks = []
        testobj.data = []
        testobj.bar = mockqtw.MockScrollBar()
        assert capsys.readouterr().out == ("called Grid.__init__\n"
                                           "called ScrollBar.__init__\n")
        testobj.add_row()
        assert testobj.rownum == 2
        assert len(testobj.checks) == 1
        assert isinstance(testobj.checks[0], testee.qtw.QCheckBox)
        assert len(testobj.data) == 1
        assert len(testobj.data[0]) == 3
        assert isinstance(testobj.data[0][0], testee.qtw.QLineEdit)
        assert isinstance(testobj.data[0][1], testee.qtw.QLineEdit)
        assert isinstance(testobj.data[0][2], testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                "called CheckBox.__init__\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockCheckBox'> at (1, 0)\n"
                "called LineEdit.__init__\n"
                "called LineEdit.setFixedWidth with arg `88`\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 1)\n"
                "called LineEdit.__init__\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockLineEdit'> at (1, 2)\n"
                "called LineEdit.__init__\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockLineEdit'> at (2, 2)\n"
                "called Scrollbar.maximum\ncalled Scrollbar.setMaximum with value `161`\n"
                "called Scrollbar.maximum\ncalled Scrollbar.setValue with value `99`\n")
        testobj.add_row(name='xx', value='yy', desc='zz')
        assert testobj.rownum == 4
        assert len(testobj.checks) == 2
        assert isinstance(testobj.checks[1], testee.qtw.QCheckBox)
        assert len(testobj.data) == 2
        assert len(testobj.data[0]) == 3
        assert isinstance(testobj.data[1][0], testee.qtw.QLineEdit)
        assert isinstance(testobj.data[1][1], testee.qtw.QLineEdit)
        assert isinstance(testobj.data[1][2], testee.qtw.QLineEdit)
        assert capsys.readouterr().out == (
                "called CheckBox.__init__\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockCheckBox'> at (3, 0)\n"
                "called LineEdit.__init__\n"
                "called LineEdit.setFixedWidth with arg `88`\n"
                "called LineEdit.setReadOnly with arg `True`\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockLineEdit'> at (3, 1)\n"
                "called LineEdit.__init__\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockLineEdit'> at (3, 2)\n"
                "called LineEdit.__init__\n"
                "called Grid.addWidget with arg of type"
                " <class 'mockgui.mockqtwidgets.MockLineEdit'> at (4, 2)\n"
                "called Scrollbar.maximum\ncalled Scrollbar.setMaximum with value `161`\n"
                "called Scrollbar.maximum\ncalled Scrollbar.setValue with value `99`\n")

    def test_delete_row(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.delete_row
        """
        check = mockqtw.MockCheckBox()
        w_name = mockqtw.MockLineEdit()
        w_value = mockqtw.MockLineEdit()
        w_desc = mockqtw.MockLineEdit()
        gsizer = mockqtw.MockGridLayout()
        assert capsys.readouterr().out == ("called CheckBox.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called Grid.__init__\n")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.checks = ['', check]
        testobj.data = [[], [w_name, w_value, w_desc]]
        testobj.gsizer = gsizer
        testobj.delete_row(1)
        assert testobj.checks == ['']
        assert testobj.data == [[]]
        assert capsys.readouterr().out == ("called Grid.removeWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           "called CheckBox.close\n"
                                           "called Grid.removeWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLineEdit'>\n"
                                           "called LineEdit.close\n"
                                           "called Grid.removeWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLineEdit'>\n"
                                           "called LineEdit.close\n"
                                           "called Grid.removeWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLineEdit'>\n"
                                           "called LineEdit.close\n")

    def test_add_setting(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.add_setting
        """
        def mock_add():
            print('called ExtraSettingsDialog.add_row')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_row = mock_add
        testobj.add_setting()
        assert capsys.readouterr().out == ("called ExtraSettingsDialog.add_row\n")

    def test_remove_settings(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.remove_settings
        """
        def mock_ask(*args):
            print('called ask_question with args', args)
            return False
        def mock_ask_2(*args):
            print('called ask_question with args', args)
            return True
        def mock_delete(num):
            print(f'called delete_row with arg {num}')
        check1 = mockqtw.MockCheckBox()
        check2 = mockqtw.MockCheckBox()
        check2.setChecked(True)
        check3 = mockqtw.MockCheckBox()
        check3.setChecked(True)
        assert capsys.readouterr().out == ("called CheckBox.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n"
                                           "called CheckBox.__init__\n"
                                           "called CheckBox.setChecked with arg True\n")
        monkeypatch.setattr(testee, 'ask_question', mock_ask)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.delete_row = mock_delete
        testobj.checks = [check1]
        testobj.remove_settings()
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")
        testobj.checks = [check1, check2, check3]
        testobj.remove_settings()
        assert capsys.readouterr().out == (
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called ask_question with args ({testobj.parent}, 'Q_REMSET')\n")
        monkeypatch.setattr(testee, 'ask_question', mock_ask_2)
        testobj.remove_settings()
        assert capsys.readouterr().out == (
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                "called CheckBox.isChecked\n"
                f"called ask_question with args ({testobj.parent}, 'Q_REMSET')\n"
                "called delete_row with arg 2\n"
                "called delete_row with arg 1\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for ExtraSettingsDialog.accept
        """
        def mock_accept(*args):
            print('called ExtraSettingsDialog.accept_extrasettings with args', args)
            return False
        def mock_accept_2(*args):
            print('called ExtraSettingsDialog.accept_extrasettings with args', args)
            return True
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(accept_extrasettings=mock_accept)
        testobj.c_rebuild = mockqtw.MockCheckBox()
        testobj.c_showdet = mockqtw.MockCheckBox()
        testobj.c_redef = mockqtw.MockCheckBox()
        w1 = mockqtw.MockLineEdit('xx')
        w2 = mockqtw.MockLineEdit('yy')
        w3 = mockqtw.MockLineEdit('zz')
        testobj.t_program = mockqtw.MockLineEdit('aaa')
        testobj.t_title = mockqtw.MockLineEdit('bbbb')
        assert capsys.readouterr().out == ("called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n"
                                           "called LineEdit.__init__\ncalled LineEdit.__init__\n")
        testobj.data = [(w1, w2, w3)]
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\ncalled LineEdit.text\n"
                "called LineEdit.text\ncalled LineEdit.text\n"
                "called LineEdit.text\ncalled CheckBox.isChecked\n"
                "called CheckBox.isChecked\ncalled CheckBox.isChecked\n"
                "called ExtraSettingsDialog.accept_extrasettings with args"
                " ('aaa', 'bbbb', False, False, False, [('xx', 'yy', 'zz')])\n"
                "called CheckBox.setChecked with arg False\n"
                "called CheckBox.setChecked with arg False\n")
        testobj.master.accept_extrasettings = mock_accept_2
        testobj.accept()
        assert capsys.readouterr().out == (
                "called LineEdit.text\ncalled LineEdit.text\n"
                "called LineEdit.text\ncalled LineEdit.text\n"
                "called LineEdit.text\ncalled CheckBox.isChecked\n"
                "called CheckBox.isChecked\ncalled CheckBox.isChecked\n"
                "called ExtraSettingsDialog.accept_extrasettings with args"
                " ('aaa', 'bbbb', False, False, False, [('xx', 'yy', 'zz')])\n"
                "called Dialog.accept\n")


class TestEntryDialog:
    """unittest for dialogs_qt.EntryDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.EntryDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called EntryDialog.__init__ with args', args)
        monkeypatch.setattr(testee.EntryDialog, '__init__', mock_init)
        testobj = testee.EntryDialog()
        testobj.parent = mockqtw.MockFrame()
        testobj.parent.master = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called EntryDialog.__init__ with args ()\n'
                                           "called Frame.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for EntryDialog.__init__
        """
        def mock_add(*args):
            "stub"
        def mock_delete(*args):
            "stub"
        def mock_addbutton(self, *args):
            print('called ButtonBox.addButton with args', args)
            return mockqtw.MockPushButton()
        parent = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        master = types.SimpleNamespace(title='title',
                                       captions={'XX': 'xxxx', 'YY': 'yyyy', 'C_ADDKEY': 'add',
                                                 'C_REMKEY': 'remove'})
        master.book = types.SimpleNamespace(page=types.SimpleNamespace())
        master.book.page.column_info = [('XX', 1), ('YY', 2)]
        master.book.page.data = {}
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        monkeypatch.setattr(testee.qtw, 'QTableWidgetItem', mockqtw.MockTableItem)
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        monkeypatch.setattr(mockqtw.MockButtonBox, 'addButton', mock_addbutton)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.EntryDialog, 'add_key', mock_add)
        monkeypatch.setattr(testee.EntryDialog, 'delete_key', mock_delete)
        testobj = testee.EntryDialog(parent, master)
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.p0list, testee.qtw.QTableWidget)
        assert testobj.numrows == len(master.book.page.data)
        assert capsys.readouterr().out == expected_output['entry'].format(testobj=testobj)

        master.book.page.data = {1: ['xx', 'yy'], 2: ['aa', 'bb']}
        testobj = testee.EntryDialog(parent, master)
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert isinstance(testobj.p0list, testee.qtw.QTableWidget)
        assert testobj.numrows == len(master.book.page.data)
        assert capsys.readouterr().out == expected_output['entry2'].format(testobj=testobj)

    def test_add_key(self, monkeypatch, capsys):
        """unittest for EntryDialog.add_key
        """
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        monkeypatch.setattr(testee.qtw, 'QTableWidgetItem', mockqtw.MockTableItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = testee.qtw.QTableWidget()
        testobj.p0list.setColumnCount(2)
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n"
                                           "called Table.setColumnCount with arg '2'\n")
        testobj.numrows = 1
        testobj.add_key()
        assert testobj.numrows == 2
        assert capsys.readouterr().out == (
                "called Table.insertRow with arg '1'\n"
                "called Table.columnCount\n"
                "called TableItem.__init__ with arg xy\n"
                "called TableItem.settext with arg \n"
                "called Table.setItem with args"
                " (1, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg xy\n"
                "called TableItem.settext with arg \n"
                "called Table.setItem with args"
                " (1, 1, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called Table.scrollToBottom\n")

    def test_delete_key(self, monkeypatch, capsys):
        """unittest for EntryDialog.delete_key
        """
        def mock_selected():
            print('called Table.selectedRanges')
            return [mockqtw.MockTableSelectionRange(0, 1, 1, 1)]
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = testee.qtw.QTableWidget()
        testobj.p0list.setRowCount(2)
        testobj.p0list.selectedRanges = mock_selected
        testobj.delete_key()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\n"
                                           "called Header.__init__\n"
                                           "called Table.setRowCount with arg '2'\n"
                                           "called Table.selectedRanges\n"
                                           "called TableRange.__init__ with args (0, 1, 1, 1)\n"
                                           "called TableRange.rowCount\n"
                                           "called TableRange.topRow\n"
                                           "called TableRange.topRow\n"
                                           "called Table.removeRow with arg '1'\n"
                                           "called Table.removeRow with arg '0'\n")

    def test_accept(self, monkeypatch, capsys):
        """unittest for EntryDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace(
                book=types.SimpleNamespace(page=types.SimpleNamespace()))
        testobj.p0list = testee.qtw.QTableWidget()
        testobj.p0list.setRowCount(2)
        testobj.p0list.setColumnCount(2)
        for x, y in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            testobj.p0list.setItem(x, y, mockqtw.MockTableItem(f"{x}x{y}"))
        assert capsys.readouterr().out == (
                "called Table.__init__ with args ()\n"
                "called Header.__init__\n"
                "called Header.__init__\n"
                "called Table.setRowCount with arg '2'\n"
                "called Table.setColumnCount with arg '2'\n"
                "called TableItem.__init__ with arg 0x0\n"
                "called Table.setItem with args"
                " (0, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg 0x1\n"
                "called Table.setItem with args"
                " (0, 1, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg 1x0\n"
                "called Table.setItem with args"
                " (1, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg 1x1\n"
                "called Table.setItem with args"
                " (1, 1, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n")
        testobj.accept()
        assert testobj.master.book.page.data == {1: ['0x0', '0x1'], 2: ['1x0', '1x1']}
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.columnCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (0, 1)\n"
                                           "called Table.columnCount\n"
                                           "called Table.item with args (1, 0)\n"
                                           "called Table.item with args (1, 1)\n"
                                           "called Dialog.accept\n")


class TestCompleteDialog:
    """unittest for dialogs_qt.CompleteDialog
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for dialogs_qt.CompleteDialog object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called CompleteDialog.__init__ with args', args)
        monkeypatch.setattr(testee.CompleteDialog, '__init__', mock_init)
        testobj = testee.CompleteDialog()
        testobj.parent = mockqtw.MockFrame()
        testobj.parent.master = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called CompleteDialog.__init__ with args ()\n'
                                           "called Frame.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys, expected_output):
        """unittest for CompleteDialog.__init__
        """
        def mock_get(*args):
            print('called shared.get_text with args', args)
        def mock_read(self):
            print('called CompleteDialog.read_data')
            self.cmds = ['xxx', 'yyy', 'zzz']
        def mock_build(self):
            print('called CompleteDialog.build_table')
        parent = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        master = types.SimpleNamespace()
        monkeypatch.setattr(testee.shared, 'get_text', mock_get)
        monkeypatch.setattr(testee.qtw.QDialog, '__init__', mockqtw.MockDialog.__init__)
        monkeypatch.setattr(testee.qtw.QDialog, 'setWindowTitle', mockqtw.MockDialog.setWindowTitle)
        monkeypatch.setattr(testee.qtw.QDialog, 'resize', mockqtw.MockDialog.resize)
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw.QDialog, 'reject', mockqtw.MockDialog.reject)
        monkeypatch.setattr(testee.qtw.QDialog, 'setLayout', mockqtw.MockDialog.setLayout)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        monkeypatch.setattr(testee.qtw, 'QDialogButtonBox', mockqtw.MockButtonBox)
        monkeypatch.setattr(testee.CompleteDialog, 'read_data', mock_read)
        monkeypatch.setattr(testee.CompleteDialog, 'build_table', mock_build)
        testobj = testee.CompleteDialog(parent, master)
        assert isinstance(testobj.p0list, testee.qtw.QTableWidget)
        assert isinstance(testobj.sizer, testee.qtw.QVBoxLayout)
        assert capsys.readouterr().out == expected_output['complete'].format(testobj=testobj)

    def test_accept(self, monkeypatch, capsys):
        """unittest for CompleteDialog.accept
        """
        monkeypatch.setattr(testee.qtw.QDialog, 'accept', mockqtw.MockDialog.accept)
        monkeypatch.setattr(testee.qtw, 'QTableWidget', mockqtw.MockTable)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master = types.SimpleNamespace()
        testobj.p0list = testee.qtw.QTableWidget()
        assert capsys.readouterr().out == ("called Table.__init__ with args ()\n"
                                           "called Header.__init__\ncalled Header.__init__\n")
        testobj.accept()
        assert testobj.master.dialog_data == {}
        assert capsys.readouterr().out == ("called Table.rowCount\ncalled Dialog.accept\n")
        testobj.p0list.setRowCount(2)
        testobj.p0list.setColumnCount(2)
        for x, y in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            testobj.p0list.setItem(x, y, mockqtw.MockTableItem(f"{x}x{y}"))
        assert capsys.readouterr().out == (
                "called Table.setRowCount with arg '2'\n"
                "called Table.setColumnCount with arg '2'\n"
                "called TableItem.__init__ with arg 0x0\n"
                "called Table.setItem with args"
                " (0, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg 0x1\n"
                "called Table.setItem with args"
                " (0, 1, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg 1x0\n"
                "called Table.setItem with args"
                " (1, 0, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n"
                "called TableItem.__init__ with arg 1x1\n"
                "called Table.setItem with args"
                " (1, 1, item of <class 'mockgui.mockqtwidgets.MockTableItem'>)\n")
        testobj.accept()
        assert testobj.master.dialog_data == {'0x0': '0x1', '1x0': '1x1'}
        assert capsys.readouterr().out == ("called Table.rowCount\n"
                                           "called Table.item with args (0, 0)\n"
                                           "called Table.item with args (0, 1)\n"
                                           "called Table.item with args (1, 0)\n"
                                           "called Table.item with args (1, 1)\n"
                                           "called Dialog.accept\n")

    def test_read_data(self, monkeypatch, capsys):
        """unittest for CompleteDialog.read_data
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        with pytest.raises(NotImplementedError):
            testobj.read_data()

    def _test_build_table(self, monkeypatch, capsys):
        """unittest for CompleteDialog.build_table
        """
        # not implemented, see docstring in testee
        # testobj = self.setup_testobj(monkeypatch, capsys)
        # assert testobj.build_table() == "expected_result"
        # assert capsys.readouterr().out == ("")


def test_show_dialog(monkeypatch, capsys):
    """unittest for dialogs_qt.show_dialog
    """
    def mock_exec(self):
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Rejected
    def mock_exec_2(self):
        print('called Dialog.exec')
        return testee.qtw.QDialog.DialogCode.Accepted
    cls = mockqtw.MockDialog
    win = types.SimpleNamespace(gui=mockqtw.MockFrame())
    assert capsys.readouterr().out == "called Frame.__init__\n"
    monkeypatch.setattr(mockqtw.MockDialog, 'exec', mock_exec)
    assert not testee.show_dialog(win, cls)
    assert capsys.readouterr().out == (f"called Dialog.__init__ with args {win.gui} ({win},) {{}}\n"
                                       "called Dialog.exec\n")
    monkeypatch.setattr(mockqtw.MockDialog, 'exec', mock_exec_2)
    assert testee.show_dialog(win, cls)
    assert capsys.readouterr().out == (f"called Dialog.__init__ with args {win.gui} ({win},) {{}}\n"
                                       "called Dialog.exec\n")
