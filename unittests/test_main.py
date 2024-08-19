"""unittests for ./editor/main.py
"""
import types
import pytest
import editor.main as testee


class MockSettType(testee.enum.Enum):
    """stub for shared.SettType
    """
    PLG = 'plg'
    PNL = 'pnl'
    RBLD = 'rbld'
    DETS = 'dets'
    RDEF = 'rdef'

class MockLineType(testee.enum.Enum):
    """stub for main.LineType
    """
    SETT = 'sett'
    CAPT = 'capt'
    WID = 'wid'
    ORIG = 'orig'
    KEY = 'key'

class MockSDI:
    """stub for gui.SingleDataInterface
    """
    def __init__(self, *args):
        print('called SingleDataInterface.__init__ with args', args)
    def setup_empty_screen(self, *args):
        """stub
        """
        print('called SDI.setup_empty_screen with args', args)
    def add_extra_fields(self):
        """stub
        """
        print('called SDI.add_extra_fields')
    def set_extrascreen_editable(self, *args):
        """stub
        """
        print('called SDI.set_extrascreen_editable with args', args)
    def setup_list(self):
        """stub
        """
        print('called SDI.setup_list')
    def getfirstitem(self):
        """stub
        """
        return 'first_item'
    def init_combobox(self, *args):
        """stub
        """
        print('called SingleDataInterface.init_combobox with args', args)
    def set_textfield_value(self, *args):
        """stub
        """
        print('called SingleDataInterface.set_textfield_value with args', args)
    def set_checkbox_state(self, *args):
        """stub
        """
        print('called SingleDataInterface.set_checkbox_state with args', args)
    def set_combobox_string(self, *args):
        """stub
        """
        print('called SingleDataInterface.set_combobox_string with args', args)
    def enable_save(self, value):
        """stub
        """
        print(f"called SingleDataInterface.enable_save with arg {value}")
    def enable_delete(self, value):
        """stub
        """
        print(f"called SingleDataInterface.enable_delete with arg {value}")
    def update_columns(self, *args):
        """stub
        """
        print("called SingleDataInterface.update_colums with args", args)
    def refresh_headers(self, headers):
        """stub
        """
        print(f"called SingleDataInterface.refresh_headers with arg {headers}")

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


def test_readlang(monkeypatch, tmp_path):
    """unittest for main.readlang
    """
    mock_lang = tmp_path / 'hotkeys' / 'lang'
    monkeypatch.setattr(testee.shared, 'HERELANG', mock_lang)
    mock_lang.mkdir(parents=True)
    (mock_lang / 'en').write_text("#deze overslaan\n\ncode text\n\nalso a code with text\n")
    assert testee.readlang('en') == {'code': 'text', 'also': 'a code with text'}

def test_read_settings(monkeypatch, tmp_path):
    """unittest for main.read_settings
    """
    monkeypatch.setattr(testee, 'initial_settings', {'x': '', 'a': ''})
    ini = tmp_path / 'settingsfile'
    ini.write_text('{"a": "b", "q": "r"}\n')
    assert testee.read_settings(ini) == {'a': 'b', 'filename': ini, 'x': ''}

def test_write_settings(monkeypatch, capsys, tmp_path):
    """unittest for main.write_settings
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
    monkeypatch.setattr(testee, 'initial_settings', {'x': '', 'a': ''})
    ini = tmp_path / 'settingsfile'
    testee.write_settings(settings={'a': 'b', 'filename': ini, 'x': 'y'})
    assert capsys.readouterr().out == "called json.dump with arg {'a': 'b', 'x': 'y'}\n"
    monkeypatch.setattr(testee.shutil, 'copyfile', mock_copy)
    monkeypatch.setattr(testee.shared.pathlib.Path, 'exists', lambda *x: True)
    testee.write_settings(settings={'a': 'b', 'filename': ini, 'x': 'y'})
    assert capsys.readouterr().out == (f"called shutil.copyfile with args ('{ini}',"
                                       f" '{str(ini) + '~'}')\n"
                                       "called json.dump with arg {'a': 'b', 'x': 'y'}\n")
    testee.write_settings(settings={'a': 'b', 'filename': ini, 'x': 'y'}, nobackup=True)
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
            'aaa\nbbb\n\n# Keyboard mapping\nID1 text1\nID2 text 2\n#end\nID3 text3\n')
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
    paths = (('xx', 'yy.json'), ('aa', 'bb.json'))
    pathdata = {'xx': ['xx.yy.zz', 'xxx', 1, 0, 0], 'aa': ['.bb.cc', 'aaa', 1, 1, 1]}
    assert testee.update_paths(paths, pathdata, 'en') == [('xx', 'yy.json'), ('aa', 'bb.json')]
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
    monkeypatch.setattr(testee, 'initial_columns', (('a', 1, True), 'b', 2, False))
    testee.initjson('settfile', ['xxx', 'yyy'])
    assert capsys.readouterr().out == ("called writejson with args"
                                       " ('settfile', None, {'x': 'xxx', 'y': 'yyy'},"
                                       " [(('a', 1, True), 'b', 2, False)], {}, {})\n")

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
    def mock_update(data):
        print('called Reader.update_otherstuff_outbound with arg', data)
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
                                   ' "otherstuff": {"xxx": ["a", "b", "c"], "yyy": ["q", "r"],'
                                   ' "zzz": {"m": "n"}}}')
    assert capsys.readouterr().out == ''
    reader.update_otherstuff_outbound = mock_update
    otherstuff = {'xxx': {'a', 'b', 'c'}, 'yyy': ['q', 'r'], 'zzz': {'m': 'n'}}
    testee.writejson(str(plgfile), reader, {'settings': 'dict'}, [['column', 'info']],
                     {'keycombo': 'dict'},
                     {'xxx': {'a', 'b', 'c'}, 'yyy': ['q', 'r'], 'zzz': {'m': 'n'}})
    assert plgfile.read_text() == ('{"settings": {"settings": "dict"},'
                                   ' "column_info": [["column", "info"]],'
                                   ' "keydata": {"keycombo": "dict"},'
                                   ' "otherstuff": {"xxx": ["a", "b", "c"], "yyy": ["q", "r"],'
                                   ' "zzz": {"m": "n"}}}')
    assert capsys.readouterr().out == (
            f"called Reader.update_otherstuff_outbound with arg {otherstuff}\n")
    reader = None
    testee.writejson(str(plgfile), reader, {'settings': 'dict'}, [['column', 'info']],
                     {'keycombo': 'dict'},
                     {'xxx': {'a', 'b', 'c'}, 'yyy': ['q', 'r'], 'zzz': {'m': 'n'}})
    assert plgfile.read_text() == ('{"settings": {"settings": "dict"},'
                                   ' "column_info": [["column", "info"]],'
                                   ' "keydata": {"keycombo": "dict"},'
                                   ' "otherstuff": {"xxx": ["a", "b", "c"], "yyy": ["q", "r"],'
                                   ' "zzz": {"m": "n"}}}')
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


def test_hotkeypanel_init(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.init
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
        return {'x': 'y'}, [[], []], {}, {}
    def mock_readjson_2(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '0'}, [[], []], {}, {}
    def mock_readjson_3(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return ({'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '1',
                 'RedefineKeys': '0'}, [['x', 0], ['y', 1]], {}, {})
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
    def mock_import_ok_2(*args):
        """stub
        """
        print('called importlib.import_module with args', args)
        return MockReader2()
    def mock_add(self):
        """stub
        """
        print('called HotkeyPanel.add_extra_attributes')
    def mock_refresh(self, arg):
        """stub
        """
        print(f'called HotkeyPanel.refresh_extrascreen with arg {arg}')
    pad = 'NO_PATH'
    parent = types.SimpleNamespace(parent=types.SimpleNamespace(title='A title',
                                                                captions={'I_NOPATH': 'no path',
                                                                    'I_NOSET': '{}',
                                                                    'I_NOSETFIL': '{} not found',
                                                                    'I_NOSETT': '{} no settings',
                                                                    'I_NODATA': 'no data'}),
                                   gui='parent gui')
    monkeypatch.setattr(testee.gui, 'SingleDataInterface', MockSDI)
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log_exc)
    monkeypatch.setattr(testee.shared, 'log', mock_log)
    monkeypatch.setattr(testee, 'readjson', mock_readjson)
    testobj = testee.HotkeyPanel(parent, pad)
    assert testobj.pad == pad
    assert testobj.parent == parent
    assert testobj.initializing_screen
    assert not testobj.modified
    assert testobj.title == 'A title'
    assert testobj.captions == parent.parent.captions
    assert testobj.filtertext == ''
    assert not testobj.has_extrapanel
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `NO_PATH`\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no path', 'A title')\n")

    testobj = testee.HotkeyPanel(parent, '')
    assert (testobj.settings, testobj.column_info, testobj.data) == ({}, [], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg ``\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no data:\\n\\nempty filename', 'A title')\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson_exc_1)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == ({}, [], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.json`\n'
                                       'called shared.log_exc\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no data:\\n\\nA ValueError', 'A title')\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson_exc_2)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == ({}, [], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.json`\n'
                                       'called shared.log_exc\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no data:\\n\\nplugin.json not found', 'A title')\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    # testobj.reader = types.SimpleNamespace()
    assert (testobj.settings, testobj.column_info, testobj.data) == ({'x': 'y'}, [[], []], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.json`\n'
                                       'called readjson with arg `plugin.json`\n'
                                       'called shared.log_exc\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no plugin code', 'A title')\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson_2)
    monkeypatch.setattr(testee.importlib, 'import_module', mock_import_nok)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == (
            {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '0'}, [[], []], {})
    assert capsys.readouterr().out == ('called SingleDataInterface.__init__ with args'
                                       f" ('parent gui', {testobj})\n"
                                       'called shared.log with arg `plugin.json`\n'
                                       'called readjson with arg `plugin.json`\n'
                                       "called importlib.import_module with args ('plugin',)\n"
                                       'called shared.log_exc\n'
                                       'called SDI.setup_empty_screen with args'
                                       " ('no plugin code', 'A title')\n")

    monkeypatch.setattr(testee.importlib, 'import_module', mock_import_ok)
    monkeypatch.setattr(testee.HotkeyPanel, 'add_extra_attributes', mock_add)
    monkeypatch.setattr(testee.HotkeyPanel, 'refresh_extrascreen', mock_refresh)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == (
            {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '0'}, [[], []], {})
    assert not testobj.has_extrapanel
    assert testobj.title == 'A Panel'
    assert not testobj.initializing_screen
    assert capsys.readouterr().out == ("called SingleDataInterface.__init__ with args"
                                       f" ('parent gui', {testobj})\n"
                                       "called shared.log with arg `plugin.json`\n"
                                       "called readjson with arg `plugin.json`\n"
                                       "called importlib.import_module with args ('plugin',)\n"
                                       "called SDI.setup_list\n")

    monkeypatch.setattr(testee, 'readjson', mock_readjson_3)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == (
            {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '1', 'RedefineKeys': '0'},
            [['x', 0], ['y', 1]], {})
    assert testobj.has_extrapanel
    assert testobj.title == 'A Panel'
    assert not testobj.initializing_screen
    assert capsys.readouterr().out == ("called SingleDataInterface.__init__ with args"
                                       f" ('parent gui', {testobj})\n"
                                       "called shared.log with arg `plugin.json`\n"
                                       "called readjson with arg `plugin.json`\n"
                                       "called importlib.import_module with args ('plugin',)\n"
                                       "called HotkeyPanel.add_extra_attributes\n"
                                       "called SDI.add_extra_fields\n"
                                       "called SDI.set_extrascreen_editable with args (False,)\n"
                                       "called SDI.setup_list\n"
                                       "called HotkeyPanel.refresh_extrascreen with arg first_item\n")

    monkeypatch.setattr(testee.importlib, 'import_module', mock_import_ok_2)
    testobj = testee.HotkeyPanel(parent, 'plugin.json')
    assert (testobj.settings, testobj.column_info, testobj.data) == (
            {'PluginName': 'plugin', 'PanelName': 'A Panel', 'ShowDetails': '1', 'RedefineKeys': '0'},
            [['x', 0], ['y', 1]], {})
    assert testobj.has_extrapanel
    assert testobj.title == 'A Panel'
    assert not testobj.initializing_screen
    assert capsys.readouterr().out == ("called SingleDataInterface.__init__ with args"
                                       f" ('parent gui', {testobj})\n"
                                       "called shared.log with arg `plugin.json`\n"
                                       "called readjson with arg `plugin.json`\n"
                                       "called importlib.import_module with args ('plugin',)\n"
                                       "called Reader.update_otherstuff_inbound with arg {}\n"
                                       "called HotkeyPanel.add_extra_attributes\n"
                                       "called SDI.add_extra_fields\n"
                                       "called SDI.set_extrascreen_editable with args (False,)\n"
                                       "called SDI.setup_list\n"
                                       "called HotkeyPanel.refresh_extrascreen with arg first_item\n")

def setup_hotkeypanel(monkeypatch, capsys):
    """stub for initializing main.HotKeyPanel when needed
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

