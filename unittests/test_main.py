"""unittests for ./editor/main.py
"""
import types
import pytest
from editor import main as testee


class MockSettType(testee.shared.enum.Enum):
    """stub for shared.SettType
    """
    PLG = 'plg'
    PNL = 'pnl'
    RBLD = 'rbld'
    DETS = 'dets'
    RDEF = 'rdef'


class MockSDI:
    """stub for gui.SingleDataInterface
    """
    def __init__(self, *args):
        print('called SingleDataInterface.__init__ with args', args)
    def add_button_to_line(self, *args):
        print("called SDI.add_button_to_line with args", args)
        return 'button'
    def add_checkbox_to_line(self, *args):
        print("called SDI.add_checkbox_to_line with args", args)
        return 'checkbox'
    def add_combobox_to_line(self, *args, **kwargs):
        print("called SDI.add_combobox_to_line with args", args, kwargs)
        return 'combobox'
    def add_descfield_to_line(self, line):
        print(f"called SDI.add_descfield_to_line with arg {line}")
        return 'textarea'
    def add_extra_fields(self):
        print('called SDI.add_extra_fields')
    def add_label_to_line(self, *args, **kwargs):
        print("called SDI.add_label_to_line with args", args, kwargs)
        return 'label'
    def add_listitem(self, *args):
        print('called SDI.add_listitem with args', args)
    def add_separator_to_line(self, line):
        print(f"called SDI.add_separator_to_line with arg {line}")
    def add_textfield_to_line(self, *args, **kwargs):
        print("called SDI.add_textfield_to_line with args", args, kwargs)
        return 'textinput'
    def build_listitem(self, *args):
        print("called SDI.build_listitem with args", args)
        return f'item-{args[0]}'
    def clear_list(self, arg):
        print(f'called SDI.clear_list with arg {arg}')
    def enable_delete(self, value):
        print(f"called SDI.enable_delete with arg {value}")
    def enable_button(self, *args):
        print('called SDI.enable_button with args', args)
    def enable_save(self, value):
        print(f"called SDI.enable_save with arg {value}")
    def finalize_screen(self, *args):
        print('called SDI.finalize_screen with args', args)
    def get_choice_value(self, *args):
        print('called SDI.get_choice_value with args', args)
        return args[0], 'abcdef'
    def get_combobox_value(self, arg):
        print('called SDI.get_combobox_value with arg', arg)
        return arg.name
    def get_combobox_selection(self, arg):
        print(f"called SDI.get_combobox_selection with arg '{arg}'")
        return 'xxx'
    def getfirstitem(self, *args):
        print('called SDI.getfirstitem with args', args)
        return 'first_item'
    def get_itemdata(self, arg):
        print(f"called SDI.get_itemdata with arg '{arg}'")
        return '1'
    def get_listitem_at_position(self, *args):
        print("called SDI.get_listitem_at_position with args", args)
        return 'item at position'
    def get_listitem_position(self, *args):
        print("called SDI.get_listitem_position with args", args)
        return 'position of keydef X'
    def get_listbox_selection(self, arg):
        print('called SDI.get_listbox_selection with arg', arg)
        return 'keydef X', 'position'
    def get_widget_text(self, *args):
        print("called SDI.get_widget_text with args", args)
        return 'snark'
    def init_combobox(self, *args):
        print('called SDI.init_combobox with args', args)
    def on_item_selected(self):
        "dummy callback"
    def refresh_headers(self, *args):
        print("called SDI.refresh_headers with args", args)
    def resize_if_necessary(self):
        print('called SDI.resize_if_necessary')
    def set_checkbox_state(self, *args):
        print('called SDI.set_checkbox_state with args', args)
    def set_combobox_string(self, *args):
        print('called SDI.set_combobox_string with args', args)
    def set_extrapanel_editable(self, *args):
        print('called SDI.set_extrapanel_editable with args', args)
    def set_focus_to(self, arg):
        print(f"called SDI.set_focus_to with arg '{arg}'")
    def set_label_text(self, *args):
        print('called SDI.set_label_text with args', args)
    def set_listitemtext(self, *args):
        print('called SDI.set_listitemtext with args', args)
        return args[0]
    def set_listselection(self, *args):
        print('called SDI.set_listselection with args', args)
    def set_textfield_value(self, *args):
        print('called SDI.set_textfield_value with args', args)
    def set_title(self, value):
        print(f"called SDI.set_title with arg '{value}'")
    def setup_empty_screen(self, *args):
        print('called SDI.setup_empty_screen with args', args)
    def setup_list(self, *args):
        print('called SDI.setup_list with args', args)
        return 'p0list'
    def start_line(self, box):
        print(f"called SDI.start_line with arg {box}")
        return 'line'
    def start_extrapanel(self, number):
        print(f"called SDI.start_extrapanel with arg {number}")
        return 'panel'
    def update_columns(self, *args):
        print("called SDI.update_columns with args", args)


class MockReader:
    """stub for plugin program
    """


class MockReader2:
    """stub for plugin program
    """
    def build_data(self):
        """stub
        """
    def update_otherstuff_inbound(self, data):
        """stub
        """
        print('called Reader.update_otherstuff_inbound with arg', data)
        return data
    def get_frameheight(self):
        print('called reader.get_frameheight')
        return 'frameheight'
    def layout_extra_fields(self, *args):
        print('called reader.layout_extra_fields with args', args)


class MockEditor:
    """stub for main.Editor (and its gui component)
    """
    def __init__(self):
        def mock_message(text):
            print(f"called EditorGui.statusbar_message with arg '{text}'")
        print('called Editor.__init__')
        self.gui = types.SimpleNamespace(statusbar_message=mock_message)
        self.pluginfiles = {}


class MockTabGui:
    """stub for gui.TabbedInterface
    """
    def __init__(self, *args):
        print('called TabbedInterface.__init__ with args', args)
        self._removecounter = 0
    def add_button_to_line(self, *args):
        print('called TabbedInterface.add_button_to_line with args', args)
        return 'button'
    def add_combobox_to_line(self, *args, **kwargs):
        print('called TabbedInterface.add_combobox_to_line with args', args, kwargs)
        return 'combobox'
    def add_list_to_line(self, line):
        print('called TabbedInterface.add_list_to_line with arg', line)
    def add_margin_to_line(self, line):
        print('called TabbedInterface.add_margin_to_line with arg', line)
    def add_selector_to_line(self, *args):
        print('called TabbedInterface.add_selector_to_line with args', args)
    def add_separator_to_line(self, line):
        print('called TabbedInterface.add_separator_to_line with arg', line)
    def add_subscreen(self, win):
        # print(f'called TabbedInterface.add_subscreen with arg of type {type(win)}')
        print(f'called TabbedInterface.add_subscreen with arg {win}')
    def add_text_to_line(self, *args):
        print('called TabbedInterface.add_text_to_line with args', args)
        return 'text'
    def add_tool(self, *args):
        print('called TabbedInterface.add_tool with args', args)
    def add_to_selector(self, *args):
        print("called TabbedInterface.add_to_selector with args", args)
    def clear_selector(self):
        """stub
        """
        print('called TabbedInterface.clear_selector')
    def enable_widget(self, *args):
        print('called TabbedInterface.enable_widget with args', args)
    def enable_search_text(self, state):
        print(f"called TabbedInterface.enable_search_text with arg {state}")
    def finalize_display(self, box):
        print('called TabbedInterface.finalize_display with arg', box)
    def format_screen(self):
        print("called TabbedInterface.format_screen")
    def get_button_text(self, arg):
        print("called TabbedInterface.get_button_text with arg", arg)
        return 'on'
    def get_combobox_index(self, arg):
        print('called TabbedInterface.get_combobox_index with arg', arg)
        return 2
    def get_combobox_index_for_item(self, *args):
        print("called TabbedInterface.get_combobox_index_for_item with args", args)
        return 1
    def get_combobox_value(self, arg):
        print('called TabbedInterface.get_combobox_value with arg', arg)
        return 'xxx'
    def get_found_keydef_position(self, *args):
        print("called TabbedInterface.get_found_keydef_position with args", args)
        return 2
    def get_panel(self):
        print('called TabbedInterface.get_panel')
        return None
    def get_search_text(self):
        print("called TabbedInterface.get_search_text")
        return 'this'
    def on_pagechange(self, *args):
        print('called TabbedInterface.on_pagechange with args', args)
    def on_textchange(self, *args):
        print('called TabbedInterface.on_textchange with args', args)
    def refresh_combobox(self, *args):
        print('called TabbedInterface.refresh_combobox with args', args)
    def refresh_locs(self, headers):
        print(f"called TabbedInterface.refresh_locs with arg '{headers}'")
    def remove_tool(self, *args):
        print('called TabbedInterface.remove_tool with args', args)
        self._removecounter += 1
        if self._removecounter % 2 == 0:
            return None
        return f'item #{self._removecounter}'
    def setcaption(self, *args):
        print('called TabbedInterface.setcaption with args', args)
    def set_button_text(self, *args):
        print("called TabbedInterface.set_button_text with args", args)
    def set_combobox_index(self, *args):
        print('called TabbedInterface.set_combobox_index with args', args)
    def set_combobox_text(self, *args):
        print('called TabbedInterface.set_combobox_text with args', args)
    def set_found_keydef_position(self, *args):
        print("called TabbedInterface.set_found_keydef_position with args", args)
    def set_selected_keydef_item(self, *args):
        print("called TabbedInterface.set_selected_keydef_item with args", args)
    def set_selected_panel(self, *args):
        print("called TabbedInterface.set_selected_panel with args", args)
    def set_selected_tool(self, arg):
        print(f"called TabbedInterface.set_selected_tool with arg '{arg}'")
    def set_selector_value(self, *args):
        print('called TabbedInterface.set_selector_value with args', args)
    def setup_search(self):
        print('called TabbedInterface.setup_search')
    def setup_selector(self, arg):
        print('called TabbedInterface.setup_selector with arg', arg)
        return 'selector'
    def start_display(self):
        print('called TabbedInterface.start_display')
        return 'screen'
    def start_line(self, box):
        print('called TabbedInterface.start_line with arg', box)
        return 'line'
    def update_search(self, arg):
        """stub
        """
        print("called TabbedInterface.update_search with arg", arg)


class MockHotkeyPanel:
    """stub for main.HotkeyPanel
    """
    def __init__(self, *args):
        print('called HotkeyPanel.__init__ with args', args)
        self.settings = {}
        self.gui = 'SingleDataInterface'
        self._name = args[1]
        if testee.os.path.basename(args[1]) == 'itsnotthere':
            self.settings[testee.shared.SettType.PLG.value] = 'xxx'
    def __repr__(self):
        """stub
        """
        return f"<HotkeyPanel '{self._name}'>"
    def add_extra_attributes(self):
        print('called HotkeyPanel.add_extra_attributes')
    def add_extrapanel_fields(self):
        print('called HotkeyPanel.add_extrapanel_fields')
        self.b_save = 'b_save'
        self.b_del = 'b_del'
        return ['screen', 'fields']
    def populate_list(self, arg):
        print(f'called HotkeyPanel.populate_list with arg {arg}')
    def readkeys(self):
        """stub
        """
        print('called HotkeyPanel.readkeys')
    def read_settings_from_path(self, arg):
        print(f"called HotkeyPanel.read_settings_from_path with arg '{arg}'")
        return 'no data', [{}, [], {}, {}]
    def refresh_extrapanel(self, arg):
        print(f'called HotkeyPanel.add_extrapanel_fields with arg {arg}')
    def savekeys(self):
        """stub
        """
        print('called HotkeyPanel.savekeys')
        return False
    def setcaptions(self):
        """stub
        """
        print('called HotkeyPanel.setcaptions')
    def set_title(self):
        """stub
        """
        print('called HotkeyPanel.set_title')


class MockGui:
    "stub for gui.Gui"
    def __init__(self, arg):
        print(f'called Gui.__init__ with arg {arg}')
    def close(self):
        print('called Gui.close')
    def go(self, arg):
        print('called Gui.go with arg', arg)
    def resize_empty_screen(self, *args):
        print('called Gui.resize_empty_screen with args', args)
    def setup_empty_screen(self, *args):
        print('called Gui.setup_empty_screen with args', args)
    def setup_list(self, *args):
        print('called Gui.setup_list with args', args)
    def setup_menu(self, **kwargs):
        print('called Gui.setup_menu with args', kwargs)
    def setup_tabs(self):
        print('called Gui.setup_tabs')
    def set_window_title(self, text):
        """stub
        """
        print(f"called Gui.set_window_title with arg '{text}'")
    def statusbar_message(self, *args):
        """stub
        """
        print('called Gui.statusbar_message with args', args)
    def start_display(self):
        print('called Gui.start_display')
        return 'box'
    def add_choicebook_to_display(self, *args):
        print('called Gui.add_choicebook_to_display with args', args)
    def add_exitbutton_to_display(self, *args):
        print('called Gui.add_exitbutton_to_display with args', args)
        return 'exitbutton'


class MockChoiceBook:
    "stub for main.ChoiceBook"
    def __init__(self, arg):
        print(f"called ChoiceBook.__init__ with arg '{arg}'")
        self.gui = MockTabGui()
    def on_page_changed(self, start):
        print(f"called ChoiceBook.on_page_changed with arg '{start}'")
    def init_search_buttons(self):
        print("called ChoiceBook.init_search_buttons")
    def enable_search_buttons(self, **kwargs):
        print("called ChoiceBook.enable_search_buttons with args", kwargs)
    def set_selected_tool(self, arg):
        print('called ChoiceBook.set_selected_tool with arg', arg)


def test_readlang(monkeypatch, tmp_path):
    """unittest for main.readlang
    """
    mock_lang = tmp_path / 'hotkeys' / 'lang'
    monkeypatch.setattr(testee.shared, 'HERELANG', mock_lang)
    mock_lang.mkdir(parents=True)
    (mock_lang / 'en').write_text("#deze overslaan\n\ncode text\n\nalso a code with text\n")
    assert testee.readlang('en') == {'code': 'text', 'also': 'a code with text'}


def test_normalize_cloc(monkeypatch):
    """unittest for main.normalize_cloc
    """
    def mock_expand(arg):
        return f'expanded/{arg}'
    def mock_abspath(arg):
        return f'absolute/{arg}'
    monkeypatch.setattr(testee.os.path, 'expanduser', mock_expand)
    monkeypatch.setattr(testee.os.path, 'abspath', mock_abspath)
    assert testee.normalize_cloc('/cloc') == "absolute/expanded//cloc"
    assert testee.normalize_cloc('~/cloc') == "absolute/expanded/~/cloc"
    assert testee.normalize_cloc('./cloc') == "absolute/expanded/./cloc"
    assert testee.normalize_cloc('cloc') == "absolute/expanded/projects/hotkeys/cloc"


def test_read_config(monkeypatch, tmp_path):
    """unittest for main.read_config
    """
    monkeypatch.setattr(testee, 'initial_config', {'x': '', 'a': ''})
    ini = tmp_path / 'configfile'
    ini.write_text('{"a": "b", "q": "r"}\n')
    assert testee.read_config(ini) == {'a': 'b', 'filename': ini, 'x': ''}


def test_write_config(monkeypatch, capsys, tmp_path):
    """unittest for main.write_config
    """
    def mock_copy(*args):
        """stub
        """
        print('called shutil.copyfile with args', args)
    def mock_dump(*args):
        """stub
        """
        print('called json.dump with arg', args[0])
    monkeypatch.setattr(testee.json, 'dump', mock_dump)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'exists', lambda *x: False)
    monkeypatch.setattr(testee, 'initial_config', {'x': '', 'a': ''})
    ini = tmp_path / 'settingsfile'
    testee.write_config({'a': 'b', 'filename': ini, 'x': 'y'})
    assert capsys.readouterr().out == "called json.dump with arg {'a': 'b', 'x': 'y'}\n"
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'exists', lambda *x: True)
    testee.write_config({'a': 'b', 'filename': ini, 'x': 'y'})
    assert capsys.readouterr().out == (f"called shutil.copyfile with args ('{ini}',"
                                       f" '{str(ini) + '~'}')\n"
                                       "called json.dump with arg {'a': 'b', 'x': 'y'}\n")
    testee.write_config({'a': 'b', 'filename': ini, 'x': 'y'}, nobackup=True)
    assert capsys.readouterr().out == "called json.dump with arg {'a': 'b', 'x': 'y'}\n"


def test_read_columntitledata(monkeypatch, capsys, tmp_path):
    """unittest for main.read_columntitledata
    """
    def mock_log(*args, **kwargs):
        """stub
        """
        print('called shared.log with args', args, kwargs)
    monkeypatch.setattr(testee.shared, 'log', mock_log)
    monkeypatch.setattr(testee.shared, 'HERELANG', tmp_path / 'languages')
    editor = types.SimpleNamespace(ini={'lang': 'en.lng'})
    (tmp_path / 'languages').mkdir()
    (tmp_path / 'languages' / 'en.lng').write_text(
            'aaa\nbbb\n\n# Keyboard mapping\nID1 text1\nID2 text 2\n#end\nID3 text3\n#x\n#y\n')
    assert testee.read_columntitledata(editor) == (['ID1', 'ID2'], ['text1', 'text 2'])
    assert capsys.readouterr().out == (
            "called shared.log with args (['aaa'],) {'always': True}\n"
            "called shared.log with args (['bbb'],) {'always': True}\n"
            "called shared.log with args (['ID1', 'text1'],) {'always': True}\n"
            "called shared.log with args (['ID2', 'text 2'],) {'always': True}\n"
            "called shared.log with args (['ID3', 'text3'],) {'always': True}\n")


def test_add_columntitledata(monkeypatch, tmp_path):
    """unittest for main.add_columntitledata
    """
    mock_lang = tmp_path / 'hotkeys' / 'lang'
    monkeypatch.setattr(testee.shared, 'HERELANG', mock_lang)
    mock_lang.mkdir(parents=True)
    oldtext_start = 'aa bb\ncc dd\n\n# Keyboard mapping...\npp rr\n'
    oldtext_end = '\nss tt\n'
    (mock_lang / 'en').write_text(oldtext_start + oldtext_end)
    (mock_lang / 'nl').write_text(oldtext_start + oldtext_end)
    newdata = {'en': {'a': 'b'}, 'nl': {'x': 'y'}}
    testee.add_columntitledata(newdata)
    assert (mock_lang / 'en~').read_text() == oldtext_start + oldtext_end
    assert (mock_lang / 'nl~').read_text() == oldtext_start + oldtext_end
    assert (mock_lang / 'en').read_text() == oldtext_start + 'a b\n' + oldtext_end
    assert (mock_lang / 'nl').read_text() == oldtext_start + 'x y\n' + oldtext_end


def test_update_paths(monkeypatch, capsys):
    """unittest for main.update_paths
    """
    def mock_write(*args):
        """stub
        """
        print('called path.write with args', args)
    def mock_initjson(*args):
        """stub
        """
        print('called initjson with args', args)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'write_text', mock_write)
    monkeypatch.setattr(testee, 'initjson', mock_initjson)
    paths = (('xx', 'yy.json'), ('aa', 'bb.json'), ('qq', 'rr.json'))
    pathdata = {'xx': ['xx.yy.zz', 'xxx', 1, 0, 0], 'aa': ['.bb.cc', 'aaa', 1, 1, 1]}
    assert testee.update_paths(paths, pathdata) == [('xx', 'yy.json'), ('aa', 'bb.json'),
                                                    ('qq', 'rr.json')]
    assert capsys.readouterr().out == (
            f"called path.write with args ({testee.BASE / 'xx' / 'yy' / 'zz.py'!r},"
            f" {testee.plugin_skeleton!r})\n"
            f"called initjson with args ({testee.BASE / 'yy.json'!r},"
            " ['xx.yy.zz', 'xxx', 1, 0, 0])\n"
            f"called path.write with args ({testee.BASE / 'bb' / 'cc.py'!r},"
            f" {testee.plugin_skeleton!r})\n"
            f"called initjson with args ({testee.BASE / 'bb.json'!r}, ['.bb.cc', 'aaa', 1, 1, 1])\n")


def test_initjson(monkeypatch, capsys):
    """unittest for main.initjson
    """
    def mock_write(*args):
        """stub
        """
        print('called writejson with args', args)
    monkeypatch.setattr(testee, 'writejson', mock_write)
    monkeypatch.setattr(testee.shared, 'settingnames', ['x', 'y'])
    monkeypatch.setattr(testee, 'initial_columns', [('a', 1, True), ('b', 2, False)])
    testee.initjson('settfile', ['xxx', 'yyy'])
    assert capsys.readouterr().out == ("called writejson with args"
                                       " ('settfile', None, {'x': 'xxx', 'y': 'yyy'},"
                                       " [('a', 1, True), ('b', 2, False)], {}, {})\n")
    assert testee.initjson('', ['xxx', 'yyy']) == ({'x': 'xxx', 'y': 'yyy'},
                                                   [('a', 1, True), ('b', 2, False)], {})
    assert capsys.readouterr().out == ""


def test_readjson(tmp_path):
    """unittest for main.readjson
    """
    plgfile = tmp_path / 'test' / 'plugin.json'
    plgfile.parent.mkdir()
    plgfile.write_text('{"settings": {"settings": "dict"}, "column_info": [["column", "info"]],'
                       ' "keydata": {"keycombo": "dict"}, "otherstuff": {}}')
    assert testee.readjson(plgfile) == ({"settings": "dict"}, [["column", "info"]],
                                        {"keycombo": "dict"}, {"otherstuff": {}})


