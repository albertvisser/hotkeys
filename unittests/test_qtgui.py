"""unittests for ./editor/gui_qt.py
"""
import types
import pytest
from mockgui import mockqtwidgets as mockqtw
from editor import gui_qt as testee

maingui = """\
called Frame.__init__
called VBox.__init__
called VBox.addWidget with arg of type <class 'test_qtgui.MockTabbedInterface'>
called HBox.__init__
called HBox.addStretch
called PushButton.__init__ with args ('Exit text', {testobj}) {{}}
called Signal.connect with args ({testobj.editor.exit},)
called PushButton.setDefault with arg `True`
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called MainWidget.setCentralWindow with arg of type `<class 'mockgui.mockqtwidgets.MockFrame'>`
called MainWindow.show
called Application.exec
"""
empty = """\
called VBox.__init__
called HBox.__init__
called HBox.addStretch
called Label.__init__ with args ('nodata', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addStretch
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
"""
tabbed1 = """\
called ComboBox.__init__
called ComboBox.setMinimumContentsLength with arg 5
called ComboBox.setEditable with arg `False`
called ComboBox.__init__
called ComboBox.setMinimumContentsLength with arg 20
called ComboBox.setEditable with arg `True`
called Signal.connect with args ({testobj.master.on_text_changed},)
called PushButton.__init__ with args ('', {testobj}) {{}}
called Signal.connect with args ({testobj.master.find_next},)
called PushButton.setEnabled with arg `False`
called PushButton.__init__ with args ('', {testobj}) {{}}
called Signal.connect with args ({testobj.master.find_prev},)
called PushButton.setEnabled with arg `False`
called PushButton.__init__ with args ('xxx', {testobj}) {{}}
called Signal.connect with args ({testobj.master.filter},)
called PushButton.setEnabled with arg `False`
"""
tabbed2 = """\
called ComboBox.__init__
called ComboBox.__init__
called ComboBox.__init__
called PushButton.__init__ with args () {{}}
called PushButton.__init__ with args () {{}}
called PushButton.__init__ with args () {{}}
called StackedWidget.__init__
called VBox.__init__
called HBox.__init__
called HBox.addSpacing
called Label.__init__ with args ('', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called HBox.addStretch
called Label.__init__ with args ('', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called Label.__init__ with args (':', {testobj})
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockLabel'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockComboBox'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addSpacing
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockStackedWidget'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called TabbedInterface.setcaptions
"""
sdilist_start = """\
called VBox.__init__
"""
sdilist_middle = """\
called Tree.setHeaderLabels with arg `['Xxx']`
called Tree.setAlternatingRowColors with arg True
called Signal.connect with args ({testobj.on_item_selected},)
called Tree.header
called Header.__init__
called Header.setSectionsClickable with value True
called Header.resizeSection for col 0 width 10
called Header.setStretchLastSection with arg True
called HotkeyPanel.populate_list
called Tree.setSortingEnabled with arg True
called HBox.__init__
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockTreeWidget'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called SingleDataInterface.layout_extra_fields with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
"""
sdilist_end = """\
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called SingleDataInterface.set_listselection with arg 0
"""
sdiextra_start = """\
called VBox.__init__
called VBox.__init__
called HBox.__init__
called HBox.__init__
called fieldhandler.layout_keymodfields
called HBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.addStretch
called fieldhandler.layout_commandfields
"""
sdiextra_middle_11 = """\
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called HBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockPushButton'>
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
"""
sdiextra_middle_12 = "called fieldhandler.layout_descfield\n"
sdiextra_middle_21 = "called plugin.layout_extra_fields_topline\n"
sdiextra_middle_22 = """\
called plugin.layout_extra_fields_nextline
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called HBox.__init__
"""
sdiextra_middle_23 = "called plugin.layout_extra_fields\n"
sdiextra_end = """\
called VBox.addLayout with arg of type <class 'mockgui.mockqtwidgets.MockHBoxLayout'>
called Frame.setLayout with arg of type <class 'mockgui.mockqtwidgets.MockVBoxLayout'>
called VBox.addWidget with arg of type <class 'mockgui.mockqtwidgets.MockFrame'>
"""

@pytest.fixture
def expected_output():
    """generic fixture for ouput expectations
    """
    return {'emptyscreen': empty, "maingui": maingui, "tabbed_search": tabbed1,
            "tabbed_screen": tabbed2, 'sdi_list_1': sdilist_start + sdilist_end,
            'sdi_list_2': sdilist_start + sdilist_middle + sdilist_end,
            'sdi_extra_1': sdiextra_start + sdiextra_middle_11 + sdiextra_middle_12 + sdiextra_end,
            'sdi_extra_2': (sdiextra_start + sdiextra_middle_21 + sdiextra_middle_11
                            + sdiextra_middle_22 + sdiextra_middle_12 + sdiextra_middle_23
                            + sdiextra_end)}


class MockGui:
    """testdouble for gui.Gui object
    """


class MockTabbedInterface:
    """testdouble for gui_qt.TabbedInterface object
    """


class MockSDI:
    """testdouble for gui_qt.SingleDataInterface object
    """


class MockHotkeyPanel:
    """testdouble for main.HotkeyPanel object
    """
    def process_changed_selection(self, *args):
        "stub for method call"
        print('called HotkeyPanel.process_changed_selection with args', args)
    def apply_changes(self):
        "stub for method call"
        print('called HotkeyPanel.apply_changes')
    def apply_deletion(self):
        "stub for method call"
        print('called HotkeyPanel.apply_deletion')


class MockChoiceBook:
    """testdouble for main.TabbedWidget object
    """
    def __init__(self):
        self.gui = MockTabbedInterface()
        self.page = MockHotkeyPanel()
    def on_page_changed(self):
        "stub for method call"
    def on_text_changed(self):
        "stub for method call"
    def find_next(self):
        "stub for method call"
    def find_prev(self):
        "stub for method call"
    def filter(self):
        "stub for method call"


class MockEditor:
    """testdouble for main.Editor object
    """
    def __init__(self):
        self.book = MockChoiceBook()