def test_hotkeypanel_readkeys(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.readkeys
    """
    def mock_readjson(arg):
        """stub
        """
        print(f'called readjson with arg `{arg}`')
        return {}, [], 'jsondata', {}
    monkeypatch.setattr(testee, 'readjson', mock_readjson)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.pad = 'plugin.json'
    testobj.readkeys()
    assert testobj.data == 'jsondata'
    assert capsys.readouterr().out == 'called readjson with arg `plugin.json`\n'

def test_hotkeypanel_savekeys(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.savekeys
    """
    def mock_logexc():
        print('called shared.log_exc')
    def mock_writejson(*args):
        print('called writejson with args', args)
    def mock_savekeys(arg):
        print('called Reader.savekeys with arg', arg)
        raise AttributeError
    def mock_savekeys_2(arg):
        print('called Reader.savekeys with arg', arg)
    def mock_set_title(**kwargs):
        print('called HotkeyPanel.set_title with args', kwargs)
    monkeypatch.setattr(testee.shared, 'log_exc', mock_logexc)
    monkeypatch.setattr(testee, 'writejson', mock_writejson)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.reader.savekeys = mock_savekeys
    testobj.pad = 'xxxx.json'
    testobj.settings = ['settings']
    testobj.column_info = ['column', 'info']
    testobj.data = ['data']
    testobj.otherstuff = ['other', 'stuff']
    testobj.set_title = mock_set_title
    testobj.parent.parent.ini = {'lang': 'en'}
    testobj.savekeys()
    assert capsys.readouterr().out == (f"called Reader.savekeys with arg {testobj}\n"
                                       "called shared.log_exc\n"
                                       f"called writejson with args ('xxxx.json', {testobj.reader},"
                                       " ['settings'],"
                                       " ['column', 'info'], ['data'], ['other', 'stuff'])\n"
                                       "called HotkeyPanel.set_title with args {'modified': False}\n")

    testobj.reader.savekeys = mock_savekeys_2
    testobj.savekeys()
    assert capsys.readouterr().out == (f"called Reader.savekeys with arg {testobj}\n"
                                       f"called writejson with args ('xxxx.json', {testobj.reader},"
                                       " ['settings'],"
                                       " ['column', 'info'], ['data'], ['other', 'stuff'])\n"
                                       "called HotkeyPanel.set_title with args {'modified': False}\n")

def test_hotkeypanel_setcaptions(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.setcaptions
    """
    class MockWidget:
        "stub for getting just a reference to a widget"
    def mock_title():
        print('called HotKeyPanel.set_title')
    def mock_labeltext(*args):
        print('called HotkeyPanelGui.set_label_text with args', args)
    def mock_resize():
        print('called HotkeyPanelGui.resize_if_necessary')
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.parent.parent.captions = {'C_KTXT': 'key', 'M_WIN': 'win', 'M_CTRL': 'ctrl',
                                      'M_ALT': 'alt', 'M_SHFT': 'shift', 'C_CNTXT': 'context',
                                      'C_CMD': 'command', 'C_PARMS': 'parms', 'C_CTRL': 'control',
                                      'C_BPARMS': 'bparms', 'C_APARMS': 'aparms',
                                      'C_FEAT': 'feature', 'C_SAVE': 'save', 'C_DEL': 'delete'}
    testobj.set_title = mock_title
    testobj.gui.set_label_text = mock_labeltext
    testobj.gui.resize_if_necessary = mock_resize
    testobj.gui.lbl_key = MockWidget()
    testobj.gui.cb_win = MockWidget()
    testobj.gui.cb_ctrl = MockWidget()
    testobj.gui.cb_alt = MockWidget()
    testobj.gui.cb_shift = MockWidget()
    testobj.gui.lbl_context = MockWidget()
    testobj.gui.txt_cmd = MockWidget()
    testobj.gui.lbl_parms = MockWidget()
    testobj.gui.lbl_controls = MockWidget()
    testobj.gui.pre_parms_label = MockWidget()
    testobj.gui.post_parms_label = MockWidget()
    testobj.gui.feature_label = MockWidget()
    testobj.gui.b_save = MockWidget()
    testobj.gui.b_del = MockWidget()
    testobj.fields = ['C_KEY']
    testobj.has_extrapanel = False
    testobj.setcaptions()
    assert capsys.readouterr().out == ("called HotKeyPanel.set_title\n")
    testobj.fields = []
    testobj.has_extrapanel = True
    testobj.setcaptions()
    assert capsys.readouterr().out == (
            "called HotKeyPanel.set_title\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.b_save}, 'save')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.b_del}, 'delete')\n"
            "called HotkeyPanelGui.resize_if_necessary\n")
    testobj.fields = ['C_KEY', 'C_MODS', 'C_CNTXT', 'C_CMD', 'C_PARMS', 'C_CTRL', 'C_BPARMS',
                      'C_APARMS', 'C_FEAT']
    testobj.setcaptions()
    assert capsys.readouterr().out == (
            "called HotKeyPanel.set_title\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.lbl_key}, 'key')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.cb_win}, '+win  ')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.cb_ctrl}, '+ctrl  ')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.cb_alt}, '+alt  ')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.cb_shift}, '+shift  ')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.lbl_context},"
            " 'context:')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.txt_cmd}, 'command')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.lbl_parms}, 'parms')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.lbl_controls},"
            " 'control')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.pre_parms_label},"
            " 'bparms:')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.post_parms_label},"
            " 'aparms:')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.feature_label},"
            " 'feature:')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.b_save}, 'save')\n"
            f"called HotkeyPanelGui.set_label_text with args ({testobj.gui.b_del}, 'delete')\n"
            "called HotkeyPanelGui.resize_if_necessary\n")

def test_hotkeypanel_populate_list(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.populate_list
    """
    def mock_logexc():
        print('called shared.log_exc')
    def mock_clear():
        print('called HotkeyPanelGui.clear_list')
    def mock_build(key):
        print(f"called HotkeyPanelGui.build_listitem with arg '{key}'")
        return f'item-{key}'
    def mock_set_text(*args):
        print('called HotkeyPanelGui.set_listitemtext with args', args)
    def mock_add(item):
        print(f'called HotkeyPanelGui.add_listitem with arg {item}')
    def mock_select(pos):
        print(f'called HotkeyPanelGui.set_listselection with arg {pos}')
    monkeypatch.setattr(testee.shared, 'log_exc', mock_logexc)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.captions = {'C_DFLT': 'default', 'C_RDEF': 'custom'}
    testobj.gui.clear_list = mock_clear
    testobj.gui.build_listitem = mock_build
    testobj.gui.set_listitemtext = mock_set_text
    testobj.gui.add_listitem = mock_add
    testobj.gui.set_listselection = mock_select
    testobj.data = {}
    testobj.populate_list()
    assert capsys.readouterr().out == "called HotkeyPanelGui.clear_list\n"
    testobj.column_info = [('xxx', 10, False), ('yyy', 20, False), ('zzz', 5, True)]
    testobj.data = {'a': 'key error', '1': ['aaa', 'bbb', 'S'], 2: ['ppp', 'qqq', 'rrr']}
    testobj.populate_list()
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.clear_list\n"
            "called shared.log_exc\n"
            "called HotkeyPanelGui.build_listitem with arg '1'\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-1', 0, 'aaa')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-1', 1, 'bbb')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-1', 2, 'default')\n"
            "called HotkeyPanelGui.add_listitem with arg item-1\n"
            "called HotkeyPanelGui.build_listitem with arg '2'\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-2', 0, 'ppp')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-2', 1, 'qqq')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-2', 2, 'custom')\n"
            "called HotkeyPanelGui.add_listitem with arg item-2\n"
            "called HotkeyPanelGui.set_listselection with arg 0\n")
    testobj.data = {3: ['ppp', 'qqq']}  # te weinig kolommen in data
    with pytest.raises(IndexError) as exc:
        testobj.populate_list()
    assert str(exc.value) == 'list index out of range'
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.clear_list\n"
            "called HotkeyPanelGui.build_listitem with arg '3'\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 0, 'ppp')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 1, 'qqq')\n"
            "['ppp', 'qqq']\n")
    testobj.data = {3: ['ppp', 'qqq', 'R', 'sss']}  # te veel kolommen
    testobj.populate_list()
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.clear_list\n"
            "called HotkeyPanelGui.build_listitem with arg '3'\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 0, 'ppp')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 1, 'qqq')\n"
            "called HotkeyPanelGui.set_listitemtext with args ('item-3', 2, 'custom')\n"
            "called HotkeyPanelGui.add_listitem with arg item-3\n"
            "called HotkeyPanelGui.set_listselection with arg 0\n")