def test_writejson(tmp_path, capsys):
    """unittest for main.writejson
    """
    def mock_update_out(data):
        print('called Reader.update_otherstuff_outbound with arg', data)
        return data
    def mock_update_in(data):
        print('called Reader.update_otherstuff_inbound with arg', data)
        return data
    plgfile = tmp_path / 'test' / 'plugin.json'
    plgfile.parent.mkdir()
    reader = MockReader()
    testee.writejson(plgfile, reader, {'settings': 'dict'}, [['column', 'info']],
                     {'keycombo': 'dict'}, {})
    assert plgfile.read_text() == ('{"settings": {"settings": "dict"},'
                                   ' "column_info": [["column", "info"]],'
                                   ' "keydata": {"keycombo": "dict"}}')
    assert capsys.readouterr().out == ''
    testee.writejson(str(plgfile), reader, {'settings': 'dict'}, [['column', 'info']],
                     {'keycombo': 'dict'},
                     {'xxx': {'a', 'b', 'c'}, 'yyy': ['q', 'r'], 'zzz': {'m': 'n'}})
    assert plgfile.read_text() == ('{"settings": {"settings": "dict"},'
                                   ' "column_info": [["column", "info"]],'
                                   ' "keydata": {"keycombo": "dict"},'
                                   ' "xxx": ["a", "b", "c"], "yyy": ["q", "r"], "zzz": {"m": "n"}}')
    assert capsys.readouterr().out == ''
    reader.update_otherstuff_outbound = mock_update_out
    reader.update_otherstuff_inbound = mock_update_in
    otherstuff = {'xxx': {'a', 'b', 'c'}, 'yyy': ['q', 'r'], 'zzz': {'m': 'n'}}
    testee.writejson(str(plgfile), reader, {'settings': 'dict'}, [['column', 'info']],
                     {'keycombo': 'dict'},
                     {'xxx': {'a', 'b', 'c'}, 'yyy': ['q', 'r'], 'zzz': {'m': 'n'}})
    assert plgfile.read_text() == ('{"settings": {"settings": "dict"},'
                                   ' "column_info": [["column", "info"]],'
                                   ' "keydata": {"keycombo": "dict"},'
                                   ' "xxx": ["a", "b", "c"], "yyy": ["q", "r"], "zzz": {"m": "n"}}')
    assert capsys.readouterr().out == (
            f"called Reader.update_otherstuff_outbound with arg {otherstuff}\n"
            f"called Reader.update_otherstuff_inbound with arg {otherstuff}\n")
    reader = None
    testee.writejson(str(plgfile), reader, {'settings': 'dict'}, [['column', 'info']],
                     {'keycombo': 'dict'},
                     {'xxx': {'a', 'b', 'c'}, 'yyy': ['q', 'r'], 'zzz': {'m': 'n'}})
    assert plgfile.read_text() == ('{"settings": {"settings": "dict"},'
                                   ' "column_info": [["column", "info"]],'
                                   ' "keydata": {"keycombo": "dict"},'
                                   ' "xxx": ["a", "b", "c"], "yyy": ["q", "r"], "zzz": {"m": "n"}}')
    assert capsys.readouterr().out == ''