class TestFieldHandler:
    """unittests for gui.FieldHandler
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.FieldHandler object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called FieldHandler.__init__ with args', args)
        monkeypatch.setattr(testee.FieldHandler, '__init__', mock_init)
        testobj = testee.FieldHandler()
        testobj.gui = types.SimpleNamespace()
        testobj.master = types.SimpleNamespace()
        assert capsys.readouterr().out == 'called FieldHandler.__init__ with args ()\n'
        return testobj

    def test_init(self):
        """unittest for FieldHandler.__init__
        """
        gui = types.SimpleNamespace(master=types.SimpleNamespace())
        testobj = testee.FieldHandler(gui)
        assert testobj.gui == gui
        assert testobj.master == gui.master

    def test_build_fields(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_fields
        """
        def mock_key():
            print("called FieldHandler.build_keyfield")
        def mock_mods():
            print("called FieldHandler.build_modfields")
        def mock_context():
            print("called FieldHandler.build_context_field")
        def mock_command():
            print("called FieldHandler.build_command_field")
        def mock_parms():
            print("called FieldHandler.build_parms_field")
        def mock_control():
            print("called FieldHandler.build_control_field")
        def mock_preparms():
            print("called FieldHandler.build_preparms_field")
        def mock_postparms():
            print("called FieldHandler.build_postparms_field")
        def mock_feature():
            print("called FieldHandler.build_featurefield")
        def mock_desc():
            print("called FieldHandler.build_descfield")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.build_keyfield = mock_key
        testobj.build_modfields = mock_mods
        testobj.build_context_field = mock_context
        testobj.build_command_field = mock_command
        testobj.build_parms_field = mock_parms
        testobj.build_control_field = mock_control
        testobj.build_preparms_field = mock_preparms
        testobj.build_postparms_field = mock_postparms
        testobj.build_featurefield = mock_feature
        testobj.build_descfield = mock_desc

        testobj.master.fields = []
        testobj.build_fields()
        assert capsys.readouterr().out == ""
        testobj.master.fields = ['C_KEY', 'C_MODS', 'C_CNTXT', 'C_CMD', 'C_PARMS', 'C_CTRL',
                                 'C_BPARMS', 'C_APARMS', 'C_FEAT', 'C_DESC']
        testobj.build_fields()
        assert capsys.readouterr().out == ("called FieldHandler.build_keyfield\n"
                                           "called FieldHandler.build_modfields\n"
                                           "called FieldHandler.build_context_field\n"
                                           "called FieldHandler.build_command_field\n"
                                           "called FieldHandler.build_parms_field\n"
                                           "called FieldHandler.build_control_field\n"
                                           "called FieldHandler.build_preparms_field\n"
                                           "called FieldHandler.build_postparms_field\n"
                                           "called FieldHandler.build_featurefield\n"
                                           "called FieldHandler.build_descfield\n")

    def test_build_keyfield(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_keyfield
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        monkeypatch.setattr(mockqtw.MockLineEdit, 'textChanged', {str: mockqtw.MockSignal()})
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentTextChanged', {str: mockqtw.MockSignal()})
        assert capsys.readouterr().out == "called Signal.__init__\ncalled Signal.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.screenfields = []
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.master.on_text = lambda *x: 'x'
        testobj.master.on_combobox = lambda *x: 'x'
        testobj.master.captions = {'C_KTXT': 'xxx'}
        testobj.master.keylist = None
        testobj.build_keyfield()
        assert isinstance(testobj.gui.lbl_key, testee.qtw.QLabel)
        assert isinstance(testobj.gui.txt_key, testee.qtw.QLineEdit)
        assert testobj.gui.screenfields == [testobj.gui.txt_key]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx ', {testobj.gui.frm})\n"
                "called LineEdit.__init__\n"
                "called LineEdit.setMaximumWidth with arg `90`\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_text},"
                f" {testobj.gui.txt_key}, <class 'str'>),)\n")
        testobj.master.keylist = ['x']
        testobj.gui.screenfields = []
        testobj.build_keyfield()
        assert isinstance(testobj.gui.lbl_key, testee.qtw.QLabel)
        assert isinstance(testobj.gui.cmb_key, testee.qtw.QComboBox)
        assert testobj.gui.screenfields == [testobj.gui.cmb_key]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx ', {testobj.gui.frm})\n"
                "called ComboBox.__init__\n"
                "called ComboBox.setMaximumWidth with arg `90`\n"
                "called ComboBox.addItems with arg ['x']\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_combobox},"
                f" {testobj.gui.cmb_key}, <class 'str'>),)\n")

    def test_build_modfields(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_modfields
        """
        monkeypatch.setattr(testee.qtw, 'QCheckBox', mockqtw.MockCheckBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.screenfields = []
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.master.on_checkbox = lambda *x: 'x'
        testobj.master.captions = {'M_CTRL': 'xxx', 'M_ALT': 'yyy', 'M_SHFT': 'zzz', 'M_WIN': 'qqq'}
        testobj.build_modfields()
        assert isinstance(testobj.gui.cb_ctrl, testee.qtw.QCheckBox)
        assert isinstance(testobj.gui.cb_alt, testee.qtw.QCheckBox)
        assert isinstance(testobj.gui.cb_shift, testee.qtw.QCheckBox)
        assert isinstance(testobj.gui.cb_win, testee.qtw.QCheckBox)
        assert testobj.gui.screenfields == [testobj.gui.cb_ctrl, testobj.gui.cb_alt,
                                            testobj.gui.cb_shift, testobj.gui.cb_win]
        assert capsys.readouterr().out == (
                "called CheckBox.__init__\n"
                "called CheckBox.setChecked with arg False\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_checkbox},"
                f" {testobj.gui.cb_ctrl}),)\n"
                "called CheckBox.__init__\n"
                "called CheckBox.setChecked with arg False\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_checkbox},"
                f" {testobj.gui.cb_alt}),)\n"
                "called CheckBox.__init__\n"
                "called CheckBox.setChecked with arg False\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_checkbox},"
                f" {testobj.gui.cb_shift}),)\n"
                "called CheckBox.__init__\n"
                "called CheckBox.setChecked with arg False\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_checkbox},"
                f" {testobj.gui.cb_win}),)\n")

    def test_build_context_field(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_context_field
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentTextChanged', {str: mockqtw.MockSignal()})
        assert capsys.readouterr().out == "called Signal.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.screenfields = []
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.master.captions = {'C_CNTXT': 'xxx'}
        testobj.master.contextslist = ['x']
        testobj.master.on_combobox = lambda *x: 'x'
        testobj.build_context_field()
        assert isinstance(testobj.gui.lbl_context, testee.qtw.QLabel)
        assert isinstance(testobj.gui.cmb_context, testee.qtw.QComboBox)
        assert testobj.gui.screenfields == [testobj.gui.cmb_context]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx', {testobj.gui.frm})\n"
                "called ComboBox.__init__\n"
                "called ComboBox.addItems with arg ['x']\n"
                "called ComboBox.setMaximumWidth with arg `110`\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_combobox},"
                f" {testobj.gui.cmb_context}, <class 'str'>),)\n")

    def test_build_command_field(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_command_field
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentTextChanged', {str: mockqtw.MockSignal()})
        assert capsys.readouterr().out == "called Signal.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.screenfields = []
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.master.captions = {'C_CTXT': 'xxx'}
        testobj.master.commandslist = ['x']
        testobj.master.on_combobox = lambda *x: 'x'
        testobj.master.fields = []
        testobj.build_command_field()
        assert isinstance(testobj.gui.txt_cmd, testee.qtw.QLabel)
        assert isinstance(testobj.gui.cmb_commando, testee.qtw.QComboBox)
        assert testobj.gui.screenfields == [testobj.gui.cmb_commando]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx ', {testobj.gui.frm})\n"
                "called ComboBox.__init__\n"
                "called ComboBox.setMaximumWidth with arg `150`\n"
                "called ComboBox.addItems with arg ['x']\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_combobox},"
                f" {testobj.gui.cmb_commando}, <class 'str'>),)\n")
        testobj.gui.screenfields = []
        testobj.master.fields = ['C_CNTXT']
        testobj.build_command_field()
        assert isinstance(testobj.gui.txt_cmd, testee.qtw.QLabel)
        assert isinstance(testobj.gui.cmb_commando, testee.qtw.QComboBox)
        assert testobj.gui.screenfields == [testobj.gui.cmb_commando]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx ', {testobj.gui.frm})\n"
                "called ComboBox.__init__\n"
                "called ComboBox.setMaximumWidth with arg `150`\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_combobox},"
                f" {testobj.gui.cmb_commando}, <class 'str'>),)\n")

    def test_build_parms_field(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_parms_field
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.screenfields = []
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.master.captions = {'C_PARMS': 'xxx'}
        testobj.build_parms_field()
        assert isinstance(testobj.gui.lbl_parms, testee.qtw.QLabel)
        assert isinstance(testobj.gui.txt_parms, testee.qtw.QLineEdit)
        assert testobj.gui.screenfields == [testobj.gui.txt_parms]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx', {testobj.gui.frm})\n"
                "called LineEdit.__init__\n"
                "called LineEdit.setMaximumWidth with arg `280`\n")

    def test_build_control_field(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_control_field
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(mockqtw.MockComboBox, 'currentTextChanged', {str: mockqtw.MockSignal()})
        assert capsys.readouterr().out == "called Signal.__init__\n"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.screenfields = []
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.master.captions = {'C_CTRL': 'xxx'}
        testobj.master.controlslist = ['x']
        testobj.master.on_combobox = lambda *x: 'x'
        testobj.build_control_field()
        assert isinstance(testobj.gui.cmb_controls, testee.qtw.QComboBox)
        assert testobj.gui.screenfields == [testobj.gui.cmb_controls]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ('xxx', {testobj.gui.frm})\n"
                "called ComboBox.__init__\n"
                "called ComboBox.addItems with arg ['x']\n"
                f"called Signal.connect with args (functools.partial({testobj.master.on_combobox},"
                f" {testobj.gui.cmb_controls}, <class 'str'>),)\n")

    def test_build_preparms_field(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_preparms_field
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.screenfields = []
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.build_preparms_field()
        assert isinstance(testobj.gui.pre_parms_label, testee.qtw.QLabel)
        assert isinstance(testobj.gui.pre_parms_text, testee.qtw.QLineEdit)
        assert testobj.gui.screenfields == [testobj.gui.pre_parms_text]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ({testobj.gui.frm},)\n"
                "called LineEdit.__init__\n")

    def test_build_postparms_field(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_postparms_field
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QLineEdit', mockqtw.MockLineEdit)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.screenfields = []
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.build_postparms_field()
        assert isinstance(testobj.gui.post_parms_label, testee.qtw.QLabel)
        assert isinstance(testobj.gui.post_parms_text, testee.qtw.QLineEdit)
        assert testobj.gui.screenfields == [testobj.gui.post_parms_text]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ({testobj.gui.frm},)\n"
                "called LineEdit.__init__\n")

    def test_build_feature_field(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_feature_field
        """
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.screenfields = []
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.master.featurelist = ['x']
        testobj.build_featurefield()
        assert isinstance(testobj.gui.feature_label, testee.qtw.QLabel)
        assert isinstance(testobj.gui.feature_select, testee.qtw.QComboBox)
        assert testobj.gui.screenfields == [testobj.gui.feature_select]
        assert capsys.readouterr().out == (
                f"called Label.__init__ with args ({testobj.gui.frm},)\n"
                "called ComboBox.__init__\n"
                "called ComboBox.addItems with arg ['x']\n")

    def test_build_desc_field(self, monkeypatch, capsys):
        """unittest for FieldHandler.build_desc_field
        """
        monkeypatch.setattr(testee.qtw, 'QTextEdit', mockqtw.MockEditorWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.frm = mockqtw.MockFrame()
        assert capsys.readouterr().out == "called Frame.__init__\n"
        testobj.build_descfield()
        assert isinstance(testobj.gui.txt_oms, testee.qtw.QTextEdit)
        assert capsys.readouterr().out == (f"called Editor.__init__ with args ({testobj.gui.frm},)\n"
                                           "called Editor.setReadOnly with arg `True`\n")

    def test_layout_keymodfields(self, monkeypatch, capsys):
        """unittest for FieldHandler.layout_keymodfields
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.lbl_key = mockqtw.MockLabel()
        testobj.gui.txt_key = mockqtw.MockLineEdit()
        testobj.gui.cmb_key = mockqtw.MockComboBox()
        testobj.gui.cb_ctrl = mockqtw.MockCheckBox()
        testobj.gui.cb_alt = mockqtw.MockCheckBox()
        testobj.gui.cb_shift = mockqtw.MockCheckBox()
        testobj.gui.cb_win = mockqtw.MockCheckBox()
        sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == ("called Label.__init__\ncalled LineEdit.__init__\n"
                                           "called ComboBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled CheckBox.__init__\n"
                                           "called CheckBox.__init__\ncalled VBox.__init__\n")
        testobj.master.fields = ['C_KEY']
        testobj.master.keylist = None
        testobj.layout_keymodfields(sizer)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'>\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLineEdit'>\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n")
        testobj.master.keylist = ['x']
        testobj.layout_keymodfields(sizer)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'>\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockComboBox'>\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n")
        testobj.master.fields = ['C_MODS']
        testobj.layout_keymodfields(mockqtw.MockVBoxLayout())
        assert capsys.readouterr().out == ("called VBox.__init__\ncalled HBox.__init__\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockCheckBox'>\n"
                                           "called HBox.addStretch\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n")

    def test_layout_commandfields(self, monkeypatch, capsys):
        """unittest for FieldHandler.layout_commandfields
        """
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.lbl_context = mockqtw.MockLabel()
        testobj.gui.cmb_context = mockqtw.MockComboBox()
        testobj.gui.txt_cmd = mockqtw.MockLineEdit()
        testobj.gui.cmb_commando = mockqtw.MockComboBox()
        sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == ("called Label.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called LineEdit.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called VBox.__init__\n")
        testobj.master.fields = ['C_CNTXT']
        testobj.layout_commandfields(sizer)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLabel'>\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockComboBox'>\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n")
        testobj.master.fields = ['C_CMD']
        testobj.layout_commandfields(sizer)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockLineEdit'>\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockComboBox'>\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n")

    def test_layout_descfield(self, monkeypatch, capsys):
        """unittest for FieldHandler.layout_descfield
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.txt_oms = mockqtw.MockEditorWidget()
        sizer = mockqtw.MockVBoxLayout()
        assert capsys.readouterr().out == ("called Editor.__init__\ncalled VBox.__init__\n")
        testobj.master.fields = []
        testobj.layout_descfield(sizer)
        assert capsys.readouterr().out == ""
        testobj.master.fields = ['C_DESC']
        testobj.layout_descfield(sizer)
        assert capsys.readouterr().out == ("called HBox.__init__\n"
                                           "called HBox.addWidget with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockEditorWidget'>\n"
                                           "called VBox.addLayout with arg of type"
                                           " <class 'mockgui.mockqtwidgets.MockHBoxLayout'>\n")


class TestSingleDataInterface:
    """unittests for gui_qt.SingleDataInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.SingleDataInterface object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called SingleDataInterface.__init__ with args', args)
        monkeypatch.setattr(testee.SingleDataInterface, '__init__', mock_init)
        testobj = testee.SingleDataInterface()
        testobj.parent = MockTabbedInterface()
        testobj.master = MockHotkeyPanel()
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args ()\n'
                                           "called Tree.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.__init__
        """
        monkeypatch.setattr(testee.qtw.QFrame, '__init__', mockqtw.MockFrame.__init__)
        monkeypatch.setattr(testee.qtw, 'QTreeWidget', mockqtw.MockTreeWidget)
        testobj = testee.SingleDataInterface('parent', 'master')
        assert testobj.parent == 'parent'
        assert testobj.master == 'master'
        assert isinstance(testobj.p0list, testee.qtw.QTreeWidget)
        assert isinstance(testobj.fieldhandler, testee.FieldHandler)
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called Tree.__init__\n")

    def test_setup_empty_screen(self, monkeypatch, capsys, expected_output):
        """unittest for SingleDataInterface.setup_empty_screen
        """
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.SingleDataInterface, 'setLayout', mockqtw.MockFrame.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setup_empty_screen('nodata', 'title')
        assert testobj.title == 'title'
        assert capsys.readouterr().out == expected_output['emptyscreen'].format(testobj=testobj)

    def test_setup_list(self, monkeypatch, capsys, expected_output):
        """unittest for SingleDataInterface.setup_list
        """
        def mock_populate():
            print('called HotkeyPanel.populate_list')
        def mock_layout(arg):
            print(f'called SingleDataInterface.layout_extra_fields with arg of type {type(arg)}')
        def mock_set(arg):
            print(f'called SingleDataInterface.set_listselection with arg {arg}')
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.p0list = mockqtw.MockTreeWidget()
        testobj.master.column_info = []
        testobj.master.captions = {'xxx': 'Xxx'}
        testobj.master.has_extrapanel = False
        testobj.master.populate_list = mock_populate
        testobj.layout_extra_fields = mock_layout
        monkeypatch.setattr(testee.qtw.QFrame, 'setLayout', mockqtw.MockFrame.setLayout)
        testobj.set_listselection = mock_set
        testobj.setup_list()
        assert capsys.readouterr().out == expected_output['sdi_list_1'].format(testobj=testobj)
        testobj.master.column_info = [('xxx', 10)]
        testobj.master.has_extrapanel = True
        testobj.setup_list()
        assert capsys.readouterr().out == expected_output['sdi_list_2'].format(testobj=testobj)

    def test_add_extra_fields(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_extra_fields
        """
        def mock_build():
            print('called fieldhandler.build_fields')
        def mock_get():
            print('called plugin.get_frameheight')
            return 'frameheight'
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.fieldhandler = types.SimpleNamespace(build_fields=mock_build)
        testobj.master.captions = {'C_SAVE': 'xxx', 'C_DEL': 'yyy'}
        testobj.master.reader = types.SimpleNamespace()
        testobj.add_extra_fields()
        assert testobj.screenfields == []
        assert isinstance(testobj.frm, testee.qtw.QFrame)
        assert isinstance(testobj.b_save, testee.qtw.QPushButton)
        assert isinstance(testobj.b_del, testee.qtw.QPushButton)
        assert testobj._savestates == (False, False)
        assert capsys.readouterr().out == (
                "called Frame.__init__\n"
                "called Frame.setMaximumHeight with arg `90`\n"
                "called fieldhandler.build_fields\n"
                f"called PushButton.__init__ with args ('xxx', {testobj.frm}) {{}}\n"
                "called PushButton.setEnabled with arg `False`\n"
                f"called Signal.connect with args ({testobj.on_update},)\n"
                f"called PushButton.__init__ with args ('yyy', {testobj.frm}) {{}}\n"
                "called PushButton.setEnabled with arg `False`\n"
                f"called Signal.connect with args ({testobj.on_delete},)\n")
        testobj.master.reader = types.SimpleNamespace(get_frameheight=mock_get)
        testobj.add_extra_fields()
        assert testobj.screenfields == []
        assert isinstance(testobj.frm, testee.qtw.QFrame)
        assert isinstance(testobj.b_save, testee.qtw.QPushButton)
        assert isinstance(testobj.b_del, testee.qtw.QPushButton)
        assert testobj._savestates == (False, False)
        assert capsys.readouterr().out == (
                "called Frame.__init__\n"
                "called plugin.get_frameheight\n"
                "called Frame.setMaximumHeight with arg `frameheight`\n"
                "called fieldhandler.build_fields\n"
                f"called PushButton.__init__ with args ('xxx', {testobj.frm}) {{}}\n"
                "called PushButton.setEnabled with arg `False`\n"
                f"called Signal.connect with args ({testobj.on_update},)\n"
                f"called PushButton.__init__ with args ('yyy', {testobj.frm}) {{}}\n"
                "called PushButton.setEnabled with arg `False`\n"
                f"called Signal.connect with args ({testobj.on_delete},)\n")

    def test_set_extrascreen_editable(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_extrascreen_editable
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.screenfields = [mockqtw.MockLineEdit(), mockqtw.MockCheckBox()]
        testobj.b_save = mockqtw.MockPushButton()
        testobj.b_del = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called CheckBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj._savestates = (False, False)
        testobj.set_extrascreen_editable(True)
        assert capsys.readouterr().out == ("called LineEdit.setEnabled with arg True\n"
                                           "called CheckBox.setEnabled with arg True\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n")
        testobj.b_save.setEnabled(True)
        testobj.b_del.setEnabled(True)
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n")
        testobj._savestates = ()
        testobj.set_extrascreen_editable(False)
        assert testobj._savestates == (True, True)
        assert capsys.readouterr().out == ("called LineEdit.setEnabled with arg False\n"
                                           "called CheckBox.setEnabled with arg False\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n")

    def test_layout_extra_fields(self, monkeypatch, capsys, expected_output):
        """unittest for SingleDataInterface.layout_extra_fields
        """
        def mock_layout1(arg):
            print('called fieldhandler.layout_keymodfields')
        def mock_layout2(arg):
            print('called fieldhandler.layout_commandfields')
        def mock_layout3(arg):
            print('called fieldhandler.layout_descfield')
        def mock_extra1(*args):
            print('called plugin.layout_extra_fields_topline')
        def mock_extra2(*args):
            print('called plugin.layout_extra_fields_nextline')
        def mock_extra3(*args):
            print('called plugin.layout_extra_fields')
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.frm = mockqtw.MockFrame()
        testobj.b_save = mockqtw.MockPushButton()
        testobj.b_del = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called Frame.__init__\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.fieldhandler = types.SimpleNamespace(layout_keymodfields=mock_layout1,
                                                     layout_commandfields=mock_layout2,
                                                     layout_descfield=mock_layout3)
        testobj.master.reader = types.SimpleNamespace()
        testobj.layout_extra_fields(mockqtw.MockVBoxLayout())
        assert capsys.readouterr().out == expected_output['sdi_extra_1'].format(testobj=testobj)
        testobj.master.reader = types.SimpleNamespace(layout_extra_fields_topline=mock_extra1,
                                                      layout_extra_fields_nextline=mock_extra2,
                                                      layout_extra_fields=mock_extra3)
        testobj.layout_extra_fields(mockqtw.MockVBoxLayout())
        assert capsys.readouterr().out == expected_output['sdi_extra_2'].format(testobj=testobj)

    def test_resize_if_necessary(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.resize_if_necessary
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.resize_if_necessary()
        assert capsys.readouterr().out == ""

    def test_on_item_selected(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_item_selected
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.has_extrapanel = True
        testobj.on_item_selected('', 'olditem')
        assert capsys.readouterr().out == ""
        testobj.master.has_extrapanel = False
        testobj.on_item_selected('newitem', 'olditem')
        assert capsys.readouterr().out == ""
        testobj.master.has_extrapanel = True
        testobj.on_item_selected('newitem', 'olditem')
        assert capsys.readouterr().out == (
                "called HotkeyPanel.process_changed_selection with args ('newitem', 'olditem')\n")

    def test_on_update(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_update
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_update()
        assert capsys.readouterr().out == ("called HotkeyPanel.apply_changes\n"
                                           "called Tree.setFocus\n")

    def test_on_delete(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.on_delete
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.on_delete()
        assert capsys.readouterr().out == ("called HotkeyPanel.apply_deletion\n"
                                           "called Tree.setFocus\n")

    def test_update_columns(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.update_columns
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.update_columns('oldcount', 'newcount')
        assert capsys.readouterr().out == ""

    def test_refresh_headers(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.refresh_headers
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.column_info = (('xxx', 10), ('yyy', 20))
        testobj.refresh_headers(['head', 'ers'])
        assert capsys.readouterr().out == ("called Tree.setColumnCount with arg `2`\n"
                                           "called Tree.setHeaderLabels with arg `['head', 'ers']`\n"
                                           "called Tree.header\ncalled Header.__init__\n"
                                           "called Header.setSectionsClickable with value True\n"
                                           "called Header.resizeSection for col 0 width 10\n"
                                           "called Header.resizeSection for col 1 width 20\n"
                                           "called Header.setStretchLastSection with arg True\n")

    def test_set_title(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.parent = MockChoiceBook()
        testobj.master.parent.parent = MockEditor()
        testobj.master.parent.parent.gui = mockqtw.MockMainWindow()
        assert capsys.readouterr().out == ("called MainWindow.__init__\n"
                                           "called Application.__init__\n")
        testobj.set_title('title')
        assert capsys.readouterr().out == "called MainWindow.setWindowTitle to `title`\n"

    def test_clear_list(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.clear_list
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_list()
        assert capsys.readouterr().out == "called Tree.clear\n"

    def test_build_listitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.build_listitem
        """
        monkeypatch.setattr(testee.qtw, 'QTreeWidgetItem', mockqtw.MockTreeItem)
        testobj = self.setup_testobj(monkeypatch, capsys)
        result = testobj.build_listitem('key')
        assert isinstance(result, testee.qtw.QTreeWidgetItem)
        assert result.data(0, testee.core.Qt.ItemDataRole.UserRole) == 'key'
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setData to `key` with role"
                f" {testee.core.Qt.ItemDataRole.UserRole} for col 0\n"
                f"called TreeItem.data for col 0 role {testee.core.Qt.ItemDataRole.UserRole}\n")

    def test_set_listitemtext(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_listitemtext
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ()\n"
        testobj.set_listitemtext(item, 1, 'value')
        assert capsys.readouterr().out == ("called TreeItem.setText with arg `value` for col 1\n"
                                           "called TreeItem.setTooltip with args (1, 'value')\n")

    def test_add_listitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.add_listitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.add_listitem('new_item')
        assert capsys.readouterr().out == "called Tree.addTopLevelItem\n"

    def test_set_listselection(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_listselection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        treeitem = mockqtw.MockTreeItem()
        testobj.p0list.addTopLevelItem(treeitem)
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called Tree.addTopLevelItem\n")
        testobj.set_listselection(0)
        assert capsys.readouterr().out == (
                "called Tree.topLevelItem with arg `0`\n"
                "called Tree.setCurrentItem with arg `Tree.topLevelItem`\n")

    def test_getfirstitem(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.getfirstitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        treeitem = mockqtw.MockTreeItem()
        testobj.p0list.addTopLevelItem(treeitem)
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called TreeItem.__init__ with args ()\n"
                                           "called Tree.addTopLevelItem\n")
        assert testobj.getfirstitem() == 'Tree.topLevelItem'
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `0`\n")

    def test_get_widget_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_widget_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        ted = mockqtw.MockLineEdit()
        ted.setText('xxx')
        assert capsys.readouterr().out == ("called LineEdit.__init__\n"
                                           "called LineEdit.setText with arg `xxx`\n")
        assert testobj.get_widget_text(ted, 'text') == "xxx"
        assert capsys.readouterr().out == ("called LineEdit.text\n")
        assert testobj.get_widget_text(ted, 'xxx') == "xxx"
        assert capsys.readouterr().out == ("called LineEdit.text\n")

    def test_enable_save(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.enable_save
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.b_save = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.enable_save(True)
        assert testobj.b_save.isEnabled()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n")
        testobj.enable_save(False)
        assert not testobj.b_save.isEnabled()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `False`\n")

    def test_get_choice_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_choice_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_choice_value(cb, 'dummy', 'text') == (cb, 'text')

    def test_init_combobox(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.init_combobox
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.init_combobox(cb)
        assert capsys.readouterr().out == ("called ComboBox.clear\n")
        testobj.init_combobox(cb, choices=[])
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.addItems with arg []\n")
        testobj.init_combobox(cb, choices=['xxx', 'yyy'])
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.addItems with arg ['xxx', 'yyy']\n")

    def test_set_combobox_string(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_combobox_string
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.set_combobox_string(cb, 'value', [])
        assert capsys.readouterr().out == ""
        testobj.set_combobox_string(cb, 'value', ['value', 'list'])
        assert capsys.readouterr().out == "called ComboBox.setCurrentIndex with arg `0`\n"

    def test_get_combobox_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_combobox_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_combobox_text(cb) == "current text"
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_get_combobox_selection(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_combobox_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.get_combobox_selection(cb)
        assert capsys.readouterr().out == ("called ComboBox.currentText\n")

    def test_set_label_text(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_label_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        lbl = mockqtw.MockLabel()
        assert capsys.readouterr().out == "called Label.__init__\n"
        testobj.set_label_text(lbl, 'value')
        assert capsys.readouterr().out == "called Label.setText with arg `value`\n"

    def test_set_textfield_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_textfield_value

        wordt gebruikt voor zowel QLineEdit, QComboBox en QTextEdit
        dit is ducktyping, elk apart testen niet nodig
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        txt = mockqtw.MockLineEdit()
        assert capsys.readouterr().out == "called LineEdit.__init__\n"
        testobj.set_textfield_value(txt, 'value')
        assert capsys.readouterr().out == ("called LineEdit.setText with arg `value`\n")

    def test_get_check_value(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_check_value
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert testobj.get_check_value(cb, True) == (cb, True)
        assert capsys.readouterr().out == ""
        assert testobj.get_check_value(cb, False) == (cb, False)
        assert capsys.readouterr().out == ""

    def test_get_checkbox_state(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_checkbox_state
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        assert not testobj.get_checkbox_state(cb)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")
        cb.setChecked(True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"
        assert testobj.get_checkbox_state(cb)
        assert capsys.readouterr().out == ("called CheckBox.isChecked\n")

    def test_set_checkbox_state(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.set_checkbox_state
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        cb = mockqtw.MockCheckBox()
        assert capsys.readouterr().out == "called CheckBox.__init__\n"
        testobj.set_checkbox_state(cb, False)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg False\n"
        testobj.set_checkbox_state(cb, True)
        assert capsys.readouterr().out == "called CheckBox.setChecked with arg True\n"

    def test_get_keydef_at_position(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_keydef_at_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        result = testobj.get_keydef_at_position(1)
        assert result == 'Tree.topLevelItem'
        assert capsys.readouterr().out == ("called Tree.topLevelItem with arg `1`\n")

    def test_enable_delete(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.enable_delete
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.b_del = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.enable_delete(True)
        assert testobj.b_del.isEnabled()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n")
        testobj.enable_delete(False)
        assert not testobj.b_del.isEnabled()
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `False`\n")

    def test_get_itemdata(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_itemdata
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        item = mockqtw.MockTreeItem()
        item.setData(0, testee.core.Qt.ItemDataRole.UserRole, 'data')
        assert capsys.readouterr().out == (
                "called TreeItem.__init__ with args ()\n"
                "called TreeItem.setData to `data` with role"
                f" {testee.core.Qt.ItemDataRole.UserRole} for col 0\n")
        assert testobj.get_itemdata(item) == "data"
        assert capsys.readouterr().out == (
                f"called TreeItem.data for col 0 role {testee.core.Qt.ItemDataRole.UserRole}\n")

    def test_get_selected_keydef(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_selected_keydef
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        result = testobj.get_selected_keydef()
        assert result == 'called Tree.currentItem'
        assert capsys.readouterr().out == ("")

    def test_get_keydef_position(self, monkeypatch, capsys):
        """unittest for SingleDataInterface.get_keydef_position
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_keydef_position('item') == 'index'
        assert capsys.readouterr().out == ("called Tree.indexOfTopLevelItem with arg `item`\n")


class TestTabbedInterface:
    """unittests for gui_qt.TabbedInterface
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.TabbedInterface object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called TabbedInterface.__init__ with args', args)
        monkeypatch.setattr(testee.TabbedInterface, '__init__', mock_init)
        testobj = testee.TabbedInterface()
        testobj.parent = MockGui()
        testobj.master = MockChoiceBook()
        assert capsys.readouterr().out == 'called TabbedInterface.__init__ with args ()\n'
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for TabbedInterface.__init__
        """
        monkeypatch.setattr(testee.qtw.QFrame, '__init__', mockqtw.MockFrame.__init__)
        testobj = testee.TabbedInterface('parent', 'master')
        assert testobj.parent == 'parent'
        assert testobj.master == 'master'
        assert capsys.readouterr().out == ("called Frame.__init__\n")

    def test_setup_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.setup_selector
        """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QStackedWidget', mockqtw.MockStackedWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setup_selector()
        assert isinstance(testobj.sel, testee.qtw.QComboBox)
        assert isinstance(testobj.pnl, testee.qtw.QStackedWidget)
        assert capsys.readouterr().out == (
                "called ComboBox.__init__\n"
                f"called Signal.connect with args ({testobj.master.on_page_changed},)\n"
                "called StackedWidget.__init__\n")

    def test_setup_search(self, monkeypatch, capsys, expected_output):
        """unittest for TabbedInterface.setup_search
        """
        monkeypatch.setattr(testee.qtw, 'QComboBox', mockqtw.MockComboBox)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.editor = MockEditor()
        testobj.parent.editor.captions = {'C_FILTER': 'xxx'}
        testobj.setup_search()
        assert isinstance(testobj.find_loc, testee.qtw.QComboBox)
        assert isinstance(testobj.find, testee.qtw.QComboBox)
        assert isinstance(testobj.b_next, testee.qtw.QPushButton)
        assert isinstance(testobj.b_prev, testee.qtw.QPushButton)
        assert isinstance(testobj.b_filter, testee.qtw.QPushButton)
        assert not testobj.filter_on
        assert capsys.readouterr().out == expected_output['tabbed_search'].format(testobj=testobj)

    def test_add_subscreen(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_subscreen
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockStackedWidget()
        win = MockHotkeyPanel()
        win.gui = MockSDI()
        testobj.add_subscreen(win)
        assert capsys.readouterr().out == ("called StackedWidget.__init__\n"
                                           f"called StackedWidget.addWidget with arg {win.gui}\n")

    def test_add_to_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_to_selector
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.add_to_selector('text')
        assert capsys.readouterr().out == ("called ComboBox.addItems with arg `text`\n")

    def test_format_screen(self, monkeypatch, capsys, expected_output):
        """unittest for TabbedInterface.format_screen
        """
        def mock_setcaptions():
            print('called TabbedInterface.setcaptions')
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QLabel', mockqtw.MockLabel)
        monkeypatch.setattr(testee.TabbedInterface, 'setLayout', mockqtw.MockFrame.setLayout)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_loc = mockqtw.MockComboBox()
        testobj.find = mockqtw.MockComboBox()
        testobj.sel = mockqtw.MockComboBox()
        testobj.b_next = mockqtw.MockPushButton()
        testobj.b_prev = mockqtw.MockPushButton()
        testobj.b_filter = mockqtw.MockPushButton()
        testobj.pnl = mockqtw.MockStackedWidget()
        testobj.setcaptions = mock_setcaptions
        testobj.format_screen()
        assert capsys.readouterr().out == expected_output['tabbed_screen'].format(testobj=testobj)

    def test_setcaptions(self, monkeypatch, capsys):
        """unittest for TabbedInterface.setcaptions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.editor = MockEditor()
        testobj.parent.editor.captions = {'C_NEXT': 'xxx', 'C_PREV': 'yyy', 'C_SELPRG': 'zzz',
                                          'C_FIND': 'aaa', 'C_FLTOFF': 'bbb', 'C_FILTER': 'ccc',
                                          'C_EXIT': 'ddd'}
        testobj.b_next = mockqtw.MockPushButton()
        testobj.b_prev = mockqtw.MockPushButton()
        testobj.sel_text = mockqtw.MockLabel()
        testobj.find_text = mockqtw.MockLabel()
        testobj.b_filter = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called Label.__init__\n"
                                           "called Label.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.filter_on = False
        testobj.setcaptions()
        assert capsys.readouterr().out == ("called PushButton.setText with arg `xxx`\n"
                                           "called PushButton.setText with arg `yyy`\n"
                                           "called Label.setText with arg `zzz`\n"
                                           "called Label.setText with arg `aaa`\n"
                                           "called PushButton.setText with arg `ccc`\n")
        testobj.parent.b_exit = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.filter_on = True
        testobj.setcaptions()
        assert capsys.readouterr().out == ("called PushButton.setText with arg `xxx`\n"
                                           "called PushButton.setText with arg `yyy`\n"
                                           "called Label.setText with arg `zzz`\n"
                                           "called Label.setText with arg `aaa`\n"
                                           "called PushButton.setText with arg `bbb`\n"
                                           "called PushButton.setText with arg `ddd`\n")

    def test_get_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockStackedWidget()
        assert testobj.get_panel() == "current widget"
        assert capsys.readouterr().out == ("called StackedWidget.__init__\n"
                                           "called StackedWidget.currentWidget\n")

    def test_get_selected_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_tool
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_selected_tool() == "current text"
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_set_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        testobj.set_selected_panel(2)
        assert capsys.readouterr().out == "called StackedWidget.setCurrentIndex with arg 2\n"

    def test_update_search(self, monkeypatch, capsys):
        """unittest for TabbedInterface.update_search
        """
        def mock_init():
            print('called TabbedInterface.init_search_buttons')
        def mock_enable(**kwargs):
            print('called TabbedInterface.enable_search_buttons with args', kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_loc = mockqtw.MockComboBox()
        testobj.find = mockqtw.MockComboBox()
        testobj.b_filter = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called ComboBox.__init__\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.master.page.filtertext = ''
        testobj.parent.captions = {'C_FLTOFF': 'xxx'}
        testobj.init_search_buttons = mock_init
        testobj.enable_search_buttons = mock_enable
        testobj.update_search(['items'])
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.addItems with arg ['items']\n"
                                           "called ComboBox.setCurrentText with arg `items`\n"
                                           "called ComboBox.setEditText with arg ``\n"
                                           "called ComboBox.setEnabled with arg True\n"
                                           "called TabbedInterface.init_search_buttons\n")
        testobj.master.page.filtertext = 'qqq'
        testobj.update_search(['items', 'last'])
        assert capsys.readouterr().out == (
                "called ComboBox.clear\n"
                "called ComboBox.addItems with arg ['items', 'last']\n"
                "called ComboBox.setCurrentText with arg `last`\n"
                "called ComboBox.setEditText with arg `qqq`\n"
                "called PushButton.setText with arg `xxx`\n"
                "called TabbedInterface.enable_search_buttons with args {'filter': True}\n")

    def test_get_search_col(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_search_col
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_loc = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_search_col() == "current text"
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_find_items(self, monkeypatch, capsys):
        """unittest for TabbedInterface.find_items
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.zoekcol = 'xxx'
        page = MockHotkeyPanel()
        page.gui = MockSDI()
        page.gui.p0list = mockqtw.MockTreeWidget()
        assert testobj.find_items(page, 'text') == []
        assert capsys.readouterr().out == ("called Tree.__init__\n"
                                           "called Tree.findItems with args ('text',"
                                           f" {testee.core.Qt.MatchFlag.MatchContains!r}, 'xxx')\n")

    def test_init_search_buttons(self, monkeypatch, capsys):
        """unittest for TabbedInterface.init_search_buttons
        """
        def mock_enable(**kwargs):
            print("called TabbedInterface.enable_search_buttons with args", kwargs)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.enable_search_buttons = mock_enable
        testobj.init_search_buttons()
        assert capsys.readouterr().out == ("called TabbedInterface.enable_search_buttons with args"
                                           " {'next': False, 'prev': False, 'filter': False}\n")

    def test_set_selected_keydef_item(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_keydef_item
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.items_found = ['xxx', 'yyy', 'zzz']
        page = MockHotkeyPanel()
        page.gui = MockSDI()
        page.gui.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.set_selected_keydef_item(page, 2)
        assert capsys.readouterr().out == ("called Tree.setCurrentItem with arg `zzz`\n"
                                           "called Tree.scrollToItem with arg `zzz`\n")

    def test_enable_search_buttons(self, monkeypatch, capsys):
        """unittest for TabbedInterface.enable_search_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.b_next = mockqtw.MockPushButton()
        testobj.b_prev = mockqtw.MockPushButton()
        testobj.b_filter = mockqtw.MockPushButton()
        assert capsys.readouterr().out == ("called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n"
                                           "called PushButton.__init__ with args () {}\n")
        testobj.enable_search_buttons()
        assert capsys.readouterr().out == ""
        testobj.enable_search_buttons(next=False, prev=False, filter=False)
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n"
                                           "called PushButton.setEnabled with arg `False`\n")
        testobj.enable_search_buttons(next=True, prev=True, filter=True)
        assert capsys.readouterr().out == ("called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n"
                                           "called PushButton.setEnabled with arg `True`\n")

    def test_get_filter_state_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_filter_state_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.b_filter = mockqtw.MockPushButton('xxx')
        assert capsys.readouterr().out == "called PushButton.__init__ with args ('xxx',) {}\n"
        assert testobj.get_filter_state_text() == "xxx"
        assert capsys.readouterr().out == ""

    def test_get_search_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_search_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_search_text() == "current text"
        assert capsys.readouterr().out == "called ComboBox.currentText\n"

    def test_get_found_keydef_position(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_found_keydef_position
        """
        item = mockqtw.MockTreeItem('xxx', 'yyy')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx', 'yyy')\n"
        def mock_current():
            print('called Tree.currentItem')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        # testobj.master.page = MockHotkeyPanel()
        testobj.master.page.gui = MockSDI()
        testobj.master.page.gui.p0list = mockqtw.MockTreeWidget()
        testobj.master.page.gui.p0list.currentItem = mock_current
        assert capsys.readouterr().out == "called Tree.__init__\n"
        assert testobj.get_found_keydef_position() == ('xxx', 'yyy')
        assert capsys.readouterr().out == ("called Tree.currentItem\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n")

    def test_enable_search_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.enable_search_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.enable_search_text(True)
        assert capsys.readouterr().out == "called ComboBox.setEnabled with arg True\n"

    def test_set_found_keydef_position(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_found_keydef_position
        """
        item = mockqtw.MockTreeItem('xxx', 'yyy')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('xxx', 'yyy')\n"
        def mock_count():
            print('called Tree.topLevelItemCount')
            return 2
        item2 = mockqtw.MockTreeItem('aaa', 'bbb')
        assert capsys.readouterr().out == "called TreeItem.__init__ with args ('aaa', 'bbb')\n"
        def mock_item(num):
            print(f'called Tree.topLevelItem with arg {num}')
            if num == 1:
                return item
            return item2
        def mock_current():
            print('called Tree.currentItem')
            return item
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.master.page.gui = MockSDI()
        testobj.master.page.gui.p0list = mockqtw.MockTreeWidget()
        assert capsys.readouterr().out == "called Tree.__init__\n"
        testobj.master.page.gui.p0list.topLevelItemCount = mock_count
        testobj.master.page.gui.p0list.topLevelItem = mock_item
        testobj.master.page.gui.p0list.currentItem = mock_current
        testobj.master.reposition = ('xxx', 'yyy')
        testobj.set_found_keydef_position()
        assert capsys.readouterr().out == ("called Tree.topLevelItemCount\n"
                                           "called Tree.topLevelItem with arg 0\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           "called Tree.topLevelItem with arg 1\n"
                                           "called TreeItem.text for col 0\n"
                                           "called TreeItem.text for col 1\n"
                                           f"called Tree.setCurrentItem with arg `{item}`\n")

    def test_set_filter_state_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_filter_state_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.b_filter = mockqtw.MockPushButton()
        assert capsys.readouterr().out == "called PushButton.__init__ with args () {}\n"
        testobj.set_filter_state_text("state")
        assert capsys.readouterr().out == "called PushButton.setText with arg `state`\n"

    def test_get_selected_index(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.get_selected_index()
        assert capsys.readouterr().out == "called ComboBox.currentIndex\n"

    def test_clear_selector(self, monkeypatch, capsys):
        """unittest for TabbedInterface.clear_selector
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.clear_selector()
        assert capsys.readouterr().out == "called ComboBox.clear\n"

    def test_remove_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.remove_tool
        """
        win = mockqtw.MockFrame()
        win.master = 'master'
        assert capsys.readouterr().out == "called Frame.__init__\n"
        def mock_widget(num):
            print(f"called StackedWidget.widget with arg {num}")
            return win
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockStackedWidget()
        testobj.pnl.widget = mock_widget
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        assert testobj.remove_tool(1, 'program', []) is None
        assert capsys.readouterr().out == ("called StackedWidget.widget with arg 1\n"
                                           f"called StackedWidget.removeWidget with arg {win}\n"
                                           "called Frame.close\n")
        assert testobj.remove_tool(1, 'program', ['program', 'list']) == "master"
        assert capsys.readouterr().out == ("called StackedWidget.widget with arg 1\n"
                                           f"called StackedWidget.removeWidget with arg {win}\n")

    def test_add_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.add_tool
        """
        def mock_add(win):
            print(f'called TabbedInterface.add_subscreen with arg {win}')
        def mock_add_to(prog):
            print(f'called TabbedInterface.add_to_selector with arg {prog}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.add_subscreen = mock_add
        testobj.add_to_selector = mock_add_to
        testobj.add_tool('program', 'win')
        assert capsys.readouterr().out == (
                "called TabbedInterface.add_subscreen with arg win\n"
                "called TabbedInterface.add_to_selector with arg program\n")

    def test_get_new_selection(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_new_selection
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        assert testobj.get_new_selection('item') == 1
        assert capsys.readouterr().out == "called ComboBox.findText with args ('item',)\n"

    def test_set_selected_tool(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_selected_tool
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.set_selected_tool('selection')
        assert capsys.readouterr().out == "called ComboBox.setCurrentIndex with arg `selection`\n"

    def test_get_selected_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = mockqtw.MockComboBox()
        testobj.pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == ("called ComboBox.__init__\n"
                                           "called StackedWidget.__init__\n")
        assert testobj.get_selected_panel() == (1, 'widget')
        assert capsys.readouterr().out == ("called ComboBox.currentIndex\n"
                                           "called StackedWidget.widget with arg {num}\n")

    def test_replace_panel(self, monkeypatch, capsys):
        """unittest for TabbedInterface.replace_panel
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockStackedWidget()
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        testobj.replace_panel('indx', 'win', 'newwin')
        assert capsys.readouterr().out == (
                "called StackedWidget.insertWidget with args ('indx', 'newwin')\n"
                "called StackedWidget.setCurrentIndex with arg indx\n"
                "called StackedWidget.removeWidget with arg win\n")

    def test_set_panel_editable(self, monkeypatch, capsys):
        """unittest for TabbedInterface.set_panel_editable
        """
        def mock_set(arg):
            print(f"called Frame.set_extrascreen_editable with arg {arg}")
        win = mockqtw.MockFrame()
        win.set_extrascreen_editable = mock_set
        assert capsys.readouterr().out == "called Frame.__init__\n"
        def mock_widget():
            print("called StackedWidget.currentWidget")
            return win
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pnl = mockqtw.MockStackedWidget()
        testobj.pnl.currentWidget = mock_widget
        assert capsys.readouterr().out == "called StackedWidget.__init__\n"
        testobj.set_panel_editable(True)
        assert capsys.readouterr().out == ("called StackedWidget.currentWidget\n"
                                           "called Frame.set_extrascreen_editable with arg True\n")
        testobj.set_panel_editable(False)
        assert capsys.readouterr().out == ("called StackedWidget.currentWidget\n"
                                           "called Frame.set_extrascreen_editable with arg False\n")

    def test_refresh_locs(self, monkeypatch, capsys):
        """unittest for TabbedInterface.refresh_locs
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.find_loc = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.refresh_locs(['headers'])
        assert capsys.readouterr().out == ("called ComboBox.clear\n"
                                           "called ComboBox.addItems with arg ['headers']\n")

    def test_get_selected_text(self, monkeypatch, capsys):
        """unittest for TabbedInterface.get_selected_text
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = mockqtw.MockComboBox()
        assert capsys.readouterr().out == "called ComboBox.__init__\n"
        testobj.get_selected_text()
        assert capsys.readouterr().out == ("called ComboBox.currentText\n")


class TestGui:
    """unittests for gui_qt.Gui
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for gui_qt.Gui object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Gui.__init__ with args', args)
        monkeypatch.setattr(testee.Gui, '__init__', mock_init)
        testobj = testee.Gui()
        testobj.editor = MockEditor()
        testobj.app = mockqtw.MockApplication()
        testobj.sb = mockqtw.MockStatusBar()
        testobj.menu_bar = mockqtw.MockMenuBar()
        assert capsys.readouterr().out == ("called Gui.__init__ with args ()\n"
                                           "called Application.__init__\n"
                                           "called StatusBar.__init__ with args ()\n"
                                           "called MenuBar.__init__\n")
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Gui.__init__
        """
        monkeypatch.setattr(testee.qtw.QMainWindow, '__init__', mockqtw.MockMainWindow.__init__)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'resize', mockqtw.MockMainWindow.resize)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'statusBar', mockqtw.MockMainWindow.statusBar)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'menuBar', mockqtw.MockMainWindow.menuBar)
        monkeypatch.setattr(testee.qtw.QApplication, '__init__', mockqtw.MockApplication.__init__)
        monkeypatch.setattr(testee.shared, 'LIN', False)
        testobj = testee.Gui()
        assert testobj.editor is None
        assert isinstance(testobj.app, mockqtw.MockApplication)
        assert isinstance(testobj.sb, mockqtw.MockStatusBar)
        assert isinstance(testobj.menu_bar, mockqtw.MockMenuBar)
        assert testobj.menuitems == {}
        assert capsys.readouterr().out == ("called Application.__init__\n"
                                           "called MainWindow.__init__\n"
                                           "called Application.__init__\n"
                                           "called MainWindow.resize with args (688, 594)\n"
                                           "called MainWindow.statusBar\n"
                                           "called StatusBar.__init__ with args ()\n"
                                           "called MainWindow.menuBar\n"
                                           "called MenuBar.__init__\n")
        monkeypatch.setattr(testee.shared, 'LIN', True)
        parent = MockEditor()
        testobj = testee.Gui(parent)
        assert testobj.editor == parent
        assert isinstance(testobj.app, mockqtw.MockApplication)
        assert isinstance(testobj.sb, mockqtw.MockStatusBar)
        assert isinstance(testobj.menu_bar, mockqtw.MockMenuBar)
        assert testobj.menuitems == {}
        assert capsys.readouterr().out == ("called Application.__init__\n"
                                           "called MainWindow.__init__\n"
                                           "called Application.__init__\n"
                                           "called MainWindow.resize with args (1140, 594)\n"
                                           "called MainWindow.statusBar\n"
                                           "called StatusBar.__init__ with args ()\n"
                                           "called MainWindow.menuBar\n"
                                           "called MenuBar.__init__\n")

    def test_resize_empty_screen(self, monkeypatch, capsys):
        """unittest for Gui.resize_empty_screen
        """
        def mock_resize(*args):
            print('called Gui.resize with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.resize = mock_resize
        testobj.resize_empty_screen(10, 20)
        assert capsys.readouterr().out == ("called Gui.resize with args (10, 20)\n")

    def test_go(self, monkeypatch, capsys, expected_output):
        """unittest for Gui.go
        """
        monkeypatch.setattr(testee.qtw, 'QFrame', mockqtw.MockFrame)
        monkeypatch.setattr(testee.qtw, 'QVBoxLayout', mockqtw.MockVBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QHBoxLayout', mockqtw.MockHBoxLayout)
        monkeypatch.setattr(testee.qtw, 'QPushButton', mockqtw.MockPushButton)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'setCentralWidget',
                            mockqtw.MockMainWindow.setCentralWidget)
        monkeypatch.setattr(testee.qtw.QMainWindow, 'show', mockqtw.MockMainWindow.show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.captions = {'C_EXIT': 'Exit text'}
        testobj.editor.exit = lambda x: x
        with pytest.raises(SystemExit):
            testobj.go()
        assert capsys.readouterr().out == expected_output["maingui"].format(testobj=testobj)

    def test_set_window_title(self, monkeypatch, capsys):
        """unittest for Gui.set_window_title
        """
        monkeypatch.setattr(testee.Gui, 'setWindowTitle', mockqtw.MockMainWindow.setWindowTitle)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_window_title('title')
        assert capsys.readouterr().out == ("called MainWindow.setWindowTitle to `title`\n")

    def test_statusbar_message(self, monkeypatch, capsys):
        """unittest for Gui.statusbar_message
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.statusbar_message('message')
        assert capsys.readouterr().out == ("called StatusBar.showMessage with arg `message`\n")

    def test_setup_tabs(self, monkeypatch, capsys):
        """unittest for Gui.setup_tabs
        """
        monkeypatch.setattr(testee.Gui, 'setCentralWidget', mockqtw.MockMainWindow.setCentralWidget)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.setup_tabs()
        assert capsys.readouterr().out == ("called MainWidget.setCentralWindow with arg of type"
                                           " `<class 'test_qtgui.MockTabbedInterface'>`\n")

    def test_setup_menu(self, monkeypatch, capsys):
        """unittest for Gui.setup_menu
        """
        def mock_create(*args):
            print(f'called Gui.create_menuaction with args {args}')
            result = mockqtw.MockAction()
            return result
        def mock_get():
            print('called Editor.get_menudata')
            return []
        def mock_get_2():
            print('called Editor.get_menudata')
            return [('menu', [('xxx', (mock_callback, 'XXX')), -1,
                              ('submenu', ([('yyy', (mock_callback, 'YYY'))], ''))
                              ])]
        def mock_callback():
            "stub for function object"
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menu_bar = mockqtw.MockMenuBar()
        assert capsys.readouterr().out == "called MenuBar.__init__\n"
        testobj.editor.get_menudata = mock_get
        testobj.editor.captions = {}
        testobj.menuitems = {'M_TOOL': mockqtw.MockAction()}
        assert capsys.readouterr().out == "called Action.__init__ with args ()\n"
        testobj.create_menuaction = mock_create
        testobj.setup_menu(minimal=True)
        assert capsys.readouterr().out == ("called MenuBar.clear\n"
                                           "called Editor.get_menudata\n"
                                           "called Action.setEnabled with arg `False`\n")
        testobj.editor.captions = {'menu': 'Menutitle', 'xxx': 'Menuitem X', 'submenu': 'Subtitle',
                                   'yyy': 'Menuitem Y'}
        testobj.menuitems = {}
        testobj.editor.get_menudata = mock_get_2
        testobj.setup_menu()
        assert list(testobj.menuitems) == ['menu', 'xxx', 'submenu', 'yyy']
        assert isinstance(testobj.menuitems['menu'], mockqtw.MockMenu)
        assert isinstance(testobj.menuitems['submenu'], mockqtw.MockMenu)
        assert isinstance(testobj.menuitems['xxx'], mockqtw.MockAction)
        assert isinstance(testobj.menuitems['yyy'], mockqtw.MockAction)
        assert capsys.readouterr().out == (
                "called MenuBar.clear\n"
                "called Editor.get_menudata\n"
                "called MenuBar.addMenu with arg  Menutitle\n"
                "called Menu.__init__ with args ('Menutitle',)\n"
                f"called Gui.create_menuaction with args ('xxx', {mock_callback}, 'XXX')\n"
                "called Action.__init__ with args ()\n"
                "called Menu.addAction\n"
                "called Menu.addSeparator\n"
                "called Action.__init__ with args ('-----', None)\n"
                "called Menu.addMenu with args ('Subtitle',)\n"
                "called Menu.__init__ with args ()\n"
                f"called Gui.create_menuaction with args ('yyy', {mock_callback}, 'YYY')\n"
                "called Action.__init__ with args ()\n"
                "called Menu.addAction\n")

    def test_create_menuaction(self, monkeypatch, capsys):
        """unittest for Gui.create_menuaction
        """
        def mock_callback():
            "stub for function object"
        monkeypatch.setattr(testee.gui, 'QAction', mockqtw.MockAction)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.captions = {'xxx': 'yyyyyy'}
        result = testobj.create_menuaction('xxx', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n")

        testobj.editor.captions = {'M_READ': 'yyyyyy'}
        testobj.editor.book.page.data = {}
        result = testobj.create_menuaction('M_READ', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.data = {'keydef': ['x']}
        result = testobj.create_menuaction('M_READ', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n")

        testobj.editor.captions = {'M_RBLD': 'yyyyyy'}
        testobj.editor.book.page.settings = {}
        result = testobj.create_menuaction('M_RBLD', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.settings = {testee.shared.SettType.RBLD.value: False}
        result = testobj.create_menuaction('M_RBLD', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.settings = {testee.shared.SettType.RBLD.value: True}
        result = testobj.create_menuaction('M_RBLD', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `True`\n")

        testobj.editor.captions = {'M_SAVE': 'yyyyyy'}
        testobj.editor.book.page.settings = {}
        result = testobj.create_menuaction('M_SAVE', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.settings = {testee.shared.SettType.RDEF.value: False}
        result = testobj.create_menuaction('M_SAVE', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `False`\n")
        testobj.editor.book.page.settings = {testee.shared.SettType.RDEF.value: True}
        result = testobj.create_menuaction('M_SAVE', mock_callback, 'shortcut')
        assert isinstance(result, testee.gui.QAction)
        assert capsys.readouterr().out == (
                f"called Action.__init__ with args ('yyyyyy', {testobj})\n"
                f"called Signal.connect with args ({mock_callback},)\n"
                "called Action.setShortcut with arg `shortcut`\n"
                "called Action.setEnabled with arg `True`\n")

    def test_setcaptions(self, monkeypatch, capsys):
        """unittest for Gui.setcaptions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.editor.captions = {'menu': 'xxxxx', 'menuaction': 'yyyyyy'}
        testobj.menuitems = {'menu': mockqtw.MockMenu(), 'menuaction': mockqtw.MockAction()}
        assert capsys.readouterr().out == ("called Menu.__init__ with args ()\n"
                                           "called Action.__init__ with args ()\n")
        testobj.setcaptions()
        assert capsys.readouterr().out == ("called Menu.setTitle with arg 'xxxxx'\n"
                                           "called Action.setText with arg `yyyyyy`\n")
        testobj.menuitems = {'xxx': 'yyy'}
        with pytest.raises(AttributeError) as exc:
            testobj.setcaptions()
        assert str(exc.value) == "'str' object has no attribute 'setText'"

    def test_modify_menuitem(self, monkeypatch, capsys):
        """unittest for Gui.modify_menuitem
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.menuitems = {'caption': mockqtw.MockAction()}
        assert capsys.readouterr().out == 'called Action.__init__ with args ()\n'
        testobj.modify_menuitem('caption', 'setting')
        assert capsys.readouterr().out == "called Action.setEnabled with arg `setting`\n"