def test_hotkeypanel_add_extra_attributes(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.add_extra_attributes
    """
    def mock_logexc():
        print('called shared.log_exc')
    def mock_add(arg):
        print('called Reader.add_extra_attributes with arg', arg)
    monkeypatch.setattr(testee.shared, 'log_exc', mock_logexc)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
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
    assert capsys.readouterr().out == "called shared.log_exc\n"
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

def test_hotkeypanel_set_title(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.set_title
    """
    def mock_set(value):
        print(f"called HotkeyPanelGui.set_title with arg '{value}'")
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.captions = {"T_MOD": '(*)'}
    testobj.gui.set_title = mock_set
    testobj.modified = True
    testobj.title = 'xxxx'
    testobj.set_title()
    assert capsys.readouterr().out == ("called HotkeyPanelGui.set_title with arg 'xxxx (*)'\n")
    testobj.modified = False
    testobj.set_title()
    assert capsys.readouterr().out == ("called HotkeyPanelGui.set_title with arg 'xxxx'\n")
    testobj.modified = False
    testobj.set_title(modified=True)
    assert capsys.readouterr().out == ("called HotkeyPanelGui.set_title with arg 'xxxx (*)'\n")
    testobj.modified = True
    testobj.set_title(modified=False)
    assert capsys.readouterr().out == ("called HotkeyPanelGui.set_title with arg 'xxxx'\n")

def test_hotkeypanel_exit(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.exit
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
    testobj = setup_hotkeypanel(monkeypatch, capsys)
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

def test_hotkeypanel_on_text(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.on_text
    """
    def mock_get(*args):
        print("called HotkeyPanelGui.get_widget_text with args", args)
        return 'snark'
    def mock_enable(state):
        print(f'called HotkeyPanelGui.enable_save with arg {state}')
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.gui.get_widget_text = mock_get
    testobj.gui.enable_save = mock_enable
    testobj.field_indexes = {'C_KEY': 1}
    testobj._origdata = ['', 'snork']
    testobj._newdata = ['', '']
    testobj.initializing_screen = True
    testobj.fields = []
    testobj.defchanged = True
    testobj.on_text('x')
    assert testobj.defchanged
    assert capsys.readouterr().out == ""
    testobj.initializing_screen = False
    testobj.defchanged = True
    testobj.on_text('xx')
    assert not testobj.defchanged
    assert testobj._newdata == ['', '']
    assert capsys.readouterr().out == "called HotkeyPanelGui.get_widget_text with args ('xx',)\n"
    testobj.fields = ['C_KEY']
    # breakpoint()
    testobj.on_text('xx')
    assert testobj.defchanged
    assert testobj._newdata == ['', 'snark']
    assert capsys.readouterr().out == ("called HotkeyPanelGui.get_widget_text with args ('xx',)\n"
                                       "called HotkeyPanelGui.enable_save with arg True\n")
    testobj._origdata = ['', 'snark']
    testobj._newdata = ['', '']
    testobj.on_text('xx')
    assert not testobj.defchanged
    assert testobj._newdata == ['', '']
    assert capsys.readouterr().out == ("called HotkeyPanelGui.get_widget_text with args ('xx',)\n"
                                       "called HotkeyPanelGui.enable_save with arg False\n")

def test_hotkeypanel_on_combobox(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.on_combobox
    """
    def mock_set(value):
        print(f'called HotkeyPanel.set_changed_indicators with arg {value}')
    def mock_adjust(*args):
        print('called HotkeyPanel.adjust_other_fields_if_needed with args', args)
    def mock_reset(value):
        print(f'called HotkeyPanel.reset_changed_indicators_if_needed with arg {value}')
    def mock_get_value(*args):
        print('called SingleDataInterface.get_choice_value with args', args)
        return args[0], 'abcdef'
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.gui.cmb_key = types.SimpleNamespace(name='C_KEY')
    testobj.gui.cmb_commando = types.SimpleNamespace(name='C_CMD')
    testobj.gui.cmb_context = types.SimpleNamespace(name='C_CNTXT')
    testobj.gui.cmb_controls = types.SimpleNamespace(name='C_CTRL')
    testobj.gui.get_choice_value = mock_get_value
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
    assert capsys.readouterr().out == (
        "called SingleDataInterface.get_choice_value with args ('None',)\n")

    testobj.on_combobox(testobj.gui.cmb_key)
    assert testobj._newdata == ['abcdef', '', '', '']
    assert capsys.readouterr().out == (
        f"called SingleDataInterface.get_choice_value with args ({testobj.gui.cmb_key},)\n"
        f"called HotkeyPanel.adjust_other_fields_if_needed with args ({testobj.gui.cmb_key},"
        " 'abcdef')\n"
        "called HotkeyPanel.set_changed_indicators with arg True\n")
    testobj._newdata = ['', '', '', '']
    testobj.on_combobox(testobj.gui.cmb_context)
    assert testobj._newdata == ['', 'abcdef', '', '']
    assert capsys.readouterr().out == (
        f"called SingleDataInterface.get_choice_value with args ({testobj.gui.cmb_context},)\n"
        f"called HotkeyPanel.adjust_other_fields_if_needed with args ({testobj.gui.cmb_context},"
        " 'abcdef')\n"
        "called HotkeyPanel.set_changed_indicators with arg True\n")
    testobj._newdata = ['', '', '', '']
    testobj.on_combobox(testobj.gui.cmb_commando)
    assert testobj._newdata == ['', '', 'abcdef', '']
    assert capsys.readouterr().out == (
        f"called SingleDataInterface.get_choice_value with args ({testobj.gui.cmb_commando},)\n"
        f"called HotkeyPanel.adjust_other_fields_if_needed with args ({testobj.gui.cmb_commando},"
        " 'abcdef')\n"
        "called HotkeyPanel.set_changed_indicators with arg True\n")
    testobj._newdata = ['', '', '', '']
    testobj.on_combobox(testobj.gui.cmb_controls)
    assert testobj._newdata == ['', '', '', 'abcdef']
    assert capsys.readouterr().out == (
        f"called SingleDataInterface.get_choice_value with args ({testobj.gui.cmb_controls},)\n"
        f"called HotkeyPanel.adjust_other_fields_if_needed with args ({testobj.gui.cmb_controls},"
        " 'abcdef')\n"
        "called HotkeyPanel.set_changed_indicators with arg True\n")
    testobj._origdata = ['', '', '', 'abcdef']
    # breakpoint()
    testobj.on_combobox(testobj.gui.cmb_controls)
    assert capsys.readouterr().out == (
        f"called SingleDataInterface.get_choice_value with args ({testobj.gui.cmb_controls},)\n"
        "called HotkeyPanel.reset_changed_indicators_if_needed with arg namespace(name='C_CTRL')\n")

def test_hotkeypanel_adjust_other_fields_if_needed(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.adjust_other_fields_if_needed
    """
    def mock_init(*args):
        print('called SingleDataInterface.init_combobox with args', args)
    def mock_set(*args):
        print('called SingleDataInterface.set_textbox_value with args', args)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.gui.init_combobox = mock_init
    testobj.gui.set_textfield_value = mock_set
    testobj.captions = {'M_NODESC': 'no desc'}
    testobj.adjust_other_fields_if_needed("", '')
    assert capsys.readouterr().out == ("")
    testobj.gui.cmb_context = types.SimpleNamespace(name='C_CNTXT')
    testobj.adjust_other_fields_if_needed(testobj.gui.cmb_context, '')
    assert capsys.readouterr().out == ("")
    testobj.contextactionsdict = {}
    testobj.adjust_other_fields_if_needed(testobj.gui.cmb_context, '')
    assert capsys.readouterr().out == ("")
    testobj.commandslist = ['xx']
    testobj.adjust_other_fields_if_needed(testobj.gui.cmb_context, '')
    assert capsys.readouterr().out == ("")
    testobj.gui.cmb_commando = types.SimpleNamespace(name='C_CMD')
    testobj.adjust_other_fields_if_needed(testobj.gui.cmb_context, '')
    assert capsys.readouterr().out == ("called SingleDataInterface.init_combobox with args"
                                       " (namespace(name='C_CMD'), ['xx'])\n")
    testobj.contextactionsdict = {'yy': ['zz']}
    testobj.adjust_other_fields_if_needed(testobj.gui.cmb_context, 'yy')
    assert capsys.readouterr().out == ("called SingleDataInterface.init_combobox with args"
                                       " (namespace(name='C_CMD'), ['zz'])\n")
    testobj.descriptions = {}
    testobj.adjust_other_fields_if_needed(testobj.gui.cmb_commando, '')
    assert capsys.readouterr().out == ("")
    testobj.gui.txt_oms = types.SimpleNamespace(name='C_TEXT')
    testobj.adjust_other_fields_if_needed(testobj.gui.cmb_commando, '')
    assert capsys.readouterr().out == ("called SingleDataInterface.set_textbox_value with args"
                                       " (namespace(name='C_TEXT'), 'no desc')\n")
    testobj.descriptions = {'qq': 'rrrr'}
    testobj.adjust_other_fields_if_needed(testobj.gui.cmb_commando, 'qq')
    assert capsys.readouterr().out == ("called SingleDataInterface.set_textbox_value with args"
                                       " (namespace(name='C_TEXT'), 'rrrr')\n")

def test_hotkeypanel_reset_changed_indicators_if_needed(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.reset_changed_indicators_if_needed
    """
    def mock_get(arg):
        print('called SingleDataInterface.get_combobox_value with arg', arg)
        return arg.name
    def mock_set(arg):
        print('called SingleDataInterface.set_changed_indicators with arg', arg)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.gui.get_combobox_value = mock_get
    testobj.set_changed_indicators = mock_set
    testobj.field_indexes = {'C_KEY': 3, 'C_CMD': 2}
    testobj._origdata = ['1', '2', '3', '4']
    testobj.reset_changed_indicators_if_needed("")
    assert capsys.readouterr().out == ("")
    testobj.gui.cmb_commando = types.SimpleNamespace(name='C_CMD')
    testobj.reset_changed_indicators_if_needed("")
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_combobox_value with arg namespace(name='C_CMD')\n")
    testobj.gui.cmb_key = types.SimpleNamespace(name='C_KEY')
    testobj.reset_changed_indicators_if_needed("")
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_combobox_value with arg namespace(name='C_CMD')\n")
    testobj.reset_changed_indicators_if_needed(testobj.gui.cmb_commando)
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_combobox_value with arg namespace(name='C_KEY')\n")
    testobj.reset_changed_indicators_if_needed(testobj.gui.cmb_key)
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_combobox_value with arg namespace(name='C_CMD')\n")
    testobj._origdata = ['1', '2', 'C_CMD', 'C_KEY']
    testobj.reset_changed_indicators_if_needed(testobj.gui.cmb_commando)
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_combobox_value with arg namespace(name='C_KEY')\n"
            "called SingleDataInterface.set_changed_indicators with arg False\n")
    testobj.reset_changed_indicators_if_needed(testobj.gui.cmb_key)
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_combobox_value with arg namespace(name='C_CMD')\n"
            "called SingleDataInterface.set_changed_indicators with arg False\n")


def test_hotkeypanel_set_changed_indicators(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.set_changed_indicators
    """
    def mock_enable(value):
        print(f"called HotkeyPanelGui.enable_save with arg '{value}')")
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.gui.enable_save = mock_enable
    testobj.defchanged = False
    testobj.fields = []
    testobj.set_changed_indicators(True)
    assert testobj.defchanged
    assert capsys.readouterr().out == ""
    testobj.defchanged = True
    testobj.fields = ['C_CMD']
    testobj.set_changed_indicators(False)
    assert not testobj.defchanged
    assert capsys.readouterr().out == "called HotkeyPanelGui.enable_save with arg 'False')\n"

def test_hotkeypanel_on_checkbox(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.on_checkbox
    """
    def mock_set(value):
        print(f'called HotkeyPanel.set_changed_indicators with arg {value}')
    def mock_get_value(*args):
        print('called SingleDataInterface.get_check_value with args', args)
        return 'qqq', True
    def mock_get_state(cb):
        print(f'called SingleDataInterface.get_check_state with arg {cb}')
        return True
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.set_changed_indicators = mock_set
    testobj.field_indexes = {'C_MODS': [0, 1, 2, 3]}
    testobj.gui.get_check_value = mock_get_value
    testobj.gui.get_checkbox_state = mock_get_state
    testobj.gui.cb_shift = 'xxx'
    testobj.gui.cb_ctrl = 'yyy'
    testobj.gui.cb_alt = 'zzz'
    testobj.gui.cb_win = 'qqq'
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

def test_hotkeypanel_refresh_extrascreen(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.refresh_extrascreen
    """
    def mock_get(arg):
        print(f"called SingleDataInterface.get_itemdata with arg '{arg}'")
        return '1'
    def mock_get_list(arg):
        print(f"called SingleDataInterface.get_valuelist with arg '{arg}'")
        return ['value', 'list']
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.fields = []
    testobj.data = {'1': []}
    testobj.init_origdata = ['', False, False, False, False, '', '', '', '', '', '', '']
    testobj.field_indexes = {'C_KEY': 0, 'C_MODS': [1, 2, 3, 4], 'C_CNTXT': 5, 'C_CMD': 6,
                             'C_PARMS': 7, 'C_CTRL': 8, 'C_BPARMS': 9, 'C_APARMS': 10, 'C_FEAT': 11}
    testobj.get_valuelist = mock_get_list
    testobj.gui.get_itemdata = mock_get
    testobj.gui.cmb_key = 'key'

    testobj.refresh_extrascreen('')
    assert not hasattr(testobj, '_origdata')
    assert capsys.readouterr().out == ""
    testobj.refresh_extrascreen('selitem')
    assert testobj._origdata == testobj.init_origdata
    assert capsys.readouterr().out == "called SingleDataInterface.get_itemdata with arg 'selitem'\n"
    testobj.fields = ['C_KEY', 'C_MODS', 'C_TYPE']
    testobj.data = {'1': ['X', 'CWAS', 'S']}
    testobj.settings = {testee.shared.SettType.RDEF.value: 0}
    testobj.keylist = None
    testobj.gui.txt_key = 'key text'
    testobj.refresh_extrascreen('selitem')
    assert testobj._origdata == ['X', False, False, False, False, '', '', '', '', '', '', '']
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_itemdata with arg 'selitem'\n"
            "called SingleDataInterface.set_textfield_value with args ('key text', 'X')\n")
    testobj.data = {'1': ['X', 'ACS', 'S']}
    testobj.gui.cb_shift = ' with shift'
    testobj.gui.cb_ctrl = ' with ctrl'
    testobj.gui.cb_alt = ' with alt'
    testobj.gui.cb_win = ' with win'
    testobj.settings = {testee.shared.SettType.RDEF.value: 1}
    testobj.keylist = ['a', 'b', 'c']
    testobj.refresh_extrascreen('selitem')
    assert testobj._origdata == ['X', True, True, True, False, '', '', '', '', '', '', '']
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_itemdata with arg 'selitem'\n"
            "called SingleDataInterface.enable_delete with arg False\n"
            "called SingleDataInterface.set_checkbox_state with args (' with shift', True)\n"
            "called SingleDataInterface.set_checkbox_state with args (' with ctrl', True)\n"
            "called SingleDataInterface.set_checkbox_state with args (' with alt', True)\n"
            "called SingleDataInterface.set_checkbox_state with args (' with win', False)\n"
            "called SingleDataInterface.get_valuelist with arg 'C_KEY'\n"
            "called SingleDataInterface.set_combobox_string with args"
            " ('key', 'X', ['value', 'list'])\n")
    testobj.fields = ['C_KEY', 'C_TYPE', 'C_CNTXT', 'C_CMD', 'C_DESC', 'C_PARMS', 'C_CTRL',
                      'C_BPARMS', 'C_APARMS', 'C_FEAT']
    testobj.data = {'1': ['X', 'U', 'xx', 'yy', 'zz', 'aa', 'bb', 'cc', 'dd', 'ee']}
    # breakpoint()
    testobj.refresh_extrascreen('selitem')
    assert testobj._origdata == ['X', False, False, False, False, '', '', '', '', '', '', '']
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_itemdata with arg 'selitem'\n"
            "called SingleDataInterface.enable_save with arg False\n"
            "called SingleDataInterface.enable_delete with arg False\n"
            "called SingleDataInterface.enable_delete with arg True\n"
            "called SingleDataInterface.get_valuelist with arg 'C_KEY'\n"
            "called SingleDataInterface.set_combobox_string with args"
            " ('key', 'X', ['value', 'list'])\n"
            "C_CNTXT aanwezig in fields zonder corresponderend veld op scherm\n"
            "C_CMD aanwezig in fields zonder corresponderend veld op scherm\n"
            "C_DESC aanwezig in fields zonder corresponderend veld op scherm\n"
            "C_PARMS aanwezig in fields zonder corresponderend veld op scherm\n"
            "C_CTRL aanwezig in fields zonder corresponderend veld op scherm\n"
            "C_BPARMS aanwezig in fields zonder corresponderend veld op scherm\n"
            "C_APARMS aanwezig in fields zonder corresponderend veld op scherm\n"
            "C_FEAT aanwezig in fields zonder corresponderend veld op scherm\n")
    testobj.gui.cmb_context = 'context'
    testobj.gui.cmb_commando = 'command'
    testobj.gui.txt_oms = 'desc'
    testobj.gui.txt_parms = 'parms'
    testobj.gui.cmb_controls = 'controls'
    testobj.gui.pre_parms_text = 'pre-args'
    testobj.gui.post_parms_text = 'post-args'
    testobj.gui.feature_select = 'feature'
    testobj.refresh_extrascreen('selitem')
    assert testobj._origdata == ['X', False, False, False, False, 'xx', 'yy', 'aa', 'bb', 'cc',
                                 'dd', 'ee']
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_itemdata with arg 'selitem'\n"
            "called SingleDataInterface.enable_save with arg False\n"
            "called SingleDataInterface.enable_delete with arg False\n"
            "called SingleDataInterface.enable_delete with arg True\n"
            "called SingleDataInterface.get_valuelist with arg 'C_KEY'\n"
            "called SingleDataInterface.set_combobox_string with args"
            " ('key', 'X', ['value', 'list'])\n"
            "called SingleDataInterface.get_valuelist with arg 'C_CNTXT'\n"
            "called SingleDataInterface.set_combobox_string with args"
            " ('context', 'xx', ['value', 'list'])\n"
            "called SingleDataInterface.get_valuelist with arg 'C_CMD'\n"
            "called SingleDataInterface.set_combobox_string with args"
            " ('command', 'yy', ['value', 'list'])\n"
            "called SingleDataInterface.set_textfield_value with args ('desc', 'zz')\n"
            "called SingleDataInterface.set_textfield_value with args ('parms', 'aa')\n"
            "called SingleDataInterface.get_valuelist with arg 'C_CTRL'\n"
            "called SingleDataInterface.set_combobox_string with args"
            " ('controls', 'bb', ['value', 'list'])\n"
            "called SingleDataInterface.set_textfield_value with args ('pre-args', 'cc')\n"
            "called SingleDataInterface.set_textfield_value with args ('post-args', 'dd')\n"
            "called SingleDataInterface.get_valuelist with arg 'C_FEAT'\n"
            "called SingleDataInterface.set_combobox_string with args"
            " ('feature', 'ee', ['value', 'list'])\n")

def test_hotkeypanel_get_valuelist(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.get_valuelist
    """
    def mock_init(*args):
        print('called HotkeyPanelGui.init_combobox with arg', args)
    def mock_get(arg):
        print(f"called HotkeyPanelGui.get_combobox_selection with arg '{arg}'")
        return 'xxx'
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.keylist = ['a']
    testobj.contextslist = ['b']
    testobj.fields = ['C_CNTXT']
    testobj.contextactionsdict = {'xxx': ['c']}
    testobj.commandslist = ['d']
    testobj.controlslist = ['e']
    testobj.featurelist = ['f']
    testobj.gui.cmb_commando = 'xx'
    testobj.gui.init_combobox = mock_init
    testobj.gui.cmb_context = 'yy'
    testobj.gui.get_combobox_selection = mock_get

    assert testobj.get_valuelist('xx') == []
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_KEY') == ['a']
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_CNTXT') == ['b']
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_CMD') == ['c']
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.init_combobox with arg ('xx',)\n"
            "called HotkeyPanelGui.get_combobox_selection with arg 'yy'\n"
            "called HotkeyPanelGui.init_combobox with arg ('xx', ['c'])\n")
    testobj.contextactionsdict = {}
    assert testobj.get_valuelist('C_CMD') == ['d']
    assert capsys.readouterr().out == (
            "called HotkeyPanelGui.init_combobox with arg ('xx',)\n"
            "called HotkeyPanelGui.get_combobox_selection with arg 'yy'\n"
            "called HotkeyPanelGui.init_combobox with arg ('xx', ['d'])\n")
    testobj.fields = []
    assert testobj.get_valuelist('C_CMD') == ['d']
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_CTRL') == ['e']
    assert capsys.readouterr().out == ""
    assert testobj.get_valuelist('C_FEAT') == ['f']
    assert capsys.readouterr().out == ""

def test_hotkeypanel_process_changed_selection(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.process_changed_selection
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
    def mock_get():
        print("called HotKeyPanel.get_selected_keydef")
        return 'item b'
    def mock_refresh(arg):
        print(f"called HotKeyPanel.refresh_extrascreen with arg '{arg}'")
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.check_for_changes = mock_check
    testobj.check_for_selected_keydef = mock_check_keydef
    testobj.ask_what_to_do = mock_ask
    testobj.apply_changes = mock_apply
    testobj.gui.get_selected_keydef = mock_get
    testobj.refresh_extrascreen = mock_refresh
    testobj.settings = {testee.shared.SettType.RDEF.value: '0'}
    testobj.initializing_screen = True
    testobj.process_changed_selection('newitem', 'olditem')
    assert capsys.readouterr().out == ("called HotKeyPanel.get_selected_keydef\n"
                                       "called HotKeyPanel.refresh_extrascreen with arg 'item b'\n")
    testobj.settings = {testee.shared.SettType.RDEF.value: '1'}
    testobj.process_changed_selection('newitem', 'olditem')
    assert capsys.readouterr().out == "called HotKeyPanel.refresh_extrascreen with arg 'newitem'\n"
    testobj.initializing_screen = False
    testobj.process_changed_selection('newitem', 'olditem')
    assert capsys.readouterr().out == (
            "called HotKeyPanel.check_for_changes\n"
            "called HotKeyPanel.check_for_selected_keydef with arg 'yyy'\n"
            "called HotKeyPanel.ask_what_to_do with args (True, 'newitem', 'olditem')\n"
            "called HotKeyPanel.refresh_extrascreen with arg 'newitem'\n")
    testobj.ask_what_to_do = mock_ask_2
    testobj.process_changed_selection('newitem', 'olditem')
    assert capsys.readouterr().out == (
            "called HotKeyPanel.check_for_changes\n"
            "called HotKeyPanel.check_for_selected_keydef with arg 'yyy'\n"
            "called HotKeyPanel.ask_what_to_do with args (True, 'newitem', 'olditem')\n"
            "called HotKeyPanel.apply_changes with args (True, 1, 'yyy')\n"
            "called HotKeyPanel.refresh_extrascreen with arg 'item a'\n")

def test_hotkeypanel_check_for_changes(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.check_for_changes
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.field_indexes = {'C_KEY': 0, 'C_MODS': [1, 2, 3, 4], 'C_CNTXT': 5}
    testobj._origdata = ['x', True, False, True, False, 'zzz']
    testobj._newdata = ['x', True, False, True, False, 'zzz']
    assert testobj.check_for_changes() == ([False, False, False],
                                           ['x', [True, False, True, False], 'zzz'])
    testobj._newdata = ['y', False, True, False, True, 'zzzz']
    assert testobj.check_for_changes() == ([True, True, True],
                                           ['y', [False, True, False, True], 'zzzz'])

def test_hotkeypanel_check_for_selected_keydef(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.check_for_selected_keydef
    """
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.fields = ['C_KEY', 'C_MODS', 'C_CNTXT']
    testobj.data = {1: ['x', 'y', 'z', 'aaaaaaa'], 2: ['p', 'q', 'r', 'bbbbbb']}
    assert testobj.check_for_selected_keydef(['x', 'y', 'z']) == (True, 1)
    assert testobj.check_for_selected_keydef(['k', 'l', 'm']) == (False, -1)

def test_hotkeypanel_ask_what_to_do(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.ask_what_to_do
    """
    def mock_ask(*args):
        print('called gui.ask_question with args', args)
        return 'answered'
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
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

def test_hotkeypanel_apply_changes(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.apply_changes
    """
    def mock_get_sel():
        print('called SingleDataInterface.get_selected_keydef')
        return 'keydef X'
    def mock_get_pos(item):
        print(f"called SingleDataInterface.get_keydef_position with arg '{item}'")
        return 'position of keydef X'
    def mock_get_at(pos):
        print(f"called SingleDataInterface.get_keydef_at_position with arg '{pos}'")
        return 'item at position'
    def mock_populate(pos):
        print(f"called HotkeyPanel.populate_list with arg '{pos}'")
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.gui.get_selected_keydef = mock_get_sel
    testobj.gui.get_keydef_position = mock_get_pos
    testobj.gui.get_keydef_at_position = mock_get_at
    testobj.populate_list = mock_populate
    testobj.fields = [('C_KEY', 10, 'x'), ('C_MODS', 4, 'y'), ('C_CMD', 12, 'z')]
    testobj.field_indexes = {'C_KEY': 0, 'C_MODS': 1, 'C_CMD': 2}
    testobj.data = {1: ['x', 'y', 'z'], 2: ['a', 'b', 'c']}
    testobj._newdata = ['ppp', 'qqq', 'rrr']
    assert testobj.apply_changes(True, 1, (0, 'WASD')) == 'item at position'
    assert testobj.data == {1: ['ppp', 'WASD', 'rrr'], 2: ['a', 'b', 'c']}
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_selected_keydef\n"
            "called SingleDataInterface.get_keydef_position with arg 'keydef X'\n"
            "called SingleDataInterface.get_keydef_at_position with arg 'position of keydef X'\n"
            "called HotkeyPanel.populate_list with arg 'position of keydef X'\n")
    testobj.data = {1: ['x', 'y', 'z'], 2: ['a', 'b', 'c']}
    assert testobj.apply_changes(False, 1, (0, 'WASD')) == 'item at position'
    assert testobj.data == {0: ['a', 'b', 'c'], 1: ['ppp', 'qqq', 'rrr'], 2: ['x', 'y', 'z']}
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_selected_keydef\n"
            "called SingleDataInterface.get_keydef_position with arg 'keydef X'\n"
            "called SingleDataInterface.get_keydef_at_position with arg 'position of keydef X'\n"
            "called HotkeyPanel.populate_list with arg 'position of keydef X'\n")
    testobj.data = {1: ['x', 'y', 'z'], 2: ['a', 'b', 'c']}

def test_hotkeypanel_apply_deletion(monkeypatch, capsys):
    """unittest for main.HotkeyPanel.apply_deletion
    """
    def mock_show(*args, **kwargs):
        print('called gui.show_message with args', args, kwargs)
    def mock_get_sel():
        print('called SingleDataInterface.get_selected_keydef')
        return 'keydef X'
    def mock_get_pos(item):
        print(f"called SingleDataInterface.get_keydef_position with arg '{item}'")
        return 'position of keydef X'
    def mock_get_itemdata(item):
        print(f"called SingleDataInterface.get_itemdata with arg '{item}'")
        return 1
    def mock_set_title(**kwargs):
        print("called HotkeyPanel.set_title with args", kwargs)
    def mock_populate_list(self, **kwargs):
        print("called HotkeyPanel.populate_list with args", kwargs)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    testobj = setup_hotkeypanel(monkeypatch, capsys)
    testobj.gui.get_selected_keydef = mock_get_sel
    testobj.gui.get_keydef_position = mock_get_pos
    testobj.gui.get_itemdata = mock_get_itemdata
    testobj.set_title = mock_set_title
    testobj.populate_list = mock_populate_list
    testobj.defkeys = {'key': 'orig'}
    testobj.omsdict = {'orig': 'original'}
    testobj.captions = {'001': 'C_TYPE'}
    testobj.data = {1: ['key', 'S']}
    testobj.apply_deletion()
    assert testobj.data == {1: ['key', 'S']}
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_selected_keydef\n"
            "called SingleDataInterface.get_keydef_position with arg 'keydef X'\n"
            "called SingleDataInterface.get_itemdata with arg 'keydef X'\n"
            f"called gui.show_message with args ({testobj.parent}, 'I_STDDEF') {{}}\n")
    testobj.captions = {'001': 'C_KEY'}
    testobj.data = {1: ['key', 'U']}
    testobj.apply_deletion()
    assert testobj.data == {1: ('key', 'S', 'orig', 'original')}
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_selected_keydef\n"
            "called SingleDataInterface.get_keydef_position with arg 'keydef X'\n"
            "called SingleDataInterface.get_itemdata with arg 'keydef X'\n"
            "called SingleDataInterface.enable_save with arg False\n"
            "called SingleDataInterface.enable_delete with arg False\n"
            "called HotkeyPanel.set_title with args {'modified': True}\n"
            "called HotkeyPanel.populate_list with args {}\n")
    testobj.omsdict = {}
    testobj.data = {1: ['key', 'U']}
    testobj.apply_deletion()
    assert testobj.data == {1: ('key', 'S', '', 'orig')}
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_selected_keydef\n"
            "called SingleDataInterface.get_keydef_position with arg 'keydef X'\n"
            "called SingleDataInterface.get_itemdata with arg 'keydef X'\n"
            "called SingleDataInterface.enable_save with arg False\n"
            "called SingleDataInterface.enable_delete with arg False\n"
            "called HotkeyPanel.set_title with args {'modified': True}\n"
            "called HotkeyPanel.populate_list with args {}\n")
    testobj.defkeys = {}
    testobj.data = {1: ['key', 'U']}
    testobj.apply_deletion()
    assert testobj.data == {}
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_selected_keydef\n"
            "called SingleDataInterface.get_keydef_position with arg 'keydef X'\n"
            "called SingleDataInterface.get_itemdata with arg 'keydef X'\n"
            "called SingleDataInterface.enable_save with arg False\n"
            "called SingleDataInterface.enable_delete with arg False\n"
            "called HotkeyPanel.set_title with args {'modified': True}\n"
            "called HotkeyPanel.populate_list with args {}\n")
    testobj.captions = {'001': 'C_KY'}
    testobj.data = {1: ['key', 'U']}
    testobj.apply_deletion()
    assert testobj.data == {1: ['key', 'U']}
    assert capsys.readouterr().out == (
            "called SingleDataInterface.get_selected_keydef\n"
            "called SingleDataInterface.get_keydef_position with arg 'keydef X'\n"
            "called SingleDataInterface.get_itemdata with arg 'keydef X'\n"
            "called SingleDataInterface.enable_save with arg False\n"
            "called SingleDataInterface.enable_delete with arg False\n"
            "called HotkeyPanel.set_title with args {'modified': True}\n"
            "called HotkeyPanel.populate_list with args {}\n")


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
    def setup_selector(self):
        """stub
        """
        print('called TabbedInterface.setup_selector')
    def clear_selector(self):
        """stub
        """
        print('called TabbedInterface.clear_selector')
    def setup_search(self):
        """stub
        """
        print('called TabbedInterface.setup_search')
    def add_subscreen(self, win):
        """stub
        """
        print(f'called TabbedInterface.add_subscreen with arg of type {type(win)}')
    def add_to_selector(self, txt):
        """stub
        """
        print(f"called TabbedInterface.add_to_selector with arg '{txt}'")
    def format_screen(self):
        """stub
        """
        print("called TabbedInterface.format_screen")
    def update_search(self, arg):
        """stub
        """
        print("called TabbedInterface.update_search with arg", arg)
    def init_search_buttons(self):
        """stub
        """
        print("called TabbedInterface.init_search_buttons")
    def set_selected_tool(self, arg):
        """stub
        """
        print(f"called TabbedInterface.set_selected_tool with arg '{arg}'")
    def set_selected_panel(self, *args):
        """stub
        """
        print("called TabbedInterface.set_selected_panel with args", args)
    def set_selected_keydef_item(self, *args):
        """stub
        """
        print("called TabbedInterface.set_selected_keydef_item with args", args)
    def enable_search_buttons(self, **kwargs):
        """stub
        """
        print("called TabbedInterface.enable_search_buttons with args", kwargs)
    def enable_search_text(self, state):
        """stub
        """
        print(f"called TabbedInterface.enable_search_text with arg {state}")
    def set_found_keydef_position(self, *args):
        """stub
        """
        print("called TabbedInterface.set_found_keydef_position with args", args)
    def set_filter_state_text(self, text):
        """stub
        """
        print(f"called TabbedInterface.set_filter_state_text with arg {text}")
    def get_selected_index(self):
        """stub
        """
        print('called TabbedInterface.get_selected_index')
        return 2
    def get_new_selection(self, arg):
        """stub
        """
        print(f"called TabbedInterface.get_new_selection with arg '{arg}'")
        return 1
    def remove_tool(self, *args):
        """stub
        """
        print('called TabbedInterface.remove_tool with args', args)
        self._removecounter += 1
        if self._removecounter % 2 == 0:
            return None
        return f'item #{self._removecounter}'
    def add_tool(self, *args):
        """stub
        """
        print('called TabbedInterface.add_tool with args', args)
    def refresh_locs(self, headers):
        """stub
        """
        print(f"called TabbedInterface.refresh_locs with arg '{headers}'")


class MockHotkeyPanel:
    """stub for main.HotkeyPanel
    """
    def __init__(self, *args):
        print('called HotkeyPanel.__init__ with args', args)
        self.settings = {}
        self.gui = 'HotkeyPanelGui'
        self._name = args[1]
        if testee.os.path.basename(args[1]) == 'itsnotthere':
            self.settings[testee.shared.SettType.PLG.value] = 'xxx'
    def __repr__(self):
        """stub
        """
        return f"<HotkeyPanel '{self._name}'>"
    def readkeys(self):
        """stub
        """
        print('called HotkeyPanel.readkeys')
    def populate_list(self):
        """stub
        """
        print('called HotkeyPanel.populate_list')
    def setcaptions(self):
        """stub
        """
        print('called HotkeyPanel.setcaptions')
    def set_title(self):
        """stub
        """
        print('called HotkeyPanel.set_title')


def test_choicebook_init(monkeypatch, capsys, tmp_path):
    """unittest for main.ChoiceBook.init
    """
    def mock_log():
        print('called shared.log_exc')
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log)
    plgfile = tmp_path / 'isthere'
    plgfile.touch()
    monkeypatch.setattr(testee.gui, 'TabbedInterface', MockTabGui)
    monkeypatch.setattr(testee, 'HotkeyPanel', MockHotkeyPanel)
    parent = MockEditor()
    parent.ini = {'plugins': [('xxx', str(plgfile)), ('yyy', 'itsnotthere')]}
    # breakpoint()
    testobj = testee.ChoiceBook(parent)
    assert testobj.parent == parent
    assert testobj.page is None
    assert isinstance(testobj.gui, testee.gui.TabbedInterface)
    assert testobj.parent.pluginfiles == {'xxx': '', 'yyy': 'xxx'}
    assert capsys.readouterr().out == (
            "called Editor.__init__\n"
            f"called TabbedInterface.__init__ with args ({testobj.parent.gui}, {testobj})\n"
            "called TabbedInterface.setup_selector\n"
            "called TabbedInterface.setup_search\n"
            f"called HotkeyPanel.__init__ with args ({testobj}, '{plgfile}')\n"
            "called TabbedInterface.add_subscreen with arg of type"
            " <class 'test_main.MockHotkeyPanel'>\n"
            "called shared.log_exc\n"
            "called TabbedInterface.add_to_selector with arg 'xxx'\n"
            f"called HotkeyPanel.__init__ with args ({testobj}, '{testee.BASE}/itsnotthere')\n"
            "called TabbedInterface.add_subscreen with arg of type"
            " <class 'test_main.MockHotkeyPanel'>\n"
            "called TabbedInterface.add_to_selector with arg 'yyy'\n"
            "called TabbedInterface.format_screen\n")

def setup_choicebook(monkeypatch, capsys):
    """stub for main.Editor.book
    """
    def mock_init(self):
        print('called ChoiceBook.__init__')
    monkeypatch.setattr(testee.ChoiceBook, '__init__', mock_init)
    testobj = testee.ChoiceBook()
    testobj.parent = MockEditor()
    testobj.gui = MockTabGui()
    assert capsys.readouterr().out == ('called ChoiceBook.__init__\n'
                                       "called Editor.__init__\n"
                                       "called TabbedInterface.__init__ with args ()\n")
    return testobj

def test_choicebook_on_page_changed(monkeypatch, capsys):
    """unittest for main.ChoiceBook.on_page_changed
    """
    win = MockSDI()
    assert capsys.readouterr().out == 'called SingleDataInterface.__init__ with args ()\n'
    def mock_get():
        print('called TabbedInterface.get_panel')
        return None
    def mock_get_2():
        print('called TabbedInterface.get_panel')
        return win
    def mock_exit():
        print('called SingleDataInterface.exit')
        return False
    def mock_exit_2():
        print('called SingleDataInterface.exit')
        return True
    def mock_get_tool():
        print('called TabbedInterface.get_selected_tool')
        return 'xxx'
    def mock_setup():
        print('called EditorGui.setup_menu')
    win.master = MockHotkeyPanel('testobj', '')
    assert capsys.readouterr().out == "called HotkeyPanel.__init__ with args ('testobj', '')\n"
    win.master.modified = True
    win.master.column_info = [('x', 1)]
    win.master.data = {1: 'y'}
    win.exit = mock_exit
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.parent.captions = {'M_DESC': "it's {}", 'x': 'column'}
    testobj.gui.get_selected_tool = mock_get_tool
    testobj.gui.get_panel = mock_get
    testobj.parent.gui.setup_menu = mock_setup

    testobj.parent.book = None
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == ""

    testobj.parent.book = testobj
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == "called TabbedInterface.get_panel\n"

    testobj.gui.get_panel = mock_get_2
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == ("called TabbedInterface.get_panel\n"
                                       "called SingleDataInterface.exit\n")

    win.exit = mock_exit_2
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_panel\n"
            "called SingleDataInterface.exit\n"
            "called TabbedInterface.get_selected_tool\n"
            "called EditorGui.statusbar_message with arg 'it's xxx'\n"
            "called TabbedInterface.set_selected_panel with args (1,)\n"
            "called TabbedInterface.get_panel\n"
            "called EditorGui.setup_menu\n")

    win.master.settings = {'a': 'b'}
    testobj.on_page_changed(1)
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_panel\n"
            "called SingleDataInterface.exit\n"
            "called TabbedInterface.get_selected_tool\n"
            "called EditorGui.statusbar_message with arg 'it's xxx'\n"
            "called TabbedInterface.set_selected_panel with args (1,)\n"
            "called TabbedInterface.get_panel\n"
            "called EditorGui.setup_menu\n"
            "called HotkeyPanel.setcaptions\n"
            "called TabbedInterface.update_search with arg ['column']\n")

def test_choicebook_on_text_changed(monkeypatch, capsys):
    """unittest for main.ChoiceBook.on_text_changed
    """
    def mock_get():
        print("called TabbedInterface.get_search_col")
        return "yyy"
    def mock_find(*args):
        print("called TabbedInterface.find_items with args", args)
        return []
    def mock_find_2(*args):
        print("called TabbedInterface.find_items with args", args)
        return ['item-1', 'item-2']
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.parent.captions = {"I_#FOUND": "{} found", "I_NOTFND": "no {}"}
    testobj.page = MockHotkeyPanel(testobj, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
    testobj.page.column_info = [('x', 0), ('y', 1)]
    testobj.page.captions = {'x': 'xxx', 'y': 'yyy'}
    testobj.page.data = {1: 'a', 2: 'b'}
    testobj.gui.get_search_col = mock_get
    testobj.gui.find_items = mock_find
    testobj.on_text_changed('qq')
    assert testobj.zoekcol == 1
    assert testobj.items_found == []
    assert not hasattr(testobj, 'founditem')
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_search_col\n"
            "called TabbedInterface.get_search_col\n"
            f"called TabbedInterface.find_items with args ({testobj.page}, 'qq')\n"
            "called TabbedInterface.init_search_buttons\n"
            "called EditorGui.statusbar_message with arg 'no qq'\n")

    testobj.gui.find_items = mock_find_2
    testobj.on_text_changed('qq')
    assert testobj.zoekcol == 1
    assert testobj.items_found == ['item-1', 'item-2']
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_search_col\n"
            "called TabbedInterface.get_search_col\n"
            f"called TabbedInterface.find_items with args ({testobj.page}, 'qq')\n"
            "called TabbedInterface.init_search_buttons\n"
            f"called TabbedInterface.set_selected_keydef_item with args ({testobj.page}, 0)\n"
            "called EditorGui.statusbar_message with arg '2 found'\n")

    testobj.page.data = {1: 'a', 2: 'b', 3: 'c'}
    testobj.on_text_changed('qq')
    assert testobj.zoekcol == 1
    assert testobj.items_found == ['item-1', 'item-2']
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_search_col\n"
            "called TabbedInterface.get_search_col\n"
            f"called TabbedInterface.find_items with args ({testobj.page}, 'qq')\n"
            "called TabbedInterface.init_search_buttons\n"
            f"called TabbedInterface.set_selected_keydef_item with args ({testobj.page}, 0)\n"
            "called TabbedInterface.enable_search_buttons with args {'next': True, 'filter': True}\n"
            "called EditorGui.statusbar_message with arg '2 found'\n")

    testobj.page.captions = {'x': 'xxx', 'y': 'zzz'}
    testobj.gui.find_items = mock_find
    testobj.on_text_changed('qq')
    assert testobj.zoekcol == -1
    assert testobj.items_found == []
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_search_col\n"
            "called TabbedInterface.get_search_col\n"
            f"called TabbedInterface.find_items with args ({testobj.page}, 'qq')\n"
            "called TabbedInterface.init_search_buttons\n"
            "called EditorGui.statusbar_message with arg 'no qq'\n")

def test_choicebook_find_next(monkeypatch, capsys):
    """unittest for main.ChoiceBook.find_next
    """
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.page = MockHotkeyPanel(testobj, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
    testobj.parent.captions = {'I_NONXT': 'xxx'}
    testobj.items_found = ['x', 'y']
    testobj.founditem = 1
    testobj.find_next()
    assert testobj.founditem == 1
    assert capsys.readouterr().out == (
            "called TabbedInterface.enable_search_buttons with args {'prev': True}\n"
            "called EditorGui.statusbar_message with arg 'xxx'\n"
            "called TabbedInterface.enable_search_buttons with args {'next': False}\n")
    testobj.founditem = 0
    testobj.find_next()
    assert testobj.founditem == 1
    assert capsys.readouterr().out == (
            "called TabbedInterface.enable_search_buttons with args {'prev': True}\n"
            f"called TabbedInterface.set_selected_keydef_item with args ({testobj.page}, 1)\n")

def test_choicebook_find_prev(monkeypatch, capsys):
    """unittest for main.ChoiceBook.find_prev
    """
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.page = MockHotkeyPanel(testobj, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
    testobj.parent.captions = {'I_NOPRV': 'uuu'}
    testobj.items_found = ['x', 'y']
    testobj.founditem = 1
    testobj.find_prev()
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.enable_search_buttons with args {'next': True}\n"
            f"called TabbedInterface.set_selected_keydef_item with args ({testobj.page}, 0)\n")
    testobj.founditem = 0
    testobj.find_prev()
    assert testobj.founditem == 0
    assert capsys.readouterr().out == (
            "called TabbedInterface.enable_search_buttons with args {'next': True}\n"
            "called EditorGui.statusbar_message with arg 'uuu'\n"
            "called TabbedInterface.enable_search_buttons with args {'prev': False}\n")

def test_choicebook_filter(monkeypatch, capsys):
    """unittest for main.ChoiceBook.filter
    """
    def mock_get_filter_text():
        print("called TabbedInterface.get_filter_state_text")
        return 'on'
    def mock_get_filter_text_2():
        print("called TabbedInterface.get_filter_state_text")
        return 'off'
    def mock_get_search_text():
        print("called TabbedInterface.get_search_text")
        return 'this'
    def mock_get_pos():
        print("called TabbedInterface.get_found_keydef_position")
        return 2
    def mock_on_text(text):
        print(f"called ChoiceBook.on_text_changed with arg '{text}'")
    testobj = setup_choicebook(monkeypatch, capsys)
    testobj.page = MockHotkeyPanel(testobj, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj}, '')\n")
    testobj.parent.captions = {'C_FILTER': 'on', 'C_FLTOFF': 'off'}
    testobj.gui.get_filter_state_text = mock_get_filter_text
    testobj.gui.get_search_text = mock_get_search_text
    testobj.gui.get_found_keydef_position = mock_get_pos
    testobj.on_text_changed = mock_on_text
    testobj.zoekcol = 1
    testobj.page.data = {1: ['x', 'that'], 2: ['y', 'this'], 3: ['z', ''], 4: ['q', 'and this']}
    testobj.items_found = []
    testobj.filter()
    assert capsys.readouterr().out == ""
    testobj.items_found = ['x', 'y']
    testobj.filter()
    assert testobj.reposition == 2
    assert testobj.filter_on
    assert testobj.page.filtertext == 'this'
    assert testobj.page.olddata == {1: ['x', 'that'], 2: ['y', 'this'], 3: ['z', ''],
                                    4: ['q', 'and this']}
    assert testobj.page.data == {1: ['y', 'this'], 3: ['q', 'and this']}
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_filter_state_text\n"
            "called TabbedInterface.get_search_text\n"
            "called TabbedInterface.get_found_keydef_position\n"
            "called TabbedInterface.enable_search_buttons with args {'next': False, 'prev': False}\n"
            "called TabbedInterface.enable_search_text with arg False\n"
            "called HotkeyPanel.populate_list\n"
            "called TabbedInterface.set_found_keydef_position with args ()\n"
            "called TabbedInterface.set_filter_state_text with arg off\n")
    testobj.gui.get_filter_state_text = mock_get_filter_text_2
    testobj.filter()
    assert testobj.reposition == 2
    assert not testobj.filter_on
    assert testobj.page.filtertext == ''
    assert testobj.page.olddata == {1: ['x', 'that'], 2: ['y', 'this'], 3: ['z', ''],
                                    4: ['q', 'and this']}
    assert testobj.page.data == {1: ['x', 'that'], 2: ['y', 'this'], 3: ['z', ''],
                                 4: ['q', 'and this']}
    assert capsys.readouterr().out == (
            "called TabbedInterface.get_filter_state_text\n"
            "called TabbedInterface.get_search_text\n"
            "called TabbedInterface.get_found_keydef_position\n"
            "called TabbedInterface.enable_search_buttons with args {'next': True, 'prev': True}\n"
            "called TabbedInterface.enable_search_text with arg True\n"
            "called HotkeyPanel.populate_list\n"
            "called TabbedInterface.set_found_keydef_position with args ()\n"
            "called TabbedInterface.set_filter_state_text with arg on\n"
            "called ChoiceBook.on_text_changed with arg 'this'\n")


class MockGui:
    "stub for gui.Gui"
    def __init__(self, arg):
        print(f'called Gui.__init__ with arg {arg}')
    def set_window_title(self, text):
        """stub
        """
        print(f"called Gui.set_window_title with arg '{text}'")
    def statusbar_message(self, *args):
        """stub
        """
        print('called Gui.statusbar_message with args', args)
    def setup_tabs(self):
        """stub
        """
        print('called Gui.setup_tabs')
    def go(self):
        """stub
        """
        print('called Gui.go')
    def resize_empty_screen(self, *args):
        """stub
        """
        print('called Gui.resize_empty_screen with args', args)
    def close(self):
        """stub
        """
        print('called Gui.close')


class MockChoiceBook:
    "stub for main.ChoiceBook"
    def __init__(self, arg):
        print(f"called ChoiceBook.__init__ with arg '{arg}'")
        self.gui = MockTabGui()
    def on_page_changed(self, start):
        """stub
        """
        print(f"called ChoiceBook.on_page_changed with arg '{start}'")


def test_editor_init(monkeypatch, capsys):
    """unittest for main.Editor.init
    """
    def mock_save_log():
        print('called shared.save_log')
    def mock_read(arg):
        print(f"called read_settings with arg '{arg}'")
        return {'lang': 'en', 'title': '', 'initial': '', 'plugins': []}
    def mock_read_2(arg):
        print(f"called read_settings with arg '{arg}'")
        return {'lang': 'en', 'title': '', 'initial': 'y', 'plugins': [('x', 'xxx'), ('y', 'yyy')]}
    def mock_read_3(arg):
        print(f"called read_settings with arg '{arg}'")
        return {'lang': 'en', 'title': 'qqq', 'initial': 'x', 'plugins': [('x', 'xxx')]}
    def mock_readcaptions(self, arg):
        print(f"called Editor.readcaptions with arg '{arg}'")
        self.captions = {'T_MAIN': 'maintitle', 'T_HELLO': 'hello from {}'}
    def mock_show(self):
        print('called Editor.show_empty_screen')
    def mock_set(self):
        print('called Editor.setcaptions')
    monkeypatch.setattr(testee.shared, 'save_log', mock_save_log)
    monkeypatch.setattr(testee, 'read_settings', mock_read)
    monkeypatch.setattr(testee.Editor, 'show_empty_screen', mock_show)
    monkeypatch.setattr(testee.Editor, 'readcaptions', mock_readcaptions)
    monkeypatch.setattr(testee.gui, 'Gui', MockGui)
    monkeypatch.setattr(testee, 'ChoiceBook', MockChoiceBook)
    monkeypatch.setattr(testee.Editor, 'setcaptions', mock_set)
    monkeypatch.setattr(testee, 'CONF', 'mock_conf')
    monkeypatch.setattr(testee, 'BASE', testee.pathlib.Path('/confbase'))
    args = types.SimpleNamespace(conf='', start='')
    testobj = testee.Editor(args)
    assert testobj.ini == {'initial': '', 'lang': 'en', 'plugins': [], 'title': ''}
    assert testobj.pluginfiles == {}
    assert testobj.book is None
    assert isinstance(testobj.gui, testee.gui.Gui)
    assert capsys.readouterr().out == ("called shared.save_log\n"
                                       "called read_settings with arg 'mock_conf'\n"
                                       "called Editor.readcaptions with arg 'en'\n"
                                       f"called Gui.__init__ with arg {testobj}\n"
                                       "called Editor.show_empty_screen\n"
                                       "called Gui.go\n")
    monkeypatch.setattr(testee, 'read_settings', mock_read_2)
    args = types.SimpleNamespace(conf='other_conf', start='y')
    testobj = testee.Editor(args)
    assert testobj.ini == {'initial': 'y', 'lang': 'en', 'title': '', 'plugins': [('x', 'xxx'),
                                                                                  ('y', 'yyy')]}
    assert testobj.pluginfiles == {}
    assert isinstance(testobj.gui, testee.gui.Gui)
    assert isinstance(testobj.book, testee.ChoiceBook)
    assert capsys.readouterr().out == (
            "called shared.save_log\n"
            "called read_settings with arg '/confbase/other_conf'\n"
            "called Editor.readcaptions with arg 'en'\n"
            f"called Gui.__init__ with arg {testobj}\n"
            "called Gui.set_window_title with arg 'maintitle'\n"
            "called Gui.statusbar_message with args ('hello from maintitle',)\n"
            f"called ChoiceBook.__init__ with arg '{testobj}'\n"
            "called TabbedInterface.__init__ with args ()\n"
            "called Gui.setup_tabs\n"
            "called TabbedInterface.set_selected_tool with arg '1'\n"
            "called ChoiceBook.on_page_changed with arg '1'\n"
            "called Editor.setcaptions\n"
            "called Gui.go\n")
    monkeypatch.setattr(testee, 'read_settings', mock_read_3)
    args = types.SimpleNamespace(conf='/yet/another/conf', start='')
    testobj = testee.Editor(args)
    assert testobj.ini == {'initial': 'x', 'lang': 'en', 'title': 'qqq', 'plugins': [('x', 'xxx')]}
    assert testobj.pluginfiles == {}
    assert isinstance(testobj.gui, testee.gui.Gui)
    assert isinstance(testobj.book, testee.ChoiceBook)
    assert capsys.readouterr().out == (
            "called shared.save_log\n"
            "called read_settings with arg '/yet/another/conf'\n"
            "called Editor.readcaptions with arg 'en'\n"
            f"called Gui.__init__ with arg {testobj}\n"
            "called Gui.set_window_title with arg 'maintitle'\n"
            "called Gui.statusbar_message with args ('hello from maintitle',)\n"
            f"called ChoiceBook.__init__ with arg '{testobj}'\n"
            "called TabbedInterface.__init__ with args ()\n"
            "called Gui.setup_tabs\n"
            "called TabbedInterface.set_selected_tool with arg '0'\n"
            "called ChoiceBook.on_page_changed with arg '0'\n"
            "called Editor.setcaptions\n"
            "called Gui.go\n")

def setup_editor(monkeypatch, capsys):
    """stub for main.Editor
    """
    def mock_init(self):
        print('called Editor.__init__')
    monkeypatch.setattr(testee.Editor, '__init__', mock_init)
    testobj = testee.Editor()
    testobj.book = MockChoiceBook(testobj)
    testobj.gui = MockGui(testobj)
    assert capsys.readouterr().out == ('called Editor.__init__\n'
                                       f"called ChoiceBook.__init__ with arg '{testobj}'\n"
                                       'called TabbedInterface.__init__ with args ()\n'
                                       f'called Gui.__init__ with arg {testobj}\n')
    return testobj

def test_editor_show_empty_screen(monkeypatch, capsys):
    """unittest for main.Editor.show_empty_screen
    """
    class MockDummy:
        "stub for gui.DummyPage"
        def __init__(self, *args):
            print('called gui.DummyPage.__init__ with args', args)
    def mock_init(self):
        print('called Editor.__init__')
    monkeypatch.setattr(testee.Editor, '__init__', mock_init)
    monkeypatch.setattr(testee.gui, 'DummyPage', MockDummy)
    testobj = testee.Editor()
    testobj.gui = MockGui(testobj)
    assert capsys.readouterr().out == ('called Editor.__init__\n'
                                       f'called Gui.__init__ with arg {testobj}\n')
    testobj.captions = {'EMPTY_CONFIG_TEXT': 'Empty'}
    testobj.show_empty_screen()
    assert isinstance(testobj.book, testee.SimpleNamespace)
    assert isinstance(testobj.book.gui, testee.gui.DummyPage)
    assert isinstance(testobj.book.page, testee.SimpleNamespace)
    assert testobj.book.page.gui == testobj.book.gui
    assert capsys.readouterr().out == (
            f"called gui.DummyPage.__init__ with args ({testobj.gui}, 'Empty')\n"
            "called Gui.resize_empty_screen with args (640, 80)\n")

def test_editor_get_menudata(monkeypatch, capsys):
    """unittest for main.Editor.get_menudata
    """
    testobj = setup_editor(monkeypatch, capsys)
    menus = testobj.get_menudata()
    assert [x[0] for x in menus] == ['M_APP', 'M_TOOL', 'M_HELP']
    submenus = [x[1] for x in menus]
    assert [x[0] for x in submenus[0]] == ['M_SETT', 'M_EXIT']
    assert [x[0] for x in submenus[1]] == ['M_SETT2', 'M_READ', 'M_RBLD', 'M_SAVE']
    assert [x[0] for x in submenus[2]] == ['M_ABOUT']
    # subsubmenus = [x[1] for x in submenus[0]]
    # assert [x[0] for x in subsubmenus] == ['M_LOC', 'M_LANG', 'M_PREF']
    # subsubmenus = [x[1] for x in submenus[1]]
    # assert [x[0] for x in subsubmenus] == ['M_COL', 'M_MISC', 'M_ENTR']

def test_editor_m_read(monkeypatch, capsys):
    """unittest for main.Editor.m_read
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
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
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
            "called HotkeyPanel.populate_list\n")
    testobj.book.page.modified = True
    testobj.m_read()
    assert capsys.readouterr().out == ("called HotkeyPanel.readkeys\n"
                                       "called HotkeyPanel.populate_list\n")
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
    testobj.m_read()
    assert capsys.readouterr().out == ("called HotkeyPanel.readkeys\n"
                                       "called HotkeyPanel.populate_list\n")

def test_editor_m_save(monkeypatch, capsys):
    """unittest for main.Editor.m_save
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
    monkeypatch.setattr(testee.shared, 'log_exc', mock_log)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
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
            "called shared.log_exc\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_DEFSAV')\n")
    testobj.book.page.modified = True
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask)
    testobj.m_save(event=None)
    assert capsys.readouterr().out == (
            "called shared.log_exc\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_DEFSAV')\n")
    monkeypatch.setattr(testee.gui, 'ask_question', mock_ask_2)
    testobj.m_save(event=None)
    assert capsys.readouterr().out == (
            "called shared.log_exc\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_DEFSAV')\n")
    testobj.book.page.savekeys = mock_savekeys
    testobj.m_save(event=None)
    assert capsys.readouterr().out == (
            "called HotkeyPanel.savekeys\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_RSTRT')\n")

def test_editor_m_loc(monkeypatch, capsys):
    """unittest for main.Editor.m_loc
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
        print(f"called Editor.write_settings with arg '{name}'")
    def mock_clear(arg):
        print('called Editor.clear_book with arg {arg}')
        return []
    def mock_rebuild(*args):
        print('called Editor.rebuild_book with args', args)
        return []
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
    monkeypatch.setattr(testee, 'write_settings', mock_write)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.clear_book = mock_clear
    testobj.rebuild_book = mock_rebuild
    testobj.ini = {'plugins': [('p', 'q'), ('r', 's')]}
    testobj.m_loc()
    assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.FilesDialog})\n")
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_2)
    testobj.m_loc()
    assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.FilesDialog})\n"
            "called TabbedInterface.get_selected_index\n"
            "called Editor.write_settings with arg '{'plugins': [('x', 'y')]}'\n"
            "called Editor.clear_book with arg {arg}\n"
            "called Editor.rebuild_book with args (['p', 'r'], ['q', 's'], [])\n"
            "called TabbedInterface.set_selected_tool with arg '1'\n")
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show_3)
    testobj.ini = {'plugins': [('p', 'q'), ('r', 's')]}
    testobj.m_loc()
    assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.FilesDialog})\n"
            "called TabbedInterface.get_selected_index\n"
            "called Editor.write_settings with arg '{'plugins': [('x', 'y'), ('a', 'b')]}'\n"
            "called Editor.clear_book with arg {arg}\n"
            "called Editor.rebuild_book with args (['p', 'r'], ['q', 's'], [])\n"
            "called TabbedInterface.get_new_selection with arg 'last added'\n"
            "called TabbedInterface.set_selected_tool with arg '1'\n")