def test_quick_check(monkeypatch, capsys):
    """unittest for main.quick_check
    """
    def mock_log_exc():
        """stub
        """
        print('called shared.log_exc')
    def mock_readjson(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return {}, [[], []], {}, {}
    def mock_readjson_2(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return {}, [[], []], {1: [], 2: []}, {}
    def mock_readjson_3(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return {}, [[], []], {1: ['x', 'y'], 2: ['a', 'b']}, {}
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log_exc)
    monkeypatch.setattr(testee, 'readjson', mock_readjson)
    testee.quick_check('plugin.json')
    assert capsys.readouterr().out == ('called readjson with arg `plugin.json`\n'
                                       'plugin.json: No keydefs found in this file\n')
    monkeypatch.setattr(testee, 'readjson', mock_readjson_2)
    testee.quick_check('plugin.json')
    assert capsys.readouterr().out == ('called readjson with arg `plugin.json`\n'
                                       'inconsistent item lengths in plugin.json\n'
                                       '1 []\n')
    monkeypatch.setattr(testee, 'readjson', mock_readjson_3)
    testee.quick_check('plugin.json')
    assert capsys.readouterr().out == ('called readjson with arg `plugin.json`\n'
                                       'plugin.json: No errors found\n')

    assert capsys.readouterr().out == ("")


class TestHotkeyPanel:
    """unittests for main.HotkeyPanel
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.HotkeyPanel object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called HotkeyPanel.__init__ with args', args)
        monkeypatch.setattr(testee.HotkeyPanel, '__init__', mock_init)
        testobj = testee.HotkeyPanel()
        testobj.parent = types.SimpleNamespace(parent=types.SimpleNamespace())
        testobj.gui = MockSDI()  # types.SimpleNamespace()
        testobj.reader = types.SimpleNamespace()
        assert capsys.readouterr().out == ('called HotkeyPanel.__init__ with args ()\n'
                                           'called SingleDataInterface.__init__ with args ()\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.__init__
        """
        # def mock_update(arg):
        #     print(f'called plugin.update_otherstuff_inbound with arg {arg}')
        #     return {'other': 'stuff'}
        def mock_read(self, arg):
            print(f"called HotkeyPanel.read_settings_from_path with arg '{arg}'")
            self.reader = MockReader()
            return '', [{testee.shared.SettType.PNL.value: 'PanelName',
                         testee.shared.SettType.DETS.value: False},
                        [('fld1', 1), ('fld2', 2)], {}, {'other': 'stuff'}]
        def mock_read_2(self, arg):
            print(f"called HotkeyPanel.read_settings_from_path with arg '{arg}'")
            self.reader = MockReader2()
            return '', [{testee.shared.SettType.PNL.value: 'PanelName',
                         testee.shared.SettType.DETS.value: True,
                         testee.shared.SettType.RDEF.value: False},
                        [('fld1', 1), ('fld2', 2)], {}, {'other': 'stuff'}]
        parent = types.SimpleNamespace(parent=types.SimpleNamespace(title='A title',
                                                                    captions={'cap': 'tions'}),
                                       gui='parent gui')
        monkeypatch.setattr(testee.gui, 'SingleDataInterface', MockSDI)
        monkeypatch.setattr(testee.HotkeyPanel, 'read_settings_from_path',
                            MockHotkeyPanel.read_settings_from_path)
        monkeypatch.setattr(testee.HotkeyPanel, 'populate_list',
                            MockHotkeyPanel.populate_list)
        monkeypatch.setattr(testee.HotkeyPanel, 'add_extra_attributes',
                            MockHotkeyPanel.add_extra_attributes)
        monkeypatch.setattr(testee.HotkeyPanel, 'add_extrapanel_fields',
                            MockHotkeyPanel.add_extrapanel_fields)
        monkeypatch.setattr(testee.HotkeyPanel, 'refresh_extrapanel',
                            MockHotkeyPanel.refresh_extrapanel)
        testobj = testee.HotkeyPanel(parent, 'path/to/settings')
        assert testobj.pad == 'path/to/settings'
        assert testobj.parent == parent
        assert testobj.title == 'A title'
        assert testobj.captions == {'cap': 'tions'}
        assert not testobj.modified
        assert testobj.filtertext == ''
        assert not testobj.has_extrapanel
        assert isinstance(testobj.gui, testee.gui.SingleDataInterface)
        assert capsys.readouterr().out == (
                f"called SingleDataInterface.__init__ with args ('parent gui', {testobj})\n"
                "called HotkeyPanel.read_settings_from_path with arg 'path/to/settings'\n"
                "called SDI.setup_empty_screen with args ('no data', 'A title')\n"
                "called SDI.finalize_screen with args ()\n")

        monkeypatch.setattr(testee.HotkeyPanel, 'read_settings_from_path', mock_read)
        testobj.parent.parent.captions = {'fld1': 'head1', 'fld2': 'head2'}
        testobj = testee.HotkeyPanel(parent, 'path/to/settings')
        assert testobj.pad == 'path/to/settings'
        assert testobj.parent == parent
        assert testobj.title == 'PanelName'
        assert testobj.captions == {'fld1': 'head1', 'fld2': 'head2'}
        assert not testobj.modified
        assert testobj.filtertext == ''
        assert not testobj.has_extrapanel
        assert isinstance(testobj.gui, testee.gui.SingleDataInterface)
        assert testobj.parent.page == testobj
        assert testobj.p0list == 'p0list'
        assert capsys.readouterr().out == (
                f"called SingleDataInterface.__init__ with args ('parent gui', {testobj})\n"
                "called HotkeyPanel.read_settings_from_path with arg 'path/to/settings'\n"
                "called SDI.setup_list with args"
                f" (['head1', 'head2'], [1, 2], {testobj.gui.on_item_selected})\n"
                "called HotkeyPanel.populate_list with arg p0list\n"
                "called SDI.finalize_screen with args ()\n")

        monkeypatch.setattr(testee.HotkeyPanel, 'read_settings_from_path', mock_read_2)
        testobj = testee.HotkeyPanel(parent, 'path/to/settings')
        assert testobj.pad == 'path/to/settings'
        assert testobj.parent == parent
        assert testobj.title == 'PanelName'
        assert testobj.captions == {'fld1': 'head1', 'fld2': 'head2'}
        assert not testobj.modified
        assert testobj.filtertext == ''
        assert testobj.has_extrapanel
        assert isinstance(testobj.gui, testee.gui.SingleDataInterface)
        assert testobj.parent.page == testobj
        assert testobj.p0list == 'p0list'
        assert testobj.fields == ['fld1', 'fld2']
        assert capsys.readouterr().out == (
                f"called SingleDataInterface.__init__ with args ('parent gui', {testobj})\n"
                "called HotkeyPanel.read_settings_from_path with arg 'path/to/settings'\n"
                "called SDI.setup_list with args"
                f" (['head1', 'head2'], [1, 2], {testobj.gui.on_item_selected})\n"
                "called HotkeyPanel.populate_list with arg p0list\n"
                "called Reader.update_otherstuff_inbound with arg {'other': 'stuff'}\n"
                "called HotkeyPanel.add_extra_attributes\n"
                "called HotkeyPanel.add_extrapanel_fields\n"
                "called SDI.set_extrapanel_editable with args"
                " (['screen', 'fields'], ['b_save', 'b_del'], False)\n"
                "called SDI.getfirstitem with args ('p0list',)\n"
                "called HotkeyPanel.add_extrapanel_fields with arg first_item\n"
                "called SDI.set_listselection with args ('p0list', 0)\n"
                "called SDI.finalize_screen with args ()\n")

    def test_read_settings_from_path(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.read_settings_from_path
        """
        def mock_log(text):
            """stub
            """
            print(f'called shared.log with arg `{text}`')
        def mock_log_exc():
            """stub
            """
            print('called shared.log_exc')
        def mock_readjson_exc_1(arg):
            """stub
            """
            raise ValueError('A ValueError')
        def mock_readjson_exc_2(arg):
            """stub
            """
            raise FileNotFoundError('A FileNotFoundError')
        def mock_readjson(arg):
            """stub
            """
            print(f'called readjson with arg `{arg}`')
            return {}, [[], []], {}, {}
        def mock_readjson_2(arg):
            """stub
            """
            print(f'called readjson with arg `{arg}`')
            return {'x': 'y'}, [], {}, {}
        def mock_readjson_3(arg):
            """stub
            """
            print(f'called readjson with arg `{arg}`')
            return {'x': 'y'}, [[], []], {}, {}
        def mock_readjson_4(arg):
            """stub
            """
            print(f'called readjson with arg `{arg}`')
            return ({'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': False}, [[], []],
                    {}, {})
        def mock_import_nok(*args):
            """stub
            """
            print('called importlib.import_module with args', args)
            raise ImportError
        def mock_import_ok(*args):
            """stub
            """
            print('called importlib.import_module with args', args)
            return mock_reader
        monkeypatch.setattr(testee.gui, 'SingleDataInterface', MockSDI)
        monkeypatch.setattr(testee.shared, 'log_exc', mock_log_exc)
        monkeypatch.setattr(testee.shared, 'log', mock_log)
        monkeypatch.setattr(testee, 'readjson', mock_readjson)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.captions = {'I_NOPATH': 'no path', 'I_NOSET': '{}', 'I_NOSETFIL': '{} not found',
                          'I_NOSETT': '{} no settings', 'I_NODATA': 'no data'}
        pad = 'NO_PATH'
        assert testobj.read_settings_from_path(pad) == ('no path', ({}, [], {}, {}))

        assert testobj.read_settings_from_path('') == ('empty filename', ({}, [], {}, {}))

        monkeypatch.setattr(testee, 'readjson', mock_readjson_exc_1)
        assert testobj.read_settings_from_path('plugin.json') == ('A ValueError', ({}, [], {}, {}))

        monkeypatch.setattr(testee, 'readjson', mock_readjson_exc_2)
        assert testobj.read_settings_from_path('plugin.json') == ('plugin.json not found',
                                                                  ({}, [], {}, {}))

        monkeypatch.setattr(testee, 'readjson', mock_readjson)
        assert testobj.read_settings_from_path('plugin.json') == ('no data',
                                                                  ({}, [[], []], {}, {}))

        monkeypatch.setattr(testee, 'readjson', mock_readjson_2)
        assert testobj.read_settings_from_path('plugin.json') == ('no data',
                                                                  ({'x': 'y'}, [], {}, {}))

        monkeypatch.setattr(testee, 'readjson', mock_readjson_3)
        assert testobj.read_settings_from_path('plugin.json') == ('no plugin code',
                                                                  ({'x': 'y'}, [[], []], {}, {}))

        monkeypatch.setattr(testee, 'readjson', mock_readjson_4)
        monkeypatch.setattr(testee.importlib, 'import_module', mock_import_nok)
        assert testobj.read_settings_from_path('plugin.json') == ('no plugin code', (
                {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': False},
                [[], []], {}, {}))

        mock_reader = MockReader()
        monkeypatch.setattr(testee.importlib, 'import_module', mock_import_ok)
        assert testobj.read_settings_from_path('plugin.json') == ('', (
                {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': False},
                [[], []], {}, {}))
        assert testobj.reader == mock_reader

    def test_readkeys(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.readkeys
        """
        def mock_readjson(arg):
            """stub
            """
            print(f'called readjson with arg `{arg}`')
            return {}, [], 'jsondata', {}
        monkeypatch.setattr(testee, 'readjson', mock_readjson)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pad = 'plugin.json'
        testobj.readkeys()
        assert testobj.data == 'jsondata'
        assert capsys.readouterr().out == 'called readjson with arg `plugin.json`\n'

    def test_savekeys(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.savekeys
        """
        def mock_logexc():
            print('called shared.log_exc')
        def mock_writejson(*args):
            print('called writejson with args', args)
        def mock_savekeys(arg):
            print('called Reader.savekeys with arg', arg)
        def mock_set_title(**kwargs):
            print('called HotkeyPanel.set_title with args', kwargs)
        monkeypatch.setattr(testee.shared, 'log_exc', mock_logexc)
        monkeypatch.setattr(testee, 'writejson', mock_writejson)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.pad = 'xxxx.json'
        testobj.settings = ['settings']
        testobj.column_info = ['column', 'info']
        testobj.data = ['data']
        testobj.otherstuff = ['other', 'stuff']
        testobj.set_title = mock_set_title
        testobj.parent.parent.ini = {'lang': 'en'}
        assert not testobj.savekeys()
        assert testobj.parent.data == testobj.data
        assert capsys.readouterr().out == ""
        testobj.parent.data = []
        testobj.reader.savekeys = mock_savekeys
        assert testobj.savekeys()
        assert testobj.parent.data == testobj.data
        assert capsys.readouterr().out == (
                f"called Reader.savekeys with arg {testobj}\n"
                f"called writejson with args ('xxxx.json', {testobj.reader},"
                " ['settings'], ['column', 'info'], ['data'], ['other', 'stuff'])\n"
                "called HotkeyPanel.set_title with args {'modified': False}\n")

    def test_setcaptions(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.setcaptions
        """
        def mock_title():
            print('called HotKeyPanel.set_title')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.parent.captions = {'C_KTXT': 'key', 'M_WIN': 'win', 'M_CTRL': 'ctrl',
                                          'M_ALT': 'alt', 'M_SHFT': 'shift', 'C_CNTXT': 'context',
                                          'C_CMD': 'command', 'C_PARMS': 'parms', 'C_CTRL': 'control',
                                          'C_BPARMS': 'bparms', 'C_APARMS': 'aparms',
                                          'C_FEAT': 'feature', 'C_SAVE': 'save', 'C_DEL': 'delete'}
        testobj.set_title = mock_title
        testobj.lbl_key = 'lbl_key'
        testobj.cb_win = 'cb_win'
        testobj.cb_ctrl = 'cb_ctrl'
        testobj.cb_alt = 'cb_alt'
        testobj.cb_shift = 'cb_shift'
        testobj.lbl_context = 'lbl_context'
        testobj.txt_cmd = 'txt_cmd'
        testobj.lbl_parms = 'lbl_parms'
        testobj.lbl_controls = 'lbl_controls'
        testobj.pre_parms_label = 'pre_parms_label'
        testobj.post_parms_label = 'post_parms_label'
        testobj.feature_label = 'feature_label'
        testobj.b_save = 'b_save'
        testobj.b_del = 'b_del'
        testobj.fields = ['C_KEY']
        testobj.has_extrapanel = False
        testobj.setcaptions()
        assert capsys.readouterr().out == ("called HotKeyPanel.set_title\n")
        testobj.fields = []
        testobj.has_extrapanel = True
        testobj.setcaptions()
        assert capsys.readouterr().out == (
                "called HotKeyPanel.set_title\n"
                "called SDI.set_label_text with args ('b_save', 'save')\n"
                "called SDI.set_label_text with args ('b_del', 'delete')\n"
                "called SDI.resize_if_necessary\n")
        testobj.fields = ['C_KEY', 'C_MODS', 'C_CNTXT', 'C_CMD', 'C_PARMS', 'C_CTRL', 'C_BPARMS',
                          'C_APARMS', 'C_FEAT']
        testobj.setcaptions()
        assert capsys.readouterr().out == (
                "called HotKeyPanel.set_title\n"
                "called SDI.set_label_text with args ('lbl_key', 'key')\n"
                "called SDI.set_label_text with args ('cb_win', '+win  ')\n"
                "called SDI.set_label_text with args ('cb_ctrl', '+ctrl  ')\n"
                "called SDI.set_label_text with args ('cb_alt', '+alt  ')\n"
                "called SDI.set_label_text with args ('cb_shift', '+shift  ')\n"
                "called SDI.set_label_text with args ('lbl_context'," " 'context:')\n"
                "called SDI.set_label_text with args ('txt_cmd', 'command:')\n"
                "called SDI.set_label_text with args ('lbl_parms', 'parms:')\n"
                "called SDI.set_label_text with args ('lbl_controls'," " 'control:')\n"
                "called SDI.set_label_text with args ('pre_parms_label'," " 'bparms:')\n"
                "called SDI.set_label_text with args ('post_parms_label'," " 'aparms:')\n"
                "called SDI.set_label_text with args ('feature_label'," " 'feature:')\n"
                "called SDI.set_label_text with args ('b_save', 'save')\n"
                "called SDI.set_label_text with args ('b_del', 'delete')\n"
                "called SDI.resize_if_necessary\n")

    def test_populate_list(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.populate_list
        """
        def mock_logexc():
            print('called shared.log_exc')
        monkeypatch.setattr(testee.shared, 'log_exc', mock_logexc)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.captions = {'C_DFLT': 'default', 'C_RDEF': 'custom'}
        testobj.data = {}
        testobj.p0list = 'p0list'
        testobj.populate_list(testobj.p0list)
        assert capsys.readouterr().out == "called SDI.clear_list with arg p0list\n"
        testobj.column_info = [('xxx', 10, False), ('yyy', 20, False), ('zzz', 5, True)]
        testobj.data = {'a': 'key error', '1': ['aaa', 'bbb', 'S'], 2: ['ppp', 'qqq', 'rrr']}
        testobj.populate_list(testobj.p0list)
        assert capsys.readouterr().out == (
                "called SDI.clear_list with arg p0list\n"
                "called shared.log_exc\n"
                "called SDI.build_listitem with args ('1',)\n"
                "called SDI.set_listitemtext with args ('item-1', 0, 'aaa')\n"
                "called SDI.set_listitemtext with args ('item-1', 1, 'bbb')\n"
                "called SDI.set_listitemtext with args ('item-1', 2, 'default')\n"
                "called SDI.add_listitem with args ('p0list', 'item-1')\n"
                "called SDI.build_listitem with args (2,)\n"
                "called SDI.set_listitemtext with args ('item-2', 0, 'ppp')\n"
                "called SDI.set_listitemtext with args ('item-2', 1, 'qqq')\n"
                "called SDI.set_listitemtext with args ('item-2', 2, 'custom')\n"
                "called SDI.add_listitem with args ('p0list', 'item-2')\n"
                "called SDI.set_listselection with args ('p0list', 0)\n")
        testobj.data = {3: ['ppp', 'qqq']}  # te weinig kolommen in data
        with pytest.raises(IndexError) as exc:
            testobj.populate_list(testobj.p0list)
        assert str(exc.value) == 'list index out of range'
        assert capsys.readouterr().out == (
                "called SDI.clear_list with arg p0list\n"
                "called SDI.build_listitem with args (3,)\n"
                "called SDI.set_listitemtext with args ('item-3', 0, 'ppp')\n"
                "called SDI.set_listitemtext with args ('item-3', 1, 'qqq')\n"
                "['ppp', 'qqq']\n")
        testobj.data = {3: ['ppp', 'qqq', 'R', 'sss']}  # te veel kolommen
        testobj.populate_list(testobj.p0list)
        assert capsys.readouterr().out == (
                "called SDI.clear_list with arg p0list\n"
                "called SDI.build_listitem with args (3,)\n"
                "called SDI.set_listitemtext with args ('item-3', 0, 'ppp')\n"
                "called SDI.set_listitemtext with args ('item-3', 1, 'qqq')\n"
                "called SDI.set_listitemtext with args ('item-3', 2, 'custom')\n"
                "called SDI.add_listitem with args ('p0list', 'item-3')\n"
                "called SDI.set_listselection with args ('p0list', 0)\n")

    def test_add_extra_attributes(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.add_extra_attributes
        """
        def mock_logexc():
            print('called shared.log_exc')
        def mock_add(arg):
            print('called Reader.add_extra_attributes with arg', arg)
        monkeypatch.setattr(testee.shared, 'log_exc', mock_logexc)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reader = types.SimpleNamespace()
        testobj.add_extra_attributes()
        assert testobj.init_origdata == ['', False, False, False, False, '', '', '', '', '', '', '']
        assert testobj.field_indexes == {'C_KEY': 0, 'C_MODS': [1, 2, 3, 4], 'C_CNTXT': 5, 'C_CMD': 6,
                                         'C_PARMS': 7, 'C_CTRL': 8, 'C_BPARMS': 9, 'C_APARMS': 10,
                                         'C_FEAT': 11}
        assert testobj.keylist == [
                "'", '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ';',
                '=', 'A', 'B', 'Backspace', 'C', 'D', 'Del', 'Down', 'E', 'End', 'Enter', 'Esc', 'F',
                'F1', 'F10', 'F11', 'F12', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'G', 'H',
                'Home', 'I', 'Insert', 'J', 'K', 'L', 'Left', 'Letter', 'Letter(s)', 'M', 'N', 'Num*',
                'Num+', 'Num-', 'Num/', 'O', 'P', 'PgDn', 'PgUp', 'Q', 'R', 'Right', 'S', 'Space', 'T',
                'Tab', 'U', 'Up', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '`']
        assert testobj.contextslist == []
        assert testobj.commandslist == []
        assert testobj.defkeys == []
        assert testobj.contextactionsdict == {}
        assert testobj.omsdict == {}
        assert testobj.descriptions == {}
        assert capsys.readouterr().out == ""
        testobj.reader = types.SimpleNamespace(add_extra_attributes=mock_add)
        testobj.add_extra_attributes()
        assert testobj.init_origdata == ['', False, False, False, False, '', '', '', '', '', '', '']
        assert testobj.field_indexes == {'C_KEY': 0, 'C_MODS': [1, 2, 3, 4], 'C_CNTXT': 5, 'C_CMD': 6,
                                         'C_PARMS': 7, 'C_CTRL': 8, 'C_BPARMS': 9, 'C_APARMS': 10,
                                         'C_FEAT': 11}
        assert testobj.keylist == [
                "'", '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ';',
                '=', 'A', 'B', 'Backspace', 'C', 'D', 'Del', 'Down', 'E', 'End', 'Enter', 'Esc', 'F',
                'F1', 'F10', 'F11', 'F12', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'G', 'H',
                'Home', 'I', 'Insert', 'J', 'K', 'L', 'Left', 'Letter', 'Letter(s)', 'M', 'N', 'Num*',
                'Num+', 'Num-', 'Num/', 'O', 'P', 'PgDn', 'PgUp', 'Q', 'R', 'Right', 'S', 'Space', 'T',
                'Tab', 'U', 'Up', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '`']
        assert testobj.contextslist == []
        assert testobj.commandslist == []
        assert testobj.defkeys == []
        assert testobj.contextactionsdict == {}
        assert testobj.omsdict == {}
        assert testobj.descriptions == {}
        assert capsys.readouterr().out == f"called Reader.add_extra_attributes with arg {testobj}\n"

    def test_add_extrapanel_fields(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.add_extrapanel_fields
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.reader = MockReader()
        testobj.captions = {'C_KTXT': 'key', 'M_CTRL': 'ctrl', 'M_ALT': 'alt', 'M_SHFT': 'shift',
                            'M_WIN': 'win', 'C_CNTXT': 'ctx', 'C_CTXT': 'cmnd', 'C_PARMS': 'params',
                            'C_CTRL': 'where', 'C_BPARMS': 'fore', 'C_APARMS': 'aft',
                            'C_FEAT': 'feat', 'C_SAVE': 'save', 'C_DEL': 'del'}
        testobj.fields = []
        testobj.keylist = None
        testobj.contextslist = ['contexts']
        testobj.commandslist = ['command']
        testobj.controlslist = ['controls']
        testobj.featurelist = ['features']
        testobj.add_extrapanel_fields()
        assert testobj.b_save == 'button'
        assert testobj.b_del == 'button'
        assert capsys.readouterr().out == (
                "called SDI.start_extrapanel with arg 90\n"
                "called SDI.start_line with arg panel\n"
                "called SDI.add_separator_to_line with arg line\n"
                f"called SDI.add_button_to_line with args ('line', 'save', {testobj.on_update})\n"
                f"called SDI.add_button_to_line with args ('line', 'del', {testobj.on_delete})\n"
                "called SDI.start_line with arg panel\n")
        testobj.reader = MockReader2()
        testobj.fields = ['C_MODS', 'C_KEY', 'C_CNTXT', 'C_CMD', 'C_PARMS', 'C_CTRL',
                          'C_BPARMS', 'C_APARMS', 'C_FEAT', 'C_DESC']
        testobj.add_extrapanel_fields()
        for field in (testobj.lbl_key, testobj.lbl_context, testobj.txt_cmd, testobj.lbl_parms,
                      testobj.lbl_controls,
                      testobj.pre_parms_label, testobj.post_parms_label, testobj.feature_label):
            assert field == 'label'
        for field in (testobj.cmb_context, testobj.cmb_commando, testobj.cmb_controls,
                      testobj.feature_select):
            assert field == 'combobox'
        for field in (testobj.cb_ctrl, testobj.cb_alt, testobj.cb_shift, testobj.cb_win):
            assert field == 'checkbox'
        for field in (testobj.txt_key, testobj.txt_parms, testobj.pre_parms_text,
                      testobj.post_parms_text):
            assert field == 'textinput'
        assert testobj.b_save == 'button'
        assert testobj.b_del == 'button'
        assert testobj.txt_oms == 'textarea'
        assert capsys.readouterr().out == (
                "called reader.get_frameheight\n"
                "called SDI.start_extrapanel with arg frameheight\n"
                "called SDI.start_line with arg panel\n"
                "called SDI.add_label_to_line with args ('line', 'key') {}\n"
                "called SDI.add_textfield_to_line with args"
                f" ('line',) {{'width': 90, 'callback': {testobj.on_key_edit}}}\n"
                "called SDI.add_label_to_line with args ('line', '  ') {}\n"
                "called SDI.add_checkbox_to_line with args ('line', '+ctrl ')\n"
                "called SDI.add_checkbox_to_line with args ('line', '+alt ')\n"
                "called SDI.add_checkbox_to_line with args ('line', '+shift ')\n"
                "called SDI.add_checkbox_to_line with args ('line', '+win ')\n"
                "called SDI.add_separator_to_line with arg line\n"
                "called SDI.add_label_to_line with args ('line', 'ctx') {}\n"
                "called SDI.add_combobox_to_line with args"
                " ('line',) {'width': 110, 'items': ['contexts']}\n"
                "called SDI.add_label_to_line with args ('line', 'cmnd') {}\n"
                "called SDI.add_combobox_to_line with args ('line',) {'width': 150, 'items': []}\n"
                "called SDI.add_label_to_line with args ('line', 'params') {'add': False}\n"
                "called SDI.add_textfield_to_line with args ('line',) {'width': 280, 'add': False}\n"
                "called SDI.add_label_to_line with args ('line', 'where') {'add': False}\n"
                "called SDI.add_combobox_to_line with args ('line',)"
                " {'items': ['controls'], 'add': False}\n"
                "called SDI.add_label_to_line with args ('line', 'fore') {}\n"
                "called SDI.add_textfield_to_line with args ('line',) {}\n"
                "called SDI.add_label_to_line with args ('line', 'aft') {}\n"
                "called SDI.add_textfield_to_line with args ('line',) {}\n"
                "called SDI.add_label_to_line with args ('line', 'feat') {}\n"
                "called SDI.add_combobox_to_line with args ('line',) {'items': ['features']}\n"
                f"called SDI.add_button_to_line with args ('line', 'save', {testobj.on_update})\n"
                f"called SDI.add_button_to_line with args ('line', 'del', {testobj.on_delete})\n"
                "called SDI.start_line with arg panel\n"
                "called SDI.add_descfield_to_line with arg line\n"
                f"called reader.layout_extra_fields with args ({testobj}, 'line')\n")
        testobj.fields = ['C_KEY']
        testobj.keylist = ['keys']
        testobj.add_extrapanel_fields()
        assert testobj.cmb_key == 'combobox'
        assert testobj.b_save == 'button'
        assert testobj.b_del == 'button'
        assert testobj.txt_oms == 'textarea'
        assert capsys.readouterr().out == (
                "called reader.get_frameheight\n"
                "called SDI.start_extrapanel with arg frameheight\n"
                "called SDI.start_line with arg panel\n"
                "called SDI.add_label_to_line with args ('line', 'key') {}\n"
                "called SDI.add_combobox_to_line with args"
                " ('line',) {'width': 90, 'items': ['keys']}\n"
                "called SDI.add_separator_to_line with arg line\n"
                f"called SDI.add_button_to_line with args ('line', 'save', {testobj.on_update})\n"
                f"called SDI.add_button_to_line with args ('line', 'del', {testobj.on_delete})\n"
                "called SDI.start_line with arg panel\n"
                f"called reader.layout_extra_fields with args ({testobj}, 'line')\n")

    def test_set_title(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.set_title
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.captions = {"T_MOD": '(*)'}
        testobj.modified = True
        testobj.title = 'xxxx'
        testobj.set_title()
        assert capsys.readouterr().out == ("called SDI.set_title with arg 'xxxx (*)'\n")
        testobj.modified = False
        testobj.set_title()
        assert capsys.readouterr().out == ("called SDI.set_title with arg 'xxxx'\n")
        testobj.modified = False
        testobj.set_title(modified=True)
        assert capsys.readouterr().out == ("called SDI.set_title with arg 'xxxx (*)'\n")
        testobj.modified = True
        testobj.set_title(modified=False)
        assert capsys.readouterr().out == ("called SDI.set_title with arg 'xxxx'\n")

    def test_on_update(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.on_update
        """
        def mock_check():
            print("called HotKeyPanel.check_for_changes")
            return 'xxx', 'yyy'
        def mock_check_sel(arg):
            print(f"called HotKeyPanel.check_for_selected_keydef with arg '{arg}'")
            return 'aaa', 'bbb'
        def mock_apply(*args):
            print('called HotkeyPanel.apply_changes with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check_for_changes = mock_check
        testobj.check_for_selected_keydef = mock_check_sel
        testobj.apply_changes = mock_apply
        testobj.p0list = 'p0list'
        testobj.on_update()
        assert capsys.readouterr().out == (
                "called HotKeyPanel.check_for_changes\n"
                "called HotKeyPanel.check_for_selected_keydef with arg 'yyy'\n"
                "called HotkeyPanel.apply_changes with args ('aaa', 'bbb', 'yyy')\n"
                "called SDI.set_focus_to with arg 'p0list'\n")

    def test_on_delete(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.on_delete
        """
        def mock_apply():
            print('called HotkeyPanel.apply_deletion')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.apply_deletion = mock_apply
        testobj.p0list = 'p0list'
        testobj.on_delete()
        assert capsys.readouterr().out == ("called HotkeyPanel.apply_deletion\n"
                                           "called SDI.set_focus_to with arg 'p0list'\n")

    def test_exit(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.exit
        """
        def mock_ask(*args):
            print('called gui.ask_ync_question with args', args)
            return True, None
        def mock_ask_2(*args):
            print('called gui.ask_ync_question with args', args)
            return False, True
        def mock_ask_3(*args):
            print('called gui.ask_ync_question with args', args)
            return False, False
        def mock_save():
            print('called HotkeyPanel.savekeys')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testee.gui.ask_ync_question = mock_ask
        testobj.savekeys = mock_save
        testobj.modified = False
        assert testobj.exit()
        assert capsys.readouterr().out == ""

        testobj.modified = True
        assert testobj.exit()
        assert capsys.readouterr().out == (
                f"called gui.ask_ync_question with args ({testobj.gui}, 'Q_SAVXIT')\n"
                "called HotkeyPanel.savekeys\n")

        testee.gui.ask_ync_question = mock_ask_2
        assert not testobj.exit()
        assert capsys.readouterr().out == (
                f"called gui.ask_ync_question with args ({testobj.gui}, 'Q_SAVXIT')\n")

        testee.gui.ask_ync_question = mock_ask_3
        assert testobj.exit()
        assert capsys.readouterr().out == (
                f"called gui.ask_ync_question with args ({testobj.gui}, 'Q_SAVXIT')\n")

    def test_on_key_edit(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.on_key_edit
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.field_indexes = {'C_KEY': 1}
        testobj._origdata = ['', 'snork']
        testobj._newdata = ['', '']
        testobj.initializing_screen = True
        testobj.fields = []
        testobj.b_save = 'b_save'
        testobj.defchanged = True
        testobj.on_key_edit('x')
        assert testobj.defchanged
        assert capsys.readouterr().out == ""
        testobj.initializing_screen = False
        # deze test was omdat de routine eerder voorzag in meer situaties dan C_KEY
        # testobj.on_key_edit('xx')
        # assert not testobj.defchanged
        # assert testobj._newdata == ['', '']
        # assert capsys.readouterr().out == "called SDI.get_widget_text with args ('xx',)\n"
        testobj.fields = ['C_KEY']
        testobj.on_key_edit('xx')
        assert testobj.defchanged
        assert testobj._newdata == ['', 'snark']
        assert capsys.readouterr().out == ("called SDI.get_widget_text with args ('xx',)\n"
                                           "called SDI.enable_button with args ('b_save', True)\n")
        testobj._origdata = ['', 'snark']
        testobj._newdata = ['', '']
        testobj.on_key_edit('xx')
        assert not testobj.defchanged
        assert testobj._newdata == ['', '']
        assert capsys.readouterr().out == ("called SDI.get_widget_text with args ('xx',)\n"
                                           "called SDI.enable_button with args ('b_save', False)\n")

    def test_on_combobox(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.on_combobox
        """
        def mock_set(value):
            print(f'called HotkeyPanel.set_changed_indicators with arg {value}')
        def mock_adjust(*args):
            print('called HotkeyPanel.adjust_other_fields_if_needed with args', args)
        def mock_reset(value):
            print(f'called HotkeyPanel.reset_changed_indicators_if_needed with arg {value}')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.cmb_key = types.SimpleNamespace(name='C_KEY')
        testobj.gui.cmb_commando = types.SimpleNamespace(name='C_CMD')
        testobj.gui.cmb_context = types.SimpleNamespace(name='C_CNTXT')
        testobj.gui.cmb_controls = types.SimpleNamespace(name='C_CTRL')
        testobj.set_changed_indicators = mock_set
        testobj.reset_changed_indicators_if_needed = mock_reset
        testobj.adjust_other_fields_if_needed = mock_adjust
        testobj.field_indexes = {'C_KEY': 0, 'C_CNTXT': 1, 'C_CMD': 2, 'C_CTRL': 3}
        testobj.fields = ['C_KEY', 'C_CNTXT', 'C_CMD', 'C_CTRL']
        testobj._origdata = ['', '', '', '']
        testobj._newdata = ['', '', '', '']

        testobj.initializing_screen = True
        testobj.gui.initializing_keydef = True
        testobj.on_combobox()
        assert capsys.readouterr().out == ""
        testobj.initializing_screen = False
        testobj.on_combobox()
        assert capsys.readouterr().out == ""
        testobj.gui.initializing_keydef = False

        testobj.on_combobox('None')
        assert capsys.readouterr().out == "called SDI.get_choice_value with args ('None',)\n"

        testobj.on_combobox(testobj.gui.cmb_key)
        assert testobj._newdata == ['abcdef', '', '', '']
        assert capsys.readouterr().out == (
            f"called SDI.get_choice_value with args ({testobj.gui.cmb_key},)\n"
            f"called HotkeyPanel.adjust_other_fields_if_needed with args ({testobj.gui.cmb_key},"
            " 'abcdef')\n"
            "called HotkeyPanel.set_changed_indicators with arg True\n")
        testobj._newdata = ['', '', '', '']
        testobj.on_combobox(testobj.gui.cmb_context)
        assert testobj._newdata == ['', 'abcdef', '', '']
        assert capsys.readouterr().out == (
            f"called SDI.get_choice_value with args ({testobj.gui.cmb_context},)\n"
            f"called HotkeyPanel.adjust_other_fields_if_needed with args ({testobj.gui.cmb_context},"
            " 'abcdef')\n"
            "called HotkeyPanel.set_changed_indicators with arg True\n")
        testobj._newdata = ['', '', '', '']
        testobj.on_combobox(testobj.gui.cmb_commando)
        assert testobj._newdata == ['', '', 'abcdef', '']
        assert capsys.readouterr().out == (
            f"called SDI.get_choice_value with args ({testobj.gui.cmb_commando},)\n"
            f"called HotkeyPanel.adjust_other_fields_if_needed with args ({testobj.gui.cmb_commando},"
            " 'abcdef')\n"
            "called HotkeyPanel.set_changed_indicators with arg True\n")
        testobj._newdata = ['', '', '', '']
        testobj.on_combobox(testobj.gui.cmb_controls)
        assert testobj._newdata == ['', '', '', 'abcdef']
        assert capsys.readouterr().out == (
            f"called SDI.get_choice_value with args ({testobj.gui.cmb_controls},)\n"
            f"called HotkeyPanel.adjust_other_fields_if_needed with args ({testobj.gui.cmb_controls},"
            " 'abcdef')\n"
            "called HotkeyPanel.set_changed_indicators with arg True\n")
        testobj._origdata = ['', '', '', 'abcdef']
        # breakpoint()
        testobj.on_combobox(testobj.gui.cmb_controls)
        assert capsys.readouterr().out == (
            f"called SDI.get_choice_value with args ({testobj.gui.cmb_controls},)\n"
            "called HotkeyPanel.reset_changed_indicators_if_needed with arg namespace(name='C_CTRL')\n")

    def test_adjust_other_fields_if_needed(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.adjust_other_fields_if_needed
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.captions = {'M_NODESC': 'no desc'}
        testobj.adjust_other_fields_if_needed("", '')
        assert capsys.readouterr().out == ("")
        testobj.cmb_context = types.SimpleNamespace(name='C_CNTXT')
        testobj.adjust_other_fields_if_needed(testobj.cmb_context, '')
        assert capsys.readouterr().out == ("")
        testobj.contextactionsdict = {}
        testobj.adjust_other_fields_if_needed(testobj.cmb_context, '')
        assert capsys.readouterr().out == ("")
        testobj.commandslist = ['xx']
        testobj.adjust_other_fields_if_needed(testobj.cmb_context, '')
        assert capsys.readouterr().out == ("")
        testobj.cmb_commando = types.SimpleNamespace(name='C_CMD')
        testobj.adjust_other_fields_if_needed(testobj.cmb_context, '')
        assert capsys.readouterr().out == ("called SDI.init_combobox with args"
                                           " (namespace(name='C_CMD'), ['xx'])\n")
        testobj.contextactionsdict = {'yy': ['zz']}
        testobj.adjust_other_fields_if_needed(testobj.cmb_context, 'yy')
        assert capsys.readouterr().out == ("called SDI.init_combobox with args"
                                           " (namespace(name='C_CMD'), ['zz'])\n")
        testobj.descriptions = {}
        testobj.adjust_other_fields_if_needed(testobj.cmb_commando, '')
        assert capsys.readouterr().out == ("")
        testobj.txt_oms = types.SimpleNamespace(name='C_TEXT')
        testobj.adjust_other_fields_if_needed(testobj.cmb_commando, '')
        assert capsys.readouterr().out == ("called SDI.set_textfield_value with args"
                                           " (namespace(name='C_TEXT'), 'no desc')\n")
        testobj.descriptions = {'qq': 'rrrr'}
        testobj.adjust_other_fields_if_needed(testobj.cmb_commando, 'qq')
        assert capsys.readouterr().out == ("called SDI.set_textfield_value with args"
                                           " (namespace(name='C_TEXT'), 'rrrr')\n")

    def test_reset_changed_indicators_if_needed(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.reset_changed_indicators_if_needed
        """
        def mock_set(arg):
            print('called HotkeyPanel.set_changed_indicators with arg', arg)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.field_indexes = {'C_KEY': 3, 'C_CMD': 2}
        testobj._origdata = ['1', '2', '3', '4']
        testobj.set_changed_indicators = mock_set
        testobj.reset_changed_indicators_if_needed("")
        assert capsys.readouterr().out == ("")
        testobj.cmb_commando = types.SimpleNamespace(name='C_CMD')
        testobj.reset_changed_indicators_if_needed("")
        assert capsys.readouterr().out == (
                "called SDI.get_combobox_value with arg namespace(name='C_CMD')\n")
        testobj.cmb_key = types.SimpleNamespace(name='C_KEY')
        testobj.reset_changed_indicators_if_needed("")
        assert capsys.readouterr().out == (
                "called SDI.get_combobox_value with arg namespace(name='C_CMD')\n")
        testobj.reset_changed_indicators_if_needed(testobj.cmb_commando)
        assert capsys.readouterr().out == (
                "called SDI.get_combobox_value with arg namespace(name='C_KEY')\n")
        testobj.reset_changed_indicators_if_needed(testobj.cmb_key)
        assert capsys.readouterr().out == (
                "called SDI.get_combobox_value with arg namespace(name='C_CMD')\n")
        testobj._origdata = ['1', '2', 'C_CMD', 'C_KEY']
        # breakpoint()
        testobj.reset_changed_indicators_if_needed(testobj.cmb_commando)
        assert capsys.readouterr().out == (
                "called SDI.get_combobox_value with arg namespace(name='C_KEY')\n"
                "called HotkeyPanel.set_changed_indicators with arg False\n")
        testobj.reset_changed_indicators_if_needed(testobj.cmb_key)
        assert capsys.readouterr().out == (
                "called SDI.get_combobox_value with arg namespace(name='C_CMD')\n"
                "called HotkeyPanel.set_changed_indicators with arg False\n")

    def test_set_changed_indicators(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.set_changed_indicators
        """
        def mock_enable(value):
            print(f"called HotkeyPanelGui.enable_save with arg '{value}')")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.enable_save = mock_enable
        testobj.defchanged = False
        testobj.fields = []
        testobj.set_changed_indicators(True)
        assert testobj.defchanged
        assert capsys.readouterr().out == ""
        testobj.defchanged = True
        testobj.fields = ['C_CMD']
        testobj.b_save = 'b_save'
        testobj.set_changed_indicators(False)
        assert not testobj.defchanged
        assert capsys.readouterr().out == "called SDI.enable_button with args ('b_save', False)\n"

    def test_on_checkbox(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.on_checkbox
        """
        def mock_set(value):
            print(f'called HotkeyPanel.set_changed_indicators with arg {value}')
        def mock_get_value(*args):
            print('called SingleDataInterface.get_check_value with args', args)
            return 'qqq', True
        def mock_get_state(cb):
            print(f'called SingleDataInterface.get_check_state with arg {cb}')
            return True
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_changed_indicators = mock_set
        testobj.field_indexes = {'C_MODS': [0, 1, 2, 3]}
        testobj.gui.get_check_value = mock_get_value
        testobj.gui.get_checkbox_state = mock_get_state
        testobj.cb_shift = 'xxx'
        testobj.cb_ctrl = 'yyy'
        testobj.cb_alt = 'zzz'
        testobj.cb_win = 'qqq'
        testobj._origdata = [True, True, True, False]
        testobj._newdata = testobj._origdata
        testobj.initializing_screen = True
        testobj.on_checkbox()
        assert capsys.readouterr().out == ""

        testobj.initializing_screen = False
        testobj.gui.initializing_keydef = False
        testobj._origdata = [True, True, True, False]
        testobj._newdata = testobj._origdata
        testobj.on_checkbox()
        assert testobj._newdata == [True, True, True, True]
        assert capsys.readouterr().out == ("called SingleDataInterface.get_check_value with args ()\n"
                                           "called HotkeyPanel.set_changed_indicators with arg True\n")

        testobj._origdata = [True, True, True, False]
        testobj._newdata = testobj._origdata
        testobj.gui.initializing_keydef = True
        testobj.on_checkbox()
        assert testobj._newdata == [True, True, True, True]
        assert capsys.readouterr().out == "called SingleDataInterface.get_check_value with args ()\n"

        testobj._origdata = [True, True, True, True, 'xxx']
        testobj._newdata = testobj._origdata
        testobj.fields = []
        testobj.on_checkbox()
        assert testobj._newdata == testobj._origdata
        assert capsys.readouterr().out == ("called SingleDataInterface.get_check_value with args ()\n"
                                           "called SingleDataInterface.get_check_state with arg xxx\n"
                                           "called SingleDataInterface.get_check_state with arg yyy\n"
                                           "called SingleDataInterface.get_check_state with arg zzz\n"
                                           "called SingleDataInterface.get_check_state with arg qqq\n"
                                           "called HotkeyPanel.set_changed_indicators with arg True\n")
        testobj._origdata = [False, True, True, True, 'xxx']
        testobj._newdata = testobj._origdata
        testobj.fields = []
        testobj.on_checkbox()
        assert testobj._newdata == testobj._origdata
        assert capsys.readouterr().out == ("called SingleDataInterface.get_check_value with args ()\n"
                                           "called SingleDataInterface.get_check_state with arg xxx\n"
                                           "called SingleDataInterface.get_check_state with arg yyy\n"
                                           "called SingleDataInterface.get_check_state with arg zzz\n"
                                           "called SingleDataInterface.get_check_state with arg qqq\n")

    def test_refresh_extrapanel(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.refresh_extrapanel
        """
        def mock_get_list(arg):
            nonlocal counter
            print(f"called SDI.get_valuelist with arg '{arg}'")
            counter += 1
            if counter == 2:
                return []
            return ['value', 'list']
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.fields = []
        testobj.data = {'1': []}
        testobj.init_origdata = ['', False, False, False, False, '', '', '', '', '', '', '']
        testobj.field_indexes = {'C_KEY': 0, 'C_MODS': [1, 2, 3, 4], 'C_CNTXT': 5, 'C_CMD': 6,
                                 'C_PARMS': 7, 'C_CTRL': 8, 'C_BPARMS': 9, 'C_APARMS': 10,
                                 'C_FEAT': 11}
        testobj.get_valuelist = mock_get_list
        testobj.cmb_key = 'key'
        testobj.b_del = 'b_del'

        testobj.refresh_extrapanel('')
        assert not hasattr(testobj, '_origdata')
        assert capsys.readouterr().out == ""
        testobj.refresh_extrapanel('selitem')
        assert testobj._origdata == testobj.init_origdata
        assert capsys.readouterr().out == "called SDI.get_itemdata with arg 'selitem'\n"
        testobj.fields = ['C_KEY', 'C_MODS', 'C_TYPE']
        testobj.data = {'1': ['X', 'CWAS', 'S']}
        testobj.settings = {testee.shared.SettType.RDEF.value: 0}
        testobj.keylist = None
        testobj.txt_key = 'key text'
        testobj.refresh_extrapanel('selitem')
        assert testobj._origdata == ['X', False, False, False, False, '', '', '', '', '', '', '']
        assert capsys.readouterr().out == (
                "called SDI.get_itemdata with arg 'selitem'\n"
                "called SDI.set_textfield_value with args ('key text', 'X')\n")
        testobj.data = {'1': ['X', 'ACS', 'S']}
        testobj.cb_shift = ' with shift'
        testobj.cb_ctrl = ' with ctrl'
        testobj.cb_alt = ' with alt'
        testobj.cb_win = ' with win'
        testobj.settings[testee.shared.SettType.RDEF.value] = 1
        testobj.keylist = ['a', 'b', 'c']
        counter = 0
        testobj.refresh_extrapanel('selitem')
        assert testobj._origdata == ['X', True, True, True, False, '', '', '', '', '', '', '']
        assert capsys.readouterr().out == (
                "called SDI.get_itemdata with arg 'selitem'\n"
                "called SDI.enable_button with args ('b_del', False)\n"
                "called SDI.set_checkbox_state with args (' with shift', True)\n"
                "called SDI.set_checkbox_state with args (' with ctrl', True)\n"
                "called SDI.set_checkbox_state with args (' with alt', True)\n"
                "called SDI.set_checkbox_state with args (' with win', False)\n"
                "called SDI.get_valuelist with arg 'C_KEY'\n"
                "called SDI.set_combobox_string with args"
                " ('key', 'X', ['value', 'list'])\n")
        testobj.fields = ['C_KEY', 'C_TYPE', 'C_CNTXT', 'C_CMD', 'C_DESC', 'C_PARMS', 'C_CTRL',
                          'C_BPARMS', 'C_APARMS', 'C_FEAT']
        testobj.data = {'1': ['X', 'U', 'xx', 'yy', 'zz', 'aa', 'bb', 'cc', 'dd', 'ee']}
        testobj.settings[testee.shared.SettType.PLG.value] = 'xxx.yyy.zzz'
        counter = 0
        testobj.b_save = 'b_save'
        testobj.refresh_extrapanel('selitem')
        assert testobj._origdata == ['X', False, False, False, False, '', '', '', '', '', '', '']
        assert capsys.readouterr().out == (
                "called SDI.get_itemdata with arg 'selitem'\n"
                "called SDI.enable_button with args ('b_save', False)\n"
                "called SDI.enable_button with args ('b_del', False)\n"
                "called SDI.enable_button with args ('b_del', True)\n"
                "called SDI.get_valuelist with arg 'C_KEY'\n"
                "called SDI.set_combobox_string with args"
                " ('key', 'X', ['value', 'list'])\n"
                "zzz: C_CNTXT aanwezig in fields zonder corresponderend veld op scherm\n"
                "zzz: C_CMD aanwezig in fields zonder corresponderend veld op scherm\n"
                "zzz: C_DESC aanwezig in fields zonder corresponderend veld op scherm\n"
                "zzz: C_PARMS aanwezig in fields zonder corresponderend veld op scherm\n"
                "zzz: C_CTRL aanwezig in fields zonder corresponderend veld op scherm\n"
                "zzz: C_BPARMS aanwezig in fields zonder corresponderend veld op scherm\n"
                "zzz: C_APARMS aanwezig in fields zonder corresponderend veld op scherm\n"
                "zzz: C_FEAT aanwezig in fields zonder corresponderend veld op scherm\n")
        testobj.cmb_context = 'context'
        testobj.cmb_commando = 'command'
        testobj.txt_oms = 'desc'
        testobj.txt_parms = 'parms'
        testobj.cmb_controls = 'controls'
        testobj.pre_parms_text = 'pre-args'
        testobj.post_parms_text = 'post-args'
        testobj.feature_select = 'feature'
        counter = 0
        testobj.refresh_extrapanel('selitem')
        assert testobj._origdata == ['X', False, False, False, False, 'xx', 'yy', 'aa', 'bb', 'cc',
                                     'dd', 'ee']
        assert capsys.readouterr().out == (
                "called SDI.get_itemdata with arg 'selitem'\n"
                "called SDI.enable_button with args ('b_save', False)\n"
                "called SDI.enable_button with args ('b_del', False)\n"
                "called SDI.enable_button with args ('b_del', True)\n"
                "called SDI.get_valuelist with arg 'C_KEY'\n"
                "called SDI.set_combobox_string with args ('key', 'X', ['value', 'list'])\n"
                "called SDI.get_valuelist with arg 'C_CNTXT'\n"
                "called SDI.get_valuelist with arg 'C_CMD'\n"
                "called SDI.set_combobox_string with args ('command', 'yy', ['value', 'list'])\n"
                "called SDI.set_textfield_value with args ('desc', 'zz')\n"
                "called SDI.set_textfield_value with args ('parms', 'aa')\n"
                "called SDI.get_valuelist with arg 'C_CTRL'\n"
                "called SDI.set_combobox_string with args ('controls', 'bb', ['value', 'list'])\n"
                "called SDI.set_textfield_value with args ('pre-args', 'cc')\n"
                "called SDI.set_textfield_value with args ('post-args', 'dd')\n"
                "called SDI.get_valuelist with arg 'C_FEAT'\n"
                "called SDI.set_combobox_string with args ('feature', 'ee', ['value', 'list'])\n")

    def test_get_valuelist(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.get_valuelist
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.keylist = ['a']
        testobj.contextslist = ['b']
        testobj.fields = ['C_CNTXT']
        testobj.contextactionsdict = {'yy': ['c']}
        testobj.commandslist = ['d']
        testobj.controlslist = ['e']
        testobj.featurelist = ['f']
        testobj.cmb_commando = 'xx'
        testobj.cmb_context = types.SimpleNamespace(name='yy')

        assert testobj.get_valuelist('xx') == []
        assert capsys.readouterr().out == ""
        assert testobj.get_valuelist('C_KEY') == ['a']
        assert capsys.readouterr().out == ""
        assert testobj.get_valuelist('C_CNTXT') == ['b']
        assert capsys.readouterr().out == ""
        assert testobj.get_valuelist('C_CMD') == ['c']
        assert capsys.readouterr().out == (
                "called SDI.init_combobox with args ('xx',)\n"
                f"called SDI.get_combobox_value with arg {testobj.cmb_context}\n"
                "called SDI.init_combobox with args ('xx', ['c'])\n")
        testobj.contextactionsdict = {}
        assert testobj.get_valuelist('C_CMD') == ['d']
        assert capsys.readouterr().out == (
                "called SDI.init_combobox with args ('xx',)\n"
                f"called SDI.get_combobox_value with arg {testobj.cmb_context}\n"
                "called SDI.init_combobox with args ('xx', ['d'])\n")
        testobj.fields = []
        assert testobj.get_valuelist('C_CMD') == ['d']
        assert capsys.readouterr().out == ""
        assert testobj.get_valuelist('C_CTRL') == ['e']
        assert capsys.readouterr().out == ""
        assert testobj.get_valuelist('C_FEAT') == ['f']
        assert capsys.readouterr().out == ""

    def test_process_changed_selection(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.process_changed_selection
        """
        def mock_check():
            print("called HotKeyPanel.check_for_changes")
            return 'xxx', 'yyy'
        def mock_check_keydef(arg):
            print(f"called HotKeyPanel.check_for_selected_keydef with arg '{arg}'")
            return True, 1
        def mock_ask(*args):
            print("called HotKeyPanel.ask_what_to_do with args", args)
            return False
        def mock_ask_2(*args):
            print("called HotKeyPanel.ask_what_to_do with args", args)
            return True
        def mock_apply(*args):
            print("called HotKeyPanel.apply_changes with args", args)
            return 'item a'
        def mock_get(arg):
            print(f"called HotKeyPanel.get_listbox_selection with arg '{arg}'")
            return 'item b'
        def mock_refresh(arg):
            print(f"called HotKeyPanel.refresh_extrapanel with arg '{arg}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check_for_changes = mock_check
        testobj.check_for_selected_keydef = mock_check_keydef
        testobj.ask_what_to_do = mock_ask
        testobj.apply_changes = mock_apply
        testobj.gui.get_listbox_selection = mock_get
        testobj.refresh_extrapanel = mock_refresh
        testobj.settings = {testee.shared.SettType.RDEF.value: False}  # '0'}
        testobj.initializing_screen = True
        testobj.p0list = 'p0list'
        testobj.process_changed_selection('newitem', 'olditem')
        assert capsys.readouterr().out == (
                "called HotKeyPanel.get_listbox_selection with arg 'p0list'\n"
                "called HotKeyPanel.refresh_extrapanel with arg 'i'\n")
        testobj.settings = {testee.shared.SettType.RDEF.value: True}  # '1'}
        testobj.process_changed_selection('newitem', 'olditem')
        assert capsys.readouterr().out == (
                "called HotKeyPanel.refresh_extrapanel with arg 'newitem'\n")
        testobj.initializing_screen = False
        testobj.process_changed_selection('newitem', 'olditem')
        assert capsys.readouterr().out == (
                "called HotKeyPanel.check_for_changes\n"
                "called HotKeyPanel.check_for_selected_keydef with arg 'yyy'\n"
                "called HotKeyPanel.ask_what_to_do with args (True, 'newitem', 'olditem')\n"
                "called HotKeyPanel.refresh_extrapanel with arg 'newitem'\n")
        testobj.ask_what_to_do = mock_ask_2
        testobj.process_changed_selection('newitem', 'olditem')
        assert capsys.readouterr().out == (
                "called HotKeyPanel.check_for_changes\n"
                "called HotKeyPanel.check_for_selected_keydef with arg 'yyy'\n"
                "called HotKeyPanel.ask_what_to_do with args (True, 'newitem', 'olditem')\n"
                "called HotKeyPanel.apply_changes with args (True, 1, 'yyy')\n"
                "called HotKeyPanel.refresh_extrapanel with arg 'item a'\n")

    def test_check_for_changes(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.check_for_changes
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.field_indexes = {'C_KEY': 0, 'C_MODS': [1, 2, 3, 4], 'C_CNTXT': 5}
        testobj._origdata = ['x', True, False, True, False, 'zzz']
        testobj._newdata = ['x', True, False, True, False, 'zzz']
        assert testobj.check_for_changes() == ([False, False, False],
                                               ['x', [True, False, True, False], 'zzz'])
        testobj._newdata = ['y', False, True, False, True, 'zzzz']
        assert testobj.check_for_changes() == ([True, True, True],
                                               ['y', [False, True, False, True], 'zzzz'])

    def test_check_for_selected_keydef(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.check_for_selected_keydef
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.fields = ['C_KEY', 'C_MODS', 'C_CNTXT']
        testobj.data = {1: ['x', 'y', 'z', 'aaaaaaa'], 2: ['p', 'q', 'r', 'bbbbbb']}
        assert testobj.check_for_selected_keydef(['x', 'y', 'z']) == (True, 1)
        assert testobj.check_for_selected_keydef(['k', 'l', 'm']) == (False, -1)

    def test_ask_what_to_do(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.ask_what_to_do
        """
        def mock_ask(*args):
            print('called gui.ask_question with args', args)
            return 'answered'
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj._newdata = ['x', 'y', 'z']
        testobj._origdata = ['x', 'y', 'z']
        assert not testobj.ask_what_to_do(True, 'newitem', 'olditem')
        assert capsys.readouterr().out == ""
        testobj._origdata = ['x', 'y', 'w']
        assert testobj.ask_what_to_do(True, 'newitem', 'olditem') == 'answered'
        assert capsys.readouterr().out == ("called gui.ask_question with args"
                                           f" ({testobj.gui}, 'Q_SAVCHG')\n")
        assert testobj.ask_what_to_do(True, 'newitem', None) == 'answered'
        assert capsys.readouterr().out == ("called gui.ask_question with args"
                                           f" ({testobj.gui}, 'Q_DPLKEY')\n")
        assert testobj.ask_what_to_do(False, 'newitem', 'olditem') == 'answered'
        assert capsys.readouterr().out == ("called gui.ask_question with args"
                                           f" ({testobj.gui}, 'Q_SAVCHG')\n")
        assert testobj.ask_what_to_do(False, 'newitem', None)
        assert capsys.readouterr().out == ""

    def test_apply_changes(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.apply_changes
        """
        def mock_populate(pos):
            print(f"called HotkeyPanel.populate_list with arg '{pos}'")
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.populate_list = mock_populate
        testobj.p0list = 'p0list'
        testobj.fields = [('C_KEY', 10, 'x'), ('C_MODS', 4, 'y'), ('C_CMD', 12, 'z')]
        testobj.field_indexes = {'C_KEY': 0, 'C_MODS': 1, 'C_CMD': 2}
        testobj.data = {1: ['x', 'y', 'z'], 2: ['a', 'b', 'c']}
        testobj._newdata = ['ppp', 'qqq', 'rrr']
        assert testobj.apply_changes(True, 1, (0, 'WASD')) == 'item at position'
        assert testobj.data == {1: ['ppp', 'WASD', 'rrr'], 2: ['a', 'b', 'c']}
        assert capsys.readouterr().out == (
                "called SDI.get_listbox_selection with arg p0list\n"
                # "called SDI.get_listitem_position with args ('p0list', 'keydef X')\n"
                # "called SDI.get_listitem_at_position with args ('p0list', 'position of keydef X')\n"
                "called SDI.get_listitem_at_position with args ('p0list', 'position')\n"
                # "called HotkeyPanel.populate_list with arg 'position of keydef X'\n")
                "called HotkeyPanel.populate_list with arg 'position'\n")
        testobj.data = {1: ['x', 'y', 'z'], 2: ['a', 'b', 'c']}
        assert testobj.apply_changes(False, 1, (0, 'WASD')) == 'item at position'
        assert testobj.data == {0: ['a', 'b', 'c'], 1: ['ppp', 'qqq', 'rrr'], 2: ['x', 'y', 'z']}
        assert capsys.readouterr().out == (
                "called SDI.get_listbox_selection with arg p0list\n"
                # "called SDI.get_listitem_position with args ('p0list', 'keydef X')\n"
                # "called SDI.get_listitem_at_position with args ('p0list', 'position of keydef X')\n"
                "called SDI.get_listitem_at_position with args ('p0list', 'position')\n"
                # "called HotkeyPanel.populate_list with arg 'position of keydef X'\n")
                "called HotkeyPanel.populate_list with arg 'position'\n")
        testobj.data = {1: ['x', 'y', 'z'], 2: ['a', 'b', 'c']}

    def _test_apply_deletion(self, monkeypatch, capsys):
        """unittest for HotkeyPanel.apply_deletion
        """
        # twijfels of de te testen routine wel klopt, dus test uitgezet
        # theoretisch zou ik desondanks deze moeten kunnen definiëren
        # de regels zijn:
        # als er geen TYPE indicator is dan kan er gewoon verwijderd worden
        # als er een TYPE indicator is en deze een S aangeeft, dan kan er niet verwijderd worden
        # als er een TYPE indicator is en deze een R aangeeft, dan kijken of er een standaard definitie is
        #   zo ja, deze terugzetten, zo nee dan net als als er geen standaard is de definitie leeg maken
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_set_title(**kwargs):
            print("called HotkeyPanel.set_title with args", kwargs)
        def mock_populate_list(self, **kwargs):
            print("called HotkeyPanel.populate_list with args", kwargs)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.set_title = mock_set_title
        testobj.populate_list = mock_populate_list
        testobj.defkeys = {'key': 'orig'}
        testobj.omsdict = {'orig': 'original'}
        testobj.captions = {'001': 'C_TYPE'}
        testobj.data = {'1': ['key', 'S']}
        testobj.apply_deletion()
        assert testobj.data == {'1': ['key', 'S']}
        assert capsys.readouterr().out == (
                "called SDI.get_selected_keydef\n"
                "called SDI.get_keydef_position with arg 'keydef X'\n"
                "called SDI.get_itemdata with arg 'keydef X'\n"
                f"called gui.show_message with args ({testobj.parent}, 'I_STDDEF') {{}}\n")
        testobj.data = {'1': ['key', 'U']}
        testobj.apply_deletion()
        assert testobj.data == {'1': ['key', 'U']}
        assert capsys.readouterr().out == (
                "called SDI.get_selected_keydef\n"
                "called SDI.get_keydef_position with arg 'keydef X'\n"
                "called SDI.get_itemdata with arg 'keydef X'\n"
                "called SDI.enable_save with arg False\n"
                "called SDI.enable_delete with arg False\n"
                "called HotkeyPanel.set_title with args {'modified': True}\n"
                "called HotkeyPanel.populate_list with args {}\n")

        testobj.captions = {'001': 'C_KEY'}
        testobj.data = {'1': ['key', 'U']}
        testobj.apply_deletion()
        assert testobj.data == {'1': ('key', 'S', 'orig', 'original')}
        assert capsys.readouterr().out == (
                "called SDI.get_selected_keydef\n"
                "called SDI.get_keydef_position with arg 'keydef X'\n"
                "called SDI.get_itemdata with arg 'keydef X'\n"
                "called SDI.enable_save with arg False\n"
                "called SDI.enable_delete with arg False\n"
                "called HotkeyPanel.set_title with args {'modified': True}\n"
                "called HotkeyPanel.populate_list with args {}\n")
        testobj.omsdict = {}
        testobj.data = {'1': ['key', 'U']}
        testobj.apply_deletion()
        assert testobj.data == {'1': ('key', 'S', '', 'orig')}
        assert capsys.readouterr().out == (
                "called SDI.get_selected_keydef\n"
                "called SDI.get_keydef_position with arg 'keydef X'\n"
                "called SDI.get_itemdata with arg 'keydef X'\n"
                "called SDI.enable_save with arg False\n"
                "called SDI.enable_delete with arg False\n"
                "called HotkeyPanel.set_title with args {'modified': True}\n"
                "called HotkeyPanel.populate_list with args {}\n")
        testobj.defkeys = {}
        testobj.data = {'1': ['key', 'U']}
        testobj.apply_deletion()
        assert testobj.data == {}
        assert capsys.readouterr().out == (
                "called SDI.get_selected_keydef\n"
                "called SDI.get_keydef_position with arg 'keydef X'\n"
                "called SDI.get_itemdata with arg 'keydef X'\n"
                "called SDI.enable_save with arg False\n"
                "called SDI.enable_delete with arg False\n"
                "called HotkeyPanel.set_title with args {'modified': True}\n"
                "called HotkeyPanel.populate_list with args {}\n")
        testobj.captions = {'001': 'C_KY'}
        testobj.data = {'1': ['key', 'U']}
        testobj.apply_deletion()
        assert testobj.data == {'1': ['key', 'U']}
        assert capsys.readouterr().out == (
                "called SDI.get_selected_keydef\n"
                "called SDI.get_keydef_position with arg 'keydef X'\n"
                "called SDI.get_itemdata with arg 'keydef X'\n"
                "called SDI.enable_save with arg False\n"
                "called SDI.enable_delete with arg False\n"
                "called HotkeyPanel.set_title with args {'modified': True}\n"
                "called HotkeyPanel.populate_list with args {}\n")


class TestChoiceBook:
    """unittests for main.ChoiceBook
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.ChoiceBook object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called ChoiceBook.__init__ with args', args)
        monkeypatch.setattr(testee.ChoiceBook, '__init__', mock_init)
        testobj = testee.ChoiceBook()
        testobj.parent = MockEditor()
        testobj.gui = MockTabGui()
        assert capsys.readouterr().out == ('called ChoiceBook.__init__ with args ()\n'
                                           "called Editor.__init__\n"
                                           "called TabbedInterface.__init__ with args ()\n")
        return testobj

    def test_init(self, monkeypatch, capsys, tmp_path):
        """unittest for ChoiceBook.__init__
        """
        def mock_log():
            print('called shared.log_exc')
        def mock_callback(self):
            "empty function just for reference"
        def mock_set(self):
            print('called ChoiceBook,setcaptions')
        monkeypatch.setattr(testee.shared, 'log_exc', mock_log)
        plgfile = tmp_path / 'isthere'
        plgfile.touch()
        monkeypatch.setattr(testee.gui, 'TabbedInterface', MockTabGui)
        monkeypatch.setattr(testee, 'HotkeyPanel', MockHotkeyPanel)
        monkeypatch.setattr(testee.ChoiceBook, 'on_page_changed', mock_callback)
        monkeypatch.setattr(testee.ChoiceBook, 'on_text_changed', mock_callback)
        monkeypatch.setattr(testee.ChoiceBook, 'find_next', mock_callback)
        monkeypatch.setattr(testee.ChoiceBook, 'find_prev', mock_callback)
        monkeypatch.setattr(testee.ChoiceBook, 'setcaptions', mock_set)
        parent = MockEditor()
        parent.ini = {'plugins': [('xxx', str(plgfile)), ('yyy', 'itsnotthere')]}
        parent.captions = {'C_FILTER': 'filtertext'}
        # breakpoint()
        testobj = testee.ChoiceBook(parent)
        assert testobj.parent == parent
        assert testobj.page is None
        assert isinstance(testobj.gui, testee.gui.TabbedInterface)
        assert testobj.parent.pluginfiles == {'xxx': '', 'yyy': 'xxx'}
        assert capsys.readouterr().out == (
                "called Editor.__init__\n"
                f"called TabbedInterface.__init__ with args ({testobj.parent.gui}, {testobj})\n"
                # f"called TabbedInterface.setup_selector with arg {testobj.on_page_changed}\n"
                f"called TabbedInterface.setup_selector with arg {testobj.gui.on_pagechange}\n"
                f"called HotkeyPanel.__init__ with args ({testobj}, '{plgfile}')\n"
                "called TabbedInterface.add_subscreen with arg SingleDataInterface\n"
                "called shared.log_exc\n"
                "called TabbedInterface.add_to_selector with args ('selector', 'xxx')\n"
                f"called HotkeyPanel.__init__ with args ({testobj}, '{testee.BASE}/itsnotthere')\n"
                "called TabbedInterface.add_subscreen with arg SingleDataInterface\n"
                "called TabbedInterface.add_to_selector with args ('selector', 'yyy')\n"
                "called TabbedInterface.start_display\n"
                "called TabbedInterface.start_line with arg screen\n"
                "called TabbedInterface.add_margin_to_line with arg line\n"
                "called TabbedInterface.add_text_to_line with args ('line',)\n"
                "called TabbedInterface.add_selector_to_line with args ('line', 'selector')\n"
                "called TabbedInterface.add_separator_to_line with arg line\n"
                "called TabbedInterface.add_text_to_line with args ('line',)\n"
                "called TabbedInterface.add_combobox_to_line with args ('line',) {'minwidth': 5}\n"
                "called TabbedInterface.add_text_to_line with args ('line', ':')\n"
                "called TabbedInterface.add_combobox_to_line with args ('line',)"
                # f" {{'minwidth': 20, 'editable': True, 'callback': {testobj.on_text_changed}}}\n"
                f" {{'minwidth': 20, 'editable': True, 'callback': {testobj.gui.on_textchange}}}\n"
                "called TabbedInterface.add_button_to_line with args"
                f" ('line', 'filtertext', {testobj.filter}, False)\n"
                "called TabbedInterface.add_button_to_line with args"
                f" ('line', '', {testobj.find_next}, False)\n"
                "called TabbedInterface.add_button_to_line with args"
                f" ('line', '', {testobj.find_prev}, False)\n"
                "called TabbedInterface.add_margin_to_line with arg line\n"
                "called TabbedInterface.start_line with arg screen\n"
                "called TabbedInterface.add_list_to_line with arg line\n"
                "called TabbedInterface.finalize_display with arg screen\n"
                "called ChoiceBook,setcaptions\n")

    def test_setcaptions(self, monkeypatch, capsys):
        """unittest for ChoiceBook.setcaptions
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.captions = {'C_NEXT': 'next', 'C_PREV': 'prev', 'C_SELPRG': 'select',
                                   'C_FIND': 'find', 'C_FLTOFF': 'off', 'C_FILTER': 'on',
                                   'C_EXIT': 'exit'}
        testobj.b_next = 'bnext'
        testobj.b_prev = 'bprev'
        testobj.sel_text = 'sel_text'
        testobj.find_text = 'find_text'
        testobj.b_filter = 'bfilter'
        testobj.filter_on = False
        testobj.setcaptions()
        assert capsys.readouterr().out == (
                "called TabbedInterface.setcaption with args ('bnext', 'next')\n"
                "called TabbedInterface.setcaption with args ('bprev', 'prev')\n"
                "called TabbedInterface.setcaption with args ('sel_text', 'select')\n"
                "called TabbedInterface.setcaption with args ('find_text', 'find')\n"
                "called TabbedInterface.setcaption with args ('bfilter', 'on')\n")
        testobj.parent.b_exit = 'bexit'
        testobj.filter_on = True
        testobj.setcaptions()
        assert capsys.readouterr().out == (
                "called TabbedInterface.setcaption with args ('bnext', 'next')\n"
                "called TabbedInterface.setcaption with args ('bprev', 'prev')\n"
                "called TabbedInterface.setcaption with args ('sel_text', 'select')\n"
                "called TabbedInterface.setcaption with args ('find_text', 'find')\n"
                "called TabbedInterface.setcaption with args ('bfilter', 'off')\n"
                "called TabbedInterface.setcaption with args ('bexit', 'exit')\n")

    def test_on_page_changed(self, monkeypatch, capsys):
        """unittest for ChoiceBook.on_page_changed
        """
        def mock_get():
            print('called TabbedInterface.get_panel')
            return win
        def mock_exit():
            print('called SingleDataInterface.exit')
            return False
        def mock_exit_2():
            print('called SingleDataInterface.exit')
            return True
        def mock_setup():
            print('called EditorGui.setup_menu')
        def mock_update(arg):
            print('called ChoiceBook.update_searchwidgets with arg', arg)
        win = MockSDI()
        assert capsys.readouterr().out == 'called SingleDataInterface.__init__ with args ()\n'
        win.master = MockHotkeyPanel('testobj', '')
        assert capsys.readouterr().out == "called HotkeyPanel.__init__ with args ('testobj', '')\n"
        win.master.modified = True
        win.master.column_info = [('x', 1)]
        win.master.data = {1: 'y'}
        win.exit = mock_exit
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.captions = {'I_DESC': "it's {}", 'x': 'column'}
        testobj.parent.gui.setup_menu = mock_setup
        testobj.sel = 'selector'
        testobj.update_searchwidgets = mock_update

        testobj.parent.book = None
        testobj.on_page_changed(1)
        assert capsys.readouterr().out == ""

        testobj.parent.book = testobj
        testobj.on_page_changed(1)
        assert capsys.readouterr().out == "called TabbedInterface.get_panel\n"

        testobj.gui.get_panel = mock_get
        testobj.on_page_changed(1)
        assert capsys.readouterr().out == ("called TabbedInterface.get_panel\n"
                                           "called SingleDataInterface.exit\n")

        win.master.modified = False
        # testobj.gui.get_panel = mock_get
        testobj.on_page_changed(1)
        assert capsys.readouterr().out == (
                "called TabbedInterface.get_panel\n"
                "called TabbedInterface.get_combobox_value with arg selector\n"
                "called EditorGui.statusbar_message with arg 'it's xxx'\n"
                "called TabbedInterface.set_selected_panel with args (1,)\n"
                "called TabbedInterface.get_panel\n"
                "called EditorGui.setup_menu\n")

        win.master.modified = True
        win.exit = mock_exit_2
        testobj.on_page_changed(1)
        assert capsys.readouterr().out == (
                "called TabbedInterface.get_panel\n"
                "called SingleDataInterface.exit\n"
                "called TabbedInterface.get_combobox_value with arg selector\n"
                "called EditorGui.statusbar_message with arg 'it's xxx'\n"
                "called TabbedInterface.set_selected_panel with args (1,)\n"
                "called TabbedInterface.get_panel\n"
                "called EditorGui.setup_menu\n")

        win.master.settings = {'a': 'b'}
        testobj.on_page_changed(1)
        assert capsys.readouterr().out == (
                "called TabbedInterface.get_panel\n"
                "called SingleDataInterface.exit\n"
                "called TabbedInterface.get_combobox_value with arg selector\n"
                "called EditorGui.statusbar_message with arg 'it's xxx'\n"
                "called TabbedInterface.set_selected_panel with args (1,)\n"
                "called TabbedInterface.get_panel\n"
                "called EditorGui.setup_menu\n"
                "called HotkeyPanel.setcaptions\n"
                "called ChoiceBook.update_searchwidgets with arg ['column']\n")

    def test_on_text_changed(self, monkeypatch, capsys):
        """unittest for ChoiceBook.on_text_changed
        """
        def mock_get(arg):
            print("called TabbedInterface.get_combobox_value with arg", arg)
            return "yyy"
        def mock_find(*args):
            print("called TabbedInterface.find_items with args", args)
            return []
        def mock_find_2(*args):
            print("called TabbedInterface.find_items with args", args)
            return ['item-1', 'item-2']
        monkeypatch.setattr(testee.ChoiceBook, 'init_search_buttons',
                            MockChoiceBook.init_search_buttons)
        monkeypatch.setattr(testee.ChoiceBook, 'enable_search_buttons',
                            MockChoiceBook.enable_search_buttons)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.captions = {"I_#FOUND": "{} found", "I_NOTFND": "no {}"}
        testobj.page = MockHotkeyPanel(testobj, '')
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
        testobj.page.column_info = [('x', 0), ('y', 1)]
        testobj.page.captions = {'x': 'xxx', 'y': 'yyy'}
        testobj.page.data = {1: 'a', 2: 'b'}
        testobj.page.p0list = 'p0list'
        testobj.find_loc = types.SimpleNamespace(name='yyy')
        testobj.gui.get_combobox_value = mock_get
        testobj.gui.find_items = mock_find
        # breakpoint()
        testobj.on_text_changed('qq')
        assert testobj.zoekcol == 1
        assert testobj.items_found == []
        assert not hasattr(testobj, 'founditem')
        assert capsys.readouterr().out == (
                f"called TabbedInterface.get_combobox_value with arg {testobj.find_loc}\n"
                "called TabbedInterface.find_items with args ('p0list', 1, 'qq')\n"
                "called ChoiceBook.init_search_buttons\n"
                "called EditorGui.statusbar_message with arg 'no qq'\n")

        testobj.gui.find_items = mock_find_2
        testobj.on_text_changed('qq')
        assert testobj.zoekcol == 1
        assert testobj.items_found == ['item-1', 'item-2']
        assert testobj.founditem == 0
        assert capsys.readouterr().out == (
                f"called TabbedInterface.get_combobox_value with arg {testobj.find_loc}\n"
                "called TabbedInterface.find_items with args ('p0list', 1, 'qq')\n"
                "called ChoiceBook.init_search_buttons\n"
                "called TabbedInterface.set_selected_keydef_item with args"
                " ('p0list', ['item-1', 'item-2'], 0)\n"
                "called EditorGui.statusbar_message with arg '2 found'\n")

        testobj.page.data = {1: 'a', 2: 'b', 3: 'c'}
        testobj.on_text_changed('qq')
        assert testobj.zoekcol == 1
        assert testobj.items_found == ['item-1', 'item-2']
        assert testobj.founditem == 0
        assert capsys.readouterr().out == (
                f"called TabbedInterface.get_combobox_value with arg {testobj.find_loc}\n"
                "called TabbedInterface.find_items with args ('p0list', 1, 'qq')\n"
                "called ChoiceBook.init_search_buttons\n"
                "called TabbedInterface.set_selected_keydef_item with args"
                " ('p0list', ['item-1', 'item-2'], 0)\n"
                "called ChoiceBook.enable_search_buttons with args {'nxt': True, 'flt': True}\n"
                "called EditorGui.statusbar_message with arg '2 found'\n")

        testobj.page.captions = {'x': 'xxx', 'y': 'zzz'}
        testobj.gui.find_items = mock_find
        testobj.on_text_changed('qq')
        assert testobj.zoekcol == -1
        assert testobj.items_found == []
        assert testobj.founditem == 0
        assert capsys.readouterr().out == (
                f"called TabbedInterface.get_combobox_value with arg {testobj.find_loc}\n"
                "called TabbedInterface.find_items with args ('p0list', -1, 'qq')\n"
                "called ChoiceBook.init_search_buttons\n"
                "called EditorGui.statusbar_message with arg 'no qq'\n")

    def test_find_next(self, monkeypatch, capsys):
        """unittest for ChoiceBook.find_next
        """
        monkeypatch.setattr(testee.ChoiceBook, 'enable_search_buttons',
                            MockChoiceBook.enable_search_buttons)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.page = MockHotkeyPanel(testobj, '')
        testobj.page.p0list = 'p0list'
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
        testobj.parent.captions = {'I_NONXT': 'xxx'}
        testobj.items_found = ['x', 'y']
        testobj.founditem = 1
        testobj.find_next()
        assert testobj.founditem == 1
        assert capsys.readouterr().out == (
                "called ChoiceBook.enable_search_buttons with args {'prv': True}\n"
                "called EditorGui.statusbar_message with arg 'xxx'\n"
                "called ChoiceBook.enable_search_buttons with args {'nxt': False}\n")
        testobj.founditem = 0
        testobj.find_next()
        assert testobj.founditem == 1
        assert capsys.readouterr().out == (
                "called ChoiceBook.enable_search_buttons with args {'prv': True}\n"
                "called TabbedInterface.set_selected_keydef_item with args"
                " ('p0list', ['x', 'y'], 1)\n")

    def test_find_prev(self, monkeypatch, capsys):
        """unittest for ChoiceBook.find_prev
        """
        monkeypatch.setattr(testee.ChoiceBook, 'enable_search_buttons',
                            MockChoiceBook.enable_search_buttons)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.page = MockHotkeyPanel(testobj, '')
        testobj.page.p0list = 'p0list'
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
        testobj.parent.captions = {'I_NOPRV': 'uuu'}
        testobj.items_found = ['x', 'y']
        testobj.founditem = 1
        testobj.find_prev()
        assert testobj.founditem == 0
        assert capsys.readouterr().out == (
                "called ChoiceBook.enable_search_buttons with args {'nxt': True}\n"
                "called TabbedInterface.set_selected_keydef_item with args"
                " ('p0list', ['x', 'y'], 0)\n")
        testobj.founditem = 0
        testobj.find_prev()
        assert testobj.founditem == 0
        assert capsys.readouterr().out == (
                "called ChoiceBook.enable_search_buttons with args {'nxt': True}\n"
                "called EditorGui.statusbar_message with arg 'uuu'\n"
                "called ChoiceBook.enable_search_buttons with args {'prv': False}\n")

    def test_filter(self, monkeypatch, capsys):
        """unittest for ChoiceBook.filter
        """
        def mock_get_text(arg):
            print("called TabbedInterface.get_button_text with arg", arg)
            return 'off'
        def mock_on_text(text):
            print(f"called ChoiceBook.on_text_changed with arg '{text}'")
        monkeypatch.setattr(testee.ChoiceBook, 'enable_search_buttons',
                            MockChoiceBook.enable_search_buttons)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.page = MockHotkeyPanel(testobj, '')
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
        testobj.parent.captions = {'C_FILTER': 'on', 'C_FLTOFF': 'off'}
        testobj.on_text_changed = mock_on_text
        testobj.zoekcol = 1
        testobj.page.data = {1: ['x', 'that'], 2: ['y', 'xxx'], 3: ['z', ''], 4: ['q', 'and xxx']}
        testobj.page.p0list = 'p0list'
        testobj.b_filter = 'b_filter'
        testobj.find = 'find'
        testobj.items_found = []
        testobj.filter()
        assert capsys.readouterr().out == ""
        testobj.items_found = ['x', 'y']
        testobj.filter()
        assert testobj.filter_on
        assert testobj.page.filtertext == 'xxx'
        assert testobj.page.origdata == {1: ['x', 'that'], 2: ['y', 'xxx'], 3: ['z', ''],
                                         4: ['q', 'and xxx']}
        assert testobj.page.data == {'2': ['y', 'xxx'], '4': ['q', 'and xxx']}
        assert capsys.readouterr().out == (
            "called TabbedInterface.get_button_text with arg b_filter\n"
            "called TabbedInterface.get_combobox_value with arg find\n"
            "called TabbedInterface.get_found_keydef_position with args ('p0list',)\n"
            "called ChoiceBook.enable_search_buttons with args {'nxt': False, 'prv': False}\n"
            "called TabbedInterface.enable_widget with args ('find', False)\n"
            "called HotkeyPanel.populate_list with arg p0list\n"
            "called TabbedInterface.set_found_keydef_position with args ('p0list', 2)\n"
            "called TabbedInterface.set_button_text with args ('b_filter', 'off')\n")
        testobj.gui.get_button_text = mock_get_text
        testobj.filter()
        assert not testobj.filter_on
        assert testobj.page.filtertext == ''
        assert testobj.page.origdata == {1: ['x', 'that'], 2: ['y', 'xxx'], 3: ['z', ''],
                                         4: ['q', 'and xxx']}
        assert testobj.page.data == {1: ['x', 'that'], 2: ['y', 'xxx'], 3: ['z', ''],
                                     4: ['q', 'and xxx']}
        assert capsys.readouterr().out == (
            "called TabbedInterface.get_button_text with arg b_filter\n"
            "called TabbedInterface.get_combobox_value with arg find\n"
            "called TabbedInterface.get_found_keydef_position with args ('p0list',)\n"
            "called ChoiceBook.enable_search_buttons with args {'nxt': True, 'prv': True}\n"
            "called TabbedInterface.enable_widget with args ('find', True)\n"
            "called HotkeyPanel.populate_list with arg p0list\n"
            "called TabbedInterface.set_found_keydef_position with args ('p0list', 2)\n"
            "called TabbedInterface.set_button_text with args ('b_filter', 'on')\n"
            "called ChoiceBook.on_text_changed with arg 'xxx'\n")

    def test_set_selected_tool(self, monkeypatch, capsys):
        """unittest for ChoiceBook.set_selected_tool
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = 'selector'
        testobj.set_selected_tool('start')
        assert capsys.readouterr().out == (
                "called TabbedInterface.set_combobox_index with args ('selector', 'start')\n")

    def test_update_searchwidgets(self, monkeypatch, capsys):
        """unittest for ChoiceBook.update_search
        """
        monkeypatch.setattr(testee.ChoiceBook, 'enable_search_buttons',
                            MockChoiceBook.enable_search_buttons)
        monkeypatch.setattr(testee.ChoiceBook, 'init_search_buttons',
                            MockChoiceBook.init_search_buttons)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.parent.captions = {'C_FLTOFF': 'off'}
        testobj.find_loc = 'find_loc'
        testobj.find = 'find'
        testobj.b_filter = 'bfilter'
        testobj.page = types.SimpleNamespace(filtertext='')
        testobj.update_searchwidgets(['items'])
        assert capsys.readouterr().out == (
                "called TabbedInterface.refresh_combobox with args ('find_loc', ['items'])\n"
                "called TabbedInterface.set_combobox_text with args ('find', '')\n"
                "called ChoiceBook.init_search_buttons\n")
        testobj.page.filtertext = 'xxx'
        testobj.update_searchwidgets(['items'])
        assert capsys.readouterr().out == (
                "called TabbedInterface.refresh_combobox with args ('find_loc', ['items'])\n"
                "called TabbedInterface.set_combobox_text with args ('find', 'xxx')\n"
                "called TabbedInterface.setcaption with args ('bfilter', 'off')\n"
                "called ChoiceBook.enable_search_buttons with args {'flt': True}\n")

    def test_init_search_buttons(self, monkeypatch, capsys):
        """unittest for ChoiceBook.init_search_buttons
        """
        monkeypatch.setattr(testee.ChoiceBook, 'enable_search_buttons',
                            MockChoiceBook.enable_search_buttons)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.init_search_buttons()
        assert capsys.readouterr().out == ("called ChoiceBook.enable_search_buttons with args"
                                           " {'nxt': False, 'prv': False, 'flt': False}\n")

    def test_enable_search_buttons(self, monkeypatch, capsys):
        """unittest for ChoiceBook.enable_search_buttons
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.b_next = 'bnext'
        testobj.b_prev = 'bprev'
        testobj.b_filter = 'bfilter'
        testobj.enable_search_buttons(nxt=None, prv=None, flt=None)
        assert capsys.readouterr().out == ""
        testobj.enable_search_buttons(nxt=False, prv=False, flt=False)
        assert capsys.readouterr().out == (
                "called TabbedInterface.enable_widget with args ('bnext', False)\n"
                "called TabbedInterface.enable_widget with args ('bprev', False)\n"
                "called TabbedInterface.enable_widget with args ('bfilter', False)\n")
        testobj.enable_search_buttons(nxt=True, prv=True, flt=True)
        assert capsys.readouterr().out == (
                "called TabbedInterface.enable_widget with args ('bnext', True)\n"
                "called TabbedInterface.enable_widget with args ('bprev', True)\n"
                "called TabbedInterface.enable_widget with args ('bfilter', True)\n")

    def test_add_tool(self, monkeypatch, capsys):
        """unittest for ChoiceBook.add_tool
        """
        def mock_add(win):
            print(f'called TabbedInterface.add_subscreen with arg {win}')
        def mock_add_to(*args):
            print('called TabbedInterface.add_to_selector with args', args)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.sel = 'selector'
        testobj.gui.add_subscreen = mock_add
        testobj.gui.add_to_selector = mock_add_to
        testobj.add_tool('program', 'win')
        assert capsys.readouterr().out == (
                "called TabbedInterface.add_subscreen with arg win\n"
                "called TabbedInterface.add_to_selector with args ('selector', 'program')\n")


class TestEditor:
    """unittests for main.Editor
    """
    def setup_testobj(self, monkeypatch, capsys):
        """stub for main.Editor object

        create the object skipping the normal initialization
        intercept messages during creation
        return the object so that other methods can be monkeypatched in the caller
        """
        def mock_init(self, *args):
            """stub
            """
            print('called Editor.__init__ with args', args)
        monkeypatch.setattr(testee.Editor, '__init__', mock_init)
        testobj = testee.Editor()
        testobj.book = MockChoiceBook(testobj)
        testobj.gui = MockGui(testobj)
        assert capsys.readouterr().out == ('called Editor.__init__ with args ()\n'
                                           f"called ChoiceBook.__init__ with arg '{testobj}'\n"
                                           'called TabbedInterface.__init__ with args ()\n'
                                           f'called Gui.__init__ with arg {testobj}\n')
        return testobj

    def test_init(self, monkeypatch, capsys):
        """unittest for Editor.__init__
        """
        def mock_save_log():
            print('called shared.save_log')
        def mock_read(arg):
            print(f"called read_config with arg '{arg}'")
            return {'lang': 'en', 'title': '', 'initial': '', 'plugins': []}
        def mock_read_2(arg):
            print(f"called read_config with arg '{arg}'")
            return {'lang': 'en', 'title': '', 'initial': 'y', 'plugins': [('x', 'xxx'), ('y', 'yyy')]}
        def mock_read_3(arg):
            print(f"called read_config with arg '{arg}'")
            return {'lang': 'en', 'title': 'qqq', 'initial': 'x', 'plugins': [('x', 'xxx')]}
        def mock_read_4(arg):
            print(f"called read_config with arg '{arg}'")
            return {'lang': 'en', 'title': 'qqq', 'initial': '', 'plugins': [('x', 'xxx')]}
        def mock_readcaptions(self, arg):
            print(f"called Editor.readcaptions with arg '{arg}'")
            self.captions = {'T_MAIN': 'maintitle', 'T_HELLO': 'hello from {}', 'C_EXIT': 'exit'}
        # def mock_show(self):
        #     print('called Editor.show_empty_screen')
        def mock_set(self):
            print('called Editor.setcaptions')
        monkeypatch.setattr(testee.shared, 'save_log', mock_save_log)
        monkeypatch.setattr(testee, 'read_config', mock_read)
        # monkeypatch.setattr(testee.Editor, 'show_empty_screen', mock_show)
        monkeypatch.setattr(testee.Editor, 'readcaptions', mock_readcaptions)
        monkeypatch.setattr(testee.gui, 'Gui', MockGui)
        monkeypatch.setattr(testee, 'ChoiceBook', MockChoiceBook)
        monkeypatch.setattr(testee.Editor, 'setcaptions', mock_set)

        monkeypatch.setattr(testee, 'CONF', testee.pathlib.Path('mock_conf'))
        monkeypatch.setattr(testee, 'BASE', testee.pathlib.Path('/confbase'))
        args = types.SimpleNamespace(conf='', start='')
        testobj = testee.Editor(args)
        assert testobj.ini == {'lang': 'english.lng', 'plugins': [], 'filename': testee.CONF,
                               'startup': 'Remember', 'initial': ''}
        assert testobj.pluginfiles == {}
        assert isinstance(testobj.book, testee.ChoiceBook)
        assert testobj.book.page.settings == {'PluginName': '', 'PanelName': '', 'RebuildData': False,
                                              'ShowDetails': False, 'RedefineKeys': False}
        assert testobj.book.page.data == {}
        assert testobj.book.page.exit()
        assert isinstance(testobj.gui, testee.gui.Gui)
        assert not testobj.forgetatexit
        assert capsys.readouterr().out == (
                "called shared.save_log\n"
                "called Editor.readcaptions with arg 'english.lng'\n"
                f"called Gui.__init__ with arg {testobj}\n"
                "called Gui.set_window_title with arg 'maintitle'\n"
                "called Gui.statusbar_message with args ('hello from maintitle',)\n"
                f"called ChoiceBook.__init__ with arg '{testobj}'\n"
                "called TabbedInterface.__init__ with args ()\n"
                "called Gui.setup_menu with args {'minimal': True}\n"
                "called Gui.start_display\n"
                f"called Gui.add_choicebook_to_display with args ('box', {testobj.book.gui})\n"
                f"called Gui.add_exitbutton_to_display with args ('box', ('exit', {testobj.exit}))\n"
                "called Gui.go with arg box\n")
        monkeypatch.setattr(testee.pathlib.Path, 'exists', lambda *x: True)
        monkeypatch.setattr(testee, 'read_config', mock_read_2)
        args = types.SimpleNamespace(conf='other_conf', start='y')
        testobj = testee.Editor(args)
        assert testobj.ini == {'initial': 'y', 'lang': 'en', 'title': '', 'plugins': [('x', 'xxx'),
                                                                                      ('y', 'yyy')]}
        assert testobj.pluginfiles == {}
        assert isinstance(testobj.gui, testee.gui.Gui)
        assert isinstance(testobj.book, testee.ChoiceBook)
        assert testobj.forgetatexit
        assert capsys.readouterr().out == (
                "called shared.save_log\n"
                "called read_config with arg '/confbase/other_conf'\n"
                "called Editor.readcaptions with arg 'en'\n"
                f"called Gui.__init__ with arg {testobj}\n"
                "called Gui.set_window_title with arg 'maintitle'\n"
                "called Gui.statusbar_message with args ('hello from maintitle',)\n"
                f"called ChoiceBook.__init__ with arg '{testobj}'\n"
                "called TabbedInterface.__init__ with args ()\n"
                "called ChoiceBook.set_selected_tool with arg 1\n"
                "called ChoiceBook.on_page_changed with arg '1'\n"
                "called Editor.setcaptions\n"
                "called Gui.start_display\n"
                f"called Gui.add_choicebook_to_display with args ('box', {testobj.book.gui})\n"
                f"called Gui.add_exitbutton_to_display with args ('box', ('exit', {testobj.exit}))\n"
                "called Gui.go with arg box\n")
        args = types.SimpleNamespace(conf='other_conf', start='z')
        with pytest.raises(ValueError) as e:
            testobj = testee.Editor(args)
        assert str(e.value) == "Can't start with z: possible values are ['x', 'y']"
        assert capsys.readouterr().out == (
                "called shared.save_log\n"
                "called read_config with arg '/confbase/other_conf'\n")

        monkeypatch.setattr(testee, 'read_config', mock_read_3)
        args = types.SimpleNamespace(conf='/yet/another/conf', start='')
        testobj = testee.Editor(args)
        assert testobj.ini == {'initial': 'x', 'lang': 'en', 'title': 'qqq', 'plugins': [('x', 'xxx')]}
        assert testobj.pluginfiles == {}
        assert isinstance(testobj.gui, testee.gui.Gui)
        assert isinstance(testobj.book, testee.ChoiceBook)
        assert capsys.readouterr().out == (
                "called shared.save_log\n"
                "called read_config with arg '/yet/another/conf'\n"
                "called Editor.readcaptions with arg 'en'\n"
                f"called Gui.__init__ with arg {testobj}\n"
                "called Gui.set_window_title with arg 'maintitle'\n"
                "called Gui.statusbar_message with args ('hello from maintitle',)\n"
                f"called ChoiceBook.__init__ with arg '{testobj}'\n"
                "called TabbedInterface.__init__ with args ()\n"
                "called ChoiceBook.set_selected_tool with arg 0\n"
                "called ChoiceBook.on_page_changed with arg '0'\n"
                "called Editor.setcaptions\n"
                "called Gui.start_display\n"
                f"called Gui.add_choicebook_to_display with args ('box', {testobj.book.gui})\n"
                f"called Gui.add_exitbutton_to_display with args ('box', ('exit', {testobj.exit}))\n"
                "called Gui.go with arg box\n")
        testobj.ini['initial'] = ''
        monkeypatch.setattr(testee, 'read_config', mock_read_4)
        testobj = testee.Editor(args)
        assert testobj.ini == {'initial': '', 'lang': 'en', 'title': 'qqq', 'plugins': [('x', 'xxx')]}
        assert testobj.pluginfiles == {}
        assert isinstance(testobj.gui, testee.gui.Gui)
        assert isinstance(testobj.book, testee.ChoiceBook)
        assert capsys.readouterr().out == (
                "called shared.save_log\n"
                "called read_config with arg '/yet/another/conf'\n"
                "called Editor.readcaptions with arg 'en'\n"
                f"called Gui.__init__ with arg {testobj}\n"
                "called Gui.set_window_title with arg 'maintitle'\n"
                "called Gui.statusbar_message with args ('hello from maintitle',)\n"
                f"called ChoiceBook.__init__ with arg '{testobj}'\n"
                "called TabbedInterface.__init__ with args ()\n"
                "called Editor.setcaptions\n"
                "called Gui.start_display\n"
                f"called Gui.add_choicebook_to_display with args ('box', {testobj.book.gui})\n"
                f"called Gui.add_exitbutton_to_display with args ('box', ('exit', {testobj.exit}))\n"
                "called Gui.go with arg box\n")

    def test_determine_startapp_index(self, monkeypatch, capsys):
        """unittest for Editor.determine_startapp_index
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ini = {}
        assert testobj.determine_startapp_index('y', []) == -1
        assert capsys.readouterr().out == ""
        testobj.ini['initial'] = 'x'
        assert testobj.determine_startapp_index('y', ['x', 'z']) == 0
        assert capsys.readouterr().out == ""
        assert testobj.determine_startapp_index('y', ['x', 'y', 'z']) == 1
        assert capsys.readouterr().out == ""

    def test_get_menudata(self, monkeypatch, capsys):
        """unittest for Editor.get_menudata
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        menus = testobj.get_menudata()
        assert [x[0] for x in menus] == ['M_APP', 'M_TOOL', 'M_HELP']
        submenus = [x[1] for x in menus]
        assert [x[0] for x in submenus[0]] == ['M_SETT', 'M_EXIT']
        assert [x[0] for x in submenus[1]] == ['M_SETT2', 'M_ENTR', 'M_DESC', 'M_READ', 'M_RBLD',
                                               'M_SAVE']
        assert [x[0] for x in submenus[2]] == ['M_ABOUT']

    def test_m_read(self, monkeypatch, capsys):
        """unittest for Editor.m_read
        """
        def mock_show(*args):
            print('called gui.show_message with args', args)
        def mock_ask(*args):
            print('called gui.ask_question with args', args)
            return False
        def mock_ask_2(*args):
            print('called gui.ask_question with args', args)
            return True
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.page = MockHotkeyPanel(testobj.book, '')
        testobj.book.page.p0list = 'p0list'
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
        testobj.book.page.settings = []
        testobj.m_read()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_ADDSET')\n")
        testobj.book.page.settings = ['x']
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
        testobj.book.page.modified = False
        testobj.m_read()
        assert capsys.readouterr().out == (
                f"called gui.ask_question with args ({testobj.gui}, 'Q_NOCHG')\n")
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
        testobj.m_read()
        assert capsys.readouterr().out == (
                f"called gui.ask_question with args ({testobj.gui}, 'Q_NOCHG')\n"
                "called HotkeyPanel.readkeys\n"
                "called HotkeyPanel.populate_list with arg p0list\n")
        testobj.book.page.modified = True
        testobj.m_read()
        assert capsys.readouterr().out == ("called HotkeyPanel.readkeys\n"
                                           "called HotkeyPanel.populate_list with arg p0list\n")
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
        testobj.m_read()
        assert capsys.readouterr().out == ("called HotkeyPanel.readkeys\n"
                                           "called HotkeyPanel.populate_list with arg p0list\n")

    def test_m_save(self, monkeypatch, capsys):
        """unittest for Editor.m_save
        """
        def mock_ask(*args):
            print('called gui.ask_question with args', args)
            return False
        def mock_ask_2(*args):
            print('called gui.ask_question with args', args)
            return True
        def mock_show(*args):
            print('called gui.show_message with args', args)
        def mock_log():
            print('called shared.log_exc')
        def mock_savekeys():
            print('called HotkeyPanel.savekeys')
            return True
        monkeypatch.setattr(testee.shared, 'log_exc', mock_log)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.page = MockHotkeyPanel(testobj.book, '')
        testobj.book.page.reader = types.SimpleNamespace()
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
        testobj.book.page.modified = False
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
        testobj.m_save(event=None)
        assert capsys.readouterr().out == (
                f"called gui.ask_question with args ({testobj.gui}, 'Q_NOCHG')\n")
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
        testobj.m_save(event=None)
        assert capsys.readouterr().out == (
                f"called gui.ask_question with args ({testobj.gui}, 'Q_NOCHG')\n"
                "called HotkeyPanel.savekeys\n"
                f"called gui.show_message with args ({testobj.gui}, 'I_DEFSAV')\n")
        testobj.book.page.modified = True
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
        testobj.m_save(event=None)
        assert capsys.readouterr().out == (
                "called HotkeyPanel.savekeys\n"
                f"called gui.show_message with args ({testobj.gui}, 'I_DEFSAV')\n")
        monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
        testobj.m_save(event=None)
        assert capsys.readouterr().out == (
                "called HotkeyPanel.savekeys\n"
                f"called gui.show_message with args ({testobj.gui}, 'I_DEFSAV')\n")
        testobj.book.page.savekeys = mock_savekeys
        testobj.m_save(event=None)
        assert capsys.readouterr().out == (
                "called HotkeyPanel.savekeys\n"
                f"called gui.show_message with args ({testobj.gui}, 'I_RSTRT')\n")

    def test_m_loc(self, monkeypatch, capsys):
        """unittest for Editor.m_loc
        """
        def mock_show(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called gui.show_dialog with args', args)
            args[0].last_added = None
            args[0].ini['plugins'] = [('x', 'y')]
            return True
        def mock_show_3(*args):
            print('called gui.show_dialog with args', args)
            args[0].last_added = 'last added'
            args[0].ini['plugins'] = [('x', 'y'), ('a', 'b')]
            return True
        def mock_write(name):
            print(f"called Editor.write_config with arg '{name}'")
        def mock_clear(arg):
            print('called Editor.clear_book with arg {arg}')
            return []
        def mock_rebuild(*args):
            print('called Editor.rebuild_book with args', args)
            return []
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        monkeypatch.setattr(testee, 'write_config', mock_write)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.clear_book = mock_clear
        testobj.rebuild_book = mock_rebuild
        testobj.ini = {'plugins': [('p', 'q'), ('r', 's')]}
        testobj.book.sel = 'selector'
        testobj.m_loc()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.FilesDialog})\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        testobj.m_loc()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.FilesDialog})\n"
                "called TabbedInterface.get_combobox_index with arg selector\n"
                "called Editor.write_config with arg '{'plugins': [('x', 'y')]}'\n"
                "called Editor.clear_book with arg {arg}\n"
                "called Editor.rebuild_book with args (['p', 'r'], ['q', 's'], [])\n"
                "called TabbedInterface.set_combobox_index with args ('selector', 1)\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_3)
        testobj.ini = {'plugins': [('p', 'q'), ('r', 's')]}
        testobj.m_loc()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.FilesDialog})\n"
                "called TabbedInterface.get_combobox_index with arg selector\n"
                "called Editor.write_config with arg '{'plugins': [('x', 'y'), ('a', 'b')]}'\n"
                "called Editor.clear_book with arg {arg}\n"
                "called Editor.rebuild_book with args (['p', 'r'], ['q', 's'], [])\n"
                "called TabbedInterface.get_combobox_index_for_item with args"
                " ('selector', 'last added')\n"
                "called TabbedInterface.set_combobox_index with args ('selector', 1)\n")

    def test_clear_book(self, monkeypatch, capsys):
        """unittest for Editor.clear_book
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ini = {'plugins': [('p', 'q'), ('r', 's')]}
        testobj.pluginfiles = {'a': 'aaa', 'b': 'bbb', 'c': 'ccc'}
        testobj.book.sel = 'selector'
        assert testobj.clear_book(['xxx', 'b', 'zzz']) == {'zzz': 'item #1', 'xxx': 'item #3'}
        assert testobj.pluginfiles == {'a': 'aaa', 'c': 'ccc'}
        assert capsys.readouterr().out == (
                "called TabbedInterface.refresh_combobox with args ('selector',)\n"
                "called TabbedInterface.remove_tool with args (2, 'zzz', ['p', 'r'])\n"
                "called TabbedInterface.remove_tool with args (1, 'b', ['p', 'r'])\n"
                "called TabbedInterface.remove_tool with args (0, 'xxx', ['p', 'r'])\n")

    def test_rebuild_book(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.rebuild_book
        """
        monkeypatch.setattr(testee, 'HotkeyPanel', MockHotkeyPanel)
        testobj = self.setup_testobj(monkeypatch, capsys)
        current_programs = ['p']
        current_paths = ['q']
        items_to_retain = {'p': 'q'}
        testobj.ini = {'plugins': [('p', 'q'), ('r', 's')]}
        testobj.rebuild_book(current_programs, current_paths, items_to_retain)
        assert capsys.readouterr().out == (
                "called TabbedInterface.add_tool with args ('p', 'q')\n"
                f"called HotkeyPanel.__init__ with args ({testobj.book}, '{testee.BASE}/s')\n"
                f"called TabbedInterface.add_tool with args ('r', <HotkeyPanel '{testee.BASE}/s'>)\n")
        (tmp_path / 's').touch()
        testobj.ini = {'plugins': [('p', 'qq'), ('r', f'{tmp_path}/s')]}
        testobj.rebuild_book(current_programs, current_paths, items_to_retain)
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, 'qq')\n"
                "called TabbedInterface.add_tool with args ('p', <HotkeyPanel 'qq'>)\n"
                f"called HotkeyPanel.__init__ with args ({testobj.book}, '{tmp_path}/s')\n"
                f"called TabbedInterface.add_tool with args ('r', <HotkeyPanel '{tmp_path}/s'>)\n")

    def test_accept_pathsettings(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.accept_pathsettings
        """
        def mock_write(data):
            print(f"called write_config with arg '{data}'")
        def mock_update(*args):
            print('called update_paths with args', args)
            return []
        def mock_check(*args):
            print('called Editor.check_plugin_settings with args', args)
            return False
        def mock_check_2(*args):
            print('called Editor.check_plugin_settings with args', args)
            return True
        monkeypatch.setattr(testee, 'write_config', mock_write)
        monkeypatch.setattr(testee, 'update_paths', mock_update)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.check_plugin_settings = mock_check

        testobj.last_added = 'xx'
        testobj.ini = {'lang': 'en'}
        testobj.accept_pathsettings([], {}, [])
        assert testobj.last_added == ''
        assert testobj.ini['plugins'] == []
        assert testobj.last_added == ''
        assert capsys.readouterr().out == "called update_paths with args ([], {})\n"

        testobj.last_added = 'xx'
        testobj.ini['startup'] = testee.shared.mode_f
        testobj.ini['initial'] = 'yy'
        testobj.ini['plugins'] = [('zz', 'path/to/zz')]
        testobj.pluginfiles = {}
        name_path_list = [('xx', 'path/to/xx')]
        settingsdata = {'xx': ('path/to/xx',), 'zz': ('path/to/zz',)}
        assert not testobj.accept_pathsettings(name_path_list, settingsdata, [])
        assert testobj.ini["startup"] == testee.shared.mode_r
        assert testobj.pluginfiles == {}
        assert testobj.last_added == 'xx'
        assert capsys.readouterr().out == (
                "called write_config with arg '{'lang': 'en', 'plugins': [('zz', 'path/to/zz')],"
                " 'startup': 'Remember', 'initial': 'yy'}'\n"
                "called Editor.check_plugin_settings with args ('xx', 'path/to/xx', ('path/to/xx',))\n")

        name_path_list = [('zz', 'path/to/zz')]
        assert testobj.accept_pathsettings(name_path_list, settingsdata, [])
        assert testobj.pluginfiles == {}
        assert capsys.readouterr().out == (
                "called update_paths with args ([('zz', 'path/to/zz')], {})\n")

        testobj.check_plugin_settings = mock_check_2
        file_to_remove = tmp_path / 'obsolete'
        file_to_remove.touch()
        name_path_list = [('xx', 'path/to/xx')]
        assert testobj.accept_pathsettings(name_path_list, settingsdata, [str(file_to_remove)])
        assert testobj.pluginfiles == {'xx': 'path/to/xx'}
        assert testobj.ini['plugins'] == []
        assert capsys.readouterr().out == (
                "called Editor.check_plugin_settings with args ('xx', 'path/to/xx', ('path/to/xx',))\n"
                "called update_paths with args ([('xx', 'path/to/xx')], {})\n")

    def test_check_plugin_settings(self, monkeypatch, capsys):
        """unittest for Editor.check_plugin_settings
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_readjson(filename):
            print(f"called readjson with arg '{filename}'")
            raise IsADirectoryError
        def mock_readjson_2(filename):
            print(f"called readjson with arg '{filename}'")
            raise ValueError
        def mock_readjson_3(filename):
            print(f"called readjson with arg '{filename}'")
            return ({},)
        def mock_readjson_4(filename):
            print(f"called readjson with arg '{filename}'")
            return ({testee.shared.SettType.PLG.value: 'prog'},)
        def mock_import_nok(*args):
            """stub
            """
            print('called importlib.import_module with args', args)
            raise ImportError
        def mock_import_ok(*args):
            """stub
            """
            print('called importlib.import_module with args', args)
            return MockReader()
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        monkeypatch.setattr(testee, 'readjson', mock_readjson)
        monkeypatch.setattr(testee.importlib, 'import_module', mock_import_nok)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.captions = {'I_FILLALL': 'fillall error', 'I_NOKDEF': 'nokeydef error: {}',
                            'I_NOPLNAM': 'noplnam error: {}', 'I_NOPLREF': 'noplref error: {}'}
        assert not testobj.check_plugin_settings('pluginname', '', [])
        assert capsys.readouterr().out == (
               f"called gui.show_message with args ({testobj.gui},) {{'text': 'fillall error'}}\n")
        assert testobj.check_plugin_settings('pluginname', 'datafilename', ('xxx', ''))
        assert capsys.readouterr().out == ''
        # assert not testobj.check_plugin_settings('pluginname', 'datafilename.csv', ('',))
        # assert capsys.readouterr().out == (
        #         "called readjson with arg 'datafilename.csv'\n"
        #         f"called gui.show_message with args ({testobj.gui},)"
        #         " {'text': 'nokeydef error: datafilename.csv'}\n")
        monkeypatch.setattr(testee, 'readjson', mock_readjson_2)
        assert not testobj.check_plugin_settings('pluginname', 'datafilename.json', ('',))
        assert capsys.readouterr().out == (
                "called readjson with arg 'datafilename.json'\n"
                f"called gui.show_message with args ({testobj.gui},)"
                " {'text': 'nokeydef error: datafilename.json'}\n")
        monkeypatch.setattr(testee, 'readjson', mock_readjson_3)
        assert not testobj.check_plugin_settings('pluginname', 'datafilename.json', ('',))
        assert capsys.readouterr().out == (
                "called readjson with arg 'datafilename.json'\n"
                f"called gui.show_message with args ({testobj.gui},)"
                " {'text': 'noplnam error: datafilename.json'}\n")
        monkeypatch.setattr(testee, 'readjson', mock_readjson_4)
        assert not testobj.check_plugin_settings('pluginname', 'datafilename.json', ('',))
        assert capsys.readouterr().out == (
                "called readjson with arg 'datafilename.json'\n"
                "called importlib.import_module with args ('prog',)\n"
                f"called gui.show_message with args ({testobj.gui},)"
                " {'text': 'noplref error: datafilename.json'}\n")
        monkeypatch.setattr(testee, 'readjson', mock_readjson_3)
        monkeypatch.setattr(testee.importlib, 'import_module', mock_import_nok)
        assert not testobj.check_plugin_settings('pluginname', 'datafilename.json', ('prgname',))
        assert capsys.readouterr().out == (
                "called importlib.import_module with args ('prgname',)\n"
                f"called gui.show_message with args ({testobj.gui},)"
                " {'text': 'noplref error: datafilename.json'}\n")
        monkeypatch.setattr(testee.importlib, 'import_module', mock_import_ok)
        assert testobj.check_plugin_settings('pluginname', 'datafilename.json', ('prgname',))
        assert capsys.readouterr().out == "called importlib.import_module with args ('prgname',)\n"

    def test_m_rebuild(self, monkeypatch, capsys):
        """unittest for Editor.m_rebuild
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_writejson(*args):
            print("called writejson with args", args)
        def mock_build(arg):
            print(f"called Plugin.build_data with arg '{arg}'")
            raise FileNotFoundError
        def mock_build_2(arg):
            print(f"called Plugin.build_data with arg '{arg}'")
            return None
        def mock_build_3(arg):
            print(f"called Plugin.build_data with arg '{arg}'")
            return {}, {'other': 'stuff'}
        def mock_build_4(arg):
            print(f"called Plugin.build_data with arg '{arg}'")
            return ({},)
        def mock_build_5(arg):
            print(f"called Plugin.build_data with arg '{arg}'")
            return {'key': 'def'}, {'other': 'stuff'}
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        monkeypatch.setattr(testee, 'writejson', mock_writejson)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.page = MockHotkeyPanel(testobj.book, '')
        assert capsys.readouterr().out == f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n"
        testobj.book.page.reader = MockReader()
        testobj.book.page.column_info = {'column': 'info'}
        testobj.book.page.p0list = 'p0list'
        testobj.ini = {'lang': 'en'}
        testobj.captions = {'I_RBLD': 'RBLD', 'I_NODEFS': 'NODEFS', 'I_NOEXTRA': 'NOEXTRA',
                            'I_NORBLD': 'NORBLD {}', 'I_ERRRBLD': 'ERRRBLD', 'I_#FOUND': '#FOUND {}'}
        # testobj.p0list = 'p0list'
        testobj.book.page.settings = {}
        testobj.m_rebuild()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_ADDSET') {{}}\n")
        testobj.book.page.settings = {'plugin': 'settings'}
        testobj.m_rebuild()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_DEFRBLD') {{}}\n")
        testobj.book.page.descriptions = {'old': 'descs'}
        testobj.book.page.reader.build_data = mock_build
        testobj.m_rebuild()
        assert capsys.readouterr().out == (
                "called Plugin.build_data with arg '<HotkeyPanel ''>'\n"
                f"called gui.show_message with args ({testobj.gui},) {{'text': 'ERRRBLD\\n()'}}\n")
        testobj.book.page.reader.build_data = mock_build_2
        testobj.m_rebuild()
        assert capsys.readouterr().out == (
                "called Plugin.build_data with arg '<HotkeyPanel ''>'\n")
        testobj.book.page.reader.build_data = mock_build_3
        testobj.m_rebuild()
        assert capsys.readouterr().out == (
                "called Plugin.build_data with arg '<HotkeyPanel ''>'\n"
                f"called gui.show_message with args ({testobj.gui},)"
                " {'text': 'NORBLD #FOUND NODEFS'}\n")
        testobj.book.page.reader.build_data = mock_build_4
        testobj.m_rebuild()
        assert capsys.readouterr().out == (
                "called Plugin.build_data with arg '<HotkeyPanel ''>'\n"
                f"called gui.show_message with args ({testobj.gui},)"
                " {'text': 'NORBLD #FOUND NOEXTRA'}\n")
        testobj.book.page.reader.build_data = mock_build_5
        testobj.book.page.pad = 'testfile.json'
        testobj.m_rebuild()
        assert capsys.readouterr().out == (
                "called Plugin.build_data with arg '<HotkeyPanel ''>'\n"
                f"called writejson with args ('testfile.json', {testobj.book.page.reader},"
                " {'plugin': 'settings'}, {'column': 'info'}, {'key': 'def'}, {'other': 'stuff'})\n"
                "called HotkeyPanel.populate_list with arg p0list\n"
                f"called gui.show_message with args ({testobj.gui},) {{'text': 'RBLD'}}\n")

    def test_accept_pluginsettings(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.accept_pluginsettings
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_find(arg):
            print(f"called importlib.util.find_spec with arg '{arg}'")
            return arg
        def mock_find_2(arg):
            print(f"called importlib.util.find_spec with arg '{arg}'")
            return ''
        clocpath = tmp_path / 'cloc'
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        monkeypatch.setattr(testee.importlib.util, 'find_spec', mock_find)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert not testobj.accept_pluginsettings('', 'ploc', 'title', '0', '1', '0')
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_NEEDNAME') {{}}\n")
        clocpath.touch()
        assert not testobj.accept_pluginsettings(str(clocpath), 'ploc', 'title', '0', '1', '0')
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_GOTSETFIL')"
                f" {{'args': ['{clocpath}']}}\n")
        clocpath.unlink()
        assert not testobj.accept_pluginsettings(str(clocpath), 'ploc', 'title', '0', '1', '0')
        assert capsys.readouterr().out == (
                "called importlib.util.find_spec with arg 'ploc'\n"
                f"called gui.show_message with args ({testobj.gui}, 'I_GOTPLGFIL')"
                f" {{'args': ['ploc']}}\n")
        monkeypatch.setattr(testee.importlib.util, 'find_spec', mock_find_2)
        assert testobj.accept_pluginsettings(str(clocpath), 'ploc', 'title', '0', '1', '0')
        assert testobj.gui.data == [f'{clocpath}', 'ploc', 'title', 0, 1, 0]
        assert capsys.readouterr().out == "called importlib.util.find_spec with arg 'ploc'\n"

        assert testobj.accept_pluginsettings('clocpath', 'ploc', 'title', '0', '1', '0')
        path = testee.os.path.expanduser("~/projects/hotkeys/projects/hotkeys/clocpath")
        assert testobj.gui.data == [path, 'ploc', 'title', 0, 1, 0]
        assert capsys.readouterr().out == "called importlib.util.find_spec with arg 'ploc'\n"
        assert testobj.accept_pluginsettings('./clocpath', 'ploc', 'title', '0', '1', '0')
        path = testee.os.path.expanduser("~/projects/hotkeys/clocpath")
        assert testobj.gui.data == [path, 'ploc', 'title', 0, 1, 0]
        assert capsys.readouterr().out == "called importlib.util.find_spec with arg 'ploc'\n"
        assert testobj.accept_pluginsettings('~/clocpath', 'ploc', 'title', '0', '1', '0')
        path = testee.os.path.expanduser("~/clocpath")
        assert testobj.gui.data == [path, 'ploc', 'title', 0, 1, 0]
        assert capsys.readouterr().out == "called importlib.util.find_spec with arg 'ploc'\n"

    def test_m_tool(self, monkeypatch, capsys):
        """unittest for Editor.m_tool
        """
        def mock_show(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called gui.show_dialog with args', args)
            win = args[0]
            win.book.page.pad = 'path/to/data.json'
            win.book.page.settings = {testee.shared.SettType.RDEF.value: True,  # 1,
                                      testee.shared.SettType.DETS.value: True,  # 1,
                                      testee.shared.SettType.RBLD.value: True}  # 1}
            win.book.page.column_info = ['x']
            win.book.page.data = {1: ['y', 'z']}
            win.book.page.otherstuff = {'a': {'b': 'c'}}
            return True
        def mock_writejson(*args):
            print('called writejson with args', args)
        def mock_modify(*args):
            print('called SingleDataInterface.modify_menu_item with args', args)
        def mock_get_panel(*args):
            print("called TabbedInterface.get_selected_panel with args", args)
            return 'oldwin'
        def mock_replace(*args):
            print("called TabbedInterface.replace_panel with args", args)
        def mock_set_editable(value):
            print(f"called TabbedInterface.set_panel_editable with arg {value}")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        monkeypatch.setattr(testee, 'HotkeyPanel', MockHotkeyPanel)
        monkeypatch.setattr(testee, 'writejson', mock_writejson)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ini = {'plugins': [('a', 'aaa'), ('b', 'bbb'), ('c', 'ccc')]}
        testobj.book.page = MockHotkeyPanel(testobj.book, '')
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
        testobj.book.page.settings = {testee.shared.SettType.RDEF.value: 0}
        testobj.book.page.has_extrapanel = False
        testobj.book.sel = 'selector'
        testobj.gui.modify_menuitem = mock_modify
        testobj.book.gui.get_selected_panel = mock_get_panel
        testobj.book.gui.replace_panel = mock_replace
        testobj.book.gui.set_panel_editable = mock_set_editable
        testobj.m_tool()
        assert not testobj.book.page.has_extrapanel
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.ExtraSettingsDialog})\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        testobj.book.page.settings = {}
        testobj.book.page.has_extrapanel = False
        testobj.book.page.reader = MockReader()
        testobj.m_tool()
        assert testobj.book.page.has_extrapanel
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.ExtraSettingsDialog})\n"
                f"called writejson with args ('path/to/data.json', {testobj.book.page.reader},"
                " {'RedefineKeys': True, 'ShowDetails': True, 'RebuildData': True},"
                " ['x'], {1: ['y', 'z']}, {'a': {'b': 'c'}})\n"
                "called SingleDataInterface.modify_menu_item with args ('M_SAVE', True)\n"
                "called SingleDataInterface.modify_menu_item with args ('M_RBLD', True)\n"
                "called TabbedInterface.get_combobox_index with arg selector\n"
                "called TabbedInterface.get_selected_panel with args (2,)\n"
                f"called HotkeyPanel.__init__ with args ({testobj.book}, 'ccc')\n"
                "called TabbedInterface.replace_panel with args"
                " (2, 'oldwin', 'SingleDataInterface')\n")
        # testobj.book.page.settings = {testee.shared.SettType.RDEF.value: 1}
        testobj.book.page.settings = {}
        testobj.book.page.has_extrapanel = True
        testobj.m_tool()
        assert testobj.book.page.has_extrapanel
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.ExtraSettingsDialog})\n"
                f"called writejson with args ('path/to/data.json', {testobj.book.page.reader},"
                " {'RedefineKeys': True, 'ShowDetails': True, 'RebuildData': True},"
                " ['x'], {1: ['y', 'z']}, {'a': {'b': 'c'}})\n"
                "called SingleDataInterface.modify_menu_item with args ('M_SAVE', True)\n"
                "called SingleDataInterface.modify_menu_item with args ('M_RBLD', True)\n"
                "called TabbedInterface.get_combobox_index with arg selector\n"
                "called TabbedInterface.get_selected_panel with args (2,)\n"
                "called TabbedInterface.set_panel_editable with arg True\n")
        testobj.book.page.settings = {testee.shared.SettType.RDEF.value: 1}
        testobj.m_tool()
        assert testobj.book.page.has_extrapanel
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.ExtraSettingsDialog})\n"
                f"called writejson with args ('path/to/data.json', {testobj.book.page.reader},"
                " {'RedefineKeys': True, 'ShowDetails': True, 'RebuildData': True},"
                " ['x'], {1: ['y', 'z']}, {'a': {'b': 'c'}})\n"
                "called SingleDataInterface.modify_menu_item with args ('M_SAVE', True)\n"
                "called SingleDataInterface.modify_menu_item with args ('M_RBLD', True)\n"
                "called TabbedInterface.get_combobox_index with arg selector\n"
                "called TabbedInterface.get_selected_panel with args (2,)\n")

    def test_accept_extrasettings(self, monkeypatch, capsys):
        """unittest for Editor.accept_extrasettings
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_add():
            pass
        def mock_remove():
            print('called Editor.remove_custom_settings')
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.remove_custom_settings = mock_remove
        testobj.book.page = MockHotkeyPanel(testobj.book, '')
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
        testobj.book.page.title = ''
        testobj.book.page.settings = {}
        testobj.book.page.reader = MockReader()
        testobj.accept_extrasettings('program', 'title', None, False, True, [])
        assert not testobj.book.page.settings
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_NODET') {{}}\n")
        testobj.accept_extrasettings('program', 'title', None, True, None, [])
        assert not testobj.book.page.settings
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_IMPLXTRA') {{}}\n")
        testobj.book.page.reader.add_extra_attributes = mock_add
        testobj.accept_extrasettings('program', 'title', True, True, True, [('name', 'value', 'desc')])
        assert testobj.book.page.settings == {'PluginName': 'program',
                                              'PanelName': 'title',
                                              'RebuildData': True,
                                              'ShowDetails': True,
                                              'RedefineKeys': True,
                                              'name': 'value',
                                              'extra': {'name': 'desc'}}
        assert capsys.readouterr().out == ("called HotkeyPanel.set_title\n"
                                           "called Editor.remove_custom_settings\n")
        testobj.book.page.title = 'title'
        testobj.book.page.settings = {}
        testobj.accept_extrasettings('program', 'title', False, False, False, [])
        assert testobj.book.page.settings == {'PluginName': 'program',
                                              'PanelName': 'title',
                                              'RebuildData': False,
                                              'ShowDetails': False,
                                              'RedefineKeys': False,
                                              'extra': {}}
        assert capsys.readouterr().out == ("called Editor.remove_custom_settings\n")

    def test_remove_custom_settings(self, monkeypatch, capsys):
        """unittest for Editor.remove_custom_settings
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.page = MockHotkeyPanel(testobj.book, '')
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
        testobj.book.page.settings = {'xxx': 'aaaaaaa', 'yyy': 'bbbbbbb', 'zzz': 'ccccccc'}
        monkeypatch.setattr(testee.shared, 'settingnames', ['xxx', 'zzz'])
        testobj.remove_custom_settings()
        assert testobj.book.page.settings == {'xxx': 'aaaaaaa', 'zzz': 'ccccccc'}

    def test_m_col(self, monkeypatch, capsys):
        """unittest for Editor.m_col
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_writejson(*args):
            print('called writejson with args', args)
        def mock_show_dialog(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_show_dialog_2(*args):
            print('called gui.show_dialog with args', args)
            return True
        def mock_read(arg):
            print(f"called Editor.read_columntitledata with arg '{arg}'")
            return [], []
        def mock_build():
            print("called Editor.build_new_pagedata")
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog)
        monkeypatch.setattr(testee, 'read_columntitledata', mock_read)
        monkeypatch.setattr(testee, 'HotkeyPanel', MockHotkeyPanel)
        monkeypatch.setattr(testee, 'writejson', mock_writejson)

        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ini = {'lang': 'en'}
        testobj.build_new_pagedata = mock_build
        testobj.book.page = MockHotkeyPanel(testobj.book, '')
        testobj.book.page.gui = MockSDI()
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n"
                "called SingleDataInterface.__init__ with args ()\n")

        testobj.book.page.p0list = 'p0list'
        testobj.book.find_loc = 'find_loc'
        testobj.book.page.settings = {}
        testobj.book.page.column_info = [('xx', 10, False, 0, 0)]
        testobj.new_column_info = [('xx', 10, False, 0, 0)]
        testobj.book.page.otherstuff = {'other': 'stuff'}
        testobj.book.page.pad = 'testfile.json'
        testobj.m_col()
        assert capsys.readouterr().out == (
                f"called Editor.read_columntitledata with arg '{testobj}'\n"
                f"called gui.show_message with args ({testobj.gui}, 'I_ADDSET') {{}}\n")
        testobj.book.page.settings = {'page': 'settings'}
        testobj.book.page.reader = MockReader()
        testobj.captions = {'xx': 'aaa', 'yy': 'bbb'}
        testobj.m_col()
        assert capsys.readouterr().out == (
                f"called Editor.read_columntitledata with arg '{testobj}'\n"
                f"called gui.show_dialog with args ({testobj}, {testee.gui.ColumnSettingsDialog})\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_dialog_2)
        testobj.m_col()
        assert capsys.readouterr().out == (
                f"called Editor.read_columntitledata with arg '{testobj}'\n"
                f"called gui.show_dialog with args ({testobj}, {testee.gui.ColumnSettingsDialog})\n"
                f"called gui.show_message with args ({testobj.gui}, 'I_NOCHG') {{}}\n")
        testobj.new_column_info = [('xx', 10, False, 0, 0), ('yy', 15, False, 1, 'new')]
        testobj.book.page.settings = {'page': 'settings'}
        testobj.m_col()
        assert testobj.book.page.column_info == [('xx', 10, False, 0), ('yy', 15, False, 1)]
        assert capsys.readouterr().out == (
                f"called Editor.read_columntitledata with arg '{testobj}'\n"
                f"called gui.show_dialog with args ({testobj}, {testee.gui.ColumnSettingsDialog})\n"
                "called Editor.build_new_pagedata\n"
                f"called writejson with args ('testfile.json', {testobj.book.page.reader},"
                " {'page': 'settings'},"
                " [('xx', 10, False, 0), ('yy', 15, False, 1)], None, {'other': 'stuff'})\n"
                "called SDI.update_columns with args ('p0list', 1, 2)\n"
                # "called TabbedInterface.refresh_combobox with args ('find_loc', ['aaa', 'bbb'])\n"
                "called TabbedInterface.refresh_combobox with args ('find_loc', ['xx', 'yy'])\n"
                "called SDI.refresh_headers with args"
                " ('p0list', [('xx', 10, False, 0), ('yy', 15, False, 1)])\n"
                "called HotkeyPanel.populate_list with arg p0list\n")

    def test_build_new_pagedata(self, monkeypatch, capsys):
        """unittest for Editor.build_new_pagedata
        """
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.page = MockHotkeyPanel(testobj.book, '')
        testobj.book.page.data = {'qq': ['aa', 1, 'X'], 'rr': ['bb', 2, 'Z']}
        testobj.new_column_info = [('xx', 10, False, 0), ('zz', 12, False, 'new'),
                                   ('yy', 15, False, 1)]
        assert testobj.build_new_pagedata() == {'qq': ['aa', '', 1], 'rr': ['bb', '', 2]}

    def test_accept_columnsettings(self, monkeypatch, capsys):
        """unittest for Editor.accept_columnsettings
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        def mock_build(*args):
            print('called Editor.build_new_title_data with args', args)
            return True, [], []  # canceled
        def mock_build_2(new_titles, column_info):
            print(f'called Editor.build_new_title_data with args ({new_titles}, {column_info})')
            result_titles = zip(['ID1', 'ID2', 'ID3', 'ID4'], new_titles, strict=True)
            # return False, [('ID1', 'title1'), ('ID2', 'title2')], ['col', 'info']  # continue
            return False, result_titles, []
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.page = MockHotkeyPanel(testobj.book, '')
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
        testobj.captions = {}
        testobj.book.page.captions = {}
        testobj.build_new_title_data = mock_build
        data = [('x', 'a', False, 0, 0), ('y', 'b', False, 1, 1), ('x', 'c', False, 2, 2)]
        assert testobj.accept_columnsettings(data) == (False, False)
        assert testobj.captions == {}
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_DPLNAM') {{}}\n")
        data = [('x', 'a', False, 0, 0), ('y', 'b', False, 1, 1), ('', 'c', False, 2, 2)]
        assert testobj.accept_columnsettings(data) == (False, False)
        assert testobj.captions == {}
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_MISSNAM') {{}}\n")
        data = [('x', 'a', False, 0, 0), ('y', 'b', False, 2, 1), ('z', 'c', False, 2, 2)]
        assert testobj.accept_columnsettings(data) == (False, False)
        assert testobj.captions == {}
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_DPLCOL') {{}}\n")
        # data = [('xzz', '010', 0, False, 0), ('yyy', '020', 2, False, 1), ('zzz', '030', 3, False, 2),
        #         ('q', '040', 1, False, 'new')]
        data = [('xzz', '010', False, 0, 0), ('yyy', '020', False, 2, 1), ('zzz', '030', False, 3, 2),
                ('q', '040', False, 1, 'new')]
        testobj.col_names = ['xxx', 'yyy', 'zzz']
        testobj.col_textids = ['id1', 'id2', 'id3']
        testobj.book.page.column_info = []
        assert testobj.accept_columnsettings(data) == (False, True)
        assert testobj.new_column_info == [('xzz', '010', False, 0, 0), ('id2', '020', False, 2, 1), ('id3', '030', False, 3, 2), ('q', '040', False, 1, 'new')]
        assert testobj.captions == {}
        assert testobj.book.page.captions == {}
        assert capsys.readouterr().out == (
                "called Editor.build_new_title_data with args (['xzz', 'q'],"
                " [('xzz', '010', False, 0, 0), ('id2', '020', False, 2, 1),"
                " ('id3', '030', False, 3, 2), ('q', '040', False, 1, 'new')])\n")
        testobj.captions = {}
        testobj.book.page.captions = {}
        testobj.build_new_title_data = mock_build_2
        assert testobj.accept_columnsettings(data) == (True, False)
        assert testobj.new_column_info == [('ID1', '010', False, 0, 0), ('id2', '020', False, 2, 1),
                                           ('id3', '030', False, 3, 2), ('ID2', '040', False, 1, 'new')]
        assert testobj.captions == {'ID1': 'xzz', 'ID2': 'q'}
        assert testobj.book.page.captions == {'ID1': 'xzz', 'ID2': 'q'}
        assert capsys.readouterr().out == (
                "called Editor.build_new_title_data with args (['xzz', 'q'],"
                " [('xzz', '010', False, 0, 0), ('id2', '020', False, 2, 1),"
                " ('id3', '030', False, 3, 2), ('q', '040', False, 1, 'new')])\n")

        data = [('xxx', '010', False, 0, 0), ('yyy', '020', False, 1, 1), ('zzz', '030', False, 2, 2)]
        testobj.captions = {}
        testobj.book.page.captions = {}
        testobj.col_names = ['xxx', 'yyy', 'zzz']
        testobj.book.page.column_info = []
        assert testobj.accept_columnsettings(data) == (True, False)
        assert testobj.new_column_info == [('id1', '010', False, 0, 0),
                                           ('id2', '020', False, 1, 1), ('id3', '030', False, 2, 2)]
        assert testobj.captions == {}
        assert testobj.book.page.captions == {}
        assert capsys.readouterr().out == ''

    def test_build_new_title_data(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.build_new_title_data
        """
        def mock_show(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_show_2(*args):
            print('called gui.show_dialog with args', args)
            args[0].dialog_data = {'en.lng': {}, 'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}}
            return True
        def mock_show_3(*args):
            print('called gui.show_dialog with args', args)
            args[0].dialog_data = {'en.lng': {'C_NEW1': 'xxx_nl', 'C_NEW2': 'yyy_nl'},
                                   'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}}
            return True
        def mock_add(*args):
            print('called add_columntitledata with args', args)
        monkeypatch.setattr(testee.shared, 'HERELANG', tmp_path)
        (tmp_path / 'en').touch()
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
        monkeypatch.setattr(testee, 'add_columntitledata', mock_add)
        testobj = self.setup_testobj(monkeypatch, capsys)
        assert testobj.build_new_title_data([], []) == (True, None, None)
        assert testobj.dialog_data == {'textid': 'C_XXX', 'new_titles': [],
                                       'languages': [], 'colno': -1}
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.NewColumnsDialog})\n")

        (tmp_path / 'en.lng').touch()
        (tmp_path / 'nl.lng').touch()
        testobj.ini = {'lang': 'nl.lng'}
        assert testobj.build_new_title_data([], []) == (True, None, None)
        assert testobj.dialog_data == {'textid': 'C_XXX', 'new_titles': [],
                                       'languages': ['en.lng', 'nl.lng'], 'colno': 2}
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.NewColumnsDialog})\n")
        testobj.ini = {'lang': 'en.lng'}
        assert testobj.build_new_title_data([], []) == (True, None, None)
        assert testobj.dialog_data == {'textid': 'C_XXX', 'new_titles': [],
                                       'languages': ['en.lng', 'nl.lng'], 'colno': 1}
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.NewColumnsDialog})\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
        titles = ['xxx_nl', 'yyy_nl']
        coldata = [['xxx_nl', 10, False], ['yyy_nl', 10, False]]
        # breakpoint()
        canceled, title_list, column_info = testobj.build_new_title_data(titles, coldata)
        assert not canceled
        assert title_list == ['xxx_nl', 'yyy_nl']
        assert column_info == [['xxx_nl', 10, False], ['yyy_nl', 10, False]]
        assert testobj.dialog_data == {'en.lng': {}, 'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}}
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.NewColumnsDialog})\n"
                "called add_columntitledata with args ({'en.lng': {},"
                " 'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}},)\n")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_3)
        titles = ['xxx_nl', 'yyy_nl']
        coldata = [['xxx_nl', 10, False], ['yyy_nl', 10, False]]
        # breakpoint()
        canceled, title_list, column_info = testobj.build_new_title_data(titles, coldata)
        assert not canceled
        assert title_list == [('C_NEW1', 'xxx_nl'), ('C_NEW2', 'yyy_nl')]
        assert column_info == [['C_NEW1', 10, False], ['C_NEW2', 10, False]]
        assert testobj.dialog_data == {'en.lng': {'C_NEW1': 'xxx_nl', 'C_NEW2': 'yyy_nl'},
                                       'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}}
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.NewColumnsDialog})\n"
                "called add_columntitledata with args ({'en.lng': {'C_NEW1': 'xxx_nl',"
                " 'C_NEW2': 'yyy_nl'}, 'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}},)\n")

    def test_accept_newcolumns(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.accept_newcolumns
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        monkeypatch.setattr(testee.shared, 'HERELANG', tmp_path)
        (tmp_path / 'en.lng').write_text('# symbols\n\nC_SYM1  symbol1\nC_SYM2  symbol 2\n')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ini = {'lang': 'en.lng'}
        testobj.dialog_data = {'textid': 'C_XXX', 'new_titles': ['x'],
                               'languages': ['en.lng', 'nl.lng'], 'colno': 1}
        assert not testobj.accept_newcolumns([('', '', '')])
        assert testobj.dialog_data == {}
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'T_NOTALL') {{}}\n")

        testobj.dialog_data = {'textid': 'C_XXX', 'new_titles': ['x'],
                               'languages': ['en.lng', 'nl.lng'], 'colno': 1}
        assert not testobj.accept_newcolumns([('C_XXX', '', '')])
        assert testobj.dialog_data == {}
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'T_CHGSTD') {{}}\n")

        testobj.dialog_data = {'textid': 'C_XXX', 'new_titles': ['x'],
                               'languages': ['en.lng', 'nl.lng'], 'colno': 1}
        assert not testobj.accept_newcolumns([('C_XYZ', '', '')])
        assert testobj.dialog_data == {}
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'T_NOTALL') {{}}\n")

        testobj.dialog_data = {'textid': 'C_XXX', 'new_titles': ['x'],
                               'languages': ['en.lng', 'nl.lng'], 'colno': 1}
        assert not testobj.accept_newcolumns([('C_XXX', 'zzz_nl', 'zzz.en')])
        assert testobj.dialog_data == {}
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'T_CHGSTD') {{}}\n")

        testobj.dialog_data = {'textid': 'C_XXX', 'new_titles': ['x'],
                               'languages': ['en.lng', 'nl.lng'], 'colno': 1}
        assert not testobj.accept_newcolumns([('C_SYM1', 'xxx_nl', 'xxx_en')])
        assert testobj.dialog_data == {}
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'T_NOTUNIQ')"
                " {'args': ('C_SYM1',)}\n")

        testobj.dialog_data = {'textid': 'C_XXX', 'new_titles': ['x'],
                               'languages': ['en.lng', 'nl.lng'], 'colno': 1}
        assert not testobj.accept_newcolumns([('C_NEW', 'xxx_nl', 'xxx_en'),
                                              ('C_NEW', 'yyy_nl', 'yyy_en')])
        assert testobj.dialog_data == {'en.lng': {'C_NEW': 'xxx_nl'}, 'nl.lng': {'C_NEW': 'xxx_en'}}
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'T_NOTUNIQ')"
                " {'args': ('C_NEW',)}\n")

        testobj.dialog_data = {'textid': 'C_XXX', 'new_titles': ['x'],
                               'languages': ['en.lng', 'nl.lng'], 'colno': 1}
        assert testobj.accept_newcolumns([('C_NEW1', 'xxx_nl', 'xxx_en'),
                                          ('C_NEW2', 'xxx_nl', 'xxx_en')])
        assert testobj.dialog_data == {'en.lng': {'C_NEW1': 'xxx_nl', 'C_NEW2': 'xxx_nl'},
                                       'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'xxx_en'}}
        assert capsys.readouterr().out == ""

        testobj.dialog_data = {'textid': 'C_XXX', 'new_titles': ['x'],
                               'languages': ['en.lng', 'nl.lng'], 'colno': 1}
        assert testobj.accept_newcolumns([('C_NEW1', 'xxx_nl', 'xxx_en'),
                                          ('C_NEW2', 'yyy_nl', 'yyy_en')])
        assert testobj.dialog_data == {'en.lng': {'C_NEW1': 'xxx_nl', 'C_NEW2': 'yyy_nl'},
                                       'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}}
        assert capsys.readouterr().out == ""

    def test_m_entry(self, monkeypatch, capsys):
        """unittest for Editor.m_entry
        """
        def mock_show(*args):
            print('called gui.show_message with args', args)
        def mock_dialog(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_dialog_2(*args):
            print('called gui.show_dialog with args', args)
            return True
        def mock_writejson(*args):
            print('called writejson with args', args)
        monkeypatch.setattr(testee, 'writejson', mock_writejson)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ini = {'lang': 'en'}
        testobj.book.page = MockHotkeyPanel(testobj.book, 'xxx')
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, 'xxx')\n")
        testobj.book.page.settings = {}
        testobj.book.page.column_info = [('column', 'info')]
        testobj.book.page.data = {}
        testobj.book.page.otherstuff = {'other': 'stuff'}
        testobj.book.page.pad = 'settings.json'
        testobj.book.page.p0list = 'p0list'
        testobj.m_entry()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_ADDCOL')\n")

        testobj.book.page.settings = {'x': 'y'}
        testobj.book.page.colums_info = []
        testobj.m_entry()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.EntryDialog})\n")

        testobj.book.page.settings = {'x': 'y'}
        testobj.book.page.colums_info = [('column', 'info')]
        testobj.m_entry()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.EntryDialog})\n")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
        testobj.m_entry()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.EntryDialog})\n")

        testobj.book.page.data = {'a': 'b'}
        testobj.book.page.reader = MockReader()
        testobj.m_entry()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.EntryDialog})\n"
                f"called writejson with args ('settings.json', {testobj.book.page.reader},"
                " {'x': 'y'}, [('column', 'info')], {'a': 'b'}, {'other': 'stuff'})\n"
                "called HotkeyPanel.populate_list with arg p0list\n")

    def test_m_editdescs(self, monkeypatch, capsys):
        """unittest for Editor.m_editdescs
        """
        def mock_show(*args):
            print('called gui.show_message with args', args)
        def mock_dialog(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_dialog_2(*args):
            print('called gui.show_dialog with args', args)
            return True
        def mock_writejson(*args):
            print('called writejson with args', args)
        def mock_update(*args):
            print('called reader.update_descriptions with args', args)
        monkeypatch.setattr(testee, 'writejson', mock_writejson)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ini = {'lang': 'en'}
        testobj.book.page = MockHotkeyPanel(testobj.book, 'xxx')
        testobj.book.page.reader = types.SimpleNamespace()
        assert capsys.readouterr().out == (
                f"called HotkeyPanel.__init__ with args ({testobj.book}, 'xxx')\n")
        testobj.book.page.settings = {'set': 'tings'}
        testobj.book.page.column_info = [('column', 'info')]
        testobj.book.page.data = {'da': 'ta'}
        testobj.book.page.otherstuff = {'other': 'stuff'}
        testobj.book.page.pad = 'settings.json'
        testobj.book.page.p0list = 'p0list'
        testobj.m_editdescs()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_NOMAP')\n")
        testobj.book.page.descriptions = {}
        testobj.m_editdescs()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_NOMAP')\n")
        testobj.book.page.descriptions = {'desc': 'riptions'}
        testobj.m_editdescs()
        assert capsys.readouterr().out == (
                f"called gui.show_message with args ({testobj.gui}, 'I_NOMETH')\n")
        testobj.book.page.reader.update_descriptions = mock_update

        testobj.dialog_data = {'dialog': 'data'}
        testobj.m_editdescs()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.CompleteDialog})\n")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
        testobj.m_editdescs()
        assert capsys.readouterr().out == (
                f"called gui.show_dialog with args ({testobj}, {testee.gui.CompleteDialog})\n"
                f"called reader.update_descriptions with args ({testobj.book.page},"
                " {'dialog': 'data'})\n"
                f"called writejson with args ('settings.json', {testobj.book.page.reader},"
                " {'set': 'tings'}, [('column', 'info')], {'da': 'ta'}, {'other': 'stuff'})\n"
                "called HotkeyPanel.populate_list with arg p0list\n")

    def test_m_lang(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.m_lang
        """
        def mock_choice(*args, **kwargs):
            print('called gui.get_choice with args', args, kwargs)
            return '', False
        def mock_choice_2(*args, **kwargs):
            print('called gui.get_choice with args', args, kwargs)
            return 'xx', True
        def mock_write(arg):
            print(f"called write_config with arg '{arg}'")
        def mock_read(arg):
            print(f"called Editor.readcaptions with arg '{arg}'")
        def mock_set():
            print("called Editor.setcaptions")
        monkeypatch.setattr(testee, 'write_config', mock_write)
        monkeypatch.setattr(testee.gui, 'get_choice', mock_choice)
        langdir = tmp_path
        (langdir / 'en.lng').touch()
        (langdir / 'nl.lng').touch()
        monkeypatch.setattr(testee.shared, 'HERELANG', langdir)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.title = 'hello'
        testobj.captions = {'P_SELLNG': 'xxx'}
        testobj.readcaptions = mock_read
        testobj.setcaptions = mock_set
        testobj.ini = {'lang': 'du.lng'}
        testobj.m_lang()
        assert testobj.ini['lang'] == 'du.lng'
        assert capsys.readouterr().out == (
                "called gui.get_choice with args"
                f" ({testobj.gui}, 'xxx', 'hello', ['en.lng', 'nl.lng']) {{'current': 0}}\n")

        testobj.ini = {'lang': 'nl.lng'}
        testobj.m_lang()
        assert testobj.ini['lang'] == 'nl.lng'
        assert capsys.readouterr().out == (
                "called gui.get_choice with args"
                f" ({testobj.gui}, 'xxx', 'hello', ['en.lng', 'nl.lng']) {{'current': 1}}\n")

        monkeypatch.setattr(testee.gui, 'get_choice', mock_choice_2)
        testobj.m_lang()
        assert testobj.ini['lang'] == 'xx'
        assert capsys.readouterr().out == (
                "called gui.get_choice with args"
                f" ({testobj.gui}, 'xxx', 'hello', ['en.lng', 'nl.lng']) {{'current': 1}}\n"
                "called write_config with arg '{'lang': 'xx'}'\n"
                "called Editor.readcaptions with arg 'xx'\n"
                "called Editor.setcaptions\n")

    def test_m_about(self, monkeypatch, capsys):
        """unittest for Editor.m_about
        """
        def mock_show(*args, **kwargs):
            print('called gui.show_message with args', args, kwargs)
        monkeypatch.setattr(testee.gui, 'show_message', mock_show)
        monkeypatch.setattr(testee, 'VRS', 'xxx')
        monkeypatch.setattr(testee, 'AUTH', 'yyy')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.captions = {'T_ABOUT': '{} / versie {} / {} / {}', 'T_SHORT': 'this',
                            'T_LONG': 'more text'}
        testobj.m_about()
        assert capsys.readouterr().out == (
                "called gui.show_message with args"
                f" ({testobj.gui},) {{'text': 'this\\nversie xxx\\nyyy\\nmore text'}}\n")

    def test_m_pref(self, monkeypatch, capsys):
        """unittest for Editor.m_pref
        """
        def mock_dialog(*args):
            print('called gui.show_dialog with args', args)
            return False
        def mock_dialog_2(*args):
            print('called gui.show_dialog with args', args)
            args[0].prefs = ('Remember', 'unchanged')
            return True
        def mock_dialog_3(*args):
            print('called gui.show_dialog with args', args)
            args[0].prefs = ('Fixed', 'unchanged')
            return True
        def mock_dialog_4(*args):
            print('called gui.show_dialog with args', args)
            args[0].prefs = ('Remember', 'changed')
            return True
        def mock_dialog_5(*args):
            print('called gui.show_dialog with args', args)
            args[0].prefs = ('Fixed', 'changed')
            return True
        def mock_dialog_6(*args):
            print('called gui.show_dialog with args', args)
            args[0].prefs = ('', 'changed')
            return True
        def mock_write(arg):
            print(f"called write_config with arg '{arg}'")
        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog)
        monkeypatch.setattr(testee, 'write_config', mock_write)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
        testobj.m_pref()
        assert testobj.ini['startup'] == 'Fixed'
        assert testobj.ini['initial'] == 'unchanged'
        assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.InitialToolDialog})\n")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
        # testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
        testobj.m_pref()
        assert testobj.ini['startup'] == 'Remember'
        assert testobj.ini['initial'] == 'unchanged'
        assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.InitialToolDialog})\n"
            "called write_config with arg '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_3)
        testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
        testobj.m_pref()
        assert testobj.ini['startup'] == 'Fixed'
        assert testobj.ini['initial'] == 'unchanged'
        assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.InitialToolDialog})\n")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_4)
        testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
        testobj.m_pref()
        assert testobj.ini['startup'] == 'Remember'
        assert testobj.ini['initial'] == 'unchanged'
        assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.InitialToolDialog})\n"
            "called write_config with arg '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_5)
        testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
        testobj.m_pref()
        assert testobj.ini['startup'] == 'Fixed'
        assert testobj.ini['initial'] == 'changed'
        assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.InitialToolDialog})\n"
            "called write_config with arg '{'startup': 'Fixed', 'initial': 'changed'}'\n")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_6)
        testobj.ini = {'startup': 'Remember', 'initial': 'unchanged'}
        testobj.m_pref()
        assert testobj.ini['startup'] == 'Remember'
        assert testobj.ini['initial'] == 'unchanged'
        assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.InitialToolDialog})\n")

        monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_6)
        testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
        testobj.m_pref()
        assert testobj.ini['startup'] == 'Fixed'
        assert testobj.ini['initial'] == 'changed'
        assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.InitialToolDialog})\n"
            "called write_config with arg '{'startup': 'Fixed', 'initial': 'changed'}'\n")

    def test_accept_startupsettings(self, monkeypatch, capsys):
        """unittest for Editor.accept_startupsettings
        """
        monkeypatch.setattr(testee.shared, 'mode_f', 'fixed')
        monkeypatch.setattr(testee.shared, 'mode_r', 'remember')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.accept_startupsettings(True, False, 'xxx')
        assert testobj.prefs == ('fixed', 'xxx')
        testobj.accept_startupsettings(False, True, 'yyy')
        assert testobj.prefs == ('remember', 'yyy')
        testobj.accept_startupsettings(True, True, 'zzz')
        assert testobj.prefs == ('fixed', 'zzz')
        testobj.accept_startupsettings(False, False, 'qqq')
        assert testobj.prefs == (None, 'qqq')

    def test_m_exit(self, monkeypatch, capsys):
        """unittest for Editor.m_exit
        """
        def mock_exit():
            print('called Editor.exit')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.exit = mock_exit
        testobj.m_exit()
        assert capsys.readouterr().out == 'called Editor.exit\n'

    def test_exit(self, monkeypatch, capsys):
        """unittest for Editor.exit
        """
        def mock_exit():
            print('called HotkeyPanel.exit')
            return False
        def mock_exit_2():
            print('called HotkeyPanel.exit')
            return True
        def mock_write(*args, **kwargs):
            print('called write_config with args', args, kwargs)
        def mock_get():
            print('called SingledataInterface.get_selected_text')
            return 'xxx'
        monkeypatch.setattr(testee.shared, 'mode_f', 'fixed')
        monkeypatch.setattr(testee.shared, 'mode_r', 'remember')
        monkeypatch.setattr(testee, 'write_config', mock_write)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.book.page = types.SimpleNamespace(exit=mock_exit)
        testobj.book.sel = 'selector'
        testobj.ini = {}
        testobj.exit()
        assert testobj.ini == {}
        assert capsys.readouterr().out == ("called HotkeyPanel.exit\n")
        testobj.book.page = types.SimpleNamespace(exit=mock_exit_2)
        testobj.exit()
        assert testobj.ini == {}
        assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                           "called Gui.close\n")
        testobj.ini = {'startup': 'remember'}
        testobj.forgetatexit = False
        testobj.book.gui.get_selected_text = mock_get
        testobj.exit()
        assert testobj.ini['initial'] == 'xxx'
        assert capsys.readouterr().out == (
                "called HotkeyPanel.exit\n"
                "called TabbedInterface.get_combobox_value with arg selector\n"
                "called write_config with args"
                " ({'startup': 'remember', 'initial': 'xxx'},) {'nobackup': True}\n"
                "called Gui.close\n")
        testobj.ini = {'startup': 'remember', 'initial': 'yyy'}
        testobj.forgetatexit = True
        testobj.book.gui.get_selected_text = mock_get
        testobj.exit()
        assert testobj.ini['initial'] == 'yyy'
        assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                           "called Gui.close\n")
        testobj.ini = {'startup': 'remember', 'initial': 'yyy'}
        testobj.forgetatexit = False
        testobj.book.gui.get_selected_text = mock_get
        testobj.exit()
        assert testobj.ini['initial'] == 'xxx'
        assert capsys.readouterr().out == (
                "called HotkeyPanel.exit\n"
                "called TabbedInterface.get_combobox_value with arg selector\n"
                "called write_config with args"
               " ({'startup': 'remember', 'initial': 'xxx'},) {'nobackup': True}\n"
               "called Gui.close\n")
        testobj.ini = {'startup': 'remember', 'initial': 'yyy'}
        testobj.book.gui = types.SimpleNamespace()  # no controls so we get an AttributeError
        testobj.exit()
        assert testobj.ini['initial'] == 'yyy'
        assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                           "called Gui.close\n")
        testobj.ini = {'startup': 'fixed'}
        testobj.exit()
        assert testobj.ini == {'startup': 'fixed'}
        assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                           "called Gui.close\n")

    def test_change_setting(self, monkeypatch, capsys, tmp_path):
        """unittest for Editor.change_setting
        """
        ininame = tmp_path / 'mock_ini'
        ininame.touch()
        bakname = ininame.with_suffix('.bak')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.captions = {'C_SETT': 'setting', 'C_TITLE': 'xxxxx'}
        testobj.ini = {'filename': str(ininame)}
        testobj.change_setting('sett', 'was', 'is')
        assert bakname.read_text() == ''
        assert ininame.read_text() == "# setting\nSETT = 'is'\n"

        testobj.change_setting('sett', 'is', '')
        assert bakname.read_text() == "# setting\nSETT = 'is'\n"
        assert ininame.read_text() == "# setting\nSETT = ''\n"

        testobj.change_setting('sett', '', 'was')
        assert bakname.read_text() == "# setting\nSETT = ''\n"
        assert ininame.read_text() == "# setting\nSETT = 'was'\n"

        testobj.change_setting('sett', 'was', 'is')
        assert bakname.read_text() == "# setting\nSETT = 'was'\n"
        assert ininame.read_text() == "# setting\nSETT = 'is'\n"

        testobj.change_setting('title', '', 'tata')
        assert bakname.read_text() == "# setting\nSETT = 'is'\n"
        assert ininame.read_text() == "# setting\nSETT = 'is'\n# xxxxx\nTITLE = 'tata'\n"

        testobj.change_setting('title', 'tata', '')
        assert bakname.read_text() == "# setting\nSETT = 'is'\n# xxxxx\nTITLE = 'tata'\n"
        assert ininame.read_text() == "# setting\nSETT = 'is'\n"

    def test_readcaptions(self, monkeypatch, capsys):
        """unittest for Editor.readcaptions
        """
        def mock_read(lang):
            print(f"called readlang with arg '{lang}'")
            return {'captions': 'dict'}
        monkeypatch.setattr(testee, 'readlang', mock_read)
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.readcaptions('en')
        assert testobj.captions == {'captions': 'dict'}
        assert testobj.last_textid == ''

    def test_setcaptions(self, monkeypatch, capsys):
        """unittest for Editor.setcaptions
        """
        def mock_set():
            print('called EditorGui.update_menutitles')
        def mock_set2():
            print('called TabbedInterface.setcaptions')
        def mock_set3():
            print('called HotkeyPanel.setcaptions')
        testobj = self.setup_testobj(monkeypatch, capsys)
        testobj.gui.update_menutitles = mock_set
        testobj.book.setcaptions = mock_set2
        testobj.book.page = types.SimpleNamespace(setcaptions=mock_set3)
        testobj.setcaptions()
        assert capsys.readouterr().out == ("called EditorGui.update_menutitles\n"
                                           "called TabbedInterface.setcaptions\n"
                                           "called HotkeyPanel.setcaptions\n")