def test_editor_clear_book(monkeypatch, capsys):
    """unittest for main.Editor.clear_book
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.ini = {'plugins': [('p', 'q'), ('r', 's')]}
    testobj.pluginfiles = ['aaa', 'bbb', 'ccc']
    assert testobj.clear_book(['xxx', 'yyy', 'zzz']) == {'zzz': 'item #1', 'xxx': 'item #3'}
    assert testobj.pluginfiles == ['aaa', 'ccc']
    assert capsys.readouterr().out == (
            "called TabbedInterface.clear_selector\n"
            "called TabbedInterface.remove_tool with args (2, 'zzz', ['p', 'r'])\n"
            "called TabbedInterface.remove_tool with args (1, 'yyy', ['p', 'r'])\n"
            "called TabbedInterface.remove_tool with args (0, 'xxx', ['p', 'r'])\n")

def test_editor_rebuild_book(monkeypatch, capsys, tmp_path):
    """unittest for main.Editor.rebuild_book
    """
    monkeypatch.setattr(testee, 'HotkeyPanel', MockHotkeyPanel)
    testobj = setup_editor(monkeypatch, capsys)
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

def test_editor_accept_pathsettings(monkeypatch, capsys, tmp_path):
    """unittest for main.Editor.accept_pathsettings
    """
    def mock_write(data):
        print(f"called write_settings with arg '{data}'")
    def mock_update(*args):
        print('called update_paths with args', args)
        return []
    def mock_check(*args):
        print('called Editor.check_plugin_settings with args', args)
        return False
    def mock_check_2(*args):
        print('called Editor.check_plugin_settings with args', args)
        return True
    monkeypatch.setattr(testee, 'write_settings', mock_write)
    monkeypatch.setattr(testee, 'update_paths', mock_update)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.check_plugin_settings = mock_check

    testobj.last_added = 'xx'
    testobj.ini = {'lang': 'en'}
    testobj.accept_pathsettings([], {}, [])
    assert testobj.last_added == ''
    assert testobj.ini['plugins'] == []
    assert capsys.readouterr().out == "called update_paths with args ([], {}, 'en')\n"

    testobj.ini['startup'] = testee.shared.mode_f
    testobj.ini['initial'] = 'yy'
    testobj.ini['plugins'] = [('zz', 'path/to/zz')]
    testobj.pluginfiles = {}
    name_path_list = [('xx', 'path/to/xx')]
    settingsdata = {'xx': 'path/to/xx', 'zz': 'path/to/zz'}
    assert not testobj.accept_pathsettings(name_path_list, settingsdata, [])
    assert testobj.ini["startup"] == testee.shared.mode_r
    assert testobj.pluginfiles == {}
    assert capsys.readouterr().out == (
            "called write_settings with arg '{'lang': 'en', 'plugins': [('zz', 'path/to/zz')],"
            " 'startup': 'Remember', 'initial': 'yy'}'\n"
            "called Editor.check_plugin_settings with args ('xx', 'path/to/xx', 'path/to/xx')\n")

    testobj.check_plugin_settings = mock_check_2
    file_to_remove = tmp_path / 'obsolete'
    file_to_remove.touch()
    assert testobj.accept_pathsettings(name_path_list, settingsdata, [str(file_to_remove)])
    assert testobj.pluginfiles == {'xx': 'p'}
    assert testobj.ini['plugins'] == []
    assert capsys.readouterr().out == (
            "called Editor.check_plugin_settings with args ('xx', 'path/to/xx', 'path/to/xx')\n"
            "called update_paths with args ([('xx', 'path/to/xx')],"
            " {'xx': 'path/to/xx', 'zz': 'path/to/zz'}, 'en')\n")

def test_editor_check_plugin_settings(monkeypatch, capsys):
    """unittest for main.Editor.check_plugin_settings
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
    testobj = setup_editor(monkeypatch, capsys)
    testobj.captions = {'I_FILLALL': 'fillall error', 'I_NOKDEF': 'nokeydef error: {}',
                        'I_NOPLNAM': 'noplnam error: {}', 'I_NOPLREF': 'noplref error: {}'}
    assert not testobj.check_plugin_settings('pluginname', '', [])
    assert capsys.readouterr().out == (
           f"called gui.show_message with args ({testobj.gui},) {{'text': 'fillall error'}}\n")
    assert not testobj.check_plugin_settings('pluginname', 'datafilename', ('', ''))
    assert capsys.readouterr().out == (
            "called readjson with arg 'datafilename'\n"
            f"called gui.show_message with args ({testobj.gui},)"
            " {'text': 'nokeydef error: datafilename'}\n")
    assert not testobj.check_plugin_settings('pluginname', 'datafilename.csv', ('',))
    assert capsys.readouterr().out == (
            "called readjson with arg 'datafilename.csv'\n"
            f"called gui.show_message with args ({testobj.gui},)"
            " {'text': 'nokeydef error: datafilename.csv'}\n")
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

def test_editor_m_rebuild(monkeypatch, capsys):
    """unittest for main.Editor.m_rebuild
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
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
    assert capsys.readouterr().out == f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n"
    testobj.book.page.reader = MockReader()
    testobj.book.page.column_info = {'column': 'info'}
    testobj.ini = {'lang': 'en'}
    testobj.captions = {'I_RBLD': 'RBLD', 'I_NODEFS': 'NODEFS', 'I_NOEXTRA': 'NOEXTRA',
                        'I_NORBLD': 'NORBLD {}', 'I_ERRRBLD': 'ERRRBLD', 'I_#FOUND': '#FOUND {}'}
    testobj.book.page.settings = {}
    testobj.m_rebuild()
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_ADDSET') {{}}\n")
    testobj.book.page.settings = {'plugin': 'settings'}
    testobj.m_rebuild()
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_DEFRBLD') {{}}\n")
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
            "called HotkeyPanel.populate_list\n"
            f"called gui.show_message with args ({testobj.gui},) {{'text': 'RBLD'}}\n")

def test_editor_accept_pluginsettings(monkeypatch, capsys, tmp_path):
    """unittest for main.Editor.accept_pluginsettings
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
    testobj = setup_editor(monkeypatch, capsys)
    assert not testobj.accept_pluginsettings('', 'ploc', 'title', '0', '1', '0')
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_NEEDNAME') {{}}\n")
    clocpath.touch()
    assert not testobj.accept_pluginsettings(str(clocpath), 'ploc', 'title', '0', '1', '0')
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_GOTSETFIL')"
            f" {{'args': ['{clocpath}']}}\n")
    clocpath.unlink()
    # breakpoint()
    assert not testobj.accept_pluginsettings(str(clocpath), 'ploc', 'title', '0', '1', '0')
    assert capsys.readouterr().out == (
            "called importlib.util.find_spec with arg 'ploc'\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_GOTPLGFIL')"
            f" {{'args': ['ploc']}}\n")
    monkeypatch.setattr(testee.importlib.util, 'find_spec', mock_find_2)
    assert testobj.accept_pluginsettings(str(clocpath), 'ploc', 'title', '0', '1', '0')
    assert testobj.gui.data == [f'{clocpath}', 'ploc', 'title', 0, 1, 0]
    assert capsys.readouterr().out == "called importlib.util.find_spec with arg 'ploc'\n"

def test_editor_m_tool(monkeypatch, capsys):
    """unittest for main.Editor.m_tool
    """
    def mock_show(*args):
        print('called gui.show_dialog with args', args)
        return False
    def mock_show_2(*args):
        print('called gui.show_dialog with args', args)
        win = args[0]
        win.book.page.pad = 'path/to/data.json'
        win.book.page.settings = {testee.shared.SettType.RDEF.value: 1,
                                  testee.shared.SettType.DETS.value: 1,
                                  testee.shared.SettType.RBLD.value: 1}
        win.book.page.column_info = ['x']
        win.book.page.data = {1: ['y', 'z']}
        win.book.page.otherstuff = {'a': {'b': 'c'}}
        return True
    def mock_writejson(*args):
        print('called writejson with args', args)
    def mock_modify(*args):
        print('called SingleDataInterface.modify_menu_item with args', args)
    def mock_get_panel():
        print("called TabbedInterface.get_selected_panel")
        return 2, 'oldwin'
    def mock_replace(*args):
        print("called TabbedInterface.replace_panel with args", args)
    def mock_set_editable(value):
        print(f"called TabbedInterface.set_panel_editable with arg {value}")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
    monkeypatch.setattr(testee, 'HotkeyPanel', MockHotkeyPanel)
    monkeypatch.setattr(testee, 'writejson', mock_writejson)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.ini = {'plugins': [('a', 'aaa'), ('b', 'bbb'), ('c', 'ccc')]}
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
    testobj.book.page.settings = {testee.shared.SettType.RDEF.value: 0}
    testobj.book.page.has_extrapanel = False
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
            " {'RedefineKeys': 1, 'ShowDetails': 1, 'RebuildData': 1},"
            " ['x'], {1: ['y', 'z']}, {'a': {'b': 'c'}})\n"
            "called SingleDataInterface.modify_menu_item with args ('M_SAVE', True)\n"
            "called SingleDataInterface.modify_menu_item with args ('M_RBLD', True)\n"
            "called TabbedInterface.get_selected_panel\n"
            f"called HotkeyPanel.__init__ with args ({testobj.book}, 'ccc')\n"
            "called TabbedInterface.replace_panel with args (2, 'oldwin', 'HotkeyPanelGui')\n")
    # testobj.book.page.settings = {testee.shared.SettType.RDEF.value: 1}
    testobj.book.page.settings = {}
    testobj.book.page.has_extrapanel = True
    # breakpoint()
    testobj.m_tool()
    assert testobj.book.page.has_extrapanel
    assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.ExtraSettingsDialog})\n"
            f"called writejson with args ('path/to/data.json', {testobj.book.page.reader},"
            " {'RedefineKeys': 1, 'ShowDetails': 1, 'RebuildData': 1},"
            " ['x'], {1: ['y', 'z']}, {'a': {'b': 'c'}})\n"
            "called SingleDataInterface.modify_menu_item with args ('M_SAVE', True)\n"
            "called SingleDataInterface.modify_menu_item with args ('M_RBLD', True)\n"
            "called TabbedInterface.get_selected_panel\n"
            "called TabbedInterface.set_panel_editable with arg True\n")

def test_editor_accept_extrasettings(monkeypatch, capsys):
    """unittest for main.Editor.accept_extrasettings
    """
    def mock_show(*args, **kwargs):
        print('called gui.show_message with args', args, kwargs)
    def mock_add():
        pass
    def mock_remove():
        print('called Editor.remove_custom_settings')
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    testobj = setup_editor(monkeypatch, capsys)
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
                                          'RebuildData': '1',
                                          'ShowDetails': '1',
                                          'RedefineKeys': '1',
                                          'name': 'value',
                                          'extra': {'name': 'desc'}}
    assert capsys.readouterr().out == ("called HotkeyPanel.set_title\n"
                                       "called Editor.remove_custom_settings\n")
    testobj.book.page.title = 'title'
    testobj.book.page.settings = {}
    testobj.accept_extrasettings('program', 'title', False, False, False, [])
    assert testobj.book.page.settings == {'PluginName': 'program',
                                          'PanelName': 'title',
                                          'RebuildData': '0',
                                          'ShowDetails': '0',
                                          'RedefineKeys': '0',
                                          'extra': {}}
    assert capsys.readouterr().out == ("called Editor.remove_custom_settings\n")

def test_editor_remove_custom_settings(monkeypatch, capsys):
    """unittest for main.Editor.remove_custom_settings
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
    testobj.book.page.settings = {'xxx': 'aaaaaaa', 'yyy': 'bbbbbbb', 'zzz': 'ccccccc'}
    monkeypatch.setattr(testee.shared, 'settingnames', ['xxx', 'zzz'])
    testobj.remove_custom_settings()
    assert testobj.book.page.settings == {'xxx': 'aaaaaaa', 'zzz': 'ccccccc'}

def test_editor_m_col(monkeypatch, capsys):
    """unittest for main.Editor.m_col
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

    testobj = setup_editor(monkeypatch, capsys)
    testobj.ini = {'lang': 'en'}
    testobj.build_new_pagedata = mock_build
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
    testobj.book.page.gui = MockSDI()
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n"
            "called SingleDataInterface.__init__ with args ()\n")

    testobj.book.page.settings = {}
    testobj.book.page.column_info = [('xx', 10, False)]
    testobj.book.page.new_column_info = [('xx', 10, False, 0)]
    testobj.book.page.otherstuff = {'other': 'stuff'}
    testobj.book.page.pad = 'testfile.json'
    testobj.m_col()
    assert capsys.readouterr().out == (
            f"called Editor.read_columntitledata with arg '{testobj}'\n"
            f"called gui.show_message with args ({testobj.gui}, 'I_ADDSET') {{}}\n")
    testobj.book.page.settings = {'page': 'settings'}
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
    testobj.book.page.new_column_info = [('xx', 10, False, 0), ('yy', 15, False, 1)]
    testobj.captions = {'xx': 'aaa', 'yy': 'bbb'}
    testobj.book.page.settings = {'page': 'settings'}
    testobj.book.page.reader = MockReader()
    testobj.m_col()
    assert testobj.book.page.column_info == [('xx', 10, False), ('yy', 15, False)]
    assert capsys.readouterr().out == (
            f"called Editor.read_columntitledata with arg '{testobj}'\n"
            f"called gui.show_dialog with args ({testobj}, {testee.gui.ColumnSettingsDialog})\n"
            "called Editor.build_new_pagedata\n"
            f"called writejson with args ('testfile.json', {testobj.book.page.reader},"
            " {'page': 'settings'},"
            " [('xx', 10, False), ('yy', 15, False)], None, {'other': 'stuff'})\n"
            "called SingleDataInterface.update_colums with args (1, 2)\n"
            "called TabbedInterface.refresh_locs with arg '['aaa', 'bbb']'\n"
            "called SingleDataInterface.refresh_headers with arg ['aaa', 'bbb']\n"
            "called HotkeyPanel.populate_list\n")

def test_editor_build_new_pagedata(monkeypatch, capsys):
    """unittest for main.Editor.build_new_pagedata
    """
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
    testobj.book.page.data = {'qq': ['aa', 1, 'X'], 'rr': ['bb', 2, 'Z']}
    testobj.book.page.column_info = [('xx', 10, False, 0), ('zz', 12, False, 'new'),
                                     ('yy', 15, False, 1)]
    assert testobj.build_new_pagedata() == {'qq': ['aa', '', 1], 'rr': ['bb', '', 2]}

def test_editor_accept_columnsettings(monkeypatch, capsys):
    """unittest for main.Editor.accept_columnsettings
    """
    def mock_show(*args, **kwargs):
        print('called gui.show_message with args', args, kwargs)
    def mock_build(*args):
        print('called Editor.build_new_title_data with args', args)
        return True, [], []  # canceled
    def mock_build_2(*args):
        print('called Editor.build_new_title_data with args', args)
        return False, [('ID1', 'title1'), ('ID2', 'title2')], ['col', 'info']  # continue
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = MockHotkeyPanel(testobj.book, '')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj.book}, '')\n")
    testobj.captions = {}
    testobj.book.page.captions = {}
    testobj.build_new_title_data = mock_build
    data = [('x', 'a', 0), ('y', 'b', 1), ('x', 'c', 2)]
    assert testobj.accept_columnsettings(data) == (False, False)
    assert testobj.captions == {}
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_DPLNAM') {{}}\n")
    data = [('x', 'a', 0), ('y', 'b', 1), ('', 'c', 2)]
    assert testobj.accept_columnsettings(data) == (False, False)
    assert testobj.captions == {}
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_MISSNAM') {{}}\n")
    data = [('x', 'a', 0), ('y', 'b', 2), ('z', 'c', 2)]
    assert testobj.accept_columnsettings(data) == (False, False)
    assert testobj.captions == {}
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_DPLCOL') {{}}\n")
    data = [('x', 'a', 0, False, 0), ('y', 'b', 2, False, 1), ('z', 'c', 3, False, 2, ),
            ('q', 'd', 1, False, 'new')]
    testobj.col_names = ['x', 'y', 'z']
    testobj.col_textids = ['xxx', 'yyy', 'zzz']
    assert testobj.accept_columnsettings(data) == (False, True)
    assert testobj.captions == {}
    assert capsys.readouterr().out == (
            "called Editor.build_new_title_data with args (['q'], [['xxx', 'a', False, 0],"
            " ['q', 'd', False, 'new'], ['yyy', 'b', False, 1], ['zzz', 'c', False, 2]])\n")
    testobj.captions = {}
    testobj.build_new_title_data = mock_build_2
    assert testobj.accept_columnsettings(data) == (True, False)
    assert testobj.book.page.new_column_info == ['col', 'info']
    assert testobj.captions == {'ID1': 'title1', 'ID2': 'title2'}
    assert testobj.book.page.captions == {'ID1': 'title1', 'ID2': 'title2'}
    assert capsys.readouterr().out == (
            "called Editor.build_new_title_data with args (['q'], [['xxx', 'a', False, 0],"
            " ['q', 'd', False, 'new'], ['yyy', 'b', False, 1], ['zzz', 'c', False, 2]])\n")

def test_editor_build_new_title_data(monkeypatch, capsys, tmp_path):
    """unittest for main.Editor.build_new_title_data
    """
    def mock_show(*args):
        print('called gui.show_dialog with args', args)
        return False
    def mock_show_2(*args):
        print('called gui.show_dialog with args', args)
        args[0].dialog_data = {'en.lng': {'C_NEW1': 'xxx_nl', 'C_NEW2': 'yyy_nl'},
                               'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}}
        return True
    def mock_add(*args):
        print('called add_columntitledata with args', args)
    monkeypatch.setattr(testee.shared, 'HERELANG', tmp_path)
    (tmp_path / 'en.lng').touch()
    (tmp_path / 'nl.lng').touch()
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_show)
    monkeypatch.setattr(testee, 'add_columntitledata', mock_add)
    testobj = setup_editor(monkeypatch, capsys)
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
    assert title_list == [('C_NEW1', 'xxx_nl'), ('C_NEW2', 'yyy_nl')]
    assert column_info == [['C_NEW1', 10, False], ['C_NEW2', 10, False]]
    assert testobj.dialog_data == {'en.lng': {'C_NEW1': 'xxx_nl', 'C_NEW2': 'yyy_nl'},
                                   'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}}
    assert capsys.readouterr().out == (
            f"called gui.show_dialog with args ({testobj}, {testee.gui.NewColumnsDialog})\n"
            "called add_columntitledata with args ({'en.lng': {'C_NEW1': 'xxx_nl',"
            " 'C_NEW2': 'yyy_nl'}, 'nl.lng': {'C_NEW1': 'xxx_en', 'C_NEW2': 'yyy_en'}},)\n")

def test_editor_accept_newcolumns(monkeypatch, capsys, tmp_path):
    """unittest for main.Editor.accept_newcolumns
    """
    def mock_show(*args, **kwargs):
        print('called gui.show_message with args', args, kwargs)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    monkeypatch.setattr(testee.shared, 'HERELANG', tmp_path)
    (tmp_path / 'en.lng').write_text('# symbols\n\nC_SYM1  symbol1\nC_SYM2  symbol 2\n')
    testobj = setup_editor(monkeypatch, capsys)
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

def test_editor_m_entry(monkeypatch, capsys):
    """unittest for main.Editor.m_entry
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
    testobj = setup_editor(monkeypatch, capsys)
    testobj.ini = {'lang': 'en'}
    testobj.book.page = MockHotkeyPanel(testobj.book, 'xxx')
    assert capsys.readouterr().out == (
            f"called HotkeyPanel.__init__ with args ({testobj.book}, 'xxx')\n")
    testobj.book.page.settings = {}
    testobj.book.page.column_info = [('column', 'info')]
    testobj.book.page.data = {}
    testobj.book.page.otherstuff = {'other': 'stuff'}
    testobj.book.page.pad = 'settings.json'
    testobj.m_entry()
    assert capsys.readouterr().out == (
            f"called gui.show_message with args ({testobj.gui}, 'I_ADDCOL')\n")

    testobj.book.page.settings = {'x': 'y'}
    testobj.book.page.colums_info = []
    testobj.m_entry()
    assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj},"
                                       " <class 'editor.dialogs_qt.EntryDialog'>)\n")

    testobj.book.page.settings = {'x': 'y'}
    testobj.book.page.colums_info = [('column', 'info')]
    testobj.m_entry()
    assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj},"
                                       " <class 'editor.dialogs_qt.EntryDialog'>)\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
    testobj.m_entry()
    assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj},"
                                       " <class 'editor.dialogs_qt.EntryDialog'>)\n")

    testobj.book.page.data = {'a': 'b'}
    testobj.book.page.reader = MockReader()
    testobj.m_entry()
    assert capsys.readouterr().out == (f"called gui.show_dialog with args ({testobj},"
                                       " <class 'editor.dialogs_qt.EntryDialog'>)\n"
                                       "called writejson with args ('settings.json',"
                                       f" {testobj.book.page.reader},"
                                       " {'x': 'y'}, [('column', 'info')], {'a': 'b'},"
                                       " {'other': 'stuff'})\n"
                                       "called HotkeyPanel.populate_list\n")

def test_editor_m_lang(monkeypatch, capsys, tmp_path):
    """unittest for main.Editor.m_lang
    """
    def mock_choice(*args, **kwargs):
        print('called gui.get_choice with args', args, kwargs)
        return '', False
    def mock_choice_2(*args, **kwargs):
        print('called gui.get_choice with args', args, kwargs)
        return 'xx', True
    def mock_write(arg):
        print(f"called write_settings with arg '{arg}'")
    def mock_read(arg):
        print(f"called Editor.readcaptions with arg '{arg}'")
    def mock_set():
        print("called Editor.setcaptions")
    monkeypatch.setattr(testee, 'write_settings', mock_write)
    monkeypatch.setattr(testee.gui, 'get_choice', mock_choice)
    langdir = tmp_path
    (langdir / 'en.lng').touch()
    (langdir / 'nl.lng').touch()
    monkeypatch.setattr(testee.shared, 'HERELANG', langdir)
    testobj = setup_editor(monkeypatch, capsys)
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
            "called write_settings with arg '{'lang': 'xx'}'\n"
            "called Editor.readcaptions with arg 'xx'\n"
            "called Editor.setcaptions\n")

def test_editor_m_about(monkeypatch, capsys):
    """unittest for main.Editor.m_about
    """
    def mock_show(*args, **kwargs):
        print('called gui.show_message with args', args, kwargs)
    monkeypatch.setattr(testee.gui, 'show_message', mock_show)
    monkeypatch.setattr(testee, 'VRS', 'xxx')
    monkeypatch.setattr(testee, 'AUTH', 'yyy')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.captions = {'T_ABOUT': '{} / versie {} / {} / {}', 'T_SHORT': 'this',
                        'T_LONG': 'more text'}
    testobj.m_about()
    assert capsys.readouterr().out == (
            "called gui.show_message with args"
            f" ({testobj.gui},) {{'text': 'this\\nversie xxx\\nyyy\\nmore text'}}\n")

def test_editor_m_pref(monkeypatch, capsys):
    """unittest for main.Editor.m_pref
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
    def mock_write(arg):
        print(f"called write_settings with arg '{arg}'")
    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog)
    monkeypatch.setattr(testee, 'write_settings', mock_write)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
    # testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Remember'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings with arg"
            " '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_3)
    testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings with arg"
            " '{'startup': 'Fixed', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_4)
    testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Remember'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings with arg"
            " '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_5)
    testobj.ini = {'startup': 'Fixed', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'changed'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings with arg"
            " '{'startup': 'Fixed', 'initial': 'changed'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_2)
    testobj.ini = {'startup': 'Remember', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Remember'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings with arg"
            " '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_3)
    testobj.ini = {'startup': 'Remember', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings with arg"
            " '{'startup': 'Fixed', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_4)
    testobj.ini = {'startup': 'Remember', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Remember'
    assert testobj.ini['initial'] == 'unchanged'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings with arg"
            " '{'startup': 'Remember', 'initial': 'unchanged'}'\n")

    monkeypatch.setattr(testee.gui, 'show_dialog', mock_dialog_5)
    testobj.ini = {'startup': 'Remember', 'initial': 'unchanged'}
    testobj.m_pref()
    assert testobj.ini['startup'] == 'Fixed'
    assert testobj.ini['initial'] == 'changed'
    assert capsys.readouterr().out == (
            "called gui.show_dialog with args"
            f" ({testobj}, <class 'editor.dialogs_qt.InitialToolDialog'>)\n"
            "called write_settings with arg"
            " '{'startup': 'Fixed', 'initial': 'changed'}'\n")

def test_editor_accept_startupsettings(monkeypatch, capsys):
    """unittest for main.Editor.accept_startupsettings
    """
    monkeypatch.setattr(testee.shared, 'mode_f', 'fixed')
    monkeypatch.setattr(testee.shared, 'mode_r', 'remember')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.accept_startupsettings(True, False, 'xxx')
    assert testobj.prefs == ('fixed', 'xxx')
    testobj.accept_startupsettings(False, True, 'yyy')
    assert testobj.prefs == ('remember', 'yyy')
    testobj.accept_startupsettings(True, True, 'zzz')
    assert testobj.prefs == ('fixed', 'zzz')
    testobj.accept_startupsettings(False, False, 'qqq')
    assert testobj.prefs == (None, 'qqq')

def test_editor_m_exit(monkeypatch, capsys):
    """unittest for main.Editor.m_exit
    """
    def mock_exit():
        print('called Editor.exit')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.exit = mock_exit
    testobj.m_exit()
    assert capsys.readouterr().out == 'called Editor.exit\n'

def test_editor_exit(monkeypatch, capsys):
    """unittest for main.Editor.exit
    """
    def mock_exit():
        print('called HotkeyPanel.exit')
        return False
    def mock_exit_2():
        print('called HotkeyPanel.exit')
        return True
    def mock_write(*args, **kwargs):
        print('called write_settings with args', args, kwargs)
    def mock_get():
        print('called SingledataInterface.get_selected_text')
        return 'xxx'
    monkeypatch.setattr(testee.shared, 'mode_f', 'fixed')
    monkeypatch.setattr(testee.shared, 'mode_r', 'remember')
    monkeypatch.setattr(testee, 'write_settings', mock_write)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.book.page = types.SimpleNamespace(exit=mock_exit)
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
    testobj.book.gui.get_selected_text = mock_get
    testobj.exit()
    assert testobj.ini['initial'] == 'xxx'
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                       "called SingledataInterface.get_selected_text\n"
                                       "called write_settings with args"
                                       " ({'startup': 'remember', 'initial': 'xxx'},)"
                                       " {'nobackup': True}\n"
                                       "called Gui.close\n")
    testobj.ini = {'startup': 'remember', 'initial': 'yyy'}
    testobj.book.gui.get_selected_text = mock_get
    testobj.exit()
    assert testobj.ini['initial'] == 'xxx'
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                       "called SingledataInterface.get_selected_text\n"
                                       "called write_settings with args"
                                       " ({'startup': 'remember', 'initial': 'xxx'},)"
                                       " {'nobackup': True}\n"
                                       "called Gui.close\n")
    testobj.ini = {'startup': 'remember', 'initial': 'yyy'}
    testobj.book.gui = MockTabGui()
    assert capsys.readouterr().out == "called TabbedInterface.__init__ with args ()\n"
    testobj.exit()
    assert testobj.ini['initial'] == 'yyy'
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                       "called Gui.close\n")
    testobj.ini = {'startup': 'fixed'}
    testobj.exit()
    assert testobj.ini == {'startup': 'fixed'}
    assert capsys.readouterr().out == ("called HotkeyPanel.exit\n"
                                       "called Gui.close\n")

def test_editor_change_setting(monkeypatch, capsys, tmp_path):
    """unittest for main.Editor.change_setting
    """
    ininame = tmp_path / 'mock_ini'
    ininame.touch()
    bakname = ininame.with_suffix('.bak')
    testobj = setup_editor(monkeypatch, capsys)
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

def test_editor_readcaptions(monkeypatch, capsys):
    """unittest for main.Editor.readcaptions
    """
    def mock_read(lang):
        print(f"called readlang with arg '{lang}'")
        return {'captions': 'dict'}
    monkeypatch.setattr(testee, 'readlang', mock_read)
    testobj = setup_editor(monkeypatch, capsys)
    testobj.readcaptions('en')
    assert testobj.captions == {'captions': 'dict'}
    assert testobj.last_textid == ''


def test_editor_setcaptions(monkeypatch, capsys):
    """unittest for main.Editor.setcaptions
    """
    def mock_set():
        print('called EditorGui.setcaptions')
    def mock_set2():
        print('called TabbedInterface.setcaptions')
    def mock_set3():
        print('called HotkeyPanel.setcaptions')
    testobj = setup_editor(monkeypatch, capsys)
    testobj.gui.setcaptions = mock_set
    testobj.book.gui.setcaptions = mock_set2
    testobj.book.page = types.SimpleNamespace(setcaptions=mock_set3)
    testobj.setcaptions()
    assert capsys.readouterr().out == ("called EditorGui.setcaptions\n"
                                       "called TabbedInterface.setcaptions\n"
                                       "called HotkeyPanel.setcaptions\n")
